#include "TH1F.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TGraphAsymmErrors.h"

void
plottingLimit(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed, TGraph* unit, std::string& xaxis, std::string& yaxis, double min=0., double max=5., bool log=false, bool injected=false, bool legendOnRight=false)
{
  // set up styles
  canv.cd();
  canv.SetGridx(1);
  canv.SetGridy(1);
  if(log){ 
    canv.SetLogy(1); 
  }

  // draw a frame to define the range
  TH1F* hr=canv.DrawFrame(outerBand->GetX()[0]-.01, min, outerBand->GetX()[outerBand->GetN()-1]+.01, max);
  // format x axis
  hr->SetXTitle(xaxis.c_str());
  hr->GetXaxis()->SetLabelFont(62);
  hr->GetXaxis()->SetLabelSize(0.045);
  hr->GetXaxis()->SetLabelOffset(0.015);
  hr->GetXaxis()->SetTitleFont(62);
  hr->GetXaxis()->SetTitleColor(1);
  hr->GetXaxis()->SetTitleOffset(1.05);
  // format y axis
  hr->SetYTitle(yaxis.c_str());
  hr->GetYaxis()->SetLabelFont(62);
  hr->GetYaxis()->SetTitleSize(0.05);
  hr->GetYaxis()->SetTitleOffset(1.30);
  hr->GetYaxis()->SetLabelSize(0.045);
  hr->SetNdivisions(505);

  outerBand->SetLineWidth(1.);
  outerBand->SetLineColor(kBlack);
  outerBand->SetFillColor(injected ? kAzure-9 : kYellow);
  outerBand->Draw("3");
  
  innerBand->SetLineWidth(1.);
  innerBand->SetLineColor(kBlack);
  innerBand->SetFillColor(injected ? kAzure-4 : kGreen);
  innerBand->Draw("3same");
  
  expected->SetLineColor(kRed);
  expected->SetLineWidth(3);
  expected->SetLineStyle(1);
  expected->Draw("L");

  if(unit){
    unit->SetLineColor(kBlue);
    unit->SetLineWidth(3.);
    unit->Draw("Lsame");
  }
  if(observed){
    observed->SetMarkerStyle(20);
    observed->SetMarkerSize(1.0);
    observed->SetMarkerColor(kBlack);
    observed->SetLineWidth(3.);
    observed->Draw("PLsame");
  }

  // add proper legend
  TLegend* leg = new TLegend(legendOnRight ? 0.5 : 0.18, 0.70, legendOnRight ? 0.90 : 0.605, 0.90);
  leg->SetBorderSize( 0 );
  leg->SetFillStyle( 1001 );
  leg->SetFillColor(kWhite);
  if(observed){
    leg->AddEntry(observed, "observed",  "PL");
  }
  if(injected){
    leg->AddEntry( expected , "signal injected"      ,  "L" );
    leg->AddEntry( innerBand, "#pm 1#sigma injected" ,  "F" );
    leg->AddEntry( outerBand, "#pm 2#sigma injected" ,  "F" );
  }
  else{
    leg->AddEntry( expected , "expected"             ,  "L" );
    leg->AddEntry( innerBand, "#pm 1#sigma expected" ,  "F" );
    leg->AddEntry( outerBand, "#pm 2#sigma expected" ,  "F" );
  }
  leg->Draw("same");
  //canv.RedrawAxis("g");
  canv.RedrawAxis();
  return;
}
