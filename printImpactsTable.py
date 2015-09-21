#!/usr/bin/env python

import argparse
import os
import re
import sys
import json
import math

cols = {
  'exp'       : 'black',
  'bkg_stat'  : 'blue',
  'bkg_th'    : 'magenta',
  'sig_th'    : 'red'
}

names = {
  'exp'       : 'Experimental',
  'bkg_stat'  : 'Background Stat.',
  'bkg_th'    : 'Background Theory',
  'sig_th'    : 'Signal Theory'
}

poi_labels = {
  'RV' : r'\mu_{\mathrm{V}}',
  'RF' : r'\mu_{\mathrm{F}}',
  'r'  : r'\mu'
}
def SymErr(vals):
  return (vals[2]-vals[0]) / 2.

def LargestImpact(param, pois):
  vals = []
  for p in pois:
    vals.append(abs(param['impact_'+p]))
  return max(vals)

def LargestRank(param, pois):
  vals = []
  for p in pois:
    vals.append(abs(param['rank_'+p]))
  return min(vals)


parser = argparse.ArgumentParser(
    add_help=True
    )

parser.add_argument('-i', '--input')
parser.add_argument('-g', '--groups')
parser.add_argument('--max', default=20, type=float)
args = parser.parse_args()

with open(args.input) as infile:    
    data = json.load(infile)


with open(args.groups) as infile:
    groups_in = json.load(infile)
groups = {}
for key, val in groups_in.iteritems():
  for v in val: groups[v] = key

POIs = [x['name'] for x in data['POIs']]


params = data['params']

# Create ranking information
for p in POIs:
  params.sort(key = lambda k : LargestImpact(k, [p]), reverse=True)
  for i, par in enumerate(params):
    par['rank_'+p] = i+1


latex_start =  r'\tiny\begin{tabular}{lr@{$ \,\,\pm\,\, $}l'
latex_start += r'rr' * len(POIs)
latex_start += r'}'

header = (
  'Nuisance parameters '
  r'& \multicolumn{2}{c}{$(\hat{\theta} - \theta_{0})/\Delta\theta$}'
  )
for p in POIs:
  header += r'& $\Delta\hat{'+ poi_labels[p] + r'}$ & Rank '
header += '\\\\\n\\hline'

latex_end = (
  r'\hline'
  r'\end{tabular}'
  )
print latex_start

print r'\hline'
print r'Parameters of interest & \multicolumn{2}{l}{Best-fit} \\'
print r'\hline'
fmt = '%-60s & %-5.2f & %-5.2f'
for p in data['POIs']:
  line = ''
  line += fmt % ('$'+poi_labels[p['name']]+'$', p['fit'][1], SymErr(p['fit']))
  line += '\\\\'
  print line
print r'\hline'

print header

for poi in POIs:
  params.sort(key = lambda k : LargestRank(k, [poi]))
  for i,p in enumerate(data['params']):
    if i >= args.max: break
    name = p['name'].replace('_', '\\_')
    line = ''
    if groups.has_key(p['name']):
      line += '\\color{' + cols[groups[p['name']]] + '} '
    line += fmt % (name, p['fit'][1] - p['prefit'][1], SymErr(p['fit'])/SymErr(p['prefit']))
    for poix in POIs:
      line += '& %-5.2f & %-4i' % (p['impact_'+poix], p['rank_'+poix])
    line += '\\\\'
    print line
  print '\\hline'

line = '\multicolumn{5}{l}{Nuisance groups: '
sublines = []

for label,col in cols.iteritems():
  sublines.append('\\textcolor{' + col + '}{' + names[label] + '}')
line += ', '.join(sublines)
line += '}\\\\'
print line

print latex_end