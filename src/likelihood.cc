#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

/// This is the core plotting routine that can also be used within
/// root macros. It is therefore not element of the PlotLimits class.
void plottingMassScan(TCanvas& canv, TGraph* plot1D, std::string& xaxis, std::string& yaxis, double max, bool log);

void
PlotLimits::plotMassScan(TCanvas& canv, TGraph* nll)
{
  // set up styles
  SetStyle();

  TGraph* modified = new TGraph();
  // find minimum of nll
  float min = 9999.;
  for(int idx=0; idx<nll->GetN(); ++idx){
    if(min==9999 || nll->GetY()[idx]<min){
      min = nll->GetY()[idx];
    }
  }
  // fill modified
  for(int idx=0; idx<nll->GetN(); ++idx){
    modified->SetPoint(idx, nll->GetX()[idx], nll->GetY()[idx]-min);
  }
  // set proper maximum
  float max = max_<0 ? maximum(modified) : max_;
  // do the plotting
  plottingMassScan(canv, modified, xaxis_, yaxis_, max, log_);    
  // add the CMS Preliminary stamp
  CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);
  // write to file  
  if(png_){
    canv.Print(TString::Format("%s-%s.png", output_.c_str(), label_.c_str()));
  }
  if(pdf_){
    canv.Print(TString::Format("%s-%s.pdf", output_.c_str(), label_.c_str()));
    canv.Print(TString::Format("%s-%s.eps", output_.c_str(), label_.c_str()));
  }
  if(txt_){
    TString path;
    path = TString::Format("%s_%s", output_.c_str(), label_.c_str());
    print(path, modified, modified, "txt"); 
    print(path, modified, modified, "tex"); 
  }
  if(root_){
    TFile* output = new TFile("likelihood-mass-scan.root", "update");
    if(!output->cd(output_.c_str())){
	output->mkdir(output_.c_str());
	output->cd(output_.c_str());
    }
    modified->Write("mass_scan");
    output->Close();
  }
  return;
}

