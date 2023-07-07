# Comparison of signal peptide prediction methods

###Run the prediction using the von Heijne algorithm:
<code>cd src/vonHeijne  
./vHrunning.sh</code>
<br>
The final preformance of the algorithm is written into the file: <code>benchmarkDataSetResults.tsv</code>

###Run the prediction using SVM:
<code>cd src/SVM <br>
./SVMrunning.sh</code>
<br>
Optimal values of hyperparameters can be found in the file: <code>optimalHyperparams.tsv</code><br>
The final preformance is written into the file: <code>SVMbenchmarkResults.tsv</code>
