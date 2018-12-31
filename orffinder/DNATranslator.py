'''
Class to transcribe DNA into protein sequences
'''

# dicts containing DNA to protein mappings
antisense_dict = {'A':'T', 'G':'C', 'C':'G','T':'A'}
transcription_dict = {'A':'A', 'G':'G', 'C':'C','T':'U'}
translation_dict = {
'I': ['AUU', 'AUC', 'AUA'],
'L': ['CUU', 'CUC', 'CUG', 'CUA', 'UUA', 'UUG'],
'V': ['GUU', 'GUC', 'GUA', 'GUG'],
'F': ['UUU', 'UUC'],
'M': ['AUG'],
'C': ['UGU', 'UGC'],
'A': ['GCU', 'GCC', 'GCA', 'GCG'],
'G': ['GGU', 'GGC', 'GGA', 'GGG'],
'P': ['CCU', 'CCC', 'CCA', 'CCG'],
'T': ['ACU', 'ACC', 'ACA', 'ACG'],
'S': ['UCU', 'UCC', 'UCA', 'UCG', 'AGU', 'AGC'],
'Y': ['UAU', 'UAC'],
'W': ['UGG'],
'Q': ['CAA', 'CAG'],
'N': ['AAU', 'AAC'],
'H': ['CAU', 'CAC'],
'E': ['GAA', 'GAG'],
'D': ['GAU', 'GAC'],
'K': ['AAA', 'AAG'],
'R': ['CGU', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'],
'-': ['UAA', 'UAG', 'UGA']}

def transcribe(seq, transcription_dict):
    '''
    Transcribes a DNA sequence into RNA
    '''
    return [transcription_dict[i] for i in seq]

def protein_code(codon, translation_dict):
    '''
    Translates a codon into Protein
    '''
    for x in translation_dict:
        if codon in translation_dict[x]:
            return x

def translator(frame, start, end):
    '''
    Translate sequence of RNA into proteins
    '''
    trans_str = frame[start:end+1]
    output = [protein_code(x, translation_dict) for x in trans_str]
    out = ''.join(output)
    return out

class DNATranslator:

    def __init__(self, desc, seq):
        self.desc = desc
        self.seq = seq
        self.transcription = None
        self.reading_frames = []
        self.orfs = []

    def reading_frame_maker(self):
        '''
        Given a sequence, there are six possible positions that a DNA strand
        could be read from: 1, 2, 3, -1, -2, -3. These are the first three and
        last three positions, defining six sequences called reading frames. This
        function builds reading frames. Sense refers to reading frames starting
        on the left side of the sequence, anti-sense to those starting on the
        right.
        '''
        sense = [x for x in self.seq]
        sense_transcribed = [transcription_dict[x] for x in sense] #to mRNA
        pre_antisense = [x for x in self.seq]
        pre_antisense.reverse()
        antisense = [antisense_dict[x] for x in pre_antisense]
        antisense_transcribed = [transcription_dict[x] for x in antisense] #to mRNA

        # now we examine mRNA reading frames for translation
        # define position index list
        pos = [1,2,3,-1,-2,-3]
        # given a start position, divide sequence into list of triples, discard
        # last item in list if length is not 3
        for i in pos:
            if i > 0:
                # sense strand
                j = i-1
                to_translate = sense_transcribed[j:]
            else:
                # antisense strand
                j = (i*-1)-1
                to_translate = antisense_transcribed[j:]
            trans = "".join(to_translate)
            # now i divide string into chunks for reading frame search
            # solution for dividing a string into chunks adapted from
            frame = [trans[0+i:i+3] for i in range(0, len(trans), 3)]
            #we have to drop the last item in this list if it does not have length 3
            if len(frame[-1]) != 3:
                frame = frame[:-1]
            self.reading_frames.append((i,frame))

    def orf_finder(self):
        '''
        Given a reading frame, DNA can be translated into a Protein sequence
        if an open reading frame is found, that is a reading frame that has a
        particular "start" and "stop" amino acid present in the reading frame in
        that order. The open reading frame is then the subsequence defined by
        [start, stop].
        '''
        for x in self.reading_frames:
            position = x[0]
            frame = x[1]
            for i,j in enumerate(frame):
                if j == 'AUG': # start codon
                    start = i
                    # now find the stop codon index
                    sub_frame = frame[i:]
                    for y,z in enumerate(sub_frame):
                        if z in ['UAA', 'UAG', 'UGA']: # stop codon
                            end = i+y-1
                            break
                        elif y == (len(sub_frame)-1):
                            end = i+y
                    if (start<=end): # to catch bug that was happeneing at end of file
                        protein = translator(frame, start, end)
                        start_base = (start) * 3 + 1 + (abs(position)-1)
                        stop_base = start_base + len(protein)*3 - 1
                        orf = (position, start_base, stop_base, len(protein), protein)
                        self.orfs.append(orf)

    def orf_printer(self):
        '''
        Print found open reading frames as: start, stop, length of protein, protein
        '''
        for orf in self.orfs:
            print('* {} | {} | {} | {} | {}'.format(orf[0], orf[1], orf[2], orf[3],
                  orf[4]))

def orf_print(dna):
    #takes a ParserObject as input
    for obj in dna.objects:
        desc = obj[0]
        seq = obj[1]

        dna_object = DNATranslator(desc, seq)

        #dna_object.transcribe(transcription_dict)
        dna_object.reading_frame_maker()
        dna_object.orf_finder()

        for orf in dna_object.orfs:
            orf_printer(orf)
