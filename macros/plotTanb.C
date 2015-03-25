
#include <map>
#include <string>
#include <iostream>
#include <fstream>
#include <algorithm>

#include "TFile.h"
#include "TGraph.h"
#include "TCanvas.h"
#include "TGraphAsymmErrors.h"

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"

#include "HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"
#include "HiggsAnalysis/HiggsToTauTau/src/plottingTanb.cxx"

TH2D* higgsConstraint(const char* model, const char* type)
{
  int nmass, ntanb;
  double massstep, masslow, masshigh, tanblow, tanbhigh;
  if (TString::Format(model)=="lowmH") {massstep=20, masslow=300; masshigh=3100; nmass=int((masshigh-masslow)/massstep-1); tanblow=1.5; tanbhigh=9.5; ntanb=(int)((tanbhigh-tanblow)*10-1);}
  else if (TString::Format(model)=="low-tb-high") {massstep=10, masslow=150; masshigh=500; nmass=int((masshigh-masslow)/massstep-1); tanblow=0.5; tanbhigh=9.5; ntanb=(int)((tanbhigh-tanblow)*10-1);}
  else {massstep=10, masslow=90; masshigh=1000; nmass=int((masshigh-masslow)/massstep-1); tanblow=0.5; tanbhigh=60; ntanb=(int)((tanbhigh-tanblow));}//ntanb=(int)((tanbhigh-tanblow)*10-1);}

  TH2D* higgsBand= new TH2D("higgsBand", "higgsBand", nmass, masslow, masshigh, ntanb, tanblow, tanbhigh);
  for(double mass=masslow; mass<masshigh+1; mass=mass+massstep){
    std::string line;
    float tanb, mh, mA, mH, mHp;
    ifstream higgs (TString::Format("HiggsAnalysis/HiggsToTauTau/data/Higgs125/%s/higgs_%d.dat", model, (int)mass)); 
    if(higgs.is_open()){
      while(higgs.good()){
	getline(higgs,line);
	sscanf(line.c_str(),"%f %f %f %f %f", &tanb, &mh, &mA, &mH, &mHp);
	if (TString::Format(model)=="lowmH") {
	  higgsBand->SetBinContent(higgsBand->GetXaxis()->FindBin(mass), higgsBand->GetYaxis()->FindBin(tanb), mH);
	}
	else {
	  if (TString::Format(type)=="h") {
	    higgsBand->SetBinContent(higgsBand->GetXaxis()->FindBin(mass), higgsBand->GetYaxis()->FindBin(tanb), mh);
	  }
	  else if(TString::Format(type)=="H") {
	    higgsBand->SetBinContent(higgsBand->GetXaxis()->FindBin(mass), higgsBand->GetYaxis()->FindBin(tanb), mH);
	  }
	  else if(TString::Format(type)=="H+") {
	    higgsBand->SetBinContent(higgsBand->GetXaxis()->FindBin(mass), higgsBand->GetYaxis()->FindBin(tanb), mHp);
	  }
	}
      }
    }
    higgs.close();
  }
  return higgsBand;
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
  std::vector<TGraph*> gr_higgslow;
  std::vector<TGraph*> gr_higgshigh;
  std::vector<std::vector<TGraph*>> gr_higgsBands; 
  std::vector<TGraph*> gr_injected;
  // retrieve TGraphs from file 
  plane_expected=(TH2D *)file->Get(TString::Format("%s/plane_expected", channel)); 
  for(unsigned int i=0; i<10; i++){
    if((TGraph *)file->Get(TString::Format("%s/gr_minus2sigma_%d", channel, i))) gr_minus2sigma.push_back((TGraph *)file->Get(TString::Format("%s/gr_minus2sigma_%d", channel, i)));
    else break;
  }
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
  for(unsigned int i=0; i<10; i++){
    if((TGraph *)file->Get(TString::Format("%s/gr_higgslow_%d", channel, i))) gr_higgslow.push_back((TGraph *)file->Get(TString::Format("%s/gr_higgslow_%d", channel, i)));
    else break;
  }
  gr_higgsBands.push_back(gr_higgslow);
  for(unsigned int i=0; i<10; i++){
    if((TGraph *)file->Get(TString::Format("%s/gr_higgshigh_%d", channel, i))) gr_higgshigh.push_back((TGraph *)file->Get(TString::Format("%s/gr_higgshigh_%d", channel, i)));
    else break;
  } 
  gr_higgsBands.push_back(gr_higgshigh);
  
  // this is new for injected plot together with observed
  if(draw_injected_) {
    for(unsigned int i=0; i<10; i++){
      if((TGraph *)file->Get(TString::Format("%s/gr_observed_%d", "injected", i))) gr_injected.push_back((TGraph *)file->Get(TString::Format("%s/gr_observed_%d", "injected", i)));
      else break;
    }
  }

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

  // this functionality is not yet supported
  std::map<std::string, TGraph*> comparisons;

  // set up styles
  SetStyle();
  // do the plotting 
  TCanvas canv = TCanvas("canv", "Limits", 600, 800);
  plottingTanb(canv, plane_expected, gr_minus2sigma, gr_minus1sigma, gr_expected, gr_plus1sigma, gr_plus2sigma, gr_observed, gr_injected, gr_higgsBands, comparisons, xaxis_, yaxis_, theory_, min_, max_, log_, transparent_, false, MSSMvsSM_, "", true); 

  /// setup the CMS Preliminary
  TPaveText* cmsprel = new TPaveText(0.135, 0.735, 0.145+0.30, 0.785, "NDC"); 
  cmsprel->SetBorderSize(   0 );
  cmsprel->SetFillStyle(    0 );
  cmsprel->SetTextAlign(   11 );
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


