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


TGraphAsymmErrors* higgsConstraint(TGraph* expected_1, double mass, double deltaM, const char* model)
{
  TGraphAsymmErrors* graph = new TGraphAsymmErrors();
  for(unsigned int imass=0, ipoint=0; imass<expected_1->GetN(); ++imass){
    std::string line;
    bool filled = false;
    float tanb_save=-99.0, tanb, mh, mA, mH, upperTanb=-1., lowerTanb=-1.;
    double x_save=expected_1->GetX()[imass];
    ifstream higgs (TString::Format("HiggsAnalysis/HiggsToTauTau/data/Higgs125/%s/higgs_%d.dat", model, (int)x_save)); 
    if(higgs.is_open()){
      while(higgs.good()){
	getline(higgs,line);
	sscanf(line.c_str(),"%f %f %f %f", &tanb, &mh, &mA, &mH);
	if((fabs(mh-mass)<deltaM || fabs(mH-mass)<deltaM) && tanb!=tanb_save){
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
      if(upperTanb>0){
	graph->SetPointEYhigh(ipoint-1, upperTanb-lowerTanb);
      }
    }
    higgs.close();
  }
  return graph;
}


void
plotTanb(const char* filename, const char* channel, bool draw_injected_=false, double min_=0.5, double max_=60., bool MSSMvsSM_=false, bool log_=false, bool transparent_=false,  std::string dataset_="CMS Preliminary, H#rightarrow#tau#tau, 4.9 fb^{-1} at 7 TeV, 19.7 fb^{-1} at 8 TeV", std::string xaxis_="m_{A} [GeV]", std::string yaxis_="#bf{tan#beta}", std::string theory_="MSSM m_{h}^{max} scenario")
{
  TFile* file = TFile::Open(filename);
  // retrieve TGraphs from file
  TGraph* expected_1 = (TGraph*)file->Get(std::string(channel).append("/expected_1").c_str());
  TGraph* expected_2 = (TGraph*)file->Get(std::string(channel).append("/expected_2").c_str());
  TGraph* expected_3 = (TGraph*)file->Get(std::string(channel).append("/expected_3").c_str());
  TGraph* observed_1 = (TGraph*)file->Get(std::string(channel).append("/observed_1").c_str());
  TGraph* observed_2 = (TGraph*)file->Get(std::string(channel).append("/observed_2").c_str());
  TGraph* observed_3 = (TGraph*)file->Get(std::string(channel).append("/observed_3").c_str());
  TGraphAsymmErrors* innerBand_1 = (TGraphAsymmErrors*)file->Get(std::string(channel).append("/innerBand_1").c_str());
  TGraphAsymmErrors* innerBand_2 = (TGraphAsymmErrors*)file->Get(std::string(channel).append("/innerBand_2").c_str());
  TGraphAsymmErrors* innerBand_3 = (TGraphAsymmErrors*)file->Get(std::string(channel).append("/innerBand_3").c_str());
  TGraphAsymmErrors* outerBand_1 = (TGraphAsymmErrors*)file->Get(std::string(channel).append("/outerBand_1").c_str());
  TGraphAsymmErrors* outerBand_2 = (TGraphAsymmErrors*)file->Get(std::string(channel).append("/outerBand_2").c_str());
  TGraphAsymmErrors* outerBand_3 = (TGraphAsymmErrors*)file->Get(std::string(channel).append("/outerBand_3").c_str()); 
  TGraphAsymmErrors* plain_1 = (TGraphAsymmErrors*)file->Get(std::string(channel).append("/plain_1").c_str());
  TGraphAsymmErrors* plain_2 = (TGraphAsymmErrors*)file->Get(std::string(channel).append("/plain_2").c_str());

  // this is new for injected plot together with observed
  TGraph* injected_1 = 0;
  TGraph* injected_2 = 0;
  if(draw_injected_) {
    injected_1 = (TGraph*)file->Get("injected/observed_1");
    injected_2 = (TGraph*)file->Get("injected/observed_2");

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
  if(theory_=="MSSM tauphobic scenario") {model = "tauphobic";}
  if(theory_=="MSSM light-stop scenario") {model = "lightstopmod";}
  std::map<double, TGraphAsymmErrors*> higgsBands;// setup contraints from Higgs mass
  higgsBands[3] = higgsConstraint(expected_1, 125., 3., model);
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
  plottingTanb(canv, plain_1, plain_2, innerBand_1, innerBand_2, innerBand_3, outerBand_1, outerBand_2, outerBand_3, expected_1, expected_2, expected_3, observed_1, observed_2, observed_3, injected_1, injected_2, higgsBands, comparisons, xaxis_, yaxis_, theory_, min_, max_, log_, transparent_, false, true, MSSMvsSM_, "", false);

  /// setup the CMS Preliminary
  CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);
  // write results to files
  canv.Print(std::string(channel).append("_tanb").append(".png").c_str());
  canv.Print(std::string(channel).append("_tanb").append(".pdf").c_str()); 
  canv.Print(std::string(channel).append("_tanb").append(".eps").c_str()); 
  return;
}


