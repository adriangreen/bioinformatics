import sys
import urllib.request
from DNATranslator import *
from ParserObject import ParserObject

def orf_print(dna):
    '''
    Given DNA information, this function will print the possible protein
    sequences based on parsed open reading frames.
    '''
    for obj in dna.objects:
        desc = obj[0]
        seq = obj[1]
        dna_object = DNATranslator(desc, seq)
        dna_object.reading_frame_maker()
        dna_object.orf_finder()
        dna_object.orf_printer()

def accession_to_orf(accession_number):
    '''
    This function takes an NCBI accession number, downloads the associated gene
    sequences, parses the information from the resulting FASTA file and prints
    the possible protein sequences.
    '''
    api_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={}&rettype=fasta&retmode=text'.format(accession_number)
    file_name = accession_number + '.fa'
    urllib.request.urlretrieve(api_url, file_name)
    # now we will use our imported parser functions to find the ORFs
    # first we parse the file
    dna = ParserObject(file_name)
    dna.file_parser()
    orf_print(dna)

def main():
    accession_number = sys.argv[1]
    # accession_number = 'NM_005368.2'
    accession_to_orf(accession_number)

if __name__ == '__main__':
    main()
