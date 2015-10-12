#!/usr/bin/env pythonimport glob

import os
import re
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

#ROOT.gSystem.Load('$CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit.so')
#from ROOT import th1fmorph

from optparse import OptionParser

parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="This is a script to merge H+->tau nu shape files. ARG corresponds to the *root files which should get merged.")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
                  help="Run in verbose mode")
(options, args) = parser.parse_args()
## check number of arguments; in case print usage
if len(args) < 1 :
    parser.print_usage()
    exit(1)

hists = []

outputfile = ROOT.TFile("combine_histograms_hplushadronic_light.root", "RECREATE")

for arg in args :
    print arg
    mass=arg.rstrip(".root").split("_")[-1].lstrip("m")
    file = ROOT.TFile(arg, "READ")
    if not file :
        print "file not found: ", arg
    file.cd()

    for name in ROOT.gDirectory.GetListOfKeys():
        hist = file.Get(name.GetName())
        
        if hist.GetName() in hists :
            continue
        #print hist

        outputfile.cd()
        newname=""

        if "HH{MASS}_a".format(MASS=mass) in name.GetName() :
            #print name.GetName()
            newname=name.GetName().replace("HH{MASS}_a".format(MASS=mass), "CMS_ttHpHp_signal")
            newnames=newname.split("signal")
            newname=newnames[0]+"signal"+mass+newnames[-1]
            if "statBin" in name.GetName() :
                newname=newnames[0]+"signal"+mass+"_"+newnames[0]+"signal"+newnames[-1]
            newname=newname.replace("tau_ID_shape", "CMS_eff_t")                      
            newname=newname.replace("tau_ID_eToTauBarrel_shape","CMS_fake_eToTauBarrel")      
            newname=newname.replace("tau_ID_muToTau_shape","CMS_fake_muToTau")           
            newname=newname.replace("tau_ID_jetToTau_shape","CMS_fake_jetToTau")          
            newname=newname.replace("ES_taus","CMS_scale_t")      
            newname=newname.replace("b_tag","CMS_btag_CSVT")                        
            newname=newname.replace("top_pt","CMS_Hptntj_topPtReweighting")  
            newname=newname.replace("QCD_metshape","CMS_Hptntj_QCDbkg_metshape")                    
            newname=newname.replace("Emb_reweighting","CMS_Hptntj_taubkg_Reweighting")
            #print newname
            hist.SetTitle(newname)
            hist.SetName(newname)
        if "HW{MASS}_a".format(MASS=mass) in name.GetName() :
            #print name.GetName()
            newname=name.GetName().replace("HW{MASS}_a".format(MASS=mass), "CMS_ttHpW_signal")
            newnames=newname.split("signal")
            newname=newnames[0]+"signal"+mass+newnames[-1]
            if "statBin" in name.GetName() :
                newname=newnames[0]+"signal"+mass+"_"+newnames[0]+"signal"+newnames[-1]
            newname=newname.replace("tau_ID_shape", "CMS_eff_t")                      
            newname=newname.replace("tau_ID_eToTauBarrel_shape","CMS_fake_eToTauBarrel")      
            newname=newname.replace("tau_ID_muToTau_shape","CMS_fake_muToTau")           
            newname=newname.replace("tau_ID_jetToTau_shape","CMS_fake_jetToTau")          
            newname=newname.replace("ES_taus","CMS_scale_t")      
            newname=newname.replace("b_tag","CMS_btag_CSVT")                        
            newname=newname.replace("top_pt","CMS_Hptntj_topPtReweighting")  
            newname=newname.replace("QCD_metshape","CMS_Hptntj_QCDbkg_metshape")                    
            newname=newname.replace("Emb_reweighting","CMS_Hptntj_taubkg_Reweighting")
            #print newname
            hist.SetTitle(newname)
            hist.SetName(newname)   
        if "EWK_Tau" in name.GetName() : 
            #print name.GetName()
            newname=name.GetName().replace("EWK_Tau", "CMS_Hptntj_taubkg")
            newname=newname.replace("tau_ID_shape", "CMS_eff_t")                      
            newname=newname.replace("tau_ID_eToTauBarrel_shape","CMS_fake_eToTauBarrel")      
            newname=newname.replace("tau_ID_muToTau_shape","CMS_fake_muToTau")           
            newname=newname.replace("tau_ID_jetToTau_shape","CMS_fake_jetToTau")          
            newname=newname.replace("ES_taus","CMS_scale_t")      
            newname=newname.replace("b_tag","CMS_btag_CSVT")                        
            newname=newname.replace("top_pt","CMS_Hptntj_topPtReweighting")  
            newname=newname.replace("QCD_metshape","CMS_Hptntj_QCDbkg_metshape")                    
            newname=newname.replace("Emb_reweighting","CMS_Hptntj_taubkg_Reweighting")
            #print newname
            hist.SetTitle(newname)
            hist.SetName(newname)
        if "QCDinv" in name.GetName() : 
            #print name.GetName()
            newname=name.GetName().replace("QCDinv", "CMS_Hptntj_QCDbkg")
            newname=newname.replace("tau_ID_shape", "CMS_eff_t")                      
            newname=newname.replace("tau_ID_eToTauBarrel_shape","CMS_fake_eToTauBarrel")      
            newname=newname.replace("tau_ID_muToTau_shape","CMS_fake_muToTau")           
            newname=newname.replace("tau_ID_jetToTau_shape","CMS_fake_jetToTau")          
            newname=newname.replace("ES_taus","CMS_scale_t")      
            newname=newname.replace("b_tag","CMS_btag_CSVT")                        
            newname=newname.replace("top_pt","CMS_Hptntj_topPtReweighting")  
            newname=newname.replace("QCD_metshape","CMS_Hptntj_QCDbkg_metshape")                    
            newname=newname.replace("Emb_reweighting","CMS_Hptntj_taubkg_Reweighting")
            #print "hallo", newname
            hist.SetTitle(newname)
            hist.SetName(newname)
        if "EWKnontt_faketau" in name.GetName() : 
            #print name.GetName()
            newname=name.GetName().replace("EWKnontt_faketau", "CMS_Hptntj_fakebkg")
            newname=newname.replace("tau_ID_shape", "CMS_eff_t")                      
            newname=newname.replace("tau_ID_eToTauBarrel_shape","CMS_fake_eToTauBarrel")      
            newname=newname.replace("tau_ID_muToTau_shape","CMS_fake_muToTau")           
            newname=newname.replace("tau_ID_jetToTau_shape","CMS_fake_jetToTau")          
            newname=newname.replace("ES_taus","CMS_scale_t")      
            newname=newname.replace("b_tag","CMS_btag_CSVT")                        
            newname=newname.replace("top_pt","CMS_Hptntj_topPtReweighting")  
            newname=newname.replace("QCD_metshape","CMS_Hptntj_QCDbkg_metshape")                    
            newname=newname.replace("Emb_reweighting","CMS_Hptntj_taubkg_Reweighting")
            #print newname
            hist.SetTitle(newname)
            hist.SetName(newname)   
        if "tt_EWK_faketau" in name.GetName() : 
            #print name.GetName()
            newname=name.GetName().replace("tau_ID_shape", "CMS_eff_t")                      
            newname=newname.replace("tau_ID_eToTauBarrel_shape","CMS_fake_eToTauBarrel")      
            newname=newname.replace("tau_ID_muToTau_shape","CMS_fake_muToTau")           
            newname=newname.replace("tau_ID_jetToTau_shape","CMS_fake_jetToTau")          
            newname=newname.replace("ES_taus","CMS_scale_t")      
            newname=newname.replace("b_tag","CMS_btag_CSVT")                        
            newname=newname.replace("top_pt","CMS_Hptntj_topPtReweighting")  
            newname=newname.replace("QCD_metshape","CMS_Hptntj_QCDbkg_metshape")                    
            newname=newname.replace("Emb_reweighting","CMS_Hptntj_taubkg_Reweighting")
            #print newname
            hist.SetTitle(newname)
            hist.SetName(newname)  

        hist.Write()
            
        hists.append(hist.GetName())
        
