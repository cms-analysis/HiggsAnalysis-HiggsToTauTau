#include <iostream>

#include <TH1F.h>
#include <TFile.h>
#include <TROOT.h>
#include <TString.h>
#include <TSystem.h>
#include <Rtypes.h>

#include <TAxis.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TAttLine.h>
#include <TPaveText.h>

#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"

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


TH1F* refill(TH1F* hin, bool data=false)
/*
  refill histograms, divide by bin width and correct bin errors. For MC histograms set 
  bin errors to zero.
*/
{
  TH1F* hout = (TH1F*)hin->Clone(); hout->Clear();
  for(int i=0; i<hout->GetNbinsX(); ++i){
    hout->SetBinContent(i+1, hin->GetBinContent(i+1)/hin->GetBinWidth(i+1));
    if(data){
      hout->SetBinError(i+1, hout->GetBinError(i+1)/hout->GetBinWidth(i+1));
    }
    else{
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
  case 1: // Ztt 
  $Ztt
  case 2: // ttbar
  $ttbar
  case 3: // EWK
  $EWK
  case 4: // Fakes
  $Fakes
  case 5: // ggH
  $ggH125
  case 6: // qqH
  $qqH125
  case 7: // VH
  $VH125
  default :
    std::cout << "error histograms not known?!?" << std::endl;
  }
}

void 
HTT_EM_X(const char* inputfile="root/$HISTFILE", const char* directory="emu_$CATEGORY", bool scaled = true, bool log = true, float max=500., float min=0.05)
{
  // define common canvas, axes pad styles
  SetStyle(); gStyle->SetLineStyleString(11,"20 10");

  const char* dataset;
  if(std::string(inputfile).find("7tev")!=std::string::npos){dataset = "#sqrt{s} = 7 TeV, L = 4.9 fb^{-1}";}
  if(std::string(inputfile).find("8tev")!=std::string::npos){dataset = "#sqrt{s} = 8 TeV, L = 3.0 fb^{-1}";}
  
  TFile* input = new TFile(inputfile);
  TH1F* Fakes  = refill((TH1F*)input->Get(TString::Format("%s/Fakes"   , directory))); InitHist(Fakes, "", "", kMagenta-10, 1001);
  TH1F* EWK    = refill((TH1F*)input->Get(TString::Format("%s/EWK"     , directory))); InitHist(EWK  , "", "", kRed    + 2, 1001);
  TH1F* ttbar  = refill((TH1F*)input->Get(TString::Format("%s/ttbar"   , directory))); InitHist(ttbar, "", "", kBlue   - 8, 1001);
  TH1F* Ztt    = refill((TH1F*)input->Get(TString::Format("%s/Ztt"     , directory))); InitHist(Ztt  , "", "", kOrange - 4, 1001);
  TH1F* ggH    = refill((TH1F*)input->Get(TString::Format("%s/ggH125"  , directory))); InitSignal(ggH); ggH->Scale(5);
  TH1F* qqH    = refill((TH1F*)input->Get(TString::Format("%s/qqH125"  , directory))); InitSignal(qqH); qqH->Scale(5);
  TH1F* VH     = refill((TH1F*)input->Get(TString::Format("%s/VH125"   , directory))); InitSignal(VH ); VH ->Scale(5);
  TH1F* data   = refill((TH1F*)input->Get(TString::Format("%s/data_obs", directory)), true);
  InitHist(data, "#bf{m_{#tau#tau} [GeV]}", "#bf{dN/dm_{#tau#tau} [1/GeV]}"); InitData(data);

  TH1F* ref=(TH1F*)Fakes->Clone("ref");
  ref->Add(EWK  );
  ref->Add(ttbar);
  ref->Add(Ztt  );

  double unscaled[7];
  unscaled[0] = Fakes->Integral();
  unscaled[1] = EWK  ->Integral();
  unscaled[2] = ttbar->Integral();
  unscaled[3] = Ztt  ->Integral();
  unscaled[4] = ggH  ->Integral();
  unscaled[5] = qqH  ->Integral();
  unscaled[6] = VH   ->Integral();
  
  if(scaled){
    rescale(Fakes, 4); 
    rescale(EWK,   3); 
    rescale(ttbar, 2); 
    rescale(Ztt,   1); 
    rescale(ggH,   5);
    rescale(qqH,   6);
    rescale(qqH,   7);
  }

  TH1F* scales[7];
  scales[0] = new TH1F("scales-Fakes", "", 7, 0, 7);
  scales[0]->SetBinContent(1, Fakes->Integral()/unscaled[0]-1.);
  scales[1] = new TH1F("scales-EWK"  , "", 7, 0, 7);
  scales[1]->SetBinContent(2, EWK  ->Integral()/unscaled[1]-1.);
  scales[2] = new TH1F("scales-ttbar", "", 7, 0, 7);
  scales[2]->SetBinContent(3, ttbar->Integral()/unscaled[2]-1.);
  scales[3] = new TH1F("scales-Ztt"  , "", 7, 0, 7);
  scales[3]->SetBinContent(4, Ztt  ->Integral()/unscaled[3]-1.);
  scales[4] = new TH1F("scales-ggH"  , "", 7, 0, 7);
  scales[4]->SetBinContent(5, ggH  ->Integral()/unscaled[4]-1.);
  scales[5] = new TH1F("scales-qqH"  , "", 7, 0, 7);
  scales[5]->SetBinContent(6, qqH  ->Integral()/unscaled[5]-1.);
  scales[6] = new TH1F("scales-VH"   , "", 7, 0, 7);
  scales[6]->SetBinContent(7, VH   ->Integral()/unscaled[6]-1.);

  EWK  ->Add(Fakes);
  ttbar->Add(EWK  );
  Ztt  ->Add(ttbar);
  if(log){
    qqH  ->Add(VH );
    ggH  ->Add(qqH);
  }
  else{
    VH   ->Add(Ztt);
    qqH  ->Add(VH );
    ggH  ->Add(qqH);
  }

  /*
    mass plot before and after fit
  */
  TCanvas* canv = MakeCanvas("canv", "histograms", 600, 600);
  canv->cd();
  if(log){ canv->SetLogy(1); }
  // reduce the axis range if necessary
  //data->GetXaxis()->SetRange(0, 28);
  data->SetNdivisions(505);
  data->SetMinimum(min);
  data->SetMaximum(max);
  data->Draw("e");

  if(log){
    Ztt  ->Draw("same");
    ttbar->Draw("same");
    EWK  ->Draw("same");
    Fakes->Draw("same");
    ggH  ->Draw("same");
  }
  else{
    ggH  ->Draw("same");
    Ztt  ->Draw("same");
    ttbar->Draw("same");
    EWK  ->Draw("same");
    Fakes->Draw("same");
  }
  data->Draw("esame");
  canv->RedrawAxis();

  CMSPrelim(dataset, "#tau_{e}#tau_{#mu}", 0.17, 0.835);
  
  TLegend* leg = new TLegend(0.57, 0.65, 0.95, 0.90);
  SetLegendStyle(leg);
  leg->AddEntry(ggH  , "(5#times) H#rightarrow#tau#tau" , "L" );
  leg->AddEntry(data , "observed"                       , "LP");
  leg->AddEntry(Ztt  , "Z#rightarrow#tau#tau"           , "F" );
  leg->AddEntry(ttbar, "t#bar{t}"                       , "F" );
  leg->AddEntry(EWK  , "electroweak"                    , "F" );
  leg->AddEntry(Fakes, "QCD"                            , "F" );
  leg->Draw();

  TPaveText* mssm  = new TPaveText(0.83, 0.85, 0.95, 0.90, "NDC");
  mssm->SetBorderSize(   0 );
  mssm->SetFillStyle(    0 );
  mssm->SetTextAlign(   12 );
  mssm->SetTextSize ( 0.03 );
  mssm->SetTextColor(    1 );
  mssm->SetTextFont (   62 );
  mssm->AddText("m_{H}=125");
  mssm->Draw();

  /*
    Ratio Data over MC
  */
  TCanvas *canv0 = MakeCanvas("canv0", "histograms", 600, 400);
  canv0->SetGridx();
  canv0->SetGridy();
  canv0->cd();

  TH1F* zero = (TH1F*)ref ->Clone("zero"); zero->Clear();
  TH1F* rat1 = (TH1F*)data->Clone("rat1"); 
  rat1->Divide(Ztt);
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

  TH1F* rat2 = (TH1F*) Ztt->Clone("rat2");
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

  InitHist  (scales[0], "", "", kMagenta-10, 1001);
  InitHist  (scales[1], "", "", kRed    + 2, 1001);
  InitHist  (scales[2], "", "", kBlue   - 8, 1001);
  InitHist  (scales[3], "", "", kOrange - 4, 1001);
  InitSignal(scales[4]);
  InitSignal(scales[5]);
  InitSignal(scales[6]);

  scales[0]->Draw();
  scales[0]->GetXaxis()->SetBinLabel(1, "#bf{Fakes}");
  scales[0]->GetXaxis()->SetBinLabel(2, "#bf{EWK}"  );
  scales[0]->GetXaxis()->SetBinLabel(3, "#bf{ttbar}");
  scales[0]->GetXaxis()->SetBinLabel(4, "#bf{Ztt}"  );
  scales[0]->GetXaxis()->SetBinLabel(5, "#bf{ggH}"  );
  scales[0]->GetXaxis()->SetBinLabel(6, "#bf{qqH}"  );
  scales[0]->GetXaxis()->SetBinLabel(7, "#bf{VH}"   );
  scales[0]->SetMaximum(+1.0);
  scales[0]->SetMinimum(-1.0);
  scales[0]->GetYaxis()->CenterTitle();
  scales[0]->GetYaxis()->SetTitle("#bf{Fit/Prefit-1}");
  scales[0]->GetXaxis()->SetTitle("#bf{m_{#tau#tau} [GeV]}");
  scales[1]->Draw("same");
  scales[2]->Draw("same");
  scales[3]->Draw("same");
  scales[4]->Draw("same");
  scales[5]->Draw("same");
  scales[6]->Draw("same");
  zero->Draw("same");
  canv2->RedrawAxis();

  /*
    prepare output
  */
  canv ->Print(TString::Format("%s_%sscaled_%s.pdf"       , directory, scaled ? "re" : "un", log ? "LOG" : "")); 
  canv0->Print(TString::Format("%s_datamc_%sscaled_%s.png", directory, scaled ? "re" : "un", log ? "LOG" : "")); 
  canv0->Print(TString::Format("%s_datamc_%sscaled_%s.pdf", directory, scaled ? "re" : "un", log ? "LOG" : ""));
  canv1->Print(TString::Format("%s_prefit_%sscaled_%s.png", directory, scaled ? "re" : "un", log ? "LOG" : "")); 
  canv1->Print(TString::Format("%s_prefit_%sscaled_%s.pdf", directory, scaled ? "re" : "un", log ? "LOG" : ""));
  canv2->Print(TString::Format("%s_sample_%sscaled_%s.png", directory, scaled ? "re" : "un", log ? "LOG" : "")); 
  canv2->Print(TString::Format("%s_sample_%sscaled_%s.pdf", directory, scaled ? "re" : "un", log ? "LOG" : ""));
  TFile* output = new TFile(TString::Format("%s_%sscaled_%s.root", directory, scaled ? "re" : "un", log ? "LOG" : ""), "update");
  output->cd();
  data ->Write("data_obs");
  Fakes->Write("Fakes"   );
  EWK  ->Write("EWK"     );
  ttbar->Write("ttbar"   );
  Ztt  ->Write("Ztt"     );
  ggH  ->Write("ggH"     );
  qqH  ->Write("qqH"     );
  output->Close();
}
