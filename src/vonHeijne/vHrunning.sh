#!/bin/bash

mkdir ./CV
mkdir ./PSWMs
cp ../../datasets/aa-composition-uniprot.txt .

# Cross validation
for i in 0 1 2 3 4
do 	
	#extracting the cross-fold used for training
	tail -n 1723 ../../datasets/training_set.tsv | cut -f 4,5,6,7 |grep -F "$i"|cut -f 1,3,4 >./CV/"$i"cf.tsv
	#extracting all other cross-folds for testing
	tail -n 1723 ../../datasets/training_set.tsv |cut -f 4,5,6,7 | grep -v "$i"|cut -f 1,3,4 >./CV/"$i"CViter.tsv
	# getting the weight matrix of the training CF
	./vHtrain.py ./CV/"$i"cf.tsv aa-composition-uniprot.txt ./PSWMs/"$i"PSWM
	# getting the threshold and predicting on the rest of the cross-folds
	./vHtestCV.py ./PSWMs/"$i"PSWM.pkl.gz ./CV/"$i"cf.tsv ./CV/"$i"CViter.tsv
done

# formating full training dataset
tail -n 1723 ../../datasets/training_set.tsv | cut -f 4,6,7 >final_training_set.tsv

# getting the weight matrix of the entire training dataset
./vHtrain.py final_training_set.tsv aa-composition-uniprot.txt ./PSWMs/finalPSWM

# formating the benchmark dataset
tail -n 7456 ../../datasets/benchmark_set.tsv | cut -f 4,5,6 >final_benchmark_set.tsv

# testing on the benchmark dataset
./vHBenchmarkTest.py ./PSWMs/finalPSWM.pkl.gz final_benchmark_set.tsv crossValidationMetrics.tsv
