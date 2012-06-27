#include <iostream>

#include <TH1F.h>
#include <TFile.h>
#include <TMath.h>
#include <TROOT.h>
#include <TString.h>
#include <TSystem.h>
#include <Rtypes.h>

#include <TAxis.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TAttLine.h>
#include <TPaveText.h>

#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"


/**
   \class   postfit postfit.C "HiggsAnalysis/HiggsToTauTau/macros/postfit.C"

   \brief   macro to make plots for di-tau masses for all classic htt channels

   This is a macro to create di-tau masses for all classic htt channels combined
*/

void 
postfit(const char* inputfile, const char* dataset = "2011+2012", const char* extra="", float min=0.1, float max=500., bool log=true)
{
  // defining the common canvas, axes pad styles
  SetStyle(); gStyle->SetLineStyleString(11,"20 10");

  if (std::string(dataset) == std::string("2011"     )){ dataset = "2011, #sqrt{s} = 7 TeV, L = 4.9 fb^{-1}"; }
  if (std::string(dataset) == std::string("2012"     )){ dataset = "2012, #sqrt{s} = 8 TeV, L = 5.0 fb^{-1}"; }
  if (std::string(dataset) == std::string("2011+2012")){ dataset = "2011+2012, #sqrt{s} = 7-8 TeV, L = 10 fb^{-1}"; }

  TFile* input = new TFile(inputfile);
  TH1F* Fakes  = (TH1F*)input->Get("Fakes"   ); 
  TH1F* EWK    = (TH1F*)input->Get("EWK"     ); 
  TH1F* ttbar  = (TH1F*)input->Get("ttbar"   ); 
  TH1F* Ztt    = (TH1F*)input->Get("Ztt"     ); 
  TH1F* ggH    = (TH1F*)input->Get("ggH"     ); 
  TH1F* data   = (TH1F*)input->Get("data_obs"); 

  /*
    mass plot before and after fit
  */
  TCanvas *canv = MakeCanvas("canv", "histograms", 600, 600);
  if(log) canv->SetLogy(1);
  // reduce the axis range if necessary
  //data->GetXaxis()->SetRange(0, 28);
  data->SetNdivisions(505);
  data->SetMinimum(min);
  data->SetMaximum(max);
  data->Draw("e");

  if(log){
    Ztt  ->Draw("same");
    ttbar->Draw("same");
    EWK  ->Draw("same");
    Fakes->Draw("same");
    ggH  ->Draw("same");
  }
  else{
    ggH  ->Draw("same");
    Ztt  ->Draw("same");
    ttbar->Draw("same");
    EWK  ->Draw("same");
    Fakes->Draw("same");
  }
  data->Draw("esame");
  canv->RedrawAxis();

  CMSPrelim(dataset, "", 0.17, 0.835);

  TLegend* leg = new TLegend(0.57, 0.65, 0.95, 0.90);
  SetLegendStyle(leg);
  leg->AddEntry(ggH  , "(5#times) H#rightarrow#tau#tau" , "L" );
  leg->AddEntry(data , "observed"                       , "LP");
  leg->AddEntry(Ztt  , "Z#rightarrow#tau#tau"           , "F" );
  leg->AddEntry(ttbar, "t#bar{t}"                       , "F" );
  leg->AddEntry(EWK  , "electroweak"                    , "F" );
  leg->AddEntry(Fakes, "QCD"                            , "F" );
  leg->Draw();

  TPaveText* mssm  = new TPaveText(0.83, 0.85, 0.95, 0.90, "NDC");
  mssm->SetBorderSize(   0 );
  mssm->SetFillStyle(    0 );
  mssm->SetTextAlign(   12 );
  mssm->SetTextSize ( 0.03 );
  mssm->SetTextColor(    1 );
  mssm->SetTextFont (   62 );
  mssm->AddText("m_{H}=125");
  mssm->Draw();

//
//  TPaveText* cat;
//  if(std::string(category) == std::string("b") || std::string(category) == std::string("nob") || std::string(category) == std::string("nob_LOG")){
//    //cat = new TPaveText(0.52, 0.60, 0.90, 0.65, "NDC");
//    cat = new TPaveText(0.57, 0.58, 0.90, 0.65, "NDC");
//  }
//  else{
//    //cat = new TPaveText(0.57, 0.60, 0.90, 0.65, "NDC");
//    cat = new TPaveText(0.60, 0.58, 0.90, 0.65, "NDC");
//  }
//  cat->SetBorderSize(   0 );
//  cat->SetFillStyle(    0 );
//  cat->SetTextAlign(   12 );
//  cat->SetTextSize ( 0.03 );
//  cat->SetTextColor(    1 );
//  cat->SetTextFont (   62 );
//  if(category_string == std::string("b")          ){cat->AddText("b-Tag Category");    }
//  if(category_string == std::string("nob")        ){cat->AddText("Non b-Tag Category");}
//  if(category_string == std::string("nob_LOG")    ){cat->AddText("Non b-Tag Category");}
//  if(category_string == std::string("vbf")        ){cat->AddText("VBF Category");      }
//  if(category_string == std::string("boost")      ){cat->AddText("Boosted Category");  }
//  if(category_string == std::string("novbf")      ){cat->AddText("0/1-Jet Category");  }
//  if(category_string == std::string("novbf_LOG")  ){cat->AddText("0/1-Jet Category");  }
//  cat->Draw();
//
//  TPaveText* channels  = new TPaveText(0.78, 0.895, 0.90, 0.995, "NDC");
//  channels->SetBorderSize(   0 );
//  channels->SetFillStyle(    0 );
//  channels->SetTextAlign(   12 );
//  channels->SetTextSize ( 0.03 );
//  channels->SetTextColor(    1 );
//  channels->SetTextFont (   62 );
//  channels->AddText("All channels");
//  channels->Draw();
//
//  TLegend* leg;
//  TPaveText* mssm;
//  if(std::string(category) == std::string("b") || std::string(category) == std::string("nob") || std::string(category) == std::string("nob_LOG")){
//    leg = new TLegend(0.52, 0.65, 0.9, 0.90);
//    SetLegendStyle(leg);
//    leg->AddEntry(Higgs, "#phi#rightarrow#tau#tau" , "L" );
//    leg->AddEntry(data , "observed"                , "LP");
//    leg->AddEntry(Ztt  , "Z#rightarrow#tau#tau"    , "F" );
//    leg->AddEntry(ttbar, "t#bar{t}"                , "F" );
//    leg->AddEntry(EWK  , "electroweak"             , "F" );
//    leg->AddEntry(Fakes, "multijets"               , "F" );
//    leg->Draw();
//    
//    mssm  = new TPaveText(0.69, 0.85, 0.90, 0.90, "NDC");
//    mssm->SetBorderSize(   0 );
//    mssm->SetFillStyle(    0 );
//    mssm->SetTextAlign(   12 );
//    mssm->SetTextSize ( 0.03 );
//    mssm->SetTextColor(    1 );
//    mssm->SetTextFont (   62 );
//    mssm->AddText("(m_{A}=120, tan#beta=20)");
//  }
//  else{
//    leg = new TLegend(0.57, 0.65, 0.95, 0.90);
//    SetLegendStyle(leg);
//    SetLegendStyle(leg);
//    leg->AddEntry(Higgs, "(5#times) H#rightarrow#tau#tau" , "L" );
//    leg->AddEntry(data , "observed"                , "LP");
//    leg->AddEntry(Ztt  , "Z#rightarrow#tau#tau"    , "F" );
//    leg->AddEntry(ttbar, "t#bar{t}"                , "F" );
//    leg->AddEntry(EWK  , "electroweak"             , "F" );
//    leg->AddEntry(Fakes, "multijets"               , "F" );
//
//    
//    mssm  = new TPaveText(0.83, 0.85, 0.95, 0.90, "NDC");
//    mssm->SetBorderSize(   0 );
//    mssm->SetFillStyle(    0 );
//    mssm->SetTextAlign(   12 );
//    mssm->SetTextSize ( 0.03 );
//    mssm->SetTextColor(    1 );
//    mssm->SetTextFont (   62 );
//    mssm->AddText("m_{H}=120");
//    mssm->Draw();
//  }
//  leg->Draw();
//  mssm->Draw();

  /*
    prepare output
  */
  std::string newName = std::string(inputfile).substr(0, std::string(inputfile).find(".root"));
  canv->Print(TString::Format("%s.png", newName.c_str())); 
  canv->Print(TString::Format("%s.pdf", newName.c_str())); 
}
