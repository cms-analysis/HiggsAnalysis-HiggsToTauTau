#!/bin/zsh


#########Naive approach

#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-30fb/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-30fb/plain-asimov-ggH-bbH/" --model-masspoint="500-30-30fb"
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-25-30fb/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-25-30fb/plain-asimov-ggH-bbH/" --model-masspoint="500-25-30fb"
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-20-30fb/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-20-30fb/plain-asimov-ggH-bbH/" --model-masspoint="500-20-30fb"
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-15-30fb/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-15-30fb/plain-asimov-ggH-bbH/" --model-masspoint="500-15-30fb"
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-10-30fb/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-10-30fb/plain-asimov-ggH-bbH/" --model-masspoint="500-10-30fb"
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-05-30fb/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-05-30fb/plain-asimov-ggH-bbH/" --model-masspoint="500-05-30fb"
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-130-15-30fb/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-130-15-30fb/plain-asimov-ggH-bbH/" --model-masspoint="130-15-30fb"
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-200-15-30fb/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-200-15-30fb/plain-asimov-ggH-bbH/" --model-masspoint="200-15-30fb"
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-400-15-30fb/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-400-15-30fb/plain-asimov-ggH-bbH/" --model-masspoint="400-15-30fb"
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-600-15-30fb/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-600-15-30fb/plain-asimov-ggH-bbH/" --model-masspoint="600-15-30fb"

#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-30fb-A+H/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-30fb-A+H/plain-asimov-ggH-bbH/" --model-masspoint="500-30-30fb-A+H"
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-30fb-h/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-30fb-h/plain-asimov-ggH-bbH/" --model-masspoint="500-30-30fb-h"

#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-05-30fb-A+H/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-05-30fb-A+H/plain-asimov-ggH-bbH/" --model-masspoint="500-05-30fb-A+H"
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-05-30fb-h/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-05-30fb-h/plain-asimov-ggH-bbH/" --model-masspoint="500-05-30fb-h"

#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-300fb/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-300fb/plain-asimov-ggH-bbH/" --model-masspoint="500-30-300fb"

#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-05-300fb/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-05-300fb/plain-asimov-ggH-bbH/" --model-masspoint="500-05-300fb"
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-05-3000fb/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-05-3000fb/plain-asimov-ggH-bbH/" --model-masspoint="500-05-3000fb"



#########Naiuve approach with SMH as background

#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-30fb/plain-SMHbkg-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-30fb/plain-SMHbkg-asimov-ggH-bbH/" --model-masspoint="500-30-30fb-SMHbkg"
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-300fb/plain-SMHbkg-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-300fb/plain-SMHbkg-asimov-ggH-bbH/" --model-masspoint="500-30-300fb-SMHbkg"



#########Naive appraoch with SMH as signal (potential with different scales)

python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-300fb/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-300fb/plain-MSSMvsSM4-asimov-ggH-bbH/" --model-masspoint="500-30-300fb-SMHsig4" --analysis="plain-MSSMvsSM4"
python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-300fb/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-300fb/plain-MSSMvsSM-asimov-ggH-bbH/" --model-masspoint="500-30-300fb-SMHsig1" --analysis="plain-MSSMvsSM"
python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-300fb/plain-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-300fb/plain-MSSMvsSM0-asimov-ggH-bbH/" --model-masspoint="500-30-300fb-SMHsig0" --analysis="plain-MSSMvsSM0"

#########HiggsBound method

#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-BG-Only-30fb/plain-asimov-mhmodp-NLL/mt/" --mass-tolerance=0.2 --tolerance-denumerator-max --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-BG-Only-30fb/plain-asimov-ggH-bbH/" --higgs-bounds --model-masspoint="BG_Only_30fb" --expected


#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-130-15-30fb/plain-asimov-mhmodp-NLL/mt/" --mass-tolerance=0.2 --tolerance-denumerator-max --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-130-15-30fb/plain-asimov-ggH-bbH/" --higgs-bounds --model-masspoint="130_15_30fb_HB" --bg-path="$CMSSW_BASE/src/LIMITS-150707-mssm-BG-Only-30fb/plain-asimov-mhmodp-NLL/mt/" --full-nll-subtracted
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-05-30fb/plain-asimov-mhmodp-NLL/mt/" --mass-tolerance=0.2 --tolerance-denumerator-max --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-05-30fb/plain-asimov-ggH-bbH/" --higgs-bounds --model-masspoint="500_05_30fb_HB" --bg-path="$CMSSW_BASE/src/LIMITS-150707-mssm-BG-Only-30fb/plain-asimov-mhmodp-NLL/mt/"  --full-nll-subtracted
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-30fb/plain-asimov-mhmodp-NLL/mt/" --mass-tolerance=0.2 --tolerance-denumerator-max --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-30fb/plain-asimov-ggH-bbH/" --higgs-bounds --model-masspoint="500_30_30fb_HB" --bg-path="$CMSSW_BASE/src/LIMITS-150707-mssm-BG-Only-30fb/plain-asimov-mhmodp-NLL/mt/" --full-nll-subtracted

#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-130-15-30fb/plain-asimov-mhmodp-NLL/mt/" --mass-tolerance=0.2 --tolerance-denumerator-max --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-130-15-30fb/plain-asimov-ggH-bbH/" --model-masspoint="130_15_30fb" --expected
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-05-30fb/plain-asimov-mhmodp-NLL/mt/" --mass-tolerance=0.2 --tolerance-denumerator-max --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-05-30fb/plain-asimov-ggH-bbH/" --model-masspoint="500_05_30fb" --expected
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-30fb/plain-asimov-mhmodp-NLL/mt/" --mass-tolerance=0.2 --tolerance-denumerator-max --ggH-bbH-path="$CMSSW_BASE/src/LIMITS-150707-mssm-500-30-30fb/plain-asimov-ggH-bbH/" --model-masspoint="500_30_30fb" --expected


#########light vs heavy (modified naive approach)

#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS150512-mssm/bbb-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS150512-mssm/bbb-asimov-ggH-bbH/" --model-masspoint="BG_only" --light-vs-heavy
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS150527-mssm/bbb-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS150527-mssm/bbb-asimov-ggH-bbH/" --model-masspoint="500_5" --light-vs-heavy
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS150526-mssm/bbb-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS150526-mssm/bbb-asimov-ggH-bbH/" --model-masspoint="500_30_120_only" --forbidden-region-level=95 --light-vs-heavy
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS150525-mssm/bbb-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS150525-mssm/bbb-asimov-ggH-bbH/" --model-masspoint="500_30_130_only" --light-vs-heavy
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS150524-mssm/bbb-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS150524-mssm/bbb-asimov-ggH-bbH/" --model-masspoint="500_30_500_only" --light-vs-heavy
#python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py --nll-path="$CMSSW_BASE/src/LIMITS150608-mssm/bbb-asimov-mhmodp-NLL/mt/" --ggH-bbH-path="$CMSSW_BASE/src/LIMITS150608-mssm/bbb-asimov-ggH-bbH/" --model-masspoint="130_15" --light-vs-heavy
