#!/usr/bin/env python

boundariesfile = open('HiggsAnalysis/HiggsToTauTau/python/mssm_multidim_fit_boundaries.py', 'r')
txtfile = open('xs_boundaries.txt', 'r')

oldbounds = boundariesfile.read()
obbegin = oldbounds.find("    (\"ggH-bbH\",")
obend = oldbounds.find("### only makes since 90-140 GeV atm since SM ggH loop contributions are only available for those masses")
ob = oldbounds[obbegin:obend]
txt = txtfile.read()
newbounds = oldbounds.replace(ob, txt)
boundariesfile.close()
txtfile.close()
boundariesfile = open('HiggsAnalysis/HiggsToTauTau/python/mssm_multidim_fit_boundaries.py', 'w')
boundariesfile.write(newbounds)
boundariesfile.close()