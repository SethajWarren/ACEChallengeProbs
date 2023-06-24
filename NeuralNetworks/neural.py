import re
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.utils import to_categorical

STR_LIST = []

# main function
def main():

    strList = np.zeroes(1,100)
    print(strList)

    model = Sequential(name="Malware Neural Network")
    model.add(Flatten(input_shape=(100,1)))
    model.add(Dense(5, activation='sigmoid'))
    model.add(Dense(2, activation='softmax'))

    model.summary()

    #model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])


# function to get the strings from a file
def getStrings(file):
    chars = r"A-Za-z0-9/\-:.,_$%'()[\]<> "
    shortestRun = 4
    regexp = '[%s]{%d,}' % (chars, shortestRun)
    pattern = re.compile(regexp)

    return pattern.findall(file)

# start the main function
if __name__ == "__main__":
    main()



