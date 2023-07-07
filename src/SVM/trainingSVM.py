#!/usr/bin/python3

import pandas as pd
import numpy as np
import sys
import re
from sklearn.svm import SVC
from sklearn.metrics import matthews_corrcoef, make_scorer
from sklearn.model_selection import GridSearchCV, PredefinedSplit
from inputsManipluation import encodeSequences, getAAtoNumDict
import pickle
import gzip


def getCVindex(dataFile):
    df = pd.read_csv(dataFile, delimiter="\t")
    cvTagsList = df["Cross-validation fold"].tolist()
    cvFolds = PredefinedSplit(cvTagsList)
    return cvFolds


def getMCCscore(actual, predicted):
    MCC = matthews_corrcoef(actual, predicted)
    return MCC


if __name__ == "__main__":
    trainingData = sys.argv[1]
    aas = sys.argv[2]

    tuningDict = {}
    paramsDict = {}

    cvObj = getCVindex(trainingData)
    cVals = [1, 2, 4]
    gammaVals = [0.5, 1, 'scale']

    paramGrid = dict(C=cVals, gamma=gammaVals)

    gridScorer = make_scorer(getMCCscore, greater_is_better=True)
    scores = {"Accuracy": 'accuracy', "MCC": gridScorer,
              "F1": 'f1', "Precision": 'precision', "Recall": 'recall'}

    for k in [20, 22, 24]:  # doing a grid search for each of possible k values
        grid = GridSearchCV(estimator=SVC(), param_grid=paramGrid,
                            scoring=scores, cv=cvObj, refit='MCC')
        X, Y = encodeSequences(trainingData, k, getAAtoNumDict(aas))
        grid.fit(X, Y)

        # get the perf metrics for each cross-validation run for each combo of hyperparams
        resultsOfCV = grid.cv_results_
        resultsDF = pd.DataFrame.from_dict(resultsOfCV)
        fileName = 'csv-results-k-'+str(k)+'.csv'
        resultsDF.to_csv(fileName, index=False)

        tuningDict[k] = grid.best_score_
        paramsDict[k] = grid.best_params_

        # saving the best results of the grid search for each K in a separate tsv file
        gridResultDict = {
            "K": k,
            "MCC": grid.best_score_,
            "C": grid.best_params_['C'],
            "gamma": grid.best_params_['gamma']
        }
        gridResultDF = pd.DataFrame(gridResultDict, index=[0])
        gridResultDF.to_csv("gridSearchResults.tsv",
                            sep="\t", mode='a', header=True, index=False)

    KwithMaxMCC = max(tuningDict, key=tuningDict.get)

    optHyperpDict = {
        "K": KwithMaxMCC,
        "C": paramsDict[KwithMaxMCC]['C'],
        "gamma": paramsDict[KwithMaxMCC]['gamma']
    }
    optHypDF = pd.DataFrame(optHyperpDict, index=[0])
    optHypDF.to_csv("optimalHyperparams.tsv",
                    sep="\t", mode='w', header=True, index=False)
    
    # training and saving the model with the optimal hyperparameters
    mySVC = SVC(C=paramsDict[KwithMaxMCC]['C'], gamma=paramsDict[KwithMaxMCC]['gamma'])
    X_train, Y_train = encodeSequences(
        trainingData, int(KwithMaxMCC), getAAtoNumDict(aas))
    mySVC.fit(X_train, Y_train)
    pickle.dump(mySVC, gzip.open('myModel.pkl.gz', 'w'))
