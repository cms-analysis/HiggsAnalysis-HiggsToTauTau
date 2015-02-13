
#include <map>
#include <string>
#include <iostream>
#include <fstream>

#include "TFile.h"
#include "TGraph.h"
#include "TCanvas.h"
#include "TGraphAsymmErrors.h"

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"

#include "HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"
#include "HiggsAnalysis/HiggsToTauTau/src/plottingTanb.cxx"

//#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

TGraphAsymmErrors* higgsConstraint(TH2D* plane_expected, double mass, double deltaM, const char* model)
{
  TGraphAsymmErrors* graph = new TGraphAsymmErrors();
  for(unsigned int imass=0, ipoint=0; imass<plane_expected->GetNbinsX(); ++imass){
  //for(int i=300, ipoint=0; i<3101; i=i+100){
    std::string line;
    bool filled = false;
    float tanb_save=-99.0, tanb, mh, mA, mH, upperTanb=-1., lowerTanb=-1.;
    double x_save=plane_expected->GetXaxis()->GetBinUpEdge(imass);
    //double x_save=(int)i;
    ifstream higgs (TString::Format("HiggsAnalysis/HiggsToTauTau/data/Higgs125/%s/higgs_%d.dat", model, (int)x_save)); 
    std::cout << TString::Format("HiggsAnalysis/HiggsToTauTau/data/Higgs125/%s/higgs_%d.dat", model, (int)x_save) << std::endl;
    if(higgs.is_open()){
      while(higgs.good()){
	getline(higgs,line);
	sscanf(line.c_str(),"%f %f %f %f", &tanb, &mh, &mA, &mH);
	if (model=="lowmH") {
	  if(fabs(mH-mass)<deltaM && tanb!=tanb_save){
	    if(!filled){
	      graph->SetPoint(ipoint, x_save, tanb); 
	      graph->SetPointEYlow(ipoint, 0.);
	      tanb_save=tanb;
	      ipoint++; filled = true;
	      lowerTanb=tanb;
	    }
	    upperTanb=tanb;
	  }
	}
	else {
	  if(fabs(mh-mass)<deltaM && tanb!=tanb_save){
	    if(!filled){
	      graph->SetPoint(ipoint, x_save, tanb); 
	      graph->SetPointEYlow(ipoint, 0.);
	      tanb_save=tanb;
	      ipoint++; filled = true;
	      lowerTanb=tanb;
	    }
	    upperTanb=tanb;
	  }
	}
      }
      if(upperTanb>0){
	graph->SetPointEYhigh(ipoint-1, upperTanb-lowerTanb);
      }
    }
    higgs.close();
  }
  return graph;
}


