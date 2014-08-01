#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script create tables for the AN and PAS from the datacards.")
parser.add_option("-i", "--input", dest="input", default="datacards", type="string", help="Path to the complete set of datacards. [Default: datacards]")
parser.add_option("-p", "--period", dest="period", default="7TeV 8TeV", type="choice", help="Data taking period. [Default: \"7TeV, 8TeV\"]", choices=["7TeV", "8TeV", "7TeV 8TeV"])
parser.add_option("-m", "--mass", dest="mass", default="125", type="string", help="Mass for signal sample to be included in the table. For MSSM, format should be \"mA:tanb\". [Default: 125]")
parser.add_option("-a", "--analysis", dest="analysis", type="string", default="sm", help="analysis type. [Default: \"sm\"]")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="increase verbosity. [Default: False]")
parser.add_option("--postfit", dest="postfit", default=False, action="store_true", help="Print postfield yields and uncertainties. This requires to have already run the postfit plots. [Default: False]")
parser.add_option("--channels", dest="channels", default="mt, et, em, mm, tt", type="string", help="Channels to produce the tables for. [Default: \"mt, et, em, mm, tt\"]")
parser.add_option("--categories", dest="categories", default="0, 1, 2, 3, 5", type="string", help="Categories to produce the tables for. [Default: \"0, 1, 2, 3, 5\"]")
cats1 = OptionGroup(parser, "LUMI PER CHANNEL", "Luminosities per channel.")
cats1.add_option("--lumi-7TeV-mm", dest="lumi_7TeV_mm", default= 4.9, type="float", help="Luminosity used for mm channel. [Default:  4.9]")
cats1.add_option("--lumi-7TeV-ee", dest="lumi_7TeV_ee", default= 4.9, type="float", help="Luminosity used for ee channel. [Default:  4.9]")
cats1.add_option("--lumi-7TeV-em", dest="lumi_7TeV_em", default= 4.9, type="float", help="Luminosity used for em channel. [Default:  4.9]")
cats1.add_option("--lumi-7TeV-mt", dest="lumi_7TeV_mt", default= 4.9, type="float", help="Luminosity used for mt channel. [Default:  4.9]")
cats1.add_option("--lumi-7TeV-et", dest="lumi_7TeV_et", default= 4.9, type="float", help="Luminosity used for et channel. [Default:  4.9]")
cats1.add_option("--lumi-8TeV-mm", dest="lumi_8TeV_mm", default=19.7, type="float", help="Luminosity used for mm channel. [Default: 19.7]")
cats1.add_option("--lumi-8TeV-ee", dest="lumi_8TeV_ee", default=19.7, type="float", help="Luminosity used for ee channel. [Default: 19.7]")
cats1.add_option("--lumi-8TeV-em", dest="lumi_8TeV_em", default=19.7, type="float", help="Luminosity used for em channel. [Default: 19.7]")
cats1.add_option("--lumi-8TeV-mt", dest="lumi_8TeV_mt", default=19.7, type="float", help="Luminosity used for mt channel. [Default: 19.7]")
cats1.add_option("--lumi-8TeV-et", dest="lumi_8TeV_et", default=19.7, type="float", help="Luminosity used for et channel. [Default: 19.7]")
cats1.add_option("--lumi-8TeV-tt", dest="lumi_8TeV_tt", default=19.7, type="float", help="Luminosity used for tt channel. [Default: 19.7]")
parser.add_option_group(cats1)

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) > 0 :
    parser.print_usage()
    exit(1)

import os
import sys
import math
from HiggsAnalysis.HiggsToTauTau.utils import contained
from HiggsAnalysis.HiggsToTauTau.tools.mssm_xsec_tools import mssm_xsec_tools



def cross_section(process, mass, ecms) :
    """
    Determine the SM cross section for given process, higgs boson mass and center of mass energy.
    For MSSM the mass will be accompanied by the tanb value in format ma:tanb, the MSSM BR is
    also expected to be of format BR:[AHh]tt.
    """
    xs = 0.
    if options.analysis == "sm" :
        if process.find('+')>-1 :
            sub_channels = process.split('+')
            for sub_channel in sub_channels :
                xs += float(os.popen("xsec-sm {CHANNEL} {MA} {ECMS} | grep value".format(
                    CHANNEL=sub_channel, MA=mass, ECMS=ecms)).read().split()[2])
        else :
            xs += float(os.popen("xsec-sm {CHANNEL} {MA} {ECMS} | grep value".format(
                CHANNEL=process, MA=mass, ECMS=ecms)).read().split()[2])
    else :
        period = ''
        if ecms == 7.0 :
            period = '7TeV'
        else :
            period = '8TeV'
        mssm_xsec_tools_path = os.environ.get('CMSSW_BASE')+'/src/auxiliaries/models/out.mhmodp-'+period+'-tanbHigh-nnlo.root'
        scan = mssm_xsec_tools(mssm_xsec_tools_path)
        xsquery = scan.query(float(mass[:mass.find(':')]), float(mass[mass.find(':')+1:]))
        if "mass" in  process :
            if "massA" in process :
                xs = xsquery['higgses']['A']['mass']
            elif "massH" in process :
                xs = xsquery['higgses']['H']['mass']
            elif "massh" in process :
                xs = xsquery['higgses']['h']['mass']
        elif "BR" in  process :
            if "Att" in process :
                xs = xsquery['higgses']['A']['BR']
            elif "Htt" in process :
                xs = xsquery['higgses']['H']['BR']
            elif "htt" in process :
                xs = xsquery['higgses']['h']['BR']
        else :
            if "bbA" in process :
                xs = xsquery['higgses']['A']['xsec']['santander']
            elif "ggA" in process :
                xs = xsquery['higgses']['A']['xsec']['ggF']
            elif "bbH" in process :
                xs = xsquery['higgses']['H']['xsec']['santander']
            elif "ggH" in process :
                xs = xsquery['higgses']['H']['xsec']['ggF']
            elif "bbh" in process :
                xs = xsquery['higgses']['h']['xsec']['santander']
            elif "ggh" in process :
                xs = xsquery['higgses']['h']['xsec']['ggF']
    return xs

def digit(x) :
    """
    Return the number of significant digits of x, which should be included for the table. This
    is only of relevance for yields <1, for yields >1 all digits are given. the return value is
    a format string for floats.
    """
    if x == 0 :
        return "%.1f"
    elif math.log10(x)>0 :
        return "%.f"
    else :
        return "%.{DIGIT}f".format(DIGIT=int(math.ceil(-math.log10(x))))

def formated_line(name, rate, uncert) :
    """
    Return a formated line as output for the tmp files for the table yields. This line consists
    of SAMPLE-NAME, YIELD and UNCERTAINTY separated by tabulators for better readability.
    """
    line = "%s \t {YIELD} \t {UNCERT} \n".format(YIELD=digit(rate), UNCERT=digit(uncert))
    return line % (name, rate, uncert)


"""
How to treat uncertainties that are or are not correlated across channels and event categories:

 - introduce a dictionary uncertainty versus channel and category (should correspond to file names)
 - in extractor do not yet add uncertainties in quadrature but keep in lists (in files per channel
   and category)
 - when summing up categories: keep two uncerts for correlated and uncorrelated. If cat/chn found
   in list for correlated uncertainties for a given uncertainty than add linear to uncert(linear),
   otherwise add in quadrature to uncert(correlated). At the end add the two uncerts linear and
   all uncerts in quadrature. 
"""

