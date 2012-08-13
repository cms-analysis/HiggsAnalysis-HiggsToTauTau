#!/usr/bin/env python

'''

Count the number of CRAB jobs returned (i.e. root files) for a set of directories.

Author: Evan K. Friis, UW

'''

import RecoLuminosity.LumiDB.argparse as argparse
import glob
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('directories', nargs='+',
                        help='Datacard directories.  (Ex: cmb/*)')

    args = parser.parse_args()

    for dir in args.directories:
        if os.path.basename(dir) == 'common':
            continue
        print "Datacard dir: %s" % dir
        for crab_dir in glob.glob(os.path.join(dir, 'crab_*')):
            count = len(glob.glob(os.path.join(crab_dir, 'res', '*.root')))
            print " => %i files in %s" % (count, crab_dir)
