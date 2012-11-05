#!/bin/bash

./mlfit_and_copy.py ../../../HIG-12-051/VHTT/cmb/125

cp -r root root_postfit

./postfit.py root_postfit/vhtt.input_7TeV.root datacards/vhtt_1_7TeV.txt \
  --bins eemt_zh eeet_zh eeem_zh mmme_zh mmmt_zh mmet_zh eett_zh mmtt_zh \
  --verbose
./postfit.py root_postfit/vhtt.input_7TeV.root datacards/vhtt_0_7TeV.txt \
  --bins emt mmt --verbose

./postfit.py root_postfit/vhtt.input_8TeV.root datacards/vhtt_1_8TeV.txt \
  --bins eemt_zh eeet_zh eeem_zh mmme_zh mmmt_zh mmet_zh eett_zh mmtt_zh \
  --verbose
./postfit.py root_postfit/vhtt.input_8TeV.root datacards/vhtt_0_8TeV.txt \
  --bins emt mmt --verbose
