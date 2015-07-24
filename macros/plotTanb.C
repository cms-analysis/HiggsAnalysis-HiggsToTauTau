
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
  // for(unsigned int i=0; i<10; i++){
  //   if((TGraph *)file->Get(TString::Format("%s/gr_minus2sigma_%d", channel, i))) gr_minus2sigma.push_back((TGraph *)file->Get(TString::Format("%s/gr_minus2sigma_%d", channel, i)));
  //   else break;
  // }
  // for(unsigned int i=0; i<10; i++){
  //   if((TGraph *)file->Get(TString::Format("%s/gr_minus1sigma_%d", channel, i))) gr_minus1sigma.push_back((TGraph *)file->Get(TString::Format("%s/gr_minus1sigma_%d", channel, i)));
  //   else break;
  // }
  
  // for(unsigned int i=0; i<10; i++){
  //   if((TGraph *)file->Get(TString::Format("%s/gr_expected_%d", channel, i))) gr_expected.push_back((TGraph *)file->Get(TString::Format("%s/gr_expected_%d", channel, i)));
  //   else break;
  // }
  
  // for(unsigned int i=0; i<10; i++){
  //   if((TGraph *)file->Get(TString::Format("%s/gr_plus1sigma_%d", channel, i))) gr_plus1sigma.push_back((TGraph *)file->Get(TString::Format("%s/gr_plus1sigma_%d", channel, i)));
  //   else break;
  // }
  
  // for(unsigned int i=0; i<10; i++){
  //   if((TGraph *)file->Get(TString::Format("%s/gr_plus2sigma_%d", channel, i))) gr_plus2sigma.push_back((TGraph *)file->Get(TString::Format("%s/gr_plus2sigma_%d", channel, i)));
  //   else break;
  // }
  
  // for(unsigned int i=0; i<10; i++){
  //   if((TGraph *)file->Get(TString::Format("%s/gr_observed_%d", channel, i))) gr_observed.push_back((TGraph *)file->Get(TString::Format("%s/gr_observed_%d", channel, i)));
  //   else break;
  // } 
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

  TGraph* gr_m2s = new TGraph();
  gr_m2s->SetPoint( 0,   90, 4.85);
  gr_m2s->SetPoint( 1,  100, 0.5);
  gr_m2s->SetPoint( 2,  120, 3.06);
  gr_m2s->SetPoint( 3,  130, 3.22);
  gr_m2s->SetPoint( 4,  140, 0.5);
  gr_m2s->SetPoint( 5,  160, 0.5);
  gr_m2s->SetPoint( 6,  180, 0.5);
  gr_m2s->SetPoint( 7,  200, 0.5);
  gr_m2s->SetPoint( 8,  250, 0.5);
  gr_m2s->SetPoint( 9,  300, 8.92);
  gr_m2s->SetPoint(10,  350, 9.68);
  gr_m2s->SetPoint(11,  400, 13.49);
  gr_m2s->SetPoint(12,  450, 14.56);
  gr_m2s->SetPoint(13,  500, 17.80);
  gr_m2s->SetPoint(14,  600, 21.31);
  gr_m2s->SetPoint(15,  700, 26.60);
  gr_m2s->SetPoint(16,  800, 32.86);
  gr_m2s->SetPoint(17,  900, 37.82);
  gr_m2s->SetPoint(18, 1000, 47.05);
  gr_m2s->SetPoint(19, 1010, 60);
  gr_m2s->SetPoint(20,   80, 60);
  gr_m2s->SetPoint(21,   80, 0.05);
  gr_m2s->SetPoint(22,   90, 4.85);
  gr_minus2sigma.push_back(gr_m2s);
  TGraph* gr_m2s2 = new TGraph();
  gr_m2s2->SetPoint( 0,   90, 3.15);
  gr_m2s2->SetPoint( 1,  100, 0.5);
  gr_m2s2->SetPoint( 2,  120, 0.95);
  gr_m2s2->SetPoint( 3,  130, 1.38);
  gr_m2s2->SetPoint( 4,  140, 0.5);
  gr_m2s2->SetPoint( 5,  160, 0.5);
  gr_m2s2->SetPoint( 6,  180, 0.5);
  gr_m2s2->SetPoint( 7,  200, 0.5);
  gr_m2s2->SetPoint( 8,  250, 0.5);
  gr_m2s2->SetPoint( 9,  300, 3.01);
  gr_m2s2->SetPoint(10,  350, 2.85);
  gr_m2s2->SetPoint(11,  400, 2.56);
  gr_m2s2->SetPoint(12,  450, 2.56);
  gr_m2s2->SetPoint(13,  500, 2.55);
  gr_m2s2->SetPoint(14,  600, 2.55);
  gr_m2s2->SetPoint(15,  700, 2.54);
  gr_m2s2->SetPoint(16,  800, 2.62);
  gr_m2s2->SetPoint(17,  900, 2.52);
  gr_m2s2->SetPoint(18, 1000, 2.65);
  gr_m2s2->SetPoint(19, 1010, 0.05);
  gr_m2s2->SetPoint(20, 1010, 0);
  gr_m2s2->SetPoint(21,   90, 0);
  gr_m2s2->SetPoint(22,   90, 3.15);
  gr_minus2sigma.push_back(gr_m2s2);

  TGraph* gr_m1s = new TGraph();
  gr_m1s->SetPoint( 0,   90, 5.32);
  gr_m1s->SetPoint( 1,  100, 4.99);
  gr_m1s->SetPoint( 2,  120, 3.47);
  gr_m1s->SetPoint( 3,  130, 3.56);
  gr_m1s->SetPoint( 4,  140, 2.50);
  gr_m1s->SetPoint( 5,  160, 0.5);
  gr_m1s->SetPoint( 6,  180, 0.5);
  gr_m1s->SetPoint( 7,  200, 0.5);
  gr_m1s->SetPoint( 8,  250, 6.00);
  gr_m1s->SetPoint( 9,  300, 9.22);
  gr_m1s->SetPoint(10,  350, 10.71);
  gr_m1s->SetPoint(11,  400, 14.03);
  gr_m1s->SetPoint(12,  450, 15.61);
  gr_m1s->SetPoint(13,  500, 18.65);
  gr_m1s->SetPoint(14,  600, 23.16);
  gr_m1s->SetPoint(15,  700, 28.41);
  gr_m1s->SetPoint(16,  800, 34.34);
  gr_m1s->SetPoint(17,  900, 40.63);
  gr_m1s->SetPoint(18, 1000, 51.39);
  gr_m1s->SetPoint(19, 1010, 60);
  gr_m1s->SetPoint(20,   80, 60);
  gr_m1s->SetPoint(21,   80, 0.05);
  gr_m1s->SetPoint(22,   90, 5.32);
  gr_minus1sigma.push_back(gr_m1s);
  TGraph* gr_m1s2 = new TGraph();
  gr_m1s2->SetPoint( 0,   90, 2.46);
  gr_m1s2->SetPoint( 1,  100, 2.80);
  gr_m1s2->SetPoint( 2,  120, 0.84);
  gr_m1s2->SetPoint( 3,  130, 1.21);
  gr_m1s2->SetPoint( 4,  140, 1.75);
  gr_m1s2->SetPoint( 5,  160, 0.5);
  gr_m1s2->SetPoint( 6,  180, 0.5);
  gr_m1s2->SetPoint( 7,  200, 0.5);
  gr_m1s2->SetPoint( 8,  250, 6.00);
  gr_m1s2->SetPoint( 9,  300, 2.60);
  gr_m1s2->SetPoint(10,  350, 2.51);
  gr_m1s2->SetPoint(11,  400, 2.34);
  gr_m1s2->SetPoint(12,  450, 2.31);
  gr_m1s2->SetPoint(13,  500, 2.31);
  gr_m1s2->SetPoint(14,  600, 2.31);
  gr_m1s2->SetPoint(15,  700, 2.29);
 gr_m1s2->SetPoint(16,  800, 2.28);
  gr_m1s2->SetPoint(17,  900, 2.28);
  gr_m1s2->SetPoint(18, 1000, 2.31);
  gr_m1s2->SetPoint(19, 1010, 0.05);
  gr_m1s2->SetPoint(20, 1010, 0);
  gr_m1s2->SetPoint(21,   90, 0);
  gr_m1s2->SetPoint(22,   90, 2.46);
  gr_minus1sigma.push_back(gr_m1s2);

  TGraph* gr_exp = new TGraph();
  gr_exp->SetPoint( 0,   90, 6.65);
  gr_exp->SetPoint( 1,  100, 6.88);
  gr_exp->SetPoint( 2,  120, 3.92);
  gr_exp->SetPoint( 3,  130, 3.81);
  gr_exp->SetPoint( 4,  140, 3.50);
  gr_exp->SetPoint( 5,  160, 2.03);
  gr_exp->SetPoint( 6,  180, 4.51);
  gr_exp->SetPoint( 7,  200, 5.13);
  gr_exp->SetPoint( 8,  250, 7.95);
  gr_exp->SetPoint( 9,  300, 9.63);
  gr_exp->SetPoint(10,  350, 12.24);
  gr_exp->SetPoint(11,  400, 14.62);
  gr_exp->SetPoint(12,  450, 18.41);
  gr_exp->SetPoint(13,  500, 19.69);
  gr_exp->SetPoint(14,  600, 24.69);
  gr_exp->SetPoint(15,  700, 31.28);
  gr_exp->SetPoint(16,  800, 38.48);
  gr_exp->SetPoint(17,  900, 45.36);
  gr_exp->SetPoint(18, 1000, 57.77);
  gr_exp->SetPoint(19, 1010, 60);
  gr_exp->SetPoint(20,   80, 60);
  gr_exp->SetPoint(21,   80, 0.05);
  gr_exp->SetPoint(22,   90, 6.65);
  gr_expected.push_back(gr_exp);
  TGraph* gr_exp2 = new TGraph();
  gr_exp2->SetPoint( 0,   90, 1.34);
  gr_exp2->SetPoint( 1,  100, 1.10);
  gr_exp2->SetPoint( 2,  120, 0.5);
  gr_exp2->SetPoint( 3,  130, 1.08);
  gr_exp2->SetPoint( 4,  140, 1.29);
  gr_exp2->SetPoint( 5,  160, 0.5);
  gr_exp2->SetPoint( 6,  180, 2.87);
  gr_exp2->SetPoint( 7,  200, 2.46);
  gr_exp2->SetPoint( 8,  250, 1.39);
  gr_exp2->SetPoint( 9,  300, 0.5);
  gr_exp2->SetPoint(10,  300, 0);
  gr_exp2->SetPoint(11,   90, 0);
  gr_exp2->SetPoint(12,   90, 0.5);
  gr_expected.push_back(gr_exp2);
  
  TGraph* gr_p1s = new TGraph();
  gr_p1s->SetPoint( 0,   90, 7.72);
  gr_p1s->SetPoint( 1,  100, 7.84);
  gr_p1s->SetPoint( 2,  120, 5.60);
  gr_p1s->SetPoint( 3,  130, 4.82);
  gr_p1s->SetPoint( 4,  140, 4.49);
  gr_p1s->SetPoint( 5,  160, 5.23);
  gr_p1s->SetPoint( 6,  180, 5.71);
  gr_p1s->SetPoint( 7,  200, 6.34);
  gr_p1s->SetPoint( 8,  250, 8.64);
  gr_p1s->SetPoint( 9,  300, 10.99);
  gr_p1s->SetPoint(10,  350, 13.10);
  gr_p1s->SetPoint(11,  400, 17.64);
  gr_p1s->SetPoint(12,  450, 19.56);
  gr_p1s->SetPoint(13,  500, 23.29);
  gr_p1s->SetPoint(14,  600, 28.59);
  gr_p1s->SetPoint(15,  700, 34.83);
  gr_p1s->SetPoint(16,  800, 43.70);
  gr_p1s->SetPoint(17,  900, 52.51);
  gr_p1s->SetPoint(18, 1000, 70);
  gr_p1s->SetPoint(19, 1010, 71);
  gr_p1s->SetPoint(20,   80, 71);
  gr_p1s->SetPoint(21,   80, 0.05);
  gr_p1s->SetPoint(22,   90, 7.72);
  gr_plus1sigma.push_back(gr_p1s);
  TGraph* gr_p1s2 = new TGraph();
  gr_p1s2->SetPoint( 0,  120, 0.5);
  gr_p1s2->SetPoint( 1,  130, 0.89);
  gr_p1s2->SetPoint( 2,  140, 1.12);
  gr_p1s2->SetPoint( 3,  160, 0.5);
  gr_p1s2->SetPoint( 4,  160, 0);
  gr_p1s2->SetPoint( 5,  120, 0);
  gr_p1s2->SetPoint( 5,  120, 05);
  gr_plus1sigma.push_back(gr_p1s2);

  TGraph* gr_p2s = new TGraph();
  gr_p2s->SetPoint( 0,   90, 8.79);
  gr_p2s->SetPoint( 1,  100, 8.95);
  gr_p2s->SetPoint( 2,  120, 7.22);
  gr_p2s->SetPoint( 3,  130, 5.83);
  gr_p2s->SetPoint( 4,  140, 5.67);
  gr_p2s->SetPoint( 5,  160, 5.84);
  gr_p2s->SetPoint( 6,  180, 7.05);
  gr_p2s->SetPoint( 7,  200, 7.64);
  gr_p2s->SetPoint( 8,  250, 8.97);
  gr_p2s->SetPoint( 9,  300, 12.51);
  gr_p2s->SetPoint(10,  350, 15.40);
  gr_p2s->SetPoint(11,  400, 19.33);
  gr_p2s->SetPoint(12,  450, 22.78);
  gr_p2s->SetPoint(13,  500, 24.72);
  gr_p2s->SetPoint(14,  600, 31.71);
  gr_p2s->SetPoint(15,  700, 39.41);
  gr_p2s->SetPoint(16,  800, 49.30);
  gr_p2s->SetPoint(17,  900, 59.55);
  gr_p2s->SetPoint(18, 1000, 80);
  gr_p2s->SetPoint(19, 1010, 81);
  gr_p2s->SetPoint(20,   80, 81);
  gr_p2s->SetPoint(21,   80, 0.05);
  gr_p2s->SetPoint(22,   90, 8.79);
  gr_plus2sigma.push_back(gr_p2s);
  TGraph* gr_p2s2 = new TGraph();
  gr_p2s2->SetPoint( 0,  130, 0.5);
  gr_p2s2->SetPoint( 1,  140, 1.04);
  gr_p2s2->SetPoint( 2,  160, 0.5);
  gr_p2s2->SetPoint( 3,  160, 0);
  gr_p2s2->SetPoint( 4,  130, 0);
  gr_p2s2->SetPoint( 5,  130, 0.5);
  gr_plus2sigma.push_back(gr_p2s2);


  TGraph* gr_obs = new TGraph();
  gr_obs->SetPoint( 0,   90, 6.80);
  gr_obs->SetPoint( 1,  100, 7.30);
  gr_obs->SetPoint( 2,  120, 3.73);
  gr_obs->SetPoint( 3,  130, 3.67);
  gr_obs->SetPoint( 4,  140, 3.02);
  gr_obs->SetPoint( 5,  160, 3.29);
  gr_obs->SetPoint( 6,  180, 4.49);
  gr_obs->SetPoint( 7,  200, 4.95);
  gr_obs->SetPoint( 8,  250, 7.23);
  gr_obs->SetPoint( 9,  300, 9.53);
  gr_obs->SetPoint(10,  350, 14.05);
  gr_obs->SetPoint(11,  400, 19.16);
  gr_obs->SetPoint(12,  450, 19.45);
  gr_obs->SetPoint(13,  500, 20.94);
  gr_obs->SetPoint(14,  600, 26.66);
  gr_obs->SetPoint(15,  700, 33.65);
  gr_obs->SetPoint(16,  800, 42.17);
  gr_obs->SetPoint(17,  900, 49.67);
  gr_obs->SetPoint(18, 1000, 60);
  gr_obs->SetPoint(19, 1010, 61);
  gr_obs->SetPoint(20,   80, 61);
  gr_obs->SetPoint(21,   80, 0.05);
  gr_obs->SetPoint(22,   90, 6.80);
  gr_observed.push_back(gr_obs);
  TGraph* gr_obs2 = new TGraph();
  gr_obs2->SetPoint(0,  120, 0.5);
  gr_obs2->SetPoint(1,  130, 1.17);
  gr_obs2->SetPoint(2,  140, 1.51);
  gr_obs2->SetPoint(3,  160, 0.5);
  gr_obs2->SetPoint(4,  160, 0);
  gr_obs2->SetPoint(5,  120, 0);
  gr_obs2->SetPoint(6,  120, 0.5);
  gr_observed.push_back(gr_obs2);	
    

