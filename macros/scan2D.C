#include <iostream>

#include "TH2F.h"
#include "TROOT.h"
#include "TTree.h"
#include "TFile.h"
#include "TGraph.h"
#include "TString.h"

#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"

void scan2D(const char* path)
{
  SetStyle();
  TFile* file_ = TFile::Open(path);
  TTree* limit = (TTree*) file_->Get("limit");

  float nll, ggH, bbH;
  limit->SetBranchAddress("deltaNLL", &nll);  
  limit->SetBranchAddress("r_bbH"   , &bbH);  
  limit->SetBranchAddress("r_ggH"   , &ggH);
  
  TH2F* scan = new TH2F("scan", "", 40, 0., 20., 40, 0., 20.);
  int nevent = limit->GetEntries();
  for(int i=0; i<nevent; ++i){
    limit->GetEvent(i);
    scan->Fill(ggH, bbH, nll);
  }

  TCanvas* canv = new TCanvas("canv", "canv", 600, 600);
  canv->cd();
  canv->SetGridx();
  canv->SetGridy();
  canv->SetRightMargin(0.14);

  scan->SetXTitle("#sigma(gg#rightarrow #phi)");
  scan->GetXaxis()->SetLabelFont(62);
  scan->GetXaxis()->SetTitleFont(62);
  scan->GetXaxis()->SetTitleColor(1);
  scan->GetXaxis()->SetTitleOffset(1.05);
  scan->SetYTitle("#bf{#sigma(bb#rightarrow bb#phi)}");
  scan->GetYaxis()->SetLabelFont(62);
  scan->GetYaxis()->SetTitleSize(0.05);
  scan->GetYaxis()->SetTitleOffset(1.12);
  scan->GetYaxis()->SetLabelSize(0.05);
  scan->SetZTitle("#bf{#Delta NLL}");
  //scan->GetZaxis()->CenterTitle();
  scan->GetZaxis()->SetLabelFont(62);
  scan->GetZaxis()->SetTitleSize(0.04);
  scan->GetZaxis()->SetTitleOffset(1.03);
  scan->GetZaxis()->SetLabelSize(0.05);

  scan->SetMaximum(10);
  scan->Draw("colz");

  canv->Print("scan.png");
  canv->Print("scan.eps");
  canv->Print("scan.pdf");
}
