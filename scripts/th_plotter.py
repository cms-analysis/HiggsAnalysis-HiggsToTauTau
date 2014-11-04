#!/usr/bin/env python

'''
Plots tHq, H to tau tau limits
'''

import ROOT
import sys
import os
from array import array
from optparse import OptionParser

ROOT.gStyle.SetOptStat(False)

def grab_tree(folder, mass = '125') : 
  '''
  mass is usually 125 for tHq
  folder looks like LIMITS/example-bin-by-bin/sm/th
  '''
  limit_file = ROOT.TFile.Open('/'.join([folder,mass,'higgsCombine-exp.Asymptotic.mH{MASS}.root'.format(MASS=mass)]), 'r')
  limit_file.cd()
  limit_tree = ROOT.gDirectory.FindObjectAny('limit')
  return limit_tree

def get_values(tree, process) :
  '''
  process can be: th, emt, mmt
  '''
  process_dict = {
                   'th'  : 0.5,
                   'emt' : 1.5,
                   'mmt' : 2.5,
                 }

  values = []

  for evt in tree : values.append(evt.limit)
  
  process_bin = process_dict[process]
  
  xCentral = array('d',[values[2]  , values[2]  ])
  yCentral = array('d',[process_bin, process_bin])
  
  xErr2SigmaL = array('d',[ abs(values[4] - values[2]), abs(values[4] - values[2]) ])
  xErr1SigmaL = array('d',[ abs(values[3] - values[2]), abs(values[3] - values[2]) ])
  xErr2SigmaH = array('d',[ abs(values[0] - values[2]), abs(values[0] - values[2]) ])
  xErr1SigmaH = array('d',[ abs(values[1] - values[2]), abs(values[1] - values[2]) ])
  
  nullErr = array('d',[0.  , 0.  ])
  width   = array('d',[0.262, 0.262])
    
  g2sigma  = ROOT.TGraphAsymmErrors(2, xCentral, yCentral, xErr2SigmaH, xErr2SigmaL, nullErr, nullErr)
  g1sigma  = ROOT.TGraphAsymmErrors(2, xCentral, yCentral, xErr1SigmaH, xErr1SigmaL, nullErr, nullErr)
  gCentral = ROOT.TGraphAsymmErrors(2, xCentral, yCentral, nullErr    , nullErr    , width  , width  )
  
  g2sigma .SetFillColor(ROOT.kYellow)
  g1sigma .SetFillColor(ROOT.kGreen )
  
  g2sigma .SetLineColor(ROOT.kYellow)
  g1sigma .SetLineColor(ROOT.kGreen )
  gCentral.SetLineColor(ROOT.kBlack )
  
  gCentral.SetMarkerStyle(8)
  
  g2sigma .SetLineWidth(90)
  g1sigma .SetLineWidth(90)
  gCentral.SetLineWidth(2 )
  
  return [g2sigma, g1sigma, gCentral]

def multigraph(graphs, file_name, legend = False, logX = False) :
  '''
  reads a list of TGraph and plot them together.
  Graphic options are hard coded.
  '''

  c1 = ROOT.TCanvas('','',700,700)
  
  ROOT.gPad.SetLogx(logX)
  ROOT.gPad.SetLeftMargin  (0.18)
  ROOT.gPad.SetBottomMargin(0.18)
  
  ROOT.gStyle.SetTitleX(0.545) 
  ROOT.gStyle.SetTitleY(0.97 ) 
  ROOT.gStyle.SetTitleW(0.78 ) 
  ROOT.gStyle.SetTitleH(0.06 )
      
  h_support = ROOT.TH2F('','',2,-2,25,3,0,3)
  h_support.GetYaxis().SetBinLabel(3,'#mu#mu#tau')
  h_support.GetYaxis().SetBinLabel(2,'e#mu#tau'  )
  h_support.GetYaxis().SetBinLabel(1,'Combined'  )
  h_support.GetYaxis().SetLabelSize(0.05)
  h_support.GetYaxis().SetNdivisions(3)
  h_support.GetXaxis().SetLabelSize(0.)
  h_support.Draw()

  mg = ROOT.TMultiGraph()
  for graph in graphs : mg.Add(graph)
  
  mg.Draw('AZP')
  
  mg.SetTitle('CMS Preliminary tHq, H#rightarrow#tau#tau, 19.7 fb^{-1} at 8 TeV')
  
  mg.GetYaxis().SetNdivisions(0)
  mg.GetYaxis().SetLabelSize(0)
  
  mg.SetMinimum(0.)
  mg.SetMaximum(3.)
  
  mg.GetXaxis().SetRangeUser(-2.,50)
  mg.GetXaxis().SetTitleOffset(1.4)
  mg.GetXaxis().SetTitle('95% CL Limit on (#sigma#timesBR)/(#sigma#timesBR)_{y_{t}=-1}')
  
  c1.SaveAs(file_name)

def do_category(folder, process, mass='125') :
  graphs = []
  tree   = grab_tree(folder, mass)
  graphs.extend( get_values(tree, process) )
  return graphs

if __name__ == '__main__' :

  parser = OptionParser()
  parser.usage = ''' th_plotter.py <options> <folder> '''
  parser.add_option('-C', 
                    '--categories', 
                    dest    = 'categories',  
                    help    = 'categories to plot can be specified separated by a comma. Default is emt,mmt,th', 
                    default = 'emt,mmt,th')

  parser.add_option('-F', 
                    '--file_name', 
                    dest    = 'file_name',  
                    help    = 'output file name. Default is th_limit.pdf', 
                    default = 'th_limit.pdf')
      
  (options, args) = parser.parse_args()

  if len(args) != 1:
    parser.print_help() 
    sys.exit(1)
      
  graphs_tot = []
  
  for cat in options.categories.split(',') :
    cat.replace(' ','')
    folder = '/'.join([os.environ['CMSSW_BASE'],'src',args[0],cat])
    try :
      len( os.listdir(folder) )
    except :
      print '\n'
      print 'this folder %s does not exist or it is empty.\nPlease make sure you ran the limit for the categories you want to plot' %folder  
      print '\n'
      parser.print_help() 
      sys.exit(0)
    graphs = do_category( folder, cat )
    graphs_tot.extend(graphs)
  
  multigraph(graphs_tot, options.file_name)  
