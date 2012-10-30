#!/usr/bin/env python

'''

Add statistical shape errors (aka Barlow Beeston) to a shape .root file

Author: Evan K. Friis, UW Madison

'''

from RecoLuminosity.LumiDB import argparse
import fnmatch
import logging
import os
import ROOT
import shutil
import sys

log = logging.getLogger('stat_shapes')

def walk_and_copy(inputdir, outputdir, pattern, mergers, threshold, prefix):
    ''' Recursive function which copies from inputdir to outputdir '''
    for key in inputdir.GetListOfKeys():
        # Keep track of stuff we find in this directory
        directories = []
        histos = []
        name = key.GetName()
        classname = key.GetClassName()
        if classname.startswith('TDirectory'):
            directories.append(name)
        elif isinstance(inputdir.Get(name), ROOT.TH1):
            histos.append(name)
        # Copy all histograms from input -> output directory
        for histo in histos:
            th1 = inputdir.Get(histo)
            outputdir.cd()
            th1.Write()
            # Check if this histogram has shape uncertainties
            do_shapes = False
            path = inputdir.GetPath().split(':')[1]
            full_path = os.path.join(path, histo)
            # A version without a leading slash
            rel_path = full_path if full_path[0] != '/' else full_path[1:]
            #print "rel path: ", rel_path
            log.debug("Testing path %s against pattern %s", full_path, pattern)
            if fnmatch.fnmatch(histo, pattern) or \
               fnmatch.fnmatch(full_path, pattern) or \
               fnmatch.fnmatch(rel_path, pattern) :
                log.debug("Matches!")
                do_shapes = True

            if do_shapes:
                # check all bins to see if they need to be shape-errored
                log.info("Building stat shapes for %s", histo)
                # Check if we want to add any extra mergers
                error_clone = th1.Clone()
                # Check if we want to add the error from more histograms
                if mergers:
                    for merger in mergers:
                        log.info("Merging errors from %s into %s", merger, histo)
                        to_merge = inputdir.Get(merger)
                        error_clone.Add(to_merge)

                for ibin in range(1, th1.GetNbinsX()+1):
                    if th1.GetBinContent(ibin):
                        error = error_clone.GetBinError(ibin)
                        val = th1.GetBinContent(ibin)
                        # Check if we are above threshold
                        if error/val > threshold:
                            err_up = th1.Clone(
                                th1.GetName() + "_%s_%s_bin_%iUp" % (prefix, histo, ibin))
                            err_down = th1.Clone(
                                th1.GetName() + "_%s_%s_bin_%iDown" % (prefix, histo, ibin))
                            # Print to stdout, so we can capture the uncertainties
                            print "%s_%s_bin_%i" % (prefix, histo, ibin)
                            err_up.SetBinContent(ibin, val + error)
                            err_down.SetBinContent(ibin, val - error if val > error else 0.)
                            if val < error:
                                log.warning("%s_%s_bin_%iDown, is negative, pegged to zero", prefix, histo, ibin)
                            outputdir.cd()
                            err_up.Write()
                            err_down.Write()
                            log.info("==> built shape for %s bin %i", histo, ibin)

        # Now copy and recurse into subdirectories
        for subdir in directories:
            output_subdir = outputdir.mkdir(subdir)
            # Recurse
            walk_and_copy(
                inputdir.Get(subdir), output_subdir,
                pattern, mergers, threshold, prefix)

def main(inputfilename, outputfilename, matcher, mergers, threshold, prefix):
    input = ROOT.TFile(inputfilename, 'READ')
    if not input:
        raise IOError("Can't open input file: %s" % inputfilename)
    output = ROOT.TFile(outputfilename, 'RECREATE')
    if not output:
        raise IOError("Can't open output file: %s" % outputfilename)
    walk_and_copy(input, output, matcher, mergers, threshold, prefix)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input .root file')
    parser.add_argument('output', help='Output .root file')
    parser.add_argument('--prefix', default='CMS_htt_fixme',
                        help='Prefix for the systematic name,'
                        'fixme should be something like mutau, etau, etc')
    parser.add_argument('--filter', metavar='pattern',
                        help='Pattern of TH1F names to shape-ize')
    parser.add_argument('--merge-errors', nargs='+', dest='merge',
                        help='Merge in errors from different shapes. '
                        'Should be only the histogram name, which are '
                        'taken from the same directory as the filtered histo.')
    parser.add_argument('--threshold', type=float, default=0.05,
                        help='Minimum error for systematic creation,'
                        'default %(default)0.2f')
    parser.add_argument('--verbose', action='store_true',
                        help='Print debug output.')


    args = parser.parse_args()

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO if not args.verbose else logging.DEBUG)

    in_place = True
    if args.input == args.output:
        log.info("Modifying in place!  Backing up input file...")
        shutil.copy(args.input, args.input.replace('.root', '.root.bak'))
        args.output = args.output.replace('.root', '.tmp.root')

    log.info("Building shape systematics. input: %s output: %s",
             args.input, args.output)
    main(args.input, args.output, args.filter, args.merge,
         args.threshold, args.prefix)
    log.info("Moving temproary output to final destination")
    shutil.move(args.output, args.output.replace('.tmp.root', '.root'))
