#!/usr/bin/env python
'''

Extract the limit information from a Higgs combine result(s)
and write it to stdout.

Author: Evan K. Friis, UW Madison

'''

from RecoLuminosity.LumiDB import argparse
import json
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('rootfiles', nargs='+', help='Combine tool output files')
    parser.add_argument('--json', action='store_true', help='Write output as JSON')
    parser.add_argument('--datum', type=str,
                        choices=['obs', '-2', '-1', 'exp', '+1', '+2', 'mass'],
                        help='Extract only one number')
    args = parser.parse_args()

    import ROOT

    tree = ROOT.TChain('limit')
    for file in args.rootfiles:
        tree.Add(file)

    def get_quantile(x):
        # Convert a float value to a string label
        if x < 0:
            return 'obs'
        elif 0.0 < x < 0.027:
            return '-2'
        elif 0.1 < x < 0.2:
            return '-1'
        elif 0.4 < x < 0.6:
            return 'exp'
        elif 0.8 < x < 0.85:
            return '+1'
        elif 0.97 < x < 0.976:
            return '+2'
        return None

    output = {}

    for row in tree:
        quantile = get_quantile(row.quantileExpected)
        limit = row.limit
        output[quantile] = limit
        output['mass'] = row.mh

    if args.json:
        json.dump(output, sys.stdout, indent=2)
    else:
        if not args.datum:
            for key in output.keys():
                sys.stdout.write("%s: %0.2f\n" % (key, output[key]))
        else:
            sys.stdout.write("%0.2f\n" % (output[args.datum]))