def extractor(path, period):
    """
    Extract all information, which is relevant for the table from the datacards. This information
    is temporarily safed in a bunch of *.tmp files for yields and and efficiencies. Arguments are
    the full path to the corresponding datacard for a given decay-channel, event-category and run
    period and the run period, which is used to determine the production cross section for the
    Higgs boson signal. The datacards are expected to contain the event yields not for mroe than
    one decay-channel, event-category and run period.
    """
    tmp  = '/dev/null'
    #print "<extractor>: path = %s, period = %s" % (path, period)
    ## determine luminosity per channel
    lumi = {}
    if period == "7TeV" :
        lumi = {
            ## in /pb
            "tt" : 1000*options.lumi_7TeV_mm,
            "mm" : 1000*options.lumi_7TeV_mm,
            "ee" : 1000*options.lumi_7TeV_ee,
            "em" : 1000*options.lumi_7TeV_em,
            "mt" : 1000*options.lumi_7TeV_mt,
            "et" : 1000*options.lumi_7TeV_et,
            }  
    if period == "8TeV" :
        lumi = {
            ## in /pb
            "tt" : 1000*options.lumi_8TeV_tt,
            "mm" : 1000*options.lumi_8TeV_mm,
            "ee" : 1000*options.lumi_8TeV_ee,
            "em" : 1000*options.lumi_8TeV_em,
            "mt" : 1000*options.lumi_8TeV_mt,
            "et" : 1000*options.lumi_8TeV_et,
            }          
    ## determine decay channel from path  
    channel = 'NONE'
    if '_mt_' in path:
        channel = 'mt'
    if '_et_' in path:
        channel = 'et'        
    if '_em_' in path:
        channel = 'em'
    if '_mm_' in path:
        channel = 'mm'
    if '_ee_' in path:
        channel = 'ee'
    if '_tt_' in path:
        channel = 'tt'        
    ## determine event category from path
    category = ['NONE','NONE']        
    if '_0_' in  path:
        category = ['1jet_high_mediumhiggs','0'] if channel == 'tt' else ['0jet_low','0']
    if '_1_' in  path:
        category = ['1jet_high_highhiggs','1'] if channel == 'tt' else ['0jet_high','1']
        if channel == 'et' or channel == 'mt' :
            category = ['0jet_medium','1']
    if '_2_' in  path:
        category = ['vbf','2'] if channel == 'tt' else ['1jet_low','2']
        if channel == 'et' or channel == 'mt' :
            category = ['0jet_high','2']
    if '_3_' in  path:
        category = ['1jet_medium','3'] if channel == 'et' or channel == 'mt' else ['1jet_high','3']
    if '_4_' in  path:
        category = ['1jet_high_lowhiggs','4'] if channel == 'et' or channel == 'mt' else ['vbf_loose','4']
        if channel == 'mm' or channel == 'ee' :
            category = ['vbf','4']
    if '_5_' in  path:
        category = ['1jet_high_mediumhiggs','5'] if channel == 'et' or channel == 'mt' else ['vbf_tight','5']
    if '_6_' in  path:
        category = ['btag_low','6'] if options.analysis == "mssm" else ['vbf_loose','6']
    if '_7_' in  path:
        category = ['btag_high','7'] if options.analysis == "mssm" else ['vbf_tight','7']
    if '_8_' in  path:
        category = ['nobtag','8']
    if '_9_' in  path:
        category = ['btag','9']
    if '_10_' in  path:
        category = ['nobtag_low','10']
    if '_11_' in  path:
        category = ['nobtag_medium','11']
    if '_12_' in  path:
        category = ['nobtag_high','12']    
    if '_13_' in  path:
        category = ['btag_low','13']
    if '_14_' in  path:
        category = ['btag_high','14']    

    ## determine cross section for SM Higgs (in pb)
    if options.analysis == "sm" :
        xsec = {
            "ggH" : cross_section("ggH"      , options.mass, float(period[:period.find("TeV")])),
            "qqH" : cross_section("qqH"      , options.mass, float(period[:period.find("TeV")])),
            "VH"  : cross_section("WH+ZH+ttH", options.mass, float(period[:period.find("TeV")])),
            }
        ## determine BR for SM Higgs signal
        BR = cross_section("BR", options.mass, float(period[:period.find("TeV")]))
    else :
        xsec = {
            "ggA" : cross_section("ggA"      , options.mass, float(period[:period.find("TeV")])),
            "bbA" : cross_section("bbA"      , options.mass, float(period[:period.find("TeV")])),
            "ggH" : cross_section("ggH"      , options.mass, float(period[:period.find("TeV")])),
            "bbH" : cross_section("bbH"      , options.mass, float(period[:period.find("TeV")])),
            "ggh" : cross_section("ggh"      , options.mass, float(period[:period.find("TeV")])),
            "bbh" : cross_section("bbh"      , options.mass, float(period[:period.find("TeV")])),
            }
        BR = {
            "Att" : cross_section("BR:Att"   , options.mass, float(period[:period.find("TeV")])),
            "Htt" : cross_section("BR:Htt"   , options.mass, float(period[:period.find("TeV")])),
            "htt" : cross_section("BR:htt"   , options.mass, float(period[:period.find("TeV")])),
            }
        mass = {
            "mA" : cross_section("massA"     , options.mass, float(period[:period.find("TeV")])),
            "mH" : cross_section("massH"     , options.mass, float(period[:period.find("TeV")])),
            "mh" : cross_section("massh"     , options.mass, float(period[:period.find("TeV")])),
            }
        #print mass
        #print BR
        #print xsec

    ## number of observed events
    observed = 0
    ## rate of signal processes
    rate_sig = []
    ## rate of background processes
    rate_bkg = []
    ## list of background names
    names_bkg = []
    ## sum of uncertainties for signal
    uncert_sig = {}
    ## sum of uncertainties for background
    uncert_bkg = {}
    ## indicates whether line is the first of type process
    first_process_line = True
    ## indicates line of type rate is passed (starting point for uncertainty block)
    passed_rate_line = False
    ## list of uncertainties to ignore, when adding up yield uncertainties (most of
    ## the time as these are shape uncertainties)
    ignore_line = [
        'CMS_scale_t',
        'CMS_scale_j',
        'CMS_scale_u',
        'CMS_htt_mt_0',
        'CMS_htt_et_0',
        'CMS_htt_em_0',
        'CMS_htt_tt_0',
        'CMS_htt_mm_0',
        'CMS_htt_ee_0',
        ]
    ## largest index for signal samples (used for split up of uncertainties for signal
    ## and background) 
    range_sig = -1
    ## largest index for background samples (used for split up of uncertainties for
    ## signal and background)
    range_bkg = -1

    if category[0] == 'vbf_tight' and period == "7TeV" :
        file = ''
    elif category[0] == '1jet_high_lowhiggs' and channel == 'et' :
        file = ''
    else :
        file = open(path)
        ## loop A-datacard and extract all necessary inputs
        for line in file:
            ## COMMENT LINE (skip)
            if line.startswith('---') or line.startswith('#') :
                continue
            values = line.split()
            ## OBSERVATION (pick up observed number of events)
            if values[0] == 'observation':
                observed = values[1]
                continue
            ## PROCESS (organize dict's for signal and background uncertianties, collect
            ## names of backgrounds)
            if values[0] =='process' :
                if first_process_line :
                    range_bkg = len(values)
                    for idx in range(len(values)) :
                        ## if correct this change can catch categories where there is no
                        ## signal included
                        if values[idx].isdigit() and int(values[idx]) == 1 : # == 0
                            range_sig = idx #idx+1
                            break
                    first_process_line = False
                    continue
                elif len(names_bkg)==0 :
                    names_bkg = values[range_sig:]
                    continue
            ## RATE (pick up rates of signal and backgrounds)
            if values[0] == 'rate':
                passed_rate_line = True
                rate_bkg = values[range_sig:]
                rate_sig = values[1:range_sig]
                continue
            ## UNCERTAINTIES (add all relevant uncertainties for signal and backgrounds in
            ## quadrature; there is a special treatment for gmN, shapes are skipped)
            if passed_rate_line and values[0] not in ignore_line:
                if len(uncert_sig) == 0 :
                    uncert_sig = dict([(i,0) for i in range(2, range_sig+1)])
                if len(uncert_bkg) == 0 :
                    uncert_bkg = dict([(i,0) for i in range(range_sig+1, range_bkg+1)])
                ## add systematic uncertainties in quadrature for signal
                for i in range(2, range_sig+1) :
                    value = values[i]
                    if values[1] == 'gmN':                    
                        ## it never happens for the signal to have an uncertainty of type gmN
                        continue
                    try:                
                        value = float(value)
                        if value != 0 :
                            value = value-1                    
                        uncert_sig[i] += value*value
                    except ValueError:
                        continue        
                ## shift ranges in case of uncertainties of type gmN
                range_shift = 1 if values[1] == 'gmN' else 0
                ## add systematic uncertainties in quadrature for signal
                for i in range(range_sig+1+range_shift, range_bkg+1+range_shift):
                    value = values[i]
                    try:
                        value = float(value)
                        if value != 0:
                            if values[1] == 'gmN':
                                value = 1./math.sqrt(float(values[2]))
                            else:
                                value = value-1                    
                        if values[1] == 'gmN':
                            uncert_bkg[i-1] += value*value 
                        else:
                            uncert_bkg[i] += value*value  
                    except ValueError:
                        continue        
        file.close()
        #print "A", rate_sig
        
        ##get sig_rate of closest mass for h boson.
        if options.analysis == "mssm" or options.analysis == "mssm_taupt":
            masses=[90, 100, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000]
            jdx=0
            massh_helper=0
            for m in masses :
                if m==90:
                    if mass["mh"] < masses[jdx] :
                        massh_helper = m
                        break
                if m!=1000 :
                    if mass["mh"] > masses[jdx] and mass["mh"] < masses[jdx+1]:
                        if mass["mh"]-masses[jdx] < masses[jdx+1]-mass["mh"] :
                            massh_helper = m
                        else :
                            massh_helper = masses[jdx+1]
                        break
                else:
                    massh_helper = m
                jdx=jdx+1           
            path=path.replace(str(options.mass[:options.mass.find(":")]), str(massh_helper))
            #print "h", path
            ## loop h-datacard and extract all signal yield inputs
            file = open(path)
            first_process_line = True
            passed_rate_line = False
            rate_sig_h = []
            range_sig_h = -1
            for line in file:
                ## COMMENT LINE (skip)
                if line.startswith('---') or line.startswith('#') :
                    continue
                values = line.split()
                ## PROCESS (organize dict's for signal and background uncertianties, collect
                ## names of backgrounds)
                if values[0] =='process' :
                    if first_process_line :
                        for idx in range(len(values)) :
                            ## if correct this change can catch categories where there is no
                            ## signal included
                            if values[idx].isdigit() and int(values[idx]) == 1 : # == 0
                                range_sig_h = idx #idx+1
                                break
                        first_process_line = False
                        continue
                ## RATE (pick up rates of signal and backgrounds)
                if values[0] == 'rate':
                    passed_rate_line = True
                    rate_sig_h = values[1:range_sig_h]
                    continue
            #print "h", rate_sig_h
            file.close()
            ##get sig_rate of closest mass for H boson.
            jdx=0            
            massH_helper=0
            for m in masses :
                if m==90:
                    if mass["mH"] < masses[jdx] :
                        massH_helper = m
                        break
                if m!=1000 :
                    if mass["mH"] > masses[jdx] and mass["mH"] < masses[jdx+1]:
                        if mass["mH"]-masses[jdx] < masses[jdx+1]-mass["mh"] :
                            massH_helper = m
                        else :
                            massH_helper = masses[jdx+1]
                        break
                else:
                    massH_helper = m
                jdx=jdx+1
            path=path.replace(str(massh_helper), str(massH_helper))
            #print "H", path
            ## loop H-datacard and extract all signal yield inputs
            file = open(path)
            first_process_line = True
            passed_rate_line = False
            rate_sig_H = []
            range_sig_H = -1
            for line in file:
                ## COMMENT LINE (skip)
                if line.startswith('---') or line.startswith('#') :
                    continue
                values = line.split()
                ## PROCESS (organize dict's for signal and background uncertianties, collect
                ## names of backgrounds)
                if values[0] =='process' :
                    if first_process_line :
                        for idx in range(len(values)) :
                            ## if correct this change can catch categories where there is no
                            ## signal included
                            if values[idx].isdigit() and int(values[idx]) == 1 : # == 0
                                range_sig_H = idx #idx+1
                                break
                        first_process_line = False
                        continue
                ## RATE (pick up rates of signal and backgrounds)
                if values[0] == 'rate':
                    passed_rate_line = True
                    rate_sig_H = values[1:range_sig_H]
                    continue
            #print "H", rate_sig_H
            file.close()    
        
        ##read in of scale files produced within the postfit plot making
        in_str = {}
        if options.postfit:
            in_file = open("HiggsAnalysis/HiggsToTauTau/test/scales_"+channel+"_"+category[1]+"_"+period+".py",'r')
            in_str = in_file.read()
            in_file.close()
            in_str = eval(in_str.replace("scales=",""))    
    
        ## sum up total signal rate
        rate_sig_summed = 0
        if options.analysis == "mssm" or options.analysis == "mssm_taupt":
            for i in range(0, len(rate_sig)) :
                if options.postfit :
                    name = 'ggH'
                    if i!=0:
                        name = 'bbH'
                    rate_sig[i] = float(rate_sig[i])*in_str[name][0]
                    rate_sig_h[i] = float(rate_sig_h[i])*in_str[name][0]
                    rate_sig_H[i] = float(rate_sig_H[i])*in_str[name][0]
                else :
                    rate_sig[i] = float(rate_sig[i])
                    rate_sig_h[i] = float(rate_sig_h[i])
                    rate_sig_H[i] = float(rate_sig_H[i])
                    
            rate_sig_summed = xsec["ggA"]*BR["Att"]*rate_sig[0]   + xsec["bbA"]*BR["Att"]*rate_sig[1]                                                                                                            + xsec["ggh"]*BR["htt"]*rate_sig_h[0] + xsec["bbh"]*BR["htt"]*rate_sig_h[1]                                                                                                          + xsec["ggH"]*BR["Htt"]*rate_sig_H[0] + xsec["bbH"]*BR["Htt"]*rate_sig_H[1]
        else : 
            for i in range(0, len(rate_sig)):
                ## NEED TO INCLUDE POSTFIT FOR SM ALSO!!!
                rate_sig[i] = float(rate_sig[i])
                rate_sig_summed += rate_sig[i]
        ## sum up uncertainty of total signal rate
        uncert_sig_split = []
        uncert_sig_summed = 0
        if options.analysis == "mssm" or options.analysis == "mssm_taupt" : 
            if options.postfit :        
                uncert_sig_split.append(in_str["ggH"][1]*(rate_sig[0]+rate_sig_h[0]+rate_sig_H[0]))
                uncert_sig_split.append(in_str["bbH"][1]*(rate_sig[1]+rate_sig_h[1]+rate_sig_H[1]))
                uncert_sig_summed+=uncert_sig_split[0]*uncert_sig_split[0]
                uncert_sig_summed+=uncert_sig_split[1]*uncert_sig_split[1]
            else :
                uncert_sig_split.append(math.sqrt(xsec["ggA"]*BR["Att"]*xsec["ggA"]*BR["Att"]*uncert_sig[2])*(rate_sig[0]+rate_sig_h[0]+rate_sig_H[0]))
                uncert_sig_split.append(math.sqrt(xsec["bbA"]*BR["Att"]*xsec["bbA"]*BR["Att"]*uncert_sig[3])*(rate_sig[1]+rate_sig_h[1]+rate_sig_H[1]))
                uncert_sig_summed+=uncert_sig_split[0]*uncert_sig_split[0]
                uncert_sig_summed+=uncert_sig_split[1]*uncert_sig_split[1]             
        else :
            for i in range(0, len(rate_sig)):
                ## NEED TO INCLUDE POSTFIT FOR SM ALSO!!!
                ## the newest is that we can have categories w/o signal
                #if len(uncert_sig) == 0 :
                #    break
                uncert_sig_split.append(math.sqrt(uncert_sig[2+i])*rate_sig[i])
                uncert_sig_summed+=uncert_sig_split[i]*uncert_sig_split[i]
        uncert_sig_summed = math.sqrt(uncert_sig_summed)
          
        ## sum up total background rate
        rate_bkg_summed = 0
        for name, rate in zip(names_bkg, rate_bkg):
            if options.postfit :
                rate = in_str[name][0]*float(rate)
            else :
                rate = float(rate)
    	    if rate!=0.0 :
                rate = round(rate, 0 if round(math.log10(rate))>0 else -int(math.ceil(-math.log10(rate)))+1)
                rate_bkg_summed += rate
        ## sum up uncertainty of total background rate
        uncert_bkg_split = []
        uncert_bkg_summed = 0   
        u=0
        for name, rate in zip(names_bkg, rate_bkg): 
            if options.postfit : 
                uncert_bkg_split.append(in_str[name][1]*float(rate)*in_str[name][0])
                uncert_bkg_summed+=uncert_bkg_split[u]*uncert_bkg_split[u]
            else :
                uncert_bkg_split.append(math.sqrt(uncert_bkg[range_sig+1+u])*float(rate))
                uncert_bkg_summed+=uncert_bkg_split[u]*uncert_bkg_split[u]
            u=u+1
        uncert_bkg_summed = math.sqrt(uncert_bkg_summed)
          
        ## write tmp results to file, identified by channel, category and period
        yields = open(channel+'_'+category[0]+'_'+period+'.tmp', 'w')
        for name, rate, uncert in zip(names_bkg, rate_bkg, uncert_bkg_split):
            if options.postfit :
                yields.write(formated_line(name, in_str[name][0]*float(rate), uncert))                  
            else :
                yields.write(formated_line(name, float(rate), uncert))
        yields.write(formated_line('Total' , rate_bkg_summed, uncert_bkg_summed))
        yields.write(formated_line('Signal', rate_sig_summed, uncert_sig_summed))
        yields.write('Data \t %d \n' % int(observed))
        yields.close()
    
        efficiencies = open('eff_'+channel+'_'+period+'.tmp','a')
        efficiencies.write(channel+'_'+category[0]+"\n")
        if options.analysis == "mssm" or options.analysis == "mssm_taupt" :
            if len(rate_sig)>1 :
                ## for mssm the yield needs to be multiplied with xsec*BR
                efficiencies.write("ggH \t %f \t %f \n" % (xsec["ggH"]*BR["Att"]*rate_sig[0], xsec["ggH"]*BR["Att"]*lumi[channel]))
                efficiencies.write("bbH \t %f \t %f \n" % (xsec["bbH"]*BR["Att"]*rate_sig[1], xsec["bbH"]*BR["Att"]*lumi[channel]))
        else :
            if len(rate_sig)>2 :
                efficiencies.write("ggH \t %f \t %f \n" % (rate_sig[0], xsec["ggH"]*BR*lumi[channel]))
                efficiencies.write("qqH \t %f \t %f \n" % (rate_sig[1], xsec["qqH"]*BR*lumi[channel]))
                efficiencies.write("VH  \t %f \t %f \n" % (rate_sig[2], xsec["VH" ]*BR*lumi[channel]))
        efficiencies.close()
    return

