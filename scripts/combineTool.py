#!/usr/bin/env python

import argparse
import os
import re
import sys
import json
import math
import itertools
import stat
import glob
from array import array
from multiprocessing import Pool
import HiggsAnalysis.HiggsToTauTau.combine.utils as utils
from HiggsAnalysis.HiggsToTauTau.combine.opts import OPTS

from HiggsAnalysis.HiggsToTauTau.combine.base import CombineToolBase
from HiggsAnalysis.HiggsToTauTau.combine.enhanced import EnhancedCombine
from HiggsAnalysis.HiggsToTauTau.combine.impacts import Impacts

class PrintWorkspace(CombineToolBase):
    description = 'Load a Workspace and call Print()'
    requires_root = True

    def __init__(self):
        CombineToolBase.__init__(self)

    def attach_args(self, group):
        CombineToolBase.attach_args(self, group)
        group.add_argument('input', help='The input specified as FILE:WORKSPACE')

    def run_method(self):
        ws_in = args.input.split(':')
        f  = ROOT.TFile(ws_in[0])
        ws = f.Get(ws_in[1])
        ws.Print()

# class PrintSingles(SpecialCombine):
#   description = 'Print the output of MultimDitFit --algo singles'
#   requires_root = True
#   def __init__(self):
#     SpecialCombine.__init__(self)
#   def attach_args(self, group):
#     group.add_argument('input', help='The input file')
#     group.add_argument('-P', '--POIs', help='The params that were scanned (in scan order)')
#   def run_method(self):
#     POIs = args.POIs.split(',')
#     res = get_singles_results(args.input, POIs, POIs)
#     for p in POIs:
#       val = res[p][p]
#       print '%s = %.3f -%.3f/+%.3f' % (p, val[1], val[1] - val[0], val[2] - val[1])


# class RenameDataSet(SpecialCombine):
#   description = 'Change the name of a dataset in an existing workspace' 
#   requires_root = True
#   def __init__(self):
#     SpecialCombine.__init__(self)
#   def attach_args(self, group):
#     group.add_argument('input', help='The input specified as FILE:WORKSPACE:DATASET or FILE:WORKSPACE')
#     group.add_argument('output', help='The output specified as FILE:WORKSPACE:DATASET or FILE:WORKSPACE')
#     group.add_argument('-d','--data', help='Source data from other file, either FILE:WORKSPACE:DATA or FILE:DATA')
#   def run_method(self):
#     ws_in = args.input.split(':')
#     print '>> Input:  ' + str(ws_in)
#     ws_out = args.output.split(':')
#     print '>> Output: ' + str(ws_out)
#     f = ROOT.TFile(ws_in[0])
#     ws = f.Get(ws_in[1])
#     if len(ws_in) == 3:
#       data = ws.data(ws_in[2])
#     else:
#       ws_d = args.data.split(':')
#       print '>> Data: ' + str(ws_d)
#       f_d = ROOT.TFile(ws_d[0])
#       if len(ws_d) == 2:
#         data = f_d.Get(ws_d[1])
#       else:
#         data = f_d.Get(ws_d[1]).data(ws_d[2])
#       getattr(ws,'import')(data)
#     ws.SetName(ws_out[1])
#     if len(ws_out) == 3:
#       data.SetName(ws_out[2])
#     ws.writeToFile(ws_out[0])


