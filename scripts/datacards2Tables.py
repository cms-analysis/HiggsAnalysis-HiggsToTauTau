#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script create tables for the AN and PAS from the datacards.")
parser.add_option("-i", "--input", dest="input", default="datacards", type="string", help="Path to the complete set of datacards. [Default: datacards]")
parser.add_option("-p", "--period", dest="period", default="7TeV 8TeV", type="choice", help="Data taking period. [Default: \"7TeV, 8TeV\"]", choices=["7TeV", "8TeV", "7TeV 8TeV"])
parser.add_option("-m", "--mass", dest="mass", default="125", type="string", help="Mass for signal sample to be included in the table. [Default: 125]")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="increase verbosity. [Default: False]")
parser.add_option("--channels", dest="channels", default="mt, et, em, mm", type="string", help="Channels to produce the tables for. [Default: \"mt, et, em, mm\"]")
parser.add_option("--categories", dest="categories", default="0, 1, 2, 3, 5, 6, 7", type="string", help="Categories to produce the tables for. [Default: \"0, 1, 2, 3, 5, 6, 7\"]")
cats1 = OptionGroup(parser, "LUMI PER CHANNEL", "Luminosities per channel.")
cats1.add_option("--lumi-7TeV-mm", dest="lumi_7TeV_mm", default=4.9, type="float", help="Luminosity used for mm channel. [Default: 4.9]")
cats1.add_option("--lumi-7TeV-em", dest="lumi_7TeV_em", default=4.9, type="float", help="Luminosity used for em channel. [Default: 4.9]")
cats1.add_option("--lumi-7TeV-mt", dest="lumi_7TeV_mt", default=4.9, type="float", help="Luminosity used for mt channel. [Default: 4.9]")
cats1.add_option("--lumi-7TeV-et", dest="lumi_7TeV_et", default=4.9, type="float", help="Luminosity used for et channel. [Default: 4.9]")
cats1.add_option("--lumi-8TeV-mm", dest="lumi_8TeV_mm", default=3.0, type="float", help="Luminosity used for mm channel. [Default: 3.0]")
cats1.add_option("--lumi-8TeV-em", dest="lumi_8TeV_em", default=5.0, type="float", help="Luminosity used for em channel. [Default: 5.0]")
cats1.add_option("--lumi-8TeV-mt", dest="lumi_8TeV_mt", default=5.0, type="float", help="Luminosity used for mt channel. [Default: 5.0]")
cats1.add_option("--lumi-8TeV-et", dest="lumi_8TeV_et", default=5.0, type="float", help="Luminosity used for et channel. [Default: 5.0]")
parser.add_option_group(cats1)

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) > 0 :
    parser.print_usage()
    exit(1)


import os
import sys
import math
import linecache

from pprint import pprint
from operator import itemgetter, attrgetter
from HiggsAnalysis.HiggsToTauTau.utils import contained


def cross_section_sm (process, mass, ecms) :
    xs = 0.
    if process.find('+')>-1 :
        sub_channels = process.split('+')
        for sub_channel in sub_channels :
            xs += float(os.popen("xsec-sm {CHANNEL} {MA} {ECMS} | grep value".format(
                CHANNEL=sub_channel, MA=mass, ECMS=ecms)).read().split()[2])
    else :
        xs += float(os.popen("xsec-sm {CHANNEL} {MA} {ECMS} | grep value".format(
            CHANNEL=process, MA=mass, ECMS=ecms)).read().split()[2])
    return xs

