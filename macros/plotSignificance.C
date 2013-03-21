#include <string>
#include <iostream>

#include "TFile.h"
#include "TGraph.h"
#include "TCanvas.h"
#include "TGraphAsymmErrors.h"

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"

#include "HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"
#include "HiggsAnalysis/HiggsToTauTau/src/plottingSignificance.cxx"

void
plotSignificance(const char* filename, const char* channel, double min_=0., double max_=7., bool log_=false, std::string dataset_="CMS Preliminary,  H#rightarrow#tau#tau,  4.9 fb^{-1} at 7 TeV, 19.4 fb^{-1} at 8 TeV", std::string xaxis_="m_{H} [GeV]", std::string yaxis_="Significance", bool mssm_=false)
{
  TFile* file = TFile::Open(filename);
  // retrieve TGraphs from file
  TGraph* expected = (TGraph*)file->Get(std::string(channel).append("/expected").c_str());
  TGraph* observed = (TGraph*)file->Get(std::string(channel).append("/observed").c_str());
  TGraphAsymmErrors* innerBand = (TGraphAsymmErrors*)file->Get(std::string(channel).append("/innerBand").c_str());
  TGraphAsymmErrors* outerBand = (TGraphAsymmErrors*)file->Get(std::string(channel).append("/outerBand").c_str());
  // set up styles
  SetStyle();
  // create the unit lines
  TGraph* unit3 = new TGraph();
  TGraph* unit5 = new TGraph();
  for(int imass=0, ipoint=0; imass<expected->GetN(); ++imass){
    unit3->SetPoint(ipoint, expected->GetX()[imass], 3.);
    unit5->SetPoint(ipoint, expected->GetX()[imass], 5.);
    ++ipoint;
  }
  // set proper maximum
  float max = maximum(expected, max_);
  // do the plotting 
  TCanvas canv = TCanvas("canv", "Limits", 600, 600);
  // do the plotting 
  plottingSignificance(canv, innerBand, outerBand, expected, observed, unit3, unit5, xaxis_, yaxis_, min_, max, log_, mssm_);
  /// setup the CMS Preliminary
  CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);
  // write results to files
  canv.Print(std::string(channel).append("_significance").append(".png").c_str());
  canv.Print(std::string(channel).append("_significance").append(".pdf").c_str()); 
  canv.Print(std::string(channel).append("_significance").append(".eps").c_str()); 
  return;
}
