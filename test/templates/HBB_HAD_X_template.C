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
#include "$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"

$DEFINE_ASIMOV
$DEFINE_DROP_SIGNAL
$DEFINE_MSSM

/**
   \class   HTT_EM_X_template HTT_EM_X_template.C "HiggsAnalysis/HiggsToTauTau/postfit/tamplates/HTT_EM_X_template.C"

   \brief   macro template to create pre-/postfit plots of the inputs to the limit calculation

   This is a macro template to create pre-/postfit plots of the inputs tp the limit calculation.
   This macro is picked up from the produce_macros.py script in the HiggsAnalysis/HiggsToTauTau/postfit
   directory. The key words in the replace(...) function are replaced by proper values that have
   been calculated from the uncertainties as picked up from the datacards in the postfit/datacards 
   directory of the package and the pulls of the fit as picked up from the maximum likelihood fit 
   results file in the postfit/fitresults directory of the package.


   In the headline of the main macro the keywords HTT_EM_X, $HISTFILE and $CATEGORY will be 
   replaced by proper names according to the inputfile and event category, for which the polts 
   are supposed to be made.
*/

static const bool BLIND_DATA = $BLIND; //false;
static const bool FULLPLOTS = false; //true;
float blinding_MSSM(float mass){ return (100<mass); }
float maximum(TH1F* h, bool LOG=false){
  if(LOG){
    if(h->GetMaximum()>1000){ return 10000.*TMath::Nint(500*h->GetMaximum()/1000.); }
    if(h->GetMaximum()>  10){ return   100.*TMath::Nint( 50*h->GetMaximum()/  10.); }
    return 500*h->GetMaximum(); 
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
  case 1: // Bbb 
  $Bbb
  case 2: // Cbb
  $Cbb
  case 3: // Qbb
  $Qbb
  case 4: // bbB
  $bbB
  case 5: // bbX
  $bbX  
#if defined MSSM
  case 6: // bbH
  ${MSSM}bbH$MA
#endif
  default :
    std::cout << "error histograms not known?!?" << std::endl;
  }
}

