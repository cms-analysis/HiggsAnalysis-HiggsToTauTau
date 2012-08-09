#!/bin/bash

# Copy over Abdollah's results.

cp /afs/cern.ch/user/a/abdollah/public/For_Evan/Final_7TeV_1_Evan/cgs-sm-7TeV-01.conf .
cp /afs/cern.ch/user/a/abdollah/public/For_Evan/Final_7TeV_1_Evan/unc-sm-7TeV-01.conf .
cp /afs/cern.ch/user/a/abdollah/public/For_Evan/Final_7TeV_1_Evan/unc-sm-7TeV-01.vals .
hadd -f vhtt_4l.inputs-sm-7TeV.root /afs/cern.ch/user/a/abdollah/public/For_Evan/Final_7TeV_1_Evan/shapes_*.root

cp /afs/cern.ch/user/a/abdollah/public/For_Evan/Final_8TeV_1_Evan/cgs-sm-8TeV-01.conf .
cp /afs/cern.ch/user/a/abdollah/public/For_Evan/Final_8TeV_1_Evan/unc-sm-8TeV-01.conf .
cp /afs/cern.ch/user/a/abdollah/public/For_Evan/Final_8TeV_1_Evan/unc-sm-8TeV-01.vals .
hadd -f vhtt_4l.inputs-sm-8TeV.root /afs/cern.ch/user/a/abdollah/public/For_Evan/Final_8TeV_1_Evan/shapes_*.root
