from sklearn.linear_model import LogisticRegression
import pandas as pd
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine
import pymysql
import math
import matplotlib.pyplot as plt
import numpy as np

def load_data_pitches():
    db_connection_str = 'mysql+pymysql://root:MLB356@99.250.146.93/MLB'
    db_connection = create_engine(db_connection_str)

    df = pd.read_sql('SELECT * FROM Pitches', con=db_connection)
    return df

def load_data_atbats():
    db_connection_str = 'mysql+pymysql://root:MLB356@99.250.146.93/MLB'
    db_connection = create_engine(db_connection_str)

    df = pd.read_sql('SELECT * FROM AtBats LIMIT 100', con=db_connection)
    return df

def pitchal(row):
    row[row['pitch_type']] = 1
    return row

def codeal(row):
    row[row['code']] = 1
    return row

def typeal(row):
	if row['type'] == 'B':
		row['type_B'] = 1
	elif(row['type'] == 'S'):
		row['type_S'] = 1
	elif(row['type'] == 'X'):
		row['type_X'] = 1
	return row
    
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

atbats = load_data_atbats()
pitches = load_data_pitches()

df = atbats.merge(pitches, left_on='ab_id', right_on='ab_id')
df2 = df[['inning','o','p_score','p_throws','stand','top', 'px',
       'pz','start_speed','end_speed','spin_rate','spin_dir',
       'break_angle', 'break_length', 'break_y', 'ax', 'ay', 'az', 'sz_top', 'vx0', 'vy0', 'vz0', 'x',
       'x0', 'y', 'y0', 'z0', 'pfx_x', 'pfx_z', 'nasty', 'zone',
       'code', 'type', 'pitch_type', 'event_num', 'b_score', 'b_count', 's_count', 'outs', 'pitch_num','event']]
df2 = df2.dropna(inplace=False)
X = df2[['inning','o','p_score','p_throws','stand','top', 'px',
       'pz','start_speed','end_speed','spin_rate','spin_dir',
       'break_angle', 'break_length', 'break_y', 'ax', 'ay', 'az', 'sz_top', 'vx0', 'vy0', 'vz0', 'x',
       'x0', 'y', 'y0', 'z0', 'pfx_x', 'pfx_z', 'nasty', 'zone',
       'code', 'type', 'pitch_type', 'event_num', 'b_score', 'b_count', 's_count', 'outs', 'pitch_num']]
#Zones
y = df2['event']
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
X = X.apply(zoneal,axis=1)
X.drop(['zone'], axis=1,inplace=True)

#Pitch_type
for i in X['pitch_type'].unique():
    X[i] = 0
X = X.apply(pitchal,axis=1)
X.drop(['pitch_type'], axis=1,inplace=True)

#Code
for i in X['code'].unique():
    X[i] = 0
X = X.apply(codeal,axis=1)
X.drop(['code'], axis=1,inplace=True)

# Classifying Y
y_replace = {}
for i in y.unique():
    if(i == 'Single' or i == 'Double' or i == 'Triple' or i == 'Home Run'):
        y_replace[i] = 1
    else:
        y_replace[i] = 0
y.replace(y_replace,inplace=True)

# Stand
X['stand'].replace({'L':1,'R':0}, inplace=True)
X['p_throws'].replace({'L':1,'R':0}, inplace=True)
X['top'].replace({True:1,False:0}, inplace=True)

#type
X['type_B'] = 0
X['type_X'] = 0
X['type_S'] = 0
X = X.apply(typeal,axis=1)
X.drop(['type'], axis=1,inplace=True)
features = X.columns


X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
clf = LogisticRegression(random_state=0).fit(X_train, y_train)
y_pred = clf.predict(X_test)
print("Accuracy of model:")
print(clf.score(X_test,y_test))


imps = clf.coef_[0]
features_df = []
for i in range(0,len(imps)):
    curr = {}
    curr['name'] =  features[i]
    curr['imp'] = abs(imps[i])
    features_df.append(curr)
best_features = sorted(features_df, key=lambda k: k['imp'],reverse=True)[0:5]
names = list(map(lambda x: x['name'],best_features))
values = list(map(lambda x: x['imp'],best_features))

fig = plt.figure(figsize = (10, 5))
plt.bar(names, values, color='maroon', width=0.4)
plt.xlabel("Features")
plt.ylabel("Weight")
plt.title("Features with the most impact")
plt.show()

for feature in names:
    print("Consider feature" + str(feature))
    print("Value => ratio of hits:total entries")
    for x in X[feature].unique():
        f = df2[df['o'] == x]
        f2 = f[f['event'] == 1]
        print(str(x) + " => " + str(f.shape[0]/X.shape[0]))


