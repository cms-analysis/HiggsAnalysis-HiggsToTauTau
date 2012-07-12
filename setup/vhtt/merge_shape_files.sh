#!/bin/bash

echo "Combining VHTT shape files and running horizontal interpolation"

lltCategories="emt,eet,mmt" 
zhCategories="mmmt_zh,mmet_zh,mmem_zh,mmtt_zh,eemt_zh,eeet_zh,eeem_zh,eett_zh" 
lttCategories="ett_sm,mtt_sm" 

morph() 
{
  echo "LLT channels"
  horizontal-morphing.py \
    --categories="${lltCategories}"\
    --samples="VH{MASS}" \
    --uncerts="" --masses="120,130,140" --step-size=1 -i $1
  echo "ZH channels"
  horizontal-morphing.py \
    --categories="${zhCategories}"\
    --samples="VH{MASS},VH_hww{MASS}" \
    --uncerts="" --masses="120,130,140" --step-size=1 -i $1
  echo "LTT channels"
  horizontal-morphing.py \
    --categories="${lttCategories}"\
    --samples="WH{MASS}" \
    --uncerts="" --masses="120,130,140" --step-size=1 -i $1
}

echo "Combining 7TeV"
hadd -f vhtt.inputs-sm-7TeV.root \
  vhtt_4l.inputs-sm-7TeV.root \
  vhtt_ltt.inputs-sm-7TeV.root \
  vhtt_llt.inputs-sm-7TeV.root

echo "Morphing 7TeV"
morph vhtt.inputs-sm-7TeV.root 

echo "Combining 8TeV"
hadd -f vhtt.inputs-sm-8TeV.root \
  vhtt_4l.inputs-sm-8TeV.root \
  vhtt_ltt.inputs-sm-8TeV.root \
  vhtt_llt.inputs-sm-8TeV.root

echo "Morphing 8TeV"
morph vhtt.inputs-sm-8TeV.root 
