from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to produce postfit plots from a set of inputs cards (datacards), input histograms (root) and maximum likelihood fits for niussance parameter pulls (fitresults)")
## direct options
parser.add_option("-f", "--fitresults", dest="fitresults", default="fitresults/mlfit_{ANALYSIS}.txt", type="string", help="Path to the pulls of the maximum likelihood fit. [Default: \"fitresults/mlfit_{ANALYSIS}.txt\"]")
parser.add_option("-p", "--periods", dest="periods", default="7TeV 8TeV", type="string", help="List of run periods, for which postfit plots shuld be made. [Default: \"7TeV 8TeV\"]")
parser.add_option("-a", "--analysis", dest="analysis", default="sm", type="choice", help="Type of analysis (sm or mssm). Lower case is required. [Default: sm]", choices=["sm", "mssm"])
parser.add_option("-c", "--channels", dest="channels", default="em, et, mt", type="string", help="Channels for which postfit plots should be made. Individual channels should be separated by comma or whitespace. [Default: 'em, et, mt']")
parser.add_option("--sm-categories", dest="sm_categories", default="0 1 2 3 5", type="string", help="List sm of event categories. [Default: \"0 1 2 3 5\"]")
parser.add_option("--mssm-categories", dest="mssm_categories", default="0 1 2 3 6 7", type="string", help="List mssm of event categories. [Default: \"0 1 2 3 6 7\"]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) > 0 :
    parser.print_usage()
    exit(1)


from DatacardUtils import parse_dcard
# use parse_dcard to get a dictionary mapping sample name strings to fit weights

class Analysis:
    """
    A class designed to insert the proper scale factors into a pre-defined template set of plotting macros
    """
    def __init__(self, analysis, histfile, category, process_weight, template_fname, output_fname):
         """
         Takes a dictionary (mapping strings representing samples) of fit weights and inserts these into the template macro
         at template_fname. Output is written to output_fname
         """
         self.process_weight = process_weight
         self.template_fname = template_fname
         self.output_fname   = output_fname
         self.histfile       = histfile 
         self.category       = category
         self.analysis       = analysis

    def high_stat_category(self, cat) :
        if "0jet" in cat :
            return True
        if "boost" in cat :
            return True 
        #if "btag" in cat :
        #    return True
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
             line = line.replace("$DEFINE_MSSM", "#define MSSM" if self.analysis == "mssm" else "")
             line = line.replace("$DEFINE_EXTRA_SAMPLES", "#define EXTRA_SAMPLES" if self.high_stat_category(self.category) else "")
             line = line.replace(template_name, output_name)
             line = line.replace("$HISTFILE", self.histfile)
             line = line.replace("$CATEGORY", self.category)
             ## PATCH until Josh fixed his input files...
             if "et" in self.output_fname :
                 patch = "eTau" if "7TeV" in self.output_fname else "eleTau"
                 line = line.replace("$PATCH", patch)
             word_arr=line.split("\n")
             for process_name in self.process_weight.keys():
                 cand_str = "$%s" % process_name
                 output_cand = ""
                 if line.strip().startswith(cand_str):
                     print word_arr[0]
                     curr_name = process_name
                     print_me  = '''std::cout << "scaling by %f" << std::endl;''' % self.process_weight[curr_name]
                     out_line  = print_me+"hin->Scale(%f); break; \n" % self.process_weight[curr_name]
                     move_on   = True
                     output_file.write(out_line)
                     print out_line
             if not move_on:
                 output_file.write(line)
                 

## run periods
periods = options.periods.split()
for idx in range(len(periods)) : periods[idx] = periods[idx].rstrip(',')
## channels 
channels = options.channels.split()
for idx in range(len(channels)) : channels[idx] = channels[idx].rstrip(',')
## categories
categories = options.sm_categories.split() if options.analysis == "sm" else options.mssm_categories.split()
for idx in range(len(categories)) : categories[idx] = categories[idx].rstrip(',')
## fitresults
fitresults = options.fitresults.format(ANALYSIS=options.analysis)
## post-fit plots for all channels in sm and mssm
category_mapping = {
    "0" : "0jet_low",
    "1" : "0jet_high",
    "2" : "boost_low",
    "3" : "boost_high",
    "5" : "vbf",
    "6" : "btag_low",
    "7" : "btag_high",
    }

for chn in channels :
    for per in periods :
        for cat in categories :
            histfile = "htt_{CHN}.input_{PER}.root".format(CHN=chn, PER=per) if options.analysis == "sm" else "htt_{CHN}.inputs-mssm-{PER}-0.root".format(CHN=chn, PER=per)
            plots = Analysis(options.analysis, histfile, category_mapping[cat],
                             parse_dcard("datacards/htt_{CHN}_{CAT}_{PER}.txt".format(CHN=chn, CAT=cat, PER=per), fitresults, "ANYBIN"),
                             "templates/HTT_{CHN}_X_template.C".format(CHN=chn.upper()),
                             "htt_{CHN}_{CAT}_{PER}.C".format(CHN=chn, CAT=cat, PER=per)
                             )
            plots.run()

