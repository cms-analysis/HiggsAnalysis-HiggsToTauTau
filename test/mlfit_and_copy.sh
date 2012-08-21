#!/bin/bash

# ML-fit a directory of datcards and copy here for making plots
# Usage: ./mlfit_and_copy.sh path/to/datacard/mass/dir

set -o nounset
set -o errexit

dir=$1

echo "Fitting $dir"
limit.py --max-likelihood --stable --rMin -5 --rMax 5 $dir

mkdir -p datacards
mkdir -p root
mkdir -p fitresults

cp -v $dir/out/mlfit.txt ./fitresults/mlfit_sm.txt
cp -v $dir/*.txt ./datacards
cp -v $dir/../common/*.root ./root
