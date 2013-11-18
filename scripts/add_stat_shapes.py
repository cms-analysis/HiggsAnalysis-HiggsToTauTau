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

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch()  

log = logging.getLogger('stat_shapes')

def walk_and_copy(inputdir, outputdir, pattern, mergers, threshold, prefix, normalize):
    ''' Recursive function which copies from inputdir to outputdir '''
    keys = []
    for key in inputdir.GetListOfKeys():
        # Prevent double counting of histograms
        if key.GetName() in keys :
            continue
        elif isinstance(inputdir.Get(key.GetName()), ROOT.TH1) :
            keys.append(key.GetName())
        # Keep track of stuff we find in this directory
        directories = []
        histos = []
        name = key.GetName()
        classname = key.GetClassName()
        if classname.startswith('TDirectory'):
            if not name in directories :
                directories.append(name)
        elif isinstance(inputdir.Get(name), ROOT.TH1):
            if not name in histos :
                histos.append(name)
        # Copy all histograms from input -> output directory
        for histo in histos:
            th1 = inputdir.Get(histo)
            th1.SetName(histo)
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
                    error = error_clone.GetBinError(ibin)
                    val = th1.GetBinContent(ibin)
                    # Check if we are above threshold
                    above_threshold = False
                    if val:
                        if error/val > threshold:
                            above_threshold = True
                    else:
                        # If there is nothing in the bin, but there is
                        # an error, we respect this.
                        if error:
                            log.info("%s_%s_bin_%i is zero, but will have a non-zero error.",
                                     prefix, histo, ibin)
                            above_threshold = True

                    if above_threshold:
                        err_up = th1.Clone(
                            th1.GetName() + "_%s_%s_bin_%iUp" % (prefix, histo, ibin))
                        err_down = th1.Clone(
                            th1.GetName() + "_%s_%s_bin_%iDown" % (prefix, histo, ibin))
                        # Print to stdout, so we can capture the uncertainties
                        print "%s_%s_bin_%i" % (prefix, histo, ibin)
                        err_up.SetBinContent(ibin, val + error)
                        ## if not val > error bin the down entry to a small value >0 to prevent problems in combine 
                        err_down.SetBinContent(ibin, val - error if val > error else 0.01)
                        if normalize:
                            err_up.Scale(th1.Integral()/err_up.Integral())
                            err_down.Scale(th1.Integral()/err_down.Integral())
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
                pattern, mergers, threshold, prefix, normalize)

def main(inputfilename, outputfilename, matcher, mergers, threshold, prefix, normalize):
    input = ROOT.TFile(inputfilename, 'READ')
    if not input:
        raise IOError("Can't open input file: %s" % inputfilename)
    output = ROOT.TFile(outputfilename, 'RECREATE')
    if not output:
        raise IOError("Can't open output file: %s" % outputfilename)
    walk_and_copy(input, output, matcher, mergers, threshold, prefix, normalize)

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
    parser.add_argument('--normalize', action='store_true', default=False,
                        help='Normalize shifted templates to the original yield')
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
         args.threshold, args.prefix, args.normalize)
    log.info("Moving temprorary output to final destination")
    shutil.move(args.output, args.output.replace('.tmp.root', '.root'))
