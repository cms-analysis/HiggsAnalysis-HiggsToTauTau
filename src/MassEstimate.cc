#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

/// This is the core plotting routine that can also be used within
/// root macros. It is therefore not element of the PlotLimits class.
void plottingMassEstimate(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed, std::string& xaxis, std::string& yaxis, double max, bool log);

void
PlotLimits::plotMassEstimate(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed)
{
  // set up styles
  SetStyle();

  // find minimum of nll
  float minexp = 9999.;
  for(int idx=0; idx<expected->GetN(); ++idx){
    if(minexp==9999 || expected->GetY()[idx]<minexp){
      minexp = expected->GetY()[idx];
    }
  }
  float minobs = 9999.;
  for(int idx=0; idx<observed->GetN(); ++idx){
    if(minobs==9999 || observed->GetY()[idx]<minobs){
      minobs = observed->GetY()[idx];
    }
  }
  // fill modified
  TGraph* modifiedexp = new TGraph();
  for(int idx=0; idx<expected->GetN(); ++idx){
    modifiedexp->SetPoint(idx, expected->GetX()[idx], expected->GetY()[idx]-minexp);
  }
  TGraph* modifiedobs= new TGraph();
  for(int idx=0; idx<observed->GetN(); ++idx){
    modifiedobs->SetPoint(idx, observed->GetX()[idx], observed->GetY()[idx]-minobs);
  }
  TGraphAsymmErrors* modifiedinner = (TGraphAsymmErrors*) innerBand->Clone();
  for(int idx=0; idx<innerBand->GetN(); ++idx){
    modifiedinner->SetPoint(idx, innerBand->GetX()[idx], innerBand->GetY()[idx]-minexp);
  }
  TGraphAsymmErrors* modifiedouter = (TGraphAsymmErrors*) outerBand->Clone();
  for(int idx=0; idx<outerBand->GetN(); ++idx){
    modifiedouter->SetPoint(idx, outerBand->GetX()[idx], outerBand->GetY()[idx]-minexp);
  }
  // set proper maximum
  float max = max_<0 ? maximum(modifiedexp) : max_;
  // do the plotting
  plottingMassEstimate(canv, modifiedinner, modifiedouter, modifiedexp, modifiedobs, xaxis_, yaxis_, max, log_);    
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
    print(path, modifiedobs, modifiedobs, "txt"); 
    print(path, modifiedobs, modifiedobs, "tex"); 
  }
  if(root_){
    TFile* output = new TFile("likelihood-mass-scan.root", "update");
    if(!output->cd(output_.c_str())){
	output->mkdir(output_.c_str());
	output->cd(output_.c_str());
    }
    modifiedobs->Write("mass_scan");
    output->Close();
  }
  return;
}

