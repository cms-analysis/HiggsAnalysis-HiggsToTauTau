#include <iomanip>
#include <sstream>
#include <iostream>
#include "TH1.h"
#include "TF1.h"
#include "TMath.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TGraphAsymmErrors.h"
#include "TPaveText.h"
#include "Math/ProbFunc.h"

void plottingMassEstimate(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed, std::string& xaxis, std::string& yaxis, double max, bool log=false, bool parabolic=false)
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
  double fitLowerBound = 0.;
  double fitUpperBound = 9999.;
  double fitMinX = 0, fitMinY = 9999.;

  
  // calculate the DeltaNLL for the expected
  TGraph *newexpected = new TGraph();
  for(int idx=0; idx<expected->GetN(); ++idx){
    newexpected->SetPoint(idx,expected->GetX()[idx],expected->GetY()[idx]-TMath::MinElement(expected->GetN(),expected->GetY()));
  }
  for(int idx=0; idx<observed->GetN(); ++idx){
    if(observed->GetY()[idx] < minY){
      minX = observed->GetX()[idx];
      minY = observed->GetY()[idx];
    }
    if((observed->GetY()[idx]<TMath::ChisquareQuantile(0.68,1)/2 && !crossed) || (observed->GetY()[idx]>TMath::ChisquareQuantile(0.68,1)/2 && crossed)) {
      double y1 = observed->GetY()[idx]; double y2 = observed->GetY()[idx-1];
      double x1 = observed->GetX()[idx]; double x2 = observed->GetX()[idx-1];
      double slope = (y2-y1)/(x2-x1);
      if(!crossed) lowerBound = x1-(y1-0.5)/slope;
      if( crossed) upperBound = x1-(y1-0.5)/slope;
      crossed =!crossed;
    }
  }  
  if(parabolic)
  {
    float min=-90000;
    float max=90000;
    for(int idx=0; idx<observed->GetN(); ++idx) {
      if(observed->GetY()[idx]<2 && observed->GetX()[idx]>min) {
        min=observed->GetX()[idx];
      }
      if(observed->GetY()[idx]<2 && observed->GetX()[idx]<max) {
        max=observed->GetX()[idx];
      }
    }
    double fitLower = max;
    double fitUpper = min;

    observed->Fit("pol2","R","",lowerBound-(minX-lowerBound),upperBound+(upperBound-minX));
    int nStep = 1000;
    double step = (fitUpper-fitLower)/nStep;
    crossed = false;
    for(int idx = 0; idx < nStep; idx++) {
      double pNLL = observed->GetFunction("pol2")->Eval(idx*step + fitLower);
      if(pNLL < fitMinY){
        fitMinX = idx*step + fitLower;
        fitMinY = pNLL;
      } 
     if((pNLL<TMath::ChisquareQuantile(0.68,1)/2 && !crossed) || (pNLL>TMath::ChisquareQuantile(0.68,1)/2 && crossed)) {
        double y1 = pNLL;                double y2 = observed->GetFunction("pol2")->Eval((idx-1.)*step + fitLower);
        double x1 = idx*step + fitLower; double x2 = (idx-1.)*step + fitLower;
        double slope = (y2-y1)/(x2-x1);
        if(!crossed) fitLowerBound = x1-(y1-0.5)/slope;
        if( crossed) fitUpperBound = x1-(y1-0.5)/slope;
        crossed =!crossed;
      }
    }
  }

  std::cout << "-------------------------------------------------" << std::endl;
  std::cout << "Linear    Mass estimate: " << minX    << " + " << upperBound   -minX      << " - " << minX   -lowerBound    << std::endl;
 if(parabolic) { std::cout << "Quadratic Mass estimate: " << fitMinX << " + " << fitUpperBound-fitMinX   << " - " << fitMinX-fitLowerBound << std::endl;}
  std::cout << "-------------------------------------------------" << std::endl;
 TF1 * fit_function = NULL;
 if(parabolic)
 {
   minX = fitMinX;
   minY = fitMinY;
   upperBound = fitUpperBound;
   lowerBound = fitLowerBound;
   fit_function= observed->GetFunction("pol2");

 }
   // create sigma lines
  double quantile[] = {1-2*ROOT::Math::normal_cdf_c(1,1,0), 1-2*ROOT::Math::normal_cdf_c(2,1,0)};
  std::vector<TGraph*> sigmas;
  for(unsigned int isigma=0; isigma<2; ++isigma){
    TGraph* sigma = new TGraph();
    for(int idx=0; idx<observed->GetN(); ++idx){
      sigma->SetPoint(idx, observed->GetX()[idx], TMath::ChisquareQuantile(quantile[isigma],1)/2);
    }
    sigmas.push_back(sigma);
  }

  // draw a frame to define the range
  TH1F* hr=canv.DrawFrame(observed->GetX()[0]-.01, minY, observed->GetX()[observed->GetN()-1]+.01, max);
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
  hr->GetYaxis()->SetTitleFont(62);
  hr->GetYaxis()->SetTitleColor(1);
  hr->GetYaxis()->SetLabelSize(0.045);
  hr->SetNdivisions(505);
  
  outerBand->SetLineWidth(1.);
  outerBand->SetLineColor(kBlack);
  outerBand->SetFillColor(kAzure-9);
  //convert Delta NLL to 2*Delta NLL (plotting convention)
  for (int i=0;i<outerBand->GetN();i++) {
    outerBand->GetY()[i] *= 2;
    outerBand->SetPointError(i,outerBand->GetErrorXlow(i),outerBand->GetErrorXhigh(i),outerBand->GetErrorYlow(i)*2,outerBand->GetErrorYhigh(i)*2);
  }
  outerBand->Draw("3");

  innerBand->SetLineWidth(1.);
  innerBand->SetLineColor(kBlack);
  innerBand->SetFillColor(kAzure-4);
  //convert Delta NLL to 2*Delta NLL (plotting convention)
  for (int i=0;i<innerBand->GetN();i++) { 
    innerBand->GetY()[i] *= 2;
    innerBand->SetPointError(i,innerBand->GetErrorXlow(i),innerBand->GetErrorXhigh(i),innerBand->GetErrorYlow(i)*2,innerBand->GetErrorYhigh(i)*2);
  }
  innerBand->Draw("3same");

  canv.RedrawAxis();
  
  newexpected->SetLineColor(kBlue);
  newexpected->SetLineWidth(3.);
  newexpected->SetLineStyle(11);
  //convert Delta NLL to 2*Delta NLL (plotting convention)
  for (int i=0;i<newexpected->GetN();i++) newexpected->GetY()[i] *= 2;
  newexpected->Draw("Lsame");
  
  observed->SetMarkerStyle(20);
  observed->SetMarkerSize(1.0);
  observed->SetMarkerColor(kBlack);
  observed->SetLineWidth(3.);
  //convert Delta NLL to 2*Delta NLL (plotting convention)
  for (int i=0;i<observed->GetN();i++) observed->GetY()[i] *= 2;
  observed->GetFunction("pol2")->SetBit(TF1::kNotDraw);
  observed->Draw("PLsame");
  TF1 * fit_function_new=NULL;
  if(parabolic)
  {
    // A messy hack to get the fit function to double its y axis also
    fit_function_new= new TF1("fit_function_new", "pol2");
    fit_function_new->SetParameters(2*fit_function->GetParameter(0), 2*fit_function->GetParameter(1), 2*fit_function->GetParameter(2));
    fit_function_new->SetRange(lowerBound-(minX-lowerBound),upperBound+(upperBound-minX));
    fit_function_new->SetLineStyle(7);
    fit_function_new->SetLineColor(kRed-4);
    fit_function_new->SetLineStyle(7);
    fit_function_new->SetLineWidth(3);
    fit_function_new->Draw("Lsame");
  }

  for(std::vector<TGraph*>::const_iterator sigma = sigmas.begin(); sigma!=sigmas.end(); ++sigma){
    (*sigma)->SetLineColor(kGray+2);
    (*sigma)->SetLineWidth(3.);
  //convert Delta NLL to 2*Delta NLL (plotting convention)
    for (int i=0;i<(*sigma)->GetN();i++) (*sigma)->GetY()[i] *= 2;
    (*sigma)->Draw("Lsame");
  }

  TLegend* leg = new TLegend(0.45, 0.73, 0.85, 0.90);
  leg->SetBorderSize( 0 );
  leg->SetFillStyle ( 0 );
  leg->SetFillColor (kWhite);
  leg->AddEntry(observed, "Observed",  "PL");
  if(parabolic){ leg->AddEntry( fit_function_new, "Parabolic fit",  "L" ); }
  leg->AddEntry( newexpected , "H (125 GeV) Expected",  "L" );
  leg->AddEntry( innerBand, "#pm 1#sigma Expected",  "F" ); 
  leg->AddEntry( outerBand, "#pm 2#sigma Expected",  "F" ); 
  leg->Draw("same");

  /// Mass
  TPaveText * mass = new TPaveText(0.45, 0.66, 0.75, 0.72, "NDC");
  mass->SetBorderSize( 0);
  mass->SetFillStyle ( 0);
  //mass->SetTextAlign ( 0);
  //mass->SetTextSize  ( 0.06 );
  mass->SetTextColor( kBlue );
  //mass->SetTextFont (   62 );

  //int precisionMedian=3;
  //std::stringstream massText; massText << "m_{best-fit} = " << std::setprecision(precisionMedian)<< minX << "^{+"  << std::round(upperBound-minX) << "}" << "_{-" << std::round( minX-lowerBound) << "}" << " GeV";
  //mass->AddText(massText.str().c_str());
  //mass->Draw("same"); 
  
  //convert Delta NLL to 2*Delta NLL (plotting convention)
  max=max*0.5;
  /// 1 sigma
  TPaveText * sigma1 = new TPaveText(0.88, (0.6/(max*1.2))+0.09, 0.93, (0.6/(max))+0.14, "NDC");
  sigma1->SetBorderSize(   0 );
  sigma1->SetFillStyle(    0 );
  sigma1->SetTextAlign(   12 );
  sigma1->SetTextSize ( 0.04 );
  sigma1->SetTextColor( kGray+2 );
  sigma1->SetTextFont (   62 );
  sigma1->AddText("1#sigma");
  sigma1->Draw("same");

  /// 2 sigma
  TPaveText * sigma2 = new TPaveText(0.88, (1.8/(max*1.2))+0.1, 0.93, (1.8/max)+0.15, "NDC");
  sigma2->SetBorderSize(   0 );
  sigma2->SetFillStyle(    0 );
  sigma2->SetTextAlign(   12 );
  sigma2->SetTextSize ( 0.04 );
  sigma2->SetTextColor( kGray+2 );
  sigma2->SetTextFont (   62 );
  sigma2->AddText("2#sigma");
  sigma2->Draw("same"); 

  return;
}
