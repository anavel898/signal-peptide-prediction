#!/usr/bin/python3

from inputsManipluation import encodeSequences, getAAtoNumDict
import pickle
import gzip
import pandas as pd
import numpy as np
import sys
import re
from sklearn.svm import SVC
from sklearn.metrics import *


def getPerfMatrics(Y_true, Y_pred):
    acc = accuracy_score(Y_true, Y_pred)
    mcc = matthews_corrcoef(Y_true, Y_pred)
    prec = precision_score(Y_true, Y_pred)
    recl = recall_score(Y_true, Y_pred)
    f1 = f1_score(Y_true, Y_pred)
    return acc, mcc, prec, recl, f1


if __name__ == "__main__":
    data = sys.argv[1]
    aas = sys.argv[2]
    trainedModel = sys.argv[3]

    hyperperams = pd.read_csv("optimalHyperparams.tsv", delimiter="\t")
    k = int(hyperperams["K"].values[0])
    
    # extracting the real classes and encoding the sequences in the dataset
    X_vec, Y_real = encodeSequences(data, k, getAAtoNumDict(aas))
    
    # predicting the benchmark dataset using the trained model
    mySVC = pickle.load(gzip.open(trainedModel, 'r'))
    Y_predicted = mySVC.predict(X_vec)

    # saving the array of predicted classes for result analysis
    pickle.dump(Y_predicted, gzip.open('SVMpredictedClasses.pkl.gz', 'w'))

    #geting and saving the final perf metrics
    ACC, MCC, precision, recall, f1 = getPerfMatrics(Y_real, Y_predicted)
    perfsDict = {
        "Accuracy": round(ACC, 4),
        "MCC": round(MCC, 4),
        "F1": round(f1, 4),
        "Precision": round(precision, 4),
        "Recall": round(recall, 4)
    }
    perfDF = pd.DataFrame(perfsDict, index=[0])
    perfDF.to_csv("SVMbenchmarkResults.tsv", sep="\t",
                  mode="w", index=False, header=True)
