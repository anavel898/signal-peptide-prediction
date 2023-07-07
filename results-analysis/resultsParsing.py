#!/usr/bin/python3

import pandas as pd
import sys
import pickle
import gzip


def getResultsDF(inputFile, predictionsList):
    '''Appends the array of predicted classes to the dataframe of the dataset'''
    resultDF = pd.read_csv(inputFile, delimiter='\t')
    resultDF.loc[resultDF["Class"] == 'SP', 'Class'] = 1
    resultDF.loc[resultDF['Class'] == 'NO_SP', 'Class'] = 0
    resultDF['Predicted-class'] = predictionsList
    return resultDF


if __name__ == "__main__":
    wholeDataset = sys.argv[1]  # the raw version of the dataset
    classPredictions = sys.argv[2]  # the pickled array of predicted classes
    # valid inputs are VH or SVM; argument used for naming output files
    method = sys.argv[3]

    listOfPredictions = pickle.load(gzip.open(classPredictions, 'r'))

    finalDF = getResultsDF(wholeDataset, listOfPredictions)
    fileName = method+"_benchmark_wpredictions.tsv"
    finalDF.to_csv(fileName, sep='\t', index=False, header=True, mode='w')
