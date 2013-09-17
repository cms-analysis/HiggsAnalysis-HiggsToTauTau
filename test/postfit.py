#!/usr/bin/env python

'''

Script to modify a datacard shape file to match the post-fit values.

See --help for usage.

Authors: R. Wolf, A. Hinzmann, E. Friis, M. Verzetti

'''

from RecoLuminosity.LumiDB import argparse
import logging
from DatacardUtils import parse_dcard
import sys
import math

log = logging.getLogger('postfit')

def quad(*args):
    return math.sqrt( 
        sum(
            map(lambda x: x**2, args)
        )
    )

def reset_bin_errors(histogram):
    ''' Reset a histograms errors to zero '''
    if 'obs' in histogram.GetName():
        return
    for i in range(1, histogram.GetNbinsX() + 1):
        histogram.SetBinError(i, 0)


def apply_postfit_normalization(histogram, scale, scale_uncertainty):
    ''' Apply a scale factor + uncertainty to a histogram.

    The errors are *increased* by the *square* of the corresponding
    uncertainty.  The histogram is modified in place.
    '''
    histogram.Scale(scale)
    for i in range(1, histogram.GetNbinsX() + 1):
        content = histogram.GetBinContent(i)
        error = quad(
            histogram.GetBinError(i),
            (scale_uncertainty * content)
        )
        histogram.SetBinError(i, error)


def apply_postfit_shape(histogram, up, down, shift, shift_err):
    '''  Apply a shape shift.

    Histogram is modified in place.
    '''
    for bin in range(1, histogram.GetNbinsX() + 1):
        upper = up.GetBinContent(bin)
        lower = down.GetBinContent(bin)
        if down.GetBinContent(bin) < 0.01:
            lower = 0
        central = histogram.GetBinContent(bin)
        value = 1
        if shift > 0 and central > 0 and upper != central:
                value = shift * (upper / central - 1) + 1
        elif shift < 0 and central > 0 and lower != central:
                value = abs(shift) * (lower / central - 1) + 1
        if value != 1:
            central *= value
            histogram.SetBinContent(bin, central)

        uncertainty = 1
        if lower and central: #central is the shifted value!
            uncertainty = max(
                uncertainty,
                central / lower,
                lower / central)

        if upper and central:
            uncertainty = max(
                uncertainty,
                central / upper,
                upper / central)
        uncertainty = shift_err * min(2, uncertainty - 1)
        error = quad( 
            histogram.GetBinError(bin),
            (histogram.GetBinContent(bin) * uncertainty)
        )
        histogram.SetBinError(bin, error)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('shapes', help="Path to shape file (will be updated)")
    parser.add_argument('card', help="Path to datacard")
    parser.add_argument('--fitresults', default='fitresults/mlfit_sm.txt',
                        help="Path to ML fit results .txt file")
    parser.add_argument('--bins', default=["ANYBIN"], nargs='+',
                        help="Bins (channels) to update")
    parser.add_argument('--dry-run', dest='dry', action='store_true',
                        help="Don't actually change anything")
    parser.add_argument('--verbose', action='store_true')

    args = parser.parse_args()

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.DEBUG if args.verbose else logging.WARNING)

    import ROOT
    ROOT.gROOT.SetBatch(True)

    log.info("Loading input shape file %s", args.shapes)
    shapes = ROOT.TFile(args.shapes, "UPDATE")

    for bin in args.bins:
        # We rely that the histograms are in the "<bin name>/" directory.
        log.info("Examining bin directory %s", bin)
        bin_directory = shapes.Get(bin)
        bin_directory.cd()

        log.info("Parsing postfit results and data card.")
        p_weight, p_shape_weight, p_unc, p_shape_unc = parse_dcard(
            args.card, args.fitresults, bin)

        histogram_names = set([])
        # We have to do a first pass to get the names - can't modify
        # keys while iterating over them.
        for key in bin_directory.GetListOfKeys():
            name = key.GetName()
            histo = bin_directory.Get(name)
            if isinstance(histo, ROOT.TH1):
                histogram_names.add(name)

        for name in histogram_names:
            histo = bin_directory.Get(name)
            #log.debug("Found histogram: %s", name)
            # Start the errors from scratch
            reset_bin_errors(histo)

            # Apply shape shifts
            if name in p_shape_weight:
                for shape, shape_shift in p_shape_weight[name].iteritems():
                    log.info("Shifting %s/%s with shape %s by %0.3f",
                             bin, name, shape, shape_shift)
                    up = bin_directory.Get(name + "_" + shape + "Up")
                    down = bin_directory.Get(name + "_" + shape + "Down")
                    apply_postfit_shape(histo, up, down, shape_shift, 0)

            # Apply normalization scale
            if name in p_weight:
                log.info("Scaling %s/%s by %0.3f +- %0.3f",
                         bin, name, p_weight[name], p_unc[name])
                apply_postfit_normalization(histo, p_weight[name], p_unc[name])
            histo.Write(name, ROOT.TObject.kOverwrite)
