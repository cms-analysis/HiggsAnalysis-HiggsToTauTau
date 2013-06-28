from optparse import OptionParser, OptionGroup
from HiggsAnalysis.CombinedLimit.DatacardParser import *

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="Test...\n")
parser_opts = OptionGroup(parser, "DATACARD PARSER OPTIONS", "These are the options that can be passed on to configure the datacard parsing.")
addDatacardParserOptions(parser_opts)
parser.add_option_group(parser_opts)
model_opts = OptionGroup(parser, "MODEL OPTIONS", "These are the options that can be passed on to configure the creation of the model datacards.")
#model_opts.add_option("--mA", dest="mA", default="", type="string",
#                       help="The value of the free mass parameter in the model. Default: \"\"]")
model_opts.add_option("--tanb", dest="tanb", default="", type="string",
                       help="The value of tanb in the model. Default: \"\"]")
parser.add_option_group(model_opts)
signal_opts = OptionGroup(parser, "signal OPTIONS", "What signal shapes should be plotted: bbH, ggH, cmb=ggH+bbH?")
signal_opts.add_option("--signal", dest="signal", default="cmb", type="choice",
                 help="Choose the signal process to be plotted. [Default: \"cmb\"]", choices=["cmb", "bbH", "ggH"])
parser.add_option_group(signal_opts)
## check number of arguments; in case print usage
(options, args) = parser.parse_args()
## check number of arguments; in case print usage
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
import re

            
def main() :
    path= os.getcwd()
    
##     os.chdir("%s/%s" % (path, args[0]))  
##     ##harvest of datacards
##     datacards = []
##     basket = os.listdir(os.getcwd())
##     if len(basket)<1 :
##         continue
##     for piece in basket :
##         if piece.endswith('.txt') :
##             datacards.append(piece)
##     optcards = ""
##     for card in datacards :
##         ## add channel name for combined datacards (same as datacard name but w/o .txt)
##         if card.find("mA")>1 :
##             optcards += card[:card.find("_mA")]
##         elif card.find("hggmva")>-1 or card.find("testcard")>-1 :
##             optcards += "hgg"
##         else :
##             optcards += card[:card.find(".txt")]
##     ## combination of datacards
##     os.system("combineCards.py -S %s > tmp.txt" % optcards)       
##     ## do tanb_grid_new to obtain datacard
##     os.system("python tanb_grid_new.py --mA {mass} --tanb {tanb}")



    card_file = open("{PATH}/{DIRECTORY}/debug/tmp_{TANB}.00.txt".format(PATH=path, DIRECTORY=args[0], TANB=options.tanb), 'r')

    
    signal_yield = 0.0
    numbers = []
    for input_line in card_file :
        words = input_line.split()
        if len(words) < 1: continue
        if words[0] == "process" :
            for (idx, word) in enumerate(words) :
                if idx==0 :
                    continue
                if word.isdigit() or word.lstrip("-").isdigit() :
                    continue
                else :
                    if options.signal == "bbH" :
                        if word == "bbH" : 
                            numbers.append(idx)
                    elif options.signal == "ggH" :
                        if word == "ggH" : 
                            numbers.append(idx)
                    else :
                        if word == "ggH" or word == "bbH" :
                            numbers.append(idx)
                    print "numbers", numbers
        if words[0] == "rate" :
            for idx in numbers :
                print "idx", idx
                signal_yield += float(words[idx])

    print signal_yield*float(options.tanb)
           
           

main()
exit(0)
