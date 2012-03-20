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

   \brief   macro to create di-tau masses for all classic htt channels combined

   macro to create di-tau masses for all classic htt channels combined
*/

void add(TH1F* base, TH1F* adding, bool data=false){
  std::cout << "WARNING: found unequal number of bins for two histograms which are to be added." << std::endl;
  //std::cout << "N(bins)=" << base->GetNbinsX() << "  <-->  " << adding->GetNbinsX() << std::endl;
  for(int idx=0; idx<(base->GetNbinsX()<=adding->GetNbinsX() ? base->GetNbinsX() : adding->GetNbinsX()); ++idx){
    //std::cout << "[" << idx+1 << "] : " << base->GetBinLowEdge(idx+1) << "  <-->  " << adding->GetBinLowEdge(idx+1) << std::endl; 
    base->SetBinContent(idx+1, base->GetBinContent(idx+1)+adding->GetBinContent(idx+1));
    if(data){
      base->SetBinError(idx+1, TMath::Sqrt(base->GetBinError(idx+1)*base->GetBinError(idx+1)+adding->GetBinError(idx+1)*adding->GetBinError(idx+1)));
    }
  }
}

bool mssm(const char* category){
  std::string category_string(category);
  return (category_string == std::string("b"  )|| category_string == std::string("nob") || category_string == std::string("nob_LOG"));
}

