import os

type       = "rescaled" 

channels   = [
    "emu",
    "eTau",
    "muTau",
    #"mumu",
    ]

categories = [
    "0jet_low",
    "0jet_high",
    "0jet",
    "boost_low",
    "boost_high",
    "boost",
    "vbf",
    ] 

extra = {
    "emu"   : "#tau_{e}#tau_{#mu}",
    "eTau"  : "#tau_{e}#tau_{h}",
    "muTau" : "#tau_{#mu}#tau_{h}",
    "mumu"  : "#tau_{#mu}#tau_{#mu}",
    }

log = {
    ("emu"  , "0jet_low"  ) : "true",
    ("emu"  , "0jet_high" ) : "false",
    ("emu"  , "0jet"      ) : "true", 
    ("emu"  , "boost_low" ) : "false",
    ("emu"  , "boost_high") : "false",
    ("emu"  , "boost"     ) : "false",
    ("emu"  , "vbf"       ) : "false",
    ("muTau", "0jet_low"  ) : "false",
    ("muTau", "0jet_high" ) : "false",
    ("muTau", "0jet"      ) : "false", 
    ("muTau", "boost_low" ) : "false",
    ("muTau", "boost_high") : "false",
    ("muTau", "boost"     ) : "false",
    ("muTau", "vbf"       ) : "false",
    ("eTau" , "0jet_low"  ) : "false",
    ("eTau" , "0jet_high" ) : "false",
    ("eTau" , "0jet"      ) : "false", 
    ("eTau" , "boost_low" ) : "false",
    ("eTau" , "boost_high") : "false",
    ("eTau" , "boost"     ) : "false",
    ("eTau" , "vbf"       ) : "false",
    ("mumu" , "0jet_low"  ) : "true",
    ("mumu" , "0jet_high" ) : "true",
    ("mumu" , "0jet"      ) : "true", 
    ("mumu" , "boost_low" ) : "true",
    ("mumu" , "boost_high") : "true",
    ("mumu" , "boost"     ) : "true",
    ("mumu" , "vbf"       ) : "false",    
    }

max = {
    ("emu"  , "0jet_low"  ) : "1000",
    ("emu"  , "0jet_high" ) :   "80", 
    ("emu"  , "0jet"      ) : "1000",
    ("emu"  , "boost_low" ) :  "160",
    ("emu"  , "boost_high") :   "45",
    ("emu"  , "boost"     ) :  "200",
    ("emu"  , "vbf"       ) :  "3.0",
    ("muTau", "0jet_low"  ) : "2400",
    ("muTau", "0jet_high" ) :  "350",
    ("muTau", "0jet"      ) : "3000", 
    ("muTau", "boost_low" ) :  "450",
    ("muTau", "boost_high") :  "150",
    ("muTau", "boost"     ) :  "700",
    ("muTau", "vbf"       ) :  "6.0",
    ("eTau" , "0jet_low"  ) :  "120",
    ("eTau" , "0jet_high" ) :   "45",
    ("eTau" , "0jet"      ) :  "140", 
    ("eTau" , "boost_low" ) :  "100",
    ("eTau" , "boost_high") :   "40",
    ("eTau" , "boost"     ) :  "120",
    ("eTau" , "vbf"       ) :  "4.0",
    ("mumu" , "0jet_low"  ) : "1200",
    ("mumu" , "0jet_high" ) :   "80", 
    ("mumu" , "0jet"      ) : "1200",
    ("mumu" , "boost_low" ) :  "120",
    ("mumu" , "boost_high") :   "50",
    ("mumu" , "boost"     ) :  "160",
    ("mumu" , "vbf"       ) :  "2.8",    
    }

