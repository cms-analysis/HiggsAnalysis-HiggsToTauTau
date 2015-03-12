#!/usr/bin/env python
import fnmatch
import os
import ROOT
import sys
import math
import json
import re
from optparse import OptionParser

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

usage = """
"""
parser = OptionParser(usage=usage)

parser.add_option("--ws", dest="ws", help="The input workspace")
parser.add_option("--cfg", dest="cfg", help="json file specifying groups")

(options, args) = parser.parse_args()

ws = options.ws
cfg = options.cfg

ROOT.gSystem.Load('$CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit')

data = json.load(open(cfg))

#print data

paramList = listFromWorkspace(ws, 'w', 'ModelConfig_NuisParams')
#print '\n'.join(paramList)

for key, val in data.items():
  matched = set()
  #print "** Doing group: " + key
  for pattern in val:
    rgx = re.compile(pattern)
    matched.update(x for x in paramList if re.match(rgx, x))
    #print "* Using regex: " + pattern
    #print matched
  #print key + ' group = ' + str(len(matched)) 
  print key + ' group = ' + (' '.join(matched))
    
    
