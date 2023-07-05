#!/usr/bin/python3
from vHtestingFunctions import getPerfMetrics, predict, scoreSequence
import sys
import pickle, gzip
import pandas as pd
import pickle, gzip

#name of the .pkl.gz file containing the PSWM
weightMatrix = sys.argv[1]
#.tsv file where 1st column is the class, 2nd column is the sequence, 3rd column is sequence annotated for SP
benchmarkDataset = sys.argv[2]
cvOutput = sys.argv[3] # the .tsv file containing the thresholds and perf metrics of the CV procedure
    
# obtaining the threshold as mean of threshold yielded in each iteration of CV
cvDF = pd.read_csv(cvOutput, delimiter="\t")
threshold = cvDF["Threshold"].mean()

wghtMat=pickle.load(gzip.open(weightMatrix,"r"))
aaDct = pickle.load(gzip.open("aasDict.pkl.gz","r"))

# extracting real classes
benchmarkDF = pd.read_csv(benchmarkDataset, delimiter="\t", names=["Class","Sequence","Annotated-seq"])
realCls = benchmarkDF["Class"].tolist()
for i in range(len(realCls)):
    if realCls[i] == "SP":
        realCls[i] = 1
    elif realCls[i]=="NO_SP":
        realCls[i] = 0

# predicting the benchmark dataset
predictions = predict(benchmarkDataset, threshold, wghtMat, aaDct)
# caluclating perf metrics
accuracy, MCC, f1, precision, recall = getPerfMetrics(realCls, predictions)

# writing the results into a file
perfMatrics={
    "Threshold" : round(threshold, 4),
    "Accuracy" : round(accuracy, 4),
    "MCC" : round(MCC, 4),
    "F1" : round(f1, 4),
    "Precision" : round(precision, 4),
    "Recall": round(recall, 4)
}
metricsDF = pd.DataFrame(perfMatrics, index=[0])
metricsDF.to_csv("benchmarkDataSetResults.tsv", sep="\t", mode="w", index=False, header=True)

pickle.dump(predictions, gzip.open('vHbenchmarkPredictedClasses.pkl.gz', 'w'))
