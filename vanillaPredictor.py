from keras.models import Sequential
from keras.layers import Dense
from pandas import read_csv
import numpy
import pandas as pd
from keras import optimizers

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

dataframe = read_csv('trace', sep=' ', header=None)
#dataframe[0] = dataframe[0].apply(int, base=16)

dataframes = []
for address in dataframe[0].unique():
    dataframes.append(dataframe[dataframe[0] == address])

historySize = 4
newDataframes = []
for df in dataframes:
    taken = df[1]
    #df.drop(labels=[1], axis=1,inplace = True)
    newDF = pd.DataFrame()
    for i in range(historySize + 1, 0, -1):
        #df['t-' + str(i)] = taken.shift(i).fillna(0).astype(int)
        newDF['t-' + str(i)] = taken.shift(i).fillna(0)#.astype(int)
    newDF.insert(len(newDF.columns), 't', taken)
    newDF.insert(0, 'address', df[0])

    newDataframes.append(newDF)

formattedDF = pd.concat(newDataframes, ignore_index=True)
print(formattedDF)

shuffledDF = formattedDF.sample(frac=1).reset_index(drop=True)
dataset = shuffledDF.values
# print(dataset)
# exit(0)

# split into input (X) and output (Y) variables
X = dataset[:,0:historySize + 2]
Y = dataset[:,historySize + 2]
# print(Y)
# exit(0)
# create model
model = Sequential()
model.add(Dense(12, input_dim=historySize+2, init='uniform', activation='relu'))
model.add(Dense(8, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform', activation='sigmoid'))

sgd = optimizers.SGD(lr=0.11)

# Compile model
#model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])
# Fit the model
model.fit(X, Y, epochs=150, batch_size=10,  verbose=2)
# calculate predictions
predictions = model.predict(X)
# print(predictions)
# exit(0)
# round predictions
rounded = [round(x[0]) for x in predictions]
# print(rounded)