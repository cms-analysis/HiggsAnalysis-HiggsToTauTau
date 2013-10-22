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

void
plottingTanb(TCanvas& canv, TGraphAsymmErrors* plain, TGraphAsymmErrors* plain_low, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* innerBand_low, TGraphAsymmErrors* outerBand, TGraphAsymmErrors* outerBand_low, TGraph* expected, TGraph* expected_low, TGraph* observed, TGraph* observed_low, TGraph* lowerLEP, TGraph* upperLEP, std::map<double, TGraphAsymmErrors*> higgsBands, std::map<std::string, TGraph*> comparisons, std::string& xaxis, std::string& yaxis, TGraph* injected=0, double min=0., double max=60., bool log=false, bool transparent=false)
{
  // set up styles
  canv.cd();
  //canv.SetGridx(1);
  //canv.SetGridy(1);
  if(log){ 
    canv.SetLogy(1); 
    canv.SetLogx(1); 
  }

  // setup the CMS colors
  TColor* obs = new TColor(1501, 0.463, 0.867, 0.957);
  if(transparent) obs->SetAlpha(0.5);
  TColor* lep = new TColor(1502, 0.494, 0.694, 0.298);
  if(transparent) lep->SetAlpha(1);
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
  TH1F* hr = canv.DrawFrame(outerBand->GetX()[0]-shift_label*.01, min, outerBand->GetX()[outerBand->GetN()-1]+.01, max);
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
  upperLEP->SetFillStyle(1001.);
  upperLEP->SetFillColor(lep->GetNumber());
  upperLEP->SetLineColor(ph->GetNumber());
  upperLEP->SetLineStyle(1.);
  upperLEP->SetLineWidth(4.);
  upperLEP->Draw("F");

  lowerLEP->SetFillStyle(1001.);
  lowerLEP->SetFillColor(kWhite);
  lowerLEP->SetLineColor(kWhite);
  lowerLEP->SetLineStyle(1.);
  lowerLEP->SetLineWidth(4.);
  lowerLEP->Draw("F");

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

  if(observed_low){  
    plain_low->SetLineColor(ph->GetNumber());
    plain_low->SetFillStyle(1001.);
    plain_low->SetFillColor(obs->GetNumber());
    //if (!transparent) plain_low->Draw("Fsame"); //for old style comment that one out
    observed_low->SetMarkerStyle(20);
    observed_low->SetMarkerSize(1.0);
    observed_low->SetMarkerColor(kBlack);
    observed_low->SetLineWidth(3.);  
  }

  if(outerBand){
    outerBand->SetFillStyle(1001);
    outerBand->SetFillColor(twosigma->GetNumber()); //kGray
    outerBand->SetLineColor(twosigma->GetNumber());
    outerBand->Draw("3same");
  }
  if(outerBand_low){   
    outerBand_low->SetFillStyle(1001);
    outerBand_low->SetFillColor(twosigma->GetNumber());
    outerBand_low->SetLineColor(twosigma->GetNumber());
    //outerBand_low->Draw("3same"); 
  }

  innerBand->SetFillStyle(1001);
  innerBand->SetFillColor(onesigma->GetNumber()); //kGray+1
  innerBand->SetLineColor(onesigma->GetNumber());
  innerBand->Draw("3same");
  if(innerBand_low){
    innerBand_low->SetFillStyle(1001);
    innerBand_low->SetFillColor(onesigma->GetNumber());
    innerBand_low->SetLineColor(onesigma->GetNumber());
    //innerBand_low->Draw("3same");
  }

  expected->SetLineColor(kGray+2);
  expected->SetLineWidth(3);
  expected->SetLineStyle(1);
  expected->Draw("Lsame");
  if(expected_low){ 
    expected_low->SetLineColor(kGray+2);
    expected_low->SetLineWidth(3);
    expected_low->SetLineStyle(1);
    //expected_low->Draw("Lsame");
  }

  if(observed){;
    if(transparent) plain->Draw("Fsame");
    observed->Draw("Lsame");
  }
  if(observed_low){  
    //if(transparent) plain_low->Draw("Fsame"); //for old style comment that one out
    //observed_low->Draw("Lsame");
  }

  if(injected){
    injected->SetLineColor(kRed+2);
    injected->SetLineWidth(3);
    injected->SetLineStyle(1);
    injected->Draw("Lsame");
  }
  
  int idx=0;
  int coloredBands[] = {kRed, kRed-7, kRed-9}; 
  for(std::map<double,TGraphAsymmErrors*>::reverse_iterator band = higgsBands.rbegin(); band!=higgsBands.rend(); ++band, ++idx){
    //for(std::map<double,TGraphAsymmErrors*>::const_iterator band = higgsBands.begin(); band!=higgsBands.end(); ++band, ++idx){
    band->second->SetLineColor(coloredBands[idx]);
    band->second->SetFillColor(coloredBands[idx]);
    band->second->Draw("3same");
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
    theory1= new TPaveText(0.55, 0.20, 0.9, 0.26, "NDC");
  }
  theory1->SetBorderSize(   0 );
  theory1->SetFillStyle(    0 );
  theory1->SetTextAlign(   12 );
  theory1->SetTextSize ( 0.04 );
  theory1->SetTextColor(    1 );
  theory1->SetTextFont (   62 );
  theory1->AddText("MSSM m_{h}^{max} scenario");
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
  theory2->Draw();

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
  leg->SetHeader("95% CL Excluded:");
  if(observed){ 
    observed->SetFillColor(obs->GetNumber()); 
    leg->AddEntry(observed, "observed", "FL");
    //leg->AddEntry(observed, "SM Higgs injected", "FL");
  }
  if(injected){
    leg->AddEntry(injected , "SM H injected",  "L" );
    //leg->AddEntry((TObject*)0 , "injected",  "" );
    //leg->AddEntry(innerBand, "#pm 1#sigma Asimov","F");
    //if(outerBand){ 
    //  leg->AddEntry(outerBand, "#pm 2#sigma Asimov", "F"); 
    //}
  }
  leg->AddEntry(expected, "expected", "L");
  //if(!injected){
    leg->AddEntry(innerBand, "#pm 1#sigma expected","F");
    if(outerBand){ 
      leg->AddEntry(outerBand, "#pm 2#sigma expected", "F"); 
      //  }
  }
  for(std::map<double,TGraphAsymmErrors*>::const_iterator band = higgsBands.begin(); band!=higgsBands.end(); ++band){
    leg->AddEntry(band->second, TString::Format("m_{h,H}=125GeV #pm %.0fGeV", band->first), "F");
  }
  leg->AddEntry(upperLEP, "LEP", "F");
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
