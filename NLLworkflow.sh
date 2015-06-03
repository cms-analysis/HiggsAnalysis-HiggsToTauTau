#!/bin/zsh

#signal sample (500,30)
rm $CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root
hadd $CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root $CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/*/NLL*.root
root -l -b -q '$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/macros/NLLAnalysis.C("$CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root")'
python HiggsAnalysis/HiggsToTauTau/scripts/multidimNLL.py --nll-path="$CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-ggH-bbH/" --ggH-bbH-path-asimov="$CMSSW_BASE/src/LIMITS150512-mssm/bbb-asimov-ggH-bbH/" --nll-offset="1042244.16"
root -l -b -q '$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/macros/NLLPlot.C("$CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root")'
#BG only
#rm $CMSSW_BASE/src/LIMITS150512-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root
#hadd $CMSSW_BASE/src/LIMITS150512-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root $CMSSW_BASE/src/LIMITS150512-mssm/bbb-asimov-mhmodp-NLL/mt/*/NLL*.root
#root -l -b -q '$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/macros/NLLAnalysis.C("$CMSSW_BASE/src/LIMITS150512-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root")'
#python HiggsAnalysis/HiggsToTauTau/scripts/multidimNLL.py --nll-path="$CMSSW_BASE/src/LIMITS150512-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS150512-mssm/bbb-asimov-ggH-bbH/" --ggH-bbH-path-asimov="$CMSSW_BASE/src/LIMITS150512-mssm/bbb-asimov-ggH-bbH/" --nll-offset="1039364.57"
#root -l -b -q '$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/macros/NLLPlot.C("$CMSSW_BASE/src/LIMITS150512-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root")'
#sigmal sample (500,5)
#rm $CMSSW_BASE/src/LIMITS150527-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root
#hadd $CMSSW_BASE/src/LIMITS150527-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root $CMSSW_BASE/src/LIMITS150527-mssm/bbb-asimov-mhmodp-NLL/mt/*/NLL*.root
#root -l -b -q '$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/macros/NLLAnalysis.C("$CMSSW_BASE/src/LIMITS150527-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root")'
#python HiggsAnalysis/HiggsToTauTau/scripts/multidimNLL.py --nll-path="$CMSSW_BASE/src/LIMITS150527-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS150527-mssm/bbb-asimov-ggH-bbH/" --ggH-bbH-path-asimov="$CMSSW_BASE/src/LIMITS150512-mssm/bbb-asimov-ggH-bbH/" --nll-offset="1042244.16"
#root -l -b -q '$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/macros/NLLPlot.C("$CMSSW_BASE/src/LIMITS150527-mssm/bbb-asimov-mhmodp-NLL/mt/NLLHistogram.Full.root")'
