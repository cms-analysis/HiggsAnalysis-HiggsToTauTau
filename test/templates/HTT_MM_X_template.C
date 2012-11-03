#include <iostream>

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

#include "$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"

$DEFINE_DROP_SIGNAL
$DEFINE_MSSM

/**
   \class   HTT_MM_X_template HTT_MM_X_template.C "HiggsAnalysis/HiggsToTauTau/postfit/tamplates/HTT_MM_X_template.C"

   \brief   macro template to create pre-/postfit plots of the inputs to the limit calculation

   This is a macro template to create pre-/postfit plots of the inputs tp the limit calculation.
   This macro is picked up from the produce_macros.py script in the HiggsAnalysis/HiggsToTauTau/postfit
   directory. The key words in the replace(...) function are replaced by proper values that have
   been calculated from the uncertainties as picked up from the datacards in the postfit/datacards 
   directory of the package and the pulls of the fit as picked up from the maximum likelihood fit 
   results file in the postfit/fitresults directory of the package.

   
   In the headline of the main macro the keywords HTT_MM_X, $HISTFILE and $CATEGORY will be 
   replaced by proper names according to the inputfile and event category, for which the polts 
   are supposed to be made.
*/

static const bool BLIND_DATA = false; //false;
float blinding_SM(float mass){ return (100<mass && mass<150); }
float blinding_MSSM(float mass){ return (100<mass); }
float maximum(TH1F* h, bool LOG=false){
  if(LOG){
    if(h->GetMaximum()>1000){ return 1000.*TMath::Nint(500*h->GetMaximum()/1000.); }
    if(h->GetMaximum()>  10){ return   10.*TMath::Nint( 50*h->GetMaximum()/  10.); }
    return 50*h->GetMaximum(); 
  }
  else{
    if(h->GetMaximum()>  12){ return 10.*TMath::Nint((1.3*h->GetMaximum()/10.)); }
    if(h->GetMaximum()> 1.2){ return TMath::Nint((1.6*h->GetMaximum())); }
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
    std::cout << "hist not found: " << sample << "  -- close here" << std::endl;
    exit(1);  
  }
  TH1F* hout = (TH1F*)hin->Clone(); hout->Clear();
  for(int i=0; i<hout->GetNbinsX(); ++i){
    if(data){
#if defined MSSM
      hout->SetBinContent(i+1, BLIND_DATA && blinding_MSSM(hin->GetBinCenter(i+1)) ? 0. : hin->GetBinContent(i+1)/hin->GetBinWidth(i+1));
      hout->SetBinError  (i+1, BLIND_DATA && blinding_MSSM(hin->GetBinCenter(i+1)) ? 0. : hin->GetBinError(i+1)/hin->GetBinWidth(i+1));
#else
      hout->SetBinContent(i+1, BLIND_DATA && blinding_SM(hin->GetBinCenter(i+1)) ? 0. : hin->GetBinContent(i+1)/hin->GetBinWidth(i+1));
      hout->SetBinError  (i+1, BLIND_DATA && blinding_SM(hin->GetBinCenter(i+1)) ? 0. : hin->GetBinError(i+1)/hin->GetBinWidth(i+1));
#endif
    }
    else{
      hout->SetBinContent(i+1, hin->GetBinContent(i+1)/hin->GetBinWidth(i+1));
      hout->SetBinError(i+1, 0.);
    }
  }
  return hout;
}


void rescale(TH1F* hin, unsigned int idx)
/*
  rescale histograms according to fit results. The keywords like $Ztt will be replaced 
  by a cout statement and a scaling command.
*/
{
  switch(idx){
  case 1: // ZTT 
  $ZTT  
  case 2: // ZMM 
  $ZMM 
  case 3: // TTJ 
  $TTJ
  case 4: // QCD
  $QCD
  case 5: // Dibosons
  $Dibosons
  case 6: // WJets
  $WJets
#if defined MSSM
  case 7: // ggH
  ${MSSM}ggH160
  case 8: // bbH
  ${MSSM}bbH160
#else
#ifndef DROP_SIGNAL
  case 7: // ggH
  ${SM}ggH125
  case 8: // qqH
  ${SM}qqH125
  case 9: // VH
  ${SM}VH125
#endif
#endif
  default :
    std::cout << "error histograms not known?!?" << std::endl;
  }
}

