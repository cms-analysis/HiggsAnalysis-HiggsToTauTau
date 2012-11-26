#include <map>
#include <iostream>

#include "TH2F.h"
#include "TROOT.h"
#include "TTree.h"
#include "TFile.h"
#include "TGraph.h"
#include "TString.h"

#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"

void scan2D(const char* path, std::string xval="r_ggH", int xbin=10, float xmin=0., float xmax=20., std::string yval="r_bbH", int ybin=10, float ymin=0., float ymax=20., bool mssm=true, bool log=true, bool temp=true)
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
    if(scan->GetBinContent(scan->FindBin(x,y))==0){scan->Fill(x, y, nll);}
  }
  float best_fit=50, best_fit_help, x_save, y_save;
  for(int i=0; i<nevent; ++i){
    limit->GetEvent(i);
    best_fit_help=scan->GetBinContent(scan->FindBin(x,y));
    //std::cout <<scan->GetBinContent(scan->FindBin(x,y)) <<std::endl;
    if (best_fit>=best_fit_help) {best_fit=best_fit_help; x_save=x; y_save=y;
     //  std::cout << "best fit point: " << std::endl;
//       std::cout << "r_ggH: " << x_save << std::endl; 
//       std::cout << "r_bbH: " << y_save << std::endl; 
//       std::cout << "nll: " << best_fit << std::endl; 
//       std::cout << std::endl;
    }
  }  
  std::cout << "best fit point: " << std::endl;
  std::cout << "r_ggH: " << x_save << std::endl; 
  std::cout << "r_bbH: " << y_save << std::endl; 
  std::cout << "nll: " << best_fit << std::endl; 

  std::map<std::pair<std::string, bool>, const char*> axis_titles;
  axis_titles[std::make_pair<std::string, bool>(std::string("r_bbH"), true )] = "#bf{#sigma(gg#rightarrowbb#phi)#timesBR (pb)}";
  axis_titles[std::make_pair<std::string, bool>(std::string("r_ggH"), true )] = "#sigma(gg#rightarrow#phi)#timesBR (pb)";
  axis_titles[std::make_pair<std::string, bool>(std::string("r_ggH"), false)] = "#sigma(gg#rightarrowH)/#sigma(SM)";
  axis_titles[std::make_pair<std::string, bool>(std::string("r_qqH"), false)] = "#bf{#sigma(qq#rightarrowqqH)/#sigma(SM)}";
  axis_titles[std::make_pair<std::string, bool>(std::string("CF"   ), false)] = "#bf{c_{F}}";
  axis_titles[std::make_pair<std::string, bool>(std::string("CV"   ), false)] = "c_{V}";

  TCanvas* canv = new TCanvas("canv", "canv", 600, 600);
  canv->cd();
  if(log) canv->SetLogz();
  canv->SetGridx();
  canv->SetGridy();
  canv->SetRightMargin(0.14);

  TPaveText * label = new TPaveText(0.50, 0.80, 1.0, 0.90, "NDC");
  label->SetBorderSize(   0 );
  label->SetFillStyle(    0 );
  label->SetTextAlign(   12 );
  label->SetTextSize ( 0.05 );
  label->SetTextColor(    1 );
  label->SetTextFont (   62 );
  label->AddText("m_{H}=125 GeV");
  label->Draw();

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
  scan->SetZTitle("#bf{#Delta NLL}");
  scan->GetZaxis()->SetLabelFont(62);
  scan->GetZaxis()->SetTitleSize(0.04);
  scan->GetZaxis()->SetTitleOffset(1.03);
  scan->GetZaxis()->SetLabelSize(0.04);

  scan->SetMinimum(0.);
  //scan->SetMaximum(2);

  /// new draw contours
  double contours[1];
  contours[0] = 1.;      //68%
  contours[1] = 1.92;    //95%.
  scan->SetContour(2, contours);

  // Draw contours as filled regions, and Save points
  scan->Draw("CONT Z LIST");
  canv->Update(); // Needed to force the plotting and retrieve the contours in TGraph


  // Get Contours
  TObjArray *conts = (TObjArray*)gROOT->GetListOfSpecials()->FindObject("contours");

  TCanvas* canv2 = new TCanvas("canv", "canv", 600, 600);
  canv2->cd();
  if (log) canv2->SetLogz();
  canv2->SetGridx();
  canv2->SetGridy();
  canv2->SetRightMargin(0.14);

 //  TPaveText * label2 = new TPaveText(0.50, 0.80, 1.0, 0.90, "NDC");