def extractor(inputfile, period):
    lumi_mm = options.lumi_7TeV_mm if options.period == "7TeV" else options.lumi_8TeV_mm
    lumi_em = options.lumi_7TeV_em if options.period == "7TeV" else options.lumi_8TeV_em
    lumi_et = options.lumi_7TeV_et if options.period == "7TeV" else options.lumi_8TeV_et
    lumi_mt = options.lumi_7TeV_mt if options.period == "7TeV" else options.lumi_8TeV_mt
    
    file = open(inputfile)

    nomeFile = '/dev/null'
    channel = 'mt'
    category = 'NONE'

    if '_et_' in str(file):
        channel = 'et'
    if '_em_' in str(file):
        channel = 'em'
    if '_mm_' in str(file):    
        channel = 'mm'
    if '_tt_' in str(file):    
        channel = 'tt'
    if '_0_' in str(file):
        category = '0Jet_lowPt'
    if '_1_' in str(file):
        category = '0Jet_highPt'
    if '_2_' in str(file):
        category = 'Boosted_lowPt'
    if '_3_' in str(file):
        category = 'Boosted_highPt'
    if '_4_' in str(file):
        category = '2Jets'
    if '_5_' in str(file):
        category = 'VBF'
    if '_6_'in str(file):
        category = 'Btag_lowPt'
    if '_7_'in str(file):
        category = 'Btag_highPt'

    nomeFileEff = 'eff'+channel+'_'+period+'.tmp'            
    nomeFileTab = channel+'_'+category+'_'+period+'.tmp'
    
    lines = ['imax',
             'jmax',
             'kmax',
             'shapes',
             '------------------------------------------------------------------------------------------------------------------------------------',
             '-------------------------------------------------------------------------------', 
             'observation',
             'bin',
             'process',
             'rate',
    #         'lumi',
             'CMS_scale_t',
             'CMS_scale_j',
             'CMS_scale_u'
             ]


    sum = 0

    sums = {}
    rate = []
    name = []
    data = 0
    signal = []
    errSignal = {}
    first = True
    rangeSM = 5
    rangeNoB = 7
    rangeB = 4
    myRange = rangeSM
    myMaxRange = 0
    ## cross sectino for Sm and MSSM Higgs signal yield
    ## lumi in pb
    lumi = {
        "mm" : 1000*lumi_mm,
        "em" : 1000*lumi_em,
        "mt" : 1000*lumi_mt,
        "et" : 1000*lumi_et,
      }  
    xsec = {
        "ggH" : cross_section_sm("ggH", options.mass, float(options.period[:options.period.find("TeV")])),
        "qqH" : cross_section_sm("ggH", options.mass, float(options.period[:options.period.find("TeV")])),
        "VH"  : cross_section_sm("WH+ZH+ttH", options.mass, float(options.period[:options.period.find("TeV")])),
        }
    BR   = cross_section_sm("BR", options.mass, float(options.period[:options.period.find("TeV")]))

    sigmaMSSM = [0.3519*lumi[channel], 0.6481*lumi[channel]]
    BR_norm = 1

    tanbeta =10
    #BR H->TauTau TBeta_10 = 0.107
    #BR H->TauTau TBeta_20 = 0.114

    sigmaMSSM_tanb20 = [9.02*lumi[channel]*BR_norm, 14.9*lumi[channel]*BR_norm]
    sigmaMSSM_tanb10 = [2.21*lumi[channel]*BR_norm, 3.64*lumi[channel]*BR_norm]
    sigmaMSSM_tanbeta = sigmaMSSM_tanb20

    if float(tanbeta) == 10:
        sigmaMSSM_tanbeta = sigmaMSSM_tanb10

    foundProcess = False
    for line in file:
        values = line.split()
        # print values
        if values[0] == 'observation':
            data = values[1]
        if values[0]=='process' and foundProcess == False:
            foundProcess = True
            continue
            
        if len(name)==0 and values[0]=='process' and foundProcess == True:
            #Setting the lenght of the field for the bkgs
            myMaxRange = len(values)+1
            name = values[4:]
            
        if values[0]=='rate':
            rate = values[4:]
            signal = values[1:4]
            

        elif values[0] not in lines:  
            if first:        
                errSignal = dict( [ (i,0) for i in range(2, myRange)])
                sums = dict( [ (i,0) for i in range(myRange, myMaxRange)])
                first = False

            for i in range(2, myRange):
                value = values[i]
                if values[1] == 'gmN':                    
                    # it never happens for the signal to have gmN uncertainty anyway
                    continue

                try:                
                    value = float(value)
                    if value != 0:
                        value =  value - 1                    
                    errSignal[i] += value*value
                except ValueError:
                    continue        

            myNewRange = myRange
            myNewMaxRange = myMaxRange
            if values[1] == 'gmN':                
                myNewRange = myRange + 1
                myNewMaxRange = myMaxRange + 1

            #print values[0]
            for i in range(myNewRange, myNewMaxRange):
                value = values[i]

                try:
                    value = float(value)
                    if value != 0:
                        if values[1] == 'gmN':
                            value = value / math.sqrt(float(values[2]))
                        else:
                            value =  value - 1                    
                    #print value            
                    if values[1] == 'gmN':
                        #print sums[i-1]                                                
                        sums[i-1] += value*value 
                        #print sums[i-1]
                    else:
                        #print sums[i]
                        sums[i] += value*value  
                        #print sums[i]
                except ValueError:
                    continue        

            ##DEBUG
            #print values[0]
            #for myErrors in sums.values():
            #    print math.sqrt(myErrors) 

    totbkg = 0
    for i in range(0, len(rate)):
        rate[i] = float(rate[i])
        digit = round(math.log10(rate[i])) if math.log10(rate[i])>0 else -int(math.ceil(-math.log10(rate[i])))
        print rate[i], digit, round(math.log10(rate[i]))
        rate[i] = round(rate[i], 0 if round(math.log10(rate[i])) else -int(math.ceil(-math.log10(rate[i]))))
        print rate[i]
        totbkg += rate[i]

    errors = [ math.sqrt(value) for value in sums.values() ]
    errorsSignal = [ math.sqrt(value) for value in errSignal.values() ]

    totErrorSignal =0
    totSignal = 0
    for i in range(0,len(errorsSignal)):
        errorsSignal[i] = errorsSignal[i]*float(signal[i])
        totErrorSignal = totErrorSignal+errorsSignal[i]
        totSignal = totSignal + float(signal[i])
        
    totErrorSignal = totErrorSignal / totSignal

    value0 = float(signal[0]) / float(xsec["ggH"]*BR*lumi[channel])
    value1 = float(signal[1]) / float(xsec["qqH"]*BR*lumi[channel])
    value2 = float(signal[2]) / float(xsec["VH" ]*BR*lumi[channel])

    effFile = open(nomeFileEff,'a')
    effFile.write("\n *** "+str(channel)+str(category)+"\n")
    effFile.write("ggH: %.2e \n" %value0)
    effFile.write("VBFH: %.2e \n" %value1)
    effFile.write("VH: %.2e \n" %value2)
    effFile.close()

    for i in range(0, len(errors)):
        errors[i]=errors[i]*rate[i]
        if errors[i] > 100:
            errors[i] = round(errors[i]) 

    totalError =0
    for i in range(0, len(errors)):

        totalError =totalError + (errors[i])*(errors[i])
    totalError = math.sqrt(totalError)

    if '_0.txt' in str(file):
        name.pop(3)
        name[3] = 'ZLL'
        rate[4] += rate[3]
        rate.pop(3)
        errors[4] = math.sqrt(errors[4]*errors[4]+ errors[3]*errors[3])
        errors.pop(3)

    tabFile = open(nomeFileTab,'w') 

    for na, ra, err in zip( name, rate, errors ):
        digit = int(math.log10(float(ra)))
        tabFile.write('%s & %d \pm %d &\n' % ( na, round(float(ra)), round(float(err))))
    tabFile.write('Total Bkg & %d \\pm %d\n' %(round(totbkg), round(totalError)))
    tabFile.write('Signal & %d \pm %d &\n' %(totSignal,totErrorSignal*totSignal))
    tabFile.write('Data & %d & \n'%float(data))
    tabFile.close()
    return 0

