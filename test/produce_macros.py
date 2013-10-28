from HiggsAnalysis.HiggsToTauTau.LimitsConfig import configuration
from optparse import OptionParser, OptionGroup
import os


## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to produce postfit plos from a set of inputs cards (datacards), input histograms (root) and maximum likelihood fits for niussance parameter pulls (fitresults)")
## direct options
parser.add_option("-f", "--fitresults", dest="fitresults", default="fitresults/mlfit_{ANALYSIS}.txt", type="string", help="Path to the pulls of the maximum likelihood fit. [Default: \"fitresults/mlfit_{ANALYSIS}.txt\"]")
parser.add_option("-a", "--analysis", dest="analysis", default="sm", type="choice", help="Type of analysis (sm or mssm). Lower case is required. [Default: sm]", choices=["sm", "mssm"])
parser.add_option("-y", "--yields", dest="yields", default="1", type="int", help="Shift yield uncertainties. [Default: '1']")
parser.add_option("-s", "--shapes", dest="shapes", default="1", type="int", help="Shift shape uncertainties. [Default: '1']")
parser.add_option("--shapes-mm-special", dest="shapes_mm_special", default="0", type="int", help="Shift shape uncertainties in the mm channel. This option is needed to make an estimate on the additional stat. uncertainties in the mm channel when using the msv distribution instead of the actual 2-d discriminator folded to 1 dimonesion, which goes into hte limit calculation in the MSSM analysis. This option automatically switches the option --shapes to 0, as this option is not applicable in this case. [Default: '0']")
parser.add_option("--mA", dest="mA", default="160", type="float", help="Mass of pseudoscalar mA only needed for mssm. [Default: '160']")
parser.add_option("--tanb", dest="tanb", default="8", type="float", help="Tanb only needed for mssm. [Default: '8']")
parser.add_option("-u", "--uncertainties", dest="uncertainties", default="1", type="int", help="Set uncertainties of backgrounds. [Default: '1']")
parser.add_option("-o", "--omit", dest="omit", default="0", type="int", help="Do not include uncertainty from original file. [Default: '0']")
parser.add_option("--asimov", dest="asimov", action="store_true", default=False, help="Use asimov dataset for postfit-plots. [Default: 'False']")
parser.add_option("--no-0jet-signal", dest="no_zero_jet", action="store_false", default=False, help="Add signal in the 0-jet event category of the mt, et, em channels [Default: False]")
parser.add_option("--add-mutau-soft", dest="add_mutau_soft", action="store_true", default=False, help="Add the soft categories to the mt channel [Default: False]")
parser.add_option("--hww-signal", dest="hwwsig", action="store_true", default=False, help="Add H->WW processes as background to the em channel [Default: False]")
parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False, help="Run in verbose more. [Default: 'False']")
parser.add_option("-c", "--config", dest="config", default="", help="Additional configuration file for the channels, periods and categories. [Default: '']")

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) > 0 :
    parser.print_usage()
    exit(1)

## switch option.shapes off inany case when option.shapes_mm_special is active,
## as in this case option shapes is not applicable
if options.shapes_mm_special :
    options.shapes = 0

## use parse_dcard to get a dictionary mapping
## sample name strings to fit weights
from DatacardUtils import parse_dcard
from ROOT import *
from HiggsAnalysis.HiggsToTauTau.tools.mssm_xsec_tools import mssm_xsec_tools ##not needed atm
from HiggsAnalysis.HiggsToTauTau.ModelParams_BASE import ModelParams_BASE

