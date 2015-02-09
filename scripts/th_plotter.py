#!/usr/bin/env python

'''
Plots tHq, H to tau tau limits
'''

import ROOT
import sys
import os
from array import array
from optparse import OptionParser
from copy import deepcopy as dc
from CMSStyle import *

ROOT.gStyle.SetOptStat(False)
ROOT.gStyle.SetLegendBorderSize(0)

def grab_tree(folder, mass = '125', type = 'exp') : 
  '''
  mass is usually 125 for tHq
  folder looks like LIMITS/example-bin-by-bin/sm/th
  type can be either exp or obs
  '''
  limit_file = ROOT.TFile.Open('/'.join([folder,mass,'higgsCombine-{TYPE}.Asymptotic.mH{MASS}.root'.format(TYPE=type,MASS=mass)]), 'r')
  limit_file.cd()
  limit_tree = ROOT.gDirectory.FindObjectAny('limit')
  return limit_tree

def get_values_exp(tree, process) :
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
  gCentral.SetLineColor(ROOT.kRed   )

#   gCentral.SetLineStyle(ROOT.kBlack )
  
  gCentral.SetMarkerStyle(8)
  
  g2sigma .SetLineWidth(90)
  g1sigma .SetLineWidth(90)
  gCentral.SetLineWidth(2 )
  
  return [g2sigma, g1sigma, gCentral]

def get_values_obs(tree, process) :
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
  
  #import pdb ; pdb.set_trace()
  
  xCentral = array('d',[values[0]  , values[0]  ])
  yCentral = array('d',[process_bin, process_bin])
    
  nullErr = array('d',[0.  , 0.  ])
  width   = array('d',[0.262, 0.262])
    
  gCentral = ROOT.TGraphAsymmErrors(2, xCentral, yCentral, nullErr, nullErr, width, width)
  gCentral.SetLineColor(ROOT.kBlack)

  gCentral.SetMarkerStyle(8)
  gCentral.SetLineWidth(2 )
  
  return [gCentral]

def build_legend(graphs, titles, options = None) :
  
  my_graphs = dc(graphs)
  
  if options : zipped = zip(my_graphs,graphs,titles,options)
  else       : zipped = zip(my_graphs,graphs,titles)
  
  l1 = ROOT.TLegend(0.6,0.22,0.88,0.40)
  l1.SetHeader('m_{H} = 125 GeV')
  for entry in zipped : 
    entry[0].SetLineWidth(2)
    entry[0].SetFillColor(entry[1].GetLineColor())
    import pdb ; pdb.set_trace()
    if options : l1.AddEntry(entry[0],entry[2],entry[3])  
    else       : l1.AddEntry(entry[0],entry[2])  

  l1.SetFillColor(0)
    
  return l1

def set_style(logX) :

  ROOT.gPad.SetLogx(logX)
  ROOT.gPad.SetLeftMargin  (0.18)
  ROOT.gPad.SetBottomMargin(0.18)
  
  ROOT.gStyle.SetTitleX(0.545) 
  ROOT.gStyle.SetTitleY(0.97 ) 
  ROOT.gStyle.SetTitleW(0.78 ) 
  ROOT.gStyle.SetTitleH(0.06 )
     
def multigraph(graphs, file_name, legend = False, logX = False, obs = False) :
  '''
  reads a list of TGraph and plot them together.
  Graphic options are hard coded.
  '''

  c1 = ROOT.TCanvas('','',700,700)
  
  set_style(logX)
        
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
  
  #mg.SetTitle('CMS Preliminary tH, H#rightarrow#tau#tau, 19.7 fb^{-1} at 8 TeV')
  
  mg.GetYaxis().SetNdivisions(0)
  mg.GetYaxis().SetLabelSize(0)
  
  mg.SetMinimum(0.)
  mg.SetMaximum(3.)
  
  mg.GetXaxis().SetRangeUser(-2.,60)
  mg.GetXaxis().SetTitleOffset(1.4)
  mg.GetXaxis().SetTitle('95% CL Limit on (#sigma#timesBR)/(#sigma#timesBR)_{y_{t}=-1}')

  if legend :
    
    #legend_list = 
    import pdb ; pdb.set_trace()
    if obs :
      leg = build_legend(
                         graphs[:4]                                  ,
                         ['2 #sigma band', '1 #sigma band','Expected', 'Observed'],
                         ['f'            , 'f'            ,'l'       , 'l'       ],
                         )
    else :
      leg = build_legend(
                         graphs[:3]                                   ,
                         ['2 #sigma band', '1 #sigma band','Expected'],
                         ['f'            , 'f'            ,'l'       ],
                         )
    leg.Draw('sameAEPZ')
  
  CMS_lumi(ROOT.gPad, 2, 0)
  c1.SaveAs(file_name)

def do_category(folder, process, mass='125', type = 'exp') :
  #import pdb ; pdb.set_trace()
  graphs = []
  tree   = grab_tree(folder, mass, type)
  if type == 'exp' : graphs.extend( get_values_exp(tree, process) )
  else             : graphs.extend( get_values_obs(tree, process) )
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

  parser.add_option('-O', 
                    '--observed', 
                    dest    = 'observed',  
                    help    = 'show observed limit. Default is False', 
                    default = False)
      
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
    graphs = do_category(folder, cat)
    graphs_tot.extend(graphs)
    
    if options.observed :
      obs_graphs = do_category(folder, cat, type='obs')
      graphs_tot.extend(obs_graphs)
      
  
  multigraph(graphs_tot, options.file_name, legend=True, obs=options.observed)  