def getLine(file, n, m=-1):
    #print "get line from file:", file
    line = linecache.getline(file,n)
    line1 = 'dummy 0'
    if m != -1:
        line1 = linecache.getline(file,m)
    values = line.split()
    values1 = line1.split()

    myValue = float(values[1])+ float(values1[1])
    myValue = '%.1e' % myValue
    myValue_ab = myValue.split('e')
    myValue_a = '%s' % myValue_ab[1]
    myValue_after = myValue_a[2]
    myValue_toBeReturn = [myValue_ab[0],myValue_after]
    return myValue_toBeReturn

def mergingCategories(channel, category, period):
    file1 = channel+'_'+category+'_lowPt_'+period+'.tmp'
    file2 = channel+'_'+category+'_highPt_'+period+'.tmp'
    newfile = channel+'_'+category+'_'+period+'.tmp'
    
    samples = []
    events1 = []
    events2 = []
    errors1 = []
    errors2 = []
    total1 = 0
    errTot1 = 0
    total2 = 0 
    errTot2 = 0
    data1 = 0
    data2 = 0
    myfile = open(file1)
    for line in myfile:
        values = line.split()
        if values[0] == 'Total':
            samples.append('Total Bkg')
            events1.append(float(values[3]))
            errors1.append(float(values[5]))
        if values[0] != 'Data' and values[0] != 'Total':
            samples.append(values[0])
            events1.append(float(values[2]))
            errors1.append(float(values[4]))
        if values[0] == 'Data':
            data1 = float(values[2])

    myfile = open(file2)
    for line in myfile:
        values = line.split()
        if values[0] == 'Total':
            events2.append(float(values[3]))
            errors2.append(float(values[5]))
        if values[0] != 'Data' and values[0] != 'Total':
            events2.append(float(values[2]))
            errors2.append(float(values[4]))
        if values[0] == 'Data':
            data2 = float(values[2])

    myfile = open(newfile,'a')
    for i in range(len(samples)):
        myfile.write('%s & %d \pm %d \n' %(samples[i],events1[i]+events2[i],math.sqrt(errors1[i]*errors1[i]+errors2[i]*errors2[i])))
    myfile.write('Data & %d &\n'%(data1+data2))
        
