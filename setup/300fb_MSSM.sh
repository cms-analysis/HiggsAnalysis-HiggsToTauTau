#!/bin/bash

# Scale 8TeV cards to 14TeV and 300 fb-1 
#
# The modified cards/shape files appear with the 14TeV period suffix.
# Scales only mt, et, em, and mm channels.
#
# The theory errors (PDF, QCD scale) can turned off by modifying the 
# copy_8_to_14 function in this file.
#
# Author: Evan K. Friis, UW Madison

# Copy original data cards
#python init-setup.py

function copy_8_to_14 {
   for src in `ls $1/*8TeV* | grep -v root`
   do
     dest=`echo $src | sed "s|8TeV|14TeV|"`
     # Uncomment for with theory errors
     # cp $src $dest
     # Uncomment next line for no theory errors
     cat $src | grep -v -e "pdf_" -e "QCDscale_" -e "UEPS" > $dest
   done
}

copy_8_to_14 mt
scaleTo14TeV.py \
  -i mt/htt_mt.inputs-mssm-8TeV-0.root -o mt/htt_mt.inputs-mssm-14TeV-0.root \
  tt=TT,TT_fine_binning,TT_CMS_scale_t_mutau_8TeVDown,TT_CMS_eff_t_mssmHigh_mutau_8TeVDown,TT_CMS_scale_t_mutau_8TeVUp,TT_CMS_eff_t_mssmHigh_mutau_8TeVUp Z=ZLL,ZLL_fine_binning,ZLL_CMS_scale_t_mutau_8TeVDown,ZLL_CMS_eff_t_mssmHigh_mutau_8TeVDown,ZLL_CMS_scale_t_mutau_8TeVUp,ZLL_CMS_eff_t_mssmHigh_mutau_8TeVUp,ZJ,ZJ_fine_binning,ZJ_CMS_scale_t_mutau_8TeVDown,ZJ_CMS_eff_t_mssmHigh_mutau_8TeVDown,ZJ_CMS_scale_t_mutau_8TeVUp,ZJ_CMS_eff_t_mssmHigh_mutau_8TeVUp,ZL,ZL_fine_binning,ZL_CMS_scale_t_mutau_8TeVDown,ZL_CMS_eff_t_mssmHigh_mutau_8TeVDown,ZL_CMS_scale_t_mutau_8TeVUp,ZL_CMS_eff_t_mssmHigh_mutau_8TeVUp,ZTT,ZTT_fine_binning,ZTT_CMS_scale_t_mutau_8TeVDown,ZTT_CMS_eff_t_mssmHigh_mutau_8TeVDown,ZTT_CMS_scale_t_mutau_8TeVUp,ZTT_CMS_eff_t_mssmHigh_mutau_8TeVUp QCD=QCD,QCD_fine_binning,QCD_CMS_scale_t_mutau_8TeVDown,QCD_CMS_eff_t_mssmHigh_mutau_8TeVDown,QCD_CMS_scale_t_mutau_8TeVUp,QCD_CMS_eff_t_mssmHigh_mutau_8TeVUp W=W,W_fine_binning,W_CMS_scale_t_mutau_8TeVDown,W_CMS_eff_t_mssmHigh_mutau_8TeVDown,W_CMS_scale_t_mutau_8TeVUp,W_CMS_eff_t_mssmHigh_mutau_8TeVUp WZ=VV,VV_fine_binning,VV_CMS_scale_t_mutau_8TeVDown,VV_CMS_eff_t_mssmHigh_mutau_8TeVDown,VV_CMS_scale_t_mutau_8TeVUp,VV_CMS_eff_t_mssmHigh_mutau_8TeVUp VH=VH125 qqH=qqH125 ggH=ggH125
root -q -b "${CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleLumi.C+(\"mt/htt_mt.inputs-mssm-14TeV-0.root\",19.7,300,true,2)"


copy_8_to_14 et
scaleTo14TeV.py \
  -i et/htt_et.inputs-mssm-8TeV-0.root -o et/htt_et.inputs-mssm-14TeV-0.root \
  tt=TT,TT_fine_binning,TT_CMS_scale_t_etau_8TeVDown,TT_CMS_eff_t_mssmHigh_etau_8TeVDown,TT_CMS_scale_t_etau_8TeVUp,TT_CMS_eff_t_mssmHigh_etau_8TeVUp Z=ZLL,ZLL_fine_binning,ZLL_CMS_scale_t_etau_8TeVDown,ZLL_CMS_eff_t_mssmHigh_etau_8TeVDown,ZLL_CMS_scale_t_etau_8TeVUp,ZLL_CMS_eff_t_mssmHigh_etau_8TeVUp,ZJ,ZJ_fine_binning,ZJ_CMS_scale_t_etau_8TeVDown,ZJ_CMS_eff_t_mssmHigh_etau_8TeVDown,ZJ_CMS_scale_t_etau_8TeVUp,ZJ_CMS_eff_t_mssmHigh_etau_8TeVUp,ZL,ZL_fine_binning,ZL_CMS_scale_t_etau_8TeVDown,ZL_CMS_eff_t_mssmHigh_etau_8TeVDown,ZL_CMS_scale_t_etau_8TeVUp,ZL_CMS_eff_t_mssmHigh_etau_8TeVUp,ZTT,ZTT_fine_binning,ZTT_CMS_scale_t_etau_8TeVDown,ZTT_CMS_eff_t_mssmHigh_etau_8TeVDown,ZTT_CMS_scale_t_etau_8TeVUp,ZTT_CMS_eff_t_mssmHigh_etau_8TeVUp QCD=QCD,QCD_fine_binning,QCD_CMS_scale_t_etau_8TeVDown,QCD_CMS_eff_t_mssmHigh_etau_8TeVDown,QCD_CMS_scale_t_etau_8TeVUp,QCD_CMS_eff_t_mssmHigh_etau_8TeVUp W=W,W_fine_binning,W_CMS_scale_t_etau_8TeVDown,W_CMS_eff_t_mssmHigh_etau_8TeVDown,W_CMS_scale_t_etau_8TeVUp,W_CMS_eff_t_mssmHigh_etau_8TeVUp WZ=VV,VV_fine_binning,VV_CMS_scale_t_etau_8TeVDown,VV_CMS_eff_t_mssmHigh_etau_8TeVDown,VV_CMS_scale_t_etau_8TeVUp,VV_CMS_eff_t_mssmHigh_etau_8TeVUp VH=VH125 qqH=qqH125 ggH=ggH125
