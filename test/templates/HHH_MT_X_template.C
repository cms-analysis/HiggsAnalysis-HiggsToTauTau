#include <iostream>
#include <algorithm>

#include <TH1F.h>
#include <TFile.h>
#include <TROOT.h>
#include <TString.h>
#include <TSystem.h>
#include <Rtypes.h>

#include <TMath.h>
#include <TAxis.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TAttLine.h>
#include <TPaveText.h>
#include <TColor.h>

#include "$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"
#include "$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"

static const float SIGNAL_SCALE = 10.;

$DEFINE_ASIMOV
$DEFINE_DROP_SIGNAL
$DEFINE_EXTRA_SAMPLES
$DEFINE_MSSM

/**
   \class   HTT_MT_X_template HTT_MT_X_template.C "HiggsAnalysis/HiggsToTauTau/postfit/tamplates/HTT_MT_X_template.C"

   \brief   macro template to create pre-/postfit plots of the inputs to the limit calculation

   This is a macro template to create pre-/postfit plots of the inputs to the limit calculation.
   This macro is picked up from the produce_macros.py script in the HiggsAnalysis/HiggsToTauTau/test
   directory. The key words are replaced by proper values.
*/

static const bool BLIND_DATA = $BLIND; //false;
static const bool FULLPLOTS = true; //true;
static const bool CONVERVATIVE_CHI2 = false;
static const float UPPER_EDGE = 1005; // 695; 1495;

float blinding_SM(float mass){ return (100<mass && mass<150); }
float blinding_MSSM(float mass){ return (200<mass && mass<400); }
float maximum(TH1F* h, bool LOG=false){
  if(LOG){
    if(h->GetMaximum()>1000){ return 1000.*TMath::Nint(30*h->GetMaximum()/1000.); }
    if(h->GetMaximum()>  10){ return   10.*TMath::Nint(30*h->GetMaximum()/  10.); }
    return 50*h->GetMaximum(); 
  }
  else{
    if(h->GetMaximum()>  12){ return 10.*TMath::Nint((1.20*h->GetMaximum()/10.)); }
    if(h->GetMaximum()> 1.2){ return TMath::Nint((1.50*h->GetMaximum())); }
    return 1.6*h->GetMaximum(); 
  }
}

TH1F* refill(TH1F* hin, const char* sample, bool data=false)
/*
  refill histograms, divide by bin width and correct bin errors. For MC histograms set 
  bin errors to zero.
*/
{
  if(hin==0){
    std::cout << "hist not found: " << sample << " -- close here" << std::endl;
    exit(1);  
  }
  TH1F* hout = (TH1F*)hin->Clone(); hout->Clear();
  for(int i=0; i<hout->GetNbinsX(); ++i){
    if(data){
#if defined MSSM
      hout->SetBinContent(i+1, BLIND_DATA && blinding_MSSM(hin->GetBinCenter(i+1)) ? 0. : hin->GetBinContent(i+1)/hin->GetBinWidth(i+1));
      hout->SetBinError  (i+1, BLIND_DATA && blinding_MSSM(hin->GetBinCenter(i+1)) ? 0. : hin->GetBinError(i+1)/hin->GetBinWidth(i+1));
#else
      hout->SetBinContent(i+1, BLIND_DATA && blinding_SM  (hin->GetBinCenter(i+1)) ? 0. : hin->GetBinContent(i+1)/hin->GetBinWidth(i+1));
      hout->SetBinError  (i+1, BLIND_DATA && blinding_SM  (hin->GetBinCenter(i+1)) ? 0. : hin->GetBinError(i+1)/hin->GetBinWidth(i+1));
#endif
    }
    else{
      hout->SetBinContent(i+1, hin->GetBinContent(i+1)/hin->GetBinWidth(i+1));
      hout->SetBinError(i+1, 0.);
    }
  }
  return hout;
}

TH1F* shape_histos(TH1F* hin, const TString datacard, const TString name)
/*
  use the proper histograms and errors including shpae uncertainties as provided by combine
*/
{
  TH1F* hout = (TH1F*)hin->Clone(); hout->Clear();
  TFile* mlfit = new TFile("fitresults/mlfit.root", "READ");
  TH1F* shape = (TH1F*)mlfit->Get(TString("shapes_fit_s/").Append(datacard).Append("/").Append(name)); // currently problems with data and hioggsprocesses -> different name

  if(shape==0) std::cout << " No histogram found for " << name << std::endl;

  //  for(int i=0; i<hout->GetNbinsX(); ++i)
  for(int i=1; i<hout->GetNbinsX()+1; i++)
  {

    Float_t Norig = hin->GetBinContent(i)*hin->GetBinWidth(i);
    Float_t Nshape = shape->GetBinContent(i);
    Float_t scale_err = (Nshape==0) ? 1 : Norig/Nshape;

    //    hout->SetBinContent(i,shape->GetBinContent(i));
    hout->SetBinContent(i,hin->GetBinContent(i)*hin->GetBinWidth(i));
    hout->SetBinError(i,shape->GetBinError(i)*scale_err);
  }
  mlfit->Close();
  return hout;
}

