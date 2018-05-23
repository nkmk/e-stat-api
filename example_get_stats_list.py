import urllib.request
import urllib.parse
import json
import pandas as pd
import pprint

with open('setting/get_stats_list_sample.json') as f:
    print(f.read())
# {
#     "statsCode": "00200524",
#     "surveyYears": "2017"
# }

with open('setting/get_stats_list_sample.json') as f:
    p = json.load(f)

print(p)
# {'statsCode': '00200524', 'surveyYears': '2017'}

print(type(p))
# <class 'dict'>

with open('setting/app_id_sample.json') as f:
    print(f.read())
# {
#     "appId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# }

with open('setting/app_id.json') as f:
    p_id = json.load(f)

p.update(p_id)

url = ('http://api.e-stat.go.jp/rest/2.1/app/json/getStatsList?'
       + urllib.parse.urlencode(p))

with urllib.request.urlopen(url) as response:
    data = response.read()

print(type(data))
# <class 'bytes'>

d = json.loads(data)

pprint.pprint(d, depth=3)
# {'GET_STATS_LIST': {'DATALIST_INF': {'NUMBER': 21,
#                                      'RESULT_INF': {...},
#                                      'TABLE_INF': [...]},
#                     'PARAMETER': {'DATA_FORMAT': 'J',
#                                   'LANG': 'J',
#                                   'STATS_CODE': '00200524',
#                                   'SURVEY_YEARS': 2017},
#                     'RESULT': {'DATE': '2018-05-23T22:28:58.392+09:00',
#                                'ERROR_MSG': '正常に終了しました。',
#                                'STATUS': 0}}}

table_info_list = d['GET_STATS_LIST']['DATALIST_INF']['TABLE_INF']

print(type(table_info_list))
# <class 'list'>

print(len(table_info_list))
# 21

print(type(table_info_list[0]))
# <class 'dict'>

pprint.pprint(table_info_list[0])
# {'@id': '0003215840',
#  'CYCLE': '-',
#  'GOV_ORG': {'$': '総務省', '@code': '00200'},
#  'MAIN_CATEGORY': {'$': '人口・世帯', '@code': '02'},
#  'OPEN_DATE': '2018-04-13',
#  'OVERALL_TOTAL_NUMBER': 816,
#  'SMALL_AREA': 0,
#  'STATISTICS_NAME': '人口推計 平成29年10月1日現在人口推計',
#  'STATISTICS_NAME_SPEC': {'TABULATION_CATEGORY': '人口推計',
#                           'TABULATION_SUB_CATEGORY1': '平成29年10月1日現在人口推計'},
#  'STAT_NAME': {'$': '人口推計', '@code': '00200524'},
#  'SUB_CATEGORY': {'$': '人口', '@code': '01'},
#  'SURVEY_DATE': 201710,
#  'TITLE': {'$': '年齢（各歳），男女別人口及び人口性比－総人口，日本人人口', '@no': '001'},
#  'TITLE_SPEC': {'TABLE_NAME': '年齢（各歳），男女別人口及び人口性比－総人口，日本人人口'},
#  'UPDATED_DATE': '2018-04-14'}

df = pd.io.json.json_normalize(table_info_list, sep='_')

print(df.columns)
# Index(['@id', 'CYCLE', 'GOV_ORG_$', 'GOV_ORG_@code', 'MAIN_CATEGORY_$',
#        'MAIN_CATEGORY_@code', 'OPEN_DATE', 'OVERALL_TOTAL_NUMBER',
#        'SMALL_AREA', 'STATISTICS_NAME',
#        'STATISTICS_NAME_SPEC_TABULATION_CATEGORY',
#        'STATISTICS_NAME_SPEC_TABULATION_SUB_CATEGORY1', 'STAT_NAME_$',
#        'STAT_NAME_@code', 'SUB_CATEGORY_$', 'SUB_CATEGORY_@code',
#        'SURVEY_DATE', 'TITLE_$', 'TITLE_@no', 'TITLE_SPEC_TABLE_NAME',
#        'UPDATED_DATE'],
#       dtype='object')

df.columns = [s.replace('@', '').replace('$', 'val') for s in df.columns]
print(df.columns)
# Index(['id', 'CYCLE', 'GOV_ORG_val', 'GOV_ORG_code', 'MAIN_CATEGORY_val',
#        'MAIN_CATEGORY_code', 'OPEN_DATE', 'OVERALL_TOTAL_NUMBER', 'SMALL_AREA',
#        'STATISTICS_NAME', 'STATISTICS_NAME_SPEC_TABULATION_CATEGORY',
#        'STATISTICS_NAME_SPEC_TABULATION_SUB_CATEGORY1', 'STAT_NAME_val',
#        'STAT_NAME_code', 'SUB_CATEGORY_val', 'SUB_CATEGORY_code',
#        'SURVEY_DATE', 'TITLE_val', 'TITLE_no', 'TITLE_SPEC_TABLE_NAME',
#        'UPDATED_DATE'],
#       dtype='object')

df.to_csv('download/stats_list_{}_{}.csv'.format(p['statsCode'], p["surveyYears"]), index=False)
