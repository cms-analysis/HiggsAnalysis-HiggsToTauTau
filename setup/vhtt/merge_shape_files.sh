#!/bin/bash

echo "Combining VHTT shape files"

hadd -f vhtt.inputs-sm-7TeV.root \
  vhtt_4l.inputs-sm-7TeV.root \
  vhtt_ltt.inputs-sm-7TeV.root \
  vhtt_llt.inputs-sm-7TeV.root

hadd -f vhtt.inputs-sm-8TeV.root \
  vhtt_4l.inputs-sm-8TeV.root \
  vhtt_ltt.inputs-sm-8TeV.root \
  vhtt_llt.inputs-sm-8TeV.root