void rescale(TH1F* hin, unsigned int idx)
/*
  rescale histograms according to fit results. The keywords like $Ztt will be replaced 
  by a cout statement and a scaling command.
*/
{
  switch(idx){
  case  1: // ZTT 
  $ZTT
  case  2: // TT
  $TT
  case  3: // W   [EWK1]
  $W
#if defined EXTRA_SAMPLES
  case  4: // ZJ  [EWK2]
  $ZJ
  case  5: // ZL  [EWK3]
  $ZL
#else
  case  4: // ZLL [EWK2]
  $ZLL
#endif
  case  6: // VV  [EWK ]
  $VV
  case  7: // QCD
  $QCD
#if defined MSSM
  case  8: // ggH
  $ggHTohhTo2Tau2B$MH
/*  case 9:
  $ggH_SM125 
  case 10:
  $qqH_SM125 
  case 11:
  $VH_SM125
  case 12:
  $ZHToBB_SM125
  case 13:
  $WHToBB_SM125
*/

/*
  case 9:
  $ggAToZhToLLTauTau$MA
  case 10:
  $ggAToZhToLLBB$MA
  case  11: // bbH
  $bbH$MA
*/
#else
#ifndef DROP_SIGNAL
//  case  8: // ggH
 // ${SM}ggH125
  //case  9: // qqH
  //${SM}qqH125
  //case 10: // VH
  ///${SM}VH125
#endif
#endif
  default :
    std::cout << "error histograms not known?!?" << std::endl;
  }
}

