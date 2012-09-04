'''

DataCard.py

Class which wraps a .txt limit datacard.  Offers convenience methods
to get the total yields combining bins, with the correctly calculated errors.

Usage:

    >>> dc = DataCard("path/to/card.txt")
    >>> obs = dc.get_obs("muTau_*") # adds up muTau_vbf + muTau_boost
    >>> ztt_yield = dc.get_rate("muTau_*", "ZTT") # gets rate for ZTT w/ error
    >>> print ztt_yield.nominal_value, ztt_yield.std_dev()

Author: Evan K. Friis, UW Madison

'''

from HiggsAnalysis.CombinedLimit.DatacardParser import \
        parseCard, addDatacardParserOptions
import fnmatch
import math
from optparse import OptionParser
import os
from HiggsAnalysis.HiggsToTauTau.uncertainties import ufloat
import sys

# The DatacardParser takes some wacky arguments
_parser = OptionParser()
addDatacardParserOptions(_parser)
(_options, _args) = _parser.parse_args([])
_options.bin = True # fake that is a binary output, so that we parse shape lines

def quad(*xs):
    return math.sqrt(sum(x*x for x in xs))

class DataCard(object):
    def __init__(self, filename):
        self.file = open(os.path.expandvars(filename), 'r')
        # Read the card into a set of dictionaries
        self.card = parseCard(self.file, _options)

        # Create a dictionary of named systematics in the card.
        # Each one has an uncertainty centered at zero, with sigma=1
        self.systematics = {}
        for syst in self.card.systs:
            self.systematics[syst[0]] = ufloat((0, 1), syst[0])

    def get_obs(self, bins, excludebin=None):

        if isinstance(bins, basestring):
            bins = [bins]
        if isinstance(excludebin, basestring):
            excludebin = [excludebin]

        matching_bins = set([])

        for binpattern in bins:
            for realbin in self.card.exp.keys():
                # First check if we explicitly exclude it
                excluded = False
                if excludebin is not None:
                    for excludepattern in excludebin:
                        if fnmatch.fnmatch(realbin, excludepattern):
                            excluded = True
                            break
                if excluded:
                    continue
                # otherwise check if it matches a desired bin
                if fnmatch.fnmatch(realbin, binpattern) or fnmatch.fnmatch(realbin, 'bin' + binpattern):
                    matching_bins.add(realbin)

        obs = 0
        for bin in matching_bins:
            obs += self.card.obs[bin]
        return int(obs)


    def get_rate(self, bins, process, excludesys=None, excludebin=None):
        ''' Get the total yield for [process] in the sum of bins

        Includes all systematic error.  Optionally, pass a list
        of patterns to exclude.

        Bins can include wildcards.

        Returns a ufloat object.

        >>> dc = DataCard("$fsa/StatTools/test/vh3l_120.txt")
        >>> rate = dc.get_rate('*', 'ZZ').nominal_value
        >>> rate
        0.254
        >>> exp_error = quad(0.045, 0.04, 0.04, 0.015, 0.02, 0.02, 0.02, 0.01,
        ...                  0.04, 0.192)
        >>> abs(dc.get_rate('*', 'ZZ').std_dev() - rate*exp_error) < 1e-6
        True

        '''
        if isinstance(bins, basestring):
            bins = [bins]
        if isinstance(excludebin, basestring):
            excludebin = [excludebin]

        matching_bins = set([])

        for binpattern in bins:
            for realbin in self.card.exp.keys():
                # First check if we explicitly exclude it
                excluded = False
                if excludebin is not None:
                    for excludepattern in excludebin:
                        if fnmatch.fnmatch(realbin, excludepattern):
                            excluded = True
                            break
                if excluded:
                    continue
                # otherwise check if it matches a desired bin
                if fnmatch.fnmatch(realbin, binpattern) or fnmatch.fnmatch(realbin, 'bin' + binpattern):
                    matching_bins.add(realbin)

        if not matching_bins:
            raise KeyError("No bins match patterns: %s \n\n Available: %s" % (
                " ".join(bins), " ".join(self.card.exp.keys())))

        total_expected = 0

        for bin in matching_bins:
            total_relative_error = 1
            if bin not in self.card.exp:
                raise KeyError("Can't find bin %s in card, I have: %s" %
                               (bin, " ".join(self.card.exp.keys())))
            the_bin = self.card.exp[bin]
            if not process in the_bin:
                raise KeyError("Can't find process %s in bin %s, I have: %s" %
                               (process, bin, " ".join(the_bin.keys())))

            expected = the_bin[process]
            for syst in self.card.systs:
                if excludesys and syst[0] in excludesys:
                    continue
                error_object = self.systematics[syst[0]]
                error = syst[4][bin][process]
                if error and error != 1:
                    if isinstance(error, list): # up/down format
                        error = error[1]
                    if syst[2] != 'gmN':
                        percent_error = error - 1
                        multiplier = 1 + percent_error*error_object
                        total_relative_error = total_relative_error*multiplier
                    else:
                        n = syst[3][0]
                        multiplier = 1 + (math.sqrt(n)/n)*error_object
                        total_relative_error = total_relative_error*multiplier
                #print syst[0], error, total_relative_error
            total_expected += expected*total_relative_error
        return total_expected

    def get_systematic_effect(self, bins, process, systematics):
        ''' Get the total relative effect of a systematic on a process yield

        >>> dc = DataCard("$fsa/StatTools/test/vh3l_120.txt")
        >>> dc.get_systematic_effect('1', 'WZ', 'lumi')
        0.0
        >>> abs(dc.get_systematic_effect('1', 'ZZ', 'lumi') - 0.045) < 1e-6
        True

        '''

        if isinstance(systematics, basestring):
            systematics = [systematics]

        errors = [0]

        rate = self.get_rate(bins, process)
        for systematic in systematics:
            for var, error in rate.error_components().items():
                if var.tag == systematic:
                    errors.append(error)
        return quad(*errors)/rate.nominal_value

    def get_systematics(self, bins, process, excludesys=None):
        ''' Return a list of the systematic effects, sorted by descending size

        The format is [(syst_name1, rel. error), (syst_name2, ... ]
        '''
        rate = self.get_rate(bins, process, excludesys)
        errors = [('Total', rate.std_dev()/rate.nominal_value)]
        for var, error in rate.error_components().items():
            errors.append((var.tag.strip(), error/rate.nominal_value))

        errors.sort(key = lambda x: -1*x[1])
        return errors

    def print_systematics(self, bins, process, stream=sys.stdout, excludesys=None):
        ''' Print out a nice list of the systematic effects '''
        errors = self.get_systematics(bins, process, excludesys)
        rate = self.get_rate(bins, process, excludesys)
        for i in range(70):
            stream.write('=')
        stream.write('\n')
        stream.write("%-40s: %0.2f +- %0.2f\n" % (
            process + ' (' + ','.join(bins) + ')',
            rate.nominal_value, rate.std_dev()))
        for i in range(70):
            stream.write('-')
        stream.write('\n')
        for error in errors:
            stream.write("%-40s: %0.1f%%\n" % (error[0], 100.*error[1]))
        for i in range(70):
            stream.write('=')
        stream.write('\n')

if __name__ == "__main__":
    import doctest; doctest.testmod()

