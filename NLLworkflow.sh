#!/bin/zsh
rm $CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root
hadd $CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root $CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/*/NLL*.root
root -l -b -q '$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/macros/NLLAnalysis.C("$CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root")'
cp $CMSSW_BASE/src/xs_boundaries.txt $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/scripts/
python $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/scripts/adjust_mssm_multidimfit_boundaries.py
rm $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/scripts/xs_boundaries.txt
rm $CMSSW_BASE/src/xs_boundaries.txt