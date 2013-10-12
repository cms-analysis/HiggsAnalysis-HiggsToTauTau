#include "string" 
#include "vector" 
#include "fstream"
#include "iomanip"
#include "iostream"
#include "algorithm"

#include "TTree.h"
#include "TFile.h"
#include "TAxis.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TPaveLabel.h"
#include "TGraphAsymmErrors.h"
#include "TLine.h"

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"
#include "HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"

static const double MARKER_SIZE = 1.3;  // 0.7

std::string legendEntry(const std::string& channel){
  std::string title;
  if(channel==std::string("em"        )) title = std::string("e#mu");
  if(channel==std::string("et"        )) title = std::string("e#tau_{h}");
  if(channel==std::string("mt"        )) title = std::string("#mu#tau_{h}");
  if(channel==std::string("tt"        )) title = std::string("#tau_{h}#tau_{h}");
  if(channel==std::string("mm"        )) title = std::string("#mu#mu");
  if(channel==std::string("ee"        )) title = std::string("ee");
  if(channel==std::string("vhtt"      )) title = std::string("VH#rightarrow#tau#tau");
  if(channel==std::string("htt"       )) title = std::string("H#rightarrow#tau#tau");
  if(channel==std::string("cmb"       )) title = std::string("H#rightarrow#tau#tau+VH#rightarrow#tau#tau");
  if(channel==std::string("0jet"      )) title = std::string("0-Jet");
  if(channel==std::string("1jet"      )) title = std::string("1-Jet");
  if(channel==std::string("2jet"      )) title = std::string("2-Jet (VBF)");
  if(channel==std::string("vbf"       )) title = std::string("2-Jet (VBF)");
  if(channel==std::string("boost"     )) title = std::string("1-Jet");
  if(channel==std::string("btag"      )) title = std::string("B-Tag");
  if(channel==std::string("nobtag"    )) title = std::string("No B-Tag");
  if(channel==std::string("ggH"       )) title = std::string("gg#rightarrow#phi (bbH profiled)");
  if(channel==std::string("bbH"       )) title = std::string("gg#rightarrowbb#phi (ggH profiled)");
  if(channel==std::string("mvis"      )) title = std::string("Visible mass");
  if(channel==std::string("test-0"    )) title = std::string("gg#rightarrow#phi (bbH set to 0)");
  if(channel==std::string("test-1"    )) title = std::string("gg#rightarrowbb#phi (ggH set to 0)");
  if(channel==std::string("test-2"    )) title = std::string("gg#rightarrowbb#phi (w/o prefit)");
  if(channel==std::string("test-3"    )) title = std::string("gg#rightarrow#phi (w/o prefit)");
  if(channel==std::string("test-4"    )) title = std::string("Test-4");
  if(channel==std::string("test-5"    )) title = std::string("Test-5");
  if(channel==std::string("HIG-11-020")) title = std::string("HIG-11-020 (1.6 fb^{-1})");
  if(channel==std::string("HIG-11-020")) title = std::string("HIG-11-020 (1.6 fb^{-1})");
  if(channel==std::string("HIG-11-029")) title = std::string("HIG-11-029 (4.9 fb^{-1})");
  if(channel==std::string("HIG-12-018")) title = std::string("HIG-12-018 (10 fb^{-1})");
  if(channel==std::string("HIG-12-032")) title = std::string("HIG-12-032 (5-10 fb^{-1})");
  if(channel==std::string("HIG-12-043")) title = std::string("HIG-12-043 (17 fb^{-1})");
  if(channel==std::string("HIG-12-050")) title = std::string("HIG-12-050 (17 fb^{-1})");
  return title;
}