def mergingPeriods(channel, cat, compressed=True):
    if compressed :
        if cat == "1" or cat == "3" or cat=="7" :
            return
        catlabels = {
            "0" : '0Jet',
            "2" : 'Boosted',
            "5" : 'VBF',
            "6" : 'Btag',
            }
    else :
        catlabels = {
            "0" : '0Jet_lowPt',
            "1" : '0Jet_highPt',
            "2" : 'Boosted_low_Pt',
            "3" : 'Boosted_highPt',
            "5" : 'VBF',
            "6" : 'Btag_lowPt',
            "7" : 'Btag_highPt',
            }
    file1 = channel+'_'+catlabels[cat]+'_7TeV.tmp'
    file2 = channel+'_'+catlabels[cat]+'_8TeV.tmp'
    newfile = channel+'_'+catlabels[cat]+'_7+8TeV.tmp'
    #print "writing file: ", newfile
    
    samples = []
    events1 = []
    events2 = []
    errors1 = []
    errors2 = []
    total1 = 0
    errTot1 = 0
    total2 = 0 
    errTot2 = 0
    data1 = 0
    data2 = 0
    myfile = open(file1)
    for line in myfile:
        values = line.split()
        if values[0] == 'Total':
            samples.append('Total Bkg')
            events1.append(float(values[3]))
            errors1.append(float(values[5]))
        if values[0] != 'Data' and values[0] != 'Total':
            samples.append(values[0])
            events1.append(float(values[2]))
            errors1.append(float(values[4]))
        if values[0] == 'Data':
            data1 = float(values[2])

    myfile = open(file2)
    for line in myfile:
        values = line.split()
        if values[0] == 'Total':
            events2.append(float(values[3]))
            errors2.append(float(values[5]))
        if values[0] != 'Data' and values[0] != 'Total':
            events2.append(float(values[2]))
            errors2.append(float(values[4]))
        if values[0] == 'Data':
            data2 = float(values[2])

    myfile = open(newfile,'a')
    for i in range(len(samples)):
        myfile.write('%s & %d \pm %d \n' %(samples[i],events1[i]+events2[i],math.sqrt(errors1[i]*errors1[i]+errors2[i]*errors2[i])))
    myfile.write('Data & %d &\n'%(data1+data2))
 

def mergingEfficiencies() :
    """
    this is to merge the efficiencies
    """
    print "not yet implemented"
    

def chooseCategory(samples, myList, cat='0Jet_lowPt'):
    myNN = {}
    addZLL = False
    for i in range(len(myList)):
        if myList[i][0] == cat:
            if myList[i][1] == "ZJ" or myList[i][1] == "ZL" :
                addZLL=True
            #print "append value for sample:", myList[i][1], "category:", myList[i][0], "value:", myList[i][2] 
            myNN[myList[i][1]] = myList[i][2]
    if addZLL :
        ## add ZL and ZJ for mt and et
        myNN["ZLL"] = str(float(myNN['ZL'])+float(myNN['ZJ']))
    return myNN 

def blankColumn(number_of_samples) :
    i=0
    myNN = []
    for i in range(number_of_samples):
        myNN.append("-")
        i=i+1                
    return myNN

