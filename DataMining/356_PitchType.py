from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree
from sqlalchemy import create_engine
import pymysql

def load_data():
    db_connection_str = 'mysql+pymysql://root:MLB356@99.250.146.93/MLB'
    db_connection = create_engine(db_connection_str)

    df = pd.read_sql('SELECT * FROM Pitches', con=db_connection)
    return df


def preprocess_data(pitcher_df):
    pitcher_df = pitcher_df[pitcher_df['pitch_type'] != 'UN']
    pitcher_df = pitcher_df.replace({'FO': 'PO'})
    pitcher_df2 = pitcher_df[['px', 'pz', 'start_speed', 'end_speed', 'spin_rate', 'spin_dir',
       'break_angle', 'break_length', 'break_y', 'ax', 'ay', 'az',
       'sz_top', 'vx0', 'vy0', 'vz0', 'x', 'x0', 'y', 'y0',
       'z0', 'pfx_x', 'pfx_z','b_count', 's_count','pitch_num', 'pitch_type']]
    pitcher_df2 = pitcher_df2.dropna(inplace=False)
    X = pitcher_df2[['px', 'pz', 'start_speed', 'end_speed', 'spin_rate', 'spin_dir',
       'break_angle', 'break_length', 'break_y', 'ax', 'ay', 'az',
       'sz_top', 'vx0', 'vy0', 'vz0', 'x', 'x0', 'y', 'y0',
       'z0', 'pfx_x', 'pfx_z','b_count', 's_count','pitch_num']]
    y = pitcher_df2['pitch_type']
    replace_dict = {}
    replace_dict = {}
    replace_dict_rev = {}
    i = 1
    for x in pitcher_df2['pitch_type'].unique():
        replace_dict[x] = i
        replace_dict_rev[i] = x
        i = i+1
    y = y.replace(replace_dict,inplace=False)
    return X,y,replace_dict_rev

def train_model(X_train, y_train):
    dtree_model = DecisionTreeClassifier(max_depth=4).fit(X_train, y_train)
    return dtree_model

def print_accuracy_score(y_test,dtree_predictions):
    count = 0
    y_test = y_test.tolist()
    for i in range(0,len(y_test)):
        if(dtree_predictions[i] == y_test[i]):
            count = count + 1
    print(str(count/len(y_test)))

def validation(dtree_model,y_test,X_test):
    dtree_predictions = dtree_model.predict(X_test)
    # creating a confusion matrix
    cm = confusion_matrix(y_test, dtree_predictions)

    list_cm = []
    for arr in cm:
        list_cm.append(list(arr))
    cm_sum = 0
    for i in cm:
        cm_sum = cm_sum + sum(i)
    print_accuracy_score(y_test,dtree_predictions)

def metrics(cm,index,cm_sum):
    result = {
        'TN': 0,
        'FN': 0,
        'TP': 0,
        'FP': 0,
        'precision' : 0,
        'recall' : 0,
        'f1_score' : 0
    }
    result['TP'] = cm[index][index]
    for row in range(0,len(cm)):
        if(row == index):
            continue
        result['FP'] = result['FP'] + cm[index][row]
    for col in range(0,len(cm)):
        if(col == index):
            continue
        result['FN'] = result['FN']+ cm[col][index]
    result['TN'] = cm_sum - result['FN'] - result['TP'] - result['FP']
    result['precision'] = result['TP']/(result['TP'] + result['FP'])
    result['recall'] = result['TP'] / (result['TP'] + result['FN'])
    if(result['precision'] == 0 and result['recall'] == 0):
        result['f1_score'] = 0
    else:
        result['f1_score'] = ( 2*result['precision']*result['recall'] ) / (result['precision'] + result['recall'])
    return result

def metrics_each_class(dtree_model,replace_dict_rev,cm):
    cm_sum = 0
    for i in cm:
        cm_sum = cm_sum + sum(i)
    classes = []
    for i in range(0,len(cm)):
        class_name = replace_dict_rev[i+1]
        curr = {}
        curr['name'] = class_name
        curr['metrics'] = metrics(cm,i,cm_sum)
        classes.append(curr)
    
    return classes