//   label2->SetBorderSize(   0 );
//   label2->SetFillStyle(    0 );
//   label2->SetTextAlign(   12 );
//   label2->SetTextSize ( 0.05 );
//   label2->SetTextColor(    1 );
//   label2->SetTextFont (   62 );
//   label2->AddText("m_{H}=125 GeV");
//   label2->Draw();

  TH2F* scan2 = new TH2F("scan2", "", xbin, xmin, xmax, ybin, ymin, ymax);
  if(temp){
    int nevent2 = limit->GetEntries();
    for(int i=0; i<nevent2; ++i){
      limit->GetEvent(i);
      if(scan2->GetBinContent(scan2->FindBin(x,y))==0){scan2->Fill(x, y, nll);}
    }
  }
  scan2->SetXTitle(axis_titles[std::pair<std::string, bool>(xval, mssm)]);
  scan2->GetXaxis()->SetLabelFont(62);
  scan2->GetXaxis()->SetTitleFont(62);
  scan2->GetXaxis()->SetTitleColor(1);
  scan2->GetXaxis()->SetTitleOffset(1.05);
  scan2->SetYTitle(axis_titles[std::pair<std::string, bool>(yval, mssm)]);
  scan2->GetYaxis()->SetLabelFont(62);
  scan2->GetYaxis()->SetTitleSize(0.05);
  scan2->GetYaxis()->SetTitleOffset(1.4);
  scan2->GetYaxis()->SetLabelSize(0.05);
  scan2->SetZTitle("#bf{#Delta NLL}");
  scan2->GetZaxis()->SetLabelFont(62);
  scan2->GetZaxis()->SetTitleSize(0.04);
  scan2->GetZaxis()->SetTitleOffset(1.03);
  scan2->GetZaxis()->SetLabelSize(0.04);
  scan2->SetMinimum(0.);
  scan2->Draw("colz");

  TLegend* leg = new TLegend(0.42, 0.70, 0.80, 0.90);
  leg->SetBorderSize( 0 );
  leg->SetFillStyle ( 0 );
  leg->SetFillColor (kWhite);

  if(temp){
  //get and draw contours 
  //std::cout << "conts " << conts->GetEntries() << std::endl;
    for (int ic=0; ic<conts->GetEntries(); ic++) {   
      TList* graphlist = (TList*)conts->At(ic);  
      //std::cout << "graphlist " << graphlist->GetEntries() << std::endl;
      for (int ig=0; ig<graphlist->GetEntries(); ig++) {
	TGraph* gr = (TGraph*)graphlist->At(ig);
	if (ic==0) {
	  //std::cout << "ic " <<  ic << "  ig " << ig << std::endl;
	  gr->SetLineColor(kBlack);
	  gr->SetLineStyle(1);
	  if( ig==graphlist->GetEntries()-1 ) leg->AddEntry(gr, "68% CL contour"  ,  "L" );
	}
	if (ic==1) {
	  //std::cout << "ic " <<  ic << "  ig " << ig << std::endl;
	  gr->SetLineColor(kBlack);
	  gr->SetLineStyle(2);
	  if( ig==graphlist->GetEntries()-1 ) leg->AddEntry(gr, "95% CL contour"  ,  "L" );
	}
	gr->SetLineWidth(3);
	gr->Draw("contsame");
      }
    }
  }
  else{  
    TList* graphlist1 = (TList*)conts->At(1);  
    TGraph* gr1 = (TGraph*)graphlist1->At(0);
    int m=gr1->GetN(); //get ploted array dimention
    double bx[m];
    double by[m];
    //std::cout<<m<<std::endl;
    for(Int_t i=0; i<m; i++) {
      gr1->GetPoint(i,bx[i],by[i]);
      //cout<<i<<"th element of X array: "<<bx[i]<<endl;
      //cout<<i<<"th element of Y array: "<<by[i]<<endl;
    }
    TGraph *newgr1 = new TGraph();
    newgr1->SetPoint(0,0,0);
    for(int i=0; i<m; i++){
      newgr1->SetPoint(i+1, bx[i], by[i]);
    }
    gr1->SetLineStyle(2);
    gr1->SetLineWidth(3);
    gr1->SetLineColor(kBlack);
    newgr1->SetFillColor(kCyan);
    newgr1->Draw("cfsame");
    gr1->Draw("contsame");
    leg->AddEntry(gr1, "95% CL contour"  ,  "L" );
    
    
    TList* graphlist0 = (TList*)conts->At(0);
    TGraph* gr0 = (TGraph*)graphlist0->At(0);
    int n=gr0->GetN(); //get ploted array dimention
    double ax[n];
    double ay[n];
    //std::cout<<n<<std::endl;
    for(Int_t i=0; i<n; i++) {
      gr0->GetPoint(i,ax[i],ay[i]);
      //cout<<i<<"th element of X array: "<<ax[i]<<endl;
      //cout<<i<<"th element of Y array: "<<ay[i]<<endl;
    }
    TGraph *newgr0 = new TGraph();
    newgr0->SetPoint(0,0,0);
    for(int i=0; i<n; i++){
      newgr0->SetPoint(i+1, ax[i], ay[i]);
    }
    gr0->SetLineStyle(1);
    gr0->SetLineWidth(3);
    gr0->SetLineColor(kBlack);
    newgr0->SetFillColor(kBlue);
    newgr0->Draw("cfsame");
    gr0->Draw("contsame");
    leg->AddEntry(gr0, "68% CL contour"  ,  "L" );
  }

  TGraph *bestfit = new TGraph();
  bestfit->SetPoint(0, x_save, y_save);
  bestfit->SetMarkerStyle(34);
  bestfit->SetMarkerSize(3.0);
  bestfit->SetMarkerColor(kBlack);
  bestfit->Draw("Psame");
  leg->AddEntry(bestfit, "best fit point"  ,  "P" );

  leg->Draw("same");

  canv2->Print("scan-ggH-qqH-125.png");
  canv2->Print("scan-ggH-qqH-125.eps");
  canv2->Print("scan-ggH-qqH-125.pdf");
}
