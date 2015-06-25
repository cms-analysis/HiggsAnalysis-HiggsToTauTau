#!/usr/bin/env python

import argparse
import os
import re
import sys
import json
import math

OPTS = {
  'vanilla' : '--minimizerStrategy 0 --minimizerTolerance 0.1 --cminOldRobustMinimize 0',
  'prefitAsimovSToy' : '-M GenerateOnly --expectSignal 1 -t -1 --saveToys --saveWorkspace --noMCbonly 1',
  'prefitAsimovBToy' : '-M GenerateOnly --expectSignal 0 -t -1 --saveToys --saveWorkspace --noMCbonly 1',
  'robust' :    '--robustFit 1 --minimizerTolerance 0.1 --minimizerAlgo Minuit2 --minimizerStrategy 0 --minimizerAlgoForMinos Minuit2 --minimizerStrategyForMinos 0 --cminPreScan --cminPreFit 1 --X-rtd FITTER_DYN_STEP --cminFallbackAlgo "Minuit2,0:0.1" --cminFallbackAlgo "Minuit2,Minimize,0:0.1" --cminOldRobustMinimize 0',
  'robustL' :    '--robustFit 1 --minimizerTolerance 0.1 --minimizerAlgo Minuit2 --minimizerStrategy 0 --minimizerAlgoForMinos Minuit2 --minimizerStrategyForMinos 0 --cminPreScan --cminPreFit 1 --X-rtd FITTER_DYN_STEP --cminFallbackAlgo "Minuit2,0:0.1" --cminFallbackAlgo "Minuit2,Minimize,0:0.1" --cminOldRobustMinimize 0 --minimizerToleranceForMinos 0.001',
  'robustNew' : '--robustFit 1 --minimizerTolerance 0.1 --minimizerAlgo Minuit2 --minimizerStrategy 0 --minimizerAlgoForMinos Minuit2 --minimizerStrategyForMinos 0 --cminPreScan --cminPreFit 1 --cminFallbackAlgo "Minuit2,0:0.1" --cminFallbackAlgo "Minuit2,Minimize,0:0.1" --cminOldRobustMinimize 0 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --minimizerToleranceForMinos 0.1',
  'MLHesse': '--minimizerTolerance 0.1 --minimizerAlgo Minuit2 --minimizerStrategy 0 --cminFallbackAlgo "Minuit2,0:0.1" --cminFallbackAlgo "Minuit2,Minimize,0:0.1" --cminOldRobustMinimize 0 --out ./ --minos none --skipBOnlyFit --noMCbonly 1 --cminPreScan'
}

DRY_RUN=False


def run(command):
  print command
  if not DRY_RUN: return os.system(command)

def split_vals(vals):
  res = set()
  first = vals.split(',')
  for f in first:
    second = re.split('[:|]', f)
    print second
    if len(second) == 1: res.add(second[0])
    if len(second) == 3:
      x1 = float(second[0])
      ndigs = '0'
      split_step = second[2].split('.')
      if len(split_step) == 2:
        ndigs = len(split_step[1])
      fmt = '%.'+str(ndigs)+'f'
      while x1 < float(second[1]) + 0.001:
        res.add(fmt % x1)
        x1 += float(second[2])
  return sorted([x for x in res], key = lambda x : float(x))

def list_from_workspace(file, workspace, set):
  res = []
  wsFile = ROOT.TFile(file)
  argSet = wsFile.Get(workspace).set(set)
  it = argSet.createIterator()
  var = it.Next()
  while var:
    #var.Print()
    res.append(var.GetName())
    var = it.Next()
  return res

def get_singles_results(file, scanned, columns):
  res = { }
  f = ROOT.TFile(file)
  if f is None or f.IsZombie(): return None
  t = f.Get("limit")
  for i,param in enumerate(scanned): 
    res[param] = { }
    for col in columns:
      allvals = [getattr(evt, col) for evt in t]
      res[param][col] = [allvals[i*2+2], allvals[0], allvals[i*2+1]]
  return res