void compareBestFit(const char* filename="test.root", const char* channelstr="boost,vbf,vhtt,cmb+", const char* type="sm", double mass=125, double minimum=-1., double maximum=4.5, const char* label="Preliminary, #sqrt{s}=7-8 TeV, L = 24.3 fb^{-1}, H #rightarrow #tau #tau")
{
  SetStyle();
  std::cout << " ********************************************************************************************************\n"
	    << " * Usage     : root -l                                                                                   \n"
	    << " *             .x macros/compareBestFit.C+(filename, channelstr, type)                                   \n"
	    << " *                                                                                                       \n"
	    << " * Arguments :  + filename   const char*     full path to the input file                                 \n"
	    << " *              + channelstr const char*     list of channels; choose between: 'cmb', 'htt', 'em',       \n"
	    << " *                                           'et', 'mt', 'mm', 'vhtt', 'hgg', 'hww', 'ggH',              \n"
	    << " *                                           'bbH', 'nomix[-200, +200]', 'mhmax[-400, -200, +200]'       \n"
	    << " *                                           'mhmax[+400, +600, +800]', 'test-0...5', 'saeff', 'gluph'   \n"
	    << " *                                           The list should be comma separated and may contain          \n"
	    << " *                                           whitespaces                                                 \n"
	    << " *              + type       const char*     type of plot; choose between 'sm' and 'mssm'                \n"
	    << " *                                                                                                       \n"
	    << " *              + mass       double          Higgs mass for which the plot should be performed           \n"
	    << " *                                                                                                       \n"
	    << " *              + minimum    double          Minimum value for the x-Axis (best fit value)               \n"
	    << " *                                                                                                       \n"
	    << " *              + maximum    double          Maximum value for the x-Axis (best fit value)               \n"
	    << " *                                                                                                       \n"
	    << " ********************************************************************************************************\n";

  /// open input file  
  TFile* inputFile = new TFile(filename); if(inputFile->IsZombie()){ std::cout << "ERROR:: file: " << filename << " does not exist.\n"; }

  /// prepare input parameters
  std::vector<std::string> channels;
  string2Vector(cleanupWhitespaces(channelstr), channels);

  /// prepare histograms
  std::vector<TGraph*> hexp;
  std::vector<TGraph*> hband;
  for(unsigned i=0; i<channels.size(); ++i){
    hexp.push_back(get<TGraph>(inputFile, std::string(channels[i]).append("/expected").c_str()));
    hband.push_back(get<TGraph>(inputFile, std::string(channels[i]).append("/innerBand").c_str()));
  }
  int massid = 0; 
  for(int i0  = 0; i0 < hexp[hexp.size()-1]->GetN(); i0++) {   
    double lX = 0; double lY = 0; 
    hexp[hexp.size()-1]->GetPoint(i0, lX, lY);
    if(lX==mass) {massid = i0; break;}
  }
    
  /// do the drawing
  TCanvas* canv1 = new TCanvas("canv1", "Best Fit Comparison", 600, 600);
  canv1->cd();
  canv1->SetGridx(0);
  canv1->SetGridy(0);

  TLine* SM   = new TLine(1, 0, 1, hexp.size());
  TLine* ZERO = new TLine(0, 0, 0, hexp.size());
  
  double *lBestFitX = new double[4];
  double *lBestFitY = new double[4]; 
  lBestFitX[0] = hexp[hexp.size()-1]->Eval(mass) - hband[hband.size()-1]->GetErrorYlow(massid);
  lBestFitX[1] = hexp[hexp.size()-1]->Eval(mass) + hband[hband.size()-1]->GetErrorYhigh(massid);
  lBestFitX[3] = hexp[hexp.size()-1]->Eval(mass) - hband[hband.size()-1]->GetErrorYlow(massid);
  lBestFitX[2] = hexp[hexp.size()-1]->Eval(mass) + hband[hband.size()-1]->GetErrorYhigh(massid);
  lBestFitY[0] = hexp.size();
  lBestFitY[1] = hexp.size();
  lBestFitY[2] = 0;
  lBestFitY[3] = 0;
  TGraph* BAND = new TGraph(4,lBestFitX,lBestFitY); BAND->SetFillColor(kYellow);
  TLine * BEST = new TLine (hexp[hexp.size()-1]->Eval(mass),0,hexp[hexp.size()-1]->Eval(mass),hexp.size()); BEST->SetLineStyle(kDashed); BEST->SetLineColor(kRed);
  bool firstPlot=true;
  for(unsigned int i=0; i<hexp.size(); ++i){
    double value[1] = {hexp[i]->Eval(mass)};
    double position[1] = {hexp.size()-i-0.5}; 

    double x;
    double y;
    double el=0;
    double eh=0;
    int k = hexp[i]->GetN();
    for(int l=0; l<k; l++){
      hexp[i]->GetPoint(l, x, y);
      if(x==mass){
	el=hband[i]->GetErrorYlow(l);
	eh=hband[i]->GetErrorYhigh(l);
	break;
      }
    }

    double elow[1] = {el};
    double ehigh[1] = {eh};
    double help1[1] = {0.0};
    double help2[1] = {0.0};
    TGraphAsymmErrors *gr = new TGraphAsymmErrors(1, value, position, elow, ehigh, help1, help2);
    if(firstPlot){
      if(std::string(type) == std::string("mssm")){
	gr->SetMaximum(hexp.size());
	gr->SetMinimum(0);
      }
      else{
	gr->SetMaximum(hexp.size());
	gr->SetMinimum(0);
      }
      // format x-axis
      std::string x_title;
      if(std::string(type).find("mssm")!=std::string::npos){
	x_title = std::string("best fit for #sigma(#phi#rightarrow#tau#tau)");
      }
      else{
	x_title = std::string("best fit for #sigma/#sigma_{SM}");
      }
      
      gr->GetXaxis()->SetTitle(x_title.c_str());
      gr->GetXaxis()->SetLabelFont(62);
      gr->GetXaxis()->SetTitleFont(62);
      gr->GetXaxis()->SetTitleColor(1);
      gr->GetXaxis()->SetTitleOffset(1.05);
      gr->GetXaxis()->SetLimits(minimum, maximum);

      BAND->GetXaxis()->SetTitle(x_title.c_str());
      BAND->GetXaxis()->SetLabelFont(62);
      BAND->GetXaxis()->SetTitleFont(62);
      BAND->GetXaxis()->SetTitleColor(1);
      BAND->GetXaxis()->SetTitleOffset(1.05);
      BAND->GetXaxis()->SetLimits(minimum, maximum);

      // format y-axis
      //BAND->GetYaxis()->Set(hexp.size(), 0, hexp.size());
      gr  ->GetYaxis()->Set(hexp.size(), 0, hexp.size());
      //std::cout<<gr->GetYaxis()->GetBinCenter(hexp.size()-i)<<std::endl;
      //BAND->GetYaxis()->SetBinLabel(hexp.size()-1, legendEntry(channels[hexp.size()-1]).c_str());
      for(unsigned int j=0; j<hexp.size(); ++j){
	gr  ->GetYaxis()->SetBinLabel(hexp.size()-j, legendEntry(channels[j]).c_str());
      }
      gr->GetYaxis()->SetTickLength(0);
      gr->GetYaxis()->SetLabelFont(62);
      gr->GetYaxis()->SetTitleFont(62);
      gr->GetYaxis()->SetLabelSize(0.07);
      gr->GetYaxis()->SetTitle("");
      gr->GetYaxis()->SetLabelFont(62);
      gr->GetYaxis()->SetTitleOffset(1.05);
      gr->GetYaxis()->SetLabelSize(0.03);           
      gr->GetYaxis()->SetLabelOffset(-0.32);           

      BAND->GetYaxis()->SetLabelFont(62);
      BAND->GetYaxis()->SetTitleFont(62);
      BAND->GetYaxis()->SetLabelSize(0.07);
      BAND->GetYaxis()->SetTitle("");
      BAND->GetYaxis()->SetLabelFont(62);
      BAND->GetYaxis()->SetTitleOffset(1.05);
      BAND->GetYaxis()->SetLabelSize(0.03);           
      BAND->GetYaxis()->SetLabelOffset(-0.32);           
    }
    BAND->GetYaxis()->SetLabelSize(0.07);
    BAND->SetTitle("");
    gr  ->GetYaxis()->SetLabelSize(0.07);
    gr->SetTitle("");
    gr->SetLineStyle( 1.);
    gr->SetLineWidth( 2.); 
    gr->SetLineColor(kBlack);
    gr->SetMarkerStyle(kFullCircle);
    gr->SetMarkerSize(MARKER_SIZE);
    gr->SetMarkerColor(kBlack);
    if(firstPlot) gr->Draw("AP");  
    if(firstPlot) {
      BAND->Draw("Fsame");  
      BEST->Draw("l");
      TLine *lLine = new TLine(minimum,1.0,maximum,1.0); lLine->SetLineWidth(3); lLine->SetLineColor(kBlue+2);
      lLine->Draw();
      SM->SetLineWidth(3);
      SM->SetLineColor(kGreen+3);
      if(std::string(type).find("mssm")==std::string::npos) SM->Draw("same");
    }
    gr->Draw(firstPlot ? "Psame" : "Psame");
    //gr->Draw(firstPlot ? "AL" : "Lsame");
    firstPlot=false;
  }
  ZERO->SetLineWidth(3);
  ZERO->SetLineColor(kBlue);
  ZERO->SetLineStyle(11);
  //ZERO->Draw("same");
  
  //TPaveText *pt = new TPaveText(2*(maximum+minimum)/3,hexp.size()-0.3,maximum,hexp.size()-0.02);
  TPaveText *pt = new TPaveText(0.76, 0.88, 1.0, 1.0, "NDC");
  if(std::string(type).find("mssm")!=std::string::npos) pt->AddText(TString::Format("m_{A} = %0.0f GeV" , mass));
  else pt->AddText(TString::Format("m_{H} = %0.0f GeV" , mass));
  pt->SetBorderSize(   0 );
  pt->SetFillStyle(    0 );
  pt->SetTextAlign(   12 );
  pt->SetTextSize ( 0.03 );
  pt->SetTextColor(    1 );
  pt->SetTextFont (   62 );
  pt->Draw("same");
  canv1->RedrawAxis();
  CMSPrelim(label, "", 0.15, 0.835);
  
  canv1->Print(std::string("BestFit").append(std::string(type).find("mssm")!=std::string::npos ? "_mssm.png" : "_sm.png").c_str());
  canv1->Print(std::string("BestFit").append(std::string(type).find("mssm")!=std::string::npos ? "_mssm.pdf" : "_sm.pdf").c_str());
  canv1->Print(std::string("BestFit").append(std::string(type).find("mssm")!=std::string::npos ? "_mssm.pdf" : "_sm.eps").c_str());
  return;
}
