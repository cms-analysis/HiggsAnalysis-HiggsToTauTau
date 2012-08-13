#!/usr/bin/env python

'''

Count the number of CRAB jobs returned (i.e. root files) for a set of directories.

Author: Evan K. Friis, UW

'''

import RecoLuminosity.LumiDB.argparse as argparse
import glob
import os
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('directories', nargs='+',
                        help='Datacard directories.  (Ex: cmb/*)')

    args = parser.parse_args()

    no_entries = set([])

    for dir in args.directories:
        if os.path.basename(dir) == 'common':
            continue
        sys.stderr.write("Datacard dir: %s\n" % dir)
        for crab_dir in glob.glob(os.path.join(dir, 'crab_*')):
            count = len(glob.glob(os.path.join(crab_dir, 'res', '*.root')))
            sys.stderr.write(" => %i files in %s\n" % (count, crab_dir))
            if not count:
                no_entries.add(crab_dir)


    if no_entries:
        sys.stderr.write("There are %i crab dirs with no entries!\n" % len(no_entries))
        # Write them to stdout
        for bad in no_entries:
            sys.stdout.write(bad + '\n')
