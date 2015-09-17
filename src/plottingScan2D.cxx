#include "TCanvas.h"
#include "TGraph.h"
#include "TH2D.h"
#include "TFile.h"
#include "TLegend.h"
#include "TPaveText.h"
#include "TMarker.h"
//#include "httStyle.cxx"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"
#include <iostream>

void plottingScan2D(TCanvas& canv, TH2D* h2d, TGraph* bestfit, TGraph* c68, TGraph* c95, TString file, TMarker* SMexpected, TMarker* SMexpectedLayer, std::string& xaxis, std::string& yaxis, std::string& masslabel, int mass, double xmin, double xmax, double ymin, double ymax, bool temp, bool log) {
  canv.cd();
  SetStyle();
  TFile infile(file);

  h2d->GetXaxis()->SetTitle(xaxis.c_str());  
  if(xmax>0){
    h2d->GetXaxis()->SetRange(h2d->GetXaxis()->FindBin(xmin), h2d->GetXaxis()->FindBin(xmax)-1);
  }
  h2d->GetXaxis()->SetLabelFont(62);
  h2d->GetXaxis()->SetLabelOffset(0.018);
  h2d->GetXaxis()->SetTitleColor(1);
  h2d->GetXaxis()->SetTitleOffset(1.05);
  h2d->GetXaxis()->SetTitleFont(62);
  h2d->GetXaxis()->SetTitleSize(0.055);
  h2d->GetYaxis()->SetTitle(yaxis.c_str());  
  if(ymax>0){
    h2d->GetYaxis()->SetRange(h2d->GetYaxis()->FindBin(ymin), h2d->GetYaxis()->FindBin(ymax)-1);
  }
  h2d->GetYaxis()->SetLabelFont(62);
  h2d->GetYaxis()->SetLabelOffset(0.023);
  h2d->GetYaxis()->SetTitleSize(0.055);
  h2d->GetYaxis()->SetTitleOffset(1.4);
  h2d->GetYaxis()->SetTitleFont(62);
  h2d->GetYaxis()->SetLabelSize(0.04);
  h2d->GetZaxis()->SetTitle("#bf{#Delta NLL}");
  h2d->GetZaxis()->SetLabelFont(62);
  h2d->GetZaxis()->SetTitleSize(0.04);
  h2d->GetZaxis()->SetTitleOffset(1.03);
  h2d->GetZaxis()->SetLabelSize(0.04);
  h2d->SetNdivisions(505, "X");
  h2d->SetNdivisions(505, "Y");
  h2d->SetMinimum(0.);
  h2d->SetNameTitle("","");
  h2d->Draw("AXIS");
  if(temp) h2d->Draw("COLZ");
  
  c95->SetLineStyle(1);
  c95->SetLineColor(kBlack);
  c95->SetLineWidth(3);
  c95->SetFillColor(kBlue-10);
  c68->SetLineStyle(1);
  c68->SetLineColor(kBlack);
  c68->SetLineWidth(3);
  c68->SetFillColor(kBlue-8);
  if(!temp) c95->Draw("F SAME");
  if(!temp) c68->Draw("F SAME");
  c95->Draw("CONT SAME");
  c68->Draw("CONT SAME");
  
  TLegend* leg;
  if(SMexpected && masslabel=="m_{#phi}") leg = new TLegend(0.60, 0.60, 0.90, 0.90);
  else leg = new TLegend(0.60, 0.70, 0.90, 0.90);
  leg->SetBorderSize( 0 );
  leg->SetFillStyle ( 0 );
  leg->SetFillColor (kWhite);
  if(!temp) leg->AddEntry(c95, "95% CL", "F");
  if(!temp) leg->AddEntry(c68, "68% CL", "F");
  if(temp) leg->AddEntry(c95, "95% CL", "L");
  if(temp) leg->AddEntry(c68, "68% CL", "L");
  leg->AddEntry(bestfit, "Best fit", "P"); 
  if(SMexpected && masslabel=="m_{H}"){ leg->AddEntry(SMexpected, "SM", "P"); } 
  if(SMexpected && masslabel=="m_{#phi}"){ leg->AddEntry(SMexpected, "Expected for", "P"); } 
  if(SMexpected && masslabel=="m_{#phi}"){ leg->AddEntry((TObject*)0, "SM H(125 GeV)", ""); }                                                                                          
  leg->Draw("SAME");
  if(SMexpectedLayer){
    TLegend* leg1;
    if(SMexpected && masslabel=="m_{#phi}") leg1 = new TLegend(0.60, 0.60, 0.90, 0.90);
    else leg1 = new TLegend(0.60, 0.70, 0.90, 0.90);
    leg1->SetBorderSize( 0 );
    leg1->SetFillStyle ( 0 );
    leg1->SetFillColor (kWhite);
    if(!temp) leg1->AddEntry(c95, " ", "");
    if(!temp) leg1->AddEntry(c68, " ", "");
    if(temp) leg1->AddEntry(c95, " ", "");
    if(temp) leg1->AddEntry(c68, " ", "");
    leg1->AddEntry(bestfit, " ", " "); 
    if(SMexpected && masslabel=="m_{H}"){ leg1->AddEntry(SMexpectedLayer, " ", "P"); } 
    if(SMexpected && masslabel=="m_{#phi}"){ leg1->AddEntry(SMexpectedLayer, " ", "P"); } 
    if(SMexpected && masslabel=="m_{#phi}"){ leg1->AddEntry((TObject*)0, " ", ""); }                                                                                          
    leg1->Draw("SAME");
  }

  TMarker* MSSMexpected = 0;
  MSSMexpected = new TMarker();
  TMarker* MSSMexpectedLayer = 0;
  MSSMexpectedLayer = new TMarker();
  MSSMexpected->SetMarkerSize(3.0); MSSMexpected->SetMarkerColor(1); MSSMexpected->SetMarkerStyle(29);
  MSSMexpectedLayer->SetMarkerSize(1.8); MSSMexpectedLayer->SetMarkerColor(2); MSSMexpectedLayer->SetMarkerStyle(29);
  TLegend* leg2;
  leg2 = new TLegend(0.15, 0.66, 0.53, 0.80);
  //leg2 = new TLegend(0.52, 0.45, 0.91, 0.59);
  leg2->SetBorderSize( 0 );
  leg2->SetFillStyle ( 0 );
  leg2->SetFillColor (kWhite);
  leg2->AddEntry((TObject*)0, "Expected for", ""); 
  leg2->AddEntry(MSSMexpected, "MSSM m^{h}_{mod+} scenario", "P");  
  leg2->AddEntry((TObject*)0, "m_{A}=500 GeV, tan#beta=30", "");   
  //leg2->Draw("SAME");
  TLegend* leg3;
  leg3 = new TLegend(0.15, 0.66, 0.53, 0.80); 
  //leg3 = new TLegend(0.52, 0.45, 0.91, 0.59);
  leg3->SetBorderSize( 0 );
  leg3->SetFillStyle ( 0 );
  leg3->SetFillColor (kWhite);
  leg3->AddEntry((TObject*)0, "", ""); 
  leg3->AddEntry(MSSMexpectedLayer, " ", "P");  
  leg3->AddEntry((TObject*)0, "", "");    
  //leg3->Draw("SAME");

  TString label = TString::Format("%s = %d GeV", masslabel.c_str(), mass);
  TPaveText* textlabel = new TPaveText(0.18, 0.81, 0.50, 0.90, "NDC");
  textlabel->SetBorderSize(   0 );
  textlabel->SetFillStyle (   0 );
  textlabel->SetTextAlign (  12 );
  textlabel->SetTextSize  (0.04 );
  textlabel->SetTextColor (   1 );
  textlabel->SetTextFont  (  62 );
  textlabel->AddText(label);
  textlabel->SetLabel("");
  textlabel->Draw();
  
  canv.RedrawAxis();
  bestfit->SetMarkerStyle(34);
  bestfit->SetMarkerSize(3.0);
  bestfit->SetMarkerColor(kBlack);
  bestfit->Draw("P SAME");
  
  if(SMexpected && SMexpectedLayer){
    //Hardcoded positions of the SM expectation. Fixed for the 2 diamonds. Must be done after RedrawAxis
    if((int)mass==90  ) {SMexpected->DrawMarker(0,0); SMexpectedLayer->DrawMarker(0,0);}
    if((int)mass==100 ) {SMexpected->DrawMarker(0.676,0.090);SMexpectedLayer->DrawMarker(0.676,0.090);}
    if((int)mass==120 ) {SMexpected->DrawMarker(1.815,0.077);SMexpectedLayer->DrawMarker(1.815,0.077);}
    if((int)mass==125 ) {SMexpected->DrawMarker(1.325,0.057);SMexpectedLayer->DrawMarker(1.325,0.057);}
    if((int)mass==130 ) {SMexpected->DrawMarker(0.979,0.034);SMexpectedLayer->DrawMarker(0.979,0.034);}
    if((int)mass==140 ) {SMexpected->DrawMarker(0.514,0.014);SMexpectedLayer->DrawMarker(0.514,0.014);}
    if((int)mass==160 ) {SMexpected->DrawMarker(0.146,0.009);SMexpectedLayer->DrawMarker(0.146,0.009);}
    if((int)mass==180 ) {SMexpected->DrawMarker(0.014,0.010);SMexpectedLayer->DrawMarker(0.014,0.010);}
    if((int)mass==200 ) {SMexpected->DrawMarker(0,0);SMexpectedLayer->DrawMarker(0,0);}
    if((int)mass==250 ) {SMexpected->DrawMarker(0,0);SMexpectedLayer->DrawMarker(0,0);}
    if((int)mass==300 ) {SMexpected->DrawMarker(0,0);SMexpectedLayer->DrawMarker(0,0);}
    if((int)mass==350 ) {SMexpected->DrawMarker(0,0);SMexpectedLayer->DrawMarker(0,0);}
    if((int)mass==400 ) {SMexpected->DrawMarker(0,0);SMexpectedLayer->DrawMarker(0,0);}
    if((int)mass==450 ) {SMexpected->DrawMarker(0,0);SMexpectedLayer->DrawMarker(0,0);}
    if((int)mass==500 ) {SMexpected->DrawMarker(0,0);SMexpectedLayer->DrawMarker(0,0);}
    if((int)mass==600 ) {SMexpected->DrawMarker(0,0);SMexpectedLayer->DrawMarker(0,0);}
    if((int)mass==700 ) {SMexpected->DrawMarker(0,0);SMexpectedLayer->DrawMarker(0,0);}
    if((int)mass==800 ) {SMexpected->DrawMarker(0,0);SMexpectedLayer->DrawMarker(0,0);}
    if((int)mass==900 ) {SMexpected->DrawMarker(0,0);SMexpectedLayer->DrawMarker(0,0);}
    if((int)mass==1000) {SMexpected->DrawMarker(0,0);SMexpectedLayer->DrawMarker(0,0);}         
  }

    //Hardcoded positions of the MSSM mhmodp mA=500GeV tanb=30 expectation. Fixed for the 2 diamonds. Must be done after RedrawAxis
  //   if((int)mass==90  ) {MSSMexpected->DrawMarker(0,0); MSSMexpectedLayer->DrawMarker(0,0);}
//     if((int)mass==100 ) {MSSMexpected->DrawMarker(0,0); MSSMexpectedLayer->DrawMarker(0,0);}
//     if((int)mass==120 ) {MSSMexpected->DrawMarker(1.204,0);MSSMexpectedLayer->DrawMarker(1.204,0);}
//     if((int)mass==125 ) {MSSMexpected->DrawMarker(0.871,0);MSSMexpectedLayer->DrawMarker(0.871,0);}
//     if((int)mass==130 ) {MSSMexpected->DrawMarker(0.625,0);MSSMexpectedLayer->DrawMarker(0.625,0);}
//     if((int)mass==140 ) {MSSMexpected->DrawMarker(0.275,0);MSSMexpectedLayer->DrawMarker(0.275,0);}
//     if((int)mass==160 ) {MSSMexpected->DrawMarker(0,0);MSSMexpectedLayer->DrawMarker(0,0);}
//     if((int)mass==180 ) {MSSMexpected->DrawMarker(0,0);MSSMexpectedLayer->DrawMarker(0,0);}
//     if((int)mass==200 ) {MSSMexpected->DrawMarker(0,0);MSSMexpectedLayer->DrawMarker(0,0);}
//     if((int)mass==250 ) {MSSMexpected->DrawMarker(0,0);MSSMexpectedLayer->DrawMarker(0,0);}
//     if((int)mass==300 ) {MSSMexpected->DrawMarker(0,0);MSSMexpectedLayer->DrawMarker(0,0);}
//     if((int)mass==350 ) {MSSMexpected->DrawMarker(0.003,0.026);MSSMexpectedLayer->DrawMarker(0.003,0.026);}
//     if((int)mass==400 ) {MSSMexpected->DrawMarker(0.01,0.047);MSSMexpectedLayer->DrawMarker(0.01,0.047);}
//     if((int)mass==450 ) {MSSMexpected->DrawMarker(0.013,0.051);MSSMexpectedLayer->DrawMarker(0.013,0.051);}
//     if((int)mass==500 ) {MSSMexpected->DrawMarker(0.01,0.048);MSSMexpectedLayer->DrawMarker(0.01,0.048);}
//     if((int)mass==600 ) {MSSMexpected->DrawMarker(0,0.027);MSSMexpectedLayer->DrawMarker(0,0.027);}
//     if((int)mass==700 ) {MSSMexpected->DrawMarker(0,0.014);MSSMexpectedLayer->DrawMarker(0,0.014);}
//     if((int)mass==800 ) {MSSMexpected->DrawMarker(0,0.006);MSSMexpectedLayer->DrawMarker(0,0.006);}
//     if((int)mass==900 ) {MSSMexpected->DrawMarker(0,0);MSSMexpectedLayer->DrawMarker(0,0);}
//     if((int)mass==1000) {MSSMexpected->DrawMarker(0,0);MSSMexpectedLayer->DrawMarker(0,0);}   
    
  

  return;
}
