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


void injectedSignal(const char* filename, const char* channelstr, double minimum=0., double maximum=5., bool log=false, const char* label=" Preliminary, #sqrt{s} = 7+8 TeV, H#rightarrow#tau#tau, L = 10 fb^{-1}")
{
  SetStyle();

  std::cout << " *******************************************************************************************************\n"
	    << " * Usage     : root -l                                                                                  \n"
	    << " *             .x MitLimits/Higgs2Tau/macros/injectSignal.C+(file, chn, min, max, log, label)           \n"
	    << " *                                                                                                      \n"
	    << " * Arguments :  + file     const char*      full path to the input file                                 \n"
	    << " *              + chn      const char*      list of channels; choose between: 'cmb', 'htt', 'emu',      \n"
	    << " *                                          'etau', 'mutau', 'mumu', 'vhtt', 'hgg', 'hww', 'ggH',       \n"
	    << " *                                          'bbH', 'nomix[-200, +200]', 'mhmax[-400, -200, +200]'       \n"
	    << " *                                          'mhmax[+400, +600, +800]', 'test-0...5', 'saeff', 'gluph'   \n"
	    << " *                                          The list should be comma separated and may contain          \n"
	    << " *                                          whitespaces                                                 \n"
	    << " *              + max       double          maximum of the plot (default is 5.)                         \n"
	    << " *                                                                                                      \n"
	    << " *              + min       double          minimum of the plot (default is 0.)                         \n"
	    << " *                                                                                                      \n"
	    << " *              + log       bool            set log scale yes or no (default is false)                  \n"
	    << " *                                                                                                      \n"
	    << " *******************************************************************************************************\n";

  /// open input file  
  TFile* inputFile = new TFile(filename); if(inputFile->IsZombie()){ std::cout << "ERROR:: file: " << filename << " does not exist.\n"; }
  /// prepare input parameters
  std::vector<std::string> channels;
  string2Vector(cleanupWhitespaces(channelstr), channels);

  /// prepare histograms
  std::vector<TGraph*> observed, expected;
  std::vector<TGraphAsymmErrors*> innerBand, outerBand;

  for(unsigned i=0; i<channels.size(); ++i){    
    /// observed
    observed.push_back(get<TGraph>(inputFile, std::string(channels[i]).append("/observed").c_str()));
    ///expected
    expected.push_back(get<TGraph>(inputFile, std::string(channels[i]).append("/expected").c_str()));
    /// inner band
    innerBand.push_back(get<TGraphAsymmErrors>(inputFile, std::string(channels[i]).append("/innerBand").c_str()));
    /// outer band
    outerBand.push_back(get<TGraphAsymmErrors>(inputFile, std::string(channels[i]).append("/outerBand").c_str()));
    std::cout << outerBand.size() << std::endl;
  }

  /// do the drawing
  TCanvas* canv = new TCanvas("canv", "Signal Injection", 600, 600);
  canv->cd();
  canv->SetGridx(1);
  canv->SetGridy(1);

  // draw a frame to define the range
  TH1F* hr = canv->DrawFrame(outerBand[0]->GetX()[0]-.01, minimum, outerBand[0]->GetX()[outerBand[0]->GetN()-1]+.01, maximum);
  hr->SetXTitle("m_{H} [GeV]");
  hr->GetXaxis()->SetLabelFont(62);
  hr->GetXaxis()->SetLabelSize(0.045);
  hr->GetXaxis()->SetLabelOffset(0.015);
  hr->GetXaxis()->SetTitleFont(62);
  hr->GetXaxis()->SetTitleColor(1);
  hr->GetXaxis()->SetTitleOffset(1.05);
  hr->SetYTitle("95% CL limit on #sigma/#sigma_{SM}");
  hr->GetYaxis()->SetLabelFont(62);
  hr->GetYaxis()->SetTitleSize(0.05);
  hr->GetYaxis()->SetTitleOffset(1.30);
  hr->GetYaxis()->SetLabelSize(0.045);

  // create the unit line
  TGraph* unit = new TGraph();
  for(int ipoint=0; ipoint<expected[0]->GetN(); ++ipoint){
    unit->SetPoint(ipoint, expected[0]->GetX()[ipoint], 1.);
  }
  
  outerBand[0]->SetLineColor(kBlack);
  //outerBand[0]->SetLineStyle(11);
  outerBand[0]->SetLineWidth(1.);
  outerBand[0]->SetFillColor(kYellow);
  outerBand[0]->Draw("3");

  innerBand[0]->SetLineColor(kBlack);
  //innerBand[0]->SetLineStyle(11);
  innerBand[0]->SetLineWidth(1.);
  innerBand[0]->SetFillColor(kGreen);
  innerBand[0]->Draw("3same");

  expected[0]->SetLineColor(kRed);
  expected[0]->SetLineWidth(3);
  expected[0]->SetLineStyle(1);
  expected[0]->Draw("L");

  unit->SetLineColor(kBlue);
  unit->SetLineWidth(3.);
  unit->Draw("Lsame");

  for(unsigned int idx=0; idx<observed.size(); ++idx){
    if(idx==0){
      observed[idx]->SetLineStyle(11);
      observed[idx]->SetLineWidth(3.);
      observed[idx]->Draw("Lsame");
    }
    else{
      observed[idx]->SetMarkerStyle(20);
      observed[idx]->SetMarkerSize(1.0);
      observed[idx]->SetMarkerColor(kBlack);
      observed[idx]->SetLineWidth(3.);
      observed[idx]->Draw("PLsame");
    }
  }
  /// setup the CMS Preliminary
  CMSPrelim(label, "", 0.145, 0.835);

  /// add the proper legend
  TLegend* leg = new TLegend(0.18, 0.70, 0.805, 0.90);
  leg->SetBorderSize( 0 );
  leg->SetFillStyle ( 1001 );
  //leg->SetFillStyle ( 0 );
  leg->SetFillColor (kWhite);
  //leg->SetHeader( "95% CL Limits" );
  if(observed.size()>0){ leg->AddEntry( observed[0] , "simulation signal inj. (m_{H}=125 GeV)" ,  "L"  );}
  if(observed.size()>1){ leg->AddEntry( observed[1] , "observed",  "PL" );}
  //if(observed.size()>1){ leg->AddEntry( observed[1] , "single toy (inj. signal)",  "PL" );}
  leg->AddEntry( expected[0] , "expected"             ,  "L" );
  leg->AddEntry( innerBand[0], "#pm 1#sigma expected" ,  "F" );
  leg->AddEntry( outerBand[0], "#pm 2#sigma expected" ,  "F" );
  leg->Draw("same");
  //canv.RedrawAxis("g");
  canv->RedrawAxis();

  canv->Print(std::string("injected.png").c_str());
  canv->Print(std::string("injected.pdf").c_str());
  canv->Print(std::string("injected.eps").c_str());

  return;
}
