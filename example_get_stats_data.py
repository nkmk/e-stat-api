import urllib.request
import urllib.parse
import json

with open('setting/get_stats_data_sample.json') as f:
    print(f.read())
# {
#     "statsDataId": "0003215840"
# }

with open('setting/get_stats_data_sample.json') as f:
    p = json.load(f)

with open('setting/app_id.json') as f:
    p_id = json.load(f)

p.update(p_id)

url = ('http://api.e-stat.go.jp/rest/2.1/app/getSimpleStatsData?'
       + urllib.parse.urlencode(p))

with urllib.request.urlopen(url) as response:
    data = response.read()

print(type(data))
# <class 'bytes'>

with open('download/stats_data_{}_header.csv'.format(p['statsDataId']), 'w') as f:
    f.writelines(data.decode())

p['sectionHeaderFlg'] = 2

url = ('http://api.e-stat.go.jp/rest/2.1/app/getSimpleStatsData?'
       + urllib.parse.urlencode(p))

with urllib.request.urlopen(url) as response:
    data = response.read()

with open('download/stats_data_{}.csv'.format(p['statsDataId']), 'w') as f:
    f.writelines(data.decode().split('\n', 1)[1])
