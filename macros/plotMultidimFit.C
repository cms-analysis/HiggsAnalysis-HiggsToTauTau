#include <string>
#include <vector>
#include <iostream>

#include "TKey.h"
#include "TFile.h"
#include "TGraph.h"
#include "TCanvas.h"
#include "TRegexp.h"
#include "TGraphAsymmErrors.h"

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"

#include "HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"
#include "HiggsAnalysis/HiggsToTauTau/src/plottingScan2D.cxx"

void
plotMultidimFit(const char* filename, const char* channel, int mass=125, bool temp_=false, bool log_=false, std::string dataset_="CMS Preliminary,  H#rightarrow#tau#tau,  4.9 fb^{-1} at 7 TeV, 19.4 fb^{-1} at 8 TeV", std::string xaxis_="#kappa_{V}", std::string yaxis_="#kappa_{F}", bool mssm_=false)
{
  TFile* file = TFile::Open(filename);
  TString style = temp_ ? "graph" : "filled";

  // retrieve TGraphs from file
  TH2F* plot2D;
  TRegexp regex2D(TString::Format("plot2D_%d_*", mass));
  TGraph* bestfit;
  TRegexp regexXY(TString::Format("bestfit_%d_*", mass));
  std::vector<TGraph*> graph68;
  TRegexp regex68(TString::Format("%s68_%d_*", style.Data(), mass));
  std::vector<TGraph*> graph95;
  TRegexp regex95(TString::Format("%s95_%d_*", style.Data(), mass));

  file->cd(channel);
  TIter next(gDirectory->GetListOfKeys());
  TKey* iobj;
  while((iobj = (TKey*)next())){
    TString obj(iobj->GetName());
    if(obj.Contains(regex2D)){
      plot2D = (TH2F*)file->Get(TString::Format("%s/%s", channel, obj.Data()));
    }
    if(obj.Contains(regexXY)){
      bestfit = (TGraph*)file->Get(TString::Format("%s/%s", channel, obj.Data()));
    }
    if(obj.Contains(regex68)){
      std::cout << " ...found object: " << iobj->GetName() << std::endl; 
      graph68.push_back((TGraph*)file->Get(TString::Format("%s/%s", channel, obj.Data())));
    }
    if(obj.Contains(regex95)){
      std::cout << " ...found object: " << iobj->GetName() << std::endl; 
      graph95.push_back((TGraph*)file->Get(TString::Format("%s/%s", channel, obj.Data())));
    }
  }
  //return;

  // set up styles
  SetStyle();
  // do the plotting 
  TCanvas canv = TCanvas("canv", "Limits", 600, 600);
  std::string masslabel = mssm_ ? std::string("m_{#phi}") : std::string("m_{H}");
  plotting2DScan(canv, plot2D, graph95 , graph68 , bestfit, xaxis_, yaxis_, masslabel, mass, -1, -1, -1, -1, temp_, log_); 
  /// setup the CMS Preliminary
  CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);
  // write results to files
  canv.Print(std::string(channel).append("_scan2D").append(".png").c_str());
  canv.Print(std::string(channel).append("_scan2D").append(".pdf").c_str()); 
  canv.Print(std::string(channel).append("_scan2D").append(".eps").c_str()); 
  return;
}
