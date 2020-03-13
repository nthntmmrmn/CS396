import warnings
import pandas as pd
import numpy as np
import json
from sklearn.model_selection import KFold
from sklearn.metrics import roc_auc_score, accuracy_score, r2_score, confusion_matrix
from sklearn import metrics
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
import math
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
import time
import seaborn as sn
from mpl_toolkits.mplot3d import Axes3D
import geopandas as gpd
# import geoplot as gplt
import descartes
from shapely.geometry import Point, Polygon
warnings.simplefilter('ignore')

AZ_bus = pd.read_json('AZ_business_all.json')

businesses = AZ_bus[['latitude','longitude']].to_numpy()
targets = AZ_bus['is_open'].to_numpy()
features = AZ_bus[['time_open','reviews_per_week','density','relative_stars','relative_review_count']].astype(int).to_numpy()

kf = KFold(n_splits=5, shuffle=True)

business_predicted = []
probs_per_bus = []
actual = []
all_pred = []

t = []
p = []
accuracy_score_nb = []
probs_nb = []
for train_index, test_index in kf.split(features):
    X_train, X_test = features[train_index], features[test_index]
    y_train, y_test = targets[train_index], targets[test_index]
    
    actual.append(targets[test_index])
    business_predicted.append(businesses[test_index])
    
    RF = AdaBoostClassifier(base_estimator=RandomForestClassifier(n_estimators=100, max_depth = 3, class_weight='balanced'), learning_rate=1, n_estimators=100).fit(X_train, y_train)
    y_pred = RF.predict(X_test)
    
    p.append(y_pred)
    t.append(y_test)
    
    probs_per_bus.append(RF.predict_proba(X_test))
    all_pred.append(y_pred)
    
    accuracy_score_nb.append(accuracy_score(y_test, y_pred))

print(f'KNN Classification Accuracy Score: {np.mean(accuracy_score_nb)}')
flat_t = [item for sublist in t for item in sublist]
flat_p = [item for sublist in p for item in sublist]
tn, fp, fn, tp = confusion_matrix(flat_t, flat_p).ravel()
cm = confusion_matrix(flat_t, flat_p)
print(f'tn: {tn}, fn: {fn}, tp: {tp}, fp: {fp}')
print(tn / (tn+fp))

print(metrics.classification_report(flat_t, flat_p, target_names=['closed','open']))

df_cm = pd.DataFrame(cm, range(2), range(2))
print(df_cm)
# plt.figure(figsize=(10,7))
sn.set(font_scale=1.4) # for label size

all_val = df_cm.to_numpy().flatten()
total = all_val.sum()

labels = [f'{v1}\n{round(v2, 2)}%' for v1, v2 in
          zip(all_val,all_val/total*100)]

labels = np.asarray(labels).reshape(2,2)
x_ticks = ['Closed', 'Open']
y_ticks = ['Closed', 'Open']

img = sn.heatmap(df_cm, annot=labels, annot_kws={"size": 14}, fmt='', cmap="YlGnBu", xticklabels=x_ticks, yticklabels=y_ticks) # font size

plt.savefig('confusion_matrix.png')

#############################################################

all_lat_long = np.concatenate((business_predicted[0],business_predicted[1],business_predicted[2],business_predicted[3],business_predicted[4]))
all_lat_long = all_lat_long.reshape((-1,2))

world = gpd.read_file('../states21basic/states.shp')
# crs = {'init': 'epsg:4326'}
# geometry = [Point(xy) for xy in zip(latlng.longitude, latlng.latitude)]

geo_df = gpd.GeoDataFrame(all_lat_long[:100], geometry=gpd.points_from_xy(all_lat_long[:100,0], all_lat_long[:100,1]))
fig,ax = plt.subplots(figsize=(15,15))
# world.plot(ax=ax, alpha=0.4, color='grey')
world[usa.state_abbr == 'AZ'].plot(ax=ax, alpha=0.4, color='grey')

geo_df.plot(ax=ax, markersize=0.5, color='red', marker='o')

