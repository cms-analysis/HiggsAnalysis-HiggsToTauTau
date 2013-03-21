#include <map>
#include <string>
#include <iostream>

#include "TFile.h"
#include "TGraph.h"
#include "TCanvas.h"
#include "TGraphAsymmErrors.h"

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"

#include "HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"
#include "HiggsAnalysis/HiggsToTauTau/src/plottingTanb.cxx"

void
plotTanb(const char* filename, const char* channel, double min_=0., double max_=50., bool log_=false, std::string dataset_="CMS Preliminary,  H#rightarrow#tau#tau,  4.9 fb^{-1} at 7 TeV, 12.1 fb^{-1} at 8 TeV", std::string xaxis_="m_{A} [GeV]", std::string yaxis_="#bf{tan#beta}")
{
  TFile* file = TFile::Open(filename);
  // retrieve TGraphs from file
  TGraph* expected = (TGraph*)file->Get(std::string(channel).append("/expected").c_str());
  TGraph* observed = (TGraph*)file->Get(std::string(channel).append("/observed").c_str());
  TGraph* upperLEP = (TGraph*)file->Get(std::string(channel).append("/upperLEP").c_str());
  TGraph* lowerLEP = (TGraph*)file->Get(std::string(channel).append("/lowerLEP").c_str());
  TGraphAsymmErrors* innerBand = (TGraphAsymmErrors*)file->Get(std::string(channel).append("/innerBand").c_str());
  TGraphAsymmErrors* outerBand = (TGraphAsymmErrors*)file->Get(std::string(channel).append("/outerBand").c_str());
  TGraphAsymmErrors* plain = (TGraphAsymmErrors*)file->Get(std::string(channel).append("/plain").c_str());

  // this functionality is not yet supported
  std::map<double, TGraphAsymmErrors*> higgsBands;

  // set up styles
  SetStyle();
  // do the plotting 
  TCanvas canv = TCanvas("canv", "Limits", 600, 600);
  // do the plotting 
  plottingTanb(canv, plain, innerBand, outerBand, expected, observed, lowerLEP, upperLEP, higgsBands, xaxis_, yaxis_, min_, max_, log_);
  /// setup the CMS Preliminary
  CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);
  // write results to files
  canv.Print(std::string(channel).append("_tanb").append(".png").c_str());
  canv.Print(std::string(channel).append("_tanb").append(".pdf").c_str()); 
  canv.Print(std::string(channel).append("_tanb").append(".eps").c_str()); 
  return;
}
