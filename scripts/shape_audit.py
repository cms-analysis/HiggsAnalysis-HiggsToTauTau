#!/usr/bin/env python
'''

Generate a webpage showing the different shapes in the data card.

Author: Evan K. Friis

'''

from RecoLuminosity.LumiDB import argparse
import fnmatch
import os
import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat('111111111')

def walk(inputdir):
    ''' Recursive function which generates (path, subdirs, histos) '''
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
        path = inputdir.GetPath().split(':')[1]
        # Yield the stuff in this directory
    yield (path, tuple(directories), tuple(histos))
    # Now get the stuff in sub directories
    for directory in directories:
        for subresult in walk(inputdir.Get(directory)):
            yield subresult

def seperate_histos(histo_list, signal_pattern, err_pattern, exclude):
    ''' Separate histogram lists into backgrounds, shape_uncs, and signals '''
    signals = []
    shapes = []
    bkgs = []
    for x in histo_list:
        if 'obs' in x:
            continue
        if fnmatch.fnmatch(x, signal_pattern):
            signals.append(x)
        elif fnmatch.fnmatch(x, err_pattern):
            shapes.append(x)
        elif not fnmatch.fnmatch(x, exclude):
            bkgs.append(x)
    return (tuple(signals), tuple(shapes), tuple(bkgs))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input .root file')
    parser.add_argument('--output-dir', default='shape_audit',
                        dest='outputdir', help='Output directory')
    parser.add_argument('--signal-matcher', default='*H*0*',
                        dest='sigmatch',
                        help='Shell glob-style matcher for signal processes')
    parser.add_argument('--shape-unc-matcher', default='*CMS_*',
                        dest='shapematch',
                        help='Shell glob-style matcher for shape errors.  These shapes arent shown.')
    parser.add_argument('--exclude', default='*H*',
                        dest='exclude',
                        help="Exclude these shapes.  Shapes which match --signal-matcher are always shown")

    args = parser.parse_args()

    input_file = ROOT.TFile(args.input, 'READ')

    if not os.path.exists(args.outputdir):
        os.makedirs(args.outputdir)

    index_file = open(os.path.join(args.outputdir, 'index.html'), 'w')

    def writeln(x):
        index_file.write(x + '\n')

    writeln(r'<h1>Shape Audit</h1>' + '\n')
    writeln(r'<h3>%s</h3>' % args.input)

    canvas = ROOT.TCanvas("asdf", "asdf", 300, 300)

    for path, subdirs, histos in walk(input_file):
        path = path.replace('/', '', 1)
        if not histos:
            continue
        writeln('<hr>')
        writeln('<h4>%s</h4>' % path)

        signals, shape_errors, bkgs = seperate_histos(
            histos, args.sigmatch, args.shapematch, args.exclude)

        output_plot_dir = os.path.join(args.outputdir, path)
        if not os.path.exists(output_plot_dir):
            os.makedirs(output_plot_dir)

        for i, shape in enumerate(bkgs + signals):
            histo = input_file.Get(os.path.join(path, shape))
            histo.SetStats(True)
            histo.SetLineColor(ROOT.EColor.kBlack)
            # Different color for signals
            if shape in signals:
                histo.SetLineColor(ROOT.EColor.kAzure-3)
            histo.SetMarkerSize(0.5)
            histo.SetMarkerStyle(21)
            histo.SetLineStyle(0)
            histo.SetLineWidth(1)
            histo.SetFillStyle(0)
            pave = ROOT.TPaveText(0.7, 0.7, 0.9, 0.9, "brNDC")
            pave.SetBorderSize(0)
            pave.SetFillStyle(0)
            pave.AddText(shape)
            histo.Draw('hist,e')
            pave.Draw()
            plotfile = os.path.join(output_plot_dir, shape) + '.png'
            canvas.SaveAs(plotfile)
            writeln('<img src=%s/%s.png>' % (path, shape))
            if (i+1) % 3 == 0:
                writeln('<br>')

        writeln('<br>')
