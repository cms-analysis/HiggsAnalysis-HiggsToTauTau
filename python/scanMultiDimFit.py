#!/usr/bin/env python

'''

Scan the output of the combine -M MultiDimFit likelihood scan, and determine
the best fit and confidence interval.

Author: Evan K. Friis, UW

'''

import json
import sys
from optparse import OptionParser, OptionGroup

def extract_band(filename, deltaNLLTarget=0.5):
    ''' Turn the NLL scan into a central value (best fit) + band '''
    # Import ROOT here so it can't mess with sys.argv
    import ROOT
    file = ROOT.TFile(filename)
    limit_tree = file.Get("limit")
    values = []
    for row in limit_tree:
        values.append( (row.r, row.deltaNLL) )

    # Split the likelihood into left and right of minimum
    left_of_minimum = []
    right_of_minimum = []

    found_zero = False
    best_r = None
    full_graph = ROOT.TGraph(len(values)-1)
    for i, (r, deltaNLL) in enumerate(values):
        if not best_r:
            best_r = r
            continue
        if ROOT.TMath.IsNaN(deltaNLL):
            #print "skipping nan"
            continue
        full_graph.SetPoint(i-1, r, deltaNLL)
        if r < best_r:
            #print 'L %0.2f => %0.2f' % (r, deltaNLL)
            left_of_minimum.append( (r, deltaNLL) )
        else:
            #print 'R %0.2f => %0.2f' % (r, deltaNLL)
            right_of_minimum.append( (r, deltaNLL) )

    # Now convert these into TGraphs
    left = ROOT.TGraph(len(left_of_minimum))
    right = ROOT.TGraph(len(right_of_minimum))

    # Populate the graphs, inverting the x and y axis - what we are interested
    # in is the r value at deltaNLL = 0.5, this makes it easy.
    for i, (r, deltaNLL) in enumerate(left_of_minimum):
        left.SetPoint(i, deltaNLL, r)
    for i, (r, deltaNLL) in enumerate(right_of_minimum):
        right.SetPoint(i, deltaNLL, r)

    # Extract the lower and upper bounds on r
    lower_bound = left.Eval(deltaNLLTarget)
    upper_bound = right.Eval(deltaNLLTarget)

    return (lower_bound, best_r, upper_bound, full_graph)

if __name__ == "__main__":
    parser = OptionParser(usage="usage: %prog [options] combine_output.root",
                          description="Convert output of -M MultiDimFit to a confidence intervale")
    ## direct options
    parser.add_option("--target", dest="target", default='0.5',
                      help='Target deltaNLL to produce bands')
    parser.add_option("--json", dest="json", default=False, action='store_true',
                      help='Output in JSON format')

    (options, args) = parser.parse_args()

    if len(args) < 1 :
        parser.print_usage()
        exit(1)

    result = extract_band(args[0], float(options.target))
    if options.json:
        print json.dumps({
            'best_fit' : result[1],
            'low' : result[0],
            'high' : result[2],
        })

