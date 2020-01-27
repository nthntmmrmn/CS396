import json, sys, os
import numpy as np
import pandas as pd
import scipy.stats as stats

# get path and run check
path = sys.argv[1]
if not os.path.exists(path):
    raise Exception("PATH DOESN'T EXIST")

def main():
    hello()

def hello():
    # path = "../yelp_dataset"

    df_user = pd.read_json(path+'/user.json', lines=True)
    # reviews and fans
    reviews = df_user['review_count'].to_numpy()
    fans = df_user['fans'].to_numpy()
    print('starting calcs...')
    p1_pearson = stats.pearsonr(reviews, fans)
    _, p1_spearman = stats.spearmanr(reviews, fans)


    # useful and funny
    useful = df_user['useful'].to_numpy()
    funny = df_user['funny'].to_numpy()
    p2_pearson = stats.pearsonr(useful, funny)
    _, p2_spearman = stats.spearmanr(useful, funny)

    # useful and fans
    p3_pearson = stats.pearsonr(useful, fans)
    _, p3_spearman = stats.spearmanr(useful, fans)

    print(f'1: Pearson: {p1_pearson} \t Spearman: {p1_spearman}\n')
    print(f'2: Pearson: {p2_pearson} \t Spearman: {p2_spearman}\n')
    print(f'3: Pearson: {p3_pearson} \t Spearman: {p3_spearman}\n')


def calc():
    tot_closed = 2023+1330+1799+3185+4707
    tot_open = 12562+6645+9171+18918+39660
    print(f'Percent 1 Star Closed: {(2023/tot_closed)*100}\n')
    print(f'Percent 1 Star Open: {(12562/tot_open)*100}\n')
    avg_closed = (2023*1 + 1330*2 + 1799*3 + 3185*4 + 4707*5) / tot_closed
    avg_open = (12562*1 + 6645*2 + 9171*3 + 18918*4 + 39660*5) / tot_open
    print(f'Average Stars Closed: {avg_closed}\n')
    print(f'Average Stars Open: {avg_open}\n')

def get_stars():
    df_bus = pd.read_json(path+'/business.json', lines=True)
    closed = df_bus[df_bus['is_open']==0]
    opened = df_bus[df_bus['is_open']==1]
    closed_ids = closed['business_id'].to_numpy()
    opened_ids = opened['business_id'].to_numpy()
    # print(f'{closed} / {df_bus.shape[0]} = {closed / df_bus.shape[0]}')

    ilbus = []
    for i, l in enumerate(open(path+"/review.json").readlines()):
        data = json.loads(l)
        if i == 100000:
            break
        if data["business_id"] in opened_ids:
            ilbus.append(data)


    df_rev = pd.DataFrame.from_records(ilbus)
    print(df_rev.groupby('stars')['stars'].count())

main()


