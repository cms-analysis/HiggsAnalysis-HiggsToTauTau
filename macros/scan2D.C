#include <map>
#include <iostream>

#include "TH2F.h"
#include "TROOT.h"
#include "TTree.h"
#include "TFile.h"
#include "TGraph.h"
#include "TString.h"

#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"

void scan2D(const char* path, std::string xval="r_ggH", int xbin=10, float xmin=0., float xmax=20., std::string yval="r_bbH", int ybin=10, float ymin=0., float ymax=20., bool mssm=true)
{
  SetStyle();
  TFile* file_ = TFile::Open(path);
  TTree* limit = (TTree*) file_->Get("limit");

  float nll, x, y;
  limit->SetBranchAddress("deltaNLL", &nll );  
  limit->SetBranchAddress(xval.c_str() , &x);  
  limit->SetBranchAddress(yval.c_str() , &y);
  
  TH2F* scan = new TH2F("scan", "", xbin, xmin, xmax, ybin, ymin, ymax);
  int nevent = limit->GetEntries();
  for(int i=0; i<nevent; ++i){
    limit->GetEvent(i);
    scan->Fill(x, y, nll);
  }

  std::map<std::pair<std::string, bool>, const char*> axis_titles;
  axis_titles[std::make_pair<std::string, bool>(std::string("r_bbH"), true )] = "#sigma(gg#rightarrowbb#phi)#timesBR (pb)";
  axis_titles[std::make_pair<std::string, bool>(std::string("r_ggH"), true )] = "#sigma(gg#rightarrow#phi)#timesBR (pb)";
  axis_titles[std::make_pair<std::string, bool>(std::string("r_ggH"), false)] = "#sigma(gg#rightarrowH)/#sigma(SM)";
  axis_titles[std::make_pair<std::string, bool>(std::string("r_qqH"), false)] = "#sigma(qq#rightarrowqqH)/#sigma(SM)";
  axis_titles[std::make_pair<std::string, bool>(std::string("CF"   ), false)] = "c_{F}";
  axis_titles[std::make_pair<std::string, bool>(std::string("CV"   ), false)] = "c_{V}";

  TCanvas* canv = new TCanvas("canv", "canv", 600, 600);
  canv->cd();
  canv->SetGridx();
  canv->SetGridy();
  canv->SetRightMargin(0.14);

  scan->SetXTitle(axis_titles[std::pair<std::string, bool>(xval, mssm)]);
  scan->GetXaxis()->SetLabelFont(62);
  scan->GetXaxis()->SetTitleFont(62);
  scan->GetXaxis()->SetTitleColor(1);
  scan->GetXaxis()->SetTitleOffset(1.05);
  scan->SetYTitle(axis_titles[std::pair<std::string, bool>(yval, mssm)]);
  scan->GetYaxis()->SetLabelFont(62);
  scan->GetYaxis()->SetTitleSize(0.05);
  scan->GetYaxis()->SetTitleOffset(1.12);
  scan->GetYaxis()->SetLabelSize(0.05);
  scan->SetZTitle("#bf{#Delta NLL}");
  scan->GetZaxis()->SetLabelFont(62);
  scan->GetZaxis()->SetTitleSize(0.04);
  scan->GetZaxis()->SetTitleOffset(1.03);
  scan->GetZaxis()->SetLabelSize(0.05);

  //scan->SetMaximum(2);
  scan->Draw("colz");

  canv->Print("scan.png");
  canv->Print("scan.eps");
  canv->Print("scan.pdf");
}
