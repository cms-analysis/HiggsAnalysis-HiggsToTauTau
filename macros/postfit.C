#include <iostream>
#include <algorithm>

#include <TH1F.h>
#include <TFile.h>
#include <TMath.h>
#include <TROOT.h>
#include <TString.h>
#include <TSystem.h>
#include <Rtypes.h>

#include <TAxis.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TAttLine.h>
#include <TPaveText.h>
#include <TColor.h>

#include "$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"
#include "$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"

static const float SIGNAL_SCALE = 1.;
/**
   \class   postfit postfit.C "HiggsAnalysis/HiggsToTauTau/macros/postfit.C"

   \brief   macro to make plots for di-tau masses for all classic htt channels

   This is a macro to create di-tau masses for all classic htt channels combined
*/

static const bool HWWBG = $HWWBG;
static const bool CONSERVATIVE_CHI2 = false;
static const float UPPER_EDGE = 1495; // 695; 1495;

float maximum(TH1F* h, bool LOG=false){
  if(LOG){
    return 5.*h->GetMaximum();
  }
  else{
    if(h->GetMaximum()>  12){ return 10.*TMath::Nint((1.35*h->GetMaximum()/10.)); }
    if(h->GetMaximum()> 1.2){ return TMath::Nint((1.65*h->GetMaximum())); }
    return 1.6*h->GetMaximum(); 
  }
}

TH1F* refill(TH1F* hin, const char* sample)
/*
  refill histograms, for MC histograms set bin errors to zero.
*/
{
  if(hin==0){
    std::cout << "hist not found: " << sample << " -- this may happen for samples of type signal." << std::endl;
    bool skip = false;
    if(std::string(sample).find("ggH")==std::string::npos       ){ skip == true; }
    if(std::string(sample).find("Zmm")==std::string::npos       ){ skip == true; }
    if(std::string(sample).find("Zee")==std::string::npos       ){ skip == true; }
    if(std::string(sample).find("Fakes/QCD")==std::string::npos ){ skip == true; }
    if(skip){
      std::cout << "hist is not of type signal, Fakes/QCD or Zmm in mumu, Zee in ee, close here" << std::endl;
      exit(1);
    }
    else{
      return hin;
    }
  }
  TH1F* hout = (TH1F*)hin->Clone(); hout->Clear();
  for(int i=0; i<hout->GetNbinsX(); ++i){
    // simple refill, histograms are already devided by bin width
    // but for a useful lotting the bin errors for MC need to be 
    // set to zero.
    hout->SetBinContent(i+1, hin->GetBinContent(i+1));
    hout->SetBinError(i+1, 0.);
  }
  return hout;
}