def makingTables(channel, period, combine_categories=True):
    
    if not combine_categories:
        cat = ['0Jet_lowPt','0Jet_highPt','Boosted_lowPt','Boosted_highPt','VBF','Btag_lowPt','Btag_highPt']
    else:
        cat = ['0Jet','Boosted','VBF','Btag']

    firstCat = cat[0]
    samples = []

    rate = []
    error = []
    total = []
    errTot = []
    
    signal = []
    errsignal = []
    
    data = []
    
    texFile = channel+'-'+period+'.tex'
    output = open(texFile,'w')

    if not combine_categories :
        output.write("""
\\begin{tabular}{|l|r@{$ \,\,\pm\,\, $}l|r@{$\,\,\pm\,\,$}l|r@{$\,\,\pm\,\,$}l|r@{$\,\,\pm\,\,$}l|r@{$\,\,\pm\,\,$}l|r@{$\,\,\pm\,\,$}l|r@{$\,\,\pm\,\,$}l|}
%\cline{2-11}
%\multicolumn{1}{c|}{ } &  \multicolumn{10}{c|}{SM} & \multicolumn{4}{c|}{MSSM} \\
\\hline
Process & \multicolumn{2}{c|}{\emph{0-Jet} (low)} & \multicolumn{2}{c|}{\emph{0-Jet} (high)}  & \multicolumn{2}{c|}{\emph{Boosted} (low)} &  \multicolumn{2}{c|}{\emph{Boosted} (high)} & \multicolumn{2}{c|}{\emph{VBF}} \\\\
\\hline
""")
#        output.write("""
#\\begin{tabular}{|l|r@{$ \,\,\pm\,\, $}l|r@{$\,\,\pm\,\,$}l|r@{$\,\,\pm\,\,$}l|r@{$\,\,\pm\,\,$}l|r@{$\,\,\pm\,\,$}l|r@{$\,\,\pm\,\,$}l|r@{$\,\,\pm\,\,$}l|}
#%\cline{2-15}
#%\multicolumn{1}{c|}{ } &  \multicolumn{10}{c|}{SM} & \multicolumn{4}{c|}{MSSM} \\
#\\hline
#Process & \multicolumn{2}{c|}{\emph{0-Jet} (low)} & \multicolumn{2}{c|}{\emph{0-Jet} (high)}  & \multicolumn{2}{c|}{\emph{Boosted} (low)} &  \multicolumn{2}{c|}{\emph{Boosted} (high)} & \multicolumn{2}{c|}{\emph{VBF}} &  \multicolumn{2}{c|}{\emph{$b$-Tag} (low)} & \multicolumn{2}{c|}{\emph{$b$-Tag} (high)} \\\\
#\\hline
#""")        
    else:
        output.write("""
\\begin{tabular}{|l|r@{$ \,\,\pm\,\, $}l|r@{$\,\,\pm\,\,$}l|r@{$\,\,\pm\,\,$}l|r@{$\,\,\pm\,\,$}l|}
%\cline{2-7}
%\multicolumn{1}{c|}{ } &  \multicolumn{6}{c|}{SM}  & \multicolumn{2}{c|}{MSSM} \\
\\hline
Process & \multicolumn{2}{c|}{\emph{0-Jet}} & \multicolumn{2}{c|}{\emph{Boosted}} & \multicolumn{2}{c|}{\emph{VBF}} \\\\
\\hline
""")
#        output.write("""
#\\begin{tabular}{|l|r@{$ \,\,\pm\,\, $}l|r@{$\,\,\pm\,\,$}l|r@{$\,\,\pm\,\,$}l|r@{$\,\,\pm\,\,$}l|}
#%\cline{2-9}
#%\multicolumn{1}{c|}{ } &  \multicolumn{6}{c|}{SM}  & \multicolumn{2}{c|}{MSSM} \\
#\\hline
#Process & \multicolumn{2}{c|}{\emph{0-Jet}} & \multicolumn{2}{c|}{\emph{Boosted}} & \multicolumn{2}{c|}{\emph{VBF}} &  \multicolumn{2}{c|}{\emph{$b$-Tag}} \\\\
#\\hline
#""")            

    for category in cat:
        myfile = str(channel)+'_'+str(category)+'_'+period+'.tmp'
        file = open(myfile)    
        for line in file:
            values = line.split()
            #print values
            if category == firstCat and values[0] != 'Data' and values[0] != 'Total' and values[0] != 'Signal':
                samples.append(values[0])
            if values[0] == 'Data':
                data.append(values[2])            
            if values[0] == 'Signal':
                signal.append(values[2])
                errsignal.append(values[4])                
            elif values[0] == 'Total':                
                total.append(values[3])
                errTot.append(values[5])   

            if values[0] != 'Data' and values[0] != 'Total' and values[0] != 'Signal':
                rate.append((category,values[0],values[2]))
                error.append((category,values[0],values[4]))
    
    rateCat =[]
    errorCat = []
    totCat = []
    errTotCat =[]                
    for category in cat:
        rateCat.append(chooseCategory(samples, rate,category))
        errorCat.append(chooseCategory(samples, error,category))

    for i in range(0, len(samples)):
        if samples[i] == 'VV' or samples[i] == 'EWK' :
            samples[i] = 'Dibosons'
        if samples[i] == 'TT' or samples[i] == 'ttbar' or samples[i] == 'TTJ' :
            samples[i] = 't$\\bar{\\rm{t}}$'        
        if samples[i] == 'QCD' or samples[i] == 'Fakes' :
            samples[i] = 'Multijets/Fakes'
        if samples[i] == 'W' or samples[i] == 'WJets' :
            samples[i] = 'W+jets'
        if samples[i] == 'ZLL':
            samples[i] = 'Z$\\rightarrow ll$'
        if samples[i] == 'ZL':
            samples[i] = 'Z lep. fakes $\\tau_{h}$'
        if samples[i] == 'ZJ':
            samples[i] = 'Z jet fakes $\\tau_{h}$'
        if samples[i] == 'ZTT' or samples[i] == 'Ztt' :
            samples[i] = 'Z$\\rightarrow \\tau\\tau$'
        if samples[i] == 'ZMM' :
            samples[i] = 'Z$\\rightarrow \\mu\\mu$'               

    order = {
        "mt" : ["ZTT", "QCD", "W", "ZLL", "TT", "VV"],
        "et" : ["ZTT", "QCD", "W", "ZLL", "TT", "VV"],
        "mm" : ["ZTT", "QCD", "WJets", "ZMM", "TTJ", "Dibosons"],
        "em" : ["Ztt", "Fakes", "ttbar", "EWK"],
        }
    sample_name = {
        "ZTT" : 'Z$\\rightarrow \\tau\\tau$',
        "Ztt" : 'Z$\\rightarrow \\tau\\tau$',
        "QCD" : 'QCD',
        "Fakes" : 'QCD',
        "W" : 'W+jets',
        "WJets" : 'W+jets',
        "ZLL" : 'Z+jets (l/jet faking $\\tau$)',
        "ZMM" : 'Z$\\rightarrow \\mu\\mu$',
        "TT" : 't$\\bar{\\rm{t}}$',
        "ttbar" : 't$\\bar{\\rm{t}}$',
        "TTJ" : 't$\\bar{\\rm{t}}$',
        "EWK" : 'Dibosons',
        "VV" : 'Dibosons',
        "Dibosons" : 'Dibosons',
        }

    for i in order[channel] :
        if not combine_categories:
            output.write('%s & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s \\\\\n' %(sample_name[i], rateCat[0][i], errorCat[0][i],rateCat[1][i], errorCat[1][i],rateCat[2][i], errorCat[2][i],rateCat[3][i], errorCat[3][i],rateCat[4][i], errorCat[4][i]))
            #output.write('%s & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s\\\\\n' %(sample_name[i], rateCat[0][i], errorCat[0][i],rateCat[1][i], errorCat[1][i],rateCat[2][i], errorCat[2][i],rateCat[3][i], errorCat[3][i],rateCat[4][i], errorCat[4][i],rateCat[5][i], errorCat[5][i],rateCat[6][i], errorCat[6][i]))
        if combine_categories:
            output.write('%s & %s & %s & %s & %s & %s & %s \\\\\n' %(sample_name[i], rateCat[0][i], errorCat[0][i],rateCat[1][i], errorCat[1][i],rateCat[2][i], errorCat[2][i]))
            #output.write('%s & %s & %s & %s & %s & %s & %s & %s & %s\\\\\n' %(sample_name[i], rateCat[0][i], errorCat[0][i],rateCat[1][i], errorCat[1][i],rateCat[2][i], errorCat[2][i],rateCat[3][i], errorCat[3][i]))

    output.write('\\hline\n')
    output.write('\\hline\n')

    if not combine_categories:
        output.write('Total Background & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s \\\\\n' %(total[0], errTot[0],total[1], errTot[1],total[2], errTot[2],total[3], errTot[3],total[4], errTot[4]))
        #output.write('Total Background & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s \\\\\n' %(total[0], errTot[0],total[1], errTot[1],total[2], errTot[2],total[3], errTot[3],total[4], errTot[4],total[5], errTot[5],total[6], errTot[6]))
        output.write('\\hline\n')
        output.write('H$\\rightarrow\\tau\\tau$ & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s \\\\\n' %(signal[0], errsignal[0],signal[1], errsignal[1],signal[2], errsignal[2],signal[3], errsignal[3],signal[4], errsignal[4]))
        #output.write('H$\\rightarrow\\tau\\tau$ & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s & %s \\\\\n' %(signal[0], errsignal[0],signal[1], errsignal[1],signal[2], errsignal[2],signal[3], errsignal[3],signal[4], errsignal[4],signal[5], errsignal[5],signal[6], errsignal[6]))
        output.write('\\hline\n')
        output.write('Data & \multicolumn{2}{|c|}{%s} &\multicolumn{2}{|c|}{%s} &\multicolumn{2}{|c|}{%s} &\multicolumn{2}{|c|}{%s} &\multicolumn{2}{|c|}{%s} &\multicolumn{2}{|c|}{%s} \\\\\n' %(data[0],data[1],data[2],data[3],data[4],data[5]))
        #output.write('Data & \multicolumn{2}{|c|}{%s} &\multicolumn{2}{|c|}{%s} &\multicolumn{2}{|c|}{%s} &\multicolumn{2}{|c|}{%s} &\multicolumn{2}{|c|}{%s} &\multicolumn{2}{|c|}{%s} &\multicolumn{2}{|c|}{%s} \\\\\n' %(data[0],data[1],data[2],data[3],data[4],data[5],data[6]))
    else:
        output.write('Total Background & %s & %s & %s & %s & %s & %s \\\\\n' %(total[0], errTot[0],total[1], errTot[1],total[2], errTot[2]))
        #output.write('Total Background & %s & %s & %s & %s & %s & %s & %s & %s\\\\\n' %(total[0], errTot[0],total[1], errTot[1],total[2], errTot[2],total[3], errTot[3]))
        output.write('\\hline\n')
        output.write('H$\\rightarrow\\tau\\tau$ & %s & %s & %s & %s & %s & %s \\\\\n' %(signal[0], errsignal[0],signal[1], errsignal[1],signal[2], errsignal[2]))
        #output.write('H$\\rightarrow\\tau\\tau$ & %s & %s & %s & %s & %s & %s & %s & %s \\\\\n' %(signal[0], errsignal[0],signal[1], errsignal[1],signal[2], errsignal[2],signal[3], errsignal[3]))
                                                                                         
        output.write('\\hline\n')   
        output.write('Data & \multicolumn{2}{|c|}{%s} &\multicolumn{2}{|c|}{%s} &\multicolumn{2}{|c|}{%s} \\\\\n' %(data[0],data[1],data[2]))
        #output.write('Data & \multicolumn{2}{|c|}{%s} &\multicolumn{2}{|c|}{%s} &\multicolumn{2}{|c|}{%s} &\multicolumn{2}{|c|}{%s} \\\\\n' %(data[0],data[1],data[2],data[3]))
    output.write('\\hline\n')
    
    #AND NOW FOR THE efficiencies!!!!
        
    efffile = 'eff'+channel+'_7TeV.tmp'
  
    if combine_categories:
        output.write('\\multicolumn{7}{c}{ } \\\\\n')
        output.write('\\multicolumn{2}{l}{Signal Eff.} &  \\multicolumn{5}{c}{ } \\\\\n')
        output.write('\\hline\n')
    
        value1 = getLine(efffile,3,8)
        value2 = getLine(efffile,13)
        value3 = getLine(efffile,18,23)
        value4 = getLine(efffile,28)

        output.write('gg$\\rightarrow$ H &   \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &  \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &  \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$}  \\\\\n' %(value1[0],value1[1],value2[0],value2[1],value3[0],value3[1]))
        #output.write('gg$\\rightarrow$ H &   \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &  \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &  \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} & \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$}  \\\\\n' %(value1[0],value1[1],value2[0],value2[1],value3[0],value3[1],value4[0],value4[1]))
    
        value1 = getLine(efffile,4,9)
        value2 = getLine(efffile,14)
        value3 = getLine(efffile,19,24)
        value4 = getLine(efffile,29)
      
        output.write('qq$\\rightarrow$ qqH &     \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &  \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &  \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} \\\\\n' %(value1[0],value1[1],value2[0],value2[1],value3[0],value3[1]))
        #output.write('qq$\\rightarrow$ qqH &     \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &  \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &  \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &    \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$}  \\\\\n' %(value1[0],value1[1],value2[0],value2[1],value3[0],value3[1],value4[0],value4[1]))
    
        value1 = getLine(efffile,5,10)
        value2 = getLine(efffile,15)
        value3 = getLine(efffile,20,25)
        value4 = getLine(efffile,30)

        output.write('qq$\\rightarrow$ Ht$\overline{\\rm{t}}$ or VH&   \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &  \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &  \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} \\\\\n' %(value1[0],value1[1],value2[0],value2[1],value3[0],value3[1]))
        #output.write('qq$\\rightarrow$ Ht$\overline{\\rm{t}}$ or VH&   \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &  \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &  \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &    \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$}  \\\\\n' %(value1[0],value1[1],value2[0],value2[1],value3[0],value3[1],value4[0],value4[1]))
        '''
        value1 = getLine(efffile,23)
        value2 = getLine(efffile,18)
        output.write('gg$\\rightarrow \\phi$ &  \multicolumn{2}{|c|}{-} &     \multicolumn{2}{|c|}{-} &     \multicolumn{2}{|c|}{-} & \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} & \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$}      \\\\\n' %(value1[0],value1[1], value2[0], value2[1]))
        value1 = getLine(efffile,22)
        value2 = getLine(efffile,19)
        output.write('gg$\\rightarrow$ bb$\\phi$ &  \multicolumn{2}{|c|}{-} &     \multicolumn{2}{|c|}{-} &     \multicolumn{2}{|c|}{-} & \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} & \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$}      \\\\\n' %(value1[0],value1[1],value2[0],value2[1]))

        '''
        output.write("""\\hline
\end{tabular}
\label{tab:cutflow-%s-%s}
\end{center}
\end{table*}
""" % (channel, "7+8TeV" if "7TeV" in options.period and "8TeV" in options.period else option.period))
        
    if not combine_categories:
        output.write('\\multicolumn{6}{c}{ } \\\\\n')
        output.write('\\multicolumn{2}{l}{Signal Eff.} &  \\multicolumn{4}{c}{ } \\\\\n')
        output.write('\\hline\n')
    
        value1 = getLine(efffile,3)
        value2 = getLine(efffile,8)
        value3 = getLine(efffile,13)
        value4 = getLine(efffile,18)
        value5 = getLine(efffile,23)
        value6 = getLine(efffile,28)
        value7 = getLine(efffile,33)

        output.write('gg$\\rightarrow$ H &   \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &  \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &  \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &    \\multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &     \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$}    &     \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &     \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$}    \\\\\n' %(value1[0],value1[1],value2[0],value2[1],value3[0],value3[1],value4[0],value4[1],value5[0],value5[1],value6[0],value6[1],value7[0],value7[1]))
    
        value1 = getLine(efffile,4)
        value2 = getLine(efffile,9)
        value3 = getLine(efffile,14)
        value4 = getLine(efffile,19)
        value5 = getLine(efffile,24)
        value6 = getLine(efffile,29)
        value7 = getLine(efffile,34)

        output.write('qq$\\rightarrow$ qqH &     \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &  \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &  \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &    \\multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &     \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$}    &     \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &     \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &     \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$}   \\\\\n' %(value1[0],value1[1],value2[0],value2[1],value3[0],value3[1],value4[0],value4[1],value5[0],value5[1],value6[0],value6[1],value7[0],value7[1]))

    
        value1 = getLine(efffile,5)
        value2 = getLine(efffile,10)
        value3 = getLine(efffile,15)
        value4 = getLine(efffile,20)
        value5 = getLine(efffile,25)
        value6 = getLine(efffile,30)
        value7 = getLine(efffile,35)

        output.write('qq$\\rightarrow$ Ht$\overline{\\rm{t}}$ or VH&   \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &  \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &  \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &    \\multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &     \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$}    &     \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} &     \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$}   \\\\\n' %(value1[0],value1[1],value2[0],value2[1],value3[0],value3[1],value4[0],value4[1],value5[0],value5[1],value6[0],value6[1],value7[0],value7[1]))
        '''
        value1 = getLine(efffile,23)
        value2 = getLine(efffile,18)
        output.write('gg$\\rightarrow \\phi$ &  \multicolumn{2}{|c|}{-} &     \multicolumn{2}{|c|}{-} &     \multicolumn{2}{|c|}{-} & \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} & \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$}      \\\\\n' %(value1[0],value1[1], value2[0], value2[1]))
        value1 = getLine(efffile,22)
        value2 = getLine(efffile,19)
        output.write('gg$\\rightarrow$ bb$\\phi$ &  \multicolumn{2}{|c|}{-} &     \multicolumn{2}{|c|}{-} &     \multicolumn{2}{|c|}{-} & \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$} & \multicolumn{2}{|c|}{%s$\cdot$10$^{-%s}$}      \\\\\n' %(value1[0],value1[1],value2[0],value2[1]))

        '''
        output.write('\\hline\n')
        output.write("""\\hline
\end{tabular}
\label{tab:cutflow-{CHANNEL}}
\end{center}
\end{table*}
""".format(CHANNEL=channel))



## channels
channels = options.channels.split()
for idx in range(len(channels)) : channels[idx] = channels[idx].rstrip(',')## channels
## categories
categories = options.categories.split()
for idx in range(len(categories)) : categories[idx] = categories[idx].rstrip(',')
## periods
periods = options.period.split()
for idx in range(len(periods)) : periods[idx] = periods[idx].rstrip(',')


os.system("rm -f *.tmp")
for chn in channels :
    for per in periods :
        for cat in categories :
            filename = options.input+"/htt_"+chn+"_"+cat+"_"+per+"-"+options.mass+".txt"
            extractor(filename, per)

        if contained("0", categories) and contained("1", categories):
            mergingCategories(chn,'0Jet',per)
        if contained("1", categories) and contained("2", categories):
            mergingCategories(chn,'Boosted',per)
        if contained("6", categories) and contained("7", categories):
            mergingCategories(chn,'Btag',per)
    if contained("7TeV", periods) and contained("8TeV", periods) :
        for cat in categories :
            mergingPeriods(chn, cat)
        makingTables(chn, "7+8TeV", True)
    else :
        for per in periods :
            makingTables(chn, per, True)
os.system("rm *.tmp")
