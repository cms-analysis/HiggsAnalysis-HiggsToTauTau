#!/usr/bin/env python
import fnmatch
import os
import ROOT
import sys
import math
from optparse import OptionParser
import numpy

def run(command):
  # print command
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

This script will calculate the impact of each nuisance parameter on a particular POI.
The impact is defined as the shift in the POI value when going from the global best
fit of all parameters, to points where the nuisance parameter is fixed to its +/-1 sigma
values (the remaining parameters are profiled). A second calculation is performed in
which the total uncertainty on the POI (profiling all parameters) is compared to the
uncertainty in which the nuisance parameter is frozen to its best fit value. The
contribution of this parameter to the total uncertainty on the POI value is found by
subtracting the latter from the former in quadrature. Both calculations will be performed
for the observed data, a post-fit asimov and a pre-fit asimov dataset. 

Example usage:

Perform the initial fits for the POI

  calculateImpacts.py --ws workspace.root --mH 125 --poi r --poiRange -5,5 --doInitialFit

Then calculate the impacts for all nuisance parameters, results will be printed to the screen

  calculateImpacts.py --ws workspace.root --mH 125 --poi r --poiRange -5,5

For complex models where it is not feasible to calculate all impacts in one go, you can split
the task using the offset and advance options, e.g. to run in 4 jobs, submit 4 tasks:


  calculateImpacts.py --ws workspace.root --mH 125 --poi r --poiRange -5,5 --offset 0 --advance 4
  calculateImpacts.py --ws workspace.root --mH 125 --poi r --poiRange -5,5 --offset 1 --advance 4
  calculateImpacts.py --ws workspace.root --mH 125 --poi r --poiRange -5,5 --offset 2 --advance 4
  calculateImpacts.py --ws workspace.root --mH 125 --poi r --poiRange -5,5 --offset 3 --advance 4

Then to combine the results, and write the output to a TTree:

  calculateImpacts.py --ws workspace.root --mH 125 --poi r --poiRange -5,5 --skipFits --writeTree

