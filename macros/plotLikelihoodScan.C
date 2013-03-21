#include <string>
#include <iostream>

#include "TH1F.h"
#include "TFile.h"
#include "TGraph.h"
#include "TCanvas.h"
#include "TString.h"
#include "TGraphAsymmErrors.h"

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"

#include "HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"
#include "HiggsAnalysis/HiggsToTauTau/src/plottingScan1D.cxx"

void
plotLikelihoodScan(const char* filename, const char* channel, int mass=125, double max_=70., bool log_=false, std::string dataset_="CMS Preliminary,  H#rightarrow#tau#tau,  4.9 fb^{-1} at 7 TeV, 19.4 fb^{-1} at 8 TeV", std::string xaxis_="Signal Strength", std::string yaxis_="#Delta NLL", bool mssm_=false)
{
  TFile* file = TFile::Open(filename);
  // retrieve histogram from file
  TH1F* scan1D = (TH1F*)file->Get(TString::Format("%s/plot1D_%d", channel, (int)mass));
  // set up styles
  SetStyle();
  // do the plotting 
  TCanvas canv = TCanvas("canv", "Limits", 600, 600);
  std::string masslabel = mssm_ ? std::string("m_{#phi}") : std::string("m_{H}");
  plotting1DScan(canv, scan1D, xaxis_, yaxis_, masslabel, mass, max_, 0, scan1D->GetNbinsX(), log_);    
  /// setup the CMS Preliminary
  CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);
  // write results to files
  canv.Print(std::string(channel).append("_likelihood").append(".png").c_str());
  canv.Print(std::string(channel).append("_likelihood").append(".pdf").c_str()); 
  canv.Print(std::string(channel).append("_likelihood").append(".eps").c_str()); 
  return;
}
