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
#include "TLine.h"
//#include "TRint.h"

#include <iostream>

void
plottingTanb(TCanvas& canv, TGraphAsymmErrors* plain_1, TGraphAsymmErrors* plain_2, TGraphAsymmErrors* innerBand_1, TGraphAsymmErrors* innerBand_2, TGraphAsymmErrors* innerBand_3, TGraphAsymmErrors* outerBand_1, TGraphAsymmErrors* outerBand_2, TGraphAsymmErrors* outerBand_3, TGraph* expected_1, TGraph* expected_2, TGraph* expected_3, TGraph* observed_1, TGraph* observed_2, TGraph* observed_3, TGraph* injected_1, TGraph* injected_2, std::map<double, TGraphAsymmErrors*> higgsBands, std::map<std::string, TGraph*> comparisons, std::string& xaxis, std::string& yaxis, std::string& theory, double min=0., double max=50., bool log=false, bool transparent=false, bool expectedOnly=false, bool plotOuterBand=true, bool MSSMvsSM=true, std::string HIG="", bool BlackWhite=false)
{
  // set up styles
  canv.cd();
  if(log){ 
    canv.SetLogy(1); 
   //  canv.SetLogx(1); 
  }
  
  // setup the CMS colors
  TColor* obs = new TColor(1501, 0.463, 0.867, 0.957);
  if(transparent && !BlackWhite) obs->SetAlpha(0.5); 
  TColor* twosigma = gROOT->GetColor(kGray+1);
  if(transparent) twosigma->SetAlpha(0.5);
  TColor* onesigma = gROOT->GetColor(kGray+2);
  if(transparent) onesigma->SetAlpha(0.5);
  TColor* ph = gROOT->GetColor(kYellow);
  ph->SetAlpha(0.0);
  TColor* backgroundColor = gROOT->GetColor(kRed);
  //backgroundColor->SetAlpha(0.2);

  // for logx the label for x axis values below 100 needs to be slightly shifted to prevent 
  // the label from being printed into the canvas
  int shift_label = 1.;
  if(log){
    if(observed_1){ observed_1->GetX()[0] = observed_1->GetX()[0]+0.01; }
    if(expected_1->GetX()[0]<100.){ shift_label = -1.; }
  }
  // draw a frame to define the range
  TH1F* hr = canv.DrawFrame(expected_1->GetX()[0]-shift_label*.01, min, expected_1->GetX()[expected_1->GetN()-1]+.01, max);
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
  // if(log){
//     hr->SetNdivisions(50005, "X");
//     hr->GetXaxis()->SetMoreLogLabels();
//     hr->GetXaxis()->SetNoExponent();
//     hr->GetXaxis()->SetLabelSize(0.040);
//   }

  TGraphAsymmErrors* background = new TGraphAsymmErrors();
  background->SetPoint(0, expected_1->GetX()[0], 50);
  background->SetPointEYlow (0, 50);
  background->SetPointEYhigh(0, 50); 
  for(int ipoint=1; ipoint<expected_1->GetN(); ipoint++){
    background->SetPoint(ipoint, expected_1->GetX()[ipoint], 50); 
    background->SetPointEYlow (ipoint, 50);
    background->SetPointEYhigh(ipoint, 50);
  }
  background->SetPoint(expected_1->GetN(), expected_1->GetX()[expected_1->GetN()-1], 50);
  background->SetPointEYlow(expected_1->GetN(), 50);
  background->SetPointEYhigh(expected_1->GetN(), 50); 
  background->SetFillStyle(3005.); //1001  
  background->SetFillColor(backgroundColor->GetNumber());
  //background->SetLineColor(ph->GetNumber());
  background->SetLineWidth(2); 
  background->SetLineColor(kWhite); //for legend backgroundColor->GetNumber()
  //background->Draw("3"); 

  int idx=0;
  //int coloredBands[] = {kRed, kRed-7, kRed-9};
  int coloredBands[] = {kWhite, kWhite, kWhite}; 
  for(std::map<double,TGraphAsymmErrors*>::reverse_iterator band = higgsBands.rbegin(); band!=higgsBands.rend(); ++band, ++idx){
    //for(std::map<double,TGraphAsymmErrors*>::const_iterator band = higgsBands.begin(); band!=higgsBands.end(); ++band, ++idx){
    band->second->SetLineColor(coloredBands[idx]);
    band->second->SetFillColor(coloredBands[idx]);
    band->second->Draw("3same");
  
    if(idx==0){
      int np=band->second->GetN();
      double band_ymin[np], band_ymax[np];
      double band_x[np];
      for(int i=0; i<np; i++){ 
	band->second->GetPoint(i, band_x[i], band_ymin[i]);
	band_ymax[i]=band_ymin[i] + band->second->GetErrorYhigh(i);
      }
      //Fill in and max graphs
      TGraph *band_min=new TGraph(), *band_max=new TGraph(), *connection_min=new TGraph(), *connection_max=new TGraph();
      for(int i=0; i<np; i++){ 
	//std::cout << i << " " << band_x[i] << " " << band_ymin[i] << " " << band_ymax[i] << std::endl;
	band_min->SetPoint(i, band_x[i], band_ymin[i]);
	if(theory!="MSSM low-m_{H} scenario"){band_max->SetPoint(i, band_x[i], band_ymax[i]);}
	else{	  
	  if(i==0) band_max->SetPoint(0, band_x[i], band_ymax[i]);
	  if(i==np-1) band_max->SetPoint(1, band_x[i], band_ymax[i]); 
	} 
	if(i==0){
	  connection_min->SetPoint(i, band_x[i], band_ymin[i]);
	  connection_min->SetPoint(i+1, band_x[i], band_ymax[i]);
	}
	if(i==np-1){
	  connection_max->SetPoint(0, band_x[i], band_ymin[i]);
	  connection_max->SetPoint(1, band_x[i], band_ymax[i]);
	}
      }
      connection_min->SetFillStyle(3005);
      connection_min->SetLineWidth(402);
      connection_min->SetFillColor(backgroundColor->GetNumber());
      connection_min->SetLineColor(backgroundColor->GetNumber());
      connection_min->Draw("Lsame");
      band_min->SetFillStyle(3005);
      band_min->SetLineWidth(-402);
      band_min->SetFillColor(backgroundColor->GetNumber());
      band_min->SetLineColor(backgroundColor->GetNumber());
      band_min->Draw("Lsame");
      connection_max->SetFillStyle(3005);
      connection_max->SetLineWidth(-402);
      connection_max->SetFillColor(backgroundColor->GetNumber());
      connection_max->SetLineColor(backgroundColor->GetNumber());
      connection_max->Draw("Lsame");
      band_max->SetFillStyle(3005);
      band_max->SetLineWidth(402);
      band_max->SetFillColor(backgroundColor->GetNumber());
      band_max->SetLineColor(backgroundColor->GetNumber());
      if(theory=="MSSM low-m_{H} scenario" || theory=="MSSM m_{h}^{max} scenario")  band_max->Draw("Lsame");
    }
  }

  if(!expectedOnly){
    plain_1->SetLineColor(ph->GetNumber());
    plain_1->SetFillStyle(1001.);
    plain_1->SetFillColor(obs->GetNumber());
    if (!transparent && !BlackWhite) plain_1->Draw("3same");
    observed_1->SetMarkerStyle(20);
    observed_1->SetMarkerSize(1.0);
    observed_1->SetMarkerColor(kBlack);
    observed_1->SetLineWidth(3.); 
    if(BlackWhite) observed_1->SetFillStyle(3245);    
    if(BlackWhite) observed_1->SetLineWidth(403);       
    if(BlackWhite) observed_1->SetFillColor(4); 
    
    plain_2->SetLineColor(ph->GetNumber());
    plain_2->SetFillStyle(1001.);
    plain_2->SetFillColor(obs->GetNumber());
    if (HIG=="") {
      if (!transparent && !BlackWhite) plain_2->Draw("3same"); 
    }
    observed_2->SetMarkerStyle(20);
    observed_2->SetMarkerSize(1.0);
    observed_2->SetMarkerColor(kBlack);
    observed_2->SetLineWidth(3.); 
    if(BlackWhite) observed_2->SetFillStyle(3245);         
    if(BlackWhite) observed_2->SetLineWidth(-403);           
    if(BlackWhite) observed_2->SetFillColor(4);        
    observed_3->SetMarkerStyle(20);
    observed_3->SetMarkerSize(1.0);
    observed_3->SetMarkerColor(kBlack);
    observed_3->SetLineWidth(3.); 
    if(BlackWhite) observed_3->SetFillStyle(3245);    
    if(BlackWhite) observed_3->SetLineWidth(-403);            
    if(BlackWhite) observed_3->SetFillColor(4);  
  }

  /*//Get data points from TGraphAsymmErrors
  int npoints = expected_1->GetN();
  double outerband_1_ymin[npoints], outerband_1_ymax[npoints], outerband_2_ymin[npoints], outerband_2_ymax[npoints];
  double innerband_1_ymin[npoints], innerband_1_ymax[npoints], innerband_2_ymin[npoints], innerband_2_ymax[npoints];
  double expected_1_X[npoints], expected_1_Y[npoints], expected_2_X[npoints], expected_2_Y[npoints];
  for(int i=0; i<npoints; i++){ 
    expected_1->GetPoint(i, expected_1_X[i], expected_1_Y[i]);
    expected_1->GetPoint(i, expected_2_X[i], expected_2_Y[i]);
    outerband_1_ymax[i]=expected_1_Y[i] - outerBand_1->GetErrorYlow(i);
    outerband_1_ymin[i]=expected_1_Y[i] + outerBand_1->GetErrorYhigh(i);
    outerband_2_ymax[i]=expected_2_Y[i] - outerBand_2->GetErrorYlow(i);
    outerband_2_ymin[i]=expected_2_Y[i] + outerBand_2->GetErrorYhigh(i);
    innerband_1_ymax[i]=expected_1_Y[i] - innerBand_1->GetErrorYlow(i);
    innerband_1_ymin[i]=expected_1_Y[i] + innerBand_1->GetErrorYhigh(i);
    innerband_2_ymax[i]=expected_2_Y[i] - innerBand_2->GetErrorYlow(i);
    innerband_2_ymin[i]=expected_2_Y[i] + innerBand_2->GetErrorYhigh(i);
  }
  //Fill central, min and max graphs
  TGraph *outerband_1_min=new TGraph(), *outerband_1_max=new TGraph(), *outerband_2_min=new TGraph(), *outerband_2_max=new TGraph();
  TGraph *innerband_1_min=new TGraph(), *innerband_1_max=new TGraph(), *innerband_2_min=new TGraph(), *innerband_2_max=new TGraph();
  for(int i=0; i<npoints; i++){ 
    outerband_1_min->SetPoint(i, expected_1_X[i], outerband_1_ymin[i]);
    outerband_1_max->SetPoint(i, expected_1_X[i], outerband_1_ymax[i]);
    outerband_2_min->SetPoint(i, expected_2_X[i], outerband_2_ymin[i]);
    outerband_2_max->SetPoint(i, expected_2_X[i], outerband_2_ymax[i]);
    innerband_1_min->SetPoint(i, expected_1_X[i], innerband_1_ymin[i]);
    innerband_1_max->SetPoint(i, expected_1_X[i], innerband_1_ymax[i]);
    innerband_2_min->SetPoint(i, expected_2_X[i], innerband_2_ymin[i]);
    innerband_2_max->SetPoint(i, expected_2_X[i], innerband_2_ymax[i]);
    }*/

  if(plotOuterBand){
    outerBand_1->SetFillStyle(1001);
    outerBand_1->SetFillColor(twosigma->GetNumber()); 
    outerBand_1->SetLineColor(kWhite);
    outerBand_1->SetLineWidth(1);
    //outerBand_1->SetLineColor(twosigma->GetNumber());
    outerBand_1->Draw("3same");    
    outerBand_2->SetFillStyle(1001);
    outerBand_2->SetFillColor(twosigma->GetNumber()); 
    outerBand_2->SetLineColor(twosigma->GetNumber());
    if(HIG=="") outerBand_2->Draw("3same");  
    outerBand_3->SetFillStyle(1001);
    outerBand_3->SetFillColor(twosigma->GetNumber()); 
    outerBand_3->SetLineColor(twosigma->GetNumber());
    //outerBand_3->Draw("3same");

    /*outerband_1_min->SetLineColor(kGray+1);
    outerband_1_max->SetLineColor(kGray+1);
    outerband_2_min->SetLineColor(kGray+1);
    outerband_2_max->SetLineColor(kGray+1);
    outerband_1_min->SetLineStyle(2);
    outerband_1_max->SetLineStyle(2);
    outerband_2_min->SetLineStyle(2);
    outerband_2_max->SetLineStyle(2);
    outerband_1_min->SetLineWidth(3);
    outerband_1_max->SetLineWidth(3);
    outerband_2_min->SetLineWidth(3);
    outerband_2_max->SetLineWidth(3);
    if(BlackWhite && HIG==""){
      outerband_1_min->Draw("Lsame");
      outerband_1_max->Draw("Lsame");
      outerband_2_min->Draw("Lsame");
      outerband_2_max->Draw("Lsame");
      }*/
  }
  
  innerBand_1->SetFillStyle(1001);
  innerBand_1->SetFillColor(onesigma->GetNumber()); 
  innerBand_1->SetLineColor(kWhite);
  innerBand_1->SetLineWidth(1);
  //innerBand_1->SetLineColor(onesigma->GetNumber());
  innerBand_1->Draw("3same"); 
  innerBand_2->SetFillColor(onesigma->GetNumber()); 
  innerBand_2->SetLineColor(onesigma->GetNumber());
  if(HIG=="") innerBand_2->Draw("3same"); 
  innerBand_3->SetFillStyle(1001);
  innerBand_3->SetFillColor(onesigma->GetNumber()); 
  innerBand_3->SetLineColor(onesigma->GetNumber());
  //innerBand_3->Draw("3same"); 
 
  /*innerband_1_min->SetLineColor(kGray+2);
  innerband_1_max->SetLineColor(kGray+2);
  innerband_2_min->SetLineColor(kGray+2);
  innerband_2_max->SetLineColor(kGray+2);
  innerband_1_min->SetLineStyle(9);
  innerband_1_max->SetLineStyle(9);
  innerband_2_min->SetLineStyle(9);
  innerband_2_max->SetLineStyle(9);
  innerband_1_min->SetLineWidth(3);
  innerband_1_max->SetLineWidth(3);
  innerband_2_min->SetLineWidth(3);
  innerband_2_max->SetLineWidth(3);
  if(BlackWhite && HIG=="") innerband_1_min->Draw("Lsame");
  if(BlackWhite && HIG=="") innerband_1_max->Draw("Lsame");
  if(BlackWhite && HIG=="") innerband_2_min->Draw("Lsame");
  if(BlackWhite && HIG=="") innerband_2_max->Draw("Lsame"); */
    
  expected_1->SetLineColor(kBlack); //changed from kGray+3
  expected_1->SetLineWidth(2); //changed from 3 
  expected_1->SetLineStyle(2); //changed from 1 
  if(BlackWhite) expected_1->Draw("Lsame");
  expected_2->SetLineColor(kBlack); //changed from kGray+3
  expected_2->SetLineWidth(2); //changed from 3 
  expected_2->SetLineStyle(2); //changed from 1 
  if(HIG=="" && BlackWhite) expected_2->Draw("Lsame"); 
  expected_3->SetLineColor(kBlack); //changed from kGray+3
  expected_3->SetLineWidth(2); //changed from 3 
  expected_3->SetLineStyle(2); //changed from 1 
  //expected_3->Draw("Lsame");
   
  if(injected_1){
    injected_1->SetLineColor(kBlue);
    injected_1->SetLineWidth(3);
    injected_1->SetLineStyle(1);
    injected_1->Draw("Lsame");
    injected_2->SetLineColor(kBlue);
    injected_2->SetLineWidth(3);
    injected_2->SetLineStyle(1);
    injected_2->Draw("Lsame");
  }

  if(!expectedOnly){
    if(transparent && !BlackWhite) plain_1->Draw("3same");
    observed_1->Draw("Lsame");
    if (HIG=="") {
      if(transparent && !BlackWhite) plain_2->Draw("3same");
      observed_2->Draw("Lsame");
    }
    //observed_3->Draw("Lsame"); 
    if(!BlackWhite) expected_1->Draw("Lsame");
    if(!BlackWhite && HIG=="") expected_2->Draw("Lsame");
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
    //if(theory=="MSSM light-stop scenario") theory1= new TPaveText(0.375, 0.69, 0.9, 0.75, "NDC"); //for loglog
    //else theory1= new TPaveText(0.14, 0.85, 0.9, 0.90, "NDC");
    theory1= new TPaveText(0.14, 0.85, 0.9, 0.90, "NDC");
  }
  else{
    if(theory=="MSSM low-m_{H} scenario") theory1= new TPaveText(0.55, 0.84, 0.91, 0.90, "NDC");
    else if(theory=="MSSM m_{h}^{max} scenario") theory1= new TPaveText(0.59, 0.165, 0.91, 0.225, "NDC");
    else if(theory=="MSSM m_{h}^{mod-} scenario") theory1= new TPaveText(0.59, 0.20, 0.91, 0.26, "NDC");
    else if(theory=="MSSM m_{h}^{mod+} scenario") theory1= new TPaveText(0.59, 0.20, 0.91, 0.26, "NDC");
    else if(theory=="MSSM light-stop scenario") theory1= new TPaveText(0.51, 0.20, 0.91, 0.26, "NDC"); //for loglog
    else if(theory=="MSSM light-stau scenario") theory1= new TPaveText(0.51, 0.20, 0.91, 0.26, "NDC");
    else theory1= new TPaveText(0.51, 0.20, 0.91, 0.26, "NDC");
  }
  theory1->SetBorderSize(   0 );
  theory1->SetFillStyle(    0 );
  theory1->SetTextAlign(   12 );
  theory1->SetTextSize ( 0.035);
  theory1->SetTextColor(    1 );
  theory1->SetTextFont (   62 );
  theory1->AddText(theory.c_str());
  theory1->Draw();

  /// add the proper legend
  TLegend* leg;
  if(log){
    if(theory=="MSSM #scale[1.3]{#bf{#tau}}-phobic scenario") leg = new TLegend(0.635, 0.16, 0.92, 0.41);
    //else if(theory=="MSSM light-stop scenario") leg = new TLegend(0.36, 0.745, 0.84, 0.905); // for loglog
    // else leg = new TLegend(0.635, (!higgsBands.empty() || !comparisons.empty()) ? 0.15 : 0.32, (!higgsBands.empty() || !comparisons.empty()) ? 0.92: 0.92, 0.44); // for loglog
    else leg = new TLegend(0.635, (!higgsBands.empty() || !comparisons.empty()) ? 0.16 : 0.32, (!higgsBands.empty() || !comparisons.empty()) ? 0.92: 0.92, 0.44); //for log
  }
  else{ 
    if(MSSMvsSM){
      if(theory=="MSSM low-m_{H} scenario") leg = new TLegend(0.175, 0.155, 0.59, 0.29);
      else if(theory=="MSSM light-stop scenario") leg = new TLegend(0.28, (!higgsBands.empty() || !comparisons.empty()) ? 0.57 :0.69, (!higgsBands.empty() || !comparisons.empty()) ? 0.57: 0.60, 0.89);
      else leg = new TLegend(0.21, (!higgsBands.empty() || !comparisons.empty()) ? 0.59 : 0.71, (!higgsBands.empty() || !comparisons.empty()) ? 0.49: 0.52, 0.89);
    }
    else{
      if(theory=="MSSM low-m_{H} scenario") leg = new TLegend(0.175, 0.155, 0.62, 0.30);
      else if(theory=="MSSM light-stop scenario") leg = new TLegend(0.28, (!higgsBands.empty() || !comparisons.empty()) ? 0.57 :0.69, (!higgsBands.empty() || !comparisons.empty()) ? 0.53: 0.56, 0.89);
      else leg = new TLegend(0.23, (!higgsBands.empty() || !comparisons.empty()) ? 0.57 : 0.69, (!higgsBands.empty() || !comparisons.empty()) ? 0.47: 0.50, 0.89);
    }
  }
  if(theory=="MSSM low-m_{H} scenario") leg->SetNColumns(2);
  //if(theory=="MSSM light-stop scenario" && log) leg->SetNColumns(2); //for loglog
  leg->SetBorderSize(  1 );
  leg->SetFillStyle (1001);
  leg->SetTextSize  (0.03);
  leg->SetTextFont  ( 62 ); 
  leg->SetFillColor (kWhite);
  leg->SetLineColor (kBlack);
  if(MSSMvsSM) leg->SetHeader("CL_{S}(MSSM,SM)<0.05:");
  else leg->SetHeader("95% CL Excluded:");
  if(!expectedOnly){ 
    if(!BlackWhite) observed_1->SetFillColor(obs->GetNumber()); 
    leg->AddEntry(observed_1, "Observed", "FL");
  }
  if(theory=="MSSM low-m_{H} scenario") {
    leg->AddEntry(innerBand_1, "#pm 1#sigma Expected","F");
    //if(BlackWhite && HIG=="") leg->AddEntry(innerband_1_max, "#pm 1#sigma expected","L"); 
    leg->AddEntry(expected_1, "Expected", "L");
  }
  else{
    if(injected_1) leg->AddEntry(injected_1, "SM H injected", "L");
    leg->AddEntry(expected_1, "Expected", "L");
    leg->AddEntry(innerBand_1, "#pm 1#sigma Expected","F");
    //if(BlackWhite && HIG=="") leg->AddEntry(innerband_1_max, "#pm 1#sigma expected","L");
  }
  if(plotOuterBand){ 
    leg->AddEntry(outerBand_1, "#pm 2#sigma Expected", "F"); 
    //if(BlackWhite && HIG=="") leg->AddEntry(outerband_1_max, "#pm 2#sigma expected","L"); 
    if(theory=="MSSM low-m_{H} scenario" && injected_1) leg->AddEntry(injected_1, "h_{SM} injected", "L");
  }
  //for(std::map<double,TGraphAsymmErrors*>::const_iterator band = higgsBands.begin(); band!=higgsBands.end(); ++band){
  //  leg->AddEntry(band->second, TString::Format("m_{h,H}=125GeV #pm %.0fGeV", band->first), "F");
  //}
  //if(theory=="MSSM m_{h}^{max} scenario") leg->AddEntry(upperLEP, "LEP", "F");
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
  

  TLegend* leg2;
  if(log){
    //if(theory=="MSSM light-stop scenario") leg2 = new TLegend(0.55, 0.15, 0.92, 0.20); //for loglog
    if(theory=="MSSM light-stop scenario") leg2 = new TLegend(0.57, 0.47, 0.92, 0.52); //for log
    //else leg2 = new TLegend(0.31, 0.79, 0.65, 0.84); //for loglog
    else leg2 = new TLegend(0.57, 0.60, 0.92, 0.65);
  }
  else{ 
    if(theory=="MSSM low-m_{H} scenario") leg2 = new TLegend(0.57, 0.78, 0.92, 0.83);
    else leg2 = new TLegend(0.57, 0.26, 0.92, 0.31);
  }  
  leg2->SetBorderSize( 1  );
  leg2->SetFillStyle (1001);
  leg2->SetTextSize  (0.03);
  leg2->SetTextFont  ( 62 ); 
  leg2->SetFillColor (kWhite);
  leg2->SetLineWidth (2);
  leg2->SetLineColor (kBlack);
  if(log) {
    if(theory=="MSSM low-m_{H} scenario") leg2->AddEntry(background, "m^{MSSM}_{H} #scale[1.7]{#bf{#neq}} 125#pm3 GeV", "F");
    else leg2->AddEntry(background, "m^{MSSM}_{h,H} #scale[1.7]{#bf{#neq}} 125#pm3 GeV", "F");
  }
  else {
    if(theory=="MSSM low-m_{H} scenario") leg2->AddEntry(background, "m^{MSSM}_{H} #scale[1.7]{#bf{#neq}} 125#pm3 GeV", "F");
    else leg2->AddEntry(background, "m^{MSSM}_{h,H} #scale[1.7]{#bf{#neq}} 125#pm3 GeV", "F");
  }
  leg2->Draw("same");

  TLine* legline;
  legline = new TLine(605, 13, 680, 13);
  legline->SetLineWidth(3);
  legline->SetLineColor(backgroundColor->GetNumber());
  //legline->DrawLineNDC(0.585, 0.64, 0.642, 0.64);
  legline->DrawLineNDC(leg2->GetX1()+0.015, leg2->GetY2()-0.01, leg2->GetX1()+0.072, leg2->GetY2()-0.01);
  //legline->Draw("same");
  
  //canv.RedrawAxis("g");
  canv.RedrawAxis();
  return;
}
