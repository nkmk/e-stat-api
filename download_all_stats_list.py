import json
import e_stat_utils

with open('setting/app_id.json') as f:
    p_id = json.load(f)

e_stat_utils.save_list_csv(p_id, 'download/all_stats_list.csv')