class BasicCombine:
  description = 'Just passes options through to combine with special treatment for a few args'
  requires_root = False
  def __init__(self):
    pass
  def attach_intercept_args(self, group):
    group.add_argument('-m', '--mass')
  def attach_args(self, group):
    group.add_argument('--opts', nargs='+', default=[], help='Add preset combine option groups')
  def set_args(self, known, unknown):
    self.args = known
    self.passthru = unknown
    if hasattr(args, 'opts'):
      for opt in args.opts:
        self.passthru.append(OPTS[opt])
  def run_method(self):
    if hasattr(self.args, 'method'):
      self.passthru = ['-M', self.args.method] + self.passthru
      del self.args.method
    taskqueue = []
    if self.args.mass is not None:
      mass_vals = split_vals(self.args.mass)
      for m in mass_vals:
        taskqueue.append('combine %s -m %s' % (' '.join(self.passthru), m))
    else:
      taskqueue.append('combine %s' % (' '.join(self.passthru)))
    for task in taskqueue:
      run(task)


class SpecialCombine(BasicCombine):
  def __init__(self):
    BasicCombine.__init__(self)
  def attach_intercept_args(self, group):
    pass    
  def attach_args(self, group):
    BasicCombine.attach_args(self, group)
  def run_method(self):
    pass

class PrintWorkspace(SpecialCombine):
  description = 'Load a Workspace and call Print()'
  requires_root = True
  def __init__(self):
    SpecialCombine.__init__(self)
  def attach_args(self, group):
    group.add_argument('input', help='The input specified as FILE:WORKSPACE')
    ws_in = args.input.split(':')
    f  = ROOT.TFile(ws_in[0])
    ws = f.Get(ws_in[1])
    ws.Print()

class PrintSingles(SpecialCombine):
  description = 'Print the output of MultimDitFit --algo singles'
  requires_root = True
  def __init__(self):
    SpecialCombine.__init__(self)
  def attach_args(self, group):
    group.add_argument('input', help='The input file')
    group.add_argument('-P', '--POIs', help='The params that were scanned (in scan order)')
  def run_method(self):
    POIs = args.POIs.split(',')
    res = get_singles_results(args.input, POIs, POIs)
    for p in POIs:
      val = res[p][p]
      print '%s = %.3f -%.3f/+%.3f' % (p, val[1], val[1] - val[0], val[2] - val[1])


class RenameDataSet(SpecialCombine):
  description = 'Change the name of a dataset in an existing workspace' 
  requires_root = True
  def __init__(self):
    SpecialCombine.__init__(self)
  def attach_args(self, group):
    group.add_argument('input', help='The input specified as FILE:WORKSPACE:DATASET or FILE:WORKSPACE')
    group.add_argument('output', help='The output specified as FILE:WORKSPACE:DATASET or FILE:WORKSPACE')
    group.add_argument('-d','--data', help='Source data from other file, either FILE:WORKSPACE:DATA or FILE:DATA')
  def run_method(self):
    ws_in = args.input.split(':')
    print '>> Input:  ' + str(ws_in)
    ws_out = args.output.split(':')
    print '>> Output: ' + str(ws_out)
    f = ROOT.TFile(ws_in[0])
    ws = f.Get(ws_in[1])
    if len(ws_in) == 3:
      data = ws.data(ws_in[2])
    else:
      ws_d = args.data.split(':')
      print '>> Data: ' + str(ws_d)
      f_d = ROOT.TFile(ws_d[0])
      if len(ws_d) == 2:
        data = f_d.Get(ws_d[1])
      else:
        data = f_d.Get(ws_d[1]).data(ws_d[2])
      getattr(ws,'import')(data)
    ws.SetName(ws_out[1])
    if len(ws_out) == 3:
      data.SetName(ws_out[2])
    ws.writeToFile(ws_out[0])


