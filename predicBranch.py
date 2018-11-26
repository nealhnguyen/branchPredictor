import numpy
from numpy import array
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing.sequence import pad_sequences
import pandas as pd
import random
from datetime import datetime
import time

def split(arr, numberOfSplits):
    splitSize = len(arr) // numberOfSplits

    splits = []
    beg = 0
    while beg < len(arr):
        splits.append(arr[beg:beg+splitSize])
        beg += splitSize

    return splits

def strToTimestamp(timeStr):
    try:
        #timeStr = int(datetime.strptime(timeStr, '%Y-%m-%d %H:%M:%S').strftime("%s"))
        timeStr = int(timeStr.strftime("%s"))
        return timeStr
    except Exception:
        print("here")
        return timeStr

# fix random seed for reproducibility
numpy.random.seed(7)

df = pd.read_csv('out.csv')
#dataframe = read_csv('trace', sep=' ', header=None)
#df['date'] = df['date'].map(strToTimestamp)
df['date'] = pd.to_datetime(df['date'])

# Build data 'x' and classified value 'y'
devices = ('Eufy Genie', 'Eufy Genie 2', 'Echo Dot 2', 'Google Home')
deviceID = {'Eufy Genie': 1, 'Eufy Genie 2': 2, 'Echo Dot 2': 3, 'Google Home': 4}
x, y = [], []
for device in devices:
    deviceDF = df.loc[df['name'] == device or ]

    start_date = datetime(2018,5,15,1,0)
    end_date = datetime(2018,5,15,2,0)
    mask = (deviceDF['date'] > start_date) & (deviceDF['date'] <= end_date)
    deviceDF = deviceDF.loc[mask]
    deviceDF['date'] = deviceDF['date'].map(strToTimestamp)
    deviceDF.to_csv(device+'.csv', index=False, header=True)

    splits = split(deviceDF[['date','power']].values.tolist(), 150)

    x += splits
    y += [deviceID[device]] * len(splits)

exit(0)

# shuffle the order so it's not all one device at a time
# make sure to do both with the same patter
temp = list(zip(x, y))
random.shuffle(temp)
x, y = zip(*temp)

# pad the data so that they're all the same length
x = pad_sequences(x, dtype='int32', value=-1)
y = array(y)

# Get necessary data for model
numSamples, length = x.shape
maxPower = df['date'].max()
# reshape data to be 3d if necessary
#x = x.reshape((numSamples, length, 1))

# split data into training and testing, use testing for validation
train_size = int(len(x) * 0.67)
test_size = len(x) - train_size
xTrain, yTrain, xTest, yTest = x[:train_size,:], y[:train_size], x[train_size:,:], y[train_size:]

# create the model
model = Sequential()
model.add(Embedding(maxPower, 2, input_length=length))
model.add(LSTM(100))
model.add(Dense(7, activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit(xTrain, yTrain, validation_data=(xTest, yTest), epochs=3, batch_size=64)

# Final evaluation of the model
scores = model.evaluate(xTest, yTest, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))