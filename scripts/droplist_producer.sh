#!/bin/bash

python HiggsAnalysis/HiggsToTauTau/scripts/doSM.py --update-all --label _droplist -a "bbb" 125
for i in em et mt tt
do
    submit.py --max-likelihood LIMITS_droplist/bbb/$i/125
done

for i in tt
do
    while true
    do
        if [ -s "LIMITS_droplist/bbb/$i/125/out/mlfit_largest-constraints.html" ]
        then
            python HiggsAnalysis/HiggsToTauTau/scripts/prune-uncerts-htt.py --threshold 0.05 --fit-results LIMITS_droplist/bbb/$i/125/out/mlfit.txt --whitelist "_bin_" --shielding 125:0.3 LIMITS_droplist/bbb/$i/125
            mv -v uncertainty-pruning-drop.txt uncertainty-pruning-drop_${i}.txt
            break
        fi
        sleep 15
    done
done
for i in em et mt
do
    while true
    do
        if [ -s "LIMITS_droplist/bbb/$i/125/out/mlfit_largest-constraints.html" ]
        then
            python HiggsAnalysis/HiggsToTauTau/scripts/prune-uncerts-htt.py --threshold 0.1 --fit-results LIMITS_droplist/bbb/$i/125/out/mlfit.txt --whitelist "_bin_" --shielding 125:0.3 LIMITS_droplist/bbb/$i/125
            mv -v uncertainty-pruning-drop.txt uncertainty-pruning-drop_${i}.txt
            break
        fi
        sleep 15
    done
done

#merge all droplists to one final droplist. The final name contains the current date.
cat uncertainty-pruning-drop_*.txt > uncertainty-pruning-drop-$(date +%y%m%d)-sm.txt

