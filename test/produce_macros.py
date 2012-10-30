from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to produce postfit plos from a set of inputs cards (datacards), input histograms (root) and maximum likelihood fits for niussance parameter pulls (fitresults)")
## direct options
parser.add_option("-f", "--fitresults", dest="fitresults", default="fitresults/mlfit_{ANALYSIS}.txt", type="string", help="Path to the pulls of the maximum likelihood fit. [Default: \"fitresults/mlfit_{ANALYSIS}.txt\"]")
parser.add_option("-p", "--periods", dest="periods", default="7TeV 8TeV", type="string", help="List of run periods, for which postfit plots shuld be made. [Default: \"7TeV 8TeV\"]")
parser.add_option("-a", "--analysis", dest="analysis", default="sm", type="choice", help="Type of analysis (sm or mssm). Lower case is required. [Default: sm]", choices=["sm", "mssm"])
parser.add_option("-c", "--channels", dest="channels", default="em, et, mt, mm", type="string", help="Channels for which postfit plots should be made. Individual channels should be separated by comma or whitespace. [Default: 'em, et, mt, mm']")
parser.add_option("-y", "--yields", dest="yields", default="1", type="int", help="Shift yield uncertainties. [Default: '1']")
parser.add_option("-s", "--shapes", dest="shapes", default="1", type="int", help="Shift shape uncertainties. [Default: '1']")
parser.add_option("-u", "--uncertainties", dest="uncertainties", default="0", type="int", help="Set uncertainties of backgrounds. [Default: '0']")
parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False, help="Run in verbose more. [Default: 'False']")
cats1 = OptionGroup(parser, "SM EVENT CATEGORIES", "Event categories to be picked up for the SM analysis.")
cats1.add_option("--sm-categories-mm", dest="mm_sm_categories", default="0 1 2 3 5", type="string", help="List mm of event categories. [Default: \"0 1 2 3 5\"]")
cats1.add_option("--sm-categories-em", dest="em_sm_categories", default="0 1 2 3 5", type="string", help="List em of event categories. [Default: \"0 1 2 3 5\"]")
cats1.add_option("--sm-categories-mt", dest="mt_sm_categories", default="0 1 2 3 5", type="string", help="List mt of event categories. [Default: \"0 1 2 3 5\"]")
cats1.add_option("--sm-categories-et", dest="et_sm_categories", default="0 1 2 3 5", type="string", help="List et of event categories. [Default: \"0 1 2 3 5\"]")
cats1.add_option("--sm-categories-tt", dest="tt_sm_categories", default="0 1", type="string", help="List of tt event categories. [Default: \"0 1\"]")
cats1.add_option("--sm-categories-vhtt", dest="vhtt_sm_categories", default="0 1", type="string", help="List of tt event categories. [Default: \"0 1\"]")
parser.add_option_group(cats1)
cats2 = OptionGroup(parser, "MSSM EVENT CATEGORIES", "Event categories to be used for the MSSM analysis.")
cats2.add_option("--mssm-categories-mm", dest="mm_mssm_categories", default="0 1 2 3 6 7", type="string", help="List mm of event categories. [Default: \"0 1 2 3 6 7\"]")
cats2.add_option("--mssm-categories-em", dest="em_mssm_categories", default="0 1 2 3 6 7", type="string", help="List em of event categories. [Default: \"0 1 2 3 6 7\"]")
cats2.add_option("--mssm-categories-mt", dest="mt_mssm_categories", default="0 1 2 3 6 7", type="string", help="List mt of event categories. [Default: \"0 1 2 3 6 7\"]")
cats2.add_option("--mssm-categories-et", dest="et_mssm_categories", default="0 1 2 3 6 7", type="string", help="List et of event categories. [Default: \"0 1 2 3 6 7\"]")
cats2.add_option("--mssm-categories-tt", dest="tt_mssm_categories", default="0 1", type="string", help="List of tt event categories. [Default: \"0 1\"]")
cats2.add_option("--mssm-categories-hmm", dest="hmm_mssm_categories", default="0 1", type="string", help="List of hmm event categories. [Default: \"0 1\"]")
parser.add_option_group(cats2)
## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) > 0 :
    parser.print_usage()
    exit(1)

