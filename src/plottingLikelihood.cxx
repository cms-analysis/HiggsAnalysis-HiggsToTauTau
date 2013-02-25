#include <iomanip>
#include <sstream>
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
plottingMassScan(TCanvas& canv, TGraph* plot1D, std::string& xaxis, std::string& yaxis, double max, bool log=false)
{
  // set up styles
  canv.cd();
  canv.SetGridx(1);
  canv.SetGridy(1);
  canv.SetRightMargin(0.14);
  if(log){ 
    canv.SetLogy(1); 
  }

  // determine 1sigma uncertainties on mass value
  bool crossed = false;
  double lowerBound = 0.;
  double upperBound = 9999.;
  double minX = 0, minY = 9999.;

  for(int idx=0; idx<plot1D->GetN(); ++idx){
    if(plot1D->GetY()[idx] < minY){
      minX = plot1D->GetX()[idx];
      minY = plot1D->GetY()[idx];
    }
    if((plot1D->GetY()[idx]<TMath::ChisquareQuantile(0.68,1)/2 && !crossed) || (plot1D->GetY()[idx]>TMath::ChisquareQuantile(0.68,1)/2 && crossed)) {
      double y1 = plot1D->GetY()[idx]; double y2 = plot1D->GetY()[idx-1];
      double x1 = plot1D->GetX()[idx]; double x2 = plot1D->GetX()[idx-1];
      double slope = (y2-y1)/(x2-x1);
      if(!crossed) lowerBound = x1-(y1-0.5)/slope;
      if( crossed) upperBound = x1-(y1-0.5)/slope;
      crossed =!crossed;
    }
  }
  std::cout << "-------------------------------------------------" << std::endl;
  std::cout << "Mass estimate: " << minX << " + " << upperBound-minX << " - " << minX-lowerBound << std::endl;
  std::cout << "-------------------------------------------------" << std::endl;

  // create sigma lines
  float quantile[] = {0.68, 0.95};
  std::vector<TGraph*> sigmas;
  for(unsigned int isigma=0; isigma<2; ++isigma){
    TGraph* sigma = new TGraph();
    for(int idx=0; idx<plot1D->GetN(); ++idx){
      sigma->SetPoint(idx, plot1D->GetX()[idx], TMath::ChisquareQuantile(quantile[isigma],1)/2);
    }
    sigmas.push_back(sigma);
  }

  // draw a frame to define the range
  TH1F* hr=canv.DrawFrame(plot1D->GetX()[0]-.01, minY, plot1D->GetX()[plot1D->GetN()-1]+.01, max);
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
  
  plot1D->SetMarkerColor(kBlack);
  plot1D->SetMarkerSize(1.0);
  plot1D->SetMarkerStyle(20);
  plot1D->SetLineWidth(3.);
  plot1D->Draw("PL");
  
  for(std::vector<TGraph*>::const_iterator sigma = sigmas.begin(); sigma!=sigmas.end(); ++sigma){
    (*sigma)->SetLineColor(kRed);
    (*sigma)->SetLineWidth(3.);
    (*sigma)->Draw("Lsame");
  }

  TLegend* leg = new TLegend(0.50, 0.81, 0.92, 0.90);
  leg->SetBorderSize( 0 );
  leg->SetFillStyle ( 0 );
  leg->SetFillColor (kWhite);
  leg->AddEntry(plot1D, "Likelihood scan", "L");
  //leg->Draw("same");

  /// Mass
  TPaveText * mass = new TPaveText(0.2, 0.71, 0.7, 0.81, "NDC");
  mass->SetBorderSize( 0);
  mass->SetFillStyle ( 0);
  //mass->SetTextAlign ( 0);
  //mass->SetTextSize  ( 0.06 );
  mass->SetTextColor( kBlue );
  //mass->SetTextFont (   62 );
  std::stringstream massText; massText << "m_{best-fit} = " << minX << "^{+" << std::setprecision(1) << upperBound-minX << "}" << "_{-" << std::setprecision(1) << minX-lowerBound << "}" << " GeV";
  mass->AddText(massText.str().c_str());
  mass->Draw("same"); 
  
  /// 1 sigma
  TPaveText * sigma1 = new TPaveText(0.88, (0.6/(max*1.2))+0.08, 0.93, (0.6/max)+0.13, "NDC");
  sigma1->SetBorderSize(   0 );
  sigma1->SetFillStyle(    0 );
  sigma1->SetTextAlign(   12 );
  sigma1->SetTextSize ( 0.04 );
  sigma1->SetTextColor( kRed );
  sigma1->SetTextFont (   62 );
  sigma1->AddText("1#sigma");
  sigma1->Draw("same");

  /// 2 sigma
  TPaveText * sigma2 = new TPaveText(0.88, (1.8/(max*1.2))+0.08, 0.93, (1.8/max)+0.13, "NDC");
  sigma2->SetBorderSize(   0 );
  sigma2->SetFillStyle(    0 );
  sigma2->SetTextAlign(   12 );
  sigma2->SetTextSize ( 0.04 );
  sigma2->SetTextColor( kRed );
  sigma2->SetTextFont (   62 );
  sigma2->AddText("2#sigma");
  sigma2->Draw("same"); 

  canv.RedrawAxis();
  return;
}
