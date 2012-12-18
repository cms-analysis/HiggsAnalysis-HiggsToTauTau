#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

/// This is the core plotting routine that can also be used within
/// root macros. It is therefore not element of the PlotLimits class.
void plottingSignificance(TCanvas& canv, TGraph* expected, TGraph* observed, TGraph* unit3, TGraph* unit5, std::string& xaxis, std::string& yaxis, double min, double max, bool log, bool legendOnRight);

void
PlotLimits::plotSignificance(TCanvas& canv, TGraph* expected, TGraph* observed)
{
  // set up styles
  SetStyle();
  // create the unit lines
  TGraph* unit3 = new TGraph();
  TGraph* unit5 = new TGraph();
  for(unsigned int imass=0, ipoint=0; imass<bins_.size(); ++imass){
    if(valid_[imass]){
      unit3->SetPoint(ipoint, bins_[imass], 3.);
      unit5->SetPoint(ipoint, bins_[imass], 5.);
      ++ipoint;
    }
  }
  // set proper maximum
  float max = maximum(expected);
  // do the plotting 
  plottingSignificance(canv, expected, observed, unit3, unit5, xaxis_, yaxis_, min_, max, log_, mssm_);
  /// setup the CMS Preliminary
  CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);

  if(png_){
    canv.Print(std::string(output_).append("_").append(label_).append(".png").c_str()); }
  if(pdf_){ 
    canv.Print(std::string(output_).append("_").append(label_).append(".pdf").c_str());
    canv.Print(std::string(output_).append("_").append(label_).append(".eps").c_str());
  }
  if(txt_){
    print(std::string(output_).append("_").append(label_).c_str(), expected, observed, "txt");
    print(std::string(output_).append("_").append(label_).c_str(), expected, observed, "tex");
  }
  if(root_){
    TFile* output = new TFile(std::string("limits_").append(label_).append(".root").c_str(), "update");
    if(!output->cd(output_.c_str())){
      output->mkdir(output_.c_str());
      output->cd(output_.c_str());
    }
    if(observed){ observed ->Write("observed" );}
    expected ->Write("expected" );
    output->Close();
  }
  return;
}

