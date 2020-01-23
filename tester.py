import json, sys, os
import numpy as np
import pandas as pd

# get path and run check
path = sys.argv[1]
if not os.path.exists(path):
    raise Exception("PATH DOESN'T EXIST")

df_bus = pd.read_json(path+'/business.json', lines=True)
closed = df_bus[df_bus['is_open']==0].shape[0]
closed_ids = closed['business_id'].to_numpy()
print(f'{closed} / {df_bus.shape[0]} = {closed / df_bus.shape[0]}')

ilbus = []
for l in open(path+"/review.json").readlines():
	data = json.loads(l)
	if data["business_id"] in closed_ids:
		ilbus.append(data)

df_rev = pd.DataFrame.from_records(ilbus)
print(df_rev['rating'].count)

# df_rev = pd.read_json(path+'/review.json', lines=True)
# df_rev = df_rev[df_bus["v"] == closed]['rating'].count
# df_MIA = df_tip[df_tip['business_id'] == business_id] # get all tips for McCarran Intl Airport
# dates = df_MIA['date'].dt.year.to_numpy() # get the hour of each date of the tips for MIA
# values, counts = np.unique(dates, return_counts=True) # find how many tips were left at each hour


