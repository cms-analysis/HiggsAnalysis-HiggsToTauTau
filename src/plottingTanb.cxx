
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
plottingTanb(TCanvas& canv, TH2D* h2d, std::vector<TGraph*> minus2sigma, std::vector<TGraph*> minus1sigma, std::vector<TGraph*> expected, std::vector<TGraph*> plus1sigma, std::vector<TGraph*> plus2sigma, std::vector<TGraph*> observed, std::map<double, TGraphAsymmErrors*> higgsBands, std::map<std::string, TGraph*> comparisons, std::string& xaxis, std::string& yaxis, std::string& theory, double min=0., double max=50., bool log=false, bool transparent=false, bool expectedOnly=false, bool plotOuterBand=true, bool MSSMvsSM=true, std::string HIG="", bool BlackWhite=false)
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
  //if(transparent) twosigma->SetAlpha(0.5);
  TColor* onesigma = gROOT->GetColor(kGray+2);
  //if(transparent) onesigma->SetAlpha(0.5);
  TColor* ph = gROOT->GetColor(kYellow);
  ph->SetAlpha(0.0);
  TColor* backgroundColor = gROOT->GetColor(kRed);
  //backgroundColor->SetAlpha(0.2);

  // for logx the label for x axis values below 100 needs to be slightly shifted to prevent 
  // the label from being printed into the canvas
  // int shift_label = 1.;
//   if(log){
//     if(observed[0]){ observed[0]->GetX()[0] = observed[0]->GetX()[0]+0.01; }
//     if(expected[0]->GetX()[0]<100.){ shift_label = -1.; }
//   }

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
  h2d->GetYaxis()->SetTitleOffset(1.12);
  h2d->GetYaxis()->SetLabelSize(0.05);
  h2d->GetZaxis()->SetTitle("CL_{S}/0.05");
  h2d->GetZaxis()->SetLabelFont(62);
  h2d->GetZaxis()->SetTitleSize(0.04);
  h2d->GetZaxis()->SetTitleOffset(1.03);
  h2d->GetZaxis()->SetLabelSize(0.04);
//   h2d->SetMinimum(0.);
  h2d->SetNameTitle("","");
  h2d->Draw("AXIS");
 
  //mass constraint white area
  int idx=0;
  //int coloredBands[] = {kRed, kRed-7, kRed-9};
  int coloredBands[] = {kWhite, kWhite, kWhite}; 
  TGraph *band_min=new TGraph(), *band_max=new TGraph(), *connection_min=new TGraph(), *connection_max=new TGraph();
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
      //connection_min->Draw("Lsame");
      band_min->SetFillStyle(3005);
      band_min->SetLineWidth(-402);
      band_min->SetFillColor(backgroundColor->GetNumber());
      band_min->SetLineColor(backgroundColor->GetNumber());
      //band_min->Draw("Lsame");
      connection_max->SetFillStyle(3005);
      connection_max->SetLineWidth(-402);
      connection_max->SetFillColor(backgroundColor->GetNumber());
      connection_max->SetLineColor(backgroundColor->GetNumber());
      //connection_max->Draw("Lsame");
      band_max->SetFillStyle(3005);
      band_max->SetLineWidth(402);
      band_max->SetFillColor(backgroundColor->GetNumber());
      band_max->SetLineColor(backgroundColor->GetNumber());
      //if(theory=="MSSM low-m_{H} scenario" || theory=="MSSM m_{h}^{max} scenario")  band_max->Draw("Lsame");
    }
  }
  
  //mass constraint (background color)
  TGraphAsymmErrors* background = new TGraphAsymmErrors();
