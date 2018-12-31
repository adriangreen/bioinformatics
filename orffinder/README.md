# Introduction

This file contains code that processes DNA information downloaded in FASTA
format from the NCBI website. A FASTA file is a format used to store DNA or
protein sequence information as follows:
```
>description line
ASDFASDFASDFASDFAFSDASDFASDASDFASDF
```
Sequence information is preceded by a description line delimited with >. This
code downloads a FASTA file from the NCBI website and mimics two biological processes:  transcription and translation. Transcription is the mapping of a DNA sequence to its RNA counterpart. Translation is mapping of RNA into its corresponding protein. Translation can begin at any one of six positions (the first or last three translation units in the sequence), and proceed from left to right (from the first three units) or from right to left (from the last three units). This code prints all possible protein sequences that are found in the downloaded DNA information.

This code is intended to mimic the functionality of Bioinformatics software

# Requirements
This code requires Python 3

# Usage
To run the code, use the following command:

```
python main.py accesion_number_argument
```
