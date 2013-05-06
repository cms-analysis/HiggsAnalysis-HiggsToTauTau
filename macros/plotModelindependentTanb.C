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

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"
#include "HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"

static const double MARKER_SIZE = 1.3;  // 0.7

bool
channel(std::string& label){
  return (label==std::string("BR0p1")        ||
	  label==std::string("BR0p2")       ||
	  label==std::string("BR0p3")
	  );
}

std::string legendEntry(const std::string& channel){
  std::string title;
  if(channel==std::string("BR0p1"    )) title = std::string("expected BR(#Phi#rightarrow#tau#tau)=0.1");
  if(channel==std::string("BR0p2"    )) title = std::string("expected BR(#Phi#rightarrow#tau#tau)=0.2");
  if(channel==std::string("BR0p3"    )) title = std::string("expected BR(#Phi#rightarrow#tau#tau)=0.3");
  return title;
}

void plotModelindependentTanb(const char* filename, const char* channelstr, bool expected, bool observed, double minimum=0., double maximum=20., const char* label="CMS Preliminary,  H#rightarrow#tau#tau,  4.9 fb^{-1} at 7 TeV, 19.4 fb^{-1} at 8 TeV")
{
  SetStyle();

  std::map<std::string, unsigned int> colors;
  colors["BR0p1"  ] = kBlue;
  colors["BR0p2"  ] = kGreen;
  colors["BR0p3"  ] = kRed;

  std::cout << " *******************************************************************************************************\n"
	    << " * Usage     : root -l                                                                                  \n"
	    << " *             .x MitLimits/Higgs2Tau/macros/compareLimits.C+(file, chn, exp, obs, type, min, max, log) \n"
	    << " *                                                                                                      \n"
	    << " * Arguments :  + file     const char*      full path to the input file                                 \n"
	    << " *                                                                                                      \n"
	    << " *              + chn      const char*      list of BR please order correct high to low or low to high  \n"
	    << " *                                                                                                      \n"
	    << " *              + exp      bool             compare expected limits                                     \n"
	    << " *                                                                                                      \n"
	    << " *              + obs      bool             compare observed limits                                     \n"
	    << " *                                                                                                      \n"
	    << " *              + max      double           maximum of the plot (default is 20.)                        \n"
	    << " *                                                                                                      \n"
	    << " *              + min      double           minimum of the plot (default is  0.)                        \n"
	    << " *                                                                                                      \n"
	    << " *******************************************************************************************************\n";

  /// open input file  
  TFile* inputFile = new TFile(filename); if(inputFile->IsZombie()){ std::cout << "ERROR:: file: " << filename << " does not exist.\n"; }

  /// prepare input parameters
  std::vector<std::string> channels;
  string2Vector(cleanupWhitespaces(channelstr), channels);

  /// prepare histograms
  std::vector<TGraph*> hobs, hexp;
  for(int i=0; i<channels.size(); ++i){
    if(observed) hobs.push_back(get<TGraph>(inputFile, std::string(channels[i]).append("/observed").c_str()));
    if(expected) hexp.push_back(get<TGraph>(inputFile, std::string(channels[i]).append("/expected").c_str()));
  }
  
  double x1, x2, y1, y2;
  TGraphAsymmErrors* Texp = 0;
  if(expected){
    Texp = new TGraphAsymmErrors();
    //Texp->SetPoint(0, 0, 0);
    //Texp->SetPointEYlow (0, 0);
    //Texp->SetPointEYhigh(0, 100); 
    for(int i=0; i<hexp[0]->GetN(); i++){
      hexp[0]            ->GetPoint(i, x1, y1);
      hexp[hexp.size()-1]->GetPoint(i, x2, y2);
      Texp               ->SetPoint(i, x1, y1); 
      if(y1<y2){
	Texp->SetPointEYlow (i, 0);
	Texp->SetPointEYhigh(i, y2-y1);
      }
      else{
	Texp->SetPointEYlow (i, y1-y2);
	Texp->SetPointEYhigh(i, 0);
      }
    }
  }
  
  TGraphAsymmErrors* Tobs = 0;
  if(observed){
    Tobs = new TGraphAsymmErrors();
    //Tobs->SetPoint(0, 0, 100.);
    //Tobs->SetPointEYlow (0, 0);
    //Tobs->SetPointEYhigh(0, 100); 
    for(int i=0; i<hobs[0]->GetN(); i++){
      hobs[0]            ->GetPoint(i, x1, y1);
      hobs[hexp.size()-1]->GetPoint(i, x2, y2);
      Tobs               ->SetPoint(i, x1, y1); 
      if(y1<y2){
	Tobs->SetPointEYlow (i, 0);
	Tobs->SetPointEYhigh(i, y2-y1);
      }
      else{
	Tobs->SetPointEYlow (i, y1-y2);
	Tobs->SetPointEYhigh(i, 0);
      }
    }
  }

  /// do the drawing


  TCanvas* canv1 = new TCanvas("canv1", "Limit Comparison", 600, 600);
  canv1->cd();
  canv1->SetGridx(1);
  canv1->SetGridy(1);

  bool firstPlot=true;
  for(unsigned int i=0; i<hexp.size(); ++i){
    if(firstPlot){
      hexp[i]->SetMaximum(maximum);
      hexp[i]->SetMinimum(minimum);

      // format x-axis
      std::string x_title = std::string("m_{A} [GeV]");
      hexp[i]->GetXaxis()->SetTitle(x_title.c_str());
      hexp[i]->GetXaxis()->SetLabelFont(62);
      hexp[i]->GetXaxis()->SetTitleFont(62);
      hexp[i]->GetXaxis()->SetTitleColor(1);
      hexp[i]->GetXaxis()->SetTitleOffset(1.05);
      hexp[i]->GetYaxis()->SetRangeUser(0,maximum);

      // format y-axis
      std::string y_title = std::string("#bf{tan#beta}");
      hexp[i]->GetYaxis()->SetTitle(y_title.c_str());
      hexp[i]->GetYaxis()->SetLabelFont(62);
      hexp[i]->GetYaxis()->SetTitleOffset(1.05);
      hexp[i]->GetYaxis()->SetLabelSize(0.03);
      hexp[i]->GetXaxis()->SetLimits(hexp[i]->GetX()[0]-.1, hexp[i]->GetX()[hexp[i]->GetN()-1]+.1);
      //hexp[i]->GetXaxis()->SetRangeUser(90,250);
    }
    hexp[i]->SetLineStyle( 1.);
    hexp[i]->SetLineWidth( 4.); 
    hexp[i]->SetLineColor(colors.find(channels[i])->second);
    //hexp[i]->SetMarkerStyle(20);
    //hexp[i]->SetMarkerSize(MARKER_SIZE);
    //hexp[i]->SetMarkerColor(colors.find(channels[i])->second);
    //hexp[i]->Draw(firstPlot ? "APL" : "PLsame");
    hexp[i]->Draw(firstPlot ? "AL" : "Lsame");
    firstPlot=false;
  }
  for(unsigned int i=0; i<hobs.size(); ++i){
    if(firstPlot){
      hobs[i]->SetMaximum(maximum);
      hobs[i]->SetMinimum(minimum);
   
      // format x-axis
      std::string x_title = std::string("m_{A} [GeV]");
      hobs[i]->GetXaxis()->SetTitle(x_title.c_str());
      hobs[i]->GetXaxis()->SetLabelFont(62);
      hobs[i]->GetXaxis()->SetTitleFont(62);
      hobs[i]->GetXaxis()->SetTitleColor(1);
      hobs[i]->GetXaxis()->SetTitleOffset(1.05);
      hobs[i]->GetYaxis()->SetRangeUser(0,maximum);
      
      // format y-axis
      std::string y_title = std::string("#bf{tan#beta}");
      hobs[i]->GetYaxis()->SetTitle(y_title.c_str());
      hobs[i]->GetYaxis()->SetLabelFont(62);
      hobs[i]->GetYaxis()->SetTitleOffset(1.05);
      hobs[i]->GetYaxis()->SetLabelSize(0.03);
      hobs[i]->GetXaxis()->SetLimits(hobs[i]->GetX()[0]-.1, hobs[i]->GetX()[hobs[i]->GetN()-1]+.1);
      //hobs[i]->GetXaxis()->SetRangeUser(90,250);
    }
    hobs[i]->SetLineStyle( 1.);
    hobs[i]->SetLineWidth( 4.); 
    hobs[i]->SetLineColor(colors.find(channels[i])->second);
    //hobs[i]->SetMarkerStyle(20);
    //hobs[i]->SetMarkerSize(MARKER_SIZE);
    //hobs[i]->SetMarkerColor(colors.find(channels[i])->second);
    //hobs[i]->Draw(firstPlot ? "APL" : "PLsame");
    hobs[i]->Draw(firstPlot ? "AL" : "Lsame");
    firstPlot=false;
  }
  canv1->RedrawAxis();

  if(expected){
    Texp->SetFillStyle(1001.);
    Texp->SetFillColor(kGray);
    Texp->Draw("3");    
  }

  if(observed){
    Tobs->SetFillStyle(1001.);
    Tobs->SetFillColor(kCyan);
    Tobs->Draw("3same"); 
  }
  
  canv1->RedrawAxis();

  TLegend* leg1 = new TLegend(0.1, 0.65, 0.5, 0.9);
  CMSPrelim(label, "", 0.15, 0.835);
  //leg1->SetTextSize(0.025);
  leg1->SetBorderSize( 0 );
  leg1->SetFillStyle ( 1001 );
  //leg1->SetFillColor ( 0 );
  leg1->SetFillColor (kWhite);
  leg1->SetHeader("95% CL excluded");
  if(expected){
    for(unsigned int i=0; i<hexp.size(); ++i){
      leg1->AddEntry( hexp[i] , channel(channels[i]) ? legendEntry(channels[i]).c_str() : legendEntry(channels[i]).append("-Channel").c_str(),  "L" );
    }
    leg1->AddEntry( Texp , "limits in between", "F" );
  }
  if(observed && !expected){
    for(unsigned int i=0; i<hobs.size(); ++i){
      leg1->AddEntry( hobs[i] , channel(channels[i]) ? legendEntry(channels[i]).c_str() : legendEntry(channels[i]).append("-Channel").c_str(),  "L" );
    }
    leg1->AddEntry( Tobs , "limits in between", "F" );
  }
  leg1->Draw("same");

  canv1->Print("tanb.pdf");
  canv1->Print("tanb.png");
  canv1->Print("tanb.eps");
  return;
}
