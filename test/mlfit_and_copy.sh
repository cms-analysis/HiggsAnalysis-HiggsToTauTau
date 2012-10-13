#!/bin/bash

# ML-fit a directory of datcards and copy here for making plots
# Usage: ./mlfit_and_copy.sh $CMSSW_BASE/src/MY-LIMITS/125

set -o nounset
set -o errexit

type=$1
dir=$2

echo "Fitting $type : $dir"
if [ "$type" == "SM" ]; then
    limit.py --max-likelihood --stable --rMin -5 --rMax 5 $dir
    
    mkdir -p datacards
    mkdir -p root
    mkdir -p fitresults
    
    cp -v $dir/out/mlfit.txt ./fitresults/mlfit_sm.txt
    cp -v $dir/*.txt ./datacards
    cp -v $dir/../common/*.root ./root
fi
if [ $type == "MSSM" ]; then
    limit.py --max-likelihood --stable --rMin -5 --rMax 5 $dir
    
    mkdir -p datacards
    mkdir -p root
    mkdir -p fitresults
    
    cp -v $dir/out/mlfit.txt ./fitresults/mlfit_mssm.txt
    cp -v $dir/*.txt ./datacards
    cp -v $dir/../common/*TeV-0.root ./root
fi