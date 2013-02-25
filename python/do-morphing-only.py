#!/usr/bin/env python

import os

## do morphing for em 7TeV
os.system("horizontal-morphing.py --categories='emu_vbf,emu_boost_low,emu_boost_high,emu_0jet_low,emu_0jet_high' --samples='ggH{MASS},qqH{MASS},VH{MASS}' --uncerts='CMS_scale_e_7TeV' --masses='110,115,120,125,130,135,140,145' --step-size 0.1 setups_UPLOAD/pruned/em/htt_em.inputs-sm-7TeV.root")
## do morphing fir em 8TeV high pt categories
os.system("horizontal-morphing.py --categories='emu_boost_high,emu_0jet_high' --samples='ggH{MASS},qqH{MASS},VH{MASS}' --uncerts='CMS_scale_e_highpt_8TeV' --masses='110,115,120,125,130,135,140,145' --step-size 0.1 setups_UPLOAD/pruned/em/htt_em.inputs-sm-8TeV.root")
## do morphing fir em 8TeV low pt categories
os.system("horizontal-morphing.py --categories='emu_vbf,emu_boost_low,emu_0jet_low' --samples='ggH{MASS},qqH{MASS},VH{MASS}' --uncerts='CMS_scale_e_8TeV' --masses='110,115,120,125,130,135,140,145' --step-size 0.1 setups_UPLOAD/pruned/em/htt_em.inputs-sm-8TeV.root")
## do morphing for et 7TeV
os.system("horizontal-morphing.py --categories='eleTau_vbf,eleTau_boost_low,eleTau_boost_high,eleTau_0jet_low,eleTau_0jet_high' --samples='ggH{MASS},qqH{MASS},VH{MASS}' --uncerts='CMS_scale_t_etau_7TeV' --masses='110,115,120,125,130,135,140,145' --step-size 0.1 setups_UPLOAD/pruned/et/htt_et.inputs-sm-7TeV.root")
## do morphing for et 8TeV
os.system("horizontal-morphing.py --categories='eleTau_vbf,eleTau_boost_low,eleTau_boost_high,eleTau_0jet_low,eleTau_0jet_high' --samples='ggH{MASS},qqH{MASS},VH{MASS}' --uncerts='CMS_scale_t_etau_8TeV' --masses='110,115,120,125,130,135,140,145' --step-size 0.1 setups_UPLOAD/pruned/et/htt_et.inputs-sm-8TeV.root")
## do morphing for mt 7TeV
os.system("horizontal-morphing.py --categories='muTau_vbf,muTau_boost_low,muTau_boost_high,muTau_0jet_low,muTau_0jet_high' --samples='ggH{MASS},qqH{MASS},VH{MASS}' --uncerts='CMS_scale_t_mutau_7TeV' --masses='110,115,120,125,130,135,140,145' --step-size 0.1 setups_UPLOAD/pruned/mt/htt_mt.inputs-sm-7TeV.root")
## do morphing for mt 8TeV
os.system("horizontal-morphing.py --categories='muTau_vbf,muTau_boost_low,muTau_boost_high,muTau_0jet_low,muTau_0jet_high' --samples='ggH{MASS},qqH{MASS},VH{MASS}' --uncerts='CMS_scale_t_mutau_8TeV' --masses='110,115,120,125,130,135,140,145' --step-size 0.1 setups_UPLOAD/pruned/mt/htt_mt.inputs-sm-8TeV.root")
## do morphing for tt
os.system("horizontal-morphing.py --categories='tauTau_vbf,tauTau_boost' --samples='ggH{MASS},qqH{MASS},VH{MASS}' --uncerts='CMS_scale_t_tautau_8TeV' --masses='110,115,120,125,130,135,140,145' --step-size 0.1 setups_UPLOAD/pruned/tt/htt_tt.inputs-sm-8TeV.root")
