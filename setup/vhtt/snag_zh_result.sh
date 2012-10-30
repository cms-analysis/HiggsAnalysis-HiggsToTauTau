#!/bin/bash

# Copy over Abdollah's results.

basedir7=/afs/cern.ch/user/a/abdollah/public/For_Evan/HCP/SMOOTH_7TeV
basedir8=/afs/cern.ch/user/a/abdollah/public/For_Evan/HCP/SMOOTH_8TeV

cp $basedir7/cgs-sm-7TeV-01.conf .
cp $basedir7/unc-sm-7TeV-01.conf .
cp $basedir7/unc-sm-7TeV-01.vals .
hadd -f vhtt_4l.inputs-sm-7TeV.root $basedir7/*.root

cp $basedir8/cgs-sm-8TeV-01.conf .
cp $basedir8/unc-sm-8TeV-01.conf .
cp $basedir8/unc-sm-8TeV-01.vals .
hadd -f vhtt_4l.inputs-sm-8TeV.root $basedir8/*.root