## use parse_dcard to get a dictionary mapping
## sample name strings to fit weights
from DatacardUtils import parse_dcard
from ROOT import *
import math
import os

class Analysis:
    """
    A class designed to insert the proper scale factors into a pre-defined template set of plotting macros
    """
    def __init__(self, analysis, histfile, category, process_weight, process_shape_weight, process_uncertainties, process_shape_uncertainties, template_fname, output_fname):
         """
         Takes a dictionary (mapping strings representing samples) of fit weights and inserts these into the template macro
         at template_fname. Output is written to output_fname
         """
         self.process_weight = process_weight
         self.process_shape_weight = process_shape_weight
         self.process_uncertainties = process_uncertainties
         self.process_shape_uncertainties = process_shape_uncertainties
         self.template_fname = template_fname
         self.output_fname   = output_fname
         self.histfile       = histfile 
         self.category       = category
         self.analysis       = analysis

    def high_stat_category(self, cat) :
        """
        This function defines the categories in which ZLL is split into ZL and ZJ in the et and mt channels.
        """
        if "0jet" in cat :
            return True
        if "boost" in cat :
            return True 
        #if "btag" in cat :
        #    return True
        return False

    def signal_process(self, process) :
        if "ggH" in process :
            return True
        if "qqH" in process :
            return True
        if "VH"  in process :
            return True
        if "WH"  in process :
            return True
        if "ZH"  in process :
            return True
        if "bbH" in process :
            return True
        return False
        
    def run(self):
         """
         Inserts the weights into the macros
         """
         input_file = open(self.template_fname,'r')
         output_file = open(self.output_fname,'w')
         
         curr_name = ""
         for line in input_file:
             move_on = False
             template_name = self.template_fname[self.template_fname.find("/")+1:self.template_fname.rfind("_template.C")]
             output_name   = self.output_fname[:self.output_fname.rfind(".C")]
             ## prepare first lines of macro
             line = line.replace("$CMSSW_BASE", os.environ['CMSSW_BASE'])
             line = line.replace("$DEFINE_MSSM", "#define MSSM" if self.analysis == "mssm" else "")
             line = line.replace("$DEFINE_EXTRA_SAMPLES", "#define EXTRA_SAMPLES" if self.high_stat_category(self.category) else "")
             line = line.replace(template_name, output_name)
             line = line.replace("$HISTFILE", self.histfile)
             line = line.replace("$CATEGORY", self.category)
	     if options.uncertainties and (options.yields or options.shapes):
                line = line.replace("$DRAW_ERROR", 'if(scaled) errorBand->Draw("e2same");')
                line = line.replace("$ERROR_LEGEND", 'if(scaled) leg->AddEntry(errorBand, "bkg. uncertainty" , "F" );')
	     else:
                line = line.replace("$DRAW_ERROR", '')
                line = line.replace("$ERROR_LEGEND", '')
             word_arr=line.split("\n")
             uncertainties_set=[]
             for process_name in self.process_weight.keys():
                 if self.signal_process(process_name) :
                     cand_str = "${%s}%s" % (options.analysis.upper() , process_name)
                 else :
                     cand_str = "$%s" % process_name
                 output_cand = ""
                 if line.strip().startswith(cand_str):
                     if options.verbose :
                         print word_arr[0]
                     curr_name = process_name
                     move_on   = True
                     if options.yields:
                         print_me  = '''std::cout << "scaling by %f" << std::endl;''' % self.process_weight[curr_name]
                         out_line  = print_me+"hin->Scale(%f); \n" % self.process_weight[curr_name]
                         output_file.write(out_line)
                         if options.verbose :
                             print out_line
                         if options.uncertainties:

		             input = TFile("root/"+self.histfile)
                             #print "file: ", input.GetName()
		             for key in input.GetListOfKeys():
		               if self.category in key.GetName():
                                   remnant = cand_str.rstrip(process_name)
			           histname=key.GetName()+"/"+word_arr[0][len(remnant)+2:].strip().rstrip()
                             hist = input.Get(histname)
                             ## it can happen that histograms, which are present in SM
                             ## are not present in MSSM; in this case just skip hist
                             if not hist :
                                 continue
                             #print histname, self.histfile
                             for bin in range(1,hist.GetNbinsX()+1):
		               if not process_name+str(bin) in uncertainties_set:
			         uncertainties_set+=[process_name+str(bin)]
		                 uncertainty = math.sqrt(self.process_uncertainties[curr_name])
		                 out_line  = "hin->SetBinError(%(bin)i,hin->GetBinContent(%(bin)i)*%(uncertainty)f); \n" % {"bin":bin, "uncertainty":uncertainty}
                                 output_file.write(out_line)
                                 if options.verbose :
                                     print out_line
	     if options.shapes:
               for process_name in self.process_shape_weight.keys():
                 if self.signal_process(process_name) :
                     cand_str = "${%s}%s" % (options.analysis.upper() , process_name)
                 else :
                     cand_str = "$%s" % process_name
                 output_cand = ""
                 if line.strip().startswith(cand_str):
                     curr_name = process_name
                     for shape_name in self.process_shape_weight[curr_name]:
		       input = TFile("root/"+self.histfile)
		       for key in input.GetListOfKeys():
		           if self.category in key.GetName():
                               remnant = cand_str.rstrip(process_name)
			       histname=key.GetName()+"/"+word_arr[0][len(remnant)+2:].strip().rstrip()
                       hist = input.Get(histname)
                       hist_down = input.Get(histname+"_"+shape_name+"Down")
                       hist_up = input.Get(histname+"_"+shape_name+"Up")
                       #print histname, self.histfile
                       if not hist:
                         continue
                       for bin in range(1,hist.GetNbinsX()+1):
		         shift = self.process_shape_weight[curr_name][shape_name]
                         out_line = ''
			 value = 1
                         upper = hist_up.GetBinContent(bin)
                         lower = hist_down.GetBinContent(bin) if hist_down.GetBinContent(bin)>0.01 else 0.
                         central = hist.GetBinContent(bin)
		         if shift>0 and central>0 and upper!=central:
                             if central :
                                 value = shift*(upper/central-1)+1
		         elif shift<0 and central>0 and lower!=central:
                             if lower :
                                 value = shift*(central/lower-1)+1
			 if value!=1:
		             print_me  = '''std::cout << "scaling bin %(bin)i by %(value)f" << std::endl;''' % {"bin":bin, "value":value}
		             out_line  = print_me+"hin->SetBinContent(%(bin)i,hin->GetBinContent(%(bin)i)*%(value)f); \n" % {"bin":bin, "value":value}
			 if options.uncertainties:
			   uncertainty=1
			   if hist_down.GetBinContent(bin) and hist.GetBinContent(bin):
			     uncertainty=max(uncertainty,hist.GetBinContent(bin)/hist_down.GetBinContent(bin),hist_down.GetBinContent(bin)/hist.GetBinContent(bin))
			   if hist_up.GetBinContent(bin) and hist.GetBinContent(bin):
			     uncertainty=max(uncertainty,hist.GetBinContent(bin)/hist_up.GetBinContent(bin),hist_up.GetBinContent(bin)/hist.GetBinContent(bin))
			   uncertainty = self.process_shape_uncertainties[curr_name][shape_name]*(uncertainty-1)
			   if options.verbose and uncertainty>1:
			       print "WARNING: There is a bin-by-bin uncertainty larger than 100%. Make sure there is no problem with the bin-by-bin uncertainties in the root file",histfile,"in",self.analysis,self.category,". Please check:",shape_name,"bin-down:",hist_down.GetBinContent(bin),"bin-center:",hist.GetBinContent(bin),"bin-up:",hist_up.GetBinContent(bin)
		           if not process_name+str(bin) in uncertainties_set:
   		               uncertainties_set+=[process_name+str(bin)]
                               out_line  += "hin->SetBinError(%(bin)i,hin->GetBinContent(%(bin)i)*%(uncertainty)f); \n" % {"bin":bin, "uncertainty":uncertainty}
			   elif uncertainty!=0:
                               out_line  += "hin->SetBinError(%(bin)i,sqrt(pow(hin->GetBinError(%(bin)i),2)+pow(hin->GetBinContent(%(bin)i)*%(uncertainty)f,2))); \n" % {"bin":bin, "uncertainty":uncertainty}
                         output_file.write(out_line)
                         if options.verbose :
                             if out_line :
                                 print out_line
             if not move_on:
                 output_file.write(line)
	     else:
                 output_file.write("break; \n")
                 

