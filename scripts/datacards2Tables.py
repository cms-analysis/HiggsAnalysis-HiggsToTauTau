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
parser.add_option("--categories", dest="categories", default="0, 1, 2, 3, 5", type="string", help="Categories to produce the tables for. [Default: \"0, 1, 2, 3, 5\"]")
cats1 = OptionGroup(parser, "LUMI PER CHANNEL", "Luminosities per channel.")
cats1.add_option("--lumi-7TeV-mm", dest="lumi_7TeV_mm", default= 4.9, type="float", help="Luminosity used for mm channel. [Default:  4.9]")
cats1.add_option("--lumi-7TeV-em", dest="lumi_7TeV_em", default= 4.9, type="float", help="Luminosity used for em channel. [Default:  4.9]")
cats1.add_option("--lumi-7TeV-mt", dest="lumi_7TeV_mt", default= 4.9, type="float", help="Luminosity used for mt channel. [Default:  4.9]")
cats1.add_option("--lumi-7TeV-et", dest="lumi_7TeV_et", default= 4.9, type="float", help="Luminosity used for et channel. [Default:  4.9]")
cats1.add_option("--lumi-8TeV-mm", dest="lumi_8TeV_mm", default=12.0, type="float", help="Luminosity used for mm channel. [Default: 12.0]")
cats1.add_option("--lumi-8TeV-em", dest="lumi_8TeV_em", default=12.0, type="float", help="Luminosity used for em channel. [Default: 12.0]")
cats1.add_option("--lumi-8TeV-mt", dest="lumi_8TeV_mt", default=12.0, type="float", help="Luminosity used for mt channel. [Default: 12.0]")
cats1.add_option("--lumi-8TeV-et", dest="lumi_8TeV_et", default=12.0, type="float", help="Luminosity used for et channel. [Default: 12.0]")
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


