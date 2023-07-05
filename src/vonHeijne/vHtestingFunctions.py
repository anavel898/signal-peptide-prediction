#!/usr/bin/python3

import numpy as np 
from sklearn.metrics import precision_recall_curve
import pandas as pd
from math import sqrt

def scoreSequence(weightsMatrix, sequence, aasCodes):
    '''Slides a window of length 15 over the input sequence, and scores each subsequence. Returns the best score'''
    scoresList = []
    i=0
    while i <= (len(sequence)-15):
        score = 0
        pos = 0
        for residue in sequence[i:(i+15)]:
            #print("Uslo u for petlju")
            column = aasCodes[residue]
            score= score + weightsMatrix.item(pos,column)
            pos +=1
        scoresList.append(score)
        i+=1
    #print(i)
    #print("NUMBER OF SLIDING WINDOW POSITIONS: "+str(len(scoresList)))
    return max(scoresList)

def getOptimalThreshold(scores, classes):
    '''Takes arrays of sequence scores and their true classes, and using a precission recall curve
      returns the optimal threshold'''
    optThr = 0
    precision, recall, thresholds = precision_recall_curve(classes, scores)
    fscore = (2*precision*recall)/(precision+recall)
    index = np.argmax(fscore)
    optThr = thresholds[index]
    return optThr

def getPerfMetrics(realClasses, predictedClasses):
    '''Takes arrays of true classes and predicted classes of data points, and caluclates permormance metrics'''
    TP, TN, FP, FN = 0,0,0,0
    for real, pred in zip(realClasses, predictedClasses):
        if real == pred and real == 1:
            TP += 1 
        elif real == pred and real == 0:
            TN += 1
        elif real != pred and real == 1:
            FN += 1
        elif real != pred and real == 0:
            FP +=1
    
    ACC = (TP+TN)/(TP+TN+FP+FN)
    precs = TP/(TP+FP)
    recl = TP/(TP+FN)
    F1 = (2*precs*recl)/(precs+recl)
    MCC = (TP*TN-FP*FN)/sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
    return ACC, MCC, F1, precs, recl 

def predict(testingFile, thr, weights, aasDict):
    '''Returns an array containing the predicted classes of sequences in a .tsv file'''
    testSet = pd.read_csv(testingFile, delimiter="\t", names=["Class","Sequence","Annotated-seq"])
    predictedClasses = []
    for sequence in testSet["Sequence"]:
        score = scoreSequence(weights, sequence, aasDict)
        if score >= thr:
            predictedClasses.append(1)
        else:
            predictedClasses.append(0)
    return predictedClasses
