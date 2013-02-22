#include <iostream>
#include "TH1.h"
#include "TMath.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TPaveText.h"
#include "Math/ProbFunc.h"

void
plottingLikelihood(TCanvas& canv, TGraph* expected, TGraph* observed, std::string& xaxis, std::string& yaxis, double min, double max, bool log=true, bool legendOnRight=true)
{
  min =     0;
  max = -1000;
  // set up styles
  canv.cd();
  canv.SetGridx(1);
  canv.SetGridy(1);
  if(log){ 
    canv.SetLogy(1); 
  }
  // create the unit line
  TGraph* unit = new TGraph();
  double lMass = 0;
  for(int idx=0; idx<observed->GetN(); ++idx){
    double lVal = observed->GetY()[idx]; 
    if(lVal < min) {min = lVal; lMass = observed->GetX()[idx];}
    if(lVal > max) max = lVal;
   }
  double lMassMin = 0.;
  double lMassMax = 500.;
  bool   iCross = false;
  for(int idx=0; idx<observed->GetN(); ++idx){
    observed->SetPoint(idx,observed->GetX()[idx],observed->GetY()[idx]-min);
    if(expected != 0) expected->SetPoint(idx,expected->GetX()[idx],expected->GetY()[idx]-min);
    std::cout << "====> " << observed->GetX()[idx] << " -- " << observed->GetY()[idx] << std::endl;
    if((observed->GetY()[idx] < 0.5 && !iCross) || (observed->GetY()[idx] > 0.5 && iCross)) {
      double lY1 = observed->GetY()[idx];
      double lY2 = observed->GetY()[idx-1];
      double lX1 = observed->GetX()[idx];
      double lX2 = observed->GetX()[idx-1];
      double lSlope = (lY2-lY1)/(lX2-lX1);
      if(!iCross) lMassMin = -(lY1-0.5)/lSlope + lX1; 
      if( iCross) lMassMax = -(lY1-0.5)/lSlope + lX1; 
      iCross = !iCross;
    }
  }
  max =  TMath::Max(max-min,3.);
  min =  0.;
  std::cout << "Mass : " << lMassMin << " < " << lMass  << " < " << lMassMax << std::endl;
  for(int idx=0; idx<observed->GetN(); ++idx){
    unit->SetPoint(idx, observed->GetX()[idx], min);
  }
  // create sigma lines
  std::vector<TGraph*> sigmas;
   for(unsigned int isigma=0; isigma<2; ++isigma){
    TGraph* sigma = new TGraph();
    for(int idx=0; idx<observed->GetN(); ++idx){
      sigma->SetPoint(idx, observed->GetX()[idx], min+isigma*0.5+0.5);
    }
    sigmas.push_back(sigma);
  }
  // draw a frame to define the range
  TH1F* hr=canv.DrawFrame(observed->GetX()[0]-.01, min, observed->GetX()[observed->GetN()-1]+.01, max);
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
  if(expected != 0) { 
    expected->SetLineColor(kBlue);
    expected->SetLineWidth(3.);
    expected->SetLineStyle(11);
    expected->Draw("L");
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

  TLine *lLow  = new TLine(lMassMin,min,lMassMin,max); lLow ->SetLineColor(kBlue); lLow ->Draw("same");
  TLine *lHigh = new TLine(lMassMax,min,lMassMax,max); lHigh->SetLineColor(kBlue); lHigh->Draw("same");

  /// 3 sigma
  TPaveText * sigma3 = new TPaveText(0.96, (0.5/(max*1.2))+0.08, 1.00, (0.5/max)+0.13, "NDC");
  sigma3->SetBorderSize(   0 );
  sigma3->SetFillStyle(    0 );
  sigma3->SetTextAlign(   12 );
  sigma3->SetTextSize ( 0.04 );
  sigma3->SetTextColor( kRed );
  sigma3->SetTextFont (   62 );
  sigma3->AddText("1#sigma");
  sigma3->Draw("same");

  /// 2 sigma
  TPaveText * sigma2 = new TPaveText(0.96, (1.0/(max*1.2))+0.08, 1.00, (1.0/max)+0.13, "NDC");
  sigma2->SetBorderSize(   0 );
  sigma2->SetFillStyle(    0 );
  sigma2->SetTextAlign(   12 );
  sigma2->SetTextSize ( 0.04 );
  sigma2->SetTextColor( kRed );
  sigma2->SetTextFont (   62 );
  sigma2->AddText("2#sigma");
  sigma2->Draw("same"); 

  /// 1 sigma
  TPaveText * sigma1 = new TPaveText(0.96, (1.5/(max*1.2))+0.08, 1.00, (1.5/max)+0.13, "NDC");
  sigma1->SetBorderSize(   0 );
  sigma1->SetFillStyle(    0 );
  sigma1->SetTextAlign(   12 );
  sigma1->SetTextSize ( 0.04 );
  sigma1->SetTextColor( kRed );
  sigma1->SetTextFont (   62 );
  sigma1->AddText("3#sigma");
  //sigma1->Draw("same"); 

 /// add the proper legend
  //TLegend* leg = new TLegend(legendOnRight ? 0.53 : 0.18, 0.30, legendOnRight ? 0.95 : 0.40, 0.45);
  //leg->SetBorderSize( 0 );
  //leg->SetFillStyle ( 1001 );
  //leg->SetFillColor (kWhite);
  //leg->SetHeader("Local p-value");
  //leg->AddEntry( observed, "p-value observed",  "PL");
  //if(expected != 0) leg->AddEntry( expected, "p-value expected",  "L" );
  //leg->Draw("same");
  //canv.RedrawAxis("g");
  canv.RedrawAxis();
  return;
}