// #            mX                    -2 sigma                    -1 sigma                      Median                    +1 sigma                    +2 sigma             Obs. Limit [pb]
//            90     60.00-4.85; 3.15-0.50;      60.00-5.32; 2.46-0.50;      60.00-6.65; 1.34-0.50;                 60.00-7.73;                 60.00-8.79;                 60.00-6.80; 
//           100                60.00-0.50;      60.00-4.99; 2.80-0.50;      60.00-6.88; 1.10-0.50;                 60.00-7.84;                 60.00-8.95;                 60.00-7.30; 
//           120     60.00-3.06; 0.95-0.59;      60.00-3.47; 0.84-0.68;                 60.00-3.92;                 60.00-5.60;                 60.00-7.22;                 60.00-3.73; 
//           130     60.00-3.22; 1.38-0.50;      60.00-3.56; 1.21-0.50;      60.00-3.81; 1.08-0.56;      60.00-4.82; 0.89-0.69;                 60.00-5.83;      60.00-3.67; 1.17-0.50; 
//           140                60.00-0.50;      60.00-2.50; 1.75-0.50;      60.00-3.50; 1.29-0.50;      60.00-4.49; 1.12-0.50;      60.00-5.67; 1.04-0.60;      60.00-3.02; 1.51-0.50; 
//           160                60.00-0.50;                 60.00-0.50;                 60.00-2.03;                 60.00-5.23;                 60.00-5.84;                 60.00-3.29; 
//           180                60.00-0.50;                 60.00-0.50;      60.00-4.51; 2.87-0.50;                 60.00-5.71;                 60.00-7.05;                 60.00-4.49; 
//           200                60.00-0.50;                 60.00-0.50;      60.00-5.13; 2.46-0.50;                 60.00-6.34;                 60.00-7.64;                 60.00-4.95; 
//           250                60.00-0.50;      60.00-6.00; 6.00-0.50;      60.00-7.95; 1.39-0.61;                 60.00-8.64;                 60.00-8.97;                 60.00-7.23; 
//           300     60.00-8.92; 3.01-0.50;      60.00-9.22; 2.60-0.50;                 60.00-9.63;                60.00-10.99;                60.00-12.51;                 60.00-9.53; 
//           350     60.00-9.68; 2.85-0.50;     60.00-10.71; 2.51-0.50;                60.00-12.24;                60.00-13.10;                60.00-15.40;                60.00-14.05; 
//           400    60.00-13.49; 2.56-0.50;     60.00-14.03; 2.34-0.50;                60.00-14.62;                60.00-17.64;                60.00-19.33;                60.00-19.16; 
//           450    60.00-14.56; 2.56-0.50;     60.00-15.61; 2.31-0.50;                60.00-18.41;                60.00-19.56;                60.00-22.78;                60.00-19.45; 
//           500    60.00-17.80; 2.55-0.50;     60.00-18.65; 2.31-0.50;                60.00-19.69;                60.00-23.29;                60.00-24.72;                60.00-20.94; 
//           600    60.00-21.31; 2.55-0.50;     60.00-23.16; 2.31-0.50;                60.00-24.69;                60.00-28.59;                60.00-31.71;                60.00-26.66; 
//           700    60.00-26.60; 2.54-0.50;     60.00-28.41; 2.29-0.50;                60.00-31.28;                60.00-34.83;                60.00-39.41;                60.00-33.65; 
//           800    60.00-32.86; 2.62-0.50;     60.00-34.34; 2.28-0.50;                60.00-38.48;                60.00-43.70;                60.00-49.30;                60.00-42.17; 
//           900    60.00-37.83; 2.52-0.50;     60.00-40.63; 2.28-0.50;                60.00-45.36;                60.00-52.51;                60.00-59.55;                60.00-49.67; 
//         1e+03    60.00-47.05; 2.65-0.50;     60.00-51.39; 2.31-0.50;                60.00-57.77;                           -                           -                           - 





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
  TCanvas canv = TCanvas("canv", "Limits", 600, 600);
  plottingTanb(canv, plane_expected, gr_minus2sigma, gr_minus1sigma, gr_expected, gr_plus1sigma, gr_plus2sigma, gr_observed, gr_injected, gr_higgsBands, comparisons, xaxis_, yaxis_, theory_, min_, max_, log_, transparent_, false, MSSMvsSM_, "", false, false); 

  /// setup the CMS Preliminary
  //TPaveText* cmsprel = new TPaveText(0.135, 0.735, 0.145+0.30, 0.785, "NDC"); 
  TPaveText* cmsprel = new TPaveText(0.145, 0.835+0.045, 0.145+0.30, 0.835+0.145, "NDC");
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


