#include <map>
#include <vector>
#include "TH1F.h"
#include "TColor.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TPaveText.h"
#include "TGraphAsymmErrors.h"
#include "TROOT.h"
#include "TLine.h"
#include "TH2D.h"
//#include "TRint.h"

#include <iostream>

void
plottingTanbML(TCanvas& canv, TH2D* h2d, std::string& xaxis, std::string& yaxis, std::string& theory, double min=0., double max=50., bool log=false)
{
  // set up styles
  canv.cd();
  if(log){ 
    canv.SetLogy(1); 
   //  canv.SetLogx(1); 
  }
  canv.SetRightMargin(0.15);
  // setup the CMS colors
  // TColor* obs = new TColor(1501, 0.463, 0.867, 0.957);
//   if(transparent && !Brazilian) obs->SetAlpha(0.5); 
//   TColor* onesigma = gROOT->GetColor(kGray+2);
//   TColor* ph = gROOT->GetColor(kYellow);
//   ph->SetAlpha(0.0);
//   TColor* backgroundColor = gROOT->GetColor(kRed);

  h2d->GetXaxis()->SetTitle(xaxis.c_str()); 
  //h2d->GetXaxis()->SetRange(expected[0]->GetX()[0]-shift_label*.01, expected[0]->GetX()[expected[0]->GetN()-1]+.01);
  h2d->GetXaxis()->SetRangeUser(h2d->GetXaxis()->GetBinLowEdge(1), h2d->GetXaxis()->GetBinLowEdge(h2d->GetNbinsX()-2)+h2d->GetXaxis()->GetBinWidth(h2d->GetNbinsX()-2));
  h2d->GetXaxis()->SetLabelFont(62);
  h2d->GetXaxis()->SetTitleColor(1);
  h2d->GetXaxis()->SetTitleOffset(1.05);
  h2d->GetXaxis()->SetTitleFont(62);
  h2d->GetYaxis()->SetTitle(yaxis.c_str()); 
  h2d->GetYaxis()->SetRangeUser(min, max);
  h2d->GetYaxis()->SetLabelFont(62);
  h2d->GetYaxis()->SetTitleSize(0.05);
  h2d->GetYaxis()->SetTitleOffset(1.30); //1.12
  h2d->GetYaxis()->SetLabelSize(0.05);
  h2d->GetZaxis()->SetTitle("Best Fit (#mu)");
  h2d->GetZaxis()->SetLabelFont(62);
  h2d->GetZaxis()->SetTitleSize(0.04);
  h2d->GetZaxis()->SetTitleOffset(1.03);
  h2d->GetZaxis()->SetLabelSize(0.04);
//   h2d->SetMinimum(0.);
  h2d->SetNameTitle("","");
  h2d->Draw("COLZ");

  TGraphAsymmErrors* emptybackground = new TGraphAsymmErrors();
  emptybackground->SetFillStyle(1001.);
  emptybackground->SetFillColor(kWhite);
  emptybackground->SetLineColor(kWhite);
  
  TPaveText* theory1;
  theory1= new TPaveText(0.24, 0.85, 0.76, 0.885, "NDC");
  theory1->SetBorderSize(   0 );
  theory1->SetFillStyle(    0 );
  theory1->SetTextAlign(   12 );
  theory1->SetTextSize ( 0.04);
  theory1->SetTextColor(    1 );
  theory1->SetTextFont (   62 );
  theory1->AddText(theory.c_str());

  /// add the proper legend
 //  TLegend* leg = new TLegend(0.08, 0.79, 0.61, 0.945);
//   leg->SetNColumns(2);
//   leg->SetBorderSize(  0 );
//   leg->SetFillStyle (1001);
//   leg->SetTextSize  (0.03);
//   leg->SetTextFont  ( 62 ); 
//   leg->SetFillColor (kWhite);
//   leg->SetLineColor (kBlack);
//   leg->SetHeader("Best Fit");
//   leg->Draw("same");

  theory1->Draw("same");

  canv.RedrawAxis();
  return;
}