def sum_list(source, target, squared=False) :
    """
    Sum all values from the source list into the target list. If target list is empty it will
    be initialized with the values of the source list. Otherwise the source list and the target
    list are expected to have the same number of entries in the same logical order. The option
    squared allows to add the values of the source lits quadratically into the target list.
    This function is used in merge_subsets and in merge_efficiencies.
    """
    for i in range(len(source)) :
        if len(target) == i :
            target.append(source[i]*source[i]) if squared else target.append(source[i])
        else :
            target[i]+=source[i]*source[i] if squared else source[i]

def merge_subsets(channel, categories) :
    """
    Merge the contents of a set of sub-categories, which is expected to be of type 'high',
    'high_7TeV', while it can be of any type. The sub-category is defined by an extension label
    unambiguously to identify the *.tmp file fir yields and efficiencies, which has to be produced
    in the function extract beforehand. the *.tmp files are expected to be of type channel+'_'+
    main-category+'_'+sub-category+'.tmp'. The sub-categoriy lables are passed on as extended
    dictionary argument categories. The argument channel corresponds to the channel label. Yields
    are added linearly, uncertainties are added inquadrature.
    """
    for cat, subsets in categories.iteritems() :
        ## expected rates for signal and background
        rates    = dict([(sub, []) for sub in subsets])
        ## uncertainties of rates
        uncerts  = dict([(sub, []) for sub in subsets])
        ## samples names 
        samples  = dict([(sub, []) for sub in subsets])
        ## number of observed events 
        observed = dict([(sub,  0) for sub in subsets])
        ## summed values
        observed_summed = 0
        rates_summed   = []
        uncerts_summed = []
        for sub in subsets:
            file = open(channel+'_'+cat+'_'+sub+'.tmp')
            for line in file:
                values = line.split()
                if values[0] == 'Data':
                    observed[sub] = float(values[1])
                else :
                    # work-around for problem in mt and et (different processes in VBF for 7 and 8 TeV)
                    if options.analysis == 'sm' and sub == '7TeV' and values[0] == 'ZLL' :
                        samples[sub].append('ZL')
                        rates[sub].append(float(values[1]))
                        uncerts[sub].append(float(values[2]))
                        samples[sub].append('ZJ')
                        rates[sub].append(0.0)
                        uncerts[sub].append(0.0)
                    else:
                        samples[sub].append(values[0])
                        rates[sub].append(float(values[1]))
                        uncerts[sub].append(float(values[2]))
            file.close()

        for key in samples :
            observed_summed+=observed[key]
            sum_list(rates[key], rates_summed, False)
            sum_list(uncerts[key], uncerts_summed, True)
        
        file = open(channel+'_'+cat+'.tmp','w')
        for i in range(len(samples[subsets[0]])) :
            file.write(formated_line(samples[subsets[0]][i], rates_summed[i], math.sqrt(uncerts_summed[i])))
        file.write('Data \t %d \n'% int(observed_summed))
        file.close()

