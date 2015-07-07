
1) Ordner mit dem mhmodp Szenario für Masse (500,30): aux150428-mssm, sollte in $CMSSW_BASE/src liegen.

2) Erstellung von modelabhängigen Limits:
	-> mkdir LIMITS150428-mssm in $CMSSW_BASE/src
	-> setup-htt.py -i aux150428-mssm/bbb-asimov -o LIMITS150428-mssm/bbb-asimov-mhmodp-NLL -a mssm -c 'mt' -p 8TeV --mssm-categories-mt="8 9" 90_1000:10
	-> lxb-xsec2tanb.py LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/* --model mhmodp --lxq --fineGrid
		für die Option --fineGrid müssen einige Dateien angepasst werden:
	-> submit.py --tanbNLL  LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/* --lxq --queue="-l h_vmem=4000M -l h_rt=48:00:00 -j y -o /dev/null"
		für die Option --tanbNLL müssen einige Dateien angepasst werden:
		für die Option --tanbNLL ist ein NEUER Script dabei: HiggsAnalysis/HiggsToTauTau/scripts/scriptNLL.py

3) Berechnung der Beiträge (Cross-Section*BR) von Higgs Bosonen für die (mA, tanb) Ebene:
	-> python HiggsAnalysis/HiggsToTauTau/scripts/higgsContributions_submit.py (NEUER Script)
	   hierfür müssen einige Dateien angepasst werden:
			mssm_xs.C
			mssm_xs.h
	   hierfür ist ein NEUER Script dabei: HiggsAnalysis/HiggsToTauTau/scripts/higgsContributions.py

4) Anpassung der Cross-Section*BR Grenzen für modelunabhängige LIMITS und ihre Berechnung:
	->	cvs2local.py -i aux150428-mssm/bbb-asimov -o LIMITS150428-mssm/bbb-asimov-ggH-bbH -p 8TeV -a mssm -c 'mt' --mssm-categories-mt="8 9" 90_1000:10
	-> source HiggsAnalysis/HiggsToTauTau/ggHbbHWorkflow.sh (NEUER shell-Script)
		hierfür muss 2) und 3) bereits ausgeführt worden sein
		hierfür ist ein NEUER Script dabei: HiggsAnalysis/HiggsToTauTau/scripts/adjust_mssm_boundaries.py
	-> python HiggsAnalysis/HiggsToTauTau/python/lxb-multidimfit-resubmit.py LIMITS150428-mssm-bbb-asimov-ggH-bbH-GGH-BBH-90 -o LIMITS150428-mssm/bbb-asimov-ggH-bbH/ -m '90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000'
	-> limit.py --collect --multidim-fit --physics-model="ggH-bbH" LIMITS150428-mssm/bbb-asimov-ggH-bbH/*
	-> plot --multidim-fit HiggsAnalysis/HiggsToTauTau/python/layouts/multidim-fit-ggH-bbH.py LIMITS150428-mssm/bbb-asimov-ggH-bbH
	-> rm bbb-asimov-ggH-bbH?scan?GGH-BBH*

5) Erstellung von Plots zum Vergleich der modelunabhängigen und modelabhängigen Vorgehensweise:
	-> python HiggsAnalysis/HiggsToTauTau/scripts/NLLWorkflow.py (NEUER Script)
		hierfür muss 2), 3) und 4) ausgeführt worden sein
		hierfür ist ein NEUER Script dabei: HiggsAnalysis/HiggsToTauTau/scripts/multidimNLL.py
		hierfür ist ein NEUES Macro dabei: HiggsAnalysis/HiggsToTauTau/macros/NLLPlot.C