#include "TH1F.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TPaveText.h"
#include "TGraphAsymmErrors.h"

void
plottingSignificance(TCanvas& canv, TGraph* expected, TGraph* observed, TGraph* unit3, TGraph* unit5, std::string& xaxis, std::string& yaxis, double min=0., double max=5., bool log=false, bool legendOnRight=false)
{
  // set up styles
  canv.cd();
  canv.SetGridx(1);
  canv.SetGridy(1);
  if(log){ 
    canv.SetLogy(1); 
  }

  // draw a frame to define the range
  TH1F* hr=canv.DrawFrame(expected->GetX()[0]-.01, min, expected->GetX()[expected->GetN()-1]+.01, max);
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

  expected->SetLineColor(kBlue);
  expected->SetLineWidth(3);
  expected->SetLineStyle(1);
  expected->Draw("L");

  unit3->SetLineColor(kRed);
  unit3->SetLineWidth(3.);
  unit3->SetLineStyle(11);
  unit3->Draw("Lsame");

  TPaveText * threeSigma = new TPaveText(0.955, 0.575, 1.0, 0.63, "NDC");
  threeSigma->SetBorderSize(   0 );
  threeSigma->SetFillStyle(    0 );
  threeSigma->SetTextAlign(   12 );
  threeSigma->SetTextSize ( 0.04 );
  threeSigma->SetTextColor(    2 );
  threeSigma->SetTextFont (   62 );
  threeSigma->AddText("3#sigma");
  threeSigma->Draw();

  unit5->SetLineColor(kRed);
  unit5->SetLineWidth(3.);
  unit5->SetLineStyle(11);
  unit5->Draw("Lsame");

  TPaveText * fiveSigma = new TPaveText(0.955, 0.635, 1.0, 0.69, "NDC");
  fiveSigma->SetBorderSize(   0 );
  fiveSigma->SetFillStyle(    0 );
  fiveSigma->SetTextAlign(   12 );
  fiveSigma->SetTextSize ( 0.04 );
  fiveSigma->SetTextColor(    2 );
  fiveSigma->SetTextFont (   62 );
  fiveSigma->AddText("5#sigma");
  fiveSigma->Draw();

  if(observed){
    observed->SetMarkerStyle(20);
    observed->SetMarkerSize(1.0);
    observed->SetMarkerColor(kBlack);
    observed->SetLineWidth(3.);
    observed->Draw("PLsame");
  }

  /// add the proper legend
  TLegend* leg = new TLegend(legendOnRight ? 0.5625 : 0.18, 0.80, legendOnRight ? 1.00 : 0.605, 0.90);
  leg->SetBorderSize( 0 );
  leg->SetFillStyle ( 1001 );
  leg->SetFillColor (kWhite);
  if(observed){
    leg->AddEntry(observed, "observed",  "PL");
  }
  leg->AddEntry(expected, "expected",  "L");
  leg->Draw("same");
  //canv.RedrawAxis("g");
  canv.RedrawAxis();
  return;
}