import math

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
         self.scale_output   = {}

    def drop_wjets_from_templates(self, output_name, cat) :
        """
        Indicate the event categories and channels in which to drop $Wjets from the templates. 
        """
        if 'htt_mm' in output_name :
            if cat == 'btag' :
                return True
        return False

    def high_stat_category(self, cat) :
        """
        This function defines the categories in which ZLL is split into ZL and ZJ in the et and mt channels.
        """
        if "0jet" in cat :
            return True
        if "1jet" in cat :
            return True 
        if "nobtag" in cat :
            return True
        if "btag" in cat:
            return True
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

    def drop_signal(self, category) :
        if options.no_zero_jet:
            if '0jet' in category:
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
             line = line.replace("$DEFINE_ASIMOV", "#define ASIMOV" if options.asimov else "")
             line = line.replace("$DEFINE_MSSM", "#define MSSM" if self.analysis == "mssm" else "")
             line = line.replace("$DEFINE_DROP_SIGNAL", "#define DROP_SIGNAL" if self.drop_signal(self.category) else "")
             line = line.replace("$DEFINE_HWWBG", "#define HWW_BG" if not options.hwwsig else "")
             line = line.replace("$BLIND", "false" if config.unblind else "true")
             line = line.replace("$DEFINE_EXTRA_SAMPLES", "#define EXTRA_SAMPLES" if self.high_stat_category(self.category) else "")
             line = line.replace(template_name, output_name)
             line = line.replace("$HISTFILE", self.histfile)
             line = line.replace("$CATEGORY", self.category)
             if self.drop_wjets_from_templates(output_name, self.category) :
                 line = line.replace("$WJets", "break;")
             if(options.analysis=="mssm") :
                 line = line.replace("$MA" , str(int(options.mA)))
                 line = line.replace("$TANB", str(int(options.tanb)))
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
                         print_me  = '''std::cout << "scaling by %(value)f %(name)s" << std::endl;''' % {"value":self.process_weight[curr_name],"name":curr_name}
                         out_line  = print_me+"hin->Scale(%f); \n" % self.process_weight[curr_name]
                         output_file.write(out_line)
                         self.scale_output[curr_name]=[self.process_weight[curr_name]]
                         if options.verbose :
                             print out_line
                         if options.uncertainties:
		             input = TFile("root/"+self.histfile)
                             #print "file: ", input.GetName()
		             for key in input.GetListOfKeys():
                                 if self.category=="_".join(key.GetName().split("_")[1:]):
                                     remnant = cand_str.rstrip(process_name)
                                     histname=key.GetName()+"/"+word_arr[0][len(remnant)+2:].strip().rstrip()
			     hist = input.Get(histname)
                             ## it can happen that histograms, which are present in SM
                             ## are not present in MSSM; in this case just skip hist
                             if not hist :
                                 continue
                             #print histname, self.histfile
                             self.scale_output[curr_name].append(math.sqrt(self.process_uncertainties[curr_name]))
                             for bin in range(1,hist.GetNbinsX()+1):
		               if not process_name+str(bin) in uncertainties_set:
                                   uncertainties_set+=[process_name+str(bin)]
                                   uncertainty = math.sqrt(self.process_uncertainties[curr_name])
                                   if uncertainty>0:
                                       ## in the case of options.shape_mm_special add the statistical uncertainty of each template
                                       ## to the normalization uncertainties from the fit in quadrature. Shape altering uncertainties
                                       ## from the fit are switched off, as they to not apply on the msv histograms, for which they
                                       ## have not been derived. 
                                       if options.shapes_mm_special :
                                           print "Adding stat. uncerainties from MC temapltes in mode --shapes-mm-special"
                                           uncertainty_norm = hist.GetBinContent(bin) if hist.GetBinContent(bin)>0 else 1.
                                           uncertainty=math.sqrt(uncertainty*hist.GetBinContent(bin)*uncertainty*hist.GetBinContent(bin)+
                                                                 hist.GetBinError(bin)*hist.GetBinError(bin))/uncertainty_norm
                                       out_line  = "hin->SetBinError(%(bin)i,hin->GetBinContent(%(bin)i)*%(uncertainty)f); \n" % {"bin":bin, "uncertainty":uncertainty}
                                       output_file.write(out_line)
                                   if options.verbose :
                                       print out_line
                                   elif options.verbose:
                                       print "WARNING: There is a zero yield uncertainty. Maybe you are missing uncertainties in the datacards which are in the fitresult in",
                                       self.analysis,self.category,". Please check."
	     if options.shapes:
               for process_name in self.process_shape_weight.keys():
                 if self.signal_process(process_name) :
                     cand_str = "${%s}%s" % (options.analysis.upper() , process_name)
                 else :
                     cand_str = "$%s" % process_name
                 output_cand = ""
                 if line.strip().startswith(cand_str):
		     if options.verbose:
		         print cand_str
                     curr_name = process_name
                     for shape_name in self.process_shape_weight[curr_name]:
		       if options.verbose:
		         print shape_name
		       input = TFile("root/"+self.histfile)
		       for key in input.GetListOfKeys():
		           if self.category=="_".join(key.GetName().split("_")[1:]):
                               remnant = cand_str.rstrip(process_name)
			       histname=key.GetName()+"/"+word_arr[0][len(remnant)+2:].strip().rstrip()
                       hist = input.Get(histname)
                       hist_down = input.Get(histname+"_"+shape_name+"Down")
                       hist_up = input.Get(histname+"_"+shape_name+"Up")
                       if not hist or not hist_down or not hist_up :
                         continue
                       for bin in range(1,hist.GetNbinsX()+1):
		         shift = self.process_shape_weight[curr_name][shape_name]
                         out_line = ''
			 value = 0
		         if shift>0:
                             value = (hist_up.GetBinContent(bin)-hist.GetBinContent(bin))/hist.GetBinWidth(bin)
		         elif shift<0:
                             value = (hist.GetBinContent(bin)-hist_down.GetBinContent(bin))/hist.GetBinWidth(bin)
			 if value!=0:
		             print_me  = '''std::cout << "scaling bin %(bin)i by %(shift)f %(name)s" << std::endl;''' % {"bin":bin, "shift":shift, "name":shape_name}
		             out_line = print_me+"hin->SetBinContent(%(bin)i,hin->GetBinContent(%(bin)i)+%(value)f); \n" % {"bin":bin, "value":value*shift}
			 if options.uncertainties:
			   if self.process_shape_uncertainties[curr_name][shape_name]>0.99 and self.process_shape_weight[curr_name][shape_name]==0:
			       if options.verbose:
			          print "WARNING: Nuisance parameter not constrained (>99%)",shape_name
			   uncertainty = self.process_shape_uncertainties[curr_name][shape_name]*abs(value)
			   if options.verbose and uncertainty>max(hist_down.GetBinContent(bin)/hist.GetBinWidth(bin),hist.GetBinContent(bin)/hist.GetBinWidth(bin),hist_up.GetBinContent(bin)/hist.GetBinWidth(bin)):
			       print "WARNING: There is a bin-by-bin uncertainty larger than 100%. Make sure there is no problem with the bin-by-bin uncertainties in the root file",histfile,"in",self.analysis,self.category,". Please check:",shape_name,"bin-down:",hist_down.GetBinContent(bin),"bin-center:",hist.GetBinContent(bin),"bin-up:",hist_up.GetBinContent(bin)
		           if not process_name+str(bin) in uncertainties_set:
   		               uncertainties_set+=[process_name+str(bin)]
                               if not options.omit:
                                   out_line  += "hin->SetBinError(%(bin)i,%(uncertainty)f); \n" % {"bin":bin, "uncertainty":uncertainty}
			   elif uncertainty!=0:
                               if not options.omit:
                                   out_line  += "hin->SetBinError(%(bin)i,sqrt(pow(hin->GetBinError(%(bin)i),2)+pow(%(uncertainty)f,2))); \n" % {"bin":bin, "uncertainty":uncertainty}
                         output_file.write(out_line)
                         if options.verbose :
                             if out_line :
                                 print out_line
             if not move_on:
                 output_file.write(line)
	     else:
                 output_file.write("break; \n")
                 





