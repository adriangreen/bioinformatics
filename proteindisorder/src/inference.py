# script to run inferences given model
# takes in a protein sequence as a string

from model import model
from utilities import convert_string, string_for_inference
from matplotlib import pyplot as plt
import numpy as  np

def normalize(x):
    xmax = max(x)
    xmin = min(x)
    out = []
    for i in x:
        z = 2 * (i - xmin)/(xmax - xmin) - 1
        out.append(z)
    return out

def inference():
    maxlen = 800
    nnet = model(maxlen)
    nnet.load_weights('model.h5')

    # using sequence from https://peptone.io/dspp/entry/dSPP7014_0
    sequence = 'GHVQLSLPVLQVRDVLVRGFGDSVEEALSEAREHLKNGTCGLVELEKGVLPQLEQPYVFIKRSDALSTNHGHKVVELVAEMDGIQYGRSGITLGVLVPHVGETPIAYRNVLLRKNG'
    protein_name = 'SARS-CoV protein nsp1'
    seq_array = convert_string(sequence)
    processed_sequence = string_for_inference(seq_array, maxlen)
    pred = nnet.predict(processed_sequence)

    # clip the padded zeros from the prediction output and input
    predicted_disorder = pred[0][-(len(sequence)):]
    sequence_data = [i for i in sequence]
    positions = [i for i in range(len(sequence))]

    #normalize predicted_disorder between 1 and -1 to match database
    normalized_disorder = normalize(predicted_disorder)

    plt.bar(positions, predicted_disorder)
    plt.title('Predicted Structural Disorder of {}'.format(protein_name))
    plt.xlabel('Residue Number')
    plt.ylabel('Disorder')
    #plt.xticks(positions, sequence_data)
    plt.show()

if __name__ == '__main__':
    inference()
