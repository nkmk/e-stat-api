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


def get_list(param, form='json'):
    if form == 'xml':
        url = 'http://api.e-stat.go.jp/rest/2.1/app/getStatsList?'
    else:  # json
        url = 'http://api.e-stat.go.jp/rest/2.1/app/json/getStatsList?'
    return get_api_return_val(param, url).decode()


def get_list_table_inf(param):
    d = json.loads(get_list(param, 'json'))
    return d['GET_STATS_LIST']['DATALIST_INF']['TABLE_INF']


def save_list(param, dir_path='.', filename='stats_list', form='csv',
              replace=True, sep='_', atmark='', dollar='val', **kwargs):
    path = os.path.join(dir_path, filename + '.' + form)

    if form == 'csv':
        l = get_list_table_inf(param)
        if replace:
            df = pd.io.json.json_normalize(l, sep=sep)
            df.columns = [s.replace('@', atmark).replace('$', dollar)
                          for s in df.columns]
            df.to_csv(path, index=False)
        else:
            pd.io.json.json_normalize(l).to_csv(path, index=False)
    elif form == 'json':
        d = json.loads(get_list(param, 'json'))
        with open(path, 'w') as f:
            json.dump(d, f, **kwargs)
    else:  # xml
        with open(path, 'w') as f:
            f.write(get_list(param, form))


def get_data(param, form='csv'):
    if form == 'csv':
        url = 'http://api.e-stat.go.jp/rest/2.1/app/getSimpleStatsData?'
    elif form == 'xml':
        url = 'http://api.e-stat.go.jp/rest/2.1/app/getStatsData?'
    else:  # json
        url = 'http://api.e-stat.go.jp/rest/2.1/app/json/getStatsData?'
    return get_api_return_val(param, url).decode()


def save_data(param, stats_data_id=None, dir_path='.', filename=None,
              form='csv', section_header=False, skip=True, **kwargs):
    p = param.copy()
    if stats_data_id:
        p['statsDataId'] = stats_data_id

    if not filename:
        filename = p['statsDataId']

    path = os.path.join(dir_path, filename + '.' + form)

    if section_header:
        p['sectionHeaderFlg'] = 1
    else:
        p['sectionHeaderFlg'] = 2

    if os.path.exists(path) & skip:
        print('skip {} ({} already exists)'.format(p['statsDataId'], path))
    else:
        print('download {} to {}'.format(p['statsDataId'], path))
        data = get_data(p, form)
        if form == 'json':
            d = json.loads(data)
            with open(path, 'w') as f:
                json.dump(d, f, **kwargs)
        else:  # csv, xml
            if form == 'csv' and not section_header:
                data = data.split('\n', 1)[1]
            with open(path, 'w') as f:
                f.write(data)


def save_data_multi(param, ids, dir_path='.', filename_words=None, sep='_',
                    form='csv', section_header=False, skip=True,
                    interval_time_sec=1, **kwargs):
    if filename_words:
        for i, *words in zip(ids, *filename_words):
            time.sleep(interval_time_sec)
            save_data(param, i, dir_path,
                      sep.join([str(word) for word in words]),
                      form, section_header, skip, **kwargs)
    else:
        for i in ids:
            time.sleep(interval_time_sec)
            save_data(param, i, dir_path, i,
                      form, section_header, skip, **kwargs)


def save_data_multi_direct(param_list, param_data, param_id=None,
                           dir_path='.', filename_words=None, sep='_',
                           form='csv', section_header=False, skip=True,
                           interval_time_sec=1, **kwargs):
    p_list = param_list.copy()
    p_data = param_data.copy()

    if param_id:
        p_list.update(param_id)
        p_data.update(param_id)

    l = get_list_table_inf(p_list)
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

    save_data_multi(p_data, ids, dir_path, fws, sep,
                    form, section_header, skip, interval_time_sec, **kwargs)
