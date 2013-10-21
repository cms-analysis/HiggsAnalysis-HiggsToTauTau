#include <string>
#include <iostream>

#include "TFile.h"
#include "TGraph.h"
#include "TCanvas.h"
#include "TGraphAsymmErrors.h"

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"

#include "HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"
#include "HiggsAnalysis/HiggsToTauTau/src/plottingLimit.cxx"

void
plotAsymptotic(const char* filename, const char* channel, std::string TYPE="LIMIT", bool draw_injected_=false, double min_=0., double max_=-1., bool log_=false, std::string injectedMass_="125", std::string dataset_="CMS Preliminary,  H#rightarrow#tau#tau,  4.9 fb^{-1} at 7 TeV, 19.7 fb^{-1} at 8 TeV", std::string xaxis_="m_{H} [GeV]", std::string yaxis_="95% CL limit on #sigma/#sigma_{SM}", std::string extra="", bool mssm_=false)
{
  /*
    TYPE can be: LIMIT, INJECTED, BG_HIGGS, MSSM-LOG
  */
  TFile* file = TFile::Open(filename);
  // retrieve TGraphs from file
  TGraph* expected = (TGraph*)file->Get(std::string(channel).append("/expected").c_str());
  TGraph* observed = (TGraph*)file->Get(std::string(channel).append("/observed").c_str());
  TGraphAsymmErrors* innerBand = (TGraphAsymmErrors*)file->Get(std::string(channel).append("/innerBand").c_str());
  TGraphAsymmErrors* outerBand = (TGraphAsymmErrors*)file->Get(std::string(channel).append("/outerBand").c_str());
  // set up styles
  SetStyle();
  // this is new for injected plot together with observed
  TGraph* injected = 0;
  if(draw_injected_) {injected = (TGraph*)file->Get("injected/observed");}
  // create the unit line
  TGraph* unit = 0;
  if(!mssm_){
    unit = new TGraph();
    for(int imass=0, ipoint=0; imass<expected->GetN(); ++imass){
      unit->SetPoint(ipoint, expected->GetX()[imass], 1.); ++ipoint;
    }
  }
  // set proper maximum
  float max = maximum(expected, max_);
  // do the plotting 
  TCanvas canv = TCanvas("canv", "Limits", 600, 600);
  plottingLimit(canv, innerBand, outerBand, expected, observed, unit, xaxis_, yaxis_, injected, min_, max, log_, TYPE, injectedMass_, mssm_, extra);
  // setup CMS Preliminary
  CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);
  // write results to files
  canv.Print(std::string(channel).append("_").append(TYPE).append(".png").c_str());
  canv.Print(std::string(channel).append("_").append(TYPE).append(".pdf").c_str()); 
  canv.Print(std::string(channel).append("_").append(TYPE).append(".eps").c_str()); 
  return;
}
