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
python init-setup.py

function copy_8_to_14 {
   for src in `ls $1/*8TeV* | grep -v root | grep -v mssm`
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
  -i mt/htt_mt.inputs-sm-8TeV.root -o mt/htt_mt.inputs-sm-14TeV.root \
  tt=tt Z=ZLL,ZJ,ZL,ZTT QCD=QCD W=W WZ=VV VH=VH125 qqH=qqH125 ggH=ggH125
root -q -b "${CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleLumi.C+(\"mt/htt_mt.inputs-sm-14TeV.root\",5.0,300,true,2)"


copy_8_to_14 et
scaleTo14TeV.py \
  -i et/htt_et.inputs-sm-8TeV.root -o et/htt_et.inputs-sm-14TeV.root \
  tt=tt Z=ZLL,ZJ,ZL,ZTT QCD=QCD W=W WZ=VV VH=VH125 qqH=qqH125 ggH=ggH125
root -q -b "${CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleLumi.C+(\"et/htt_et.inputs-sm-14TeV.root\",5.0,300,true,2)" 

copy_8_to_14 em
scaleTo14TeV.py \
  -i em/htt_em.inputs-sm-8TeV.root -o em/htt_em.inputs-sm-14TeV.root \
  tt=ttbar Z=Ztt WW=EWK QCD=Fakes VH=VH125 qqH=qqH125 ggH=ggH125
root -q -b "${CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleLumi.C+(\"em/htt_em.inputs-sm-14TeV.root\",5.0,300,true,2)" 

copy_8_to_14 mm
scaleTo14TeV.py \
  -i mm/htt_mm.inputs-sm-8TeV.root -o mm/htt_mm.inputs-sm-14TeV.root \
  tt=TTJ Z=ZTT,ZMM WW=Dibosons W=WJets QCD=QCD VH=VH125 qqH=qqH125 ggH=ggH125
root -q -b "${CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleLumi.C+(\"mm/htt_mm.inputs-sm-14TeV.root\",5.0,300,true,2)" 

copy_8_to_14 tt
scaleTo14TeV.py \
  -i tt/htt_tt.inputs-sm-8TeV.root -o tt/htt_tt.inputs-sm-14TeV.root \
  tt=tt Z=ZLL,ZJ,ZL,ZTT QCD=QCD W=W WZ=VV VH=VH125 qqH=qqH125 ggH=ggH125
root -q -b "${CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleLumi.C+(\"tt/htt_tt.inputs-sm-14TeV.root\",5.0,300,true,2)" 
