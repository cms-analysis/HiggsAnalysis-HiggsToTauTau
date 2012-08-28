#!/usr/bin/env python
'''

Scale up the expected luminosity in the 8TeV cards.

Modifies the appropriate systematic errors which depend on the size of control
samples.

Author: Evan K. Friis, UW Madison

'''

from RecoLuminosity.LumiDB import argparse
import os
import re
import subprocess
import shlex

# Whitespace, systematic name, whitespace, 'gmN', whitespace, number, any non-number
_gmN_matcher = re.compile('\s*(?P<systematic>\w+)\s*gmN\s*(?P<count>\d+)[^0-9]*')

def scale_gmN(file, scale_factor):
    print "Scaling systematics in %s" % file
    unc_file = open(file, 'r')
    output_lines = []
    for line in unc_file.readlines():
        match = _gmN_matcher.match(line)
        if not match:
            output_lines.append(line.strip())
        else:
            name = match.group('systematic')
            count = int(match.group('count'))
            new_count = int(scale_factor*count)
            print "Scaling gmN %s %i => %i" % (name, count, new_count)
            output_lines.append(' '.join([name, 'gmN', str(new_count)]))
    unc_file.close()
    # Rewrite the file
    unc_file = open(file, 'w')
    for line in output_lines:
        unc_file.write(line + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('currentlumi', type=float, help="Current lumi of cards")
    parser.add_argument('targetlumi', type=float, help="Target lumi")
    parser.add_argument('--channels', nargs='+',
                        default=['et', 'mt', 'tt', 'em', 'mm', 'vhtt'])

    args = parser.parse_args()

    def file_map(channel):
        ''' Get the path to the appropriate shape file for a channel '''
        if channel == 'vhtt':
            return 'vhtt/vhtt.inputs-sm-8TeV.root'
        return os.path.join(channel, 'htt_' + channel + '.inputs-sm-8TeV.root')

    def get_unc_conf_val(channel, category):
        if channel == 'vhtt':
            return ('vhtt/unc-sm-8TeV-0%i.conf' % category, 'vhtt/unc-sm-8TeV-0%i.vals' % category)
        return (os.path.join(channel, 'unc-sm-8TeV-0%i.conf' % category),
                os.path.join(channel, 'unc-sm-8TeV-0%i.vals' % category))

    # Scale each channel up
    for channel in args.channels:
        print "Scaling shape file for channel: %s" % channel
        command = "root -l -q -b {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleLumi.C+\\(\\\"{FILE}\\\",{OLDLUMI},{NEWLUMI},true,2\\)"
        shape_file = file_map(channel)
        #print command.format(
        #        CMSSW_BASE = os.environ['CMSSW_BASE'],
        #        FILE=shape_file,
        #        OLDLUMI="%0.3f" % args.currentlumi,
        #        NEWLUMI="%0.3f" % args.targetlumi,
        #    )
        shape_scaling = subprocess.Popen(
            shlex.split(command.format(
                CMSSW_BASE = os.environ['CMSSW_BASE'],
                FILE=shape_file,
                OLDLUMI="%0.3f" % args.currentlumi,
                NEWLUMI="%0.3f" % args.targetlumi,
            )), stdout=subprocess.PIPE)

        (stdout, _) = shape_scaling.communicate()
        #print stdout
        
        for category in range(8):
            unc_conf, _ = get_unc_conf_val(channel, category)
            if os.path.exists(unc_conf):
                scale_gmN(unc_conf, args.targetlumi/args.currentlumi)
