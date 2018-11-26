from keras.models import Sequential
from keras.layers import Dense
from pandas import read_csv
import numpy
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

dataframe = read_csv('trace', sep=' ', header=None)
dataframe[0] = dataframe[0].apply(int, base=16)

dataframes = []
for address in dataframe[0].unique():
    dataframes.append(dataframe[dataframe[0] == address])

historySize = 16
newDataframes = []
for df in dataframes:
    taken = df[1]
    #df.drop(labels=[1], axis=1,inplace = True)
    newDF = pd.DataFrame()
    for i in range(historySize + 1, 0, -1):
        #df['t-' + str(i)] = taken.shift(i).fillna(0).astype(int)
        newDF['t-' + str(i)] = taken.shift(i).fillna(0).astype(int)
    newDF.insert(len(newDF.columns), 't', taken)
    newDF.insert(0, 'address', df[0])

    newDataframes.append(newDF)

formattedDF = pd.concat(newDataframes, ignore_index=True)

df = formattedDF.sample(frac=1).reset_index(drop=True)

y = df['t']
x = df.drop(['t'], axis=1)

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size= 0.25, random_state=27)
print(y_test)
print(y_train)

clf = MLPClassifier(hidden_layer_sizes=(100,100), max_iter=500, alpha=0.0001,
                     solver='sgd', verbose=10,  random_state=21,tol=0.000000001)

clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)

print(accuracy_score(y_test, y_pred))
print(y_pred)