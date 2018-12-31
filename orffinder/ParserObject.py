'''
Class to store and parse DNA information from FASTA files
'''
from SequenceObject import SequenceObject

def line_generator(path):
    '''
    Generator to read in files given a path
    '''
    for line in open(path):
        yield line

def verify_description(line):
    '''
    Verifies whether or not a FASTA description line is not empty space
    '''
    if line[1] is not " ":
        result = True
    else:
        result = False
    return result

def verify_sequence(line):
    '''
    Verfies whether FASTA sequence information contains only valid characters
    '''
    valid_chars = 'ABCDEFGHIJKLMNPQRSTUVWXYZ*-'
    result = all(x in valid_chars for x in line)
    return result

class ParserObject:

    def __init__(self, file_path):
        self.file_path = file_path
        self.gen = line_generator(file_path)
        self.objects = []

    def multiple_descriptions(self, line):
        '''
        Fasta files can have multiple descriptions, meaning descriptions
        without sequences, this parses those descriptions into SequenceObjects
        with empty sequence lines
        '''
        multi_desc = line.split('>')
        for i in multi_desc[:-1]:
            x = SequenceObject(desc=i,seq='').SequenceTuple
            self.objects.append(x)
        return multi_desc[-1]

    def file_parser(self):
        '''
        Parses a FASTA file for sequence information
        '''
        current_seqobj = SequenceObject()

        try:
            while True:
                # case handling that calls functions to examine sequences
                line = next(self.gen)
                if line.endswith('\n'):
                    line = line.replace('\n',"") # strip new line character from string
                if line.startswith('>'): # description line
                    if current_seqobj.desc != [None]:
                        current_seqobj.desc = [x for x in current_seqobj.desc if
                                               x is not None]
                        current_seqobj.desc = ''.join(current_seqobj.desc)
                        current_seqobj.seq = [x for x in current_seqobj.seq if x
                                              is not None]
                        current_seqobj.seq = ''.join(current_seqobj.seq)
                        self.objects.append(current_seqobj.SequenceTuple())
                    if verify_description(line):
                        line = line[1:] # drop first identifier as it is not needed
                        if line.count('>') > 1:
                            x = multiple_descriptions(line)
                            current_seqobj = SequenceObject(desc=x)
                        else:
                            current_seqobj = SequenceObject(desc=line)
                    else: # bad description, so we will skip the sequence data as well
                        print('Invalid Description:  File not in FASTA format')
                else:
                    # line may be part of a multi-line description
                    if ' ' in line:
                        current_seqobj.desc.append(line)
                    elif line == '':
                        # Empty Line Found in Sequence
                        pass
                    else:
                        # the line may be a sequence, check if line is a valid sequence
                        line = line.upper()
                        if verify_sequence(line) and current_seqobj.desc != [None]:
                            current_seqobj.seq.append(line)
        except StopIteration: #catch iterator exception, format last output and append
            if current_seqobj.desc != [None]:
                current_seqobj.desc = [x for x in current_seqobj.desc if x is not None]
                current_seqobj.desc = ''.join(current_seqobj.desc)
                current_seqobj.seq = [x for x in current_seqobj.seq if x is not None]
                current_seqobj.seq = ''.join(current_seqobj.seq)
                self.objects.append(current_seqobj.SequenceTuple())

    def sequence_printer(self):
        '''
        Prints parsed sequence information
        '''
        for i in self.objects:
            print(i[0] + ' | ' + i[1])