# class CovMatrix(SpecialCombine):
#   description = 'Build a fit covariance matrix from scan results'
#   requires_root = True
#   def m_init__(self):
#     SpecialCombine.__init__(self)
#   def attach_args(self, group):
#     group.add_argument('-i', '--input', nargs='+', default=[], help='The input file containing the MultiDimFit singles mode output')
#     group.add_argument('-o', '--output', help='The output name in the format file:prefix')
#     group.add_argument('-P', '--POIs', help='The params that were scanned (in scan order)')
#     group.add_argument('--POIs-from-set', help='Extract from file:workspace:set instead')
#     group.add_argument('--compare', help='Compare to RooFitResult')
#   def run_method(self):
#     POIs = [] 
#     if args.POIs is not None:
#       POIs = args.POIs.split(',')
#     if args.POIs_from_set is not None:
#       ws_in = args.POIs_from_set.split(':')
#       print ws_in
#       POIs = list_from_workspace(ws_in[0], ws_in[1], ws_in[2])
#     # res = { }
#     # if len(args.input) == 1:
#     #   res.update(get_singles_results(args.input, POIs, POIs))
#     # elif len(args.input) > 1:
#     #   assert len(args.input) == len(POIs)
#     #   for i in range(len(POIs)):
#     #     res.update(get_singles_results(args.input[i], [POIs[i]], POIs))
#     # for p in POIs:
#     #   val = res[p][p]
#     #   print '%s = %.3f -%.3f/+%.3f' % (p, val[1], val[1] - val[0], val[2] - val[1])
#     # print res
#     # cor = ROOT.TMatrixDSym(len(POIs))
#     # cov = ROOT.TMatrixDSym(len(POIs))
#     # for i,p in enumerate(POIs):
#     #   cor[i][i] = ROOT.Double(1.) # diagonal correlation is 1 
#     #   cov[i][i] = ROOT.Double(pow((res[p][p][2] - res[p][p][0])/2.,2.)) # symmetrized error
#     # for i,ip in enumerate(POIs):
#     #   for j,jp in enumerate(POIs):
#     #     if i == j: continue
#     #     val_i = ((res[ip][jp][2] - res[ip][jp][0])/2.)/math.sqrt(cov[j][j])
#     #     val_j = ((res[jp][ip][2] - res[jp][ip][0])/2.)/math.sqrt(cov[i][i])
#     #     correlation = (val_i+val_j)/2. # take average correlation?
#     #     #correlation = min(val_i,val_j, key=abs) # take the max?
#     #     cor[i][j] = correlation
#     #     cor[j][i] = correlation
#     #     covariance = correlation * math.sqrt(cov[i][i]) * math.sqrt(cov[j][j])
#     #     cov[i][j] = covariance
#     #     cov[j][i] = covariance
#     compare = args.compare is not None
#     if compare:
#       f_in = args.compare.split(':')
#       f = ROOT.TFile(f_in[0])
#       fitres = f.Get(f_in[1])
#       fitres_cov = ROOT.TMatrixDSym(len(POIs))
#       fitres_cov_src = fitres.covarianceMatrix()
#       fitres_cor = ROOT.TMatrixDSym(len(POIs))
#       fitres_cor_src = fitres.correlationMatrix()
#       ipos = []
#       for p in POIs:
#         ipos.append(fitres.floatParsFinal().index(p))
#       for i,ip in enumerate(POIs):
#         for j,jp in enumerate(POIs):
#           fitres_cor[i][j] = ROOT.Double(fitres_cor_src[ipos[i]][ipos[j]])
#           fitres_cov[i][j] = ROOT.Double(fitres_cov_src[ipos[i]][ipos[j]])
#     # print 'My correlation matrix:'
#     # cor.Print()
#     if compare:
#       print 'RooFitResult correlation matrix:'
#       fitres_cor.Print()
#     # print 'My covariance matrix:'
#     # cov.Print()
#     if compare:
#       print 'RooFitResult covariance matrix:'
#       fitres_cov.Print()
#     if args.output is not None:
#       out = args.output.split(':')
#       fout = ROOT.TFile(out[0], 'RECREATE')
#       prefix = out[1]
#       # fout.WriteTObject(cor, prefix+'_cor')
#       # h_cor = self.fix_TH2(ROOT.TH2D(cor), POIs)
#       # fout.WriteTObject(h_cor, prefix+'_h_cor')
#       # fout.WriteTObject(cov, prefix+'_cov')
#       # h_cov = self.fix_TH2(ROOT.TH2D(cov), POIs)
#       # fout.WriteTObject(h_cov, prefix+'_h_cov')
#       if compare:
#         fout.WriteTObject(fitres_cor, prefix+'_comp_cor')
#         h_cor_compare = self.fix_TH2(ROOT.TH2D(fitres_cor), POIs)
#         fout.WriteTObject(h_cor_compare, prefix+'_comp_h_cor')
#         fout.WriteTObject(fitres_cov, prefix+'_comp_cov')
#         h_cov_compare = self.fix_TH2(ROOT.TH2D(fitres_cov), POIs)
#         fout.WriteTObject(h_cov_compare, prefix+'_comp_h_cov')
#   def fix_TH2(self, h, labels):
#     h_fix = h.Clone()
#     for y in range(1, h.GetNbinsY()+1):
#       for x in range(1, h.GetNbinsX()+1):
#         h_fix.SetBinContent(x, y, h.GetBinContent(x, h.GetNbinsY() + 1 - y))
#     for x in range(1, h_fix.GetNbinsX()+1):
#       h_fix.GetXaxis().SetBinLabel(x, labels[x-1])
#     for y in range(1, h_fix.GetNbinsY()+1):
#       h_fix.GetYaxis().SetBinLabel(y, labels[-y])
#     return h_fix


