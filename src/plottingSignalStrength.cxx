#include "TH1F.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TGraphAsymmErrors.h"

void
plottingSignalStrength(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraph* central, TGraph* unit, std::string& xaxis, std::string& yaxis, std::string signal, double min, double max, bool log=false, bool legendOnRight=false)
{
  // set up styles
  canv.cd();
  canv.SetGridx(1);
  canv.SetGridy(1);
  if(log){ 
    canv.SetLogy(1); 
  }

  // draw a frame to define the range
  TH1F* hr=canv.DrawFrame(innerBand->GetX()[0]-.01, min, innerBand->GetX()[innerBand->GetN()-1]+.01, max);
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

  innerBand->SetLineColor(kBlack);
  innerBand->SetLineWidth(1.);
  innerBand->SetFillColor(kGreen);
  innerBand->Draw("3same"); //maybe 4same ... than its smooth, but has a problem at last mass point ...

  central->SetMarkerStyle(20);
  central->SetMarkerSize(0.75);
  central->SetMarkerColor(kBlack);
  central->SetLineWidth(3.);
  central->Draw("PLsame");

  if(unit){
    unit->SetLineColor(kBlue);
    unit->SetLineWidth(3.);
    unit->Draw("Lsame");
  }

  /// add the proper legend
  TLegend* leg = new TLegend(legendOnRight ? 0.5625 : 0.18, 0.70, legendOnRight ? 1.00 : 0.605, 0.90);
  leg->SetBorderSize( 0 );
  leg->SetFillStyle ( 1001 );
  leg->SetFillColor (kWhite);
  leg->SetHeader( TString::Format("Best-fit for %s", signal.c_str()) );
  leg->AddEntry( central  , "Best fit",  "L" );
  leg->AddEntry( innerBand, "68% CL"  ,  "F" );
  leg->Draw("same");
  //canv.RedrawAxis("g");
  canv.RedrawAxis();
  return;
}
