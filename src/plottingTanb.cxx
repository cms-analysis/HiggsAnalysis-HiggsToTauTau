#include <map>

#include "TH1F.h"
#include "TColor.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TPaveText.h"
#include "TGraphAsymmErrors.h"

void
plottingTanb(TCanvas& canv, TGraphAsymmErrors* plain, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed, TGraph* lowerLEP, TGraph* upperLEP, std::map<double, TGraphAsymmErrors*> higgsBands, std::string& xaxis, std::string& yaxis, double min=0., double max=50., bool log=false)
{
  // set up styles
  canv.cd();
  canv.SetGridx(1);
  canv.SetGridy(1);
  if(log){ 
    canv.SetLogy(1); 
  }

  // setup the CMS colors
  TColor* obs = new TColor(1501, 0.463, 0.867, 0.957);
  TColor* lep = new TColor(1502, 0.494, 0.694, 0.298);

  // draw a frame to define the range
  TH1F* hr = canv.DrawFrame(outerBand->GetX()[0]-.1, min, outerBand->GetX()[outerBand->GetN()-1]+.1, max);
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

  upperLEP->SetFillStyle(1001.);
  upperLEP->SetFillColor(lep->GetNumber());
  upperLEP->SetLineColor(lep->GetNumber());
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
    plain->SetFillStyle(1001.);
    plain->SetFillColor(obs->GetNumber());
    plain->Draw("Fsame");

    observed->SetMarkerStyle(20);
    observed->SetMarkerSize(1.0);
    observed->SetMarkerColor(kBlack);
    observed->SetLineWidth(3.);
  }
  if(outerBand){
    outerBand->SetFillColor(kGray);
    outerBand->SetLineColor(kGray);
    outerBand->SetLineWidth(-702); 
    outerBand->Draw("3same");
  }
  innerBand->SetFillColor(kGray+1);
  innerBand->SetLineColor(kGray+1);
  innerBand->SetLineWidth(-702);
  innerBand->Draw("3same");

  expected->SetLineColor(kGray+2);
  expected->SetLineWidth(3);
  expected->SetLineStyle(1);
  expected->Draw("Lsame");

  if(observed){
    observed->Draw("Lsame");
  }
  
  int idx=0;
  int coloredBands[] = {kRed-9, kRed-7, kRed};
  for(std::map<double,TGraphAsymmErrors*>::const_iterator band = higgsBands.begin(); band!=higgsBands.end(); ++band, ++idx){
    band->second->SetLineColor(coloredBands[idx]);
    band->second->SetFillColor(coloredBands[idx]);
    band->second->Draw("3same");
  }

  TPaveText * theory1 = new TPaveText(0.5, 0.24, 0.9, 0.30, "NDC");
  theory1->SetBorderSize(   0 );
  theory1->SetFillStyle(    0 );
  theory1->SetTextAlign(   12 );
  theory1->SetTextSize ( 0.04 );
  theory1->SetTextColor(    1 );
  theory1->SetTextFont (   62 );
  theory1->AddText("MSSM m_{h}^{max} scenario");
  theory1->Draw();

  TPaveText * theory2 = new TPaveText(0.5, 0.18, 0.9, 0.24, "NDC");
  theory2->SetBorderSize(   0 );
  theory2->SetFillStyle(    0 );
  theory2->SetTextAlign(   12 );
  theory2->SetTextSize ( 0.04 );
  theory2->SetTextColor(    1 );
  theory2->SetTextFont (   62 );
  theory2->AddText("M_{SUSY} = 1 TeV");
  theory2->Draw();

  /// add the proper legend
  TLegend* leg = new TLegend(0.18, 0.60, 0.50, 0.90);
  leg->SetBorderSize(  1 );
  leg->SetFillStyle (1001);
  leg->SetTextSize  (0.04);
  leg->SetTextFont  ( 62 ); 
  leg->SetFillColor (kWhite);
  leg->SetLineColor (kBlack);
  leg->SetHeader("95% CL Excluded:");
  if(observed){ 
    observed->SetFillColor(obs->GetNumber()); 
    leg->AddEntry(observed, "Observed", "FL");
  }
  leg->AddEntry(expected, "Expected", "L");
  leg->AddEntry(innerBand, "#pm 1#sigma Expected","F");
  if(outerBand){ 
    leg->AddEntry(outerBand, "#pm 2#sigma Expected", "F"); 
  }
  for(std::map<double,TGraphAsymmErrors*>::const_iterator band = higgsBands.begin(); band!=higgsBands.end(); ++band){
    leg->AddEntry(band->second, TString::Format("mh=125GeV #pm %.0f GeV", band->first), "F");
  }
  leg->AddEntry(upperLEP, "LEP", "F");
  leg->Draw("same");
  //canv.RedrawAxis("g");
  canv.RedrawAxis();
  return;
}
