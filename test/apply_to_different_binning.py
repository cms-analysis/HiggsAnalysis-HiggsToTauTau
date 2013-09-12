#!/usr/bin/env python

'''

Script to modify a datacard shape file in the same way another shape file was modified.
Useful to propagate pulls on shapes with different binning.

Authors: M. Verzetti

Usage

apply_to_different_binning.py shapes_to_change prefit_shapes postfit_shapes 

'''

import sys
import os
import logging
import re
from RecoLuminosity.LumiDB import argparse

def check_compatibility(fine, coarse):
    'checks that there coarse histogram bin edges overlap with fine one'
    fine_edges   = [fine.GetBinLowEdge(i) for i in range( fine.GetNbinsX()+2 )]
    coarse_edges = [coarse.GetBinLowEdge(i) for i in range( coarse.GetNbinsX()+2 )]
    return all( (i in fine_edges) for i in coarse_edges)

def apply_pulls(toapply, prefit, postfit):
    'actually does the trick'
    fine_edges   = [toapply.GetBinLowEdge(i) for i in range( toapply.GetNbinsX()+2 )]
    coarse_edges = [prefit.GetBinLowEdge(i) for i in range( prefit.GetNbinsX()+2 )]
    coarse_counter = 0
    error_scale = -1
    yield_scale = -1
    for ibin, lowedge in zip(range(fine.GetNbinsX()+1), fine_edges):
        if lowedge in coarse_edges: #we are entering a new bin!
            coarse_counter += 1
            error_scale = postfit.GetBinError(coarse_counter) / prefit.GetBinError(coarse_counter)
            yield_scale = postfit.GetBinContent(coarse_counter) / prefit.GetBinContent(coarse_counter)
        toapply.SetBinContent( toapply.GetBinContent(ibin)*yield_scale )
        toapply.SetBinError( toapply.GetBinError(ibin)*error_scale )

def find_histos(dir, root = '', regex=re.compile('TH1')):
    tempList = dir.GetListOfKeys()
    retList  = []
    for it in range(0, tempList.GetSize()):
        key = tempList.At(it)
        if regex.match( key.GetClassName() ):
            retList.append( key.GetName() )
        elif 'TDirectory' in key.GetClassName():
            newroot = '/'.join([root, key.GetName()])
            retList.extend( 
                find_histos(
                    key.ReadObj(), 
                    newroot, 
                    regex)
            )
    return retList
    

import ROOT
ROOT.gROOT.SetBatch(True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('shapes_to_change', help="Path to new shape file (will be updated)")
    parser.add_argument('prefit_shapes', help="prefit shapes")
    parser.add_argument('postfit_shapes', help="postfit shapes")
    parser.add_argument('--filter-out', dest='filter', default='',
                        help="regex to remove some histogram")
    parser.add_argument('--bins', default=["ANYBIN"], nargs='+',
                        help="Bins (channels) to update")
    parser.add_argument('--verbose', action='store_true')
 
    args = parser.parse_args()
    log = logging.getLogger('apply_to_different_binning')


    logging.basicConfig(
    stream=sys.stderr,
        level=logging.DEBUG if args.verbose else logging.WARNING)
    
    log.info("Loading input shape file %s", args.shapes)
    shapes_to_change = ROOT.TFile(args.shapes_to_change, "UPDATE")
    postfit_shapes   = ROOT.TFile(args.postfit_shapes)
    prefit_shapes    = ROOT.TFile(args.prefit_shapes)

    available_histos = find_histos(shapes_to_change)
    if args.filter:
        regex = re.compile(args.filter)
        available_histos = filter( lambda x: regex.match(x), available_histos)
    
    for path in available_histos:
        to_apply = shapes_to_change.Get(path)
        prefit   = prefit_shapes.Get(path)
        postfit  = postfit_shapes.Get(path)
        if bool(prefit) and bool(postfit):
            apply_pulls(to_apply, prefit, postfit)
        elif not bool(prefit):
            log.warning('Histogram %s not found in %s. Skipping...' % (path, args.prefit_shapes))
        else:
            log.warning('Histogram %s not found in %s. Skipping...' % (path, args.postfit_shapes))
        to_apply.Write(name, ROOT.TObject.kOverwrite)
