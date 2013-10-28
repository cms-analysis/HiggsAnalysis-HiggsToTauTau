#
# Execute from HiggsAnalysis/HiggsToTauTau/test
# 
# PyROOT Style macro for S/B plot
# Last update : 26 Sep 2013
#
# Instructions
#
# - Run the following commands to generate root files containing the postfit histograms:
#   -- python produce_macros.py  -a sm -c 'tt' -u 1 -p "8TeV"
#   -- python run_macros.py  -a sm -c 'mt, et, em'  -p "7TeV 8TeV"
#
# - Run this macro by python sobWeightedCombineAll.py
#   --it relies on another macro sobWeightedCombine.py being at the same PATH
#

sep_line = '-'*70
fmt = '%-20s %-4s %-10s'

import sys
from optparse import OptionParser, OptionGroup
import ConfigParser
from sobWeightedCombine import *
from ROOT import gROOT

def sobCombine(Plotname, # TauTau_MSSM
               ListOfHistogram, # TauTau_MSSM
               Datasetname, # CMS Preliminary,  H#rightarrow#tau#tau,  4.9 fb^{-1} at 7 TeV, 19.8 fb^{-1} at 8 TeV"
               Channelname, # #tau_{h}#tau_{h}
               Categoryname, # 
               Weight,
               muValue,
               Mode,
               unblind,
               Log=False,
               Mass=125,
               Tanb=0):

    # ListOfHistogram : array of input postfit root files 
    # Plotname : name for this plot
    # Wieghts : option to apply or not apply weights

    print 'S/B combine:'
    print sep_line
    print fmt % ('Plotname', ':', Plotname)
    print fmt % ('Datasetname', ':', Datasetname)
    print fmt % ('Channelname', ':', Channelname)
    print fmt % ('Categoryname', ':', Categoryname)
    print fmt % ('Weight', ':', Weight)
    print fmt % ('mu-Value', ':', muValue)
    print fmt % ('Plot mode', ':', Mode)
    print fmt % ('Log-scale', ':', Log)
    print fmt % ('Mass', ':', Mass)
    print fmt % ('Blind', ':', unblind)
    print fmt % ('tan-beta', ':', Tanb)
    print fmt % ('# of files', ':', len(ListOfHistogram))
    print

    
    
    if Mode=='Mtt':
        sobWeightedCombine(ListOfHistogram, Plotname, Weight, float(muValue))
        sobWeightedPlot(Plotname, str(Datasetname), str(Channelname), str(Categoryname), Log, Mass, Tanb, unblind)
    elif Mode=='SOB':
        sobInputs(ListOfHistogram, Plotname + 'SOB', float(muValue))
        sobWeightedPlot(Plotname + 'SOB', str(Datasetname), str(Channelname), str(Categoryname), True, Mass, Tanb, True)
    elif Mode=='SigMtt':
        bbbsobWeightedCombine(ListOfHistogram, Plotname + 'SigMtt', Weight, float(muValue))
        sobWeightedPlot(Plotname + 'SigMtt', str(Datasetname), str(Channelname), str(Categoryname), Log, Mass, Tanb)
    else:
        print 'Choose the mode from Mtt, SOB'

def main():

    parser = OptionParser(usage='usage: %prog [options] ARGs',
                          description='S/B plot macro')
    parser.add_option('-c', '--channel', dest='channel', default='mt et tt em', action='store',
                      help='channels to be considered for the plot. Default : mt et tt em ee mm mt_soft vhtt')

    parser.add_option('-p', '--period', dest='period', default='7TeV 8TeV', action='store',
                      help='period used for the S/B plots. Default : 7TeV 8TeV')

    parser.add_option('-g', '--category', dest='category', default='0jet 1jet vbf', action='store',
                      help='categories used for the S/B plots. Default : 0jet 1jet vbf')

    parser.add_option('-m', '--mode', dest='mode', default='Mtt', action='store',
                      help='Plot mode. You can choose Mtt, SOB, SigMtt Default : Mtt')

    parser.add_option("-b", "--batch", dest='batch', action="store_true", default=True,
                      help='Set Batch mode. Default : False')

    parser.add_option("-u", "--unblind", dest='unblind', action="store_true", default=False,
                      help='Use this option when unblinding. Default : False')

    (options, args) = parser.parse_args()


    if(options.batch==True):
        gROOT.SetBatch(True)

    init = ConfigParser.SafeConfigParser()
    init.read('./config.ini')

    dict = {}
    list_all = []


    for ichn in options.channel.split():

        list = []
        
        for icat in options.category.split():
            for iperiod in options.period.split():
                list.extend(init.get(ichn, icat+'_'+iperiod).split())

        dict[ichn] = list
        list_all.extend(list)

    print
    print fmt % ('Total # of files', ':', len(list_all))

#    categoryname = 'All_category'
    categoryname = ''
    if options.category != '0jet 1jet vbf':
        categoryname = options.category

    # Individual channel
    for ichn in options.channel.split():
        pname = ichn + '_SM'

#        sobCombine(pname, dict[ichn], init.get('naming', 'caption'), init.get('naming',ichn), categoryname, 1, init.get('muvalue',ichn), options.mode)
        sobCombine(pname, dict[ichn], init.get('naming', 'caption'), init.get('naming',ichn), categoryname, 1, init.get('muvalue',ichn), options.mode, options.unblind)


    # Combine
    sobCombine('All_SM', list_all, init.get('naming', 'caption'), init.get('naming','all'), categoryname, 1, init.get('muvalue','all'), options.mode, options.unblind)






if __name__ == '__main__':
    main()


