#include <map>
#include <iostream>

#include "TROOT.h"
#include "TTree.h"
#include "TFile.h"
#include "TGraph.h"
#include "TString.h"
#include "TLegend.h"
#include "TCanvas.h"

#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"

void contourPlot2D(const char* path, const char* name, float xMax=20., float yMax=20., const char* x="ggH_mssm", const char* y="bbH_mssm", const char* label = "Projection, H#rightarrow#tau#tau, #sqrt{s} = 7-8 TeV, L=12 fb^{-1}", std::string descriptionType="MSSM")
{
  SetStyle();

  std::map<const char*, const char*> titles_;
  titles_["ggH_mssm"] = "#sigma(gg#rightarrow #phi)  (pb)";
  titles_["bbH_mssm"] = "#sigma(bb#rightarrow #phi)  (pb)";
  titles_["ggH"     ] = "#sigma(gg#rightarrow H)  (pb)";
  titles_["qqH"     ] = "#sigma(qq#rightarrow H)  (pb)";
  titles_["CV"      ] = "c_{V}";
  titles_["CF"      ] = "c_{F}";
  const char* xtitle = titles_.find(x)==titles_.end() ? x : titles_[x];
  const char* ytitle = titles_.find(y)==titles_.end() ? y : titles_[y];

  TFile* file_ = TFile::Open(path);
  TGraph* exp  = (TGraph*) file_->Get(Form("%s_exp" , name));
  TGraph* cl68 = (TGraph*) file_->Get(Form("%s_cl68", name));
  TGraph* cl95 = (TGraph*) file_->Get(Form("%s_cl95", name));
  TGraph* fit  = (TGraph*) file_->Get(Form("%s_fit" , name));
  
  TCanvas* canv = new TCanvas("canv", "canv", 600, 600);
  canv->SetGridx(); canv->SetGridy();
  TH1F* hr = canv->DrawFrame(0., 0., xMax, yMax);
  hr->GetXaxis()->SetLabelFont(62);
  hr->GetXaxis()->SetTitleFont(62);
  hr->GetXaxis()->SetTitleColor(1);
  hr->GetXaxis()->SetTitleOffset(1.05);
  hr->GetXaxis()->SetTitle(xtitle);

  hr->GetYaxis()->SetNdivisions(505);
  hr->GetYaxis()->SetLabelFont(62);
  hr->GetYaxis()->SetTitleSize(0.05);
  hr->GetYaxis()->SetTitleOffset(1.35);
  hr->GetYaxis()->SetLabelSize(0.05);
  hr->GetYaxis()->SetTitle(ytitle);

  exp->SetMarkerSize(3.);
  exp->SetMarkerColor(2);
  exp ->Draw();
  cl95->Draw("Lsame");
  cl68->Draw("Lsame");
  fit->SetMarkerSize(3.);
  fit->SetMarkerColor(4);
  fit ->Draw("Psame");
  exp ->Draw("Psame");

  CMSPrelim(label, "", 0.15, 0.835);

  /// add the proper legend
  TLegend* leg = new TLegend(0.52, 0.70, 0.90, 0.90);
  leg->SetBorderSize( 0 );
  leg->SetFillStyle ( 0 );
  leg->SetFillColor (kWhite);
  //leg->SetHeader( "95% CL Limits" );
  leg->AddEntry( exp , "injected signal" ,  "P" );
  leg->AddEntry( fit , "best fit value"  ,  "P" );
  leg->AddEntry( cl68, "68% CL contour"  ,  "L" );
  leg->AddEntry( cl95, "95% CL contour"  ,  "L" );
  leg->Draw("same");

  if(descriptionType=="MSSM"){
    TPaveText* pave1  = new TPaveText(0.17, 0.85, 0.46, 0.90, "NDC");
    pave1->SetBorderSize(   0 );
    pave1->SetFillStyle(    0 );
    pave1->SetTextAlign(   12 );
    pave1->SetTextSize ( 0.04 );
    pave1->SetTextColor(    1 );
    pave1->SetTextFont (   62 );
    pave1->AddText("#bf{68% and 95% CL}");
    pave1->Draw();
    
    TPaveText* pave2  = new TPaveText(0.17, 0.80, 0.46, 0.85, "NDC");
    pave2->SetBorderSize(   0 );
    pave2->SetFillStyle(    0 );
    pave2->SetTextAlign(   12 );
    pave2->SetTextSize ( 0.04 );
    pave2->SetTextColor(    1 );
    pave2->SetTextFont (   62 );
    pave2->AddText("#bf{ranges for #sigma #times BR}");
    pave2->Draw();
    
    TPaveText* pave3  = new TPaveText(0.17, 0.75, 0.46, 0.80, "NDC");
    pave3->SetBorderSize(   0 );
    pave3->SetFillStyle(    0 );
    pave3->SetTextAlign(   12 );
    pave3->SetTextSize ( 0.04 );
    pave3->SetTextColor(    1 );
    pave3->SetTextFont (   62 );
    pave3->AddText("#bf{for m(#phi)=130 GeV}");
    pave3->Draw();
  }
  canv->Print(Form("%s.png", name));
  canv->Print(Form("%s.eps", name));
  canv->Print(Form("%s.pdf", name));
}