void 
HTT_MM_X(bool scaled=true, bool log=true, float min=0.1, float max=-1., const char* inputfile="root/$HISTFILE", const char* directory="mumu_$CATEGORY")
{
  // define common canvas, axes pad styles
  SetStyle(); gStyle->SetLineStyleString(11,"20 10");

  const char* dataset;
  if(std::string(inputfile).find("7TeV")!=std::string::npos){dataset = "Preliminary, #sqrt{s} = 7 TeV, L = 4.9 fb^{-1}";}
  if(std::string(inputfile).find("8TeV")!=std::string::npos){dataset = "Preliminary, #sqrt{s} = 8 TeV, L = 12.0 fb^{-1}";}
  
  TFile* input = new TFile(inputfile);
  TH1F* ZTT = refill((TH1F*)input->Get(TString::Format("%s/ZTT"   , directory)), "ZTT"); InitHist(ZTT, "", "", kOrange-4, 1001);
  TH1F* ZMM    = refill((TH1F*)input->Get(TString::Format("%s/ZMM"     , directory)), "ZMM"); InitHist(ZMM  , "", "", kAzure+2, 1001);
  TH1F* TTJ  = refill((TH1F*)input->Get(TString::Format("%s/TTJ"   , directory)), "TTJ"); InitHist(TTJ, "", "", kBlue-8, 1001);
  TH1F* QCD    = refill((TH1F*)input->Get(TString::Format("%s/QCD"     , directory)), "QCD"); InitHist(QCD  , "", "", kMagenta - 10, 1001);
  TH1F* Dibosons  = refill((TH1F*)input->Get(TString::Format("%s/Dibosons"   , directory)), "Dibosons"); InitHist(Dibosons, "", "", kRed + 2, 1001);
  TH1F* WJets    = refill((TH1F*)input->Get(TString::Format("%s/WJets"     , directory)), "WJets"); InitHist(WJets  , "", "", kGreen - 4, 1001);
#ifdef MSSM
  float ggHScale = 1., bbHScale = 1.; // scenario for MSSM, mhmax, mA=160, tanb=8, times 10 for the time being
  if(std::string(inputfile).find("7TeV")!=std::string::npos){ ggHScale = 10*1300.*0.11/1000.; bbHScale = 10*4030.*0.11/1000.; }
  if(std::string(inputfile).find("8TeV")!=std::string::npos){ ggHScale = 10*1690.*0.11/1000.; bbHScale = 10*5370.*0.11/1000.; }
  TH1F* ggH    = refill((TH1F*)input->Get(TString::Format("%s/ggH160"  , directory)), "ggH"  ); InitSignal(ggH); ggH->Scale(ggHScale);
  TH1F* bbH    = refill((TH1F*)input->Get(TString::Format("%s/bbH160"  , directory)), "bbH"  ); InitSignal(bbH); bbH->Scale(bbHScale);
#else
#ifndef DROP_SIGNAL
  TH1F* ggH    = refill((TH1F*)input->Get(TString::Format("%s/ggH125"  , directory)), "ggH"  ); InitSignal(ggH); //ggH->Scale(5);
  TH1F* qqH    = refill((TH1F*)input->Get(TString::Format("%s/qqH125"  , directory)), "qqH"  ); InitSignal(qqH); //qqH->Scale(5);
  TH1F* VH     = refill((TH1F*)input->Get(TString::Format("%s/VH125"   , directory)), "VH"   ); InitSignal(VH ); //VH ->Scale(5);
#endif
#endif
  TH1F* data   = refill((TH1F*)input->Get(TString::Format("%s/data_obs", directory)), "data", true);
  InitHist(data, "#bf{m_{#tau#tau} [GeV]}", "#bf{dN/dm_{#tau#tau} [1/GeV]}"); InitData(data);

  TH1F* ref=(TH1F*)ZTT->Clone("ref");
  ref->Add(ZMM  );
  ref->Add(TTJ);
  ref->Add(QCD  );
  ref->Add(Dibosons);
  ref->Add(WJets  );

  double unscaled[9];
  unscaled[0] = ZTT->Integral();
  unscaled[1] = ZMM  ->Integral();
  unscaled[2] = TTJ->Integral();
  unscaled[3] = QCD  ->Integral();
  unscaled[4] = Dibosons  ->Integral();
  unscaled[5] = WJets  ->Integral();
#ifdef MSSM
  unscaled[6] = ggH  ->Integral();
  unscaled[7] = bbH  ->Integral();
  unscaled[8] = 0;
#else
#ifndef DROP_SIGNAL
  unscaled[6] = ggH  ->Integral();
  unscaled[7] = qqH  ->Integral();
  unscaled[8] = VH   ->Integral();
#endif
#endif
  
  if(scaled){
    rescale(ZTT, 1); 
    rescale(ZMM,   2); 
    rescale(TTJ, 3); 
    rescale(QCD,   4); 
    rescale(Dibosons, 5); 
    rescale(WJets,   6);
#ifdef MSSM 
    rescale(ggH,   7);
    rescale(bbH,   8);
#else
#ifndef DROP_SIGNAL
    rescale(ggH,   7);
    rescale(qqH,   8);
    rescale(VH,   9);
#endif
#endif
  }

  TH1F* scales[9];
  scales[0] = new TH1F("scales-ZTT", "", 9, 0, 9);
  scales[0]->SetBinContent(1, unscaled[0]>0 ? (ZTT->Integral()/unscaled[0]-1.) : 0.);
  scales[1] = new TH1F("scales-ZMM"  , "", 9, 0, 9);
  scales[1]->SetBinContent(2, unscaled[1]>0 ? (ZMM  ->Integral()/unscaled[1]-1.) : 0.);
  scales[2] = new TH1F("scales-TTJ", "", 9, 0, 9);
  scales[2]->SetBinContent(3, unscaled[2]>0 ? (TTJ->Integral()/unscaled[2]-1.) : 0.);
  scales[3] = new TH1F("scales-QCD"  , "", 9, 0, 9);
  scales[3]->SetBinContent(4, unscaled[3]>0 ? (QCD  ->Integral()/unscaled[3]-1.) : 0.);
  scales[4] = new TH1F("scales-Dibosons", "", 9, 0, 9);
  scales[4]->SetBinContent(5, unscaled[4]>0 ? (Dibosons->Integral()/unscaled[4]-1.) : 0.);
  scales[5] = new TH1F("scales-WJets"  , "", 9, 0, 9);
  scales[5]->SetBinContent(6, unscaled[5]>0 ? (WJets  ->Integral()/unscaled[5]-1.) : 0.);
#ifdef MSSM
  scales[6] = new TH1F("scales-ggH"  , "", 9, 0, 9);
  scales[6]->SetBinContent(7, unscaled[6]>0 ? (ggH  ->Integral()/unscaled[4]-1.) : 0.);
  scales[7] = new TH1F("scales-bbH"  , "", 9, 0, 9);
  scales[7]->SetBinContent(8, unscaled[7]>0 ? (bbH  ->Integral()/unscaled[5]-1.) : 0.);
  scales[8] = new TH1F("scales-NONE" , "", 9, 0, 9);
  scales[8]->SetBinContent(9, 0.);
#else
#ifndef DROP_SIGNAL
  scales[6] = new TH1F("scales-ggH"  , "", 9, 0, 9);
  scales[6]->SetBinContent(7, unscaled[6]>0 ? (ggH  ->Integral()/unscaled[4]-1.) : 0.);
  scales[7] = new TH1F("scales-qqH"  , "", 9, 0, 9);
  scales[7]->SetBinContent(8, unscaled[7]>0 ? (qqH  ->Integral()/unscaled[5]-1.) : 0.);
  scales[8] = new TH1F("scales-VH"   , "", 9, 0, 9);
  scales[8]->SetBinContent(9, unscaled[8]>0 ? (VH   ->Integral()/unscaled[6]-1.) : 0.);
#endif
#endif

  ZMM->Add(ZTT);
  TTJ->Add(ZMM);
  QCD->Add(TTJ);
  Dibosons->Add(TTJ);
  WJets->Add(Dibosons);
  if(log){
#ifdef MSSM
    ggH  ->Add(bbH);
#else
#ifndef DROP_SIGNAL
    qqH  ->Add(VH );
    ggH  ->Add(qqH);
#endif
#endif
  }
  else{
#ifdef MSSM
    bbH  ->Add(WJets);
    ggH  ->Add(bbH);
#else
#ifndef DROP_SIGNAL
    VH   ->Add(WJets);
    qqH  ->Add(VH );
    ggH  ->Add(qqH);
#endif
#endif
  }

  float helper2=0;
  float helper;
  for(int ibin=0; ibin<WJets->GetNbinsX(); ibin++){
    helper=WJets->GetBinContent(ibin+1);
    if(helper>helper2) {helper2=helper;}
    }
  max=helper2*2;


  /*
    mass plot before and after fit
  */
  TCanvas* canv = MakeCanvas("canv", "histograms", 600, 600);
  canv->cd();
  if(log){ canv->SetLogy(1); }
#if defined MSSM
  data->GetXaxis()->SetRange(0, data->FindBin(1000));
#else
  data->GetXaxis()->SetRange(0, data->FindBin(350));
#endif
  data->SetNdivisions(505);
  data->SetMinimum(min);
  data->SetMaximum(max>0 ? max : std::max(maximum(data, log), maximum(WJets, log)));
  data->Draw("e");

  TH1F* errorBand = (TH1F*)WJets ->Clone();
  errorBand  ->SetMarkerSize(0);
  errorBand  ->SetFillColor(1);
  errorBand  ->SetFillStyle(3013);
  errorBand  ->SetLineWidth(1);

  if(log){
    WJets->Draw("histsame");
    //Dibosons->Draw("histsame");
    QCD->Draw("histsame");
    TTJ->Draw("histsame");
    ZMM->Draw("histsame");
    ZTT->Draw("histsame");
#ifndef DROP_SIGNAL
    ggH->Draw("histsame");
#endif
    $DRAW_ERROR
  }
  else{
#ifndef DROP_SIGNAL
    ggH  ->Draw("histsame");
#endif
    WJets->Draw("histsame");
    //Dibosons->Draw("histsame");
    QCD->Draw("histsame");
    TTJ->Draw("histsame");
    ZMM->Draw("histsame");
    ZTT->Draw("histsame");
    $DRAW_ERROR
  }
  data->Draw("esame");
  canv->RedrawAxis();

  CMSPrelim(dataset, "#tau_{#mu}#tau_{#mu}", 0.17, 0.835);
  

#ifdef MSSM  
  TLegend* leg = new TLegend(0.45, 0.65, 0.95, 0.90);
  SetLegendStyle(leg);
  leg->AddEntry(ggH  , "10#times#phi(160 GeV)#rightarrow#tau#tau tan#beta=8" , "L" );
#else
  TLegend* leg = new TLegend(0.50, 0.65, 0.95, 0.90);
  SetLegendStyle(leg);
#ifndef DROP_SIGNAL
  leg->AddEntry(ggH  , "H(125 GeV)#rightarrow#tau#tau" , "L" );
#endif
  //leg->AddEntry(ggH  , "5#timesH(125 GeV)#rightarrow#tau#tau" , "L" );
#endif
  leg->AddEntry(data , "observed"                    , "LP");
  leg->AddEntry(ZTT  , "Z#rightarrow#tau#tau"        , "F" );
  leg->AddEntry(ZMM  , "Z#rightarrow#mu#mu"          , "F" );
  leg->AddEntry(TTJ  , "t#bar{t}"                    , "F" );
  leg->AddEntry(QCD  , "QCD"                         , "F" );
  //leg->AddEntry(Dibosons  , "Dibosons"             , "F" );
  leg->AddEntry(WJets, "electroweak"                 , "F" );
  $ERROR_LEGEND
  leg->Draw();

//#ifdef MSSM
//  TPaveText* mssm  = new TPaveText(0.69, 0.85, 0.90, 0.90, "NDC");
//  mssm->SetBorderSize(   0 );
//  mssm->SetFillStyle(    0 );
//  mssm->SetTextAlign(   12 );
//  mssm->SetTextSize ( 0.03 );
//  mssm->SetTextColor(    1 );
//  mssm->SetTextFont (   62 );
//  mssm->AddText("(m_{A}=120, tan#beta=10)");
//  mssm->Draw();
//#else
//  TPaveText* mssm  = new TPaveText(0.83, 0.85, 0.95, 0.90, "NDC");
//  mssm->SetBorderSize(   0 );
//  mssm->SetFillStyle(    0 );
//  mssm->SetTextAlign(   12 );
//  mssm->SetTextSize ( 0.03 );
//  mssm->SetTextColor(    1 );
//  mssm->SetTextFont (   62 );
//  mssm->AddText("m_{H}=125");
//  mssm->Draw();
//#endif

  /*
    Ratio Data over MC
  */
  TCanvas *canv0 = MakeCanvas("canv0", "histograms", 600, 400);
  canv0->SetGridx();
  canv0->SetGridy();
  canv0->cd();

  TH1F* zero = (TH1F*)ref ->Clone("zero"); zero->Clear();
  TH1F* rat1 = (TH1F*)data->Clone("rat"); 
  rat1->Divide(WJets);
  for(int ibin=0; ibin<rat1->GetNbinsX(); ++ibin){
    if(rat1->GetBinContent(ibin+1)>0){
      // catch cases of 0 bins, which would lead to 0-alpha*0-1
      rat1->SetBinContent(ibin+1, rat1->GetBinContent(ibin+1)-1.);
    }
    zero->SetBinContent(ibin+1, 0.);
  }
  rat1->SetLineColor(kBlack);
  rat1->SetFillColor(kGray );
  rat1->SetMaximum(+1.5);
  rat1->SetMinimum(-1.5);
  rat1->GetYaxis()->CenterTitle();
  rat1->GetYaxis()->SetTitle("#bf{Data/MC-1}");
  rat1->GetXaxis()->SetTitle("#bf{m_{#tau#tau} [GeV]}"); 
  rat1->Draw();
  zero->SetLineColor(kBlack);
  zero->Draw("same");
  canv0->RedrawAxis();

  /*
    Ratio After fit over Prefit
  */
  TCanvas *canv1 = MakeCanvas("canv1", "histograms", 600, 400);
  canv1->SetGridx();
  canv1->SetGridy();
  canv1->cd();

  TH1F* rat2 = (TH1F*) WJets->Clone("rat2");
  rat2->Divide(ref);
  for(int ibin=0; ibin<rat2->GetNbinsX(); ++ibin){
    if(rat2->GetBinContent(ibin+1)>0){
      // catch cases of 0 bins, which would lead to 0-alpha*0-1
      rat2 ->SetBinContent(ibin+1, rat2->GetBinContent(ibin+1)-1.);
    }
  }
  rat2->SetLineColor(kRed+ 3);
  rat2->SetFillColor(kRed-10);
  rat2->SetMaximum(+0.3);
  rat2->SetMinimum(-0.3);
  rat2->GetYaxis()->SetTitle("#bf{Fit/Prefit-1}");
  rat2->GetYaxis()->CenterTitle();
  rat2->GetXaxis()->SetTitle("#bf{m_{#tau#tau} [GeV]}");
  rat2->GetXaxis()->SetRange(0, 28);
  rat2->Draw();
  zero->SetLineColor(kBlack);
  zero->Draw("same");
  canv1->RedrawAxis();
  /*
    Relative shift per sample
  */
  TCanvas *canv2 = MakeCanvas("canv2", "histograms", 600, 400);
  canv2->SetGridx();
  canv2->SetGridy();
  canv2->cd();

  InitHist  (scales[0], "", "", kGreen  - 4, 1001);
  InitHist  (scales[1], "", "", kYellow - 4, 1001);
  InitHist  (scales[2], "", "", kMagenta-10, 1001);
  InitHist  (scales[3], "", "", kRed    + 2, 1001);
  InitHist  (scales[4], "", "", kBlue   - 8, 1001);
  InitHist  (scales[5], "", "", kOrange - 4, 1001);  
#ifndef DROP_SIGNAL
  InitSignal(scales[6]);
  InitSignal(scales[7]);
  InitSignal(scales[8]);
#endif
  scales[0]->Draw();
  scales[0]->GetXaxis()->SetBinLabel(1, "#bf{ZTT}");
  scales[0]->GetXaxis()->SetBinLabel(2, "#bf{ZMM}"  );
  scales[0]->GetXaxis()->SetBinLabel(3, "#bf{TTJ}");
  scales[0]->GetXaxis()->SetBinLabel(4, "#bf{QCD}"  );
  scales[0]->GetXaxis()->SetBinLabel(5, "#bf{Dibosons}");
  scales[0]->GetXaxis()->SetBinLabel(6, "#bf{WJets}"  );
#ifdef MSSM
  scales[0]->GetXaxis()->SetBinLabel(7, "#bf{ggH}"  );
  scales[0]->GetXaxis()->SetBinLabel(8, "#bf{bbH}"  );
  scales[0]->GetXaxis()->SetBinLabel(9, "#bf{NONE}" );
#else
  scales[0]->GetXaxis()->SetBinLabel(7, "#bf{ggH}"  );
  scales[0]->GetXaxis()->SetBinLabel(8, "#bf{qqH}"  );
  scales[0]->GetXaxis()->SetBinLabel(9, "#bf{VH}"   );
#endif
  scales[0]->SetMaximum(+1.5);
  scales[0]->SetMinimum(-1.5);
  scales[0]->GetYaxis()->CenterTitle();
  scales[0]->GetYaxis()->SetTitle("#bf{Fit/Prefit-1}");
  scales[1]->Draw("same");
  scales[2]->Draw("same");
  scales[3]->Draw("same");
  scales[4]->Draw("same");
  scales[5]->Draw("same");
#ifndef DROP_SIGNAL
  scales[6]->Draw("same");
  scales[7]->Draw("same");
  scales[8]->Draw("same");
#endif
  zero->Draw("same");
  canv2->RedrawAxis();

  /*
    prepare output
  */
 bool isSevenTeV = std::string(inputfile).find("7TeV")!=std::string::npos;
  canv ->Print(TString::Format("%s_%sscaled_%s_%s.png"       , directory, scaled ? "re" : "un", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "")); 
  canv ->Print(TString::Format("%s_%sscaled_%s_%s.pdf"       , directory, scaled ? "re" : "un", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "")); 
  canv ->Print(TString::Format("%s_%sscaled_%s_%s.eps"       , directory, scaled ? "re" : "un", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "")); 
  canv0->Print(TString::Format("%s_datamc_%sscaled_%s_%s.png", directory, scaled ? "re" : "un", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "")); 
  canv0->Print(TString::Format("%s_datamc_%sscaled_%s_%s.pdf", directory, scaled ? "re" : "un", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : ""));
  canv0->Print(TString::Format("%s_datamc_%sscaled_%s_%s.eps", directory, scaled ? "re" : "un", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : ""));
  canv1->Print(TString::Format("%s_prefit_%sscaled_%s_%s.png", directory, scaled ? "re" : "un", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "")); 
  canv1->Print(TString::Format("%s_prefit_%sscaled_%s_%s.pdf", directory, scaled ? "re" : "un", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : ""));
  canv1->Print(TString::Format("%s_prefit_%sscaled_%s_%s.eps", directory, scaled ? "re" : "un", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : ""));
  canv2->Print(TString::Format("%s_sample_%sscaled_%s_%s.png", directory, scaled ? "re" : "un", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "")); 
  canv2->Print(TString::Format("%s_sample_%sscaled_%s_%s.pdf", directory, scaled ? "re" : "un", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : ""));
  canv2->Print(TString::Format("%s_sample_%sscaled_%s_%s.eps", directory, scaled ? "re" : "un", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : ""));

  TFile* output = new TFile(TString::Format("%s_%sscaled_%s_%s.root", directory, scaled ? "re" : "un", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : ""), "update");
  output->cd();
  data ->Write("data_obs");
  ZTT->Write("Ztt"   );
  ZMM->Write("Zmm"     );
  TTJ->Write("ttbar"   );
  QCD->Write("Fakes"     );
  Dibosons->Write("Dibosons"   );
  WJets->Write("EWK"     );
#ifdef MSSM
  ggH  ->Write("ggH"     );
  bbH  ->Write("bbH"     );
#else
#ifndef DROP_SIGNAL
  ggH  ->Write("ggH"     );
  qqH  ->Write("qqH"     );
  VH   ->Write("VH"      );
#endif
#endif
  if(errorBand){
    errorBand->Write("errorBand");
  }
  output->Close();
}
