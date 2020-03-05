import pandas as pd
import numpy as np

df_business = pd.read_json("yelp_dataset/business.json", lines=True)
df_review = pd.read_json("yelp_dataset/review.json", lines=True)
df_review = df_review.rename(columns={'stars': 'rating'})

df_join = df_review[['business_id', 'text', 'rating']].join(df_business[['business_id', 'is_open', 'stars']].set_index('business_id'), on='business_id')

text_length = np.vectorize(len)

def my_aggregator(data):
    reviews = data['text']
    mean_review = np.mean(text_length(reviews))
    mean_polarity = np.mean([TextBlob(x).sentiment.polarity for x in reviews])
    stars = data.iloc[0]['stars']
    is_open = data.iloc[0]['is_open']
    
    r = np.zeros(5)
    rating, rating_counts = np.unique(data['rating'].to_numpy(), return_counts=True)
    total = sum(rating_counts)
    ratings = rating_counts.astype(np.float64) / total
    for i, rate in enumerate(rating):
        r[rate-1] = ratings[i]
    
    r = r*100
    return np.concatenate((r, np.array([mean_review, mean_polarity, stars, is_open])))


h = df_join.groupby('business_id').apply(my_aggregator).to_numpy()
h = np.stack(h)

df_all = pd.DataFrame(data=h, index=list(range(0,len(h))), columns=["p1", "p2", "p3", "p4", "p5", "mean_review", "mean_polarity", "stars", "is_open"])

df_all.to_json(r'features.json',orient='records')