class AsymptoticGrid(CombineToolBase):
  description = 'Calculate asymptotic limits on parameter grids' 
  requires_root = True

  def __init__(self):
    CombineToolBase.__init__(self)

  def attach_intercept_args(self, group):
    CombineToolBase.attach_intercept_args(self, group)

  def attach_args(self, group):
    CombineToolBase.attach_args(self, group)
    group.add_argument('config', help='json config file')

  def run_method(self):
    # Step 1 - open the json config file
    with open(self.args.config) as json_file:    
        cfg = json.load(json_file)
    # to do - have to handle the case where it doesn't exist
    points = []
    for igrid in cfg['grids']:
      assert(len(igrid) == 2)
      points.extend(itertools.product(utils.split_vals(igrid[0]), utils.split_vals(igrid[1])))

    POIs = cfg['POIs']

    file_dict = { }
    for p in points:
      file_dict[p] = []

    for f in glob.glob('higgsCombine.%s.*.%s.*.Asymptotic.mH*.root' % (POIs[0], POIs[1])):
      # print f
      rgx = re.compile('higgsCombine\.%s\.(?P<p1>.*)\.%s\.(?P<p2>.*)\.Asymptotic\.mH.*\.root' % (POIs[0], POIs[1]))
      matches = rgx.search(f)
      p = (matches.group('p1'), matches.group('p2'))
      if p in file_dict:
        file_dict[p].append(f)

    for key,val in file_dict.iteritems():
      name = '%s.%s.%s.%s' % (POIs[0], key[0], POIs[1], key[1])
      print '>> Point %s' % name
      if len(val) == 0:
        print 'Going to run limit for point %s' % (key,)
        point_args = '-n .%s --setPhysicsModelParameters %s=%s,%s=%s --freezeNuisances %s,%s' % (name, POIs[0], key[0], POIs[1], key[1], POIs[0], POIs[1])
        cmd = ' '.join(['combine -M Asymptotic', cfg['opts'], point_args] + self.passthru)
        self.job_queue.append(cmd)

    bail_out = len(self.job_queue) > 0
    self.flush_queue()

    if bail_out: 
        print ">> New jobs were created / run in this cycle, run the script again to collect the output"
        sys.exit(0)

    xvals = []
    yvals = []
    zvals = []
    for key,val in file_dict.iteritems():
      for filename in val:
        fin = ROOT.TFile(filename)
        if fin.IsZombie(): continue
        tree = fin.Get('limit')
        for evt in tree:
          if evt.quantileExpected == -1:
            print 'At point %s have observed CLs = %f' % (key, evt.limit)
            xvals.append(float(key[0]))
            yvals.append(float(key[1]))
            zvals.append(float(evt.limit))
    graph = ROOT.TGraph2D(len(zvals), array('d', xvals), array('d', yvals), array('d', zvals))
    h_bins = cfg['hist_binning']
    hist = ROOT.TH2F('h_observed', '', h_bins[0], h_bins[1], h_bins[2], h_bins[3], h_bins[4], h_bins[5])
    for i in xrange(1, hist.GetNbinsX()+1):
      for j in xrange(1, hist.GetNbinsY()+1):
        hist.SetBinContent(i, j, graph.Interpolate(hist.GetXaxis().GetBinCenter(i), hist.GetYaxis().GetBinCenter(j)))
    fout = ROOT.TFile('asymptotic_grid.root', 'RECREATE')
    fout.WriteTObject(graph, 'observed')
    fout.WriteTObject(hist)
    fout.Close()
    # Next step: open output files
    # Fill TGraph2D with CLs, CLs+b