def merge_efficiencies(channel, categories, periods) :
    """
    Merge the contents of the *.tmp files used to temporarily safe the information for the calculation
    of the signal efficiencies.The argument categories should contain a compact dictionary of event
    sub-categories to be contracted into main event-categories, the argument contains the list of all
    run periods to be considered. First the information per run period is added. Then the infomration
    of the event sub-categories is contracted into the main event categories. The results are safed in
    a *.tmp file labeld by the channel but no run period label. The information integrated over the
    run periods but not yet contracted into the main event categories is safed in a file which carries
    the extra label *_split.tmp. Only the signal channels ggH, qqH and VH are taken into account. VH
    it the sum of WH, ZH and ttH. 
    """
    ## list of subsets (used for contraction of sub-categories)
    subsets = []
    ## lines used to add periods
    lines = dict([(per, []) for per in periods])
    ## combine run periods
    for per in periods:
        file = open('eff_'+channel+'_'+per+'.tmp')
        for line in file :
            values = line.split()
            if len(values) == 1 :
                if not contained(values[0], subsets) :
                    subsets.append(values[0])
            lines[per].append(values)
        file.close()

    file = open('eff_'+channel+'_split.tmp', 'w')
    pidx = 1 if len(periods) > 1 else 0
    for i in range(len(lines[periods[pidx]])) :
        line = lines[periods[pidx]][i]
        if len(line) == 1 :
            file.write(line[0]+'\n')
        else :
            line_summed = []
            for per in periods :
                if i > len(lines[per])-1 :
                    continue
                for j in range(len(lines[per][i])) :
                    if len(line_summed) == j :
                        line_summed.append(float(lines[per][i][j]) if j>0 else str(lines[per][i][j]))
                    elif j>0 :
                        line_summed[j]+=float(lines[per][i][j])
            file.write("%s \t %f \t %f \n" % (line_summed[0], line_summed[1], line_summed[2]))
    file.close()

    ## lines used to add sub-categories
    lines = dict([(sub, []) for sub in subsets])
    ## combine sub-categories
    file = open('eff_'+channel+'_split.tmp')
    file_empty = True
    for line in file :
        file_empty = False
        values = line.split()
        if len(values) == 1 :
            subset = values[0]
        else :
            for value in values :
                lines[subset].append(value)
    file.close()
    if not file_empty :
        file = open('eff_'+channel+'.tmp', 'w')
        for cat, subsets in categories.iteritems() :
            file.write(channel+'_'+cat+'\n')
            if len(subsets) == 0 :
                if options.analysis == "mssm" or options.analysis == "mssm_taupt" : 
                    file.write("%s \t %s \t %s \n" % (lines[channel+'_'+cat][0], lines[channel+'_'+cat][1], lines[channel+'_'+cat][2]))
                    file.write("%s \t %s \t %s \n" % (lines[channel+'_'+cat][3], lines[channel+'_'+cat][4], lines[channel+'_'+cat][5]))
                else :
                    file.write("%s \t %s \t %s \n" % (lines[channel+'_'+cat][0], lines[channel+'_'+cat][1], lines[channel+'_'+cat][2]))
                    file.write("%s \t %s \t %s \n" % (lines[channel+'_'+cat][3], lines[channel+'_'+cat][4], lines[channel+'_'+cat][5]))
                    file.write("%s \t %s \t %s \n" % (lines[channel+'_'+cat][6], lines[channel+'_'+cat][7], lines[channel+'_'+cat][8]))
            else :
                lines_summed = {}
                if options.analysis == "mssm" or options.analysis == "mssm_taupt" :
                    lines_summed = {
                        'ggH' : 0.,
                        'bbH' : 0.,
                        }
                else:
                    lines_summed = {
                        'ggH' : 0.,
                        'qqH' : 0.,
                        'VH'  : 0.,
                        }
                for sub in subsets :
                    if options.analysis == "mssm" or options.analysis == "mssm_taupt" :
                        lines_summed['ggH']+=float(lines[channel+'_'+cat+'_'+sub][1])
                        lines_summed['bbH']+=float(lines[channel+'_'+cat+'_'+sub][4])
                    else :
                        if len(lines[channel+'_'+cat+'_'+sub])>0 :
                            lines_summed['ggH']+=float(lines[channel+'_'+cat+'_'+sub][1])
                            lines_summed['qqH']+=float(lines[channel+'_'+cat+'_'+sub][4])
                            lines_summed['VH' ]+=float(lines[channel+'_'+cat+'_'+sub][7])
                if options.analysis == "mssm" or options.analysis == "mssm_taupt" :
                    file.write("%s \t %f \t %s \n" % (lines[channel+'_'+cat+'_'+sub][0], lines_summed['ggH'], lines[channel+'_'+cat+'_'+sub][2]))
                    file.write("%s \t %f \t %s \n" % (lines[channel+'_'+cat+'_'+sub][3], lines_summed['bbH'], lines[channel+'_'+cat+'_'+sub][5]))
                else :
                    if len(lines[channel+'_'+cat+'_'+sub])>0 :
                        file.write("%s \t %f \t %s \n" % (lines[channel+'_'+cat+'_'+sub][0], lines_summed['ggH'], lines[channel+'_'+cat+'_'+sub][2]))
                        file.write("%s \t %f \t %s \n" % (lines[channel+'_'+cat+'_'+sub][3], lines_summed['qqH'], lines[channel+'_'+cat+'_'+sub][5]))
                        file.write("%s \t %f \t %s \n" % (lines[channel+'_'+cat+'_'+sub][6], lines_summed['VH' ], lines[channel+'_'+cat+'_'+sub][8]))
        file.close()

