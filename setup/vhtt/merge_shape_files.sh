#!/bin/bash

echo "Combining VHTT shape files and running horizontal interpolation"

lltCategories="emt,mmt" 
zhCategories="mmmt_zh,mmet_zh,mmme_zh,mmtt_zh,eemt_zh,eeet_zh,eeem_zh,eett_zh" 
lttCategories="ett_sm,mtt_sm" 

domorph() 
{
  echo "Morphing file $1, samples $2, categories $3" 
  echo "110->140, in 0.5"
  horizontal-morphing.py \
    --categories="$3"\
    --samples="$2" \
    --uncerts="" --masses="110,120,130,140" --step-size=0.5 \
    -i $1 -v
  echo "140->145, in 1.0"
  horizontal-morphing.py \
    --categories="$3"\
    --samples="$2" \
    --uncerts="" --masses="130,140" --step-size=1 \
    -i $1 -v --extrapolate="141,142,143,144,145"
  echo "124.5->126.5, in 0.1"
  horizontal-morphing.py \
    --categories="$3"\
    --samples="$2" \
    --uncerts="" --masses="124,127" --step-size=0.1 \
    -i $1 -v 
}

morph() 
{
  echo "LLT channels"
  domorph $1 "WH{MASS},WH_hww{MASS}"  "${lltCategories}"
  domorph $1 "VH{MASS},VH_hww{MASS}"  "${zhCategories}"
}

echo "Combining 7TeV"
hadd -f vhtt.inputs-sm-7TeV.root \
  vhtt_4l.inputs-sm-7TeV.root \
  vhtt_llt.inputs-sm-7TeV.root

echo "Morphing 7TeV"
morph vhtt.inputs-sm-7TeV.root 

echo "Combining 8TeV"
hadd -f vhtt.inputs-sm-8TeV.root \
  vhtt_4l.inputs-sm-8TeV.root \
  vhtt_llt.inputs-sm-8TeV.root

echo "Morphing 8TeV"
morph vhtt.inputs-sm-8TeV.root 
