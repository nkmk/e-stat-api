import json
import os
import time
import urllib.parse
import urllib.request

import pandas as pd


def get_api_return_val(param, url):
    url += urllib.parse.urlencode(param)
    with urllib.request.urlopen(url) as response:
        return response.read()


def get_list(param):
    url = 'http://api.e-stat.go.jp/rest/2.1/app/json/getStatsList?'
    d = json.loads(get_api_return_val(param, url))
    return d['GET_STATS_LIST']['DATALIST_INF']['TABLE_INF']


def save_list_csv(param, path, replace=True, sep='_', atmark='', dollar='val'):
    l = get_list(param)
    if replace:
        df = pd.io.json.json_normalize(l, sep=sep)
        df.columns = [s.replace('@', atmark).replace('$', dollar)
                      for s in df.columns]
        df.to_csv(path, index=False)
    else:
        pd.io.json.json_normalize(l).to_csv(path, index=False)


def get_data_csv(param):
    url = 'http://api.e-stat.go.jp/rest/2.1/app/getSimpleStatsData?'
    return get_api_return_val(param, url)


def save_data_csv(param, stats_data_id=None, dir_path='.', filename=None,
                  section_header=False, skip=True):
    if stats_data_id:
        param['statsDataId'] = stats_data_id

    if not filename:
        filename = param['statsDataId']

    path = os.path.join(dir_path, filename + '.csv')

    if section_header:
        param['sectionHeaderFlg'] = 1
        del_first_line = False
    else:
        param['sectionHeaderFlg'] = 2
        del_first_line = True

    if os.path.exists(path) & skip:
        print('skip {} ({} already exists)'.format(param['statsDataId'], path))
    else:
        print('download {} to {}'.format(param['statsDataId'], path))
        data = get_data_csv(param).decode()
        with open(path, 'w') as f:
            if del_first_line:
                f.write(data.split('\n', 1)[1])
            else:
                f.write(data)


def save_data_csv_multi(param, ids, dir_path='.', filename_words=None, sep='_',
                        section_header=False, skip=True, interval_time_sec=1):
    if filename_words:
        for i, *words in zip(ids, *filename_words):
            time.sleep(interval_time_sec)
            save_data_csv(param, i, dir_path,
                          sep.join([str(word) for word in words]),
                          section_header, skip)
    else:
        for i in ids:
            time.sleep(interval_time_sec)
            save_data_csv(param, i, dir_path, i, section_header, skip)


def save_data_csv_multi_direct(param_list, param_data, param_id,
                               dir_path='.', filename_words=None, sep='_',
                               section_header=False, skip=True,
                               interval_time_sec=1):
    param_list.update(param_id)
    param_data.update(param_id)

    l = get_list(param_list)
    ids = [d['@id'] for d in l]

    if filename_words:
        fws = []
        keys = l[0].keys()
        n = len(ids)
        for word in filename_words:
            if type(word) == list:
                if word[0] in keys:
                    fws.append([d[word[0]].get(word[1]) for d in l])
                else:
                    fws.append([word[0]] * n)
            elif word in keys:
                fws.append([d[word] for d in l])
            else:
                fws.append([word] * n)

    save_data_csv_multi(param_data, ids, dir_path, fws, sep,
                        section_header, skip, interval_time_sec)
