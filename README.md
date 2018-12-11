# Branch Predictor
This repository is used to survey different branch predicting methods. 

## cPredictor
The **cPredictor** folder contains the C code to examine results on static branch predictors, 1 bit branch predictors, 2 bit saturating branch predictors, globally shared predictors, and tournament predictors.
*To run:*
* run `make`
* call `./predictors <inFile> <outFile>` 
* `<inFile>` is the input file containing simulated branch outcomes (address, 1/0) 1= taken, 0 = not taken
* `<outfile>` prints the results
* `mcf_branch` and `gcc_branch` are placed in there as example input files

## regular
The **regular** folder contains a python script to test 2 level adaptive predictors.
*To run:*
* call `python sim.py`
* it will run a branch predictor simulation on `mcf_branch` and `gcc_branch`

## staticNN
The **staticNN** folder contians a pythons script for a feedForward neural net that will train a branch simulation file.
*To run:*
* call `python staticNN.py`
* it will run a branch predictor simulation on `gcc_branch` and output the accuracy as it trains
* note that training can take up to an hour with a large file like gcc_branch
* `mcf_branch` and `gcc_branch` are placed in there as example input files

## adaptiveNN
The adaptiveNN folder