void 
postfit_use(const char* inputfile, const char* analysis = "SM", const char* dataset = "2011+2012", const char* extra="", const char* extra2="", float min=0.1, float max=-1., bool log=true)
{
  // defining the common canvas, axes pad styles
  SetStyle(); gStyle->SetLineStyleString(11,"20 10");
  // switch for MSSM/SM
  bool MSSM = std::string(analysis) == std::string("MSSM");
  // determine label
  if (std::string(dataset) == std::string("2011"     )){ dataset = "#scale[1.5]{CMS}  h,H,A#rightarrow#tau#tau                                 4.9 fb^{-1} (7 TeV)"; }
  if (std::string(dataset) == std::string("2012"     )){ dataset = "#scale[1.5]{CMS}  h,H,A#rightarrow#tau#tau                                19.7 fb^{-1} (8 TeV)"; }
  if (std::string(dataset) == std::string("2011+2012")){ dataset = "#scale[1.5]{CMS}  h,H,A#rightarrow#tau#tau    19.7 fb^{-1} (8 TeV) + 4.9 fb^{-1} (7 TeV)"; }
  //if (std::string(dataset) == std::string("2011+2012")){ dataset = "h,H,A#rightarrow#tau#tau                19.7 fb^{-1} (8 TeV) + 4.9 fb^{-1} (7 TeV)"; }
  // determine category tag
  const char* category_extra = "";
  if(std::string(extra2) == std::string("0jet_low"  )){ category_extra = "0 jet, low p_{T}";  }
  if(std::string(extra2) == std::string("0jet_high" )){ category_extra = "0 jet, high p_{T}"; }
  if(std::string(extra2) == std::string("0jet"      )){ category_extra = "0 jet";             }
  if(std::string(extra2) == std::string("1jet_low"  )){ category_extra = "1 jet, low p_{T}";  }
  if(std::string(extra2) == std::string("1jet_high" )){ category_extra = "1 jet, high p_{T}"; }
  if(std::string(extra2) == std::string("1jet"      )){ category_extra = "1 jet";             }
  if(std::string(extra2) == std::string("vbf"       )){ category_extra = "2 jet (VBF)";       }
  if(std::string(extra2) == std::string("nobtag"    )){ category_extra = "no b-tag";          }
  if(std::string(extra2) == std::string("btag"      )){ category_extra = "b-tag";             }
  if(std::string(extra2) == std::string("nobtag_low"   )){ category_extra = "no b-tag, low p_{T}";    }
  if(std::string(extra2) == std::string("nobtag_medium")){ category_extra = "no b-tag, medium p_{T}"; }
  if(std::string(extra2) == std::string("nobtag_high"  )){ category_extra = "no b-tag, high p_{T}";   }
  if(std::string(extra2) == std::string("btag_low"     )){ category_extra = "b-tag, low p_{T}";       }
  if(std::string(extra2) == std::string("btag_high"    )){ category_extra = "b-tag, high p_{T}";      }

  TFile* input = new TFile(inputfile);
  TH1F* Fakes  = refill((TH1F*)input->Get("Fakes"   ), "Fakes/QCD"); 
  TH1F* EWK    = refill((TH1F*)input->Get("EWK"     ), "EWK"      ); 
  TH1F* ttbar  = refill((TH1F*)input->Get("ttbar"   ), "ttbar"    ); 
  TH1F* Ztt    = refill((TH1F*)input->Get("Ztt"     ), "Ztt"      ); 
  TH1F* Zmm    = refill((TH1F*)input->Get("Zmm"     ), "Zmm"      ); 
  TH1F* Zee    = refill((TH1F*)input->Get("Zee"     ), "Zee"      ); 
  TH1F* ggH    = refill((TH1F*)input->Get("ggH"     ), "ggH"      ); 
  TH1F* ggH_SM125= refill((TH1F*)input->Get("ggH_SM125"), "ggH_SM125"); 
  TH1F* VH_SM125 = refill((TH1F*)input->Get("VH_SM125" ), "VH_SM125" ); 
  //TH1F* qqH_SM125= refill((TH1F*)input->Get("qqH_SM125"), "qqH_SM125"); 
  TH1F* data   = (TH1F*)input->Get("data_obs"); 
  /*// determine channel for etau Z->ee (EWK) will be shown separated from the rest (EWK1)
  TH1F* EWK1   = 0;
  if(std::string(extra) == std::string("e#tau_{h}")){
    EWK1 = refill((TH1F*)input->Get("EWK1"),  "EWK1");
    }*/
  TH1F* ggH_hww = 0;
  if(std::string(extra) == std::string("e#mu") and HWWBG){
    ggH_hww= refill((TH1F*)input->Get("ggH_hww" ), "ggH_hww"  ); 
  }
  TH1F* errorBand = (TH1F*)input->Get("errorBand");
  
  /* 
    mass plot before and after fit
  */
  TCanvas *canv = MakeCanvas("canv", "histograms", 600, 600);
  if(log) canv->SetLogy(1);
  // reduce the axis range if necessary for linea plots and SM
  if(MSSM && !log){ data->GetXaxis()->SetRange(0, data->FindBin(345)); } else{ data->GetXaxis()->SetRange(0, data->FindBin(UPPER_EDGE)); };
  if(!MSSM){ data->GetXaxis()->SetRange(0, data->FindBin(345)); }
  data->SetNdivisions(505);
  data->SetMinimum(min);
  if(std::string(extra) == std::string("#mu#mu")){
    data->SetMaximum(max>0 ? max : std::max(maximum(data, log), maximum(Zmm, log)));
    data->Draw("e");
    if(log){
      Zmm  ->SetFillColor(TColor::GetColor(100,182,232));
      Zmm  ->Draw("same");
      Ztt  ->Draw("same");
      ttbar->Draw("same");
      Fakes->Draw("same");
      EWK ->SetFillColor(TColor::GetColor(222,90,106));
      EWK  ->Draw("same");
      if(ggH_SM125) ggH_SM125->Draw("same");
      if(ggH) ggH  ->Draw("histsame");
    }
  }
  else if(std::string(extra) == std::string("ee")){
    data->SetMaximum(max>0 ? max : std::max(maximum(data, log), maximum(Zee, log)));
    data->Draw("e");
    if(log){
      Zee  ->SetFillColor(TColor::GetColor(100,182,232));
      Zee  ->Draw("same");
      Ztt  ->Draw("same");
      ttbar->Draw("same");
      Fakes->Draw("same");
      EWK ->SetFillColor(TColor::GetColor(222,90,106));
      EWK  ->Draw("same");
      if(VH_SM125) VH_SM125->Draw("same");
      if(ggH) ggH  ->Draw("histsame");
    }
  }
  else if(std::string(extra) == std::string("e#tau_{h}")){
    data->SetMaximum(max>0 ? max : std::max(maximum(data, log), maximum(Ztt, log)));
    data->Draw("e");
    if(log){
      Ztt  ->Draw("same");
      ttbar->Draw("same");
      Zee  ->SetFillColor(TColor::GetColor(100,182,232));
      Zee  ->Draw("same");
      EWK  ->SetFillColor(TColor::GetColor(222,90,106));
      EWK  ->Draw("same");
      Fakes->Draw("same");
      if(VH_SM125) VH_SM125->Draw("same");
      if(ggH) ggH  ->Draw("histsame");
    }
    else{
      if(ggH) ggH  ->Draw("histsame");
      Ztt  ->Draw("same");
      ttbar->Draw("same");
      Zee  ->SetFillColor(TColor::GetColor(100,182,232));
      Zee  ->Draw("same");
      EWK  ->SetFillColor(TColor::GetColor(222,90,106));
      EWK  ->Draw("same");
      if(VH_SM125) VH_SM125->Draw("same");
      Fakes->Draw("same");
    } 
  }
  else if(std::string(extra) == std::string("e#mu") && HWWBG){
    data->SetMaximum(max>0 ? max : std::max(maximum(data, log), maximum(ggH_hww, log)));
    data->Draw("e");
    if(log){
      ggH_hww -> Draw("same");
      Ztt  ->Draw("same");
      ttbar->Draw("same");
      EWK ->SetFillColor(TColor::GetColor(222,90,106));
      EWK  ->Draw("same");
      Fakes->Draw("same");
      if(VH_SM125) VH_SM125->Draw("same");
      if(ggH) ggH  ->Draw("histsame");
    }
    else{
      if(ggH) ggH  ->Draw("histsame");
      ggH_hww -> Draw("same");
      Ztt  ->Draw("same");
      ttbar->Draw("same");
      EWK ->SetFillColor(TColor::GetColor(222,90,106));
      EWK  ->Draw("same");
      Fakes->Draw("same");
      if(VH_SM125) VH_SM125->Draw("same");
    } 
  }
  else{
    data->SetMaximum(max>0 ? max : std::max(maximum(data, log), maximum(Ztt, log)));
    data->Draw("e");
    if(log){
      Ztt  ->Draw("same");
      ttbar->Draw("same");
      EWK ->SetFillColor(TColor::GetColor(222,90,106));
      EWK  ->Draw("same");
      Fakes->Draw("same");
      if(VH_SM125) VH_SM125->Draw("same");
      if(ggH) ggH  ->Draw("histsame");
    }
    else{
      if(ggH) ggH  ->Draw("histsame");
      Ztt  ->Draw("same");
      ttbar->Draw("same");
      EWK ->SetFillColor(TColor::GetColor(222,90,106));
      EWK  ->Draw("same");
      Fakes->Draw("same");
      if(VH_SM125) VH_SM125->Draw("same");
    } 
  }
  if(errorBand){
    errorBand->Draw("e2same");
  }
  data->Draw("esame");
  canv->RedrawAxis();



  //CMSPrelim(dataset, extra, 0.17, 0.835);
  CMSPrelim(dataset, "", 0.16, 0.835);  
  TPaveText* chan     = new TPaveText(0.20, 0.74+0.061, 0.32, 0.74+0.161, "tlbrNDC");
  chan->SetBorderSize(   0 );
  chan->SetFillStyle(    0 );
  chan->SetTextAlign(   12 );
  chan->SetTextSize ( 0.05 );
  chan->SetTextColor(    1 );
  chan->SetTextFont (   62 );
  chan->AddText(extra);
  chan->AddText(category_extra);
  chan->Draw();
  /*
  TPaveText* cat      = new TPaveText(0.20, 0.68+0.061, 0.32, 0.68+0.161, "NDC");
  cat->SetBorderSize(   0 );
  cat->SetFillStyle(    0 );
  cat->SetTextAlign(   12 );
  cat->SetTextSize ( 0.05 );
  cat->SetTextColor(    1 );
  cat->SetTextFont (   62 );
  cat->AddText(category_extra);
  cat->Draw();
  */
  if(MSSM){
    float lower_bound = 0.44;
    TPaveText* massA      = new TPaveText(0.53, lower_bound+0.061, 0.95, lower_bound+0.151, "NDC");
    massA->SetBorderSize(   0 );
    massA->SetFillStyle(    0 );
    massA->SetTextAlign(   12 );
    massA->SetTextSize ( 0.03 );
    massA->SetTextColor(    1 );
    massA->SetTextFont (   62 );
    massA->AddText("MSSM m^{h}_{mod+} scenario");
    massA->AddText("m_{A}=$MA GeV, tan#beta=$TANB");
    massA->Draw();
  }    
  float lower_bound = 0.60;
  TLegend* leg = new TLegend(MSSM ? 0.53 : 0.50, lower_bound, 0.93, 0.90);
  SetLegendStyle(leg);
  leg->SetTextSize(0.035);
  if(MSSM){
    leg->AddEntry(ggH  , "h,H,A#rightarrow#tau#tau", "L" );
  }
  else{
    if(ggH){
      if(SIGNAL_SCALE!=1){
	leg->AddEntry(ggH  , TString::Format("%.0f#timesH(125 GeV)#rightarrow#tau#tau", SIGNAL_SCALE) , "L" );
      }
      else{
	leg->AddEntry(ggH  , "H(125 GeV)#rightarrow#tau#tau" , "L" );
      }
    }
  }
  leg->AddEntry(data , "Observed"                       , "LP");
  
  if(std::string(extra) == std::string("#mu#mu")){
    leg->AddEntry(Zmm  , "Z#rightarrow#mu#mu"    , "F" );
    leg->AddEntry(Ztt  , "Z#rightarrow#tau#tau"           , "F" );
    leg->AddEntry(ttbar, "t#bar{t}"                       , "F" );
    leg->AddEntry(Fakes, "QCD"                 , "F" );
    leg->AddEntry(EWK  , "Electroweak"                  , "F" );
    if(ggH_SM125) leg->AddEntry(ggH_SM125, "SM H(125 GeV) #rightarrow #tau#tau", "F" );
  }
  else if(std::string(extra) == std::string("ee")){
    leg->AddEntry(Zee  , "Z#rightarrowee"        , "F" );
    leg->AddEntry(Ztt  , "Z#rightarrow#tau#tau"           , "F" );
    leg->AddEntry(ttbar, "t#bar{t}"                       , "F" );
    leg->AddEntry(Fakes, "QCD"                 , "F" );
    leg->AddEntry(EWK  , "Electroweak"                  , "F" );
    if(VH_SM125) leg->AddEntry(VH_SM125, "SM H(125 GeV) #rightarrow #tau#tau", "F" );
  }
  else if(std::string(extra) == std::string("e#tau_{h}")){
    leg->AddEntry(Ztt  , "Z#rightarrow#tau#tau"           , "F" );
    leg->AddEntry(Zee  , "Z#rightarrow ee"              , "F" );
    leg->AddEntry(EWK  , "Electroweak"                  , "F" );
    leg->AddEntry(ttbar, "t#bar{t}"                       , "F" );
    leg->AddEntry(Fakes, "QCD"                 , "F" );
    if(VH_SM125) leg->AddEntry(VH_SM125, "SM H(125 GeV) #rightarrow #tau#tau", "F" );
  }
  else if(std::string(extra) == std::string("e#mu") && HWWBG){
    leg->AddEntry(ggH_hww  , "H(125 GeV)#rightarrowWW" , "F" );
    leg->AddEntry(Ztt  , "Z#rightarrow#tau#tau"           , "F" );
    leg->AddEntry(ttbar, "t#bar{t}"                       , "F" );
    leg->AddEntry(EWK  , "Electroweak"                  , "F" );
    leg->AddEntry(Fakes, "QCD"                 , "F" );
    if(VH_SM125) leg->AddEntry(VH_SM125, "SM H(125 GeV) #rightarrow #tau#tau", "F" );
  }
  else{
    leg->AddEntry(Ztt  , "Z#rightarrow#tau#tau"           , "F" );
    leg->AddEntry(ttbar, "t#bar{t}"                       , "F" );
    leg->AddEntry(EWK  , "Electroweak"                  , "F" );
    leg->AddEntry(Fakes, "QCD"                 , "F" );
    if(VH_SM125) leg->AddEntry(VH_SM125, "SM H(125 GeV) #rightarrow #tau#tau", "F" );
  }
  if(errorBand){
    leg->AddEntry(errorBand, "Bkg. uncertainty" , "F" );
  }
  leg->Draw();

  /*
    prepare output
  */
  std::string newName = std::string(inputfile).substr(0, std::string(inputfile).find(".root"));
  canv->Print(TString::Format("%s.png", newName.c_str())); 
  canv->Print(TString::Format("%s.pdf", newName.c_str())); 
  canv->Print(TString::Format("%s.eps", newName.c_str())); 

  /*
    Ratio Data over MC
  */
  TCanvas *canv0 = MakeCanvas("canv0", "histograms", 600, 400);
  canv0->SetGridx();
  canv0->SetGridy();
  canv0->cd(); 
  TH1F* model;
  if(CONSERVATIVE_CHI2){
    if(std::string(extra) == std::string("#mu#mu")){
      model = (TH1F*)Zmm ->Clone("model");
    }
    else if(std::string(extra) == std::string("ee")){
      model = (TH1F*)Zee ->Clone("model");
    }
    else if(std::string(extra) == std::string("e#mu") && HWWBG){
      model = (TH1F*)ggH_hww ->Clone("model");
    }
    else{  
      model = (TH1F*)Ztt ->Clone("model");
    }
  }
  else{
    model = (TH1F*)errorBand->Clone("model");
  }
  TH1F* test1 = (TH1F*)data->Clone("test1"); 
  for(int ibin=0; ibin<test1->GetNbinsX(); ++ibin){
    //the small value in case of 0 entries in the model is added to prevent the chis2 test from failing
    model->SetBinContent(ibin+1, model->GetBinContent(ibin+1)>0 ? model->GetBinContent(ibin+1)*model->GetBinWidth(ibin+1) : 0.01);
    model->SetBinError  (ibin+1, CONSERVATIVE_CHI2 ? 0. : model->GetBinError  (ibin+1)*model->GetBinWidth(ibin+1));
    test1->SetBinContent(ibin+1, test1->GetBinContent(ibin+1)*test1->GetBinWidth(ibin+1));
    test1->SetBinError  (ibin+1, test1->GetBinError  (ibin+1)*test1->GetBinWidth(ibin+1));
  }
  double chi2prob = test1->Chi2Test      (model,"PUW");        std::cout << "chi2prob:" << chi2prob << std::endl;
  double chi2ndof = test1->Chi2Test      (model,"CHI2/NDFUW"); std::cout << "chi2ndf :" << chi2ndof << std::endl;
  double ksprob   = test1->KolmogorovTest(model);              std::cout << "ksprob  :" << ksprob   << std::endl;
  double ksprobpe = test1->KolmogorovTest(model,"DX");         std::cout << "ksprobpe:" << ksprobpe << std::endl;  

  std::vector<double> edges;
  TH1F* zero = (TH1F*)Ztt->Clone("zero"); zero->Clear();
  TH1F* rat1 = (TH1F*)data->Clone("rat"); 
  for(int ibin=0; ibin<rat1->GetNbinsX(); ++ibin){
    rat1->SetBinContent(ibin+1, errorBand->GetBinContent(ibin+1)>0 ? data->GetBinContent(ibin+1)/errorBand->GetBinContent(ibin+1) : 0);
    rat1->SetBinError  (ibin+1, errorBand->GetBinContent(ibin+1)>0 ? data->GetBinError  (ibin+1)/errorBand->GetBinContent(ibin+1) : 0);
    zero->SetBinContent(ibin+1, 0.);
    zero->SetBinError  (ibin+1, errorBand->GetBinContent(ibin+1)>0 ? errorBand ->GetBinError  (ibin+1)/errorBand->GetBinContent(ibin+1) : 0);
  }
  for(int ibin=0; ibin<rat1->GetNbinsX(); ++ibin){
    if(rat1->GetBinContent(ibin+1)>0){
      edges.push_back(TMath::Abs(rat1->GetBinContent(ibin+1)-1.)+TMath::Abs(rat1->GetBinError(ibin+1)));
      // catch cases of 0 bins, which would lead to 0-alpha*0-1
      rat1->SetBinContent(ibin+1, rat1->GetBinContent(ibin+1)-1.);
    }
    zero->SetBinContent(ibin+1, 0.);
  }
  float range = 0.1;
  std::sort(edges.begin(), edges.end());
  if (edges[edges.size()-2]>0.1) { range = 0.2; }
  if (edges[edges.size()-2]>0.2) { range = 0.5; }
  if (edges[edges.size()-2]>0.5) { range = 1.0; }
  if (edges[edges.size()-2]>1.0) { range = 1.5; }
  if (edges[edges.size()-2]>1.5) { range = 2.0; }
  rat1->SetLineColor(kBlack);
  rat1->SetFillColor(kGray );
  rat1->SetMaximum(+range);
  rat1->SetMinimum(-range);
  rat1->GetYaxis()->CenterTitle();
  rat1->GetYaxis()->SetTitle("#bf{Data/MC-1}");
  if((std::string(extra) == std::string("#mu#mu") || std::string(extra) == std::string("ee")) && !MSSM){
    rat1->GetXaxis()->SetTitle("#bf{D}");
  }
  else{
    rat1->GetXaxis()->SetTitle("#bf{m_{#tau#tau} [GeV]}");
  }
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
  stat1->AddText(TString::Format("#chi^{2}/ndf=%.3f,  P(#chi^{2})=%.3f", chi2ndof, chi2prob));
  //stat1->AddText(TString::Format("#chi^{2}/ndf=%.3f,  P(#chi^{2})=%.3f,  P(KS)=%.3f", chi2ndof, chi2prob, ksprob));
  stat1->Draw();

  /*
    prepare output
  */
  newName = std::string(inputfile).substr(0, std::string(inputfile).find(".root")) + "_datamc";
  canv0->Print(TString::Format("%s.png", newName.c_str())); 
  canv0->Print(TString::Format("%s.pdf", newName.c_str())); 
  canv0->Print(TString::Format("%s.eps", newName.c_str())); 
}