//   background->SetPoint(0, expected[0]->GetX()[0], 50);
//   background->SetPointEYlow (0, 50);
//   background->SetPointEYhigh(0, 50); 
//   for(int ipoint=1; ipoint<expected[0]->GetN(); ipoint++){
//     background->SetPoint(ipoint, expected[0]->GetX()[ipoint], 50); 
//     background->SetPointEYlow (ipoint, 50);
//     background->SetPointEYhigh(ipoint, 50);
//   }
//   background->SetPoint(expected[0]->GetN(), expected[0]->GetX()[expected[0]->GetN()-1], 50);
//   background->SetPointEYlow(expected[0]->GetN(), 50);
//   background->SetPointEYhigh(expected[0]->GetN(), 50); 
  background->SetFillStyle(3005.); //1001  
  background->SetFillColor(backgroundColor->GetNumber());
  //background->SetLineColor(ph->GetNumber());
  background->SetLineWidth(2); 
  background->SetLineColor(kWhite); //for legend backgroundColor->GetNumber()
  //background->Draw("3"); 

   //exclusion graphs
  for(unsigned int i=0; i<minus2sigma.size(); i++){
    minus2sigma[i]->SetFillStyle(1001);
    minus2sigma[i]->SetFillColor(twosigma->GetNumber()); 
    minus2sigma[i]->SetLineColor(kWhite);
    minus2sigma[i]->SetLineWidth(1);
    minus2sigma[i]->Draw("F SAME");    
  }
  for(unsigned int i=0; i<minus1sigma.size(); i++){
    minus1sigma[i]->SetFillStyle(1001);
    minus1sigma[i]->SetFillColor(onesigma->GetNumber()); 
    minus1sigma[i]->SetLineColor(kWhite);
    minus1sigma[i]->SetLineWidth(1);
    minus1sigma[i]->Draw("F SAME");  
  }
  for(unsigned int i=0; i<plus1sigma.size(); i++){
    plus1sigma[i]->SetFillStyle(1001);
    plus1sigma[i]->SetFillColor(twosigma->GetNumber()); 
    plus1sigma[i]->SetLineColor(kWhite);
    plus1sigma[i]->SetLineWidth(1);
    plus1sigma[i]->Draw("F SAME"); 
  }
  for(unsigned int i=0; i<plus2sigma.size(); i++){
    plus2sigma[i]->SetFillStyle(1001);
    plus2sigma[i]->SetFillColor(kWhite); 
    plus2sigma[i]->SetLineColor(kWhite);
    plus2sigma[i]->SetLineWidth(1);
    plus2sigma[i]->Draw("F SAME"); 
  }

  connection_min->Draw("Lsame");
  band_min->Draw("Lsame");
  connection_max->Draw("Lsame");
  if(theory=="MSSM low-m_{H} scenario" || theory=="MSSM m_{h}^{max} scenario")  band_max->Draw("Lsame");
  
  for(unsigned int i=0; i<expected.size(); i++){
    expected[i]->SetLineColor(kBlack); 
    expected[i]->SetLineWidth(2);
    expected[i]->SetLineStyle(2); 
    expected[i]->Draw("CONT SAME");
  }
  
  if(!expectedOnly){
    for(unsigned int i=0; i<observed.size(); i++){
      observed[i]->SetFillColor(obs->GetNumber());
      observed[i]->SetMarkerStyle(20);
      observed[i]->SetMarkerSize(1.0);
      observed[i]->SetMarkerColor(kBlack);
      observed[i]->SetLineWidth(3.); 
      observed[i]->SetFillStyle(1001);
      observed[i]->Draw("F SAME"); 
      observed[i]->Draw("CONT SAME"); 
    } 
  }

//   if(injected_1){
//     injected_1->SetLineColor(kBlue);
//     injected_1->SetLineWidth(3);
//     injected_1->SetLineStyle(1);
//     injected_1->Draw("Lsame");
//     injected_2->SetLineColor(kBlue);
//     injected_2->SetLineWidth(3);
//     injected_2->SetLineStyle(1);
//     injected_2->Draw("Lsame");
//   }

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
    if(!BlackWhite) observed[0]->SetFillColor(obs->GetNumber()); 
    leg->AddEntry(observed[0], "Observed", "FL");
  }
  if(theory=="MSSM low-m_{H} scenario") {
    leg->AddEntry(minus1sigma[0], "#pm 1#sigma Expected","F");
    leg->AddEntry(expected[0], "Expected", "L");
  }
  else{
    //if(injected_1) leg->AddEntry(injected_1, "SM H injected", "L");
    leg->AddEntry(expected[0], "Expected", "L");
    leg->AddEntry(minus1sigma[0], "#pm 1#sigma Expected","F");
  }
  if(plotOuterBand){ 
    leg->AddEntry(minus2sigma[0], "#pm 2#sigma Expected", "F"); 
    //if(theory=="MSSM low-m_{H} scenario" && injected_1) leg->AddEntry(injected_1, "h_{SM} injected", "L");
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
    else leg2->AddEntry(background, "m^{MSSM}_{h} #scale[1.7]{#bf{#neq}} 125#pm3 GeV", "F");
  }
  else {
    if(theory=="MSSM low-m_{H} scenario") leg2->AddEntry(background, "m^{MSSM}_{H} #scale[1.7]{#bf{#neq}} 125#pm3 GeV", "F");
    else leg2->AddEntry(background, "m^{MSSM}_{h} #scale[1.7]{#bf{#neq}} 125#pm3 GeV", "F");
  }
  if(theory!="2HDM") leg2->Draw("same");

  TLine* legline;
  legline = new TLine(605, 13, 680, 13);
  legline->SetLineWidth(3);
  legline->SetLineColor(backgroundColor->GetNumber());
  if(theory!="2HDM") legline->DrawLineNDC(leg2->GetX1()+0.015, leg2->GetY2()-0.01, leg2->GetX1()+0.072, leg2->GetY2()-0.01);

  canv.RedrawAxis();
  return;
}