void 
//HHH_MT_X(bool scaled=true, bool log=true, float min=0.1, float max=-1., string inputfile="root/$HISTFILE", const char* directory="muTau_$CATEGORY")
HHH_MT_X(bool scaled=true, bool log=true, float min=0.1, float max=-1., string inputfile="root/$HISTFILE", const char* directory="muTau_$CATEGORY")
{
  // defining the common canvas, axes pad styles
  SetStyle(); gStyle->SetLineStyleString(11,"20 10");

  // determine category tag
  const char* category = ""; const char* category_extra = ""; const char* category_extra2 = "";
  if(std::string(directory) == std::string("muTau_2jet0tag"             )){ category = "#mu#tau_{h}";          }
  if(std::string(directory) == std::string("muTau_2jet0tag"             )){ category_extra = "2jet-0tag";          }
  if(std::string(directory) == std::string("muTau_2jet1tag"             )){ category = "#mu#tau_{h}";          }
  if(std::string(directory) == std::string("muTau_2jet1tag"             )){ category_extra = "2jet-1tag";       }
  if(std::string(directory) == std::string("muTau_2jet2tag"             )){ category = "#mu#tau_{h}";          }
  if(std::string(directory) == std::string("muTau_2jet2tag"             )){ category_extra = "2jet-2tag";         }

  const char* dataset;
#ifdef MSSM
  if(std::string(inputfile).find("7TeV")!=std::string::npos){dataset = "#scale[1.5]{CMS}  H#rightarrow hh#rightarrow#tau#tau bb                         4.9 fb^{-1} (7 TeV)";}
  if(std::string(inputfile).find("8TeV")!=std::string::npos){dataset = "#scale[1.5]{CMS}  H#rightarrow hh#rightarrow#tau#tau bb                         19.7 fb^{-1} (8 TeV)";}
  //if(std::string(inputfile).find("8TeV")!=std::string::npos){dataset = "H#rightarrow hh#rightarrow#tau#tau bb                                       19.7 fb^{-1} (8 TeV)";}
#else
  if(std::string(inputfile).find("7TeV")!=std::string::npos){dataset = "CMS, 4.9 fb^{-1} at 7 TeV";}
  if(std::string(inputfile).find("8TeV")!=std::string::npos){dataset = "CMS, 19.7 fb^{-1} at 8 TeV";}
#endif
 
  // open example histogram file
  TFile* input = new TFile(inputfile.c_str());
#ifdef MSSM
  TFile* input2 = new TFile((inputfile+"_$MH_$TANB").c_str());
#endif
  TH1F* Fakes  = refill((TH1F*)input->Get(TString::Format("%s/QCD"     , directory)), "QCD"); InitHist(Fakes, "", "", TColor::GetColor(250,202,255), 1001);
  TH1F* EWK1   = refill((TH1F*)input->Get(TString::Format("%s/W"       , directory)), "W"  ); InitHist(EWK1 , "", "", TColor::GetColor(222,90,106), 1001);
#ifdef EXTRA_SAMPLES
  TH1F* EWK2   = refill((TH1F*)input->Get(TString::Format("%s/ZJ"      , directory)), "ZJ" ); InitHist(EWK2 , "", "", TColor::GetColor(222,90,106), 1001);
  TH1F* EWK3   = refill((TH1F*)input->Get(TString::Format("%s/ZL"      , directory)), "ZL" ); InitHist(EWK3 , "", "", TColor::GetColor(222,90,106), 1001);
#else
  TH1F* EWK2   = refill((TH1F*)input->Get(TString::Format("%s/ZLL"     , directory)), "ZLL"); InitHist(EWK2 , "", "", TColor::GetColor(222,90,106), 1001);
#endif
  TH1F* EWK    = refill((TH1F*)input->Get(TString::Format("%s/VV"      , directory)), "VV" ); InitHist(EWK  , "", "", TColor::GetColor(222,90,106), 1001);
  TH1F* ttbar  = refill((TH1F*)input->Get(TString::Format("%s/TT"      , directory)), "TT" ); InitHist(ttbar, "", "", TColor::GetColor(155,152,204), 1001);
  TH1F* Ztt    = refill((TH1F*)input->Get(TString::Format("%s/ZTT"     , directory)), "ZTT"); InitHist(Ztt  , "", "", TColor::GetColor(248,206,104), 1001);
#ifdef MSSM
/*  TH1F* ggHTohhTo2Tau2B    = refill((TH1F*)input2->Get(TString::Format("%s/ggHTohhTo2Tau2B$MA" , directory)), "ggH"); InitSignal(ggHTohhTo2Tau2B); ggHTohhTo2Tau2B->Scale($TANB);
  TH1F* ggAToZhToLLTauTau = refill((TH1F*)input2->Get(TString::Format("%s/ggAToZhToLLTauTau$MA", directory)), "ggAToZHToLLTauTau"); InitSignal(ggAToZhToLLTauTau);ggAToZhToLLTauTau->Scale($TANB);
  TH1F* ggAToZhToLLBB = refill((TH1F*)input2->Get(TString::Format("%s/ggAToZhToLLBB$MA", directory)), "ggAToZHToLLBB"); InitSignal(ggAToZhToLLBB);ggAToZhToLLBB->Scale($TANB);
  TH1F* bbH    = refill((TH1F*)input2->Get(TString::Format("%s/bbH$MA" , directory)), "bbH"); InitSignal(bbH); bbH->Scale($TANB);
*/
  TH1F* ggHTohhTo2Tau2B    = refill((TH1F*)input2->Get(TString::Format("%s/ggHTohhTo2Tau2B$MH" , directory)), "ggHTohhTo2Tau2B"); InitSignal(ggHTohhTo2Tau2B); ggHTohhTo2Tau2B->Scale($TANB*SIGNAL_SCALE);
/*
  TH1F* ggAToZhToLLTauTau = refill((TH1F*)input2->Get(TString::Format("%s/ggAToZhToLLTauTau$MA", directory)), "ggAToZHToLLTauTau"); InitSignal(ggAToZhToLLTauTau); ggAToZhToLLTauTau->Scale(SIGNAL_SCALE);
  TH1F* ggAToZhToLLBB = refill((TH1F*)input2->Get(TString::Format("%s/ggAToZhToLLBB$MA", directory)), "ggAToZHToLLBB"); InitSignal(ggAToZhToLLBB); ggAToZhToLLBB->Scale(SIGNAL_SCALE);
  TH1F* bbH    = refill((TH1F*)input2->Get(TString::Format("%s/bbH$MA" , directory)), "bbH"); InitSignal(bbH); bbH->Scale(SIGNAL_SCALE);
*/

/*  TH1F* ggH_SM125= refill((TH1F*)input->Get(TString::Format("%s/ggH_SM125"  , directory)), "ggH_SM125"); InitSignal(ggH_SM125); ggH_SM125->Scale(SIGNAL_SCALE);
  TH1F* qqH_SM125= refill((TH1F*)input->Get(TString::Format("%s/qqH_SM125"  , directory)), "qqH_SM125"); InitSignal(qqH_SM125); qqH_SM125->Scale(SIGNAL_SCALE);
  TH1F* VH_SM125 = refill((TH1F*)input->Get(TString::Format("%s/VH_SM125"   , directory)), "VH_SM125" ); InitSignal(VH_SM125); VH_SM125->Scale(SIGNAL_SCALE);
  TH1F* ZHToBB_SM125 = refill((TH1F*)input->Get(TString::Format("%s/ZHToBB_SM125"   , directory)), "ZHToBB_SM125" ); InitSignal(ZHToBB_SM125); ZHToBB_SM125->Scale(SIGNAL_SCALE);
  TH1F* WHToBB_SM125 = refill((TH1F*)input->Get(TString::Format("%s/WHToBB_SM125"   , directory)), "WHToBB_SM125" ); InitSignal(WHToBB_SM125); WHToBB_SM125->Scale(SIGNAL_SCALE);
*/
/*#else
#ifndef DROP_SIGNAL
//  TH1F* ggH    = refill((TH1F*)input->Get(TString::Format("%s/ggH125"  , directory)), "ggH"); InitSignal(ggH); ggH->Scale(SIGNAL_SCALE);
//  TH1F* qqH    = refill((TH1F*)input->Get(TString::Format("%s/qqH125"  , directory)), "qqH"); InitSignal(qqH); qqH->Scale(SIGNAL_SCALE);
 // TH1F* VH     = refill((TH1F*)input->Get(TString::Format("%s/VH125"   , directory)), "VH" ); InitSignal(VH ); VH ->Scale(SIGNAL_SCALE);
#endif
*/
#endif
#ifdef ASIMOV
  TH1F* data   = refill((TH1F*)input->Get(TString::Format("%s/data_obs_asimov", directory)), "data", true);
#else
  TH1F* data   = refill((TH1F*)input->Get(TString::Format("%s/data_obs", directory)), "data",true);
#endif
  InitHist(data, "#bf{m_{H} [GeV]}", "#bf{dN/dm_{H} [1/GeV]}"); InitData(data);

  TH1F* ref=(TH1F*)Fakes->Clone("ref");
  ref->Add(EWK1 );
  ref->Add(EWK2 );
#ifdef EXTRA_SAMPLES
  ref->Add(EWK3 );
#endif
  ref->Add(EWK  );
  ref->Add(ttbar);
  ref->Add(Ztt  );

  double unscaled[8];
  unscaled[0] = Fakes->Integral();
  unscaled[1] = EWK  ->Integral();
  unscaled[1]+= EWK1 ->Integral();
  unscaled[1]+= EWK2 ->Integral();
#ifdef EXTRA_SAMPLES
  unscaled[1]+= EWK3 ->Integral();
#endif
  unscaled[2] = ttbar->Integral();
  unscaled[3] = Ztt  ->Integral();
#ifdef MSSM
  unscaled[4] = ggHTohhTo2Tau2B  ->Integral();
  /*unscaled[5] += ggH_SM125->Integral();
  unscaled[5] += qqH_SM125->Integral();
  unscaled[5] += VH_SM125->Integral();
  unscaled[5] +=ZHToBB_SM125->Integral();
  unscaled[5] +=WHToBB_SM125->Integral();
*/
/*
  unscaled[5] = ggAToZhToLLTauTau->Integral();
  unscaled[6] = ggAToZhToLLBB->Integral();
  unscaled[7] = bbH  ->Integral();
*/
/*#else
#ifndef DROP_SIGNAL
//  unscaled[4] = ggH  ->Integral();
//  unscaled[5] = qqH  ->Integral();
 // unscaled[6] = VH   ->Integral();
#endif
*/
#endif


  if(scaled){

 /* Fakes = refill(shape_histos(Fakes, datacard, "QCD"), "QCD");
  EWK1 = refill(shape_histos(EWK1, datacard, "W"), "W"); 
#ifdef EXTRA_SAMPLES
  EWK2 = refill(shape_histos(EWK2, datacard, "ZJ"), "ZJ");
  EWK3 = refill(shape_histos(EWK3, datacard, "ZL"), "ZL");
#else
  //  EWK2 = refill(shape_histos(EWK2, datacard, "ZLL"), "ZLL");
#endif
  EWK = refill(shape_histos(EWK, datacard, "VV"), "VV");
  ttbar = refill(shape_histos(ttbar, datacard, "TT"), "TT");
  Ztt = refill(shape_histos(Ztt, datacard, "ZTT"), "ZTT");
#ifdef MSSM
    ggHTohhTo2Tau2B = refill(shape_histos(ggHTohhTo2Tau2B, datacard, "ggHTohhTo2Tau2B$MA"), "ggHTohhTo2Tau2B$MA"); 
    bbH = refill(shape_histos(bbH, datacard, "bbH$MA"), "bbH$MA"); 
#else
#ifndef DROP_SIGNAL
    ggH = refill(shape_histos(ggH, datacard, "ggH"), "ggH"); 
    qqH = refill(shape_histos(qqH, datacard, "qqH"), "qqH"); 
    VH = refill(shape_histos(VH, datacard, "VH"), "VH"); 

#endif  
#endif
*/

    rescale(Fakes, 7); 
    rescale(EWK1 , 3); 
    rescale(EWK2 , 4); 
#ifdef EXTRA_SAMPLES
    rescale(EWK3 , 5);
#endif 
    rescale(EWK  , 6); 
    rescale(ttbar, 2); 
    rescale(Ztt  , 1);
#ifdef MSSM
    rescale(ggHTohhTo2Tau2B  , 8); 
    /*rescale(ggH_SM125,9);
    rescale(qqH_SM125,10);
    rescale(VH_SM125,11);
    rescale(ZHToBB_SM125,12);
    rescale(WHToBB_SM125,13);
*/
/*
    rescale(ggAToZhToLLTauTau,9);
    rescale(ggAToZhToLLBB,10);
    rescale(bbH  , 11);  
*/
/*#else
#ifndef DROP_SIGNAL
//    rescale(ggH  , 8); 
//    rescale(qqH  , 9);  
 //   rescale(VH   ,10);  
#endif
*/
#endif
  }

  TH1F* scales[5];
  scales[0] = new TH1F("scales-Fakes", "", 8, 0, 8);
  scales[0]->SetBinContent(1, unscaled[0]>0 ? (Fakes->Integral()/unscaled[0]-1.) : 0.);
  scales[1] = new TH1F("scales-EWK"  , "", 8, 0, 8);
  scales[1]->SetBinContent(2, unscaled[1]>0 ? ((EWK  ->Integral()
					       +EWK1 ->Integral()
					       +EWK2 ->Integral()
#ifdef EXTRA_SAMPLES
					       +EWK3 ->Integral()
#endif
						)/unscaled[1]-1.) : 0.);
  scales[2] = new TH1F("scales-ttbar", "", 8, 0, 8);
  scales[2]->SetBinContent(3, unscaled[2]>0 ? (ttbar->Integral()/unscaled[2]-1.) : 0.);
  scales[3] = new TH1F("scales-Ztt"  , "", 8, 0, 8);
  scales[3]->SetBinContent(4, unscaled[3]>0 ? (Ztt  ->Integral()/unscaled[3]-1.) : 0.);
#ifdef MSSM
  scales[4] = new TH1F("scales-ggHTohhTo2Tau2B"  , "", 8, 0, 8);
  scales[4]->SetBinContent(5, unscaled[4]>0 ? (ggHTohhTo2Tau2B  ->Integral()/unscaled[4]-1.) : 0.);
 // scales[5] = new TH1F("scales-SM","",8,0,8);
  //scales[5]->SetBinContent(6,unscaled[5]>0 ? ((ggH_SM125->Integral()+qqH_SM125->Integral()+VH_SM125->Integral()+ZHToBB_SM125->Integral()+WHToBB_SM125->Integral())/unscaled[5]-1.): 0.);
/*
  scales[5] = new TH1F("scales-ggAToZhToLLTauTau", "",8,0,8);
  scales[5]->SetBinContent(6, unscaled[5]>0 ? (ggAToZhToLLTauTau->Integral()/unscaled[5]-1.) : 0.);
  scales[6] = new TH1F("scales-ggAToZhToLLBB","",8,0,8);
  scales[6]->SetBinContent(7,unscaled[6]>0 ? (ggAToZhToLLBB->Integral()/unscaled[6]-1.) : 0.);
  scales[7] = new TH1F("scales-bbH"  , "", 8, 0, 8);
  scales[7]->SetBinContent(8, unscaled[7]>0 ? (bbH  ->Integral()/unscaled[7]-1.) : 0.);
*/
/*#else
#ifndef DROP_SIGNAL
  scales[4] = new TH1F("scales-ggH"  , "", 7, 0, 7);
  scales[4]->SetBinContent(5, unscaled[4]>0 ? (ggH  ->Integral()/unscaled[4]-1.) : 0.);
  scales[5] = new TH1F("scales-qqH"  , "", 7, 0, 7);
  scales[5]->SetBinContent(6, unscaled[5]>0 ? (qqH  ->Integral()/unscaled[5]-1.) : 0.);
  scales[6] = new TH1F("scales-VH"   , "", 7, 0, 7);
  scales[6]->SetBinContent(7, unscaled[6]>0 ? (VH   ->Integral()/unscaled[6]-1.) : 0.);

#endif
*/
#endif

/*#ifdef MSSM
//  qqH_SM125->Add(ggH_SM125);
 // VH_SM125->Add(qqH_SM125);
  //Fakes->Add(VH_SM125);
#endif
*/
  Fakes->Add(ttbar);
  EWK1 ->Add(Fakes);
  EWK2 ->Add(EWK1 );
#ifdef EXTRA_SAMPLES
  EWK3 ->Add(EWK2 );
  EWK  ->Add(EWK3 );
#else
  EWK  ->Add(EWK2 );
#endif
  Ztt  ->Add(EWK);
/*ggH_SM125->Add(qqH_SM125);
ggH_SM125->Add(VH_SM125);
ggH_SM125->Add(ZHToBB_SM125);
ggH_SM125->Add(WHToBB_SM125);
*/
/*  if(log){
#ifdef MSSM
    //ggH  ->Add(bbH);
#else
#ifndef DROP_SIGNAL
 //   qqH  ->Add(VH );
  //  ggH  ->Add(qqH);
#endif
#endif

  }
  else{
#ifdef MSSM    
    //bbH  ->Add(Ztt);
    //ggH  ->Add(bbH);
#else
#ifndef DROP_SIGNAL
    //VH   ->Add(Ztt);
   // qqH  ->Add(VH );
   // ggH  ->Add(qqH);
#endif
#endif
  }
*/

  /*
    Mass plot before and after fit
  */
  TCanvas *canv = MakeCanvas("canv", "histograms", 600, 600);

  canv->cd();
  if(log){ canv->SetLogy(1); }
#if defined MSSM
  if(!log){ data->GetXaxis()->SetRange(200, data->FindBin(UPPER_EDGE)); } else{ data->GetXaxis()->SetRange(200, data->FindBin(UPPER_EDGE)); };
#else
  data->GetXaxis()->SetRange(200, data->FindBin(UPPER_EDGE));
#endif
  data->SetNdivisions(505);
  data->SetMinimum(min);
#ifndef DROP_SIGNAL
  data->SetMaximum(max>0 ? max : std::max(std::max(maximum(data, log), maximum(Ztt, log)), maximum(ggHTohhTo2Tau2B, log)));
#else
  data->SetMaximum(max>0 ? max : std::max(maximum(data, log), maximum(Ztt, log)));
#endif
  data->Draw("e");

  TH1F* errorBand = (TH1F*)Ztt ->Clone("errorBand");
  errorBand  ->SetMarkerSize(0);
  errorBand  ->SetFillColor(13);
  errorBand  ->SetFillStyle(3013);
  errorBand  ->SetLineWidth(1);
  for(int idx=0; idx<errorBand->GetNbinsX(); ++idx){
    if(errorBand->GetBinContent(idx)>0){
      std::cout << "Uncertainties on summed background samples: " << errorBand->GetBinError(idx)/errorBand->GetBinContent(idx) << std::endl;
      break;
    }
  }
  if(log){
    Ztt  ->Draw("histsame");
    EWK  ->Draw("histsame");
    Fakes->Draw("histsame");
    ttbar->Draw("histsame");
#ifdef MSSM
    //VH_SM125->Draw("histsame");
#endif   
    $DRAW_ERROR
#ifndef DROP_SIGNAL
    ggHTohhTo2Tau2B  ->Draw("histsame");
    //ggH_SM125->SetLineColor(kRed);
    //ggH_SM125->Draw("histsame");
#endif
  }
  else{
    Ztt  ->Draw("histsame");
    EWK  ->Draw("histsame");
    Fakes->Draw("histsame");
    ttbar->Draw("histsame");
#ifdef MSSM
    //VH_SM125->Draw("histsame");
#endif   
    $DRAW_ERROR
 #ifndef DROP_SIGNAL
    ggHTohhTo2Tau2B  ->Draw("histsame");
    //ggH_SM125->SetLineColor(kRed);
    //ggH_SM125->Draw("histsame");
#endif
}
  data->Draw("esame");
  canv->RedrawAxis();

  //CMSPrelim(dataset, "#tau_{#mu}#tau_{h}", 0.17, 0.835);
  CMSPrelim(dataset, "", 0.16, 0.835);
#if defined MSSM
  TPaveText* chan     = new TPaveText(0.20, 0.74+0.061, 0.32, 0.74+0.161, "tlbrNDC");
  if (strcmp(category_extra2,"")!=0) chan     = new TPaveText(0.20, 0.69+0.061, 0.32, 0.74+0.161, "tlbrNDC");
#else
  TPaveText* chan     = new TPaveText(0.52, 0.35, 0.91, 0.55, "tlbrNDC");
#endif
  chan->SetBorderSize(   0 );
  chan->SetFillStyle(    0 );
  chan->SetTextAlign(   12 );
  chan->SetTextSize ( 0.05 );
  chan->SetTextColor(    1 );
  chan->SetTextFont (   62 );
  chan->AddText(category);
  chan->AddText(category_extra);
#if defined MSSM
  if (strcmp(category_extra2,"")!=0) chan->AddText(category_extra2);
#else
  chan->AddText(category_extra2);
#endif
  chan->Draw();

/*  TPaveText* cat      = new TPaveText(0.20, 0.71+0.061, 0.32, 0.71+0.161, "NDC");
  cat->SetBorderSize(   0 );
  cat->SetFillStyle(    0 );
  cat->SetTextAlign(   12 );
  cat->SetTextSize ( 0.05 );
  cat->SetTextColor(    1 );
  cat->SetTextFont (   62 );
  cat->AddText(category_extra);
  cat->Draw();

  TPaveText* cat2      = new TPaveText(0.20, 0.66+0.061, 0.32, 0.66+0.161, "NDC");
  cat2->SetBorderSize(   0 );
  cat2->SetFillStyle(    0 );
  cat2->SetTextAlign(   12 );
  cat2->SetTextSize ( 0.05 );
  cat2->SetTextColor(    1 );
  cat2->SetTextFont (   62 );
  cat2->AddText(category_extra2);
  cat2->Draw();
*/
#ifdef MSSM
  TPaveText* massA      = new TPaveText(0.53, 0.44+0.061, 0.95, 0.44+0.151, "NDC");
  massA->SetBorderSize(   0 );
  massA->SetFillStyle(    0 );
  massA->SetTextAlign(   12 );
  massA->SetTextSize ( 0.03 );
  massA->SetTextColor(    1 );
  massA->SetTextFont (   62 );
  massA->AddText("MSSM low-tan#beta-high scenario");
  massA->AddText("m_{H}=$MH GeV, tan#beta=$TANB");
  massA->Draw();
#endif

#ifdef MSSM
  TLegend* leg = new TLegend(0.53, 0.60, 0.95, 0.90);
  SetLegendStyle(leg);
  leg->AddEntry(ggHTohhTo2Tau2B  , TString::Format("%.0f#timesH#rightarrowhh#rightarrow#tau#taubb",SIGNAL_SCALE) , "L" );
//  leg->AddEntry(ggH_SM125, TString::Format("%.0f#times SM H(125 GeV) #rightarrow #tau#tau/bb ",SIGNAL_SCALE),"L");
#else
  TLegend* leg = new TLegend(0.52, 0.58, 0.92, 0.89);
  SetLegendStyle(leg);
#ifndef DROP_SIGNAL
/*  if(SIGNAL_SCALE!=1){
    leg->AddEntry(ggH  , TString::Format("%.0f#timesH(125 GeV)#rightarrow#tau#tau", SIGNAL_SCALE) , "L" );
  }
  else{
    leg->AddEntry(ggH  , "SM H(125 GeV)#rightarrow#tau#tau" , "L" );
*/
  }
