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
#include "HiggsAnalysis/HiggsToTauTau/src/plottingGoodnessOfFit.cxx"

void
plotGoodnessOfFit(const char* filename, const char* channel, int mass=125, double max_=70., bool log_=false, std::string dataset_="CMS Preliminary,  H#rightarrow#tau#tau,  4.9 fb^{-1} at 7 TeV, 19.4 fb^{-1} at 8 TeV", std::string xaxis_="Goodness of Fit", std::string yaxis_="Number of Toys", bool mssm_=false)
{
  TFile* file = TFile::Open(filename);
  // retrieve histogram from file
  TH1F*   exp = (TH1F*  )file->Get(TString::Format("%s/expected_%d", channel, (int)mass));
  TGraph* obs = (TGraph*)file->Get(TString::Format("%s/observed_%d", channel, (int)mass));
  // set up styles
  SetStyle();
  // do the plotting 
  TCanvas canv = TCanvas("canv", "Limits", 600, 600);
  std::string masslabel = mssm_ ? std::string("m_{#phi}") : std::string("m_{H}");
  plottingGoodnessOfFit(canv, exp, obs, xaxis_, yaxis_, masslabel, mass, max_, 0, exp->GetNbinsX(), log_);    
  /// setup the CMS Preliminary
  CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);
  // write results to files
  canv.Print(std::string(channel).append("_goodness_of_fit").append(".png").c_str());
  canv.Print(std::string(channel).append("_goodness_of_fit").append(".pdf").c_str()); 
  canv.Print(std::string(channel).append("_goodness_of_fit").append(".eps").c_str()); 
  return;
}