def make_tables(channel, categories, category_labels):
    """
    Create a formated tex output from a set of *.tmp input files. These files must have been produced
    before hand. The argument categories corresponds to a list of (main) event categories to be shown
    in the table. The argument categoriy_labels corresponds to a dictionary of all possible categories
    that could appear in the table to the corresponding category label that should be shown in tex
    format.
    """
    ## single column format: two right-left adjacent sub-coumns, separated by \pm 
    column_format = "r@{$ \,\,\pm\,\, $}l|"
    ## single column head: corresponding to a right-left adjacent pair of sub-columns. {LABEL} should be filled by str.format.
    column_head = " & \multicolumn{2}{c|}{%s}"

    def table_line(head, single_column_format, entries, labels={}, tail="") :
        line = head
        for i in range(0, len(entries)) :
            if len(labels) == 0 :
                line+=single_column_format
            else :
                line+=single_column_format % labels[entries[i]]
        line+= tail
        return line

    table = channel+'.tex'
    output = open(table,'w')
    output.write(table_line("\\begin{tabular}{|l|", column_format, categories, {}, "} \n"))
    output.write("\\hline \n")
    output.write(table_line("Process", column_head, categories, category_labels, "\\\\ \n"))
    output.write("\\hline \n")
    ## pick yields from tmp files as recored of format (sample, rate, uncert); for data only
    ## the value is picked
    records = []
    data    = []
    samples = dict([(cat, {}) for cat in categories])
    for cat in categories :
        file = open(channel+'_'+cat+'.tmp')
        for line in file:
            values = line.split()
            if values[0] == "Data" :
                data.append(float(values[1]))
            else :
                records.append((values[0], float(values[1]), float(values[2])))
        file.close()
        ## translate lists into dictionaries and add an entry for ZLL if needed
        samples[cat] = dict([(rec[0],(rec[1],rec[2])) for rec in records])
        if 'ZJ' in samples[cat] and 'ZL' in samples[cat] and not 'ZLL' in samples[cat]:
            samples[cat]['ZLL'] = (samples[cat]['ZL'][0]+samples[cat]['ZJ'][0], math.sqrt(samples[cat]['ZL'][1]*samples[cat]['ZL'][1]+samples[cat]['ZJ'][1]*samples[cat]['ZJ'][1]))
        if 'Dibosons' in samples[cat] and 'WJets' in samples[cat] and not 'EWK' in samples[cat]:
            samples[cat]['EWK'] = (samples[cat]['Dibosons'][0]+samples[cat]['WJets'][0], math.sqrt(samples[cat]['Dibosons'][1]*samples[cat]['Dibosons'][1]+samples[cat]['WJets'][1]*samples[cat]['WJets'][1]))
        elif 'Dibosons' in samples[cat] and not 'WJets' in samples[cat] and not 'EWK' in samples[cat]:
            samples[cat]['EWK'] = (samples[cat]['Dibosons'][0], samples[cat]['Dibosons'][1])
    ## order in which the samples should be shown in the table
    sample_order = {
        "tt" : ["ZTT", "QCD", "W", "ZJ", "TT", "VV", "Total", "Signal"],
        "mt" : ["ZTT", "QCD", "W", "ZLL", "TT", "VV", "Total", "Signal"],
        "et" : ["ZTT", "QCD", "W", "ZLL", "TT", "VV", "Total", "Signal"],
        "mm" : ["ZTT", "ZMM", "QCD", "TTJ", "EWK", "Total", "Signal"],
        "ee" : ["ZTT", "ZEE", "QCD", "TTJ", "EWK", "Total", "Signal"],
        "em" : ["Ztt", "Fakes", "ttbar", "EWK","Total", "Signal"],
        }
    ## labels of the samples that should appear in the table
    sample_labels = {
        "ZTT"      : 'Z$\\rightarrow \\tau\\tau$   ',
        "Ztt"      : 'Z$\\rightarrow \\tau\\tau$   ',
        "QCD"      : 'QCD                          ',
        "Fakes"    : 'QCD                          ',
        "W"        : 'W+jets                       ',
        "WJets"    : 'W+jets                       ',
        "ZLL"      : 'Z+jets (l/jet faking $\\tau$)',
        "ZJ"       : 'Z+jets (l/jet faking $\\tau$)',
        "ZMM"      : 'Z$\\rightarrow \\mu\\mu$     ',
        "ZEE"      : 'Z$\\rightarrow ee$           ',
        "TT"       : 't$\\bar{\\rm{t}}$            ',
        "ttbar"    : 't$\\bar{\\rm{t}}$            ',
        "TTJ"      : 't$\\bar{\\rm{t}}$            ',
        "EWK"      : 'Dibosons                     ',
        "VV"       : 'Dibosons                     ',
        "Dibosons" : 'Dibosons                     ',
        "Total"    : 'Total Background             ',
        "Signal"   : 'H$\\rightarrow\\tau\\tau$    ',
        "Data"     : 'Data                         ',
        "ggH"      : 'gg$\\rightarrow$ H           ',
        "qqH"      : 'qq$\\rightarrow$ H           ',
        "bbH"      : 'bb$\\rightarrow$ H           ',
        "VH"       : 'qq$\\rightarrow$ Ht$\overline{\\rm{t}}$ or VH ',
                }
    ## add yields for all samples, sum of all backgrounds and summed signal
    for sample in sample_order[channel] :
        line = sample_labels[sample]
        for i in range(len(categories)) :
            for x in [0, 1] :
                template = "\t & \t {DIGIT}".format(DIGIT=digit(samples[categories[i]][sample][x]))
                line += template % samples[categories[i]][sample][x]
        line+="\t \\\\ \n"
        if line.startswith('Total') :
            output.write("\\hline \n")
        output.write(line)
        output.write("\\hline \n")
    ## add data yields
    line = sample_labels['Data']
    for i in range(len(categories)) :
        template = "\t & \multicolumn{2}{|c|}{%s}" % digit(data[i])    
        line += template % data[i]
    line+="\t \\\\ \n"
    output.write(line)
    output.write("\\hline \n")
    
    ## add efficiencies
    output.write('\\multicolumn{%d}{c}{ } \\\\\n' % (1+2*len(categories)))
    output.write('\\multicolumn{%d}{l}{Signal Eff.} &  \\multicolumn{%d}{c}{ } \\\\\n' % (2, -1+2*len(categories)))
    output.write('\\hline\n')
    
    file = open('eff_'+channel+'.tmp')
    records = dict([(cat, []) for cat in categories])
    for line in file :
        values = line.split()
        if len(values) == 1 :
            cat = values[0][len(channel)+1:]
        else :
            for value in values :
                records[cat].append(value)
    file.close()
    
    effs = {}
    lines = {}
    signals_samples = []
    if options.analysis == 'mssm' or options.analysis == 'mssm_taupt' :
        signal_samples = ['ggH', 'bbH']
    else :
        signal_samples = ['ggH', 'qqH', 'VH']
    for sig in signal_samples :
        lines[sig]  = sample_labels[sig]
    for cat in categories :
        values = records[cat]
        if len(values)>0 :
            if options.analysis == "mssm" or options.analysis == 'mssm_taupt' :
                effs['ggH'] = '%.2e' % (float(values[1])/float(values[2]))
                effs['bbH'] = '%.2e' % (float(values[4])/float(values[5]))
            else :
                effs['ggH'] = '%.2e' % (float(values[1])/float(values[2]))
                effs['qqH'] = '%.2e' % (float(values[4])/float(values[5]))
                effs['VH' ] = '%.2e' % (float(values[7])/float(values[8]))
            for sig in signal_samples :
                lines[sig] += "\t & \t \multicolumn{2}{|c|}{%s $\cdot 10^{-%d}$}" % (effs[sig][:effs[sig].find('e')], int(effs[sig][effs[sig].find('-')+1:]))
        else :
            for sig in signal_samples :
                lines[sig] += "\t & \t \multicolumn{2}{|c|}{ - }"
    for sig in signal_samples :
        lines[sig] += "\\\\ \n"
        output.write(lines[sig])
        output.write("\\hline \n")
    ## and close
    output.write("\\end{tabular} \n")
    output.write("\\label{tab:cutflow-%s-%s} \n" % (channel, "7+8TeV"))
    output.write("\\end{center} \n")
    output.write("\\end{table*} \n")
    return
    

