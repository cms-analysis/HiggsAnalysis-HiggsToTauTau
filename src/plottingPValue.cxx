#include "TH1.h"
#include "TMath.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TGraphAsymmErrors.h"
#include "TPaveText.h"
#include "Math/ProbFunc.h"

void
plottingPValue(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed, std::string& xaxis, std::string& yaxis, double min, double max, bool log=true, bool legendOnRight=true)
{
  // set up styles
  canv.cd();
  //canv.SetGridx(1);
  //canv.SetGridy(1);
  if(log){ 
    canv.SetLogy(1); 
  }

  // create the unit line
  TGraph* unit = new TGraph();
  for(int idx=0; idx<expected->GetN(); ++idx){
    unit->SetPoint(idx, expected->GetX()[idx], 1.);
  }
  // create sigma lines
  std::vector<TGraph*> sigmas;
  for(unsigned int isigma=0; isigma<5; ++isigma){
    TGraph* sigma = new TGraph();
    for(int idx=0; idx<expected->GetN(); ++idx){
      sigma->SetPoint(idx, expected->GetX()[idx], ROOT::Math::normal_cdf_c(isigma+1));
    }
    sigmas.push_back(sigma);
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
  hr->GetYaxis()->SetTitleFont(62);
  hr->GetYaxis()->SetTitleSize(0.05);
  hr->GetYaxis()->SetTitleOffset(1.30);
  hr->GetYaxis()->SetLabelSize(0.045);

  bool FIRST = true;
  if(outerBand){
    outerBand->SetLineWidth(1.);
    outerBand->SetLineColor(kBlack);
    outerBand->SetFillColor(kRed-10);
    if(FIRST){
      FIRST = false;
      outerBand->Draw("3");
    }
    else{
      outerBand->Draw("3same");
    }
  }

  if(innerBand){
    innerBand->SetLineWidth(1.);
    innerBand->SetLineColor(kBlack);
    innerBand->SetFillColor(kRed-9);
    if(FIRST){
      FIRST = false;
      innerBand->Draw("3");
    }
    else{
      innerBand->Draw("3same");
    }
  }

  expected->SetLineColor(kBlue);
  expected->SetLineWidth(3.);
  expected->SetLineStyle(11);
  if(not(innerBand && outerBand)){ if(FIRST){
    FIRST = false;
    expected->Draw("L");
  }
  else{
    expected->Draw("Lsame");
  }
  }

  observed->SetMarkerStyle(20);
  observed->SetMarkerSize(1.0);
  observed->SetMarkerColor(kBlack);
  observed->SetLineWidth(3.);
  observed->Draw("PLsame");

  unit->SetLineColor(kBlue);
  unit->SetLineWidth(3.);
  unit->Draw("Lsame");

  for(std::vector<TGraph*>::const_iterator sigma = sigmas.begin(); sigma!=sigmas.end(); ++sigma){
    (*sigma)->SetLineColor(kRed);
    (*sigma)->SetLineWidth(3.);
    (*sigma)->Draw("Lsame");
  }

  /// 5 sigma
  TPaveText * sigma5 = new TPaveText(0.96, 0.38, 1.00, 0.43, "NDC");
  sigma5->SetBorderSize(   0 );
  sigma5->SetFillStyle(    0 );
  sigma5->SetTextAlign(   12 );
  sigma5->SetTextSize ( 0.04 );
  sigma5->SetTextColor( kRed );
  sigma5->SetTextFont (   62 );
  sigma5->AddText("5#sigma");
  sigma5->Draw("same");

  /// 4 sigma
  TPaveText * sigma4 = new TPaveText(0.96, 0.54, 1.00, 0.59, "NDC");
  sigma4->SetBorderSize(   0 );
  sigma4->SetFillStyle(    0 );
  sigma4->SetTextAlign(   12 );
  sigma4->SetTextSize ( 0.04 );
  sigma4->SetTextColor( kRed );
  sigma4->SetTextFont (   62 );
  sigma4->AddText("4#sigma");
  sigma4->Draw("same");

  /// 3 sigma
  TPaveText * sigma3 = new TPaveText(0.96, 0.67, 1.00, 0.72, "NDC");
  sigma3->SetBorderSize(   0 );
  sigma3->SetFillStyle(    0 );
  sigma3->SetTextAlign(   12 );
  sigma3->SetTextSize ( 0.04 );
  sigma3->SetTextColor( kRed );
  sigma3->SetTextFont (   62 );
  sigma3->AddText("3#sigma");
  sigma3->Draw("same");

  /// 2 sigma
  TPaveText * sigma2 = new TPaveText(0.96, 0.76, 1.00, 0.81, "NDC");
  sigma2->SetBorderSize(   0 );
  sigma2->SetFillStyle(    0 );
  sigma2->SetTextAlign(   12 );
  sigma2->SetTextSize ( 0.04 );
  sigma2->SetTextColor( kRed );
  sigma2->SetTextFont (   62 );
  sigma2->AddText("2#sigma");
  sigma2->Draw("same"); 

  /// 1 sigma
  TPaveText * sigma1 = new TPaveText(0.96, 0.84, 1.00, 0.88, "NDC");
  sigma1->SetBorderSize(   0 );
  sigma1->SetFillStyle(    0 );
  sigma1->SetTextAlign(   12 );
  sigma1->SetTextSize ( 0.04 );
  sigma1->SetTextColor( kRed );
  sigma1->SetTextFont (   62 );
  sigma1->AddText("1#sigma");
  sigma1->Draw("same"); 

 /// add the proper legend
  TLegend* leg;
  if(innerBand && outerBand){
    leg = new TLegend(0.18, 0.16, 0.75, 0.28);
    //leg->SetNColumns(2);
  }
  else { leg = new TLegend(legendOnRight ? 0.45 : 0.18, 0.16, legendOnRight ? 0.90 : 0.45, 0.32); }
  leg->SetBorderSize( 0 );
  leg->SetFillStyle ( 1001 );
  leg->SetFillColor (kWhite);
  //leg->SetHeader("Local p-value");
  leg->AddEntry( observed, "p-value observed",  "PL");
  if(not(innerBand && outerBand)){ leg->AddEntry( expected, "expected for SM H(m_{H})",  "L" );}
  if(innerBand){ leg->AddEntry( innerBand, "#pm 1#sigma expected for SM H(125 GeV)",  "F" ); }
  if(outerBand){ leg->AddEntry( outerBand, "#pm 2#sigma expected for SM H(125 GeV)",  "F" ); }
  leg->Draw("same");
  //canv.RedrawAxis("g");
  canv.RedrawAxis();
  return;
}
