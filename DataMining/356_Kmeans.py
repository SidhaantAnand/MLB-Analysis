import pandas as pd
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
import math
from itertools import combinations
import mysql.connector
from sqlalchemy import create_engine
import pymysql

def load_data():
    db_connection_str = 'mysql+pymysql://root:MLB_Gang@99.250.146.93/MLB'
    db_connection = create_engine(db_connection_str)

    df = pd.read_sql('SELECT * FROM Pitches', con=db_connection)
    return df


def Kmeansmodel(X,num_clusters):
    kmeans = KMeans(n_clusters=num_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(X)
    return kmeans

def preprocess_case1(X):
    zone_cast = {
    11: -1,
    13: -1,
    1: -1,
    7: -1,
    4: -1,
    2: 0,
    5: 0,
    8:0,
    3:1,
    6:1,
    9:1,
    12:1,
    14: 1
    }
    X['zone'] = X['zone'].replace(to_replace = zone_cast)
    return X

def preprocess_case2(X):
    zone_cast = {
    11: 1,
    13: -1,
    1: 1,
    7: -1,
    4: 0,
    2: 1,
    5: 0,
    8: -1,
    3: 1,
    6: 0,
    9: -1,
    12: 1,
    14: -1
    }
    X['zone'] = X['zone'].replace(to_replace = zone_cast)
    return X

def get_X_case1(pitcher_df):
    X = pitcher_df[['zone','px']]
    return X

def get_X_case2(pitcher_df):
    X = pitcher_df[['zone','pz']]
    return X


def get_X_case3(pitcher_df):
    X = pd.DataFrame(columns = ['zone','zone1','zone2','zone3','zone4','zone5','zone6','zone7','zone8','zone9','zone10','zone11','zone12','zone13','zone14','px','pz'])
    X['px'] = pitcher_df['px']
    X['pz'] = pitcher_df['pz']
    X['zone1'] = 0
    X['zone2'] = 0
    X['zone3'] = 0
    X['zone4'] = 0
    X['zone5'] = 0
    X['zone6'] = 0
    X['zone7'] = 0
    X['zone8'] = 0
    X['zone9'] = 0
    X['zone10'] = 0
    X['zone11'] = 0
    X['zone12'] = 0
    X['zone13'] = 0
    X['zone14'] = 0
    X['zone'] = pitcher_df['zone']
    return X

def zoneal(row):
    if row['zone'] == 1:
        row['zone1'] = 1
    elif(row['zone'] == 2):
        row['zone2'] = 1
    elif(row['zone'] == 3):
        row['zone3'] = 1
    elif(row['zone'] == 4):
        row['zone4'] = 1
    elif(row['zone'] == 5):
        row['zone5'] = 1
    elif(row['zone'] == 6):
        row['zone6'] = 1
    elif(row['zone'] == 7):
        row['zone7'] = 1
    elif(row['zone'] == 8):
        row['zone8'] = 1
    elif(row['zone'] == 9):
        row['zone9'] = 1
    elif(row['zone'] == 10):
        row['zone10'] = 1
    elif(row['zone'] == 11):
        row['zone11'] = 1
    elif(row['zone'] == 12):
        row['zone12'] = 1
    elif(row['zone'] == 13):
        row['zone13'] = 1
    elif(row['zone'] == 14):
        row['zone14'] = 1
    return row


def preprocess_case3(X):
    X = X.apply(zoneal,axis=1)
    X = X.drop(['zone'], axis=1,inplace=False)
    return X

def inter_cluster_dist(model_case1,model_case2,model_case3):
    for model in [model_case1,model_case2] :
        centers = model.cluster_centers_
        num_centers = len(centers)
        sums = 0
        for combo in combinations(centers, 2):
            p1, p2 = combo
            x1, y1 = p1
            x2, y2 = p2
            sums = sums +  math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        print(sums/num_centers)
    centers = model_case3.cluster_centers_
    num_centers = len(centers)
    sumss = 0
    for combo in combinations(centers, 2):
        p1, p2 = combo
        x1 = p1[12]
        y1 = p1[13]
        x2 = p2[12]
        y2 = p2[13]
        sums = sums +  math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    print(sums/num_centers)

pitcher_df = load_data()
pitcher_df = pitcher_df[['zone','px','pz']]

pitcher_df.dropna(inplace=True)

# Case 1
X = get_X_case1(pitcher_df)
X = preprocess_case1(X)
model_case1 = Kmeansmodel(X,3)
X = X.to_numpy()
plt.scatter(X[:,0], X[:,1],label='data points')
plt.scatter(model_case1.cluster_centers_[:, 0], model_case1.cluster_centers_[:, 1], s=300, c='red',label='centroids')
plt.xlabel("zone")
plt.ylabel("px")
plt.title("Clustering of px vs zone")
plt.legend()
plt.show()


# Case 2
X = get_X_case2(pitcher_df)
X = preprocess_case2(X)
model_case2 = Kmeansmodel(X,3)
X = X.to_numpy()
plt.scatter(X[:,0], X[:,1],label='data points')
plt.scatter(model_case2.cluster_centers_[:, 0], model_case2.cluster_centers_[:, 1], s=300, c='red',label='centroid')
plt.xlabel("zone")
plt.ylabel("pz")
plt.title("Clustering of pz vs zone")
plt.legend()
plt.show()

#Case 3
X = get_X_case3(pitcher_df)
X = preprocess_case3(X)
model_case3 = Kmeansmodel(X,13)