class CovMatrix(SpecialCombine):
  description = 'Build a fit covariance matrix from scan results'
  requires_root = True
  def m_init__(self):
    SpecialCombine.__init__(self)
  def attach_args(self, group):
    group.add_argument('-i', '--input', help='The input file containing the MultiDimFit singles mode output')
    group.add_argument('-o', '--output', help='The output name in the format file:prefix')
    group.add_argument('-P', '--POIs', help='The params that were scanned (in scan order)')
    group.add_argument('--POIs-from-set', help='Extract from file:workspace:set instead')
    group.add_argument('--compare', help='Compare to RooFitResult')
  def run_method(self):
    POIs = [] 
    if args.POIs is not None:
      POIs = args.POIs.split(',')
    if args.POIs_from_set is not None:
      ws_in = args.POIs_from_set.split(':')
      print ws_in
      POIs = list_from_workspace(ws_in[0], ws_in[1], ws_in[2])

    res = get_singles_results(args.input, POIs, POIs)
    cor = ROOT.TMatrixDSym(len(POIs))
    cov = ROOT.TMatrixDSym(len(POIs))
    for i,p in enumerate(POIs):
      cor[i][i] = ROOT.Double(1.) # diagonal correlation is 1 
      cov[i][i] = ROOT.Double(pow((res[p][p][2] - res[p][p][0])/2.,2.)) # symmetrized error
    for i,ip in enumerate(POIs):
      for j,jp in enumerate(POIs):
        if i == j: continue
        val_i = ((res[ip][jp][2] - res[ip][jp][0])/2.)/math.sqrt(cov[j][j])
        val_j = ((res[jp][ip][2] - res[jp][ip][0])/2.)/math.sqrt(cov[i][i])
        correlation = (val_i+val_j)/2. # take average correlation?
        #correlation = min(val_i,val_j, key=abs) # take the max?
        cor[i][j] = correlation
        cor[j][i] = correlation
        covariance = correlation * math.sqrt(cov[i][i]) * math.sqrt(cov[j][j])
        cov[i][j] = covariance
        cov[j][i] = covariance
    if args.compare is not None:
      f_in = args.compare.split(':')
      f = ROOT.TFile(f_in[0])
      fitres = f.Get(f_in[1])
      fitres_cov = ROOT.TMatrixDSym(len(POIs))
      fitres_cov_src = fitres.covarianceMatrix()
      fitres_cor = ROOT.TMatrixDSym(len(POIs))
      fitres_cor_src = fitres.correlationMatrix()
      ipos = []
      for p in POIs:
        ipos.append(fitres.floatParsFinal().index(p))
      for i,ip in enumerate(POIs):
        for j,jp in enumerate(POIs):
          fitres_cor[i][j] = ROOT.Double(fitres_cor_src[ipos[i]][ipos[j]])
          fitres_cov[i][j] = ROOT.Double(fitres_cov_src[ipos[i]][ipos[j]])
    print 'My correlation matrix:'
    cor.Print()
    if args.compare is not None:
      print 'RooFitResult correlation matrix:'
      fitres_cor.Print()
    print 'My covariance matrix:'
    cov.Print()
    if args.compare is not None:
      print 'RooFitResult covariance matrix:'
      fitres_cov.Print()
    if args.output is not None:
      out = args.output.split(':')
      fout = ROOT.TFile(out[0], 'RECREATE')
      prefix = out[1]
      fout.WriteTObject(cor, prefix+'_cor')
      h_cor = self.fix_TH2(ROOT.TH2D(cor), POIs)
      fout.WriteTObject(h_cor, prefix+'_h_cor')
      fout.WriteTObject(cov, prefix+'_cov')
      h_cov = self.fix_TH2(ROOT.TH2D(cov), POIs)
      fout.WriteTObject(h_cov, prefix+'_h_cov')
  def fix_TH2(self, h, labels):
    h_fix = h.Clone()
    for y in range(1, h.GetNbinsY()+1):
      for x in range(1, h.GetNbinsX()+1):
        h_fix.SetBinContent(x, y, h.GetBinContent(x, h.GetNbinsY() + 1 - y))
    for x in range(1, h_fix.GetNbinsX()+1):
      h_fix.GetXaxis().SetBinLabel(x, labels[x-1])
    for y in range(1, h_fix.GetNbinsY()+1):
      h_fix.GetYaxis().SetBinLabel(y, labels[-y])
    return h_fix

      



