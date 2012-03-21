#!/usr/bin/env python
from optparse import OptionParser
       
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3 ...",
                      description="Script to setup the calculation of MSSM limits from the SM hww exclusion limits. This takes into account that the presence of MSSM Higgs bosons implies that a SM-like Higgs boson should exist at ~130 GeV. The setup implies that the hww SM datacards have been setup in a corresponding directory. The preparation of the cards follows three steps. In a first step all available masses are surveyed and written into the masses.vals filw, which is of importance for the MSSM limit calculation. In a second step all signal yields in the SM datacards are divided by the SM cross section. In a third step the datacards of the mass regions which are really of relevance for the MSSM limit calculation (in most cases this will be datacards for ~130 GeV) will be copied over to the corresponding mA directory. NOTE: from this point on the hww datacards do not correspond any more to the limit at mA, but to the limit of mH (or mh) evaluated at mA. ARG1, ARG2, ARG3, ... correspond to the input directories.")
parser.add_option("-t", "--tanb",  dest="tanb",     default=10.,   type="float",   help="Value of tanb. [Default: 10]")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="Run in verbose mode. [Default: False]")
parser.add_option("-c", "--channels", dest="channels", default="hwwof_0j_shape, hwwof_1j_shape, hwwsf_0j_shape, hwwsf_1j_shape, hww_2j_cut", type="string", help="List of sub-channels [default: \"hwwof_0j_shape, hwwof_1j_shape, hwwsf_0j_shape, hwwsf_1j_shape, hww_2j_cut\"]")
parser.add_option("-x", "--cross-point", dest="cross_point", default=250., type="float", help="Cross point from where on mh dominates over mH. [Default: 250.]")

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)


import re
import os
from MitLimits.Higgs2Tau.mssm_xsec import query


def load_available_masses(decay_channel) :
    """
    Read all available masses for a given decay channel. The values are read from a file masses.vals,
    which is expected to be located in the same directory, in which the script is executed. If the
    file is not found it is looked for in a directory with name 'common' next to the current directory.
    The variable 'decay_channel' is expected to be of type of self.decay_channel (='htt_em_0',
    'htt_em_1', 'htt_em_2', ...).
    """
    masses = []
    if os.path.exists("masses.vals") :
        file = open("masses.vals", 'r')
    else :
        file = open("%s/../common/masses.vals" % os.getcwd(), 'r')
    for line in file :
        words = line.split()
        if words[0] == decay_channel :
            for word in words :
                if re.search(r"^\d+\.?\d+?$", word.strip()) :
                    masses.append(float(word))
    file.close()
    return masses

def embracing_masses(mass, masses) :
    """
    Determine the closest lower and upper mass value to 'mass' in the list of 'masses'. The return
    value of this function is a tuple of a boolean to indicate whether 'mass' was out of range or
    not and of the closest lower and upper mass value. In case that the mass was out of range the
    closest lower and upper mass values are -1. At the moment a warning is issued in this case.
    """
    lower  = -1.
    upper  = -1.
    failed = False
    for idx in range(len(masses)-1) :
        if idx == (len(masses)-2) and lower<0:
            print 'mass out of range: m=%.3f'% mass
            failed = True
        elif masses[idx]<mass and mass<=masses[idx+1] :
            lower = masses[idx  ]
            upper = masses[idx+1]
    #print "embracing masses: ", lower, " -- ", mass, " -- ", upper
    return (failed, lower, upper)

def load_masses(mA, tanb) :
    """
    Fill mh and mH depending on mA. These values are calculated from the htt tools.
    """
    ## read cross section results for htt
    htt_query = query(mA, tanb)
    mh = htt_query['higgses']['h']['mass']
    mH = htt_query['higgses']['H']['mass']
    return (mh, mH)

def prepare_hww(mA, tanb, cross_point, sub_channels) :
    """
    For the SM hww channel the selection has been optimized for each mass point. To the MSSM exclusion
    only the SM search in a mass range between ~130 and ~250 GeV really contributes. (For mA<250 GeV
    the contribution from H runs from ~130 GeV to 250 GeV; for mA>250 GeV the contribution from h is
    fixed at ~130 GeV). As the selection and the MVA discriminator for signal AND background varies as
    function of the mass (mA) the whole set of datacards and input histograms needs to be copied from
    the mass region that is of actual relevance to get the MSSM exclusion right. For simplicity the
    datacards and input files from the closest available masspoint for the hww datacards and for the
    Higgs boson of relevance (H or h) is copied to the current directory. 
    """
    (mh, mH) = load_masses(mA, tanb)
    mass = mH if (mA<cross_point) else mh
    for channel in sub_channels :
        masses = load_available_masses(channel)
        (failed, lower, upper) = embracing_masses(mass, masses)
        if not failed :
            value = lower if mass-lower<upper-mass else upper
            if value == mA :
                print "nothing needs to be done:", "mH" if mA<cross_point else "mh", "are the same"
            else :
                print "copy hww limit from ", "%.0f" % value, "to", "%.0f" % mA, "[mH-driven]" if mA<cross_point else "[mh-driven]"
                os.system("cp ../../tmp/{mass}/{channel}* .".format(mass="%.0f" % value, channel=channel[:channel.rfind('_')]))
            

## base directory introduced to allow use of absolute file paths
base_directory = os.getcwd()
## determine list of sub-channels 
channel_word = re.sub(r'\s', '', options.channels)
channel_list = channel_word.split(',')

## map ditau decay-channels to all available mass directories
channel_to_masses = {}
for channel in channel_list :
    channel_to_masses[channel] = []
    for directory in args :
        if directory.find("common")>-1 :
            continue 
        for datacard in os.listdir(directory) :
            if datacard.find(channel)>-1 :
                channel_to_masses[channel].append(directory[directory.rfind("/")+1:])
                break

if os.path.exists(args[0][:args[0].find('/')+1]+'common/masses.vals') :
    masses_file = open(args[0][:args[0].find('/')+1]+'common/masses.vals', 'a')
else :
    masses_file = open(args[0][:args[0].find('/')+1]+'common/masses.vals', 'w')

for channel in channel_to_masses :
    masses_file.write(channel+" : "+'  '.join(channel_to_masses[channel])+'\n')
masses_file.close()

## scale initial datacards to unit (i.e. divide by SM cross section)
masses = ""
for directory in args :
    if directory.find("common")>-1 :
        continue
    masses+=" "+directory[directory.rfind("/")+1:]
os.system("scale2unit.py -i %s -c hww %s" % (directory[:directory.rfind("/")], masses))

## copy mass regions relevant for the MSSM limit from hww for given mA into each corresponding mass directory
os.system("cp -r %s tmp" % args[0][:args[0].find('/')])
for directory in args :
    if directory.find("common")>-1 :
        print "> skipping directory common"
        continue 
    print "> entering directory %s" % directory
    ## visit subdirectories
    subdirectory = os.path.join(base_directory, directory)
    subdirectory = subdirectory.replace(os.path.join(base_directory, base_directory), base_directory)
    os.chdir(subdirectory)
    masspoint = float(directory[directory.rfind("/")+1:])
    prepare_hww(masspoint, options.tanb, options.cross_point, channel_list)

## cleanup
os.system("cd ../..; rm -r tmp")
print "done"
