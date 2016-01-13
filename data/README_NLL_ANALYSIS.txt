Checkout:

export SCRAM_ARCH=slc6_amd64_gcc481
cmsrel CMSSW_7_1_5
cd CMSSW_7_1_5/src/
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
git clone https://github.com/cms-analysis/HiggsAnalysis-HiggsToTauTau.git 
git clone https://github.com/roger-wolf/HiggsAnalysis-HiggsToTauTau-auxiliaries.git auxiliaries

cd HiggsAnalysis/HiggsToTauTau
git checkout git checkout origin/Model-Independent-Studies

cd $CMSSW_BASE/src
scram b -j 12 


Run:

1) create your model directories - here for an injected model of mhmod+ tanb=30 mA=500GeV with 30/fb
	-> go to directory auxiliaries/shapes/Imperial/NLL-Studies and remove the surfix "_30fb" at the chosen shape file
	-> python HiggsAnalysis/HiggsToTauTau/scripts/doMSSM.py -a plain --label='-500-30-30fb' --tail-fitting --drop-list="$PWD/auxiliaries/pruning/uncertainty-pruning-drop-131013-mssm.txt" --config="HiggsAnalysis/HiggsToTauTau/data/limits.config-mssm-150425" --update-all --blind-datacards --extra-templates='0.007354608*ggH500, 1.166089265*ggH120, 0.080838097*bbH500, 0.016368334*bbH120' --fine-scan
	-> Mark that the light scalar mass mh is taken as 120GeV and the heavy higgs scalar and pseudoscalar H and A are taken with mass 500GeV. The numbers in the extra-templates string are the xs*Br calculated at the desired injected model point. The xs*Br of A+H have to be added beforehand if they have they have the same mass. Here masses of the Higgs boson are approximately. If the correct mass of the desired model point are taken the signal templates bbH$MASS and ggH$MASS have to be generated using horizontol template morphing with the central histograms as input. Currently the doMSSM.py morphs templates from 90 to 1000 in steps of 1GeV.
	

2) Model independent Limits:
        -> mkdir LIMITS in $CMSSW_BASE/src  (not needed after step one)
        -> setup-htt.py -i aux/plain-asimov -o LIMITS/plain-asimov-mhmodp-NLL -a mssm -c 'mt' -p 8TeV --mssm-categories-mt="8 9" 90_1000:10
        -> lxb-xsec2tanb.py LIMITS/plain-asimov-mhmodp-NLL/mt/* --model mhmodp --lxq --fineGrid
        -> submit.py --tanbNLL  LIMITS/plain-asimov-mhmodp-NLL/mt/* --lxq --queue="-l h_vmem=4000M -l h_rt=48:00:00 -j y -o /dev/null"

3) Cross-Section*BR for each higgs boson in the (mA, tanb) plane:
        -> python HiggsAnalysis/HiggsToTauTau/scripts/higgsContributions_submit.py --reference-mass=(h,A,H) 
	-> This script is based the script "scripts/higgsContributions.py" and on "macros/mssm_xs.C". The neutral higgs boson are clustered depending on the mass difference between them. 2D histos with summed xs*br are stored.
	-> Run three times meaning for all three higgs bosons. It is important to chose the model you want. As the default the mhmod+ 8TeV mu=200GeV tanb=1-60 is chosen. Probably the import paths in macros/mssm_xs.C have to be adjusted. Currently only 8TeV model files are supported. For the new 13TeV model files with new histogram names and new readout tools the script has to be extended. Should be straight forward.)  

4) Model dependent Limits:
        -> cvs2local.py -i aux/plain-asimov -o LIMITS/plain-asimov-ggH-bbH -p 8TeV -a mssm -c 'mt' --mssm-categories-mt="8 9" 90_1000:10
	-> Comment out all commands you do not need in HiggsAnalysis/HiggsToTauTau/ggHbbHWorkflow.sh. Only one at a time should be uncommented. Otherwise you can of course create your own command following the given examples.
        -> source HiggsAnalysis/HiggsToTauTau/ggHbbHWorkflow.sh 
	-> This script is based on "scripts/adjust_mssm_boundaries.py" which adjusts the boundaries of the ggH-bbH plane for each mass in 90_1000:10 . After the adjustments a likelihood scan of the ggH-bbH plane is performed for all considered masses in the considered boundaries.
        -> python HiggsAnalysis/HiggsToTauTau/python/lxb-multidimfit-resubmit.py LIMITS-plain-asimov-ggH-bbH-GGH-BBH-90 -o LIMITS/plain-asimov-ggH-bbH/ -m '90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000'
	-> Redo this until you are sure that every job has completed        
	-> limit.py --collect --multidim-fit --physics-model="ggH-bbH" LIMITS/plain-asimov-ggH-bbH/*
        -> plot --multidim-fit HiggsAnalysis/HiggsToTauTau/python/layouts/multidim-fit-ggH-bbH.py LIMITS/plain-asimov-ggH-bbH
        -> rm plain-asimov-ggH-bbH?scan?GGH-BBH*
	-> rm -r LIMITS-plain-asimov-ggH-bbH-GGH-BBH-*

5) Plotting:
        -> source HiggsAnalysis/HiggsToTauTau/NLLworkflow.sh 
	-> Look into and chose or edit the ones you need.
	-> This script is based on "scripts/NLLWorkflow.py". Here the method which cluster is most sensitive in which parameter region is checked and the quantities (delta NLL etc) are calculated for the considered method. Currently the higgsbounds method and the naive approach is used. For future MSSM h-tautau searches probably a more dedicated approach needs to be implemented where the SM Higgs is used at 125GeV with different scales to fix the problems with rebuilding the direct measurements/exclusions due to the influence of the light scalar h even at high masses. All plots are made using subscripts ("scripts/multidimNLL.py", "scripts/multidimNLL_HiggsBounds.py", "scripts/multidimNLL_SMHscale.py") in . The plotting may needs some polishing. 
	-> plots can be found in directory: 

General remark:
        -> Please run step after step since some calculations dependent on each other
	-> -h does always help
	-> The code has been written quick and dirty. It works as it should but, code styling wise there is a lot of room for improvements. Feel free to do so. 


