import urllib.request
import urllib.parse
import json

with open('setting/get_stats_list_sample.json') as f:
    p = json.load(f)

with open('setting/app_id.json') as f:
    p_id = json.load(f)

p.update(p_id)

url = ('http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsList?'
       + urllib.parse.urlencode(p))

with urllib.request.urlopen(url) as response:
    data = response.read()

data_str = data.decode()

filename = 'download/stats_list_{}_{}_ver3.0_header.csv'.format(p['statsCode'], p["surveyYears"])

with open(filename, 'w') as f:
    f.write(data_str)

data_str_without_header = data_str.split('\n', 8)[-1]

filename = 'download/stats_list_{}_{}_ver3.0.csv'.format(p['statsCode'], p["surveyYears"])

with open(filename, 'w') as f:
    f.write(data_str_without_header)
