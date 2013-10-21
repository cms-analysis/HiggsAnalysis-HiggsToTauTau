#!/usr/bin/env python

'''

Merge template errors from the smallest to the largest contribution in each bin

Orignal script by: Evan K. Friis, UW Madison
Modifications by: A. Gilbert
'''

from RecoLuminosity.LumiDB import argparse
from math import sqrt
import fnmatch
import logging
import os
import ROOT
import shutil
import sys

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch()  

log = logging.getLogger('merger')

def walk_and_copy(inputdir, outputdir, folder, processes, bbb_threshold, merge_threshold):
    ''' Recursive function which copies from inputdir to outputdir '''
    merge_bkgs = processes
    found_folder = False
    path = inputdir.GetPath().split(':')[1]
    rel_path = path if path[0] != '/' else path[1:]
    if fnmatch.fnmatch(path, folder) or fnmatch.fnmatch(rel_path, folder) :
        log.debug("==== Found folder ")
        found_folder = True

    directories = []
    histos = []
    for key in inputdir.GetListOfKeys():
        # Keep track of stuff we find in this directory
        name = key.GetName()
        classname = key.GetClassName()
        if classname.startswith('TDirectory'):
            directories.append(name)
        elif isinstance(inputdir.Get(name), ROOT.TH1):
            histos.append(name)

    results = [ ]
    if found_folder:
      bbb_added = 0
      bbb_removed = 0
      hist_map = [ ]
      # First get a list of all the backgrounds we will consider
      for bkg in merge_bkgs:
        th1 = inputdir.Get(bkg)
        hist_map.extend([(bkg, inputdir.Get(bkg))])

      # loop through bins
      for ibin in range(1, hist_map[0][1].GetNbinsX()+1):
        log.debug("==== Bin %(ibin)s" % vars())
        # tot_bbb_added is the sum of squared bin errors for all
        # bacgrounds in the list that pass the bbb_threshold
        tot_bbb_added = 0.
        # In this first pass just count the total squared error
        for bkg in hist_map: 
          val = bkg[1].GetBinContent(ibin)
          err = bkg[1].GetBinError(ibin)
          if (val == 0 and  err == 0): continue
          if (val == 0 or err/val > bbb_threshold):
            bbb_added += 1
            tot_bbb_added += (err * err)
        if tot_bbb_added == 0: continue
        results = [ ]
        # In this second pass fill a new list of each background
        # with the fraction of the total squared error this background
        # contributes. Backgrounds that do not pass the bbb_threshold
        # are ignored (even if they happen to contribute a large fraction
        # of the total error!)
        for bkg in hist_map: 
          val = bkg[1].GetBinContent(ibin)
          err = bkg[1].GetBinError(ibin)
          if (val == 0 and  err == 0): continue
          if (val == 0 or err/val > bbb_threshold):
            results.extend([(bkg[0], err*err/tot_bbb_added, bkg[1])])
        # Now sort this list starting with the smallest error fraction
        results.sort(key=lambda tup: tup[1])
        #print results
        removed = 0.
        # Loop through removing bin errors, keeping track of the total
        # fraction removed. Stop once we reach the merge_threshold, or
        # the largest contributing background (whichever occurs first)
        for res in results:
          remove = False
          if res[1]+removed < merge_threshold and results.index(res) < (len(results)-1):
            log.debug("%(res)s ==> removed"% vars())
            remove = True
            bbb_removed += 1
            removed += res[1]
            res[2].SetBinError(ibin, 0.0)
          else:
            log.debug("%(res)s"% vars())
        # scale up remaining bin errors to account for the errors that were removed
        for res in results:
          expand = sqrt(1./(1.-removed))
          res[2].SetBinError(ibin, res[2].GetBinError(ibin) * expand)
      print 'Total bbb added:    '+str(bbb_added)
      print 'Total bbb removed:  '+str(bbb_removed)
      print 'Total bbb =======>: '+str(bbb_added-bbb_removed)
      
      # Copy all histograms from input -> output directory
      # If a histogram is part of the set 'results' where we merged
      # then write this instead of copying
    for histo in histos:
      th1 = inputdir.Get(histo)
      th1.SetName(histo)
      outputdir.cd()
      write_mod = True
      for res in results:
        if res[0] == histo:
          res[2].Write()
          write_mod = False
      if write_mod: 
        th1.Write()

     # Now copy and recurse into subdirectories
    for subdir in directories:
      print "subdir: "+subdir
      output_subdir = outputdir.mkdir(subdir)
     # Recurse
      walk_and_copy(
         inputdir.Get(subdir), output_subdir,
         folder, processes, bbb_threshold, merge_threshold)

def main(inputfilename, outputfilename, folder, processes, bbb_threshold, merge_threshold):
    process_list = processes.split(',')
    input = ROOT.TFile(inputfilename, 'READ')
    if not input:
        raise IOError("Can't open input file: %s" % inputfilename)
    output = ROOT.TFile(outputfilename, 'RECREATE')
    if not output:
        raise IOError("Can't open output file: %s" % outputfilename)
    print 'Input file:  '+inputfilename
    print 'Output file: '+outputfilename
    print 'Folder:      '+folder
    print 'Processes:   '+', '.join(process_list)
    walk_and_copy(input, output, folder, process_list, bbb_threshold, merge_threshold)
    #walk_and_copy(ROOT.TFile("htt_mt.inputs-sm-8TeV.root",'READ'),ROOT.TFile("htt_mt.inputs-sm-8TeV-test.root",'RECREATE'),"muTau_vbf_tight","W,QCD,ZL,ZJ",0.1,1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input .root file')
    parser.add_argument('output', help='Output .root file')
    parser.add_argument('--folder', default='',
                        help='full name of the category folder, e.g. muTau_vbf')
    parser.add_argument('--processes', metavar='pattern',
                        help='Comma separated list of backgrounds to consider for merging')
    parser.add_argument('--bbb_threshold', type=float, default=0.1,
                        help='Only consider background for merging if it passes bbb threshold'
                        'default %(default)0.1f')
    parser.add_argument('--merge_threshold', type=float, default=1.0,
                        help='Maximum fraction of total bin error that can be re-assigned'
                        'default %(default)1.0f')
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
    main(args.input, args.output, args.folder, args.processes, args.bbb_threshold,
         args.merge_threshold)
    log.info("Moving temprorary output to final destination")
    shutil.move(args.output, args.output.replace('.tmp.root', '.root'))
