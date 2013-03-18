#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

/// This is the core plotting routine that can also be used within
/// root macros. It is therefore not element of the PlotLimits class.
void plottingPValue(TCanvas& canv, TGraph* expected, TGraph* observed, std::string& xaxis, std::string& yaxis, double min, double max, bool log=true, bool legendOnRight=true);

void
PlotLimits::plotPValue(TCanvas& canv, TGraph* expected, TGraph* observed, const char* directory)
{
  // set up styles
  SetStyle();
  // do the plotting 
  plottingPValue(canv, expected, observed, xaxis_, yaxis_, min_, max_, log_, true);
  // setup the CMS Preliminary
  //CMSPrelim(dataset_.c_str(), "", 0.160, 0.835);
  CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);

  /*
  TPaveText* ext0     = new TPaveText(0.18, 0.42, 0.38, 0.47, "NDC");
  ext0->SetBorderSize(   0 );
  ext0->SetFillStyle(    0 );
  ext0->SetTextAlign(   12 );
  ext0->SetTextSize ( 0.035 );
  ext0->SetTextColor(    1 );
  ext0->SetTextFont (   42 );
  ext0->AddText("CMS Preliminary");
  ext0->Draw();

  TPaveText* ext1     = new TPaveText(0.18, 0.37, 0.38, 0.42, "NDC");
  ext1->SetBorderSize(   0 );
  ext1->SetFillStyle(    0 );
  ext1->SetTextAlign(   12 );
  ext1->SetTextSize ( 0.035 );
  ext1->SetTextColor(    1 );
  ext1->SetTextFont (   42 );
  ext1->AddText("#sqrt{s} = 7 TeV, L = 4.9 fb^{-1}");
  ext1->Draw();

  TPaveText* ext2     = new TPaveText(0.18, 0.32, 0.38, 0.37, "NDC");
  ext2->SetBorderSize(   0 );
  ext2->SetFillStyle(    0 );
  ext2->SetTextAlign(   12 );
  ext2->SetTextSize ( 0.035 );
  ext2->SetTextColor(    1 );
  ext2->SetTextFont (   42 );
  ext2->AddText("#sqrt{s} = 8 TeV, L = 19.4 fb^{-1}");
  ext2->Draw();
  
  TPaveText* ext3     = new TPaveText(0.18, 0.27, 0.38, 0.32, "NDC");
  ext3->SetBorderSize(   0 );
  ext3->SetFillStyle(    0 );
  ext3->SetTextAlign(   12 );
  ext3->SetTextSize ( 0.035 );
  ext3->SetTextColor(    1 );
  ext3->SetTextFont (   42 );
  ext3->AddText("H#rightarrow#tau#tau");
  ext3->Draw();
  */

  // write results to files
  if(png_){
    canv.Print(std::string(output_).append("_").append(label_).append(".png").c_str());
  }
  if(pdf_){
    canv.Print(std::string(output_).append("_").append(label_).append(".pdf").c_str());
    canv.Print(std::string(output_).append("_").append(label_).append(".eps").c_str());
  }
  if(txt_){
    print(std::string(output_).append("_").append(label_).c_str(), expected, observed, "txt");
    print(std::string(output_).append("_").append(label_).c_str(), expected, observed, "tex");
  }
  if(root_){
    TFile* output = new TFile(std::string("p-value-").append(label_).append(".root").c_str(), "update");
    if(!output->cd(output_.c_str())){
      output->mkdir(output_.c_str());
      output->cd(output_.c_str());
    }
    expected->Write("expected");
    observed->Write("observed");
    output->Close();
  }
  return;
}


