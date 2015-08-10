
1) create your model directories with CombineHarvester or older scripts

2) Model independent Limits:
	-> mkdir LIMITS150428-mssm in $CMSSW_BASE/src
	-> setup-htt.py -i aux150428-mssm/bbb-asimov -o LIMITS150428-mssm/bbb-asimov-mhmodp-NLL -a mssm -c 'mt' -p 8TeV --mssm-categories-mt="8 9" 90_1000:10
	-> lxb-xsec2tanb.py LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/* --model mhmodp --lxq --fineGrid
	-> submit.py --tanbNLL  LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/* --lxq --queue="-l h_vmem=4000M -l h_rt=48:00:00 -j y -o /dev/null"

3) Cross-Section*BR for each higgs boson in the (mA, tanb) plane:
	-> python HiggsAnalysis/HiggsToTauTau/scripts/higgsContributions_submit.py --reference-mass=(h,A,H) (Run three times -> all three higgs bosons) 

4) Model dependent Limits:
	->	cvs2local.py -i aux150428-mssm/bbb-asimov -o LIMITS150428-mssm/bbb-asimov-ggH-bbH -p 8TeV -a mssm -c 'mt' --mssm-categories-mt="8 9" 90_1000:10
	-> source HiggsAnalysis/HiggsToTauTau/ggHbbHWorkflow.sh 
	-> python HiggsAnalysis/HiggsToTauTau/python/lxb-multidimfit-resubmit.py LIMITS150428-mssm-bbb-asimov-ggH-bbH-GGH-BBH-90 -o LIMITS150428-mssm/bbb-asimov-ggH-bbH/ -m '90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000'
	-> limit.py --collect --multidim-fit --physics-model="ggH-bbH" LIMITS150428-mssm/bbb-asimov-ggH-bbH/*
	-> plot --multidim-fit HiggsAnalysis/HiggsToTauTau/python/layouts/multidim-fit-ggH-bbH.py LIMITS150428-mssm/bbb-asimov-ggH-bbH
	-> rm bbb-asimov-ggH-bbH?scan?GGH-BBH*

5) Plotting:
	-> python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py 

General remark:
	-> Please run step after step since some calculations dependent on each other