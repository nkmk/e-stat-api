import json
import pandas as pd
import e_stat_utils

dir_path = 'download'

with open('setting/app_id.json') as f:
    p_id = json.load(f)

with open('setting/get_stats_list_sample.json') as f:
    p_list = json.load(f)

p_list.update(p_id)
filename = 'stats_list_{}_{}'.format(p_list['statsCode'], p_list["surveyYears"])

e_stat_utils.save_list(p_list, dir_path, filename)
e_stat_utils.save_list(p_list, dir_path, filename, form='xml')
e_stat_utils.save_list(p_list, dir_path, filename, form='json',
                       ensure_ascii=False, indent=4)

with open('setting/get_stats_data_sample.json') as f:
    p_data = json.load(f)

p_data.update(p_id)

e_stat_utils.save_data(p_data, dir_path=dir_path)
e_stat_utils.save_data(p_data, dir_path=dir_path)
e_stat_utils.save_data(p_data, dir_path=dir_path, skip=False)
e_stat_utils.save_data(p_data, '0003215841', dir_path=dir_path)
e_stat_utils.save_data(p_data, dir_path=dir_path, filename='header_true', section_header=True)
# download 0003215840 to download/0003215840.csv
# skip 0003215840 (download/0003215840.csv already exists)
# download 0003215840 to download/0003215840.csv
# download 0003215841 to download/0003215841.csv
# download 0003215840 to download/header_true.csv

e_stat_utils.save_data(p_data, dir_path=dir_path, form='xml')
e_stat_utils.save_data(p_data, dir_path=dir_path, form='json',
                       ensure_ascii=False, indent=4)
# download 0003215840 to download/0003215840.xml
# download 0003215840 to download/0003215840.json

ids = ['0003215842', '0003215843', '0003215844']

e_stat_utils.save_data_multi(p_id, ids, dir_path)
# download 0003215842 to download/0003215842.csv
# download 0003215843 to download/0003215843.csv
# download 0003215844 to download/0003215844.csv

e_stat_utils.save_data_multi(p_id, ids, dir_path, form='xml')
# download 0003215842 to download/0003215842.xml
# download 0003215843 to download/0003215843.xml
# download 0003215844 to download/0003215844.xml

prefixes = ['0', '1', '2']
suffixes = ['xxx', 'yyy', 'zzz']

e_stat_utils.save_data_multi(p_id, ids, dir_path, [prefixes, ids, suffixes])
# download 0003215842 to download/0_0003215842_xxx.csv
# download 0003215843 to download/1_0003215843_yyy.csv
# download 0003215844 to download/2_0003215844_zzz.csv

df = pd.read_csv('download/all_stats_list.csv', dtype=str)

df_target = df[(df['STAT_NAME_val'] == '人口推計')
               & (df['SURVEY_DATE'].str.startswith('2017'))
               & (df['TITLE_val'].str.contains('出入国'))]

e_stat_utils.save_data_multi(p_id, df_target['id'].values, dir_path)
# download 0003215866 to download/0003215866.csv
# download 0003215870 to download/0003215870.csv

e_stat_utils.save_data_multi(p_id, df_target['id'].values, dir_path,
                             [df_target['GOV_ORG_code'].values,
                              df_target['id'].values,
                              df_target['TITLE_val'].values])
# download 0003215866 to download/00200_0003215866_参考表　年齢（５歳階級），男女別出入国者数－日本人，外国人.csv
# download 0003215870 to download/00200_0003215870_参考表　都道府県，男女別出入国者数－日本人，外国人.csv

e_stat_utils.save_data_multi_direct(p_list, p_data, p_id, dir_path,
                                    ['xxx', '@id', 'SURVEY_DATE', ['STAT_NAME', '$']])
# download 0003215840 to download/xxx_0003215840_201710_人口推計.csv
# download 0003215841 to download/xxx_0003215841_201710_人口推計.csv
# download 0003215842 to download/xxx_0003215842_201710_人口推計.csv
# download 0003215843 to download/xxx_0003215843_201710_人口推計.csv
# download 0003215844 to download/xxx_0003215844_201710_人口推計.csv
# download 0003215845 to download/xxx_0003215845_201710_人口推計.csv
# download 0003215846 to download/xxx_0003215846_201710_人口推計.csv
# download 0003215847 to download/xxx_0003215847_201710_人口推計.csv
# download 0003215848 to download/xxx_0003215848_201710_人口推計.csv
# download 0003215849 to download/xxx_0003215849_201710_人口推計.csv
# download 0003215850 to download/xxx_0003215850_201710_人口推計.csv
# download 0003215851 to download/xxx_0003215851_201710_人口推計.csv
# download 0003215852 to download/xxx_0003215852_201710_人口推計.csv
# download 0003215863 to download/xxx_0003215863_201710_人口推計.csv
# download 0003215864 to download/xxx_0003215864_201710_人口推計.csv
# download 0003215865 to download/xxx_0003215865_201710_人口推計.csv
# download 0003215866 to download/xxx_0003215866_201710_人口推計.csv
# download 0003215867 to download/xxx_0003215867_201710_人口推計.csv
# download 0003215868 to download/xxx_0003215868_201710_人口推計.csv
# download 0003215869 to download/xxx_0003215869_201710_人口推計.csv
# download 0003215870 to download/xxx_0003215870_201710_人口推計.csv