void 
HBB_HAD_X(bool scaled=true, bool log=true, float min=0.1, float max=-1., string inputfile="root/$HISTFILE", const char* directory="bb_$CATEGORY")
{
  // define common canvas, axes pad styles
  SetStyle(); gStyle->SetLineStyleString(11,"20 10");
  const char* category_extra = "";
  if(std::string(directory) == std::string("bb_had0"  )){ category_extra = "all-had_{0}";  }
  if(std::string(directory) == std::string("bb_had1"  )){ category_extra = "all-had_{1}";  }
  if(std::string(directory) == std::string("bb_had2"  )){ category_extra = "all-had_{2}";  }
  if(std::string(directory) == std::string("bb_had3"  )){ category_extra = "all-had_{3}";  }
  if(std::string(directory) == std::string("bb_had4"  )){ category_extra = "all-had_{4}";  }
  if(std::string(directory) == std::string("bb_had5"  )){ category_extra = "all-had_{5}";  }
  if(std::string(directory) == std::string("bb_lep"   )){ category_extra = "semi-lep";  }

  const char* dataset;
  if(std::string(inputfile).find("7TeV")!=std::string::npos){dataset = "Preliminary, #sqrt{s} = 7 TeV, L = 2.7 fb^{-1}";}
  if(std::string(inputfile).find("8TeV")!=std::string::npos){dataset = "Preliminary, #sqrt{s} = 8 TeV, L = 19.4 fb^{-1}";}
  
  TFile* input = new TFile(inputfile.c_str());
#ifdef MSSM
  TFile* input2 = new TFile((inputfile+"_$MA_$TANB").c_str());
#endif
  TH1F* Bbb  = refill((TH1F*)input->Get(TString::Format("%s/Bbb"   , directory)), "Bbb"); InitHist(Bbb, "", "", kMagenta-10, 1001);
  TH1F* Cbb  = refill((TH1F*)input->Get(TString::Format("%s/Cbb"   , directory)), "Cbb"); InitHist(Cbb, "", "", kRed    + 2, 1001);
  TH1F* Qbb  = refill((TH1F*)input->Get(TString::Format("%s/Qbb"   , directory)), "Qbb"); InitHist(Qbb, "", "", kBlue   - 8, 1001);
  TH1F* bbB  = refill((TH1F*)input->Get(TString::Format("%s/bbB"   , directory)), "bbB"); InitHist(bbB, "", "", kOrange - 4, 1001);
  TH1F* bbX  = refill((TH1F*)input->Get(TString::Format("%s/bbX"   , directory)), "bbX"); InitHist(bbX, "", "", kViolet - 0, 1001);
#ifdef MSSM
  //float bbHScale = 1.;
  //ggHScale = ($MSSM_SIGNAL_ggH_xseff_A + $MSSM_SIGNAL_ggH_xseff_hH);
  //bbHScale = ($MSSM_SIGNAL_bbH_xseff_A + $MSSM_SIGNAL_bbH_xseff_hH);
  TH1F* bbH  = refill((TH1F*)input2->Get(TString::Format("%s/bbH$MA"  , directory)), "bbH"  ); InitSignal(bbH); bbH->Scale($TANB); //bbH->Scale(bbHScale);
#endif
#ifdef ASIMOV
  TH1F* data   = refill((TH1F*)input->Get(TString::Format("%s/data_obs_asimov", directory)), "data", true);
#else
  TH1F* data   = refill((TH1F*)input->Get(TString::Format("%s/data_obs", directory)), "data", true);
#endif
  InitHist(data, "#bf{m_{b#bar{b}} [GeV]}", "#bf{dN/dm_{b#bar{b}} [1/GeV]}"); InitData(data);

  TH1F* ref=(TH1F*)Qbb->Clone("ref");
  ref->Add(bbX);
  ref->Add(Cbb);
  ref->Add(bbB);
  ref->Add(Bbb);

  double unscaled[7];
  unscaled[0] = Qbb ->Integral();
  unscaled[1] = bbX ->Integral();
  unscaled[2] = Cbb ->Integral();
  unscaled[3] = bbB ->Integral();
  unscaled[4] = Bbb ->Integral();
#ifdef MSSM
  unscaled[5] = bbH ->Integral();
  unscaled[6] = 0;
#endif

  if(scaled){
    rescale(Bbb,   1); 
    rescale(bbB,   4); 
    rescale(Cbb,   2); 
    rescale(bbX,   5);
    rescale(Qbb,   3);
#ifdef MSSM 
    rescale(bbH,   6);
#endif
  }

  TH1F* scales[7];
  scales[0] = new TH1F("scales-Qbb", "", 7, 0, 7);
  scales[0]->SetBinContent(1, unscaled[0]>0 ? (Qbb  ->Integral()/unscaled[0]-1.) : 0.);
  scales[1] = new TH1F("scales-bbX"  , "", 7, 0, 7);
  scales[1]->SetBinContent(2, unscaled[1]>0 ? (bbX  ->Integral()/unscaled[1]-1.) : 0.);
  scales[2] = new TH1F("scales-Cbb", "", 7, 0, 7);
  scales[2]->SetBinContent(3, unscaled[2]>0 ? (Cbb  ->Integral()/unscaled[2]-1.) : 0.);
  scales[3] = new TH1F("scales-bbB"  , "", 7, 0, 7);
  scales[3]->SetBinContent(4, unscaled[3]>0 ? (bbB  ->Integral()/unscaled[3]-1.) : 0.);
  scales[4] = new TH1F("scales-Bbb"  , "", 7, 0, 7);
  scales[4]->SetBinContent(5, unscaled[4]>0 ? (Bbb  ->Integral()/unscaled[4]-1.) : 0.);
#ifdef MSSM
  scales[5] = new TH1F("scales-bbH"  , "", 7, 0, 7);
  scales[5]->SetBinContent(6, unscaled[5]>0 ? (bbH  ->Integral()/unscaled[5]-1.) : 0.);
  scales[6] = new TH1F("scales-NONE" , "", 7, 0, 7);
  scales[6]->SetBinContent(7, 0.);
#endif

  bbX  ->Add(Qbb);
  Cbb  ->Add(bbX);
  bbB  ->Add(Cbb);
  Bbb  ->Add(bbB);
  if(!log){
#ifdef MSSM
    bbH  ->Add(Bbb);
#endif
  }

  /*
    mass plot before and after fit
  */
  TCanvas* canv = MakeCanvas("canv", "histograms", 600, 600);
  canv->cd();
  if(log){ canv->SetLogy(1); }
#if defined MSSM
  if(!log){ data->GetXaxis()->SetRange(0, data->FindBin(350)); } else{ data->GetXaxis()->SetRange(0, data->FindBin(1000)); };
#endif

  data->SetNdivisions(505);
  data->SetMinimum(min);
  data->SetMaximum(max>0 ? max : std::max(maximum(data, log), maximum(Bbb, log)));
  data->Draw("e");

  TH1F* errorBand = (TH1F*)Bbb ->Clone();
  errorBand  ->SetMarkerSize(0);
  errorBand  ->SetFillColor(1);
  errorBand  ->SetFillStyle(3013);
  errorBand  ->SetLineWidth(1);

  if(log){
    Bbb  ->Draw("histsame");
    bbB  ->Draw("histsame");
    Cbb  ->Draw("histsame");
    bbX  ->Draw("histsame");
    Qbb  ->Draw("histsame");
    $DRAW_ERROR
#ifndef DROP_SIGNAL
    bbH  ->Draw("histsame");
#endif
  }
  else{   
#ifndef DROP_SIGNAL
    bbH  ->Draw("histsame");
#endif 
    Bbb  ->Draw("histsame");
    bbB  ->Draw("histsame");
    Cbb  ->Draw("histsame");
    bbX  ->Draw("histsame");
    Qbb  ->Draw("histsame");
    $DRAW_ERROR
  }
  data->Draw("esame");
  canv->RedrawAxis();

  //CMSPrelim(dataset, "b#bar{b}", 0.17, 0.835);
  CMSPrelim(dataset, "", 0.17, 0.835);  
  TPaveText* chan     = new TPaveText(0.20, 0.74+0.061, 0.32, 0.74+0.161, "NDC");
  chan->SetBorderSize(   0 );
  chan->SetFillStyle(    0 );
  chan->SetTextAlign(   12 );
  chan->SetTextSize ( 0.05 );
  chan->SetTextColor(    1 );
  chan->SetTextFont (   62 );
  chan->AddText("b#bar{b}");
  chan->Draw();

  TPaveText* cat      = new TPaveText(0.20, 0.68+0.061, 0.32, 0.68+0.161, "NDC");
  cat->SetBorderSize(   0 );
  cat->SetFillStyle(    0 );
  cat->SetTextAlign(   12 );
  cat->SetTextSize ( 0.05 );
  cat->SetTextColor(    1 );
  cat->SetTextFont (   62 );
  cat->AddText(category_extra);
  cat->Draw();

#ifdef MSSM
  TPaveText* massA      = new TPaveText(0.75, 0.48+0.061, 0.85, 0.48+0.161, "NDC");
  massA->SetBorderSize(   0 );
  massA->SetFillStyle(    0 );
  massA->SetTextAlign(   12 );
  massA->SetTextSize ( 0.03 );
  massA->SetTextColor(    1 );
  massA->SetTextFont (   62 );
  massA->AddText("m_{A}=$MA GeV");
  massA->Draw();

  TPaveText* tanb      = new TPaveText(0.75, 0.44+0.061, 0.85, 0.44+0.161, "NDC");
  tanb->SetBorderSize(   0 );
  tanb->SetFillStyle(    0 );
  tanb->SetTextAlign(   12 );
  tanb->SetTextSize ( 0.03 );
  tanb->SetTextColor(    1 );
  tanb->SetTextFont (   62 );
  tanb->AddText("tan#beta=$TANB");
  tanb->Draw();

  TPaveText* scen      = new TPaveText(0.75, 0.40+0.061, 0.85, 0.40+0.161, "NDC");
  scen->SetBorderSize(   0 );
  scen->SetFillStyle(    0 );
  scen->SetTextAlign(   12 );
  scen->SetTextSize ( 0.03 );
  scen->SetTextColor(    1 );
  scen->SetTextFont (   62 );
  scen->AddText("m^{h}_{max}");
  scen->Draw();
#endif

#ifdef MSSM  
  TLegend* leg = new TLegend(0.55, 0.65, 0.95, 0.90);
  SetLegendStyle(leg);
  leg->AddEntry(bbH  , "#phi#rightarrowb#bar{b}" , "L" );
#endif
#ifdef ASIMOV
  leg->AddEntry(data , "sum(bkg) + SM125 GeV signal"    , "LP");
#else
  leg->AddEntry(data , "observed"                       , "LP");
#endif
  leg->AddEntry(Bbb, "Bbb"                            , "F" );
  leg->AddEntry(bbB, "bbB"                            , "F" );
  leg->AddEntry(Cbb, "Cbb"                            , "F" );
  leg->AddEntry(bbX, "bbX"                            , "F" );
  leg->AddEntry(Qbb, "Qbb"                            , "F" );
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
//  mssm->AddText("(m_{A}=250, tan#beta=5)");
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
  rat1->Divide(Bbb);
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
  rat1->GetXaxis()->SetTitle("#bf{m_{b#bar{b}} [GeV]}");
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

  TH1F* rat2 = (TH1F*) Bbb->Clone("rat2");
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
  rat2->GetXaxis()->SetTitle("#bf{m_{b#bar{b}} [GeV]}");
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

  InitHist  (scales[4], "", "", kMagenta-10, 1001);
  InitHist  (scales[2], "", "", kRed    + 2, 1001);
  InitHist  (scales[0], "", "", kBlue   - 8, 1001);
  InitHist  (scales[3], "", "", kOrange - 4, 1001);
  InitHist  (scales[1], "", "", kViolet - 0, 1001);
  scales[0]->Draw();
  scales[0]->GetXaxis()->SetBinLabel(1, "#bf{Qbb}");
  scales[0]->GetXaxis()->SetBinLabel(2, "#bf{bbX}");
  scales[0]->GetXaxis()->SetBinLabel(3, "#bf{Cbb}");
  scales[0]->GetXaxis()->SetBinLabel(4, "#bf{bbB}");
  scales[0]->GetXaxis()->SetBinLabel(5, "#bf{Bbb}");
#ifdef MSSM
  scales[0]->GetXaxis()->SetBinLabel(6, "#bf{bbH}"  );
  scales[0]->GetXaxis()->SetBinLabel(7, "#bf{NONE}" );
#endif
  scales[0]->SetMaximum(+1.0);
  scales[0]->SetMinimum(-1.0);
  scales[0]->GetYaxis()->CenterTitle();
  scales[0]->GetYaxis()->SetTitle("#bf{Fit/Prefit-1}");
  scales[1]->Draw("same");
  scales[2]->Draw("same");
  scales[3]->Draw("same");
  scales[4]->Draw("same");
  zero->Draw("same");
  canv2->RedrawAxis();

  /*
    prepare output
  */
  bool isSevenTeV = std::string(inputfile).find("7TeV")!=std::string::npos;
  canv ->Print(TString::Format("%s_%sfit_%s_%s.png"       , directory, scaled ? "post" : "pre", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "LIN")); 
  canv ->Print(TString::Format("%s_%sfit_%s_%s.pdf"       , directory, scaled ? "post" : "pre", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "LIN")); 
  canv ->Print(TString::Format("%s_%sfit_%s_%s.eps"       , directory, scaled ? "post" : "pre", isSevenTeV ? "7TeV" : "8TeV", log ? "LOG" : "LIN")); 
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
  Qbb  ->Write("Qbb"     );
  bbX  ->Write("bbX"     );
  Cbb  ->Write("Cbb"     );
  bbB  ->Write("bbB"     );
  Bbb  ->Write("Bbb"     );
#ifdef MSSM
  bbH  ->Write("bbH"     );
#endif
  if(errorBand){
    errorBand->Write("errorBand");
  }
  output->Close();
}
