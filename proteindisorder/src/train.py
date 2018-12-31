from model import model
import keras
from keras.preprocessing.sequence import pad_sequences
from keras.losses import mean_squared_error
from keras.utils import plot_model
from utilities import load_data, lettercode2onehot, shuffle_and_split, Losses
from matplotlib import pyplot as plt

def train():
    '''
    Sets up model training, executes training, saves model and graphs training
    loss
    '''
    # parameter to define input shape for model, size of largest item in database
    maxlen = 800

    x, y = load_data()
    x = [lettercode2onehot(i) for i in x]
    X = pad_sequences(x, 20*maxlen)
    Y = pad_sequences(y, maxlen, dtype='float32')

    (train_x, train_y), (test_x, test_y) = shuffle_and_split(X, Y)

    batch_size = 32
    epochs = 1

    nnet = model(maxlen)
    nnet.compile(optimizer=keras.optimizers.Adam(), loss=mean_squared_error,
                 metrics=['accuracy'])

    # save model to get loss metrics
    nn_model = nnet.fit(x=train_x, y=train_y, epochs=epochs, batch_size=batch_size,
                         validation_data=(test_x, test_y), callbacks=[Losses()])

    # model loss for plotting
    nn_loss = nn_model.history['loss']
    nn_val_loss = nn_model.history['val_loss']
    epoch_list = [i for i in range(epochs)]

    # create training loss plot
    plt.plot(epoch_list, nn_val_loss, label='Validation Loss')
    plt.plot(epoch_list, nn_loss, label="Training Loss")
    plt.legend(loc="upper right")
    plt.xlabel('Epoch')
    plt.ylabel('Mean Squared Error')
    plt.title('Training and Validation Loss')
    plt.savefig('loss_plot.png')

    # save model
    with open("model.json", "w") as fp:
        fp.write(nnet.to_json())
    # Serialize weights to HDF5
    nnet.save_weights("model.h5")

if __name__ == '__main__':
    train()