min = {
    ("emu"  , "0jet_low"  ) : "0.1",
    ("emu"  , "0jet_high" ) : "0",
    ("emu"  , "0jet"      ) : "0.3", 
    ("emu"  , "boost_low" ) : "0",
    ("emu"  , "boost_high") : "0",
    ("emu"  , "boost"     ) : "0",
    ("emu"  , "vbf"       ) : "0",
    ("muTau", "0jet_low"  ) : "0",
    ("muTau", "0jet_high" ) : "0",
    ("muTau", "0jet"      ) : "0", 
    ("muTau", "boost_low" ) : "0",
    ("muTau", "boost_high") : "0",
    ("muTau", "boost"     ) : "0",
    ("muTau", "vbf"       ) : "0",
    ("eTau" , "0jet_low"  ) : "0",
    ("eTau" , "0jet_high" ) : "0",
    ("eTau" , "0jet"      ) : "0", 
    ("eTau" , "boost_low" ) : "0",
    ("eTau" , "boost_high") : "0",
    ("eTau" , "boost"     ) : "0",
    ("eTau" , "vbf"       ) : "0",
    ("mumu" , "0jet_low"  ) : "0.1",
    ("mumu" , "0jet_high" ) : "0",
    ("mumu" , "0jet"      ) : "0.3", 
    ("mumu" , "boost_low" ) : "0",
    ("mumu" , "boost_high") : "0",
    ("mumu" , "boost"     ) : "0",
    ("mumu" , "vbf"       ) : "0",    
    }

## combine 2011+2012
for chn in channels :
    for cat in categories :
        ## combine high and low pt categories, make sure in your 
        ## list that {CAT}_low and {CAT}_high are run beforehand
        if cat == "0jet" or cat == "boost" :
            #print "hadd {CHN}_{CAT}_{TYPE}_7+8TeV.root {CHN}_{CAT}_low_{TYPE}_7+8TeV.root {CHN}_{CAT}_high_{TYPE}_7+8TeV.root".format(CHN=chn, CAT=cat, TYPE=type)
            os.system("hadd -f {CHN}_{CAT}_{TYPE}_7+8TeV.root {CHN}_{CAT}_low_{TYPE}_7+8TeV.root {CHN}_{CAT}_high_{TYPE}_7+8TeV.root".format(CHN=chn, CAT=cat, TYPE=type))
        else :
            ## patch until Josh fixes his naming conventions
            if chn == "eTau" :
                #print "hadd {CHN}_{CAT}_{TYPE}_7+8TeV.root {CHN}_{CAT}_{TYPE}_7TeV_{LOG}.root eleTau_{CAT}_{TYPE}_8TeV_{LOG}.root".format(
                #    CHN=chn, CAT=cat, TYPE=type, LOG="" if log[(chn, cat)] else "") 
                os.system("hadd -f {CHN}_{CAT}_{TYPE}_7+8TeV.root {CHN}_{CAT}_{TYPE}_7TeV_*.root eleTau_{CAT}_{TYPE}_8TeV_*.root".format(
                    CHN=chn, CAT=cat, TYPE=type))#, LOG="LOG" if log[(chn, cat)]==True else ""))
            else:
                print chn, cat, log[(chn, cat)]
                #print "hadd {CHN}_{CAT}_{TYPE}_7+8TeV.root {CHN}_{CAT}_{TYPE}_7TeV_{LOG}.root {CHN}_{CAT}_{TYPE}_8TeV_{LOG}.root".format(
                #    CHN=chn, CAT=cat, TYPE=type, LOG="LOG" if log[(chn, cat)] else "")
                os.system("hadd -f {CHN}_{CAT}_{TYPE}_7+8TeV.root {CHN}_{CAT}_{TYPE}_7TeV_*.root {CHN}_{CAT}_{TYPE}_8TeV_*.root".format(
                    CHN=chn, CAT=cat, TYPE=type))#, LOG="LOG" if log[(chn, cat)]==True else ""))
## make plots
for chn in channels :
    for cat in categories :
        print chn, cat
        os.system("root -l -q -b {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/postfit.C+\\(\\\"{CHN}_{CAT}_{TYPE}_7+8TeV.root\\\",\\\"{LABEL}\\\",\\\"{EXTRA}\\\",{MIN},{MAX},{LOG}\)".format(CMSSW_BASE=os.environ['CMSSW_BASE'], CHN=chn, CAT=cat, TYPE=type, LABEL="2011+2012", EXTRA=extra[chn], MIN=min[chn,cat], MAX=max[chn,cat], LOG=log[chn,cat]))
        
