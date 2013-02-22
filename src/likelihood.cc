#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

/// This is the core plotting routine that can also be used within
/// root macros. It is therefore not element of the PlotLimits class.
void plottingLikelihood(TCanvas& canv, TGraph* expected, TGraph* observed, std::string& xaxis, std::string& yaxis, double min, double max, bool log=true, bool legendOnRight=true);

void
PlotLimits::plotLikelihood(TCanvas& canv, TGraph* expected, TGraph* observed, const char* directory)
{
  // set up styles
  SetStyle();
  // do the plotting 
  plottingLikelihood(canv, expected, observed, xaxis_, yaxis_, min_, max_, log_, true);
  // setup the CMS Preliminary
  CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);
  // write results to files
  if(png_){
    canv.Print(std::string(output_).append("_").append(label_).append(".png").c_str());
  }
  if(pdf_){
    canv.Print(std::string(output_).append("_").append(label_).append(".pdf").c_str());
    canv.Print(std::string(output_).append("_").append(label_).append(".eps").c_str());
  }
  if(txt_){
    if(expected != 0) print(std::string(output_).append("_").append(label_).c_str(), observed,expected, "txt");
    if(expected != 0) print(std::string(output_).append("_").append(label_).c_str(), observed,expected, "tex");
  }
  if(root_){
    TFile* output = new TFile(std::string("p-value-").append(label_).append(".root").c_str(), "update");
    if(!output->cd(output_.c_str())){
      output->mkdir(output_.c_str());
      output->cd(output_.c_str());
    }
    if(expected != 0) expected->Write("expected");
    observed->Write("observed");
    output->Close();
  }
  return;
}