## run periods
periods = options.periods.split()
for idx in range(len(periods)) : periods[idx] = periods[idx].rstrip(',')
## channels 
channels = options.channels.split()
for idx in range(len(channels)) : channels[idx] = channels[idx].rstrip(',')
## switch to sm event categories
if options.analysis == "sm" :
    categories = {
        "mm"   : options.mm_sm_categories.split(),
        "em"   : options.em_sm_categories.split(),
        "mt"   : options.mt_sm_categories.split(),
        "et"   : options.et_sm_categories.split(),
        "tt"   : options.tt_sm_categories.split(),
        "vhtt" : options.vhtt_sm_categories.split(),
        }
## switch to mssm event categories
if options.analysis == "mssm" :
    categories = {
        "mm"   : options.mm_mssm_categories.split(),
        "em"   : options.em_mssm_categories.split(),
        "mt"   : options.mt_mssm_categories.split(),
        "et"   : options.et_mssm_categories.split(),
        "tt"   : options.tt_mssm_categories.split(),
        "hmm"  : options.hmm_mssm_categories.split(),
        }
for key in categories :
    for idx in range(len(categories[key])) : categories[key][idx] = categories[key][idx].rstrip(',')
## fitresults
fitresults = options.fitresults.format(ANALYSIS=options.analysis)
## post-fit plots for all channels in sm and mssm
category_mapping_classic = {
    "0" : "0jet_low",
    "1" : "0jet_high",
    "2" : "boost_low",
    "3" : "boost_high",
    "5" : "vbf",
    "6" : "btag_low",
    "7" : "btag_high",
    }