class CollectLimits(CombineToolBase):
    description = 'Aggregate limit output from combine' 
    requires_root = True

    def __init__(self):
        CombineToolBase.__init__(self)

    def attach_args(self, group):
        CombineToolBase.attach_args(self, group)
        group.add_argument('-i', '--input', nargs='+', default=[], help='The input files')
        group.add_argument('-o', '--output', help='The name of the output json file')

    def run_method(self):
        js_out = {}
        for filename in self.args.input:
            file = ROOT.TFile(filename)
            if file.IsZombie(): continue
            tree = file.Get('limit')
            for evt in tree:
                mh = str(evt.mh)
                if mh not in js_out: js_out[mh] = {}
                if evt.quantileExpected == -1:
                    js_out[mh]['observed'] = evt.limit
                elif abs(evt.quantileExpected - 0.5) < 1E-4:
                    js_out[mh]["expected"] = evt.limit
                elif abs(evt.quantileExpected - 0.025) < 1E-4:
                    js_out[mh]["-2"] = evt.limit
                elif abs(evt.quantileExpected - 0.160) < 1E-4:
                    js_out[mh]["-1"] = evt.limit
                elif abs(evt.quantileExpected - 0.840) < 1E-4:
                    js_out[mh]["+1"] = evt.limit
                elif abs(evt.quantileExpected - 0.975) < 1E-4:
                    js_out[mh]["+2"] = evt.limit
        # print js_out
        jsondata = json.dumps(js_out, sort_keys=True, indent=2, separators=(',', ': '))
        print jsondata
        if self.args.output is not None:
          with open(args.output, 'w') as out_file:
            out_file.write(jsondata)



def register_method(parser, method_dict, method_class):
  class_name = method_class.__name__
  parser.description += '  %-20s : %s\n' % (class_name, method_class.description)
  method_dict[class_name] = method_class
  
parser = argparse.ArgumentParser(
    prog='combineTool.py',
    add_help=False,
    formatter_class=argparse.RawDescriptionHelpFormatter
    )

parser.description = 'Available methods:\n\n'
methods = {}
# register_method(parser, methods, CombineToolBase)
# register_method(parser, methods, EnhancedCombine)
register_method(parser, methods, PrintWorkspace)
# register_method(parser, methods, RenameDataSet)
register_method(parser, methods, Impacts)
register_method(parser, methods, CollectLimits)
# register_method(parser, methods, CovMatrix)
# register_method(parser, methods, PrintSingles)
register_method(parser, methods, AsymptoticGrid)

parser.add_argument('-M', '--method')
# parser.add_argument('--dry-run', action='store_true', help='Commands are echoed to the screen but not run')
# parser.add_argument('--gen-job', action='store_true', help='Commands are echoed to the screen but not run')


(args, unknown) = parser.parse_known_args()

# if args.method is None:
#   parser.print_help()
#   sys.exit(0)

# DRY_RUN = args.dry_run

method = methods[args.method]() if args.method in methods else EnhancedCombine()

# Importing ROOT is quite slow, so only import if the chosen method requires it
if method.__class__.requires_root:
  print 'Importing ROOT'
  import ROOT
  ROOT.PyConfig.IgnoreCommandLineOptions = True
  ROOT.gSystem.Load('libHiggsAnalysisCombinedLimit')

# One group of options that are specific to the chosen method 
tool_group = parser.add_argument_group('%s options' % method.__class__.__name__, 'options specific to this method')
# And another group for combine options that will be intercepted 
intercept_group = parser.add_argument_group('combine options', 'standard combine options that will be re-interpreted')

# Let the chosen method create the arguments in both groups
method.attach_intercept_args(intercept_group)
method.attach_args(tool_group)

# Now we can add the normal help option
parser.add_argument('-h', '--help', action='help')
 
(args, unknown) = parser.parse_known_args()

# Print these for debugging
#print args
#print unknown

method.set_args(args, unknown)
method.run_method()



