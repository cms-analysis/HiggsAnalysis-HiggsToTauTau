#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

/// This is the core plotting routine that can also be used within
/// root macros. It is therefore not element of the PlotLimits class.
void plottingMassEstimate(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed, std::string& xaxis, std::string& yaxis, double max, bool log);

void
PlotLimits::plotMassEstimate(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed)
{
  float minobs = 9999.;
  for(int idx=0; idx<observed->GetN(); ++idx){
    if(minobs==9999 || observed->GetY()[idx]<minobs){
      minobs = observed->GetY()[idx];
    }
  } 
  TGraph* modifiedobs= new TGraph();
  for(int idx=0; idx<observed->GetN(); ++idx){
    modifiedobs->SetPoint(idx, observed->GetX()[idx], observed->GetY()[idx]-minobs);
  } 
  // set up styles
  SetStyle();
  // set proper maximum
  float max = max_<0 ? maximum(expected) : max_;
  // do the plotting
  plottingMassEstimate(canv, innerBand, outerBand, expected, modifiedobs, xaxis_, yaxis_, max, log_);    
  // add the CMS Preliminary stamp
  CMSPrelim(dataset_.c_str(), "", 0.160, 0.835);
  //CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);
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
    print(path, expected, observed, "txt"); 
    print(path, expected, observed, "tex"); 
  }
  if(root_){
    TFile* output = new TFile("likelihood-mass-scan.root", "update");
    if(!output->cd(output_.c_str())){
	output->mkdir(output_.c_str());
	output->cd(output_.c_str());
    }
    if(observed ){observed ->Write("observed" );}
    if(expected ){expected ->Write("expected" );}
    if(innerBand){innerBand->Write("innerBand");}
    if(outerBand){outerBand->Write("outerBand");}
    output->Close();
  }
  return;
}

