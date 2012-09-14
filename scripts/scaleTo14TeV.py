#!/usr/bin/env python

'''

Scale *everything* from 8 to 14 TeV (for an equivalent int. lumi)

Cross section scaling factors provided by Guillelmo Gomez-Ceballos Retuerto

http://ceballos.web.cern.ch/ceballos/mcfm/xsec_several_ecm.txt

Author: Evan K. Friis, UW Madison

'''

from RecoLuminosity.LumiDB import argparse
import os

_SCALE_FACTORS = {
    'Z' : 2.02904/1.14951,
    'W' : 2.09545/1.15786,
    'tt' : 5.59001/1.42982,
    'WZ' : 2.79381/1.23344,
    'WW' : 2.62549/1.21510,
    'ZZ' : 2.64949/1.21944,
    'QCD' : 3, # FIX ME
    # All Higgs scalings are for 125 GeV only.  VH = WH
    'VH' : 1.504/0.6966,
    'qqH' : 4.180/1.578,
    'ggH' : 49.85/19.52,
}

def walk_and_scale(inputdir, outputdir, scale_map):
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
        path = inputdir.GetPath().split(':')[1]
        for histo in histos:
            th1 = inputdir.Get(histo).Clone()
            if th1.GetName() in scale_map:
                print "Scaling", os.path.join(path,th1.GetName())
                th1.Scale(scale_map[th1.GetName()])
            outputdir.cd()
            th1.Write()

        # Now copy and recurse into subdirectories
        for subdir in directories:
            output_subdir = outputdir.mkdir(subdir)
            # Recurse
            walk_and_scale(inputdir.Get(subdir), output_subdir, scale_map)

def main(inputfilename, outputfilename, scale_map):
    input = ROOT.TFile(inputfilename, 'READ')
    if not input:
        raise IOError("Can't open input file: %s" % inputfilename)
    output = ROOT.TFile(outputfilename, 'RECREATE')
    if not output:
        raise IOError("Can't open output file: %s" % outputfilename)
    walk_and_scale(input, output, scale_map)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'scaling', nargs='+', metavar='PROC=CARDPROC1,CARDPROC2', type=str,
        help='List of PROCESS=CARDPROC pairs.  PROCESS should be one of:'
        'Z, W, tt, WZ, WW, ZZ, QCD, VH, qqH, ggH, and BINS should be a comma'
        ' separated (no spaces) list of processes in the datacard corresponding'
        ' to that physics process.'
    )

    parser.add_argument( '-i', metavar='INPUTFILE',
        help = 'Input .root file.')

    parser.add_argument( '-o', metavar='OUTPUTFILE',
        help = 'Output .root file.')

    args = parser.parse_args()

    import ROOT

    # build scale mapping
    scale_map = {}
    for scale in args.scaling:
        physics_process = scale.split('=')[0]
        card_processes = scale.split('=')[1].split(',')

        for proc in card_processes:
            print "%s => x %0.2f" % (proc, _SCALE_FACTORS[physics_process])
            scale_map[proc] = _SCALE_FACTORS[physics_process]

    main(args.i, args.o, scale_map)
