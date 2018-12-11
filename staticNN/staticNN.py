from keras.models import Sequential
from keras.layers import Dense
from pandas import read_csv
import numpy
import pandas as pd
from keras import optimizers
from sklearn.preprocessing import StandardScaler
import time

start_time = time.time()
for historySize in (10, 15, 20):
    print("-----------------------------------")
    print("historysize: " + str(historySize))
    begin_time = time.time()
    # fix random seed for reproducibility
    seed = 7
    numpy.random.seed(seed)

    dataframe = read_csv('gcc_branch', sep=' ', header=None)
    #print(dataframe)
    dataframe = dataframe.drop(dataframe.columns[0], axis=1)
    dataframe.columns = [0, 1]
    dataframe[0] = dataframe[0].apply(int, base=16)
    #dataframe[0] = dataframe[0].apply(float)
    #dataframe[1] = dataframe[1].apply(float)

    dataframes = []
    for address in dataframe[0].unique():
        dataframes.append(dataframe[dataframe[0] == address])

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
    scaler = StandardScaler()
    formattedDF['address'] = scaler.fit_transform(formattedDF['address'].values.reshape(-1, 1))
    #print(formattedDF)
    #exit(0)

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
    model.add(Dense(12, input_dim=historySize+2, activation='sigmoid'))
    model.add(Dense(historySize+2, activation='sigmoid'))
    model.add(Dense(1, activation='sigmoid'))

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
    print("--- %s seconds from start ---" % (time.time() - start_time))
    print("--- %s seconds for current run ---" % (time.time() - begin_time))
