# Branch Predictor
This repository is used to survey different branch predicting methods. 

The **cPredictor** folder contains the C code to examine results on static branch predictors, 1 bit branch predictors, 2 bit saturating branch predictors, globally shared predictors, and tournament predictors.
*To run:*
* run `make`
* call `./predictors <inFile> <outFile>` 
* `<inFile>` is the input file containing simulated branch outcomes (address, 1/0) 1= taken, 0 = not taken
* `<outfile>` prints the results
* `mcf_branch` and `gcc_branch` are placed in there as example input files

The **regular** folder contains a python script to test 2 level adaptive predictors.
*To run:*
* call `python sim.py`
* it will run a branch predictor simulation on `mcf_branch` and `gcc_branch`

The staticNN folder

The adaptiveNN folder