#endif
#endif
#ifdef ASIMOV
  leg->AddEntry(data , "sum(bkg) + H(125)"              , "LP");
#else
  leg->AddEntry(data , "Observed"                       , "LP");
#endif
  leg->AddEntry(Ztt  , "Z#rightarrow#tau#tau"           , "F" );
  leg->AddEntry(EWK  , "Electroweak"                    , "F" );
  leg->AddEntry(Fakes, "QCD"                            , "F" );
  leg->AddEntry(ttbar, "t#bar{t}"                       , "F" );
#ifdef MSSM
//  leg->AddEntry(VH_SM125, "SM H(125 GeV) #rightarrow #tau#tau", "F" );
#endif
  $ERROR_LEGEND
  leg->Draw();

  /*
    Ratio Data over MC
  */
  TCanvas *canv0 = MakeCanvas("canv0", "histograms", 600, 400);
  canv0->SetGridx();
  canv0->SetGridy();
  canv0->cd();

  TH1F* model = (TH1F*)Ztt ->Clone("model");
  TH1F* test1 = (TH1F*)data->Clone("test1"); 
  for(int ibin=0; ibin<test1->GetNbinsX(); ++ibin){
    //the small value in case of 0 entries in the model is added to prevent the chis2 test from failing
    model->SetBinContent(ibin+1, model->GetBinContent(ibin+1)>0 ? model->GetBinContent(ibin+1)*model->GetBinWidth(ibin+1) : 0.01);
    model->SetBinError  (ibin+1, CONVERVATIVE_CHI2 ? 0. : model->GetBinError  (ibin+1)*model->GetBinWidth(ibin+1));
    test1->SetBinContent(ibin+1, test1->GetBinContent(ibin+1)*test1->GetBinWidth(ibin+1));
    test1->SetBinError  (ibin+1, test1->GetBinError  (ibin+1)*test1->GetBinWidth(ibin+1));
  }
  double chi2prob =0.;
  double chi2ndof = 0.;
  double ksprob=0.;
  double ksprobpe=0.;
 
