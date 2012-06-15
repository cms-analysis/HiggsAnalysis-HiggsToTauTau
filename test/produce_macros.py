from DatacardUtils import parse_dcard
# use parse_dcard to get a dictionary mapping sample name strings to fit weights

class Analysis:
    """
    A class designed to insert the proper scale factors into a pre-defined template set of plotting macros
    """
    def __init__(self, histfile, category, process_weight, template_fname, output_fname):
         """
         Takes a dictionary (mapping strings representing samples) of fit weights and inserts these into the template macro
         at template_fname. Output is written to output_fname
         """
         self.process_weight = process_weight
         self.template_fname = template_fname
         self.output_fname   = output_fname
         self.histfile       = histfile 
         self.category       = category
         
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
             line = line.replace("$DEFINE_EXTRA_SAMPLES", "#define EXTRA_SAMPLES" if "0jet" in self.category else "")
             line = line.replace(template_name, output_name)
             line = line.replace("$HISTFILE", self.histfile)
             line = line.replace("$CATEGORY", self.category)
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
                 

# specify the fit results text files for sm and mssm cases                    
mssm_fit_path = "fitresults/mlfit_mssm.txt"
sm_fit_path   = "fitresults/mlfit_sm.txt"    
tmp_dir       ="templates/"

## post-fit plots for all channels in MSSM 
#emu_b_ana = Analysis(parse_dcard("datacards/eleMu_B_mA120.txt",mssm_results,"ANYBIN"),tmp_dir+"emuAfterFit_b_template.C","emuAfterFit_b.C")
#emu_b_ana.run()
#
#emu_nob_ana = Analysis(parse_dcard("datacards/eleMu_NoB_mA120.txt",mssm_results,"ANYBIN"),tmp_dir+"emuAfterFit_nob_template.C","emuAfterFit_nob.C")
#emu_nob_ana.run()
#
#etau_b_ana = Analysis(parse_dcard("datacards/eleTau_B_mA120.txt",mssm_results,"ANYBIN"),tmp_dir+"etauAfterFit_b_template.C","etauAfterFit_b.C")
#etau_b_ana.run()
#
#etau_nob_ana = Analysis(parse_dcard("datacards/eleTau_NoB_mA120.txt",mssm_results,"ANYBIN"),tmp_dir+"etauAfterFit_nob_template.C","etauAfterFit_nob.C")
#etau_nob_ana.run()
#
#mutau_b_ana = Analysis(parse_dcard("datacards/muTau_B_mA120.txt",mssm_results,"ANYBIN"),tmp_dir+"mutauAfterFit_b_template.C","mutauAfterFit_b.C")
#mutau_b_ana.run()
#
#mutau_nob_ana = Analysis(parse_dcard("datacards/muTau_NoB_mA120.txt",mssm_results,"ANYBIN"),tmp_dir+"mutauAfterFit_nob_template.C","mutauAfterFit_nob.C")
#mutau_nob_ana.run()


## post-fit plots for all channels in SM 
category_mapping = {
    "0" : "0jet_low",
    "1" : "0jet_high",
    "2" : "boost_low",
    "3" : "boost_high",
    "5" : "vbf",
    }

for chn in ["em", "et", "mt"] :
    for per in ["7TeV"] :
        for cat in ["0", "1", "2", "3", "5"] :
            plots = Analysis("htt_{CHN}.input_{PER}.root".format(CHN=chn, PER=per),
                             category_mapping[cat],
                             parse_dcard("datacards/htt_{CHN}_{CAT}_{PER}.txt".format(CHN=chn, CAT=cat, PER=per), sm_fit_path, "ANYBIN"),
                             tmp_dir+"HTT_{CHN}_X_template.C".format(CHN=chn.upper()),
                             "htt_{CHN}_{CAT}_{PER}.C".format(CHN=chn, CAT=cat, PER=per)
                             )
            plots.run()

