##### Introduction

Protein disorder is a feature of protein polypeptide chains where subsequences
of the residue chain do not conform to either helix or sheet structures, and instead
display random looping. Protein structure usually falls into either two helix
or sheet conformations, but new research indicates that the unordered (or looped)
regions may have important functional roles. For more information please see
[here](https://www.biorxiv.org/content/early/2017/06/01/144840). Understanding protein structure and protein disorder may allow for future important discoveries.

A recently released [database](https://github.com/PeptoneInc/dspp-keras) contains data on protein disorder for over 7500 protein sequences. For each residue in the sequence, a decimal between 1 and 3 is assigned. A 1 indicates that the residue
is most often part of a sheet structure, a 3 indicates that the residue is most
often part of a helix structure, and a 2 indicates that the residue is most often
in a state of disorder. This data is called the structural propensity of the protein,
as each number gives the propensity of a particular residue in the protein sequence
to conform to a particular structure.

Using this database, a neural network was trained to predict the structural
propensity of a given protein sequence.


##### Requirements

This code requires Python 3, and assumes that Keras and Tensorflow are installed. Other required libaries are numpy and matplotlib.

##### Training

The model is trained using the train.py script. To execute this script simply run:

```

python train.py

```

Training parameters are noted in the script and can be altered. If you wish to keep the model (model.h5) provided in the repository, please alter the name of the saved model, at the bottom of the train.py script.

##### Predictions

Predictions can be made using the inference.py script. Simply alter the protein sequence which you want to predict and execute:

```

python inference.py

```

This will output the prediction as a plot of protein residue propensity