## channels to be considered
channels = options.channels.split()
for idx in range(len(channels)) : channels[idx] = channels[idx].rstrip(',')## channels
## categories to be considered
categories = options.categories.split()
for idx in range(len(categories)) : categories[idx] = categories[idx].rstrip(',')
## periods to be considered
periods = options.period.split()
for idx in range(len(periods)) : periods[idx] = periods[idx].rstrip(',')
## extended dictionary of subsets to be contracted (used for merging of table yields)
if len(periods) == 1 and contained('7TeV', periods) :
    if options.analysis == "mssm" or options.analysis == "mssm_taupt" :
        subsets_extended = {
            "btag"  : ["7TeV"],
            "nobtag": ["7TeV"],
            }
    else :
        if len(channels) == 1 and contained('em', channels) :
            subsets_extended = {
                "0jet"  : ["low_7TeV", "high_7TeV"],
                "1jet"  : ["low_7TeV", "high_7TeV"],
                "vbf"   : ["loose_7TeV"],
                }
        elif len(channels) == 1 and contained('et', channels) :
            subsets_extended = {
                "0jet"  : ["medium_7TeV", "high_7TeV"],
                "1jet"  : ["medium_7TeV", "high_mediumhiggs_7TeV"],
                "vbf"   : ["loose_7TeV"],
                }
        elif len(channels) == 1 and contained('mt', channels) :
            subsets_extended = {
                "0jet"  : ["medium_7TeV", "high_7TeV"],
                "1jet"  : ["medium_7TeV", "high_lowhiggs_7TeV", "high_mediumhiggs_7TeV"],
                "vbf"   : ["loose_7TeV"],
                }
        elif len(channels) == 1 and contained('mm', channels) :
            subsets_extended = {
                "0jet"  : ["low_7TeV", "high_7TeV"],
                "1jet"  : ["low_7TeV", "high_7TeV"],
                "vbf"   : ["7TeV"],
                }
        elif len(channels) == 1 and contained('ee', channels) :
            subsets_extended = {
                "0jet"  : ["low_7TeV", "high_7TeV"],
                "1jet"  : ["low_7TeV", "high_7TeV"],
                "vbf"   : ["7TeV"],
                }
        else :
            subsets_extended = {}
