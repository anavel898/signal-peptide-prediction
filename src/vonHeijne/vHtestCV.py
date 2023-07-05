#!/usr/bin/python3

from vHtestingFunctions import scoreSequence, getOptimalThreshold, getPerfMetrics, predict
from sklearn.metrics import precision_recall_curve
import sys
import pickle, gzip
import pandas as pd

#name of the .pkl.gz file containing the PSWM
weightMatrix = sys.argv[1]
# .tsv files where 1st column is the class, 2nd column is the sequence, 3rd column is sequence annotated for SP
trainingFile = sys.argv[2]  # one CF from which the weight matrix was calculated
testFile = sys.argv[3]  # all other CFs which we will predict

wghtMat=pickle.load(gzip.open(weightMatrix,"r"))
aaDct = pickle.load(gzip.open("aasDict.pkl.gz","r"))

trainingScores = []
realClasses = []
    
with open(trainingFile,'r') as f:
    for entry in f:
        seq = entry.split("\t")[1]
        trainingScores.append(scoreSequence(wghtMat, seq, aaDct))
        if entry.split("\t")[0] == "SP":
            realClasses.append(1)   
        elif entry.split("\t")[0] == "NO_SP":
            realClasses.append(0)
    
threshold = getOptimalThreshold(trainingScores, realClasses)
classPredictions = predict(testFile, threshold, wghtMat, aaDct)
accuracy, MCC, f1, precision, recall = getPerfMetrics(realClasses, classPredictions)

perfMatrics={
    "Threshold" : round(threshold, 4),
    "Accuracy" : round(accuracy, 4),
    "MCC" : round(MCC, 4),
    "F1" : round(f1, 4),
    "Precision" : round(precision, 4),
    "Recall": round(recall, 4)
}

metricsDF = pd.DataFrame(perfMatrics, index=[0])
# appending the metrics to a .tsv file containing appropriate column names 
metricsDF.to_csv("crossValidationMetrics.tsv", sep="\t", mode="a", index=False, header=False)