// rescale histograms according to fit
void 
postfit(const char* category)
{
  bool log = !(std::string(category).find("LOG")==std::string::npos);

  // defining the common canvas, axes pad styles
  SetStyle();
  gStyle->SetLineStyleString(11,"20 10");
  // open histogram file
  TFile* files[3];
  std::cout << "* load " << TString::Format("MitLimits/Higgs2Tau/postfit/emu_rescaled_%s%s.root"  , category, log ? "_LOG" : "")   << std::endl;
  files[0] = new TFile(TString::Format("MitLimits/Higgs2Tau/postfit/emu_rescaled_%s.root"  , category));
  std::cout << "* load " << TString::Format("MitLimits/Higgs2Tau/postfit/etau_rescaled_%s%s.root"  , category, log ? "_LOG" : "")  << std::endl;
  files[1] = new TFile(TString::Format("MitLimits/Higgs2Tau/postfit/etau_rescaled_%s.root" , category));
  std::cout << "* load " << TString::Format("MitLimits/Higgs2Tau/postfit/mutau_rescaled_%s%s.root"  , category, log ? "_LOG" : "") << std::endl;
  files[2] = new TFile(TString::Format("MitLimits/Higgs2Tau/postfit/mutau_rescaled_%s.root", category));
  //load example histograms
  TH1F* buffer;
  TH1F* data   = (TH1F*)files[0]->Get("data_obs"); 
  buffer = (TH1F*)files[1]->Get("data_obs"); 
  if(data ->GetNbinsX()!=buffer->GetNbinsX()){ add(data , buffer, true); } else { data ->Add(buffer); }
  buffer = (TH1F*)files[2]->Get("data_obs"); 
  if(data ->GetNbinsX()!=buffer->GetNbinsX()){ add(data , buffer, true); } else { data ->Add(buffer); }

  TH1F* Ztt    = (TH1F*)files[0]->Get("Ztt"     ); 
  buffer = (TH1F*)files[1]->Get("Ztt"     ); 
  if(Ztt  ->GetNbinsX()!=buffer->GetNbinsX()){ add(Ztt  , buffer      ); } else { Ztt  ->Add(buffer); }
  buffer = (TH1F*)files[2]->Get("Ztt"     );
  if(Ztt  ->GetNbinsX()!=buffer->GetNbinsX()){ add(Ztt  , buffer      ); } else { Ztt  ->Add(buffer); }

  TH1F* ttbar  = (TH1F*)files[0]->Get("ttbar"   ); 
  buffer = (TH1F*)files[1]->Get("ttbar"   );
  if(ttbar->GetNbinsX()!=buffer->GetNbinsX()){ add(ttbar, buffer      ); } else { ttbar->Add(buffer); }
  buffer = (TH1F*)files[2]->Get("ttbar"   );
  if(ttbar->GetNbinsX()!=buffer->GetNbinsX()){ add(ttbar, buffer      ); } else { ttbar->Add(buffer); }

  TH1F* EWK    = (TH1F*)files[0]->Get("EWK"     ); 
  buffer = (TH1F*)files[1]->Get("EWK"     );
  if(EWK  ->GetNbinsX()!=buffer->GetNbinsX()){ add(EWK  , buffer      ); } else { EWK  ->Add(buffer); }
  buffer = (TH1F*)files[2]->Get("EWK"     );
  if(EWK  ->GetNbinsX()!=buffer->GetNbinsX()){ add(EWK  , buffer      ); } else { EWK  ->Add(buffer); }

  TH1F* Fakes  = (TH1F*)files[0]->Get("Fakes"   ); 
  buffer = (TH1F*)files[1]->Get("Fakes"   );
  if(Fakes->GetNbinsX()!=buffer->GetNbinsX()){ add(Fakes, buffer      ); } else { Fakes->Add(buffer); }
  buffer = (TH1F*)files[2]->Get("Fakes"   );
  if(Fakes->GetNbinsX()!=buffer->GetNbinsX()){ add(Fakes, buffer      ); } else { Fakes->Add(buffer); }

  TH1F* Higgs  = (TH1F*)files[0]->Get(mssm(category) ? "bbH" : "qqH"); 
  buffer = (TH1F*)files[1]->Get(mssm(category) ? "bbH" : "qqH");
  if(Higgs->GetNbinsX()!=buffer->GetNbinsX()){ add(Higgs, buffer      ); } else { Higgs->Add(buffer); }
  buffer = (TH1F*)files[2]->Get(mssm(category) ? "bbH" : "qqH");
  if(Higgs->GetNbinsX()!=buffer->GetNbinsX()){ add(Higgs, buffer      ); } else { Higgs->Add(buffer); }
  std::cout << "*" << std::endl;

  // define canvas
  TCanvas *canv = MakeCanvas("canv", "histograms", 600, 600);
  if(log) canv->SetLogy(1);

  canv->cd();
  std::string category_string(category);
  if(category_string == std::string("b")          ){data->SetMaximum(  20.);}
  if(category_string == std::string("nob")        ){data->SetMaximum(1450.);}//1450
  if(category_string == std::string("nob_LOG")    ){data->SetMaximum(3000.);}
  if(category_string == std::string("vbf")        ){data->SetMaximum(  2.5);}//3.
  if(category_string == std::string("boost")      ){data->SetMaximum( 20.0);}//20.
  if(category_string == std::string("novbf")      ){data->SetMaximum(1450.);}//1450
  if(category_string == std::string("novbf_LOG")  ){data->SetMaximum(3000.);}
  //data->SetMaximum( 6.);
  if(log){
    if(category_string == std::string("nob_LOG"  )) data->SetMinimum(0.2);
    if(category_string == std::string("novbf_LOG")) data->SetMinimum(1.0);
  } else{data->SetMinimum( 0.);}
  data->GetYaxis()->SetTitle("#bf{dN/dm_{#tau#tau} [1/GeV]}");
  if(std::string(category)==std::string("nob") || std::string(category) == std::string("nob_LOG")) data->GetXaxis()->SetRange(0, 35);
  data->Draw("e");

  Ztt->Draw("same");
  ttbar->Draw("same");
  EWK->Draw("same");
  Fakes->Draw("same");
  Higgs->Draw("same");
  data->Draw("esame");
  canv->RedrawAxis();

  CMSPrelim("", 0.17, 0.835);

  TPaveText* cat;
  if(std::string(category) == std::string("b") || std::string(category) == std::string("nob") || std::string(category) == std::string("nob_LOG")){
    //cat = new TPaveText(0.52, 0.60, 0.90, 0.65, "NDC");
    cat = new TPaveText(0.57, 0.58, 0.90, 0.65, "NDC");
  }
  else{
    //cat = new TPaveText(0.57, 0.60, 0.90, 0.65, "NDC");
    cat = new TPaveText(0.60, 0.58, 0.90, 0.65, "NDC");
  }
  cat->SetBorderSize(   0 );
  cat->SetFillStyle(    0 );
  cat->SetTextAlign(   12 );
  cat->SetTextSize ( 0.03 );
  cat->SetTextColor(    1 );
  cat->SetTextFont (   62 );
  if(category_string == std::string("b")          ){cat->AddText("b-Tag Category");    }
  if(category_string == std::string("nob")        ){cat->AddText("Non b-Tag Category");}
  if(category_string == std::string("nob_LOG")    ){cat->AddText("Non b-Tag Category");}
  if(category_string == std::string("vbf")        ){cat->AddText("VBF Category");      }
  if(category_string == std::string("boost")      ){cat->AddText("Boosted Category");  }
  if(category_string == std::string("novbf")      ){cat->AddText("0/1-Jet Category");  }
  if(category_string == std::string("novbf_LOG")  ){cat->AddText("0/1-Jet Category");  }
  cat->Draw();

  TPaveText* channels  = new TPaveText(0.78, 0.895, 0.90, 0.995, "NDC");
  channels->SetBorderSize(   0 );
  channels->SetFillStyle(    0 );
  channels->SetTextAlign(   12 );
  channels->SetTextSize ( 0.03 );
  channels->SetTextColor(    1 );
  channels->SetTextFont (   62 );
  channels->AddText("All channels");
  channels->Draw();

  TLegend* leg;
  TPaveText* mssm;
  if(std::string(category) == std::string("b") || std::string(category) == std::string("nob") || std::string(category) == std::string("nob_LOG")){
    leg = new TLegend(0.52, 0.65, 0.9, 0.90);
    SetLegendStyle(leg);
    leg->AddEntry(Higgs, "#phi#rightarrow#tau#tau" , "L" );
    leg->AddEntry(data , "observed"                , "LP");
    leg->AddEntry(Ztt  , "Z#rightarrow#tau#tau"    , "F" );
    leg->AddEntry(ttbar, "t#bar{t}"                , "F" );
    leg->AddEntry(EWK  , "electroweak"             , "F" );
    leg->AddEntry(Fakes, "multijets"               , "F" );
    leg->Draw();
    
    mssm  = new TPaveText(0.69, 0.85, 0.90, 0.90, "NDC");
    mssm->SetBorderSize(   0 );
    mssm->SetFillStyle(    0 );
    mssm->SetTextAlign(   12 );
    mssm->SetTextSize ( 0.03 );
    mssm->SetTextColor(    1 );
    mssm->SetTextFont (   62 );
    mssm->AddText("(m_{A}=120, tan#beta=20)");
  }
  else{
    leg = new TLegend(0.57, 0.65, 0.95, 0.90);
    SetLegendStyle(leg);
    SetLegendStyle(leg);
    leg->AddEntry(Higgs, "(5#times) H#rightarrow#tau#tau" , "L" );
    leg->AddEntry(data , "observed"                , "LP");
    leg->AddEntry(Ztt  , "Z#rightarrow#tau#tau"    , "F" );
    leg->AddEntry(ttbar, "t#bar{t}"                , "F" );
    leg->AddEntry(EWK  , "electroweak"             , "F" );
    leg->AddEntry(Fakes, "multijets"               , "F" );

    
    mssm  = new TPaveText(0.83, 0.85, 0.95, 0.90, "NDC");
    mssm->SetBorderSize(   0 );
    mssm->SetFillStyle(    0 );
    mssm->SetTextAlign(   12 );
    mssm->SetTextSize ( 0.03 );
    mssm->SetTextColor(    1 );
    mssm->SetTextFont (   62 );
    mssm->AddText("m_{H}=120");
    mssm->Draw();
  }
  leg->Draw();
  mssm->Draw();

  bool scaled=true;
  canv->Print(TString::Format("cmb_%s_%s.png", scaled ? "rescaled" : "unscaled", category)); 
  canv->Print(TString::Format("cmb_%s_%s.pdf", scaled ? "rescaled" : "unscaled", category)); 
  TFile* output = new TFile(TString::Format("cmb_%s_%s.root", scaled ? "rescaled" : "unscaled", category), "update");
  output->cd();
  data ->Write();
  Fakes->Write();
  EWK  ->Write();
  ttbar->Write();
  Ztt  ->Write();
  Higgs->Write();
  output->Close();
}