if(!BLIND_DATA){
  chi2prob = test1->Chi2Test      (model,"PUW");        std::cout << "chi2prob:" << chi2prob << std::endl;
  chi2ndof = test1->Chi2Test      (model,"CHI2/NDFUW"); std::cout << "chi2ndf :" << chi2ndof << std::endl;
  ksprob   = test1->KolmogorovTest(model);              std::cout << "ksprob  :" << ksprob   << std::endl;
  ksprobpe = test1->KolmogorovTest(model,"DX");         std::cout << "ksprobpe:" << ksprobpe << std::endl;  
}

  std::vector<double> edges;
  TH1F* zero = (TH1F*)ref->Clone("zero"); zero->Clear();
  TH1F* rat1 = (TH1F*)data->Clone("rat1"); 
  for(int ibin=0; ibin<rat1->GetNbinsX(); ++ibin){
    rat1->SetBinContent(ibin+1, Ztt->GetBinContent(ibin+1)>0 ? data->GetBinContent(ibin+1)/Ztt->GetBinContent(ibin+1) : 0);
    rat1->SetBinError  (ibin+1, Ztt->GetBinContent(ibin+1)>0 ? data->GetBinError  (ibin+1)/Ztt->GetBinContent(ibin+1) : 0);
    zero->SetBinContent(ibin+1, 0.);
    zero->SetBinError  (ibin+1, Ztt->GetBinContent(ibin+1)>0 ? Ztt ->GetBinError  (ibin+1)/Ztt->GetBinContent(ibin+1) : 0);
  }
  for(int ibin=0; ibin<rat1->GetNbinsX(); ++ibin){
    if(rat1->GetBinContent(ibin+1)>0){
      edges.push_back(TMath::Abs(rat1->GetBinContent(ibin+1)-1.)+TMath::Abs(rat1->GetBinError(ibin+1)));
      // catch cases of 0 bins, which would lead to 0-alpha*0-1
      rat1->SetBinContent(ibin+1, rat1->GetBinContent(ibin+1)-1.);
    }
  }
  float range = 0.1;
  std::sort(edges.begin(), edges.end());
