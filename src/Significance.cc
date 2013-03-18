#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

/// This is the core plotting routine that can also be used within
/// root macros. It is therefore not element of the PlotLimits class.
void plottingSignificance(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed, TGraph* unit3, TGraph* unit5, std::string& xaxis, std::string& yaxis, double min, double max, bool log, bool legendOnRight);

void
PlotLimits::plotSignificance(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed)
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
  plottingSignificance(canv, innerBand, outerBand, expected, observed, unit3, unit5, xaxis_, yaxis_, min_, max, log_, mssm_);
  /// setup the CMS Preliminary
  //CMSPrelim(dataset_.c_str(), "", 0.160, 0.835);
  CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);

  /*
  TPaveText* ext0     = new TPaveText(0.60, 0.85, 0.80, 0.90, "NDC");
  ext0->SetBorderSize(   0 );
  ext0->SetFillStyle(    0 );
  ext0->SetTextAlign(   12 );
  ext0->SetTextSize ( 0.035 );
  ext0->SetTextColor(    1 );
  ext0->SetTextFont (   42 );
  ext0->AddText("CMS Preliminary");
  ext0->Draw();

  TPaveText* ext1     = new TPaveText(0.60, 0.80, 0.80, 0.85, "NDC");
  ext1->SetBorderSize(   0 );
  ext1->SetFillStyle(    0 );
  ext1->SetTextAlign(   12 );
  ext1->SetTextSize ( 0.035 );
  ext1->SetTextColor(    1 );
  ext1->SetTextFont (   42 );
  ext1->AddText("#sqrt{s} = 7 TeV, L = 4.9 fb^{-1}");
  ext1->Draw();

  TPaveText* ext2     = new TPaveText(0.60, 0.75, 0.80, 0.80, "NDC");
  ext2->SetBorderSize(   0 );
  ext2->SetFillStyle(    0 );
  ext2->SetTextAlign(   12 );
  ext2->SetTextSize ( 0.035 );
  ext2->SetTextColor(    1 );
  ext2->SetTextFont (   42 );
  ext2->AddText("#sqrt{s} = 8 TeV, L = 19.4 fb^{-1}");
  ext2->Draw();
  
  TPaveText* ext3     = new TPaveText(0.60, 0.70, 0.80, 0.75, "NDC");
  ext3->SetBorderSize(   0 );
  ext3->SetFillStyle(    0 );
  ext3->SetTextAlign(   12 );
  ext3->SetTextSize ( 0.035 );
  ext3->SetTextColor(    1 );
  ext3->SetTextFont (   42 );
  ext3->AddText("H#rightarrow#tau#tau");
  ext3->Draw();
  */

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
    if(innerBand){ innerBand->Write("innerBand" );}
    if(outerBand){ outerBand->Write("outerBand" );}
    output->Close();
  }
  return;
}

