import json, sys, os
import numpy as np
import pandas as pd

# get path and run check
path = sys.argv[1]
if not os.path.exists(path):
    raise Exception("PATH DOESN'T EXIST")

def main():
    ##### Q1 #####
    #            #
    df_tip = pd.read_json(path+'/tip.json', lines=True) # load tips into dataframe

    print(f'Q1:{df_tip.shape[0]}') # print number of rows of df_tip (how many tips)
    #            #
    ##### Q1 #####


    ##### Q2 #####
    #            #
    getColLength= np.vectorize(len) # make len into an iterative fcn
    # run iterative fcn over text in each tip, find how many of each length text there are
    _, colLengthsCount = np.unique(getColLength(df_tip['text'].astype(str)), return_counts=True) 

    print(f'Q2:{colLengthsCount[-1]}') # print how many of longest tip text (listed in ascending order)
    #            #
    ##### Q2 #####


    ##### Q3 #####
    #            #
    tips = df_tip.groupby('user_id')['user_id'].count() # find number of tips each user made
    threshold = tips.mean() + 6*tips.std() # calculate 'outstanding' threshold

    print(f'Q3:{len(tips[tips >= threshold])}') # print how many tips were above the threshold
    #            #
    ##### Q3 #####


    ##### Q4 #####
    #            #
    df_business = pd.read_json(path+'/business.json', lines=True) # load businesses into dataframe

    business_id = df_tip['business_id'].mode().get(0) # find 'business_id' that appears the most
    # get name of the business with that id
    name = df_business[df_business['business_id'] == business_id]['name'].values[0]

    print(f'Q4:{name}')
    #            #
    ##### Q4 #####


    ##### Q5 #####
    #            #
    df_MIA = df_tip[df_tip['business_id'] == business_id] # get all tips for McCarran Intl Airport
    dates = df_MIA['date'].dt.hour.to_numpy() # get the hour of each date of the tips for MIA
    values, counts = np.unique(dates, return_counts=True) # find how many tips were left at each hour

    print(f'Q5:{values[np.argmin(counts)]}') # print the hour that had the max # of tips
    #            #
    ##### Q5 #####

main()

