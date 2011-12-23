#!/usr/bin/env python
'''

compute_limits.py

Author: Evan K. Friis, UC Davis

Command line tool which translates xsec * BR MSSM Higgs limits into the tanBeta
plane.

Takes as argument a text file with the xsec*BR limits.  The fields in the text
file can be delimited with commas, spaces, or TeX-table style.  The first column
is assumed to be the Higgs mass, and there should be a column for observed and
-2, -1, nominal, +1, and +2 expected limits.

'''

import sys
import HiggsAnalysis.HiggsToTauTau.mssm_xsec as mssm_xsec

# Convert all commas and latex stuff to spaces
def standardize_format(text):
    text = text.replace('&', ' ')
    text = text.replace('\hline', ' ')
    text = text.replace('\\', ' ')
    return text

def is_integer(string_field):
    try:
        int(string_field)
        return True
    except ValueError:
        return False

def get_columns(filename):
    # Convert the format into a set of columns
    xsec_br_limits_file = open(filename, 'r')
    limits = standardize_format(xsec_br_limits_file.read())

    # Separate the rows
    limit_lines = []
    for line in limits.split('\n'):
        clean_line = line.strip()
        if clean_line.startswith('#'):
            print "Skipping comment row %s" % line
            continue
        # Skip blank rows
        if not clean_line:
            continue
        fields = clean_line.split()
        # Check to make sure this isn't a header row
        if not is_integer(fields[0]):
            print "Skipping header row: %s" % line
            continue
        # Convert to floats
        limit_lines.append([float(x) for x in fields])
    return limit_lines

def translate_to_tan_beta(limit_lines, type, uncertainty):
    for limit_line in limit_lines:
        mass = limit_line[0]
        # Get tanb from each xsec limit
        transformed = [mass] + [
            mssm_xsec.get_tanb_limit(mass, limit, type, uncertainty)
            for limit in limit_line[1:]]
        yield transformed

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s xsec_br_limits.txt" % sys.argv[0]
        sys.exit(1)

    limit_lines = get_columns(sys.argv[1])

    #columns = ['mass',  'obs', '-2', '-1', 'exp', '+1', '+2',]
    columns = ['mass',  '', '', '', '', '', '',]
    formats = ['%6.0f'] + ['%8.2f']*(len(columns)-1)
    header_format = ['%6s'] + ['%8s']*(len(columns)-1)

    # Print different kinds of limits
    #for type in ['5flavor', '4flavor', 'santander']:
    #for uncertainty in [0, -1, 1]:
    for uncertainty in [0]:
        for type in ['5flavor', '4flavor', 'santander']:
        #for type in ['santander']:
            print "=============================================================="
            print "====  Tan Beta limits using scheme: %-12s  %-2i sigma ===" % (type, uncertainty)
            print "=============================================================="
            print " ".join(header_format) % tuple(columns)
            for transformed in translate_to_tan_beta(limit_lines, type, uncertainty):
                if '--tex' not in sys.argv:
                    print " ".join(format % value
                                   for format, value in zip(formats, transformed))
                else:
                    print " & ".join(
                        format % value
                        for format, value in zip(formats, transformed)) + " \\\\"
