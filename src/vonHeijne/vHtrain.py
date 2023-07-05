#!/usr/bin/python3

import sys
import re
import numpy as np
from math import log2
import pandas as pd
import pickle, gzip

def getAAdicts(file):
    '''Takes as input a .txt file containg aminoacid composition of a database, returns a dictionary containing said background composition, 
    a dictionary encoding aminoacids to numbers and a corresponding dictionry mapping numbers to aminoacids'''
    aasAsNumbersDict = {}
    numbersAsAAsDict = {}
    backgroundAA = {}
    with open(file, 'r') as f:
        regex = "\([A-Z]\)"
        percentage_regex = "[0-9]*\.[0-9]*"
        i = 0
        for line in f:
            x = re.search(regex, line)
            y = re.search(percentage_regex,line)
            numbersAsAAsDict[i] = x.group()[1]
            backgroundAA[x.group()[1]] = float(y.group())/100  #dividing by 100 because in the input file frequencies are expresed as %, and I want them in range 0-1
            aasAsNumbersDict[x.group()[1]] = i
            i += 1
    return aasAsNumbersDict, numbersAsAAsDict, backgroundAA

def seqToNumeric(sequence, aas_code):
    '''Takes a string and a dictionary enocidng all letters of alphabet as numbers, and returns a string where each character is 
    now the corresponding number'''
    encodedSeq = []
    for residue in sequence:
        encodedSeq.append(aas_code[residue])
    return encodedSeq

def getMotif(trainingDSFile):
    '''Extracts the 15aa long motif around the cleavage sites'''
    motifesList = []
    trainingDF = pd.read_csv(trainingDSFile, delimiter="\t", names=["Class","Sequence","Annotated-seq"])
    trainingPositives = trainingDF[trainingDF["Class"] == "SP"]   #extracting positive sequences out of the training dataset
    for seq,entry in zip(trainingPositives["Sequence"], trainingPositives["Annotated-seq"]):
        clSite = 0
        for char in entry:    
            if char == "S":
                clSite += 1
            else:
                break
        motif = seq[(clSite-13):(clSite+2)] #extracting [-13,+2] motif
        motifesList.append(motif)
    return motifesList

def getProbabilityMatrix(motifes_list, length_of_motif, aas_code):
    probMatrix = np.matrix([[1 for i in range(20)] for j in range(length_of_motif)]) #initializing a matrix of size 20xlength-of-motif with 1s for pseudocounts
    for sequence in motifes_list:
        encodedSeq = seqToNumeric(sequence, aas_code)
        seqMatrix = np.matrix([[0 for i in range(20)] for j in range(length_of_motif)]) #matrix in which sequences are one-hot encoded
        position = 0
        for residue in encodedSeq:
            seqMatrix[position, int(residue)] += 1 
            position +=1
        probMatrix = probMatrix+seqMatrix
    probMatrix = probMatrix/(len(motifes_list)+20)
    return probMatrix

def getWeightsMatrix(probMatrix, length_of_motif, backgroundAA, numToAA):
    weightsMatrix  = np.matrix([[float(0) for i in range(20)] for j in range(length_of_motif)])
    for i in range(length_of_motif):
        for j in range(20):
            backgFreq = backgroundAA[numToAA[j]]
            value = log2(probMatrix.item(i,j)/backgFreq)
            weightsMatrix.itemset((i,j), value)
    return weightsMatrix


if __name__ == '__main__':
    trainingFile = sys.argv[1]
    aasBackground = sys.argv[2] 
    outputName = sys.argv[3]

    motifes = getMotif(trainingFile)
    aasToNum, numsAsAAs, backgroundFreq = getAAdicts(aasBackground)
    probMatrix = getProbabilityMatrix(motifes, 15, aasToNum)
    wghtMatrix = getWeightsMatrix(probMatrix, 15, backgroundFreq, numsAsAAs)
    file = open(str(outputName), 'w')
    to_write = str(wghtMatrix)
    file.writelines(str(wghtMatrix))

    pickle.dump(wghtMatrix, gzip.open(outputName+".pkl.gz","w"))
    pickle.dump(aasToNum, gzip.open("aasDict.pkl.gz", "w"))
