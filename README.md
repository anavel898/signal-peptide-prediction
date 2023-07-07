# Comparison of signal peptide prediction methods

<h2>To run the prediction using the von Heijne algorithm:</h2>
<code>cd src/vonHeijne <br>
./vHrunning.sh</code>
<br>
The final preformance of the algorithm is written into the file: <code>benchmarkDataSetResults.tsv</code>

<h2>To run the precition using SVM:</h2>
<code>cd src/SVM <br>
./SVMrunning.sh</code>
<br>
Optimal values of hyperparameters can be found in the file: <code>optimalHyperparams.tsv</code>
The final preformance is written into the file: <code>SVMbenchmarkResults.tsv</code>