if(edges.size()>1){
  if (edges[edges.size()-2]>0.1) { range = 0.2; }
  if (edges[edges.size()-2]>0.2) { range = 0.5; }
  if (edges[edges.size()-2]>0.5) { range = 1.0; }
  if (edges[edges.size()-2]>1.0) { range = 1.5; }
  if (edges[edges.size()-2]>1.5) { range = 2.0; }
}
  rat1->SetLineColor(kBlack);
  rat1->SetFillColor(kGray );
  rat1->SetMaximum(+range);
  rat1->SetMinimum(-range);
  rat1->GetYaxis()->CenterTitle();
  rat1->GetYaxis()->SetTitle("#bf{Data/MC-1}");
  rat1->GetXaxis()->SetTitle("#bf{m_{H} [GeV]}");
  rat1->Draw();
  zero->SetFillStyle(  3013);
  zero->SetFillColor(kBlack);
  zero->SetLineColor(kBlack);
  zero->SetMarkerSize(0.1);
  zero->Draw("e2histsame");
  canv0->RedrawAxis();

  TPaveText* stat1 = new TPaveText(0.20, 0.76+0.061, 0.32, 0.76+0.161, "NDC");
  stat1->SetBorderSize(   0 );
  stat1->SetFillStyle(    0 );
  stat1->SetTextAlign(   12 );
  stat1->SetTextSize ( 0.05 );
  stat1->SetTextColor(    1 );
  stat1->SetTextFont (   62 );