root -q -b "${CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleLumi.C+(\"et/htt_et.inputs-mssm-14TeV-0.root\",19.7,300,true,2)" 

copy_8_to_14 em
scaleTo14TeV.py \
  -i em/htt_em.inputs-mssm-8TeV-0.root -o em/htt_em.inputs-mssm-14TeV-0.root \
  tt=ttbar,ttbar_fine_binning,ttbar_CMS_scale_e_8TeVDown,ttbar_CMS_scale_e_8TeVUp Z=Ztt,Ztt_fine_binning,Ztt_CMS_scale_e_8TeVDown,Ztt_CMS_scale_e_8TeVUp WW=EWK,EWK_fine_binning,EWK_CMS_scale_e_8TeVDown,EWK_CMS_scale_e_8TeVUp QCD=Fakes,Fakes_fine_binning,Fakes_CMS_scale_e_8TeVDown,Fakes_CMS_scale_e_8TeVUp VH=VH125 qqH=qqH125 ggH=ggH125
root -q -b "${CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleLumi.C+(\"em/htt_em.inputs-mssm-14TeV-0.root\",19.7,300,true,2)" 

copy_8_to_14 mm
scaleTo14TeV.py \
  -i mm/htt_mm.inputs-mssm-8TeV-0.root -o mm/htt_mm.inputs-mssm-14TeV-0.root \
  tt=TTJ Z=ZTT,ZMM WW=Dibosons W=WJets QCD=QCD VH=VH125 qqH=qqH125 ggH=ggH125
root -q -b "${CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleLumi.C+(\"mm/htt_mm.inputs-mssm-14TeV-0.root\",19.7,300,true,2)" 

copy_8_to_14 tt
scaleTo14TeV.py \
  -i tt/htt_tt.inputs-mssm-8TeV-0.root -o tt/htt_tt.inputs-mssm-14TeV-0.root \
  tt=TT,TT_CMS_scale_t_tautau_8TeVDown,TT_CMS_eff_t_mssmHigh_tautau_8TeVDown,TT_CMS_scale_t_tautau_8TeVUp,TT_CMS_eff_t_mssmHigh_tautau_8TeVUp Z=ZTT,ZTT_CMS_scale_t_tautau_8TeVDown,ZTT_CMS_eff_t_mssmHigh_tautau_8TeVDown,ZTT_CMS_scale_t_tautau_8TeVUp,ZTT_CMS_eff_t_mssmHigh_tautau_8TeVUp,ZJ,ZJ_CMS_scale_t_tautau_8TeVDown,ZJ_CMS_eff_t_mssmHigh_tautau_8TeVDown,ZJ_CMS_scale_t_tautau_8TeVUp,ZJ_CMS_eff_t_mssmHigh_tautau_8TeVUp,ZL,ZL_CMS_scale_t_tautau_8TeVDown,ZL_CMS_eff_t_mssmHigh_tautau_8TeVDown,ZL_CMS_scale_t_tautau_8TeVUp,ZL_CMS_eff_t_mssmHigh_tautau_8TeVUp,ZTT_fine_binning,ZL_fine_binning,ZJ_fine_binning QCD=QCD,QCD_fine_binning,QCD_CMS_scale_t_tautau_8TeVDown,QCD_CMS_eff_t_mssmHigh_tautau_8TeVDown,QCD_CMS_scale_t_tautau_8TeVUp W=W,W_fine_binning,W_CMS_scale_t_tautau_8TeVDown,W_CMS_eff_t_mssmHigh_tautau_8TeVDown,W_CMS_scale_t_tautau_8TeVUp WZ=VV,VV_fine_binning,VV_CMS_scale_t_tautau_8TeVDown,VV_CMS_eff_t_mssmHigh_tautau_8TeVDown,VV_CMS_scale_t_tautau_8TeVUp VH=VH125 qqH=qqH125 ggH=ggH125
root -q -b "${CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleLumi.C+(\"tt/htt_tt.inputs-mssm-14TeV-0.root\",18.3,300,true,2)" 
