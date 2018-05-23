import pandas as pd

df = pd.read_csv('download/all_stats_list.csv', dtype=str)

print(df.shape)
# (115716, 30)

print(df.columns)
# Index(['id', 'CYCLE', 'GOV_ORG_val', 'GOV_ORG_code', 'MAIN_CATEGORY_val',
#        'MAIN_CATEGORY_code', 'OPEN_DATE', 'OVERALL_TOTAL_NUMBER', 'SMALL_AREA',
#        'STATISTICS_NAME', 'STATISTICS_NAME_SPEC_TABULATION_CATEGORY',
#        'STATISTICS_NAME_SPEC_TABULATION_SUB_CATEGORY1',
#        'STATISTICS_NAME_SPEC_TABULATION_SUB_CATEGORY2',
#        'STATISTICS_NAME_SPEC_TABULATION_SUB_CATEGORY3',
#        'STATISTICS_NAME_SPEC_TABULATION_SUB_CATEGORY4',
#        'STATISTICS_NAME_SPEC_TABULATION_SUB_CATEGORY5', 'STAT_NAME_val',
#        'STAT_NAME_code', 'SUB_CATEGORY_val', 'SUB_CATEGORY_code',
#        'SURVEY_DATE', 'TITLE', 'TITLE_val', 'TITLE_no',
#        'TITLE_SPEC_TABLE_CATEGORY', 'TITLE_SPEC_TABLE_NAME',
#        'TITLE_SPEC_TABLE_SUB_CATEGORY1', 'TITLE_SPEC_TABLE_SUB_CATEGORY2',
#        'TITLE_SPEC_TABLE_SUB_CATEGORY3', 'UPDATED_DATE'],
#       dtype='object')

print(len(df[df['GOV_ORG_val'] == '総務省']))
# 38738

print(len(df.query('GOV_ORG_val == "総務省"')))
# 38738

print(len(df[df['SURVEY_DATE'].str.startswith('2017')]))
# 273

print(len(df.query('SURVEY_DATE.str.startswith("2017")', engine='python')))
# 273

print(len(df[df['TITLE_val'].str.contains('所得', na=False)]))
# 3643

print(df[['GOV_ORG_val', 'GOV_ORG_code']].drop_duplicates().sort_values(by='GOV_ORG_code'))
#        GOV_ORG_val GOV_ORG_code
# 0              内閣府        00100
# 1591           警察庁        00130
# 1603           総務省        00200
# 40341          法務省        00250
# 40423          財務省        00350
# 40445          国税庁        00351
# 40501        文部科学省        00400
# 51856        厚生労働省        00450
# 65005        農林水産省        00500
# 93920        経済産業省        00550
# 111137    資源エネルギー庁        00551
# 111252       国土交通省        00600

df_id = df.set_index('id')

print(df_id.loc['0003215840', 'TITLE_val'])
# 年齢（各歳），男女別人口及び人口性比－総人口，日本人人口