def cross_section_sm (process, mass, ecms) :
    """
    Determine the SM cross section for given process, higgs boson mass and center of mass energy.
    """
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
   otherwise add in quadratire to undert(correlated). At the end add the two uncerts linear and
   all uncerts in quasradture. 
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
    #print path
    ## determine luminosity per channel
    lumi = {}
    if period == "7TeV" :
        lumi = {
            ## in /pb
            "tt" : 1000*options.lumi_7TeV_mm,
            "mm" : 1000*options.lumi_7TeV_mm,
            "em" : 1000*options.lumi_7TeV_em,
            "mt" : 1000*options.lumi_7TeV_mt,
            "et" : 1000*options.lumi_7TeV_et,
            }  
    if period == "8TeV" :
        lumi = {
            ## in /pb
            "tt" : 1000*options.lumi_8TeV_mm,
            "mm" : 1000*options.lumi_8TeV_mm,
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
    if '_tt_' in path:
        channel = 'tt'        
    ## determine event category from path
    category = 'NONE'        
    if '_0_' in  path:
        category = 'boost' if channel == 'tt' else '0jet_low'
    if '_1_' in  path:
        category = 'vbf' if channel == 'tt' else '0jet_high'
    if '_2_' in  path:
        category = 'boost_low'
    if '_3_' in  path:
        category = 'boost_high'
    if '_4_' in  path:
        category = '2jets'
    if '_5_' in  path:
        category = 'vbf'
    if '_6_' in  path:
        category = 'btag_low'
    if '_7_' in  path:
        category = 'btag_high'

    ## determine cross section for SM Higgs (in pb)
    xsec = {
        "ggH" : cross_section_sm("ggH"      , options.mass, float(period[:period.find("TeV")])),
        "qqH" : cross_section_sm("qqH"      , options.mass, float(period[:period.find("TeV")])),
        "VH"  : cross_section_sm("WH+ZH+ttH", options.mass, float(period[:period.find("TeV")])),
        }
    ## determine BR for SM Higgs signal
    BR = cross_section_sm("BR", options.mass, float(period[:period.find("TeV")]))

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
        'CMS_scale_u'
        ]
    ## largest index for signal samples (used for split up of uncertainties for signal
    ## and background) 
    range_sig = -1
    ## largest index for background samples (used for split up of uncertainties for
    ## signal and background)
    range_bkg = -1

    file = open(path)
    ## loop datacard and extract all necessary inputs
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
                    if values[idx].isdigit() and int(values[idx]) == 0 :
                        range_sig = idx+1
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
    
    ## sum up total signal rate
    rate_sig_summed = 0
    for i in range(0, len(rate_sig)):
        rate_sig[i] = float(rate_sig[i])
        rate_sig_summed += rate_sig[i]
    ## sum up uncertainty of total signal rate
    uncert_sig_split = []
    uncert_sig_summed = 0
    for i in range(0, len(rate_sig)):
        uncert_sig_split.append(math.sqrt(uncert_sig[2+i])*rate_sig[i])
        uncert_sig_summed+=uncert_sig_split[i]*uncert_sig_split[i]
    uncert_sig_summed = math.sqrt(uncert_sig_summed)
    
    ## sum up total background rate
    rate_bkg_summed = 0
    for i in range(0, len(rate_bkg)):
        rate_bkg[i] = float(rate_bkg[i])
        rate_bkg[i] = round(rate_bkg[i], 0 if round(math.log10(rate_bkg[i]))>0 else -int(math.ceil(-math.log10(rate_bkg[i])))+1)
        rate_bkg_summed += rate_bkg[i]
    ## sum up uncertainty of total background rate
    uncert_bkg_split = []
    uncert_bkg_summed = 0

    for i in range(0, len(rate_bkg)):
        uncert_bkg_split.append(math.sqrt(uncert_bkg[range_sig+1+i])*rate_bkg[i])
        uncert_bkg_summed+=uncert_bkg_split[i]*uncert_bkg_split[i]        
    uncert_bkg_summed = math.sqrt(uncert_bkg_summed)

    ## write tmp results to file, identified by channel, category and period
    yields = open(channel+'_'+category+'_'+period+'.tmp', 'w')
    for name, rate, uncert in zip(names_bkg, rate_bkg, uncert_bkg_split):
        yields.write(formated_line(name, rate, uncert))
    yields.write(formated_line('Total' , rate_bkg_summed, uncert_bkg_summed))
    yields.write(formated_line('Signal', rate_sig_summed, uncert_sig_summed))
    yields.write('Data \t %d \n' % int(observed))
    yields.close()

    efficiencies = open('eff_'+channel+'_'+period+'.tmp','a')
    efficiencies.write(channel+'_'+category+"\n")
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
    for i in range(len(lines[periods[0]])) :
        line = lines[periods[0]][i]
        if len(line) == 1 :
            file.write(line[0]+'\n')
        else :
            line_summed = []
            for per in periods :
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
    for line in file :
        values = line.split()
        if len(values) == 1 :
            subset = values[0]
        else :
            for value in values :
                lines[subset].append(value)
    file.close()

    file = open('eff_'+channel+'.tmp', 'w')
    for cat, subsets in categories.iteritems() :
        file.write(channel+'_'+cat+'\n')
        if len(subsets) == 0 :
            file.write("%s \t %s \t %s \n" % (lines[channel+'_'+cat][0], lines[channel+'_'+cat][1], lines[channel+'_'+cat][2]))
            file.write("%s \t %s \t %s \n" % (lines[channel+'_'+cat][3], lines[channel+'_'+cat][4], lines[channel+'_'+cat][5]))
            file.write("%s \t %s \t %s \n" % (lines[channel+'_'+cat][6], lines[channel+'_'+cat][7], lines[channel+'_'+cat][8]))
        else :
            lines_summed = {
                'ggH' : 0.,
                'qqH' : 0.,
                'VH'  : 0.,
                }
            for sub in subsets :
                lines_summed['ggH']+=float(lines[channel+'_'+cat+'_'+sub][1])
                lines_summed['qqH']+=float(lines[channel+'_'+cat+'_'+sub][4])
                lines_summed['VH' ]+=float(lines[channel+'_'+cat+'_'+sub][7])
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
    ## order in which the samples should be shown in the table
    sample_order = {
        "tt" : ["ZTT", "QCD", "W", "ZJ", "TT", "VV", "Total", "Signal"],
        "mt" : ["ZTT", "QCD", "W", "ZLL", "TT", "VV", "Total", "Signal"],
        "et" : ["ZTT", "QCD", "W", "ZLL", "TT", "VV", "Total", "Signal"],
        "mm" : ["ZTT", "QCD", "WJets", "ZMM", "TTJ", "Dibosons", "Total", "Signal"],
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
    for sig in ['ggH', 'qqH', 'VH'] :
        lines[sig]  = sample_labels[sig]
    for cat, values in records.iteritems() :
        effs['ggH'] = '%.2e' % (float(values[1])/float(values[2]))
        effs['qqH'] = '%.2e' % (float(values[4])/float(values[5]))
        effs['VH' ] = '%.2e' % (float(values[7])/float(values[8]))
        for sig in ['ggH', 'qqH', 'VH'] :
            lines[sig] += "\t & \t \multicolumn{2}{|c|}{%s $\cdot 10^{-%d}$}" % (effs[sig][:effs[sig].find('e')], int(effs[sig][effs[sig].find('-')+1:]))
    for sig in ['ggH', 'qqH', 'VH'] :
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
    subsets_extended = {
        "0jet"  : ["low_7TeV", "high_7TeV"],
        "boost" : ["low_7TeV", "high_7TeV"],
        "vbf"   : ["7TeV"],
       #"btag"  : ["low_7TeV", "high_7TeV"],
        }
if len(periods) == 1 and contained('8TeV', periods) :
    subsets_extended = {
       #"0jet"     : ["low_8TeV", "high_8TeV"],
       #"boost"    : ["low_8TeV", "high_8TeV"],
        "boost" : ["8TeV"], ##for tt
        "vbf"   : ["8TeV"],
       #"btag"  : ["low_8TeV", "high_8TeV"],
        }
if contained('7TeV', periods) and contained('8TeV', periods) :
    subsets_extended = {
        "0jet"  : ["low_7TeV", "low_8TeV", "high_7TeV", "high_8TeV"],
        "boost" : ["low_7TeV", "low_8TeV", "high_7TeV", "high_8TeV"],
        "vbf"   : ["7TeV", "8TeV"],
       #"btag"  : ["low_7TeV", "low_8TeV", "high_7TeV", "high_8TeV"],
        }
## compact dictionary of subsets to be contraced (used fro mergin of efficiencies)
subsets_compact  = {
   #'0jet'     : ['low', 'high'],
   #'boost'    : ['low', 'high'],
    'boost'    : [], ##for tt
    'vbf'      : [],
   #'btag'  : ['low', 'high'],
    }
## categories to be shown in the table(s)
categories_in_table = [
   #'0jet',
   'boost',
   'vbf',
   #'btag'
    ]
## category labels for categories to be shown in table(s)
category_labels_in_table = {
    '0jet'     : "\emph{0-Jet}",
    'boost'    : "\emph{1-Jet}",
    'vbf'      : "\emph{VBF}",
    'btag'     : "\emph{B-Tag}",
    }

os.system("rm -f *.tmp")
for chn in channels :
    print "creating table for decay channel ", chn, "..."
    for period in periods :
        for cat in categories :
            path = options.input+"/htt_"+chn+"_"+cat+"_"+period+".txt"
            ## extract all relevant information from datacards
            extractor(path, period)
    ## merge run periods and subsets of event categories (for yields)
    merge_subsets(chn, subsets_extended)
    ## merge run periods and subsets of event categories (for efficiencies)
    merge_efficiencies(chn, subsets_compact, periods)
    ## make formated tex tables from compactified input 
    make_tables(chn, categories_in_table, category_labels_in_table)
#os.system("rm *.tmp")