if(!BLIND_DATA){
  stat1->AddText(TString::Format("#chi^{2}/ndf=%.3f,  P(#chi^{2})=%.3f", chi2ndof, chi2prob));
}
  //stat1->AddText(TString::Format("#chi^{2}/ndf=%.3f,  P(#chi^{2})=%.3f, P(KS)=%.3f", chi2ndof, chi2prob, ksprob));
  stat1->Draw();

  /*
    Ratio After fit over Prefit
  */
  TCanvas *canv1 = MakeCanvas("canv1", "histograms", 600, 400);
  canv1->SetGridx();
  canv1->SetGridy();
  canv1->cd();

  edges.clear();
  TH1F* rat2 = (TH1F*) Ztt->Clone("rat2");
  for(int ibin=0; ibin<rat2->GetNbinsX(); ++ibin){
    rat2->SetBinContent(ibin+1, ref->GetBinContent(ibin+1)>0 ? Ztt->GetBinContent(ibin+1)/ref->GetBinContent(ibin+1) : 0);
    rat2->SetBinError  (ibin+1, ref->GetBinContent(ibin+1)>0 ? Ztt->GetBinError  (ibin+1)/ref->GetBinContent(ibin+1) : 0);
  }
  for(int ibin=0; ibin<rat2->GetNbinsX(); ++ibin){
    if(rat2->GetBinContent(ibin+1)>0){
      edges.push_back(TMath::Abs(rat2->GetBinContent(ibin+1)-1.)+TMath::Abs(rat2->GetBinError(ibin+1)));
      // catch cases of 0 bins, which would lead to 0-alpha*0-1
      rat2 ->SetBinContent(ibin+1, rat2->GetBinContent(ibin+1)-1.);
    }
  }
  range = 0.1;
  std::sort(edges.begin(), edges.end());
if(edges.size()>1){
  if (edges[edges.size()-2]>0.1) { range = 0.2; }
  if (edges[edges.size()-2]>0.2) { range = 0.5; }
  if (edges[edges.size()-2]>0.5) { range = 1.0; }
  if (edges[edges.size()-2]>1.0) { range = 1.5; }
  if (edges[edges.size()-2]>1.5) { range = 2.0; }
}
#if defined MSSM
  if(!log){ rat2->GetXaxis()->SetRange(200, rat2->FindBin(UPPER_EDGE)); } else{ rat2->GetXaxis()->SetRange(200, rat2->FindBin(UPPER_EDGE)); };
#else
  rat2->GetXaxis()->SetRange(200, rat2->FindBin(UPPER_EDGE));
#endif
  rat2->SetNdivisions(505);
  rat2->SetLineColor(kRed+ 3);
  rat2->SetMarkerColor(kRed+3);
  rat2->SetMarkerSize(1.1);
  rat2->SetMaximum(+range);
  rat2->SetMinimum(-range);
  rat2->GetYaxis()->SetTitle("#bf{Postfit/Prefit-1}");
  rat2->GetYaxis()->CenterTitle();
  rat2->GetXaxis()->SetTitle("#bf{m_{H} [GeV]}");
  rat2->Draw();
  zero->SetFillStyle(  3013);
  zero->SetFillColor(kBlack);
  zero->SetLineColor(kBlack);
  zero->Draw("e2histsame");
  canv1->RedrawAxis();

  /*
    Relative shift per sample
  */
  TCanvas *canv2 = MakeCanvas("canv2", "histograms", 600, 400);
  canv2->SetGridx();
  canv2->SetGridy();
  canv2->cd();

  InitHist  (scales[0], "", "", TColor::GetColor(250,202,255), 1001);
  InitHist  (scales[1], "", "", TColor::GetColor(222,90,106), 1001);
  InitHist  (scales[2], "", "", TColor::GetColor(155,152,204), 1001);
  InitHist  (scales[3], "", "", TColor::GetColor(248,206,104), 1001);