if len(periods) == 1 and contained('8TeV', periods) :
    if options.analysis == "mssm" :
        subsets_extended = {
            "btag"  : ["8TeV"],
            "nobtag": ["8TeV"],
            }
    elif options.analysis == "mssm_taupt" :
        if len(channels) == 1 and contained('em', channels) :
            subsets_extended = {
                "btag"  : ["8TeV"],
                "nobtag": ["8TeV"],
                }
        elif len(channels) == 1 and contained('et', channels) :
            subsets_extended = {
                "btag"  : ["low_8TeV", "high_8TeV"],
                "nobtag"  : ["low_8TeV", "medium_8TeV", "high_8TeV"],
                }
        elif len(channels) == 1 and contained('mt', channels) :
            subsets_extended = {
                "btag"  : ["low_8TeV", "high_8TeV"],
                "nobtag"  : ["low_8TeV", "medium_8TeV", "high_8TeV"],
                }
        elif len(channels) == 1 and contained('tt', channels) :
            subsets_extended = {
                "btag"  : ["low_8TeV", "high_8TeV"],
                "nobtag"  : ["low_8TeV", "medium_8TeV", "high_8TeV"],
                }
        elif len(channels) == 1 and contained('mm', channels) :
            subsets_extended = {
                "btag"  : ["8TeV"],
                "nobtag": ["8TeV"],
                }
        elif len(channels) == 1 and contained('ee', channels) :
            subsets_extended = {
                "btag"  : ["8TeV"],
                "nobtag": ["8TeV"],
                }
        else :
            subsets_extended = {}
    else :
        if len(channels) == 1 and contained('em', channels) :
            subsets_extended = {
                "0jet"  : ["low_8TeV", "high_8TeV"],
                "1jet"  : ["low_8TeV", "high_8TeV"],
                "vbf"   : ["loose_8TeV", "tight_8TeV"],
                }
        elif len(channels) == 1 and contained('et', channels) :
            subsets_extended = {
                "0jet"  : ["medium_8TeV", "high_8TeV"],
                "1jet"  : ["medium_8TeV", "high_mediumhiggs_8TeV"],
                "vbf"   : ["loose_8TeV", "tight_8TeV"],
                }
        elif len(channels) == 1 and contained('mt', channels) :
            subsets_extended = {
                "0jet"  : ["medium_8TeV", "high_8TeV"],
                "1jet"  : ["medium_8TeV", "high_lowhiggs_8TeV", "high_mediumhiggs_8TeV"],
                "vbf"   : ["loose_8TeV", "tight_8TeV"],
                }
        elif len(channels) == 1 and contained('tt', channels) :
            subsets_extended = {
                "1jet"  : ["high_mediumhiggs_8TeV", "high_highhiggs_8TeV"],
                "vbf"   : ["8TeV"],
                }
        elif len(channels) == 1 and contained('mm', channels) :
            subsets_extended = {
                "0jet"  : ["low_8TeV", "high_8TeV"],
                "1jet"  : ["low_8TeV", "high_8TeV"],
                "vbf"   : ["8TeV"],
                }
        elif len(channels) == 1 and contained('ee', channels) :
            subsets_extended = {
                "0jet"  : ["low_8TeV", "high_8TeV"],
                "1jet"  : ["low_8TeV", "high_8TeV"],
                "vbf"   : ["8TeV"],
                }
        else :
            subsets_extended = {}
if contained('7TeV', periods) and contained('8TeV', periods) :
    if options.analysis == "mssm" :
        subsets_extended = {
            "btag"  : ["7TeV", "8TeV"],
            "nobtag": ["7TeV", "8TeV"],
            }
    elif options.analysis == "mssm_taupt" :
        if len(channels) == 1 and contained('em', channels) :
            subsets_extended = {
                "btag"  : ["7TeV", "8TeV"],
                "nobtag": ["7TeV", "8TeV"],
                }
        elif len(channels) == 1 and contained('et', channels) :
            subsets_extended = {
                "btag"  : ["7TeV", "low_8TeV", "high_8TeV"],
                "nobtag": ["7TeV", "low_8TeV", "medium_8TeV", "high_8TeV"],
                }
        elif len(channels) == 1 and contained('mt', channels) :
            subsets_extended = {
                "btag"  : ["7TeV", "low_8TeV", "high_8TeV"],
                "nobtag": ["7TeV", "low_8TeV", "medium_8TeV", "high_8TeV"],
                }
        elif len(channels) == 1 and contained('tt', channels) :
            subsets_extended = {
                "btag"  : ["7TeV", "low_8TeV", "high_8TeV"],
                "nobtag": ["7TeV", "low_8TeV", "medium_8TeV", "high_8TeV"],
                }
        elif len(channels) == 1 and contained('mm', channels) :
            subsets_extended = {
                "btag"  : ["7TeV", "8TeV"],
                "nobtag": ["7TeV", "8TeV"],
                }
        elif len(channels) == 1 and contained('ee', channels) :
            subsets_extended = {
                "btag"  : ["7TeV", "8TeV"],
                "nobtag": ["7TeV", "8TeV"],
                }
        else :
            subsets_extended = {}
    else :
        if len(channels) == 1 and contained('em', channels) :
            subsets_extended = {
                "0jet"  : ["low_7TeV", "low_8TeV", "high_7TeV", "high_8TeV"],
                "1jet"  : ["low_7TeV", "low_8TeV", "high_7TeV", "high_8TeV"],
                "vbf"   : ["loose_7TeV", "loose_8TeV", "tight_8TeV"],
                }
        elif len(channels) == 1 and contained('et', channels) :
            subsets_extended = {
                "0jet"  : ["medium_7TeV", "high_7TeV", "medium_8TeV", "high_8TeV"],
                "1jet"  : ["medium_7TeV", "high_mediumhiggs_7TeV", "medium_8TeV", "high_mediumhiggs_8TeV"],
                "vbf"   : ["loose_7TeV", "loose_8TeV", "tight_8TeV"],
                }
        elif len(channels) == 1 and contained('mt', channels) :
            subsets_extended = {
                "0jet"  : ["medium_7TeV", "high_7TeV", "medium_8TeV", "high_8TeV"],
                "1jet"  : ["medium_7TeV", "high_lowhiggs_7TeV", "high_mediumhiggs_7TeV", "medium_8TeV", "high_lowhiggs_8TeV", "high_mediumhiggs_8TeV"],
                "vbf"   : ["loose_7TeV", "loose_8TeV", "tight_8TeV"],
                }
        elif len(channels) == 1 and contained('tt', channels) :
            subsets_extended = {
                "1jet"  : ["high_mediumhiggs_8TeV", "high_highhiggs_8TeV"],
                "vbf"   : ["8TeV"],
                }
        elif len(channels) == 1 and contained('mm', channels) :
            subsets_extended = {
                "0jet"  : ["low_7TeV", "high_7TeV", "low_8TeV", "high_8TeV"],
                "1jet"  : ["low_7TeV", "high_7TeV", "low_8TeV", "high_8TeV"],
                "vbf"   : ["7TeV", "8TeV"],
                }
        elif len(channels) == 1 and contained('ee', channels) :
            subsets_extended = {
                "0jet"  : ["low_7TeV", "high_7TeV", "low_8TeV", "high_8TeV"],
                "1jet"  : ["low_7TeV", "high_7TeV", "low_8TeV", "high_8TeV"],
                "vbf"   : ["7TeV", "8TeV"],
                }
        else :
            subsets_extended = {}
