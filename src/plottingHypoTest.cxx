#include <map>

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
plottingHypoTest(TCanvas& canv, TGraphAsymmErrors* plain_1, TGraphAsymmErrors* plain_2, TGraphAsymmErrors* innerBand_1, TGraphAsymmErrors* innerBand_2, TGraphAsymmErrors* innerBand_3, TGraphAsymmErrors* outerBand_1, TGraphAsymmErrors* outerBand_2, TGraphAsymmErrors* outerBand_3, TGraph* expected_1, TGraph* expected_2, TGraph* expected_3, TGraph* observed_1, TGraph* observed_2, TGraph* observed_3, std::map<double, TGraphAsymmErrors*> higgsBands, std::map<std::string, TGraph*> comparisons, std::string& xaxis, std::string& yaxis, std::string& theory, double min=0., double max=50., bool log=false, bool transparent=false, bool expectedOnly=false, bool plotOuterBand=true)
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
  TColor* backgroundColor = gROOT->GetColor(kRed);
  backgroundColor->SetAlpha(0.1);

  // for logx the label for x axis values below 100 needs to be slightly shifted to prevent 
  // the label from being printed into the canvas
  int shift_label = 1.;
  if(log){
    if(observed_1){ observed_1->GetX()[0] = observed_1->GetX()[0]+0.01; }
    if(expected_1->GetX()[0]<100.){ shift_label = -1.; }
  }
  // draw a frame to define the range
  TH1F* hr = canv.DrawFrame(expected_1->GetX()[0]-shift_label*.01, min, expected_1->GetX()[expected_1->GetN()-1]+.01, max);
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

  TGraphAsymmErrors* background = new TGraphAsymmErrors();
  background->SetPoint(0, expected_1->GetX()[0], 50);
  background->SetPointEYlow (0, 50);
  background->SetPointEYhigh(0, 50); 
  for(int ipoint=1; ipoint<expected_1->GetN(); ipoint++){
    background->SetPoint(ipoint, expected_1->GetX()[ipoint], 50); 
    background->SetPointEYlow (ipoint, 50);
    background->SetPointEYhigh(ipoint, 50);
  }
  background->SetPoint(expected_1->GetN(), expected_1->GetX()[expected_1->GetN()-1], 50);
  background->SetPointEYlow (expected_1->GetN(), 50);
  background->SetPointEYhigh(expected_1->GetN(), 50); 
  background->SetFillStyle(1001.);
  background->SetFillColor(backgroundColor->GetNumber());
  background->SetLineColor(ph->GetNumber());
  background->Draw("3");

  int idx=0;
  //int coloredBands[] = {kRed, kRed-7, kRed-9};
  int coloredBands[] = {kWhite, kWhite, kWhite}; 
  for(std::map<double,TGraphAsymmErrors*>::reverse_iterator band = higgsBands.rbegin(); band!=higgsBands.rend(); ++band, ++idx){
    //for(std::map<double,TGraphAsymmErrors*>::const_iterator band = higgsBands.begin(); band!=higgsBands.end(); ++band, ++idx){
    band->second->SetLineColor(coloredBands[idx]);
    band->second->SetFillColor(coloredBands[idx]);
    band->second->Draw("3same");
  }

  if(!expectedOnly){
    plain_1->SetLineColor(ph->GetNumber());
    plain_1->SetFillStyle(1001.);
    plain_1->SetFillColor(obs->GetNumber());
    if (!transparent) plain_1->Draw("3same");
    observed_1->SetMarkerStyle(20);
    observed_1->SetMarkerSize(1.0);
    observed_1->SetMarkerColor(kBlack);
    observed_1->SetLineWidth(3.);
    
    plain_2->SetLineColor(ph->GetNumber());
    plain_2->SetFillStyle(1001.);
    plain_2->SetFillColor(obs->GetNumber());
    if (!transparent) plain_2->Draw("3same");
    observed_2->SetMarkerStyle(20);
    observed_2->SetMarkerSize(1.0);
    observed_2->SetMarkerColor(kBlack);
    observed_2->SetLineWidth(3.);
    observed_3->SetMarkerStyle(20);
    observed_3->SetMarkerSize(1.0);
    observed_3->SetMarkerColor(kBlack);
    observed_3->SetLineWidth(3.);

  }
  
  if(plotOuterBand){
    outerBand_1->SetFillStyle(1001);
    outerBand_1->SetFillColor(twosigma->GetNumber()); //kGray
    outerBand_1->SetLineColor(twosigma->GetNumber());
    outerBand_1->Draw("3same");    
    outerBand_2->SetFillStyle(1001);
    outerBand_2->SetFillColor(twosigma->GetNumber()); //kGray
    outerBand_2->SetLineColor(twosigma->GetNumber());
    outerBand_2->Draw("3same");    
    outerBand_3->SetFillStyle(1001);
    outerBand_3->SetFillColor(twosigma->GetNumber()); //kGray
    outerBand_3->SetLineColor(twosigma->GetNumber());
    //outerBand_3->Draw("3same");
  }
  
  innerBand_1->SetFillStyle(1001);
  innerBand_1->SetFillColor(onesigma->GetNumber()); //kGray+1
  innerBand_1->SetLineColor(onesigma->GetNumber());
  innerBand_1->Draw("3same"); 
  innerBand_2->SetFillStyle(1001);
  innerBand_2->SetFillColor(onesigma->GetNumber()); //kGray+1
  innerBand_2->SetLineColor(onesigma->GetNumber());
  innerBand_2->Draw("3same"); 
  innerBand_3->SetFillStyle(1001);
  innerBand_3->SetFillColor(onesigma->GetNumber()); //kGray+1
  innerBand_3->SetLineColor(onesigma->GetNumber());
  //innerBand_3->Draw("3same"); 
  
  expected_1->SetLineColor(kGray+2);
  expected_1->SetLineWidth(3);
  expected_1->SetLineStyle(1);
  expected_1->Draw("Lsame");
  expected_2->SetLineColor(kGray+2);
  expected_2->SetLineWidth(3);
  expected_2->SetLineStyle(1);
  expected_2->Draw("Lsame");
  expected_3->SetLineColor(kGray+2);
  expected_3->SetLineWidth(3);
  expected_3->SetLineStyle(1);
  //expected_3->Draw("Lsame");
  

  if(!expectedOnly){
    if(transparent) plain_1->Draw("3same");
    observed_1->Draw("Lsame");
    if(transparent) plain_2->Draw("3same"); 
    observed_2->Draw("Lsame"); 
    //observed_3->Draw("Lsame"); 
  }
  
  idx=0;
  std::map<std::string,int> coloredComps;
  coloredComps["arXiv_1211_6956" ] = kOrange+3;
  coloredComps["arXiv_1204_2760" ] = kGreen+4;
  coloredComps["arXiv_1302_2892" ] = kBlue;
  coloredComps["arXiv_1205_5736" ] = kRed;
  coloredComps["HIG_12_052_lower"] = kRed;
  coloredComps["HIG_12_052_upper"] = kRed;
  for(std::map<std::string,TGraph*>::const_iterator comp = comparisons.begin(); comp!=comparisons.end(); ++comp, ++idx){
    comp->second->SetLineColor(coloredComps[comp->second->GetName()]);
    comp->second->SetFillColor(coloredComps[comp->second->GetName()]);
    if(std::string(comp->second->GetName())==std::string("HIG_12_052_upper")){
      comp->second->SetFillStyle(3004);
      comp->second->SetLineWidth(-702);
    }
    else{
      comp->second->SetFillStyle(3005);
      comp->second->SetLineWidth(+702);
    }
    comp->second->Draw("same");
  }
  
  TPaveText* theory1;
  if(log){
    theory1= new TPaveText(0.14, 0.85, 0.9, 0.90, "NDC");
  }
  else{
    theory1= new TPaveText(0.45, 0.20, 0.9, 0.26, "NDC");
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
    theory2 = new TPaveText(0.45, 0.14, 0.9, 0.20, "NDC");
  }
  theory2->SetBorderSize(   0 );
  theory2->SetFillStyle(    0 );
  theory2->SetTextAlign(   12 );
  theory2->SetTextSize ( 0.04 );
  theory2->SetTextColor(    1 );
  theory2->SetTextFont (   62 );
  theory2->AddText("M_{SUSY} = 1 TeV");
  //if(theory=="MSSM m_{h}^{max} scenario") theory2->Draw();

  /// add the proper legend
  TLegend* leg;
  if(log){
    leg = new TLegend(0.68, (!higgsBands.empty() || !comparisons.empty()) ? 0.15 : 0.32, (!higgsBands.empty() || !comparisons.empty()) ? 0.935: 0.935, 0.61);
  }
  else{
    leg = new TLegend(0.18, (!higgsBands.empty() || !comparisons.empty()) ? 0.53 : 0.62, (!higgsBands.empty() || !comparisons.empty()) ? 0.55: 0.50, 0.89);
  }
  leg->SetBorderSize(  1 );
  leg->SetFillStyle (1001);
  leg->SetTextSize  (0.03);
  leg->SetTextFont  ( 62 ); 
  leg->SetFillColor (kWhite);
  leg->SetLineColor (kBlack);
  leg->SetHeader("CL_{S}(MSSM, SM) < 0.05:");
  if(!expectedOnly){ 
    //if(observed){ 
    observed_1->SetFillColor(obs->GetNumber()); 
    leg->AddEntry(observed_1, "observed", "FL");
  }
  leg->AddEntry(expected_1, "expected", "L");
  leg->AddEntry(innerBand_1, "#pm 1#sigma expected","F");
  if(plotOuterBand){ 
    leg->AddEntry(outerBand_1, "#pm 2#sigma expected", "F"); 
  }
  leg->AddEntry(background, "m_{h,H}#neq(125.5#pm3.0)GeV", "F");
  //for(std::map<double,TGraphAsymmErrors*>::const_iterator band = higgsBands.begin(); band!=higgsBands.end(); ++band){
  //  leg->AddEntry(band->second, TString::Format("m_{h,H}=125GeV #pm %.0fGeV", band->first), "F");
  //}
  //if(theory=="MSSM m_{h}^{max} scenario") leg->AddEntry(upperLEP, "LEP", "F");
  for(std::map<std::string,TGraph*>::const_iterator comp = comparisons.begin(); comp!=comparisons.end(); ++comp){
    if(std::string(comp->first) == std::string("EMPTY")) { continue; }
    else if(std::string(comp->first) == std::string("HIG-12-050 exp")) {
      leg->AddEntry(comp->second, (comp->first).c_str(), "L");
    }
    else{
      leg->AddEntry(comp->second, (comp->first).c_str(), "FL");
    }
  }
  leg->Draw("same");
  //canv.RedrawAxis("g");
  canv.RedrawAxis();
  return;
}
