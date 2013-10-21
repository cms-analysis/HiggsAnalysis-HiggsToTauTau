#include "TH1F.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TPaveText.h"
#include "TGraphAsymmErrors.h"
#include <iostream>

void
plottingLimit(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed, TGraph* unit, std::string& xaxis, std::string& yaxis, TGraph* expected_injected=0, double min=0., double max=5., bool log=false, std::string PLOT=std::string("LIMIT"), std::string injectedMass=std::string("125"), bool legendOnRight=false, std::string extra_label=std::string(""))
{
  // define PLOT type
  bool injected = (PLOT == std::string("INJECTED"));
  bool bestfit  = (PLOT == std::string("BESTFIT" ));
  bool BG_Higgs = (PLOT == std::string("BG_HIGGS"));
  bool mssm_log = (PLOT == std::string("MSSM-LOG"));
  // set up styles
  canv.cd();
  //canv.SetGridx(1);
  //canv.SetGridy(1);
  if(log){ 
    canv.SetLogy(1);
  }
  // for logx the label for x axis values below 100 needs to be slightly shifted to prevent 
  // the label from being printed into the canvas
  int shift_label = 1.;
  if(mssm_log){
    if(observed){ observed->GetX()[0] = observed->GetX()[0]+0.01; }
    if(expected->GetX()[0]<100.){ shift_label = -1.; }
    canv.SetLogx(1); 
  }
  // draw a frame to define the range
  TH1F* hr=canv.DrawFrame(expected->GetX()[0]-shift_label*.01, min, expected->GetX()[expected->GetN()-1]+.01, max);
  // format x axis
  hr->SetXTitle(xaxis.c_str());
  hr->GetXaxis()->SetLabelFont(62);
  hr->GetXaxis()->SetLabelSize(0.045);
  hr->GetXaxis()->SetLabelOffset(0.015);
  hr->GetXaxis()->SetTitleSize(0.05);
  hr->GetXaxis()->SetTitleFont(62);
  hr->GetXaxis()->SetTitleColor(1);
  hr->GetXaxis()->SetTitleOffset(1.05);
  // format y axis
  hr->SetYTitle(yaxis.c_str());
  hr->GetYaxis()->SetLabelFont(62);
  hr->GetYaxis()->SetTitleSize(0.05);
  hr->GetYaxis()->SetTitleOffset(1.30);
  hr->GetYaxis()->SetLabelSize(0.045);
  hr->SetNdivisions(505, "X");
  if(mssm_log){
    hr->SetNdivisions(50005, "X");
    hr->GetXaxis()->SetMoreLogLabels();
    hr->GetXaxis()->SetNoExponent();
    hr->GetXaxis()->SetLabelSize(0.040);
  }
  if(outerBand){
    outerBand->SetLineWidth(1.);
    outerBand->SetLineColor(kBlack);
    if(injected) outerBand->SetFillColor(kAzure-9);
    else if(BG_Higgs) outerBand->SetFillColor(kSpring+5);
    else outerBand->SetFillColor(kYellow);
    outerBand->Draw("3");
  }
  if(innerBand){
    if(bestfit){
      innerBand->SetMarkerColor(kBlack);
      innerBand->SetMarkerSize(1.0);
      innerBand->SetMarkerStyle(20);
      innerBand->SetLineWidth(3.);
      innerBand->SetLineColor(kBlack);
      innerBand->SetFillColor(kGreen);
      innerBand->Draw("3same");
    }
    else{
      innerBand->SetLineWidth(1.);
      innerBand->SetLineColor(kBlack);
      if(injected) innerBand->SetFillColor(kAzure-4);
      else if(BG_Higgs) innerBand->SetFillColor(kGreen+2);
      else innerBand->SetFillColor(kGreen);
      innerBand->Draw("3same");
    }
  }
  if(expected){
    if(bestfit){
      expected->SetLineColor(kBlack);
      expected->SetLineWidth(3);
      expected->SetLineStyle(1);
      expected->SetMarkerColor(kBlack);
      expected->SetMarkerSize(1.0);
      expected->SetMarkerStyle(20);
      expected->Draw("PL");
    }
    else{
      expected->SetLineColor(kRed);
      expected->SetLineWidth(3);
      expected->SetLineStyle(1);
      expected->Draw("L");
    }
  }
  if(unit){
    unit->SetLineColor(kBlue);
    unit->SetLineWidth(3.);
    unit->Draw("Lsame");
  }

  if(expected_injected){
    expected_injected->SetLineColor(kBlue);
    expected_injected->SetLineWidth(3);
    expected_injected->SetLineStyle(1);
    expected_injected->Draw("Lsame");
  }


  if(observed){
    observed->SetMarkerColor(kBlack);
    observed->SetMarkerSize(1.0);
    observed->SetMarkerStyle(20);
    observed->SetLineWidth(3.);
    observed->Draw("PLsame");
  }

  
  TPaveText* extra;
  if(!extra_label.empty()){
    extra = new TPaveText(legendOnRight ? 0.5 : 0.18, 0.60, legendOnRight ? 0.90 : 0.605, 0.70, "NDC");
    extra->SetBorderSize(   0 );
    extra->SetFillStyle (   0 );
    extra->SetTextAlign (  12 );
    extra->SetTextSize  (0.04 );
    extra->SetTextColor (   1 );
    extra->SetTextFont  (  62 );
    extra->AddText(extra_label.c_str());
    extra->Draw();
  }
  // add proper legend
  TLegend* leg = new TLegend(legendOnRight ? 0.5 : 0.18, 0.70, legendOnRight ? 0.90 : 0.605, 0.90);
  leg->SetBorderSize( 0 );
  leg->SetFillStyle( 1001 );
  leg->SetFillColor(kWhite);
  if(observed){
    leg->AddEntry(observed, "observed",  "PL");
    //leg->AddEntry(observed, "Asimov w/ H(125)",  "PL");
  }
  if(expected_injected){
    leg->AddEntry( expected_injected , TString::Format("SM H(%s GeV) injected", injectedMass.c_str()),  "L" );
  }
  if(injected){
    leg->AddEntry( expected , TString::Format("H(%s GeV) injected", injectedMass.c_str()),  "L" );
    if(innerBand){ leg->AddEntry( innerBand, TString::Format("#pm 1#sigma H(%s GeV) injected", injectedMass.c_str()),  "F" ); }
    if(outerBand){ leg->AddEntry( outerBand, TString::Format("#pm 2#sigma H(%s GeV) injected", injectedMass.c_str()),  "F" ); }
  }
  else if(BG_Higgs){
    leg->AddEntry( expected , TString::Format("H(%s GeV) as BG", injectedMass.c_str()),  "L" );
    if(innerBand){ leg->AddEntry( innerBand, TString::Format("#pm 1#sigma H(%s GeV) as BG", injectedMass.c_str()),  "F" ); }
    if(outerBand){ leg->AddEntry( outerBand, TString::Format("#pm 2#sigma H(%s GeV) as BG", injectedMass.c_str()),  "F" ); }  
  }
  else if(bestfit){
    leg->AddEntry( expected , "#sigma/#sigma_{SM} (best fit)",  "PL" );
    if(innerBand){ leg->AddEntry( innerBand, "#pm 1#sigma (best fit)" ,  "PLF" ); }
  }
  else{
    leg->AddEntry( expected , "expected",  "L" );
    if(innerBand){ leg->AddEntry( innerBand, "#pm 1#sigma expected",  "F" ); }
    if(outerBand){ leg->AddEntry( outerBand, "#pm 2#sigma expected",  "F" ); }
  }
  leg->Draw("same");
  //canv.RedrawAxis("g");
  canv.RedrawAxis();
  return;
}