class Impacts(SpecialCombine):
  description = 'Calculate nuisance parameter impacts' 
  requires_root = True
  def __init__(self):
    SpecialCombine.__init__(self)
  def attach_intercept_args(self, group):
    group.add_argument('-m', '--mass', required=True)
    group.add_argument('-d', '--datacard', required=True)
  def attach_args(self, group):
    SpecialCombine.attach_args(self, group)
    group.add_argument('--offset', default=0, type=int,
        help='Start the loop over parameters with this offset (default: %(default)s)')
    group.add_argument('--advance', default=1, type=int,
        help='Advance this many parameters each step in the loop (default: %(default)s')
    group.add_argument('--named', metavar='PARAM1,PARAM2,...',
        help=('By default the list of nuisance parameters will be loaded from the input workspace. '
              'Use this option to specify a different list'))
    group.add_argument('--doInitialFit', action='store_true',
        help=('Find the crossings of all the POIs. Must have the output from this before running with --doFits'))
    group.add_argument('--doFits', action='store_true',
        help=('Actually run the fits for the nuisance parameter impacts, otherwise just looks for the results'))
    group.add_argument('--output', '-o',
        help=('write output json to a file'))
  def run_method(self):
    offset      = self.args.offset
    advance     = self.args.advance
    passthru    = self.passthru 
    mh          = self.args.mass
    ws          = self.args.datacard
    named = []
    if args.named is not None:
      named = args.named.split(',')
    # Put intercepted args back
    passthru.extend(['-m', mh])
    passthru.extend(['-d', ws])
    pass_str = ' '.join(passthru)
    paramList = []
    if len(named) > 0:
      paramList = named
    else:
      paramList = list_from_workspace(ws, 'w', 'ModelConfig_NuisParams')
    poiList = list_from_workspace(ws, 'w', 'ModelConfig_POI')
    #print 'Have nuisance parameters: ' + str(paramList)
    print 'Have nuisance parameters: ' + str(len(paramList))
    print 'Have POIs: ' + str(poiList)
    poistr = ','.join(poiList)
    if args.doInitialFit:
      run('combine -M MultiDimFit -n _initialFit --algo singles --redefineSignalPOIs %(poistr)s %(pass_str)s --altCommit' % vars())
      sys.exit(0)
    initialRes = get_singles_results('higgsCombine_initialFit.MultiDimFit.mH%(mh)s.root' % vars(), poiList, poiList)
    res = { }
    res["POIs"] = []
    res["params"] = []
    for poi in poiList:
      res["POIs"].append({"name" : poi, "fit" : initialRes[poi][poi]})
    counter = offset
    missing = [ ]
    while counter < len(paramList):
      pres = { }
      param = paramList[counter]
      print 'Doing param ' + str(counter) + ': ' + param
      if args.doFits:
        run('combine -M MultiDimFit -n _paramFit_%(param)s --algo singles --redefineSignalPOIs %(param)s,%(poistr)s -P %(param)s --floatOtherPOIs 1 --saveInactivePOI 1 %(pass_str)s --altCommit' % vars())
      if not args.dry_run:
        paramScanRes = get_singles_results('higgsCombine_paramFit_%(param)s.MultiDimFit.mH%(mh)s.root' % vars(), [param], poiList + [param])
        if paramScanRes is None:
          missing.append((counter,param))
          counter = counter + advance
          continue
        pres.update({"name" : param, "fit" : paramScanRes[param][param]})
        for p in poiList:
          pres.update({p : paramScanRes[param][p], 'impact_'+p : (paramScanRes[param][p][2] - paramScanRes[param][p][0])/2.})
        res['params'].append(pres)
        counter = counter + advance
    jsondata = json.dumps(res, sort_keys=True, indent=2, separators=(',', ': '))
    print jsondata
    if args.output is not None:
      with open(args.output, 'w') as out_file:
        out_file.write(jsondata)
    if len(missing) > 0:
      print 'Missing inputs: ' + str(missing)

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
register_method(parser, methods, BasicCombine)
register_method(parser, methods, PrintWorkspace)
register_method(parser, methods, RenameDataSet)
register_method(parser, methods, Impacts)
register_method(parser, methods, CovMatrix)
register_method(parser, methods, PrintSingles)

parser.add_argument('-M', '--method')
parser.add_argument('--dry-run', action='store_true', help='Commands are echoed to the screen but not run')


(args, unknown) = parser.parse_known_args()

if args.method is None:
  parser.print_help()
  sys.exit(0)

DRY_RUN = args.dry_run

method = methods[args.method]() if args.method in methods else BasicCombine()

# Importing ROOT is quite slow, so only import if the chosen method requires it
if method.__class__.requires_root:
  #print 'Importing ROOT'
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



