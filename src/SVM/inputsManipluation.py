#!/usr/bin/python3
import pandas as pd
import numpy as np
import re
import sys


def getK(dataFile):
    ''''FUnction takes a tsv file containing the input data, and extracts the average lenght of the signal peptide'''
    data = pd.read_csv(dataFile, delimiter='\t')
    protsWSV = data[data["Class"] == 'SP']
    numberOfSVs = 0
    totalLengthSVs = 0
    for row in protsWSV.itertuples():
        numberOfSVs += 1
        for char in row[-1]:
            if char == 'S':
                totalLengthSVs += 1
            else:
                break
    return totalLengthSVs/numberOfSVs


def getAAtoNumDict(aaFile):
    pattern = "\([A-Z]{1}\)"
    aaDict = {}
    with open(aaFile) as f:
        i = 0
        for line in f:
            x = re.search(pattern, line)
            aaDict[x.group()[1]] = i
            i += 1
    return aaDict


def encodeSequences(dataFile, k, aaOrderDict):
    '''Function takes a file with input data and returns a bidimensional numpy array containing the encoded 
    sequences and anothed numpy array containing the corresponing classes of the data'''
    data = pd.read_csv(dataFile, delimiter='\t')
    data.loc[data['Class'] == 'SP', 'Class'] = 1
    data.loc[data['Class'] == 'NO_SP', 'Class'] = 0
    dataClasses = np.array(data['Class'].tolist())

    encodedSequences = []
    for sequence in data['Sequence (first 50 N-terminal residues)']:
        # vector of length 20, where each field corresponds to an amino acid
        codedSeq = np.zeros(20)
        # geting frequencies of each aa in the k-mer
        for char in sequence[0:k]:
            codedSeq[aaOrderDict[char]] += 1
        codedSeq = codedSeq/k
        encodedSequences.append(codedSeq)
    encoding = np.stack(encodedSequences)
    return encoding, dataClasses
