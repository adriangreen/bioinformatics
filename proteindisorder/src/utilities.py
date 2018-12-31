#utilities for training model, including data loading and preprocessing
from dsppkeras.datasets import dspp
from keras.callbacks import Callback
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import tensorflow as tf

def load_data():
    '''
    Loads data from dspp database
    '''
    X,Y = dspp.load_data()
    return X,Y

class Losses(Callback):
    '''
    Adds accuracy metrics to stdout
    '''
    def at_epoch_end(self, epoch, logs={}):
        print("Accuracy:  {}  Loss:  {}   Validation Accuracy:  {}".format(
               logs.get('acc'), logs.get('loss'), logs.get('val_loss')))


def lettercode2onehot(sequence):
    '''
    Return a binary one-hot vector
    '''
    one_digit = {'A': 0, 'C': 1, 'D': 2, 'E': 3, 'F': 4, 'G': 5, \
        'H': 6, 'I': 7, 'K': 8, 'L': 9, 'M': 10, 'N': 11, 'P': 12, \
        'Q': 13, 'R': 14, 'S': 15, 'T': 16, 'V': 17, 'W': 18, 'Y': 19}
    assert len(sequence) >= 1
    encoded = []
    for letter in sequence:
        tmp = np.zeros(20)
        tmp[one_digit[letter]] = 1
        encoded.append(tmp)
    assert len(encoded) == len(sequence)
    encoded = np.asarray(encoded)

    return list(encoded.flatten())

def shuffle_and_split(X, Y, seed=123456, fraction=0.8):
    '''
    Splits data set into training and test sets
    '''
    assert X.shape[0] == Y.shape[0]
    N = X.shape[0]
    np.random.seed(seed)
    indices = np.random.permutation(N)
    idx = int(N*fraction)
    training_idx, test_idx = indices[:idx], indices[idx:]
    (x_train, y_train) = (X[training_idx], Y[training_idx])
    (x_test, y_test) = (X[test_idx], Y[test_idx])

    return (x_train, y_train), (x_test, y_test)

def convert_string(string):
    '''
    Converts input protein sequence to numpy array
    '''
    return np.array([i for i in string])

def string_for_inference(x, maxlen):
    '''
    Takes numpy array of protein nucleotides, converts to one hot vector, pads
    '''
    X = [lettercode2onehot(x)]
    return pad_sequences(X, 20*maxlen)