void
plotTanb(const char* filename, const char* channel, bool draw_injected_=false, double min_=0.5, double max_=60., bool MSSMvsSM_=false, bool log_=false, bool transparent_=false,  std::string dataset_="#scale[1.5]{CMS}   H#rightarrow#tau#tau                            19.7 fb^{-1} (8 TeV) + 4.9 fb^{-1} (7 TeV)", std::string xaxis_="m_{A} [GeV]", std::string yaxis_="#bf{tan#beta}", std::string theory_="MSSM m_{h}^{max} scenario")
{
  TFile* file = TFile::Open(filename);
  // Grabbing contours
  TH2D *plane_expected = 0;
  std::vector<TGraph*> gr_minus2sigma;
  std::vector<TGraph*> gr_minus1sigma;
  std::vector<TGraph*> gr_expected;
  std::vector<TGraph*> gr_plus1sigma;
  std::vector<TGraph*> gr_plus2sigma;
  std::vector<TGraph*> gr_observed;
  std::vector<TGraph*> gr_injected;
  // retrieve TGraphs from file 
  plane_expected=(TH2D *)file->Get(TString::Format("%s/plane_expected", channel)); 
  for(unsigned int i=0; i<10; i++){
    if((TGraph *)file->Get(TString::Format("%s/gr_minus2sigma_%d", channel, i))) gr_minus2sigma.push_back((TGraph *)file->Get(TString::Format("%s/gr_minus2sigma_%d", channel, i)));
    //if((TGraph *)file->FindObject(TString::Format("%s/gr_expected_%d", channel, i))) std::cout<< i << " hello" << std::endl;
    else break;
  }
  //std::cout<< TString::Format("%s/expected_%d", channel, 0) << std::endl;
  //std::cout<< "finish" << std::endl;
  for(unsigned int i=0; i<10; i++){
    if((TGraph *)file->Get(TString::Format("%s/gr_minus1sigma_%d", channel, i))) gr_minus1sigma.push_back((TGraph *)file->Get(TString::Format("%s/gr_minus1sigma_%d", channel, i)));
    else break;
  }
  
  for(unsigned int i=0; i<10; i++){
    if((TGraph *)file->Get(TString::Format("%s/gr_expected_%d", channel, i))) gr_expected.push_back((TGraph *)file->Get(TString::Format("%s/gr_expected_%d", channel, i)));
    else break;
  }
  
  for(unsigned int i=0; i<10; i++){
    if((TGraph *)file->Get(TString::Format("%s/gr_plus1sigma_%d", channel, i))) gr_plus1sigma.push_back((TGraph *)file->Get(TString::Format("%s/gr_plus1sigma_%d", channel, i)));
    else break;
  }
  
  for(unsigned int i=0; i<10; i++){
    if((TGraph *)file->Get(TString::Format("%s/gr_plus2sigma_%d", channel, i))) gr_plus2sigma.push_back((TGraph *)file->Get(TString::Format("%s/gr_plus2sigma_%d", channel, i)));
    else break;
  }
  
  for(unsigned int i=0; i<10; i++){
    if((TGraph *)file->Get(TString::Format("%s/gr_observed_%d", channel, i))) gr_observed.push_back((TGraph *)file->Get(TString::Format("%s/gr_observed_%d", channel, i)));
    else break;
  }
  
  // this is new for injected plot together with observed
  if(draw_injected_) {
    for(unsigned int i=0; i<10; i++){
      if((TGraph *)file->Get(TString::Format("%s/gr_observed_%d", "injected", i))) gr_injected.push_back((TGraph *)file->Get(TString::Format("%s/gr_observed_%d", "injected", i)));
      else break;
    }
  }

  //if(draw_injected_){
  //  for( int i=0; i<expected->GetN(); i++){
  //    double shift = injected->GetY()[i]-expected->GetY()[i];
  //    innerBand->SetPoint(i, innerBand->GetX()[i], innerBand->GetY()[i]+shift);
  //    outerBand->SetPoint(i, outerBand->GetX()[i], outerBand->GetY()[i]+shift);
  //  }
  //}

  const char* model;
  if(theory_=="MSSM m_{h}^{max} scenario") {model = "mhmax-mu+200";}
  if(theory_=="MSSM m_{h}^{mod-} scenario") {model = "mhmodm";}
  if(theory_=="MSSM m_{h}^{mod+} scenario") {model = "mhmodp";}
  if(theory_=="MSSM low-m_{H} scenario") {model = "lowmH";}
  if(theory_=="MSSM light-stau scenario") {model = "lightstau1";}
  if(theory_=="MSSM #scale[1.3]{#bf{#tau}}-phobic scenario") {model = "tauphobic";}
  if(theory_=="MSSM light-stop scenario") {model = "lightstopmod";}
  if(theory_=="MSSM low-tan#beta-high scenario") {model = "low-tb-high";}
  if(theory_=="2HDM type-I") {model = "2HDMtyp1";}
  if(theory_=="2HDM type-II") {model = "2HDMtyp2";}

  // setup contraints from Higgs mass
  std::map<double, TGraphAsymmErrors*> higgsBands;
  higgsBands[3] = higgsConstraint(plane_expected, 125., 3., model);
  //for(unsigned int deltaM=0; deltaM<3; ++deltaM){
  //  higgsBands[3-deltaM] = higgsConstraint(expected_1, 125., 4-deltaM, model);
  //}
  // this functionality is not yet supported
  std::map<std::string, TGraph*> comparisons;

  // set up styles
  SetStyle();
  // do the plotting 
  TCanvas canv = TCanvas("canv", "Limits", 600, 600);
  // do the plotting 
  plottingTanb(canv, plane_expected, gr_minus2sigma, gr_minus1sigma, gr_expected, gr_plus1sigma, gr_plus2sigma, gr_observed, gr_injected, higgsBands, comparisons, xaxis_, yaxis_, theory_, min_, max_, log_, transparent_, false, true, MSSMvsSM_, "", true); 

  /// setup the CMS Preliminary
  //CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);
  // TPaveText* cmsprel  = new TPaveText(0.145, 0.835+0.06, 0.145+0.30, 0.835+0.16, "NDC");
  TPaveText* cmsprel  = new TPaveText(0.135, 0.835+0.06, 0.145+0.30, 0.835+0.16, "NDC"); //for unpublished plots
  cmsprel->SetBorderSize(   0 );
  cmsprel->SetFillStyle(    0 );
  cmsprel->SetTextAlign(   12 );
  cmsprel->SetTextSize ( 0.03 );
  cmsprel->SetTextColor(    1 );
  cmsprel->SetTextFont (   62 );
  cmsprel->AddText(dataset_.c_str());
  cmsprel->Draw();
  // write results to files
  canv.Print(std::string(channel).append("_").append(model).append("_tanb").append(".png").c_str());
  canv.Print(std::string(channel).append("_").append(model).append("_tanb").append(".pdf").c_str()); 
  canv.Print(std::string(channel).append("_").append(model).append("_tanb").append(".eps").c_str()); 
  return;
}