print(df_id.loc['0003215840'])
# CYCLE                                                                       -
# GOV_ORG_val                                                               総務省
# GOV_ORG_code                                                            00200
# MAIN_CATEGORY_val                                                       人口・世帯
# MAIN_CATEGORY_code                                                         02
# OPEN_DATE                                                          2018-04-13
# OVERALL_TOTAL_NUMBER                                                      816
# SMALL_AREA                                                                  0
# STATISTICS_NAME                                         人口推計 平成29年10月1日現在人口推計
# STATISTICS_NAME_SPEC_TABULATION_CATEGORY                                 人口推計
# STATISTICS_NAME_SPEC_TABULATION_SUB_CATEGORY1                平成29年10月1日現在人口推計
# STATISTICS_NAME_SPEC_TABULATION_SUB_CATEGORY2                             NaN
# STATISTICS_NAME_SPEC_TABULATION_SUB_CATEGORY3                             NaN
# STATISTICS_NAME_SPEC_TABULATION_SUB_CATEGORY4                             NaN
# STATISTICS_NAME_SPEC_TABULATION_SUB_CATEGORY5                             NaN
# STAT_NAME_val                                                            人口推計
# STAT_NAME_code                                                       00200524
# SUB_CATEGORY_val                                                           人口
# SUB_CATEGORY_code                                                          01
# SURVEY_DATE                                                            201710
# TITLE                                                                     NaN
# TITLE_val                                        年齢（各歳），男女別人口及び人口性比－総人口，日本人人口
# TITLE_no                                                                  001
# TITLE_SPEC_TABLE_CATEGORY                                                 NaN
# TITLE_SPEC_TABLE_NAME                            年齢（各歳），男女別人口及び人口性比－総人口，日本人人口
# TITLE_SPEC_TABLE_SUB_CATEGORY1                                            NaN
# TITLE_SPEC_TABLE_SUB_CATEGORY2                                            NaN
# TITLE_SPEC_TABLE_SUB_CATEGORY3                                            NaN
# UPDATED_DATE                                                       2018-04-14
# Name: 0003215840, dtype: object

df_population_2017 = df[(df['STAT_NAME_val'] == '人口推計')
                        & (df['SURVEY_DATE'].str.startswith('2017'))]

# df_population_2017 = df.query('STAT_NAME_val == "人口推計" & SURVEY_DATE.str.startswith("2017")', 
#                               engine='python')

print(len(df_population_2017))
# 21

print(df_population_2017[['id', 'TITLE_val']])
#                id                        TITLE_val
# 20806  0003215840     年齢（各歳），男女別人口及び人口性比－総人口，日本人人口
# 20807  0003215841       年齢（５歳階級），男女，月別人口－総人口，日本人人口
# 20808  0003215842           年齢（５歳階級），男女別人口及び割合－総人口
# 20809  0003215843       都道府県，男女別人口及び人口性比－総人口，日本人人口
# 20810  0003215844             都道府県，男女別人口－総人口，日本人人口
# 20811  0003215845                   都道府県別人口の割合－総人口
# 20812  0003215846                   都道府県別人口増減率－総人口
# 20813  0003215847                   都道府県別自然増減率－総人口
# 20814  0003215848                   都道府県別社会増減率－総人口
# 20815  0003215849    都道府県，年齢（5歳階級），男女別人口－総人口，日本人人口
# 20816  0003215850     都道府県，年齢（3区分），男女別人口－総人口，日本人人口
# 20817  0003215851  都道府県，年齢（3区分），男女別人口の割合－総人口，日本人人口
# 20818  0003215852               都道府県，男女別年齢構造指数－総人口
# 20819  0003215863    参考表　男女別人口の計算表－総人口，日本人人口，外国人人口
# 20820  0003215864   参考表　年齢（各歳），男女別人口の計算表－総人口，日本人人口
# 20821  0003215865     参考表　年齢（５歳階級），男女別死亡者数－日本人，外国人
# 20822  0003215866    参考表　年齢（５歳階級），男女別出入国者数－日本人，外国人
# 20823  0003215867     参考表　都道府県，男女別人口の計算表－総人口，日本人人口
# 20824  0003215868   参考表　都道府県，男女別出生児数及び死亡者数－日本人，外国人
# 20825  0003215869   参考表　都道府県，男女別都道府県間転出入者数－日本人，外国人
# 20826  0003215870        参考表　都道府県，男女別出入国者数－日本人，外国人

ids = df_population_2017['id'].values

print(ids)
# ['0003215840' '0003215841' '0003215842' '0003215843' '0003215844'
#  '0003215845' '0003215846' '0003215847' '0003215848' '0003215849'
#  '0003215850' '0003215851' '0003215852' '0003215863' '0003215864'
#  '0003215865' '0003215866' '0003215867' '0003215868' '0003215869'
#  '0003215870']

print(type(ids))
# <class 'numpy.ndarray'>
