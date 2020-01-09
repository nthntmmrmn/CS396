import json, sys, os
import numpy as np
import pandas as pd

path = sys.argv[1]

if not os.path.exists(path):
    raise Exception("PATH DOESN'T EXIST")

df_tip = pd.read_json(path+'/tip.json', lines=True)

##### Q1 #####
print(f'Q1:{df_tip.shape[0]}')
##### Q1 #####

getColLength= np.vectorize(len)
_, colLengthsCount = np.unique(getColLength(df_tip['text'].astype(str)), return_counts=True)

##### Q2 #####
print(f'Q2:{colLengthsCount[-1]}')
##### Q2 #####

tips = df_tip.groupby('user_id')['user_id'].count()
threshold = tips.mean() + 6*tips.std()

##### Q3 #####
print(f'Q3:{len(tips[tips >= threshold])}')
##### Q3 #####

