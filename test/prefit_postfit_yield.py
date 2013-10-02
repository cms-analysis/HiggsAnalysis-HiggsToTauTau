#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="Script to print out the yield difference in prefit to postfit plots.")
parser.add_option("--pre", dest="prefit", default="", type="string",
                  help="Path to prefit rootfile. [Default: 'Prefit.root']")
#parser.add_option("--post", dest="postfit", default="", type="string",
#                  help="Path to postfit rootfile. [Default: 'Postfit.root']")

# check number of arguments; in case print usage
(options, args) = parser.parse_args()

import os
import re
import ROOT
import operator


backgrounds = ['Ztt', 'Zmm', 'Zee', 'ttbar', 'EWK', 'EWK1', 'ggH_hww', 'Fakes', 'WJets', 'Dibosons', 'ggH', 'bbH', 'qqH', 'VH']
data = ['data_obs']


def print_yields(prefit_input, postfit_input) :
    pre_background={}
    pre_data={}
    post_background={}
    post_data={}
   
    for key in prefit_input.GetListOfKeys() :
        name=key.GetName()
        #print name, backgrounds
        if name in backgrounds :
            pre_hist  = {name: prefit_input.Get(name)}
            post_hist = {name: postfit_input.Get(name)}
            pre_background.update (pre_hist )
            post_background.update(post_hist)
        if name in data :
            pre_hist  = {name: prefit_input.Get(name)}
            post_hist = {name: postfit_input.Get(name)}
            pre_data.update (pre_hist )
            post_data.update(post_hist)
    
    pre_background2  = sorted(pre_background.items() , key=lambda hist: hist[1].Integral())
    post_background2 = sorted(post_background.items(), key=lambda hist: hist[1].Integral())
    pre_data2  = sorted(pre_data.items() , key=lambda hist: hist[1].Integral())
    post_data2 = sorted(post_data.items(), key=lambda hist: hist[1].Integral()) 

    print "%8s %15s %15s %15s" % ("sample", "prefit", "postfit", "difference")
    for (i, hist) in enumerate(pre_background2):
        pre_absolute = 0
        post_absolute= 0
        diff = 0
        if i>0 :
            for k in range(hist[1].GetNbinsX()) :
                #print pre_background2[i][0], pre_background2[i-1][0], " bin", k, "difference (post-pre): ", (post_background2[i][1].GetBinContent(k)*post_background2[i][1].GetBinWidth(k) - post_background2[i-1][1].GetBinContent(k)*post_background2[i-1][1].GetBinWidth(k)) - (pre_background2[i][1].GetBinContent(k)*pre_background2[i][1].GetBinContent(k) - pre_background2[i-1][1].GetBinContent(k)*pre_background2[i-1][1].GetBinWidth(k))
                diff += (post_background2[i][1].GetBinContent(k)*post_background2[i][1].GetBinWidth(k) - post_background2[i-1][1].GetBinContent(k)*post_background2[i-1][1].GetBinWidth(k)) - (pre_background2[i][1].GetBinContent(k)*pre_background2[i][1].GetBinWidth(k) - pre_background2[i-1][1].GetBinContent(k)*pre_background2[i-1][1].GetBinWidth(k))
                pre_absolute  += pre_background2[i][1].GetBinContent(k)*pre_background2[i][1].GetBinWidth(k) - pre_background2[i-1][1].GetBinContent(k)*pre_background2[i-1][1].GetBinWidth(k)
                post_absolute += post_background2[i][1].GetBinContent(k)*post_background2[i][1].GetBinWidth(k) - post_background2[i-1][1].GetBinContent(k)*post_background2[i-1][1].GetBinWidth(k)
        else :
            for k in range(hist[1].GetNbinsX()) :
                #print pre_background2[i][0], " bin", k, "difference (post-pre): ", post_background2[i][1].GetBinContent(k)*post_background2[i][1].GetBinWidth(k) - pre_background2[i][1].GetBinContent(k)*pre_background2[i][1].GetBinWidth(k)
                diff += post_background2[i][1].GetBinContent(k)*post_background2[i][1].GetBinWidth(k) - pre_background2[i][1].GetBinContent(k)*pre_background2[i][1].GetBinWidth(k)
                pre_absolute  += pre_background2[i][1].GetBinContent(k) *pre_background2[i][1].GetBinWidth(k)
                post_absolute += post_background2[i][1].GetBinContent(k)*post_background2[i][1].GetBinWidth(k)

        print "%8s %15.2f %15.2f %15.2f" % (post_background2[i][0], pre_absolute, post_absolute, diff)

        
    for (i, hist) in enumerate(pre_data2):
        pre_absolute = 0
        post_absolute= 0
        diff = 0
        for k in range(hist[1].GetNbinsX()) :
            #print pre_background2[i][0], " bin", k, "difference (post-pre): ", post_background2[i][1].GetBinContent(k)*post_background2[i][1].GetBinWidth(k) - pre_background2[i][1].GetBinContent(k)*pre_background2[i][1].GetBinWidth(k)
            diff += post_data2[i][1].GetBinContent(k)*post_data2[i][1].GetBinWidth(k) - pre_data2[i][1].GetBinContent(k)*pre_data2[i][1].GetBinWidth(k)
            pre_absolute  += pre_data2[i][1].GetBinContent(k) *pre_data2[i][1].GetBinWidth(k)
            post_absolute += post_data2[i][1].GetBinContent(k)*post_data2[i][1].GetBinWidth(k)

                
        print "%8s %15.2f %15.2f %15.2f" % (post_data2[i][0], pre_absolute, post_absolute, diff)   
   
   

prefit_input  = ROOT.TFile(options.prefit)
postfit_input = ROOT.TFile(options.prefit.replace("prefit","postfit"))
print_yields(prefit_input, postfit_input)
prefit_input.Close(); postfit_input.Close()

