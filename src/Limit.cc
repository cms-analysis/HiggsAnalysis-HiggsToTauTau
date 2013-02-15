#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

/// This is the core plotting routine that can also be used within
/// root macros. It is therefore not element of the PlotLimits class.
void plottingLimit(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed, TGraph* unit, std::string& xaxis, std::string& yaxis, double min, double max, bool log, std::string PLOT, std::string injectedMass, bool legendOnRight); 

void
PlotLimits::plotLimit(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed)
{
  // set up styles
  SetStyle();
  // create the unit line
  TGraph* unit = 0;
  if(!mssm_){
    unit = new TGraph();
    for(unsigned int imass=0, ipoint=0; imass<bins_.size(); ++imass){
      if(valid_[imass]){
	unit->SetPoint(ipoint, bins_[imass], 1.); ++ipoint;
      }
    }
  }
  // set proper maximum
  float max = maximum(expected);
  // do the plotting 
  std::string PLOT("LIMIT");
  if(injected_){ PLOT=std::string("INJECTED"); }
  if(BG_Higgs_){ PLOT=std::string("BG_HIGGS"); }	  
  if(bestfit_ ){ PLOT=std::string("BESTFIT" ); }
  plottingLimit(canv, innerBand, outerBand, expected, observed, unit, xaxis_, yaxis_, min_, max, log_, PLOT, injectedMass_, mssm_);
  // setup CMS Preliminary
  CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);
  // write results to files
  if(png_){ canv.Print(std::string(output_).append("_").append(label_).append(".png").c_str()); }
  if(pdf_){ 
    canv.Print(std::string(output_).append("_").append(label_).append(".pdf").c_str()); 
    canv.Print(std::string(output_).append("_").append(label_).append(".eps").c_str()); 
  }
  if(txt_){
    print(std::string(output_).append("_").append(label_).c_str(), outerBand, innerBand, expected, observed, "txt");
    print(std::string(output_).append("_").append(label_).c_str(), outerBand, innerBand, expected, observed, "tex");
  }
  if(root_){
    TFile* output = new TFile(std::string(output_).append("_").append(label_).append(".root").c_str(), "update");
    if(!output->cd(output_.c_str())){
      output->mkdir(output_.c_str());
      output->cd(output_.c_str());
    }
    if(observed ){ observed ->Write("observed" ); }
    if(expected ){ expected ->Write("expected" ); }
    if(innerBand){ innerBand->Write("innerBand"); }
    if(outerBand){ outerBand->Write("outerBand"); }
    output->Close();
  }
  return;
}

