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

float maximum(TH1F* h, bool LOG=false){
  if(LOG){
    if(h->GetMaximum()>1000){ return 1000.*TMath::Nint(500*h->GetMaximum()/1000.); }
    if(h->GetMaximum()>  10){ return   10.*TMath::Nint( 50*h->GetMaximum()/  10.); }
    return 50*h->GetMaximum(); 
  }
  else{
    if(h->GetMaximum()>  12){ return 10.*TMath::Nint((1.3*h->GetMaximum()/10.)); }
    if(h->GetMaximum()> 1.2){ return TMath::Nint((1.6*h->GetMaximum())); }
    return 1.6*h->GetMaximum(); 
  }
}

TH1F* refill(TH1F* hin, const char* sample)
/*
  refill histograms, for MC histograms set bin errors to zero.
*/
{
  if(hin==0){
    std::cout << "hist not found: " << sample << " -- this may happen for samples of type signal." << std::endl;
    if(std::string(sample).find("ggH")==std::string::npos){
      std::cout << "hist is not of type signal, close here" << std::endl;
      exit(1);
    }
    else{
      return hin;
    }
  }
  TH1F* hout = (TH1F*)hin->Clone(); hout->Clear();
  for(int i=0; i<hout->GetNbinsX(); ++i){
    // simple refill, histograms are already devided by bin width
    // but for a useful lotting the bin errors for MC need to be 
    // set to zero.
    hout->SetBinContent(i+1, hin->GetBinContent(i+1));
    hout->SetBinError(i+1, 0.);
  }
  return hout;
}

void 
postfit(const char* inputfile, const char* analysis = "SM", const char* dataset = "2011+2012", const char* extra="", float min=0.1, float max=-1., bool log=true)
{
  // defining the common canvas, axes pad styles
  SetStyle(); gStyle->SetLineStyleString(11,"20 10");
  // switch for MSSM/SM
  bool MSSM = std::string(analysis) == std::string("MSSM");
 
  if (std::string(dataset) == std::string("2011"     )){ dataset = "2011, #sqrt{s} = 7 TeV, L = 4.9 fb^{-1}"; }
  if (std::string(dataset) == std::string("2012"     )){ dataset = "2012, #sqrt{s} = 8 TeV, L = 12.0 fb^{-1}"; }
  if (std::string(dataset) == std::string("2011+2012")){ dataset = ", #sqrt{s} = 7-8 TeV, L = 17 fb^{-1}"; }

  TFile* input = new TFile(inputfile);
  TH1F* Fakes  = refill((TH1F*)input->Get("Fakes"   ), "Fakes/QCD"); 
  TH1F* EWK    = refill((TH1F*)input->Get("EWK"     ), "EWK"      ); 
  TH1F* ttbar  = refill((TH1F*)input->Get("ttbar"   ), "ttbar"    ); 
  TH1F* Ztt    = refill((TH1F*)input->Get("Ztt"     ), "Ztt"      ); 
  TH1F* ggH    = refill((TH1F*)input->Get("ggH"     ), "ggH"      ); 
  TH1F* data   = (TH1F*)input->Get("data_obs"); 
  // determine channel for etau Z->ee (EWK) will be shown separated from the rest (EWK1)
  TH1F* EWK1   = 0;
  if(std::string(extra) == std::string("#tau_{e}#tau_{h}")){
    EWK1 = refill((TH1F*)input->Get("EWK1"),  "EWK1");
  }
  TH1F* errorBand = (TH1F*)input->Get("errorBand");

  /*
    mass plot before and after fit
  */
  TCanvas *canv = MakeCanvas("canv", "histograms", 600, 600);
  if(log) canv->SetLogy(1);
  // reduce the axis range if necessary
  //data->GetXaxis()->SetRange(0, 28);
  data->SetNdivisions(505);
  data->SetMinimum(min);
  data->SetMaximum(max>0 ? max : std::max(maximum(data, log), maximum(Ztt, log)));
  data->Draw("e");

  if(log){
    Ztt  ->Draw("same");
    ttbar->Draw("same");
    EWK  ->Draw("same");
    if(EWK1){
      EWK1->Draw("same");
    }
    Fakes->Draw("same");
    if(ggH){ ggH  ->Draw("same"); }
  }
  else{
    if(ggH){ ggH  ->Draw("same"); }
    Ztt  ->Draw("same");
    ttbar->Draw("same");
    EWK  ->Draw("same");
    if(EWK1){
      EWK1->Draw("same");
    }
    Fakes->Draw("same");
  }
  if(errorBand){
    errorBand->Draw("e2same");
  }
  data->Draw("esame");
  canv->RedrawAxis();

  CMSPrelim(dataset, extra, 0.17, 0.835);

  float lower_bound = EWK1 ? 0.60 : 0.65;
  TLegend* leg = new TLegend(MSSM ? 0.45 : 0.50, lower_bound, 0.93, 0.90);
  SetLegendStyle(leg);
  if(MSSM){
    leg->AddEntry(ggH  , "#phi(160 GeV)#rightarrow#tau#tau, tan#beta=8" , "L" );
  }
  else{
    if(ggH){ leg->AddEntry(ggH  , "H(125)#rightarrow#tau#tau" , "L" ); }
  }
  leg->AddEntry(data , "observed"                       , "LP");
  leg->AddEntry(Ztt  , "Z#rightarrow#tau#tau"           , "F" );
  if(EWK1){
    leg->AddEntry(EWK  , "Z#rightarrow ee"              , "F" );
    leg->AddEntry(EWK1 , "electroweak"                  , "F" );
  }
  else{
    leg->AddEntry(EWK  , "electroweak"                  , "F" );
  }
  leg->AddEntry(ttbar, "t#bar{t}"                       , "F" );
  leg->AddEntry(Fakes, "QCD"                            , "F" );
  if(errorBand){
    leg->AddEntry(errorBand, "bkg. uncertainty" , "F" );
  }
  leg->Draw();

  /*
    prepare output
  */
  std::string newName = std::string(inputfile).substr(0, std::string(inputfile).find(".root"));
  canv->Print(TString::Format("%s.png", newName.c_str())); 
  canv->Print(TString::Format("%s.pdf", newName.c_str())); 
  canv->Print(TString::Format("%s.eps", newName.c_str())); 
}