outputfile.Close()
#print hists

#hoirzontal template morphing needed for 130
os.system("horizontal-morphing.py --categories='' --samples='CMS_ttHpHp_signal{MASS}' --uncerts='CMS_ttHpHp_signal_statBin10,CMS_ttHpHp_signal_statBin9,CMS_ttHpHp_signal_statBin8,CMS_ttHpHp_signal_statBin7,CMS_ttHpHp_signal_statBin6,CMS_ttHpHp_signal_statBin5,CMS_ttHpHp_signal_statBin4,CMS_ttHpHp_signal_statBin3,CMS_ttHpHp_signal_statBin2,CMS_ttHpHp_signal_statBin1,CMS_btag_CSVT,CMS_scale_t,CMS_eff_t,CMS_fake_eToTauBarrel,CMS_fake_muToTau,CMS_fake_jetToTau' --masses='120,140' --step-size 10. -v combine_histograms_hplushadronic_light.root".format(MASS="{MASS}"))

os.system("horizontal-morphing.py --categories='' --samples='CMS_ttHpW_signal{MASS}' --uncerts='CMS_ttHpW_signal_statBin10,CMS_ttHpW_signal_statBin9,CMS_ttHpW_signal_statBin8,CMS_ttHpW_signal_statBin7,CMS_ttHpW_signal_statBin6,CMS_ttHpW_signal_statBin5,CMS_ttHpW_signal_statBin4,CMS_ttHpW_signal_statBin3,CMS_ttHpW_signal_statBin2,CMS_ttHpW_signal_statBin1,CMS_btag_CSVT,CMS_scale_t,CMS_eff_t,CMS_fake_eToTauBarrel,CMS_fake_muToTau,CMS_fake_jetToTau' --masses='120,140' --step-size 10. -v combine_histograms_hplushadronic_light.root".format(MASS="{MASS}"))
