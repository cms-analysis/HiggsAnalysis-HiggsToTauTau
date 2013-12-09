#include "TH1F.h"
#include "TColor.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TPaveText.h"
#include "TGraphAsymmErrors.h"
#include "TROOT.h"
//#include "TRint.h"

#include <iostream>

void
plottingHypoTest(TCanvas& canv, TGraphAsymmErrors* plain, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed, std::string& xaxis, std::string& yaxis, std::string& theory, double min=0., double max=50., bool log=false, bool transparent=false)
{
  // set up styles
  canv.cd();
  if(log){ 
    canv.SetLogy(1); 
    canv.SetLogx(1); 
  }
  
  // setup the CMS colors
  TColor* obs = new TColor(1501, 0.463, 0.867, 0.957);
  if(transparent) obs->SetAlpha(0.5);
  TColor* twosigma = gROOT->GetColor(kGray);
  if(transparent) twosigma->SetAlpha(0.5);
  TColor* onesigma = gROOT->GetColor(kGray+1);
  if(transparent) onesigma->SetAlpha(0.5);
  TColor* ph = gROOT->GetColor(kYellow);
  ph->SetAlpha(0.0);

  // for logx the label for x axis values below 100 needs to be slightly shifted to prevent 
  // the label from being printed into the canvas
  int shift_label = 1.;
  if(log){
    if(observed){ observed->GetX()[0] = observed->GetX()[0]+0.01; }
    if(expected->GetX()[0]<100.){ shift_label = -1.; }
  }
  // draw a frame to define the range
  TH1F* hr = canv.DrawFrame(expected->GetX()[0]-shift_label*.01, min, expected->GetX()[expected->GetN()-1]+.01, max);
  // format x axis
  hr->SetXTitle(xaxis.c_str());
  hr->GetXaxis()->SetLabelFont(62);
  hr->GetXaxis()->SetTitleFont(62);
  hr->GetXaxis()->SetTitleColor(1);
  hr->GetXaxis()->SetTitleOffset(1.05);
  // format y axis
  hr->SetYTitle(yaxis.c_str());
  hr->GetYaxis()->SetLabelFont(62);
  hr->GetYaxis()->SetTitleSize(0.05);
  hr->GetYaxis()->SetTitleOffset(1.12);
  hr->GetYaxis()->SetLabelSize(0.05);
  if(log){
    hr->SetNdivisions(50005, "X");
    hr->GetXaxis()->SetMoreLogLabels();
    hr->GetXaxis()->SetNoExponent();
    hr->GetXaxis()->SetLabelSize(0.040);
  }

  if(observed){
    plain->SetLineColor(ph->GetNumber());
    plain->SetFillStyle(1001.);
    plain->SetFillColor(obs->GetNumber());
    if (!transparent) plain->Draw("Fsame");
    observed->SetMarkerStyle(20);
    observed->SetMarkerSize(1.0);
    observed->SetMarkerColor(kBlack);
    observed->SetLineWidth(3.);
  }
  
  if(outerBand){
    outerBand->SetFillStyle(1001);
    outerBand->SetFillColor(twosigma->GetNumber()); //kGray
    outerBand->SetLineColor(twosigma->GetNumber());
    outerBand->Draw("3same");
  }
  
  innerBand->SetFillStyle(1001);
  innerBand->SetFillColor(onesigma->GetNumber()); //kGray+1
  innerBand->SetLineColor(onesigma->GetNumber());
  innerBand->Draw("3same");
  
  expected->SetLineColor(kGray+2);
  expected->SetLineWidth(3);
  expected->SetLineStyle(1);
  expected->Draw("Lsame");

  if(observed){;
    if(transparent) plain->Draw("Fsame");
    observed->Draw("Lsame");
  }
  
  TPaveText* theory1;
  if(log){
    theory1= new TPaveText(0.14, 0.85, 0.9, 0.90, "NDC");
  }
  else{
    theory1= new TPaveText(0.55, 0.20, 0.9, 0.26, "NDC");
  }
  theory1->SetBorderSize(   0 );
  theory1->SetFillStyle(    0 );
  theory1->SetTextAlign(   12 );
  theory1->SetTextSize ( 0.04 );
  theory1->SetTextColor(    1 );
  theory1->SetTextFont (   62 );
  theory1->AddText(theory.c_str());
  theory1->Draw();

  TPaveText* theory2;
  if(log){
    theory2 = new TPaveText(0.53, 0.85, 0.9, 0.90, "NDC");
  }
  else{
    theory2 = new TPaveText(0.55, 0.14, 0.9, 0.20, "NDC");
  }
  theory2->SetBorderSize(   0 );
  theory2->SetFillStyle(    0 );
  theory2->SetTextAlign(   12 );
  theory2->SetTextSize ( 0.04 );
  theory2->SetTextColor(    1 );
  theory2->SetTextFont (   62 );
  theory2->AddText("M_{SUSY} = 1 TeV");
  if(theory=="MSSM m_{h}^{max} scenario") theory2->Draw();

  /// add the proper legend
  TLegend* leg;
  if(log){
    leg = new TLegend(0.68, 0.32, 0.935, 0.61);
  }
  else{
    leg = new TLegend(0.18, 0.62, 0.50, 0.89);
  }
  leg->SetBorderSize(  1 );
  leg->SetFillStyle (1001);
  leg->SetTextSize  (0.03);
  leg->SetTextFont  ( 62 ); 
  leg->SetFillColor (kWhite);
  leg->SetLineColor (kBlack);
  leg->SetHeader("95% CL Excluded:");
  if(observed){ 
    observed->SetFillColor(obs->GetNumber()); 
    leg->AddEntry(observed, "observed", "FL");
  }
  leg->AddEntry(expected, "expected", "L");
  leg->AddEntry(innerBand, "#pm 1#sigma expected","F");
  if(outerBand){ 
    leg->AddEntry(outerBand, "#pm 2#sigma expected", "F"); 
  }
  leg->Draw("same");
  //canv.RedrawAxis("g");
  canv.RedrawAxis();
  return;
}