#ifndef DROP_SIGNAL
  InitHist(scales[4],"","",kGreen+2,1001);
/*  InitHist(scales[5],"","",kGreen+2,1001);
  InitHist(scales[6],"","",kGreen+2,1001);
  InitHist(scales[7],"","",kGreen+2,1001);
*/
#endif
  scales[0]->Draw();
  scales[0]->GetXaxis()->SetBinLabel(1, "#bf{Fakes}");
  scales[0]->GetXaxis()->SetBinLabel(2, "#bf{EWK}"  );
  scales[0]->GetXaxis()->SetBinLabel(3, "#bf{ttbar}");
  scales[0]->GetXaxis()->SetBinLabel(4, "#bf{Ztt}"  );
#ifdef MSSM
  scales[0]->GetXaxis()->SetBinLabel(5, "#bf{ggHTohhTo2Tau2B}"  );
/*
  scales[0]->GetXaxis()->SetBinLabel(6, "#bf{ggAToZhToLLTauTau}"  );
  scales[0]->GetXaxis()->SetBinLabel(7, "#bf{ggAToZhToLLBB}"      );
  scales[0]->GetXaxis()->SetBinLabel(8, "#bf{bbH}");
*/
/*#else
  scales[0]->GetXaxis()->SetBinLabel(5, "#bf{ggH}"  );
  scales[0]->GetXaxis()->SetBinLabel(6, "#bf{qqH}"  );
  scales[0]->GetXaxis()->SetBinLabel(7, "#bf{VH}"   );
*/
#endif
  scales[0]->SetMaximum(+0.5);
  scales[0]->SetMinimum(-0.5);
  scales[0]->GetYaxis()->CenterTitle();
  scales[0]->GetYaxis()->SetTitle("#bf{Postfit/Prefit-1}");
  scales[1]->Draw("same");
  scales[2]->Draw("same");
  scales[3]->Draw("same");
#ifdef MSSM
  scales[4]->Draw("same");
/*#else
#ifndef DROP_SIGNAL
  scales[4]->Draw("same");
  scales[5]->Draw("same");
  scales[6]->Draw("same");
#endif
*/
#endif
  TH1F* zero_samples = (TH1F*)scales[0]->Clone("zero_samples"); zero_samples->Clear();
  zero_samples->SetBinContent(1,0.);
  zero_samples->Draw("same"); 
  canv2->RedrawAxis();

  /*
    prepare output
  */
  bool isSevenTeV = std::string(inputfile).find("7TeV")!=std::string::npos;
  canv   ->Print(TString::Format("%s_%sfit_%s_%s.png"       , directory, scaled ? "post" : "pre", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "LIN")); 
  canv   ->Print(TString::Format("%s_%sfit_%s_%s.pdf"       , directory, scaled ? "post" : "pre", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "LIN")); 
  canv   ->Print(TString::Format("%s_%sfit_%s_%s.eps"       , directory, scaled ? "post" : "pre", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "LIN")); 
  if(!log || FULLPLOTS)
  {
    canv0->Print(TString::Format("%s_datamc_%sfit_%s_%s.png", directory, scaled ? "post" : "pre", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "LIN")); 
    canv0->Print(TString::Format("%s_datamc_%sfit_%s_%s.pdf", directory, scaled ? "post" : "pre", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "LIN"));
    canv0->Print(TString::Format("%s_datamc_%sfit_%s_%s.eps", directory, scaled ? "post" : "pre", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "LIN"));
  }
  if((!log && scaled) || FULLPLOTS)
  {
    canv1->Print(TString::Format("%s_prefit_%sfit_%s_%s.png", directory, scaled ? "post" : "pre", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "LIN")); 
    canv1->Print(TString::Format("%s_prefit_%sfit_%s_%s.pdf", directory, scaled ? "post" : "pre", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "LIN"));
    canv1->Print(TString::Format("%s_prefit_%sfit_%s_%s.eps", directory, scaled ? "post" : "pre", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "LIN"));
    canv2->Print(TString::Format("%s_sample_%sfit_%s_%s.png", directory, scaled ? "post" : "pre", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "LIN")); 
    canv2->Print(TString::Format("%s_sample_%sfit_%s_%s.pdf", directory, scaled ? "post" : "pre", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "LIN"));
    canv2->Print(TString::Format("%s_sample_%sfit_%s_%s.eps", directory, scaled ? "post" : "pre", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "LIN"));
  }
 
  TFile* output = new TFile(TString::Format("%s_%sfit_%s_%s.root", directory, scaled ? "post" : "pre", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "LIN"), "update");
  output->cd();
  data ->Write("data_obs");
  Fakes->Write("Fakes"   );
  EWK  ->Write("EWK"     );
  ttbar->Write("ttbar"   );
  Ztt  ->Write("Ztt"     );
#ifdef MSSM
  ggHTohhTo2Tau2B  ->Write("ggHTohhTo2Tau2B"     );
/*
  ggAToZhToLLTauTau->Write("ggAToZhToLLTauTau");
  ggAToZhToLLBB->Write("ggAToZhToLLBB");
  bbH  ->Write("bbH"     );
*/
//  ggH_SM125->Write("ggH_SM125");
  //qqH_SM125->Write("qqH_SM125");
  //VH_SM125 ->Write("VH_SM125");
/*#else
#ifndef DROP_SIGNAL
 // ggH  ->Write("ggH"     );
  //qqH  ->Write("qqH"     );
 // VH   ->Write("VH"      );
#endif
*/
#endif
  if(errorBand){
    errorBand->Write("errorBand");
  }
  output->Close();
 
  delete errorBand;
  delete model;
  delete test1;
  delete zero;
  delete rat1;
  delete rat2;
  delete zero_samples;
  delete ref;
}
