#include <map>

#include "TH1F.h"
#include "TH2F.h"
#include "TColor.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TPaveText.h"
#include "TGraphAsymmErrors.h"
#include "TROOT.h"
//#include "TRint.h"
#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"
#include "HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"
#include <iostream>


void plotmHiggs(){
  
  SetStyle();
  gStyle->SetPalette(55, 0);
  
  TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
  canv->SetRightMargin(0.18);
  canv->cd();
  TFile* file_ = TFile::Open("/nfs/dust/cms/user/ffrensch/CMSSW_6_1_1_SLHCphase2tk1/src/auxiliaries/models/out.lightstau1-8TeV-tanbHigh-nnlo.root"); 
  TH2F* mh_old = (TH2F*)file_->Get("h_mh");  
  mh_old->SetTitle("");
  mh_old->SetXTitle("m_{A} [GeV]");
  mh_old->GetXaxis()->SetLabelFont(62);
  mh_old->GetXaxis()->SetTitleFont(62);
  mh_old->GetXaxis()->SetTitleColor(1);
  mh_old->GetXaxis()->SetTitleOffset(1.05);
  mh_old->SetYTitle("tan#beta");
  mh_old->GetYaxis()->SetTitleFont(62);
  mh_old->GetYaxis()->SetLabelFont(62);
  mh_old->GetYaxis()->SetTitleSize(0.05);
  mh_old->GetYaxis()->SetTitleOffset(1.08);
  mh_old->GetYaxis()->SetLabelSize(0.04);
  mh_old->SetZTitle("m_{h} [GeV]");
  mh_old->GetZaxis()->SetTitleFont(62);
  mh_old->GetZaxis()->SetLabelFont(62);
  mh_old->GetZaxis()->SetTitleSize(0.035);
  mh_old->GetZaxis()->SetTitleOffset(1.50);
  mh_old->GetZaxis()->SetLabelSize(0.04);
  mh_old->Draw("colz"); 
  TPaveText* cmsprel  = new TPaveText(0.145, 0.835+0.06, 0.145+0.30, 0.835+0.16, "NDC");
  cmsprel->SetBorderSize(   0 );
  cmsprel->SetFillStyle(    0 );
  cmsprel->SetTextAlign(   12 );
  cmsprel->SetTextSize ( 0.04 );
  cmsprel->SetTextColor(    1 );
  cmsprel->SetTextFont (   62 );
  cmsprel->AddText("MSSM light stau scenario");
  cmsprel->Draw();
  canv->Print("lightstau1.png");
  canv->Print("lightstau1.pdf");

  TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
  canv->SetRightMargin(0.18);
  canv->cd();
  TFile* file_ = TFile::Open("/nfs/dust/cms/user/ffrensch/CMSSW_6_1_1_SLHCphase2tk1/src/auxiliaries/models/out.lightstopmod-8TeV-tanbHigh-nnlo.root"); 
  TH2F* mh_old = (TH2F*)file_->Get("h_mh");  
  mh_old->SetTitle("");
  mh_old->SetXTitle("m_{A} [GeV]");
  mh_old->GetXaxis()->SetLabelFont(62);
  mh_old->GetXaxis()->SetTitleFont(62);
  mh_old->GetXaxis()->SetTitleColor(1);
  mh_old->GetXaxis()->SetTitleOffset(1.05);
  mh_old->SetYTitle("tan#beta");
  mh_old->GetYaxis()->SetTitleFont(62);
  mh_old->GetYaxis()->SetLabelFont(62);
  mh_old->GetYaxis()->SetTitleSize(0.05);
  mh_old->GetYaxis()->SetTitleOffset(1.08);
  mh_old->GetYaxis()->SetLabelSize(0.04);
  mh_old->SetZTitle("m_{h} [GeV]");
  mh_old->GetZaxis()->SetTitleFont(62);
  mh_old->GetZaxis()->SetLabelFont(62);
  mh_old->GetZaxis()->SetTitleSize(0.035);
  mh_old->GetZaxis()->SetTitleOffset(1.50);
  mh_old->GetZaxis()->SetLabelSize(0.04);
  mh_old->Draw("colz");
  TPaveText* cmsprel  = new TPaveText(0.145, 0.835+0.06, 0.145+0.30, 0.835+0.16, "NDC");
  cmsprel->SetBorderSize(   0 );
  cmsprel->SetFillStyle(    0 );
  cmsprel->SetTextAlign(   12 );
  cmsprel->SetTextSize ( 0.04 );
  cmsprel->SetTextColor(    1 );
  cmsprel->SetTextFont (   62 );
  cmsprel->AddText("MSSM light stop scenario");
  cmsprel->Draw();
  canv->Print("lightstopmod.png");
  canv->Print("lightstopmod.pdf");

  TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
  canv->SetRightMargin(0.18);
  canv->cd();
  TFile* file_ = TFile::Open("/nfs/dust/cms/user/ffrensch/CMSSW_6_1_1_SLHCphase2tk1/src/auxiliaries/models/out.mhmodm-8TeV-tanbHigh-nnlo.root"); 
  TH2F* mh_old = (TH2F*)file_->Get("h_mh");  
  mh_old->SetTitle("");
  mh_old->SetXTitle("m_{A} [GeV]");
  mh_old->GetXaxis()->SetLabelFont(62);
  mh_old->GetXaxis()->SetTitleFont(62);
  mh_old->GetXaxis()->SetTitleColor(1);
  mh_old->GetXaxis()->SetTitleOffset(1.05);
  mh_old->SetYTitle("tan#beta");
  mh_old->GetYaxis()->SetTitleFont(62);
  mh_old->GetYaxis()->SetLabelFont(62);
  mh_old->GetYaxis()->SetTitleSize(0.05);
  mh_old->GetYaxis()->SetTitleOffset(1.08);
  mh_old->GetYaxis()->SetLabelSize(0.04);
  mh_old->SetZTitle("m_{h} [GeV]");
  mh_old->GetZaxis()->SetTitleFont(62);
  mh_old->GetZaxis()->SetLabelFont(62);
  mh_old->GetZaxis()->SetTitleSize(0.035);
  mh_old->GetZaxis()->SetTitleOffset(1.50);
  mh_old->GetZaxis()->SetLabelSize(0.04);
  mh_old->Draw("colz");
  TPaveText* cmsprel  = new TPaveText(0.145, 0.835+0.06, 0.145+0.30, 0.835+0.16, "NDC");
  cmsprel->SetBorderSize(   0 );
  cmsprel->SetFillStyle(    0 );
  cmsprel->SetTextAlign(   12 );
  cmsprel->SetTextSize ( 0.04 );
  cmsprel->SetTextColor(    1 );
  cmsprel->SetTextFont (   62 );
  cmsprel->AddText("MSSM m_{h}^{mod-} scenario");
  cmsprel->Draw();
  canv->Print("mhmodm.png");
  canv->Print("mhmodm.pdf");

  TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
  canv->SetRightMargin(0.18);
  canv->cd();
  TFile* file_ = TFile::Open("/nfs/dust/cms/user/ffrensch/CMSSW_6_1_1_SLHCphase2tk1/src/auxiliaries/models/out.mhmodp-8TeV-tanbHigh-nnlo.root"); 
  TH2F* mh_old = (TH2F*)file_->Get("h_mh");  
  mh_old->SetTitle("");
  mh_old->SetXTitle("m_{A} [GeV]");
  mh_old->GetXaxis()->SetLabelFont(62);
  mh_old->GetXaxis()->SetTitleFont(62);
  mh_old->GetXaxis()->SetTitleColor(1);
  mh_old->GetXaxis()->SetTitleOffset(1.05);
  mh_old->SetYTitle("tan#beta");
  mh_old->GetYaxis()->SetTitleFont(62);
  mh_old->GetYaxis()->SetLabelFont(62);
  mh_old->GetYaxis()->SetTitleSize(0.05);
  mh_old->GetYaxis()->SetTitleOffset(1.08);
  mh_old->GetYaxis()->SetLabelSize(0.04);
  mh_old->SetZTitle("m_{h} [GeV]");
  mh_old->GetZaxis()->SetTitleFont(62);
  mh_old->GetZaxis()->SetLabelFont(62);
  mh_old->GetZaxis()->SetTitleSize(0.035);
  mh_old->GetZaxis()->SetTitleOffset(1.50);
  mh_old->GetZaxis()->SetLabelSize(0.04);
  mh_old->Draw("colz");
  TPaveText* cmsprel  = new TPaveText(0.145, 0.835+0.06, 0.145+0.30, 0.835+0.16, "NDC");
  cmsprel->SetBorderSize(   0 );
  cmsprel->SetFillStyle(    0 );
  cmsprel->SetTextAlign(   12 );
  cmsprel->SetTextSize ( 0.04 );
  cmsprel->SetTextColor(    1 );
  cmsprel->SetTextFont (   62 );
  cmsprel->AddText("MSSM m_{h}^{mod+} scenario");
  cmsprel->Draw();
  canv->Print("mhmodp.png");
  canv->Print("mhmodp.pdf");

  TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
  canv->SetRightMargin(0.18);
  canv->cd();
  TFile* file_ = TFile::Open("/nfs/dust/cms/user/ffrensch/CMSSW_6_1_1_SLHCphase2tk1/src/auxiliaries/models/out.mhmax-mu+200-8TeV-tanbHigh-nnlo.root"); 
  TH2F* mh_old = (TH2F*)file_->Get("h_mh");  
  mh_old->SetTitle("");
  mh_old->SetXTitle("m_{A} [GeV]");
  mh_old->GetXaxis()->SetLabelFont(62);
  mh_old->GetXaxis()->SetTitleFont(62);
  mh_old->GetXaxis()->SetTitleColor(1);
  mh_old->GetXaxis()->SetTitleOffset(1.05);
  mh_old->SetYTitle("tan#beta");
  mh_old->GetYaxis()->SetTitleFont(62);
  mh_old->GetYaxis()->SetLabelFont(62);
  mh_old->GetYaxis()->SetTitleSize(0.05);
  mh_old->GetYaxis()->SetTitleOffset(1.08);
  mh_old->GetYaxis()->SetLabelSize(0.04);
  mh_old->SetZTitle("m_{h} [GeV]");
  mh_old->GetZaxis()->SetTitleFont(62);
  mh_old->GetZaxis()->SetLabelFont(62);
  mh_old->GetZaxis()->SetTitleSize(0.035);
  mh_old->GetZaxis()->SetTitleOffset(1.50);
  mh_old->GetZaxis()->SetLabelSize(0.04);
  mh_old->Draw("colz");
  TPaveText* cmsprel  = new TPaveText(0.145, 0.835+0.06, 0.145+0.30, 0.835+0.16, "NDC");
  cmsprel->SetBorderSize(   0 );
  cmsprel->SetFillStyle(    0 );
  cmsprel->SetTextAlign(   12 );
  cmsprel->SetTextSize ( 0.04 );
  cmsprel->SetTextColor(    1 );
  cmsprel->SetTextFont (   62 );
  cmsprel->AddText("MSSM m_{h}^{max} scenario");
  cmsprel->Draw();
  canv->Print("mhmax.png");
  canv->Print("mhmax.pdf");

  TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
  canv->SetRightMargin(0.18);
  canv->cd();
  TFile* file_ = TFile::Open("/nfs/dust/cms/user/ffrensch/CMSSW_6_1_1_SLHCphase2tk1/src/auxiliaries/models/out.tauphobic-8TeV-tanbHigh-nnlo.root"); 
  TH2F* mh_old = (TH2F*)file_->Get("h_mh");  
  mh_old->SetTitle("");
  mh_old->SetXTitle("m_{A} [GeV]");
  mh_old->GetXaxis()->SetLabelFont(62);
  mh_old->GetXaxis()->SetTitleFont(62);
  mh_old->GetXaxis()->SetTitleColor(1);
  mh_old->GetXaxis()->SetTitleOffset(1.05);
  mh_old->SetYTitle("tan#beta");
  mh_old->GetYaxis()->SetRangeUser(1, 50);
  mh_old->GetYaxis()->SetTitleFont(62);
  mh_old->GetYaxis()->SetLabelFont(62);
  mh_old->GetYaxis()->SetTitleSize(0.05);
  mh_old->GetYaxis()->SetTitleOffset(1.08);
  mh_old->GetYaxis()->SetLabelSize(0.04);
  mh_old->SetZTitle("m_{h} [GeV]");
  mh_old->GetZaxis()->SetTitleFont(62);
  mh_old->GetZaxis()->SetLabelFont(62);
  mh_old->GetZaxis()->SetTitleSize(0.035);
  mh_old->GetZaxis()->SetTitleOffset(1.50);
  mh_old->GetZaxis()->SetLabelSize(0.04);
  mh_old->Draw("colz");
  TPaveText* cmsprel  = new TPaveText(0.145, 0.835+0.06, 0.145+0.30, 0.835+0.16, "NDC");
  cmsprel->SetBorderSize(   0 );
  cmsprel->SetFillStyle(    0 );
  cmsprel->SetTextAlign(   12 );
  cmsprel->SetTextSize ( 0.04 );
  cmsprel->SetTextColor(    1 );
  cmsprel->SetTextFont (   62 );
  cmsprel->AddText("MSSM tauphobic scenario");
  cmsprel->Draw();
  canv->Print("tauphobic.png");
  canv->Print("tauphobic.pdf");

  TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
  canv->SetRightMargin(0.18);
  canv->cd();
  TFile* file_ = TFile::Open("/nfs/dust/cms/user/ffrensch/CMSSW_6_1_1_SLHCphase2tk1/src/auxiliaries/models/out.lowmH-8TeV-tanbHigh-nnlo.root"); 
  TH2F* mh_old = (TH2F*)file_->Get("h_mH");  
  mh_old->SetTitle("");
  mh_old->SetXTitle("#mu [GeV]");
  mh_old->GetXaxis()->SetLabelFont(62);
  mh_old->GetXaxis()->SetTitleFont(62);
  mh_old->GetXaxis()->SetTitleColor(1);
  mh_old->GetXaxis()->SetTitleOffset(1.05);
  mh_old->SetYTitle("tan#beta");
  mh_old->GetYaxis()->SetTitleFont(62);
  mh_old->GetYaxis()->SetLabelFont(62);
  mh_old->GetYaxis()->SetTitleSize(0.05);
  mh_old->GetYaxis()->SetTitleOffset(1.08);
  mh_old->GetYaxis()->SetLabelSize(0.04);
  mh_old->SetZTitle("m_{H} [GeV]");
  mh_old->GetZaxis()->SetTitleFont(62);
  mh_old->GetZaxis()->SetLabelFont(62);
  mh_old->GetZaxis()->SetTitleSize(0.035);
  mh_old->GetZaxis()->SetTitleOffset(1.50);
  mh_old->GetZaxis()->SetLabelSize(0.04);
  mh_old->Draw("colz");
  TPaveText* cmsprel  = new TPaveText(0.145, 0.835+0.06, 0.145+0.30, 0.835+0.16, "NDC");
  cmsprel->SetBorderSize(   0 );
  cmsprel->SetFillStyle(    0 );
  cmsprel->SetTextAlign(   12 );
  cmsprel->SetTextSize ( 0.04 );
  cmsprel->SetTextColor(    1 );
  cmsprel->SetTextFont (   62 );
  cmsprel->AddText("MSSM low m_{H} scenario");
  cmsprel->Draw();
  canv->Print("lowmH.png");
  canv->Print("lowmH.pdf"); 

  
  //file_->Close();
}
