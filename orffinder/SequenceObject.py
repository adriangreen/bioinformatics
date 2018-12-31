'''
Class to store sequence and description information for DNA sequences
parsed from FASTA file
'''

class SequenceObject:

    def __init__(self, desc=None, seq=None):
        '''
        desc stores the description line of a FASTA file, seq stores the
        sequence
        '''
        self.desc = [desc]
        self.seq = [seq]

    def SequenceTuple(self):
        return (self.desc, self.seq)
