import re
import os
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.utils import to_categorical
from sklearn.feature_extraction import FeatureHasher
from collections import Counter
import numpy as np

# main function
def main():

    h = FeatureHasher(n_features=100, input_type="string")

    data, labels = getData()
    print(len(data))
    print(len(labels))
    # data = data/10

    # temp = []
    # for i in range(len(labels)):
    #     temp.append(to_categorical(labels[i], num_classes=2))

    # labels = temp
    
    # featHash = h.transform(data).toarray()

    model = Sequential(name="MalwareNeuralNetwork")
    model.add(Flatten(input_shape=(10,20)))
    model.add(Dense(5, activation='relu'))
    model.add(Dense(2, activation='softmax'))

    model.summary()

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])

    model.fit(data, labels, epochs=5)

# function to get the strings from a https://becominghuman.ai/simple-neural-network-on-mnist-handwritten-digit-dataset-61e47702ed25file
def getStrings(file):
    chars = r"A-Za-z0-9/\-:.,_$%'()[\]<> "
    shortestRun = 4
    regexp = '[%s]{%d,}' % (chars, shortestRun)
    pattern = re.compile(regexp)

    str = pattern.findall(file)

    mcs = Counter(str).most_common(200)
    strs = []
    for item, _ in mcs:
        strs.append(item)
    
    if len(strs) < 200:
        while len(strs) < 200:
            strs.append("pad")
        
    return strs

def getData():

    strList = []
    keyList = []

    for file in os.listdir("train/benignware"):
        exe = open("train/benignware/"+file, "r", errors="ignore").read()
        str = getStrings(exe)

        strList.append(np.array(str).reshape(10,20))
        keyList.append(0)

    
    for file in os.listdir("train/malware"):
        exe = open("train/malware/"+file, "r", errors="ignore").read()
        str = getStrings(exe)

        strList.append(np.array(str).reshape(10,20))
        keyList.append(1)

    return(np.array(strList), np.array(keyList))

# start the main function
if __name__ == "__main__":
    main()
200