## compact dictionary of subsets to be contraced (used fro mergin of efficiencies) and categories to be shown in the table(s)
if options.analysis == "mssm" :
    subsets_compact  = {
        'btag'     : [],
        'nobtag'   : [],
        }
    categories_in_table = [
        'btag',
        'nobtag',
        ]
    category_labels_in_table = {
        'btag'     : "\emph{B-Tag}",
        'nobtag'   : "\emph{No B-Tag}",
        }
elif options.analysis == "mssm_taupt" :
    if len(periods) == 1 and contained('7TeV', periods) :
        subsets_compact  = {
            'btag'     : [],
            'nobtag'   : [],
            }
        categories_in_table = [
            'btag',
            'nobtag',
            ]
        category_labels_in_table = {
            'btag'     : "\emph{B-Tag}",
            'nobtag'   : "\emph{No B-Tag}",
            }
    else :
        if len(channels) == 1 and contained('em', channels) :
            subsets_compact  = {
                'btag'     : [],
                'nobtag'   : [],
                }
        elif len(channels) == 1 and contained('et', channels) :
            subsets_compact  = {
                'btag'     : ['low', 'high'],
                'nobtag'   : ['low', 'medium', 'high'],
                }
        elif len(channels) == 1 and contained('mt', channels) :
            subsets_compact = {
                'btag'     : ['low', 'high'],
                'nobtag'   : ['low', 'medium', 'high'],
                }
        elif len(channels) == 1 and contained('tt', channels) :
            subsets_compact = {
                'btag'     : ['low', 'high'],
                'nobtag'   : ['low', 'medium', 'high'],
                }
        elif len(channels) == 1 and contained('mm', channels) :
            subsets_compact = {
                'btag'     : [],
                'nobtag'   : [],
                }
        elif len(channels) == 1 and contained('ee', channels) :
            subsets_compact = {
                'btag'     : [],
                'nobtag'   : [],
                }
        else :
            subsets_compact = {}
    categories_in_table = [
        'btag',
        'nobtag',
        ]
    category_labels_in_table = {
        'btag'     : "\emph{B-Tag}",
        'nobtag'   : "\emph{No B-Tag}",
        }
else :
    if len(periods) == 1 and contained('7TeV', periods) :
        if len(channels) == 1 and contained('em', channels) :
            subsets_compact  = {
                '0jet'     : ['low', 'high'],
                '1jet'     : ['low', 'high'],
                'vbf'      : ['loose'],
                }
        elif len(channels) == 1 and contained('et', channels) :
            subsets_compact = {
                "0jet"  : ['medium', 'high'],
                "1jet"  : ['medium', 'high_mediumhiggs'],
                "vbf"   : ['loose'],
                }
        elif len(channels) == 1 and contained('mt', channels) :
            subsets_compact = {
                "0jet"  : ['medium', 'high'],
                "1jet"  : ['medium', 'high_lowhiggs', 'high_mediumhiggs'],
                "vbf"   : ['loose'],
                }
        elif len(channels) == 1 and contained('mm', channels) :
            subsets_compact = {
                '0jet'     : ['low', 'high'],
                '1jet'     : ['low', 'high'],
                'vbf'      : [],
                }
        elif len(channels) == 1 and contained('ee', channels) :
            subsets_compact = {
                '0jet'     : ['low', 'high'],
                '1jet'     : ['low', 'high'],
                'vbf'      : [],
                }
        else :
            subsets_compact = {}
    else :
        if len(channels) == 1 and contained('em', channels) :
            subsets_compact  = {
                '0jet'     : ['low', 'high'],
                '1jet'     : ['low', 'high'],
                'vbf'      : ['loose', 'tight'],
                }
        elif len(channels) == 1 and contained('et', channels) :
            subsets_compact = {
                "0jet"  : ['medium', 'high'],
                "1jet"  : ['medium', 'high_mediumhiggs'],
                "vbf"   : ['loose', 'tight'],
                }
        elif len(channels) == 1 and contained('mt', channels) :
            subsets_compact = {
                "0jet"  : ['medium', 'high'],
                "1jet"  : ['medium', 'high_lowhiggs', 'high_mediumhiggs'],
                "vbf"   : ['loose', 'tight'],
                }
        elif len(channels) == 1 and contained('tt', channels) :
            subsets_compact = {
                "1jet"  : ['high_mediumhiggs', 'high_highhiggs'],
                "vbf"   : [],
                }
        elif len(channels) == 1 and contained('mm', channels) :
            subsets_compact = {
                '0jet'     : ['low', 'high'],
                '1jet'     : ['low', 'high'],
                'vbf'      : [],
                }
        elif len(channels) == 1 and contained('ee', channels) :
            subsets_compact = {
                '0jet'     : ['low', 'high'],
                '1jet'     : ['low', 'high'],
                'vbf'      : [],
                }
        else :
            subsets_compact = {}
    if len(channels) == 1 and contained('tt', channels) :
        categories_in_table = [
            '1jet',
            'vbf',
            ]
        category_labels_in_table = {
            '1jet'     : "\emph{1-Jet}",
            'vbf'      : "\emph{VBF}",
            }
    else :
        categories_in_table = [
            '0jet',
            '1jet',
            'vbf',
            ]
        category_labels_in_table = {
            '0jet'     : "\emph{0-Jet}",
            '1jet'     : "\emph{1-Jet}",
            'vbf'      : "\emph{VBF}",
            }

os.system("rm -f *.tmp")
for chn in channels :
    print "creating table for decay channel ", chn, "..."
    for period in periods :
        for cat in categories :
            path = None
            if options.analysis == "mssm" or options.analysis == "mssm_taupt":
                path = options.input+"/htt_"+chn+"_"+cat+"_"+period+"-"+options.mass[:options.mass.find(":")]+".txt"   
            else :
                path = options.input+"/htt_"+chn+"_"+cat+"_"+period+".txt"            
            ## extract all relevant information from datacards
            extractor(path, period)
    ## merge run periods and subsets of event categories (for yields)
    merge_subsets(chn, subsets_extended)
    ## merge run periods and subsets of event categories (for efficiencies)
    merge_efficiencies(chn, subsets_compact, periods)
    ## make formated tex tables from compactified input 
    make_tables(chn, categories_in_table, category_labels_in_table)
os.system("rm *.tmp")