WARNING: this script may not produce correct results for models with multiple POIs
"""
parser = OptionParser(usage=usage)

parser.add_option("--ws", dest="ws", help="The input workspace")
parser.add_option("--poi", dest="targetParam", metavar="POI", default='r', help="The POI for which to calculate the nuisance parameter impact")
parser.add_option("--mH", dest="mH", default='125', help="The signal mass")
parser.add_option("--poiRange", dest="poiRange", default='0,2', help="Set the range for the POI")
parser.add_option("--doInitialFit", dest="doInitialFit", action='store_true', default=False,
                  help="Perform the initial fits for the POI (only needs to be done once)")
parser.add_option("--skipFits", dest="skipFits", action='store_true', default=False,
                  help="Skip all the nuisance parameter fits, just parse the output")
parser.add_option("--writeTree", dest="writeTree", action='store_true', default=False,
                  help="Write output into a TTree")
parser.add_option("--offset", dest="offset", type='int', default=0,
                  help="initial parameter count offset")
parser.add_option("--advance", dest="advance", type='int', default=1,
                  help="number of params to advance in each step")
parser.add_option("--minimizerTolerance", dest="minimizerTolerance", type='float', default=0.01,
                  help="the minimizerTolerance passed to combine, use larger values for more complex models")

(options, args) = parser.parse_args()

ws = options.ws
doInitialFit = options.doInitialFit
skipFits = options.skipFits
writeTree = options.writeTree
targetParam = options.targetParam
poiRange = options.poiRange
mH = options.mH
offset = options.offset
advance = options.advance
minimizerTolerance = options.minimizerTolerance

standardOptions = (('-v -1 -m %(mH)s --minimizerStrategy=0 --minimizerTolerance=%(minimizerTolerance)g'
      ' --cminFallbackAlgo "Minuit2,0:0.1" --cminFallbackAlgo "Minuit2,0:1."'
      ' --robustFit 1 --minimizerAlgoForMinos=Minuit2 --minimizerToleranceForMinos=%(minimizerTolerance)g'
      ' --setPhysicsModelParameterRanges %(targetParam)s=%(poiRange)s'
      ' --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND') % vars())

ROOT.gSystem.Load('$CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit')

resList = []

### Step 1 - get list of nuisance parameters
paramList = listFromWorkspace(ws, 'w', 'ModelConfig_NuisParams')

### Step 2 - establish global best fit and save post-fit snapshot
### Note when using saveWorkspace: the global observables will be set to whatever the final state of the NPs is,
### so if we run with algo 'singles' then these are not the best-fit values, but rather the values at the end of
### the crossing search alorithm
if doInitialFit:
  # run(('combine -M MultiDimFit -n _initialFit %(standardOptions)s'
  #      ' --saveWorkspace %(ws)s') % vars())
  run(('combine -M MultiDimFit -n _initialFitSingles %(standardOptions)s'
       ' --algo singles %(ws)s') % vars())
initialRes = getScanResult('higgsCombine_initialFitSingles.MultiDimFit.mH%(mH)s.root' % vars(), targetParam)

if doInitialFit:
  initialBestFit = initialRes[1]
  run(('combine -M MultiDimFit -n _initialFit_POST %(standardOptions)s'
       ' -t -1 --toysFrequentist --expectSignal %(initialBestFit)s --saveToys --saveWorkspace %(ws)s') % vars())
  run(('combine -M MultiDimFit -n _initialFitSingles_POST %(standardOptions)s'
       ' --algo singles -t -1 --toysFrequentist --expectSignal %(initialBestFit)s %(ws)s') % vars())
  run(('combine -M MultiDimFit -n _initialFit_PRE %(standardOptions)s'
       ' -t -1 --expectSignal 1 --saveToys --saveWorkspace %(ws)s') % vars())
  run(('combine -M MultiDimFit -n _initialFitSingles_PRE %(standardOptions)s'
       ' --algo singles -t -1 --expectSignal 1 %(ws)s') % vars())
  sys.exit()

initialPostRes = getScanResult('higgsCombine_initialFitSingles_POST.MultiDimFit.mH%(mH)s.root' % vars(), targetParam)
initialPreRes = getScanResult('higgsCombine_initialFitSingles_PRE.MultiDimFit.mH%(mH)s.root' % vars(), targetParam)

#paramList = paramList[0:4]

counter = offset
while counter < len(paramList):
  param = paramList[counter]
  print 'Doing param ' + str(counter) + ': ' + param
  paramRes = {"POI" : targetParam, "POI_best" : initialRes[1], "POI_lo" : initialRes[0], "POI_hi" : initialRes[2]}

  if not skipFits:
    ### Do the parameter scans
    run(('combine -M MultiDimFit  -n _paramFit_%(param)s'
         ' --algo singles --redefineSignalPOIs %(param)s %(standardOptions)s %(ws)s') % vars())

    run(('combine -M MultiDimFit -n _paramFit_%(param)s_POST'
         ' --algo singles -t -1 --toysFrequentist --bypassFrequentistFit'
         ' -d higgsCombine_initialFit_POST.MultiDimFit.mH%(mH)s.123456.root -w w --snapshotName "MultiDimFit"'
         ' --toysFile higgsCombine_initialFit_POST.MultiDimFit.mH%(mH)s.123456.root'
         ' --redefineSignalPOIs %(param)s %(standardOptions)s') % vars())

    run(('combine -M MultiDimFit -n _paramFit_%(param)s_PRE'
         ' --algo singles -t -1 --toysFrequentist --bypassFrequentistFit'
         ' -d higgsCombine_initialFit_PRE.MultiDimFit.mH%(mH)s.123456.root -w w --snapshotName "MultiDimFit"'
         ' --toysFile higgsCombine_initialFit_PRE.MultiDimFit.mH%(mH)s.123456.root'
         ' --redefineSignalPOIs %(param)s %(standardOptions)s') % vars())

  paramScanObsRes = getScanResult('higgsCombine_paramFit_%(param)s.MultiDimFit.mH125.root' % vars(), param)
  paramObsBestFit = paramScanObsRes[1]
  paramScanPostRes = getScanResult('higgsCombine_paramFit_%(param)s_POST.MultiDimFit.mH125.root' % vars(), param)
  paramScanPreRes = getScanResult('higgsCombine_paramFit_%(param)s_PRE.MultiDimFit.mH125.root' % vars(), param)

  if not skipFits:
    ### Do "frozen" parameter scans
    run(('combine -M MultiDimFit -n _frozen_%(param)s %(standardOptions)s'
         ' --algo singles --setPhysicsModelParameters %(param)s=%(paramObsBestFit)s --freezeNuisances %(param)s %(ws)s') % vars())

    run(('combine -M MultiDimFit -n _frozen_%(param)s_POST %(standardOptions)s'
         ' --algo singles -t -1 --toysFrequentist --bypassFrequentistFit'
         ' -d higgsCombine_initialFit_POST.MultiDimFit.mH%(mH)s.123456.root -w w --snapshotName "MultiDimFit"'
         ' --toysFile higgsCombine_initialFit_POST.MultiDimFit.mH%(mH)s.123456.root'
         ' --freezeNuisances %(param)s') % vars())

    run(('combine -M MultiDimFit -n _frozen_%(param)s_PRE %(standardOptions)s'
         ' --algo singles -t -1 --toysFrequentist --bypassFrequentistFit'
         ' -d higgsCombine_initialFit_PRE.MultiDimFit.mH%(mH)s.123456.root -w w --snapshotName "MultiDimFit"'
         ' --toysFile higgsCombine_initialFit_PRE.MultiDimFit.mH%(mH)s.123456.root'
         ' --freezeNuisances %(param)s') % vars())

  freezeScanObsRes = getScanResult('higgsCombine_frozen_%(param)s.MultiDimFit.mH%(mH)s.root' % vars(), targetParam)
  paramRes.update({"param" : param, "frozen" : getDiff(getSymUncert(initialRes), getSymUncert(freezeScanObsRes))})
  freezeScanPostRes = getScanResult('higgsCombine_frozen_%(param)s_POST.MultiDimFit.mH%(mH)s.root' % vars(), targetParam)
  paramRes.update({"frozen_post" : getDiff(getSymUncert(initialPostRes), getSymUncert(freezeScanPostRes))})
  freezeScanPreRes = getScanResult('higgsCombine_frozen_%(param)s_PRE.MultiDimFit.mH%(mH)s.root' % vars(), targetParam)
  paramRes.update({"frozen_pre" : getDiff(getSymUncert(initialPreRes), getSymUncert(freezeScanPreRes))})

  loVal = paramScanObsRes[0]
  hiVal = paramScanObsRes[2]
  loValPost = paramScanPostRes[0]
  hiValPost = paramScanPostRes[2]
  loValPre = paramScanPreRes[0]
  hiValPre = paramScanPreRes[2]

  if not skipFits:
    run(('combine -M MultiDimFit -n _lo_%(param)s'
         ' --setPhysicsModelParameters %(param)s=%(loVal)s --freezeNuisances %(param)s'
         ' %(standardOptions)s %(ws)s') % vars())
    run(('combine -M MultiDimFit -n _hi_%(param)s'
         ' --setPhysicsModelParameters %(param)s=%(hiVal)s --freezeNuisances %(param)s'
         ' %(standardOptions)s %(ws)s') % vars())

    run(('combine -M MultiDimFit -n _lo_%(param)s_POST --algo singles'
         ' -t -1 --toysFrequentist --bypassFrequentistFit'
         ' -d higgsCombine_initialFit_POST.MultiDimFit.mH%(mH)s.123456.root -w w --snapshotName "MultiDimFit"'
         ' --toysFile higgsCombine_initialFit_POST.MultiDimFit.mH%(mH)s.123456.root'
         ' --setPhysicsModelParameters %(param)s=%(loValPost)s --freezeNuisances %(param)s'
         ' %(standardOptions)s') % vars())
    run(('combine -M MultiDimFit -n _hi_%(param)s_POST --algo singles'
         ' -t -1 --toysFrequentist --bypassFrequentistFit'
         ' -d higgsCombine_initialFit_POST.MultiDimFit.mH%(mH)s.123456.root -w w --snapshotName "MultiDimFit"'
         ' --toysFile higgsCombine_initialFit_POST.MultiDimFit.mH%(mH)s.123456.root'
         ' --setPhysicsModelParameters %(param)s=%(hiValPost)s --freezeNuisances %(param)s'
         ' %(standardOptions)s') % vars())

    run(('combine -M MultiDimFit -n _lo_%(param)s_PRE --algo singles'
         ' -t -1 --toysFrequentist --bypassFrequentistFit'
         ' -d higgsCombine_initialFit_PRE.MultiDimFit.mH%(mH)s.123456.root -w w --snapshotName "MultiDimFit"'
         ' --toysFile higgsCombine_initialFit_PRE.MultiDimFit.mH%(mH)s.123456.root'
         ' --setPhysicsModelParameters %(param)s=%(loValPre)s --freezeNuisances %(param)s'
         ' %(standardOptions)s') % vars())
    run(('combine -M MultiDimFit -n _hi_%(param)s_PRE --algo singles'
         ' -t -1 --toysFrequentist --bypassFrequentistFit'
         ' -d higgsCombine_initialFit_PRE.MultiDimFit.mH%(mH)s.123456.root -w w --snapshotName "MultiDimFit"'
         ' --toysFile higgsCombine_initialFit_PRE.MultiDimFit.mH%(mH)s.123456.root'
         ' --setPhysicsModelParameters %(param)s=%(hiValPre)s --freezeNuisances %(param)s'
         ' %(standardOptions)s') % vars())

  loRes = getScanResult('higgsCombine_lo_%(param)s.MultiDimFit.mH125.root' % vars(), targetParam)
  hiRes = getScanResult('higgsCombine_hi_%(param)s.MultiDimFit.mH125.root' % vars(), targetParam)
  delta = abs(hiRes[0] - loRes[0]) / 2.
  paramRes.update({"param_best" : paramScanObsRes[1], "param_lo" : loVal, "param_hi" : hiVal, "impact" : delta})

  loResPost = getScanResult('higgsCombine_lo_%(param)s_POST.MultiDimFit.mH125.root' % vars(), targetParam)
  hiResPost = getScanResult('higgsCombine_hi_%(param)s_POST.MultiDimFit.mH125.root' % vars(), targetParam)
  deltaPost = abs(hiResPost[1] - loResPost[1]) / 2.
  paramRes.update({"param_best_post" : paramScanPostRes[1], "param_lo_post" : loValPost, "param_hi_post" : hiValPost, "impact_post" : deltaPost})

  loResPre = getScanResult('higgsCombine_lo_%(param)s_PRE.MultiDimFit.mH125.root' % vars(), targetParam)
  hiResPre = getScanResult('higgsCombine_hi_%(param)s_PRE.MultiDimFit.mH125.root' % vars(), targetParam)
  deltaPre = abs(hiResPre[1] - loResPre[1]) / 2.
  paramRes.update({"param_best_pre" : paramScanPreRes[1], "param_lo_pre" : loValPre, "param_hi_pre" : hiValPre, "impact_pre" : deltaPre})

  resList.append(paramRes)
  counter = counter + advance

sortedByFrozen = sorted(resList, key=lambda dict: dict['frozen'], reverse=True)
sortedByImpact = sorted(resList, key=lambda dict: dict['impact'], reverse=True)
sortedByFrozenPost = sorted(resList, key=lambda dict: dict['frozen_post'], reverse=True)
sortedByImpactPost = sorted(resList, key=lambda dict: dict['impact_post'], reverse=True)
sortedByFrozenPre = sorted(resList, key=lambda dict: dict['frozen_pre'], reverse=True)
sortedByImpactPre = sorted(resList, key=lambda dict: dict['impact_pre'], reverse=True)

posInFrozen = {}
for i,x in enumerate(sortedByFrozen):
  posInFrozen.update({x['param'] : i+1})
posInImpact = {}
for i,x in enumerate(sortedByImpact):
  posInImpact.update({x['param'] : i+1})

posInFrozenPost = {}
for i,x in enumerate(sortedByFrozenPost):
  posInFrozenPost.update({x['param'] : i+1})
posInImpactPost = {}
for i,x in enumerate(sortedByImpactPost):
  posInImpactPost.update({x['param'] : i+1})

posInFrozenPre = {}
for i,x in enumerate(sortedByFrozenPre):
  posInFrozenPre.update({x['param'] : i+1})
posInImpactPre = {}
for i,x in enumerate(sortedByImpactPre):
  posInImpactPre.update({x['param'] : i+1})

print 'Best fit for %s (observed):         %.5f +/- %.5f' % (targetParam, initialRes[1], getSymUncert(initialRes))
print 'Best fit for %s (post-fit asimov):  %.5f +/- %.5f' % (targetParam, initialPostRes[1], getSymUncert(initialPostRes))
print 'Best fit for %s (pre-fit asimov):   %.5f +/- %.5f' % (targetParam, initialPreRes[1], getSymUncert(initialPreRes))

resList.sort(key=lambda dict: dict['impact'], reverse=True)
print '%-70s %12s %6s | %12s %6s | %12s %6s | %12s %6s | %12s %6s | %12s %6s' % ('Parameter', 'impact', 'rank', 'impact_post', 'rank', 'impact_pre', 'rank', 'frozen', 'rank', 'frozen_post', 'rank', 'frozen_pre', 'rank')
for x in resList:
  print ('%-70s %12.5f %6i | %12.5f %6i | %12.5f %6i | %12.5f %6i | %12.5f %6i | %12.5f %6i' %
      (x['param'],
       x['impact'],      posInImpact[x['param']],
       x['impact_post'], posInImpactPost[x['param']],
       x['impact_pre'],  posInImpactPre[x['param']],
       x['frozen'],      posInFrozen[x['param']],
       x['frozen_post'], posInFrozenPost[x['param']],
       x['frozen_pre'],  posInFrozenPre[x['param']]))

if writeTree:
  f = ROOT.TFile('impact.root', 'recreate')
  t = ROOT.TTree('impact', 'impact')
  name = ROOT.TString()
  t_par_best        = numpy.zeros(1, dtype=float)
  t_par_lo          = numpy.zeros(1, dtype=float)
  t_par_hi          = numpy.zeros(1, dtype=float)
  t_par_best_post   = numpy.zeros(1, dtype=float)
  t_par_lo_post     = numpy.zeros(1, dtype=float)
  t_par_hi_post     = numpy.zeros(1, dtype=float)
  t_par_best_pre    = numpy.zeros(1, dtype=float)
  t_par_lo_pre      = numpy.zeros(1, dtype=float)
  t_par_hi_pre      = numpy.zeros(1, dtype=float)
  
  t_impact            = numpy.zeros(1, dtype=float)
  t_impact_post       = numpy.zeros(1, dtype=float)
  t_impact_pre        = numpy.zeros(1, dtype=float)
  t_frozen            = numpy.zeros(1, dtype=float)
  t_frozen_post       = numpy.zeros(1, dtype=float)
  t_frozen_pre        = numpy.zeros(1, dtype=float)
  t_rank_impact       = numpy.zeros(1, dtype=int)
  t_rank_impact_post  = numpy.zeros(1, dtype=int)
  t_rank_impact_pre   = numpy.zeros(1, dtype=int)
  t_rank_frozen       = numpy.zeros(1, dtype=int)
  t_rank_frozen_post  = numpy.zeros(1, dtype=int)
  t_rank_frozen_pre   = numpy.zeros(1, dtype=int)

  t.Branch("parameter", name)

  t.Branch('par_best',            t_par_best,          "par_best/D")
  t.Branch('par_lo',              t_par_lo,            "par_lo/D")
  t.Branch('par_hi',              t_par_hi,            "par_hi/D")
  t.Branch('par_best_post',       t_par_best_post,     "par_best_post/D")
  t.Branch('par_lo_post',         t_par_lo_post,       "par_lo_post/D")
  t.Branch('par_hi_post',         t_par_hi_post,       "par_hi_post/D")
  t.Branch('par_best_pre',        t_par_best_pre,      "par_best_pre/D")
  t.Branch('par_lo_pre',          t_par_lo_pre,        "par_lo_pre/D")
  t.Branch('par_hi_pre',          t_par_hi_pre,        "par_hi_pre/D")

  t.Branch('impact',            t_impact,             "impact/D")
  t.Branch('impact_post',       t_impact_post,        "impact_post/D")
  t.Branch('impact_pre',        t_impact_pre,         "impact_pre/D")
  t.Branch('frozen',            t_frozen,             "frozen/D")
  t.Branch('frozen_post',       t_frozen_post,        "frozen_post/D")
  t.Branch('frozen_pre',        t_frozen_pre,         "frozen_pre/D")
  t.Branch('rank_impact',       t_rank_impact,        "rank_impact/I")
  t.Branch('rank_impact_post',  t_rank_impact_post,   "rank_impact_post/I")
  t.Branch('rank_impact_pre',   t_rank_impact_pre,    "rank_impact_pre/I")
  t.Branch('rank_frozen',       t_rank_frozen,        "rank_frozen/I")
  t.Branch('rank_frozen_post',  t_rank_frozen_post,   "rank_frozen_post/I")
  t.Branch('rank_frozen_pre',   t_rank_frozen_pre,    "rank_frozen_pre/I")

  for x in resList:
    name.Resize(0)
    name.Append(x['param'])
    t_par_best[0]       = x['param_best']
    t_par_lo[0]         = x['param_lo']
    t_par_hi[0]         = x['param_hi']
    t_par_best_post[0]  = x['param_best_post']
    t_par_lo_post[0]    = x['param_lo_post']
    t_par_hi_post[0]    = x['param_hi_post']
    t_par_best_pre[0]   = x['param_best_pre']
    t_par_lo_pre[0]     = x['param_lo_pre']
    t_par_hi_pre[0]     = x['param_hi_pre']
    
    t_impact[0]       = x['impact']
    t_impact_post[0]  = x['impact_post']
    t_impact_pre[0]   = x['impact_pre']
    t_frozen[0]       = x['frozen']
    t_frozen_post[0]  = x['frozen_post']
    t_frozen_pre[0]   = x['frozen_pre']
    t_rank_impact[0]      = posInImpact[x['param']]
    t_rank_impact_post[0] = posInImpactPost[x['param']]
    t_rank_impact_pre[0]  = posInImpactPre[x['param']]
    t_rank_frozen[0]      = posInFrozen[x['param']]
    t_rank_frozen_post[0] = posInFrozenPost[x['param']]
    t_rank_frozen_pre[0]  = posInFrozenPre[x['param']]
    t.Fill()
  
  f.Write()
  f.Close()




