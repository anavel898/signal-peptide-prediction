#!/usr/bin/bash

# hyperparameter tuning and training the model
.trainingSVM.py ../../datasets/training_set.tsv ../../datasets/aa-composition-uniprot.txt

# predicting the benchmark dataset
./predictionsSVM.py ../../datasets/benchmark_set.tsv ../../datasets/aa-composition-uniprot.txt myModel.pkl.gz

echo "Final model preformance:"
cat SVMbenchmarkResults.tsv
