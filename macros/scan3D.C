#include <map>
#include <iostream>

#include "/scratch/hh/dust/naf/cms/user/frensch/CMSSW_5_3_3/src/HiggsAnalysis/HiggsToTauTau/macros/Zesp/base/inc/TStyle.h"
#include "TColor.h"
#include "TH3D.h"
#include "TROOT.h"
#include "TTree.h"
#include "TFile.h"
#include "TGraph.h"
#include "TString.h"
#include "TMath.h"

//#include "/scratch/hh/dust/naf/cms/user/frensch/CMSSW_5_3_3/src/HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"


void scan3D(const char* path, std::string xval="r_ggH", int xbin=10, float xmin=0., float xmax=20., std::string yval="r_bbH", int ybin=10, float ymin=0., float ymax=20., std::string zval="mh", int zbin=10, float zmin=0., float zmax=20., bool mssm=true)
{

  //SetStyle();
  TFile* file_ = TFile::Open(path);
  TTree* limit = (TTree*) file_->Get("limit");

  float nll, x, y; double z;
  limit->SetBranchAddress("deltaNLL", &nll );  
  limit->SetBranchAddress(xval.c_str() , &x);  
  limit->SetBranchAddress(yval.c_str() , &y);
  limit->SetBranchAddress(zval.c_str() , &z);
  
  TH3D* scan = new TH3D("scan", "", xbin, xmin, xmax, ybin, ymin, ymax, zbin, zmin, zmax);
  int nevent = limit->GetEntries();
  for(int i=0; i<nevent; ++i){
    limit->GetEvent(i);
    if (z==130) std::cout << x <<" " <<y << " " <<z << " " <<TMath::Log10(nll) << endl;
    if(scan->GetBinContent(scan->FindBin(x,y,z))==0 && nll>0){
      scan->Fill(x, y, z, TMath::Log10(nll)); 
      //if(z==130) std::cout << TMath::Log10(nll) << std::endl;
    } 
  }
  float best_fit, best_fit_help, x_save, y_save, z_save;
  for(int i=0; i<nevent; ++i){
    limit->GetEvent(i);
    best_fit_help=scan->GetBinContent(scan->FindBin(x,y,z));
    if (best_fit>=best_fit_help) {best_fit=best_fit_help; x_save=x; y_save=y; z_save=z;}
    }

  std::map<std::pair<std::string, bool>, const char*> axis_titles;
  axis_titles[std::make_pair<std::string, bool>(std::string("r_bbH"), true )] = "#bf{#sigma(gg#rightarrowbb#phi)#timesBR (pb)}";
  axis_titles[std::make_pair<std::string, bool>(std::string("r_ggH"), true )] = "#sigma(gg#rightarrow#phi)#timesBR (pb)";
  axis_titles[std::make_pair<std::string, bool>(std::string("r_ggH"), false)] = "#sigma(gg#rightarrowH)/#sigma(SM)";
  axis_titles[std::make_pair<std::string, bool>(std::string("r_qqH"), false)] = "#bf{#sigma(qq#rightarrowqqH)/#sigma(SM)}";
  axis_titles[std::make_pair<std::string, bool>(std::string("CF"   ), false)] = "#bf{c_{F}}";
  axis_titles[std::make_pair<std::string, bool>(std::string("CV"   ), false)] = "#bf{c_{V}}";
  axis_titles[std::make_pair<std::string, bool>(std::string("mh"   ), true)] = "#bf{mA}";

//   TCanvas* canv = new TCanvas("canv", "canv", 600, 600);
//   canv->cd();
//   canv->SetGridx();
//   canv->SetGridy();
  //canv->SetRightMargin(0.14);

  //TPaveText * label = new TPaveText(0.50, 0.80, 1.0, 0.90, "NDC");
  //label->SetBorderSize(   0 );
  //label->SetFillStyle(    0 );
  //label->SetTextAlign(   12 );
  //label->SetTextSize ( 0.05 );
  //label->SetTextColor(    1 );
  //label->SetTextFont (   62 );
  //label->AddText("m_{H}=125 GeV");
  //label->Draw();

  scan->SetXTitle(axis_titles[std::pair<std::string, bool>(xval, mssm)]);
  scan->GetXaxis()->SetLabelFont(62);
  scan->GetXaxis()->SetTitleFont(62);
  scan->GetXaxis()->SetTitleColor(1);
  scan->GetXaxis()->SetTitleOffset(1.05);
  scan->SetYTitle(axis_titles[std::pair<std::string, bool>(yval, mssm)]);
  scan->GetYaxis()->SetLabelFont(62);
  scan->GetYaxis()->SetTitleSize(0.05);
  scan->GetYaxis()->SetTitleOffset(1.4);
  scan->GetYaxis()->SetLabelSize(0.05);
  scan->SetZTitle(axis_titles[std::pair<std::string, bool>(zval, mssm)]);
  scan->GetZaxis()->SetLabelFont(62);
  scan->GetZaxis()->SetTitleSize(0.04);
  scan->GetZaxis()->SetTitleOffset(1.03);
  scan->GetZaxis()->SetLabelSize(0.04);

  scan->SetMinimum(0.);


  //gROOT->SetStyle("Plain");
  gStyle->SetOptStat(111111);
  gStyle->SetOptFit(1);
  gStyle->SetCanvasPreferGL(true);
  gStyle->SetPalette(1);
  gStyle->SetPaletteOpacity(1.);

//   //Double_t wmin = 1;
//   //Double_t wmax = 1;
//   Double_t Red[3]    = { 0.00, 1.00, 1.00};
//   Double_t Green[3]  = { 0.00, 1.00, 0.00};
//   Double_t Blue[3]   = { 1.00, 1.00, 0.00};
//   //Double_t w    = 0.7;
//   //Double_t v    = (w-wmin)/(wmax-wmin);
//   Double_t Length[3] = { 0.00, 0.3, 1.00 };   
//   Int_t nb=50;
//   TColor::CreateGradientColorTable(3,Length,Red,Green,Blue,nb);
  // scan->SetContour(nb); 


  scan->Draw("glcolz"); 

 //  canv->Print("scan-ggH-bbH-mA.png");
//   canv->Print("scan-ggH-bbH-mA.eps");
//   canv->Print("scan-ggH-bbH-mA.pdf"); 
}