def best_classes(classes):
    classes2 = list(filter(lambda x: not(math.isnan(x['metrics']['f1_score']) or math.isnan(x['metrics']['precision']) or math.isnan(x['metrics']['recall']) ), classes))
    labels = [ sub['name'] for sub in sorted(classes2, key=lambda k: k['metrics']['f1_score'],reverse=True)[0:3] ]
    f1_scores = [ sub['metrics']['f1_score'] for sub in sorted(classes2, key=lambda k: k['metrics']['f1_score'],reverse=True)[0:3] ]
    precisions = [sub['metrics']['precision'] for sub in list(filter(lambda x : x['name'] in labels,classes2)) ]
    recalls = [sub['metrics']['recall'] for sub in list(filter(lambda x : x['name'] in labels,classes2)) ]
    return labels, precisions, recalls, f1_scores

def get_most_imp_features(model):
    model = models[2]
    features = ['px', 'pz', 'start_speed', 'end_speed', 'spin_rate', 'spin_dir',
           'break_angle', 'break_length', 'break_y', 'ax', 'ay', 'az',
           'sz_top', 'vx0', 'vy0', 'vz0', 'x', 'x0', 'y', 'y0',
           'z0', 'pfx_x', 'pfx_z','b_count', 's_count','pitch_num']
    imps_list = []
    imps = model.feature_importances_
    for i in range(0,len(imps)):
        imps_dict = {}
        imps_dict['imp'] = imps[i]
        imps_dict['name'] = features[i]
        imps_list.append(imps_dict)
    return list(map(lambda x: x['name'] , sorted(imps_list, key=lambda k: k['imp'],reverse=True)[0:5]))


def one_vs_all(pitcher_df,class_to_consider):
    pitcher_df2 = pitcher_df[['px', 'pz', 'start_speed', 'end_speed', 'spin_rate', 'spin_dir',
           'break_angle', 'break_length', 'break_y', 'ax', 'ay', 'az',
           'sz_top', 'vx0', 'vy0', 'vz0', 'x', 'x0', 'y', 'y0',
           'z0', 'pfx_x', 'pfx_z','b_count', 's_count','pitch_num','pitch_type']]
    pitcher_df2 = pitcher_df2.dropna(inplace=False)
    X = pitcher_df2[['px', 'pz', 'start_speed', 'end_speed', 'spin_rate', 'spin_dir',
           'break_angle', 'break_length', 'break_y', 'ax', 'ay', 'az',
           'sz_top', 'vx0', 'vy0', 'vz0', 'x', 'x0', 'y', 'y0',
           'z0', 'pfx_x', 'pfx_z','b_count', 's_count','pitch_num']]
    y = pitcher_df2['pitch_type']
    replace_dict = {}
    for x in pitcher_df2['pitch_type'].unique():
        replace_dict[x] = 0
        if(x == class_to_consider):
            replace_dict[x] = 1
    y = y.replace(replace_dict)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    model1 = train_model(X_train, y_train)
    print("Accuray for " + str(class_to_consider))
    validation(model1,y_test,X_test)
    return model1

pitcher_df = load_data()


X,y,replace_dict_rev = preprocess_data(pitcher_df)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

dtree_model = train_model(X_train, y_train)

dtree_predictions = dtree_model.predict(X_test)
print("Accuracy for multiclass")
print_accuracy_score(y_test,dtree_predictions)

cm = confusion_matrix(y_test, dtree_predictions)
classes = metrics_each_class(dtree_model,replace_dict_rev,cm)
labels, precisions, recalls, f1_scores = best_classes(classes)

X_axis = np.arange(3)

plt.bar(X_axis + 0.00, precisions, label='Precision', width = 0.25)
plt.bar(X_axis + 0.25, recalls, label='Recall', width = 0.25)
plt.bar(X_axis + 0.50, f1_scores, label='F1 Score', width = 0.25)


plt.xticks(X_axis, labels)
plt.xlabel("Best predicted Classes")
plt.ylabel("Evaluation metrics")
plt.title("Precision,Recall and F1 score for the best predicated classes")
plt.legend()
plt.show()

models = []
for class_to_consider in labels:
    models.append(one_vs_all(pitcher_df,class_to_consider))



