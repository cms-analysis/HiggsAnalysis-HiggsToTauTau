#!/bin/zsh

#signal sample (500,30)
rm $CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root
hadd $CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root $CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/*/NLL*.root
root -l -b -q '$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/macros/NLLAnalysis.C("$CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root")'
cp $CMSSW_BASE/src/xs_boundaries.txt $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/scripts/
python $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/scripts/adjust_mssm_multidimfit_boundaries.py
rm $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/scripts/xs_boundaries.txt
rm $CMSSW_BASE/src/xs_boundaries.txt
python HiggsAnalysis/HiggsToTauTau/scripts/multidimNLL.py --nll-path="$CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-ggH-bbH/" --ggH-bbH-path-asimov="$CMSSW_BASE/src/LIMITS150512-mssm/bbb-asimov-ggH-bbH/"
root -l -b -q '$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/macros/NLLPlot.C("$CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root")'
root -l -b -q '$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/macros/NLLPlot.C("$CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root", true)'
