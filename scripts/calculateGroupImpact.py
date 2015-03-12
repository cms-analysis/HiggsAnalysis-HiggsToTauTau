#!/usr/bin/env python
import fnmatch
import os
import ROOT
import sys
import math
from optparse import OptionParser
import numpy

def run(command):
  print command
  os.system(command)

def listFromWorkspace(file, workspace, set):
  res = []
  wsFile = ROOT.TFile(file)
  argSet = wsFile.Get(workspace).set(set)
  it = argSet.createIterator()
  var = it.Next()
  while var:
    res.append(var.GetName())
    var = it.Next()
  return res

def getScanResult(file, param):
  # print 'Getting scan result from file ' + file
  f = ROOT.TFile(file)
  t = f.Get("limit")
  valList = list({getattr(t, param) for evt in t})
  valList.sort()
  # assert len(valList) == 3
  # print valList
  return valList

def getSymUncert(vals):
  lo = vals[0]
  hi = vals[2]
  return abs((hi-lo)/2.)

def getDiff(before, after):
  if before > after:
    return math.sqrt(before*before - after*after)
  else:
    print 'PROBLEM: err before is ' + str(before) + ' and err after is ' + str(after)
    return -1.


usage = """
"""
parser = OptionParser(usage=usage)

parser.add_option("--ws", dest="ws", help="The input workspace")
parser.add_option("--poi", dest="targetParam", metavar="POI", default='r', help="The POI for which to calculate the nuisance parameter impact")
parser.add_option("--mH", dest="mH", default='125', help="The signal mass")
parser.add_option("--poiRange", dest="poiRange", default='0,2', help="Set the range for the POI")
parser.add_option("--groups", dest="groups", default=None, help="groups that should be frozen")
parser.add_option("--label", dest="label", default=None, help="label the output file")
parser.add_option("--doInitialFit", dest="doInitialFit", action='store_true', default=False,
                  help="Perform the initial fits for the POI (only needs to be done once)")
parser.add_option("--skipFits", dest="skipFits", action='store_true', default=False,
                  help="Skip all the nuisance parameter fits, just parse the output")
parser.add_option("--minimizerTolerance", dest="minimizerTolerance", type='float', default=0.01,
                  help="the minimizerTolerance passed to combine, use larger values for more complex models")

(options, args) = parser.parse_args()

ws = options.ws
doInitialFit = options.doInitialFit
targetParam = options.targetParam
poiRange = options.poiRange
mH = options.mH
minimizerTolerance = options.minimizerTolerance
groups = options.groups
skipFits = options.skipFits
label = options.label

baseOptions = (('-m %(mH)s --minimizerStrategy=0 --minimizerTolerance=%(minimizerTolerance)g'
      ' --cminFallbackAlgo "Minuit2,0:0.1" --cminFallbackAlgo "Minuit2,0:1." --cminPreScan'
      ' --setPhysicsModelParameterRanges %(targetParam)s=%(poiRange)s') % vars())

standardOptions = (baseOptions + (' --cminPreFit 1 --stepSize 0.05'
      ' --robustFit 1 --minimizerAlgoForMinos=Minuit2 --minimizerToleranceForMinos=%(minimizerTolerance)g'
      ' --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND') % vars())

ROOT.gSystem.Load('$CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit')

### Step 2 - establish global best fit and save post-fit snapshot
### Note when using saveWorkspace: the global observables will be set to whatever the final state of the NPs is,
### so if we run with algo 'singles' then these are not the best-fit values, but rather the values at the end of
### the crossing search alorithm
if doInitialFit:
  # run(('combine -M MultiDimFit -n _initialFit %(standardOptions)s'
  #      ' --saveWorkspace %(ws)s') % vars())
  run(('combine -M MultiDimFit -n _initialFitSingles %(standardOptions)s'
       ' --algo singles %(ws)s') % vars())
  run(('combine -M MultiDimFit -n _initialGrid %(baseOptions)s'
       ' --algo grid --points 100 %(ws)s') % vars())
  run(('combine -M MultiDimFit -n _initialFit %(standardOptions)s'
       ' --saveWorkspace %(ws)s') % vars())
initialRes = getScanResult('higgsCombine_initialFitSingles.MultiDimFit.mH%(mH)s.root' % vars(), targetParam)

if not skipFits:
  run(('combine -M MultiDimFit -n _frozen%(label)s %(standardOptions)s'
       ' --algo singles'
       ' -d higgsCombine_initialFit.MultiDimFit.mH%(mH)s.root -w w --snapshotName "MultiDimFit"'
       ' --freezeNuisanceGroups %(groups)s') % vars())
  run(('combine -M MultiDimFit -n _frozenGrid%(label)s %(baseOptions)s'
       ' --algo grid --points 100'
       ' -d higgsCombine_initialFit.MultiDimFit.mH%(mH)s.root -w w --snapshotName "MultiDimFit"'
       ' --freezeNuisanceGroups %(groups)s') % vars())
freezeRes = getScanResult('higgsCombine_frozen%(label)s.MultiDimFit.mH%(mH)s.root' % vars(), targetParam)


contribution = getDiff(getSymUncert(initialRes), getSymUncert(freezeRes))

print 'Best fit (observed):           %.5f +/- %.5f' % (initialRes[1], getSymUncert(initialRes))
print 'Best fit frozen (observed):    %.5f +/- %.5f' % (freezeRes[1], getSymUncert(freezeRes))
print 'Group %s contribution:  %.5f' % (label, contribution)
 