################

config=configuration(options.analysis, options.config, options.add_mutau_soft)
fitresults = options.fitresults.format(ANALYSIS=options.analysis)
for chn in config.channels :
    if chn == 'vhtt':
        continue
    for per in config.periods :
        for cat in config.categories[chn][per] :
            if chn == "hbb" :
                histfile = "{CHN}.input_{PER}-0.root".format(CHN=chn, PER=per)
            else :
                histfile = "htt_{CHN}.input_{PER}.root".format(CHN=chn, PER=per) if options.analysis == "sm" else "htt_{CHN}.inputs-mssm-{PER}-0.root".format(CHN=chn, PER=per, MA=str(int(options.mA)), TANB=str(int(options.tanb)))
                if chn == "mm" :
                ## there is one speciality for mm, which need special input files
                    histfile.replace(".root", "-svfit.root")
            if chn == "hbb" :
                process_weight, process_shape_weight, process_uncertainties, process_shape_uncertainties = parse_dcard("datacards/{CHN}_{CAT}_{PER}.txt".format(CHN=chn, CAT=cat, PER=per), fitresults, "ANYBIN")
                if cat=="6" :
                    plots = Analysis(options.analysis, histfile, config.categoryname[chn][config.categories[chn][per].index(cat)],
                                 process_weight, process_shape_weight, process_uncertainties, process_shape_uncertainties,
                                 "templates/{CHN}_LEP_X_template.C".format(CHN=chn.upper()),
                                 "{CHN}_{CAT}_{PER}.C".format(CHN=chn, CAT=cat, PER=per)
                                 )
                else :
                    plots = Analysis(options.analysis, histfile, config.categoryname[chn][config.categories[chn][per].index(cat)],
                                 process_weight, process_shape_weight, process_uncertainties, process_shape_uncertainties,
                                 "templates/{CHN}_HAD_X_template.C".format(CHN=chn.upper()),
                                 "{CHN}_{CAT}_{PER}.C".format(CHN=chn, CAT=cat, PER=per)
                                 )
            else :
                process_weight, process_shape_weight, process_uncertainties, process_shape_uncertainties = parse_dcard("datacards/htt_{CHN}_{CAT}_{PER}.txt".format(CHN=chn, CAT=cat, PER=per), fitresults, "ANYBIN")
                ## the work around for the naming is needed to account for vbf in 7TeV in et and mt
                if per == '7TeV' and cat == '6' and chn in ['mt','et']:
                   plots = Analysis(options.analysis, histfile, config.categoryname[chn][config.categories[chn][per].index(cat)][:3],
                                    process_weight, process_shape_weight, process_uncertainties, process_shape_uncertainties,
                                    "templates/HTT_{CHN}_X_template.C".format(CHN=chn.upper()),
                                    "htt_{CHN}_{CAT}_{PER}.C".format(CHN=chn, CAT=cat, PER=per)
                                    )
                else:
                   plots = Analysis(options.analysis, histfile, config.categoryname[chn][config.categories[chn][per].index(cat)],
                                    process_weight, process_shape_weight, process_uncertainties, process_shape_uncertainties,
                                    "templates/HTT_{CHN}_X_template.C".format(CHN=chn.upper()),
                                    "htt_{CHN}_{CAT}_{PER}.C".format(CHN=chn, CAT=cat, PER=per)
                                    )
            plots.run()
            scale_file=open("scales_{CHN}_{CAT}_{PER}.py".format(CHN=chn, CAT=cat, PER=per),'w')
            scale_file.write("scales="+str(plots.scale_output))
