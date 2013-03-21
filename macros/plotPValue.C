#include <string>
#include <iostream>

#include "TFile.h"
#include "TGraph.h"
#include "TCanvas.h"
#include "TGraphAsymmErrors.h"

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"

#include "HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"
#include "HiggsAnalysis/HiggsToTauTau/src/plottingPValue.cxx"

void
plotPValue(const char* filename, const char* channel, double min_=1e-8, double max_=1., bool log_=true, std::string dataset_="CMS Preliminary,  H#rightarrow#tau#tau,  4.9 fb^{-1} at 7 TeV, 19.4 fb^{-1} at 8 TeV", std::string xaxis_="m_{H} [GeV]", std::string yaxis_="Local p-value")
{
  TFile* file = TFile::Open(filename);
  // retrieve TGraphs from file
  TGraph* expected = (TGraph*)file->Get(std::string(channel).append("/expected").c_str());
  TGraph* observed = (TGraph*)file->Get(std::string(channel).append("/observed").c_str());
  // set up styles
  SetStyle();
  // do the plotting 
  TCanvas canv = TCanvas("canv", "Limits", 600, 600);
  // do the plotting 
  plottingPValue(canv, expected, observed, xaxis_, yaxis_, min_, max_, log_, true);
  // setup the CMS Preliminary
  CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);
  // write results to files
  canv.Print(std::string(channel).append("_pvalue").append(".png").c_str());
  canv.Print(std::string(channel).append("_pvalue").append(".pdf").c_str()); 
  canv.Print(std::string(channel).append("_pvalue").append(".eps").c_str()); 
  return;
}