category_mapping_tautau = {
    "0" : "boost",
    "1" : "vbf",
    }
category_mapping = {
    "mm" : category_mapping_classic,
    "em" : category_mapping_classic,
    "mt" : category_mapping_classic,
    "et" : category_mapping_classic,
    "tt" : category_mapping_tautau
    }
for chn in channels :
    for per in periods :
        for cat in categories[chn] :
            histfile = "htt_{CHN}.input_{PER}.root".format(CHN=chn, PER=per) if options.analysis == "sm" else "htt_{CHN}.inputs-mssm-{PER}.root".format(CHN=chn, PER=per)
            if chn == "mm" :
                ## there is one speciality for mm, which need special input files
                histfile.replace(".root", "-svfit.root")
	    process_weight, process_shape_weight, process_uncertainties, process_shape_uncertainties = parse_dcard("datacards/htt_{CHN}_{CAT}_{PER}.txt".format(CHN=chn, CAT=cat, PER=per), fitresults, "ANYBIN")
            plots = Analysis(options.analysis, histfile, category_mapping[chn][cat],
                             process_weight, process_shape_weight, process_uncertainties, process_shape_uncertainties,
                             "templates/HTT_{CHN}_X_template.C".format(CHN=chn.upper()),
                             "htt_{CHN}_{CAT}_{PER}.C".format(CHN=chn, CAT=cat, PER=per)
                             )
            plots.run()

