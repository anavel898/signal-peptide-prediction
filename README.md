# Comparison of signal peptide prediction methods
Signal peptides (SPs) are short amino acid sequences that control protein secretion and translocation in all living organisms. SPs can be predicted from sequence data. This project aimed to implement and compare two methods for SP prediction.

### Run the prediction using the von Heijne algorithm:  
<code>cd src/vonHeijne  
./vHrunning.sh</code>  
The final preformance of the algorithm is written into the file: <code>benchmarkDataSetResults.tsv</code>

### Run the prediction using SVM:
`cd src/SVM`  
`./SVMrunning.sh`  
Optimal values of hyperparameters can be found in the file: `optimalHyperparams.tsv`  
The final preformance is written into the file: `SVMbenchmarkResults.tsv`
