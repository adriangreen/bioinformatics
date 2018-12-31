#model file for dspp prediction, using keras

import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Activation


def model(maxlen):
    '''
    Builds neural network model for protein disorder Prediction
    '''

    model = Sequential()
    model.add(Dense(maxlen, input_shape=(20*maxlen,), activation='relu', name='dense1'))
    model.add(Dropout(0.5))
    model.add(Dense(maxlen, input_shape=(20*maxlen,), activation='relu', name='dense2'))
    model.add(Dropout(0.5))
    model.add(Dense(maxlen, input_shape=(20*maxlen,), activation='relu', name='dense3'))
    model.add(Dropout(0.5))
    model.add(Dense(maxlen, input_shape=(20*maxlen,), activation='relu', name='output'))

    return model
