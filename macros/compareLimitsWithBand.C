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

std::string legendEntry(const std::string& channel){
  std::string title;
  if(channel==std::string("em"        )) title = std::string("e#mu");
  if(channel==std::string("et"        )) title = std::string("e#tau_{h}");
  if(channel==std::string("mt"        )) title = std::string("#mu#tau_{h}");
  if(channel==std::string("tt"        )) title = std::string("#tau_{h}#tau_{h}");
  if(channel==std::string("mm"        )) title = std::string("#mu#mu");
  if(channel==std::string("vhtt"      )) title = std::string("VH#rightarrow#tau#tau+l(l)");
  if(channel==std::string("htt"       )) title = std::string("e#mu+e#tau_{h}+#mu#tau_{h}+#mu#mu");
  if(channel==std::string("cmb"       )) title = std::string("Combined(H#rightarrow#tau#tau)");
  if(channel==std::string("cmb+"      )) title = std::string("H#rightarrow#tau#tau + VH#rightarrow#tau#tau+l");
  if(channel==std::string("0jet"      )) title = std::string("0-Jet");
  if(channel==std::string("2jet"      )) title = std::string("V(jj)H(#tau#tau)");
  if(channel==std::string("vbf"       )) title = std::string("2-Jet (VBF)");
  if(channel==std::string("boost"     )) title = std::string("1-Jet");
  if(channel==std::string("btag"      )) title = std::string("B-Tag");
  if(channel==std::string("nobtag"    )) title = std::string("No B-Tag");
  if(channel==std::string("ggH"       )) title = std::string("gg#rightarrow#phi (bbH profiled)");
  if(channel==std::string("bbH"       )) title = std::string("gg#rightarrowbb#phi (ggH profiled)");
  if(channel==std::string("mvis"      )) title = std::string("Visible mass");
  if(channel==std::string("test-0"    )) title = std::string("w/o prefit");
  if(channel==std::string("test-1"    )) title = std::string("w/o prefit");
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

void compareLimitsWithBand(const char* filename, const char* channelstr, double minimum=0., double maximum=5., bool log=false, const char* label=" Preliminary, #sqrt{s} = 7+8 TeV, H#rightarrow#tau#tau, L=17 fb^{-1}", bool addExpected=false, bool addObserved=true)
{
  SetStyle();

  std::cout << " **************************************************************************************************************\n"
	    << " * Usage     : root -l                                                                                         \n"
	    << " *             .x MitLimits/Higgs2Tau/macros/injectSignal.C+(file, chn, min, max, log, label, addExp, addObs)  \n"
	    << " *                                                                                                             \n"
	    << " * Arguments :  + file     const char*      full path to the input file                                        \n"
	    << " *              + chn      const char*      list of channels; choose between: 'cmb', 'htt', 'emu',             \n"
	    << " *                                          'etau', 'mutau', 'mumu', 'vhtt', 'hgg', 'hww', 'ggH',              \n"
	    << " *                                          'bbH', 'nomix[-200, +200]', 'mhmax[-400, -200, +200]'              \n"
	    << " *                                          'mhmax[+400, +600, +800]', 'test-0...5', 'saeff', 'gluph'          \n"
	    << " *                                          The list should be comma separated and may contain                 \n"
	    << " *                                          whitespaces                                                        \n"
	    << " *              + max       double          maximum of the plot (default is 5.)                                \n"
	    << " *                                                                                                             \n"
	    << " *              + min       double          minimum of the plot (default is 0.)                                \n"
	    << " *                                                                                                             \n"
	    << " *              + log       bool            set log scale yes or no (default is false)                         \n"
	    << " *                                                                                                             \n"
	    << " *              + addExp    bool            add alternative expected limit (default is false)                  \n"
	    << " *                                                                                                             \n"
	    << " *              + addObs    bool            add alternative observed limit (default is false)                  \n"
	    << " **************************************************************************************************************\n";

  /// open input file  
  TFile* inputFile = new TFile(filename); if(inputFile->IsZombie()){ std::cout << "ERROR:: file: " << filename << " does not exist.\n"; }
  /// prepare input parameters
  std::vector<std::string> channels;
  string2Vector(cleanupWhitespaces(channelstr), channels);

  /// prepare histograms
  std::vector<TGraph*> observed, expected;
  std::vector<TGraphAsymmErrors*> innerBand, outerBand;

  std::map<std::string, unsigned int> colors;
  colors["0jet"       ] = kBlue;
  colors["2jet"       ] = kMagenta;
  colors["vbf"        ] = kRed;
  colors["boost"      ] = kGreen;
  colors["btag"       ] = kRed;
  colors["nobtag"     ] = kBlue;
  colors["em"         ] = kBlue;
  colors["et"         ] = kRed;
  colors["mt"         ] = kGreen;
  colors["mm"         ] = kMagenta;
  colors["tt"         ] = kMagenta+3;
  colors["vhtt"       ] = kMagenta+2;
  colors["cmb"        ] = kBlack;
  colors["cmb+"       ] = kGray+2;
  colors["htt"        ] = kBlack;
  colors["ggH"        ] = kRed;
  colors["bbH"        ] = kBlue;
  colors["mvis"       ] = kBlue+2;
  colors["test-0"     ] = kRed+2;
  colors["test-1"     ] = kGreen+2;
  colors["test-2"     ] = kGreen;
  colors["test-3"     ] = kRed+2;
  colors["test-4"     ] = kBlue;
  colors["test-5"     ] = kViolet-6;
  colors["HIG-11-020" ] = kBlue+2;
  colors["HIG-11-029" ] = kRed+2;
  colors["HIG-12-018" ] = kBlue;
  colors["HIG-12-032" ] = kRed+2;
  colors["HIG-12-043" ] = kRed;
  colors["HIG-12-050" ] = kBlack;

  for(unsigned i=0; i<channels.size(); ++i){    
    /// observed
    observed.push_back(get<TGraph>(inputFile, std::string(channels[i]).append("/observed").c_str()));
    ///expected
    expected.push_back(get<TGraph>(inputFile, std::string(channels[i]).append("/expected").c_str()));
    /// inner band
    innerBand.push_back(get<TGraphAsymmErrors>(inputFile, std::string(channels[i]).append("/innerBand").c_str()));
    /// outer band
    outerBand.push_back(get<TGraphAsymmErrors>(inputFile, std::string(channels[i]).append("/outerBand").c_str()));
    //std::cout << outerBand.size() << std::endl;
  }

  /// do the drawing
  TCanvas* canv = new TCanvas("canv", "Signal Injection", 600, 600);
  canv->SetLogy(log);
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

  if(addExpected){
    for(unsigned int idx=0; idx<observed.size(); ++idx){
      expected[idx]->SetLineColor(idx==0 ? kRed : kRed+2);
      expected[idx]->SetLineWidth(3);
      expected[idx]->SetLineStyle(idx==0 ? 1 : 11);
      expected[idx]->Draw("L");
    }
  }
  else{
      expected[0]->SetLineColor(kRed);
      expected[0]->SetLineWidth(3);
      expected[0]->SetLineStyle(1);
      expected[0]->Draw("L");
  }
  unit->SetLineColor(kBlue);
  unit->SetLineWidth(3.);
  unit->Draw("Lsame");

  if(addObserved){
    for(unsigned int idx=0; idx<observed.size(); ++idx){
      if(idx==0){
	observed[idx]->SetLineStyle(1);
	observed[idx]->SetMarkerStyle(20);
	observed[idx]->SetMarkerColor(colors[channels[idx]]);
	observed[idx]->SetMarkerSize(1.0);
	observed[idx]->SetLineWidth(3.);
	observed[idx]->SetLineColor(colors[channels[idx]]);
	observed[idx]->Draw("PLsame");
      }
      else{
	observed[idx]->SetLineStyle(11);
	observed[idx]->SetMarkerStyle(20);
	observed[idx]->SetMarkerSize(1.0);
	observed[idx]->SetMarkerColor(colors[channels[idx]]);
	observed[idx]->SetLineWidth(3.);
	observed[idx]->SetLineColor(colors[channels[idx]]);
	observed[idx]->Draw("PLsame");
      }
    }
  }
  else{
    observed[0]->SetLineStyle(1);
    observed[0]->SetLineWidth(3.);
    observed[0]->Draw("PLsame");
  }
  /// setup the CMS Preliminary
  CMSPrelim(label, "", 0.145, 0.835);

  /// add the proper legend
  TLegend* leg = new TLegend(0.20, 0.65, 0.64, 0.90);
  leg->SetBorderSize( 0 );
  leg->SetFillStyle ( 1001 );
  //leg->SetFillStyle ( 0 );
  leg->SetFillColor (kWhite);
  //leg->SetHeader( "95% CL Limits" );
  if(expected.size()>0){ leg->AddEntry( expected[0] , "expected (HIG-12-018)",  "L" );}
  leg->AddEntry( innerBand[0], "#pm 1#sigma expected" ,  "F" );
  leg->AddEntry( outerBand[0], "#pm 2#sigma expected" ,  "F" );
  for(unsigned int idx=0; idx<observed.size(); ++idx){
    leg->AddEntry( observed[idx] , legendEntry(channels[idx]).c_str(), "PL");
  }
  //if(observed.size()>0){ leg->AddEntry( observed[0] , "observed HCP",  "PL" );}
  //if(observed.size()>1){ leg->AddEntry( observed[1] , "single toy (inj. signal)",  "PL" );}
  //if(expected.size()>1 && addExpected){ leg->AddEntry( expected[1] , "projection to 5+12/fb",  "L" );}
  leg->Draw("same");
  //canv.RedrawAxis("g");
  canv->RedrawAxis();

  canv->Print(std::string("injected.png").c_str());
  canv->Print(std::string("injected.pdf").c_str());
  canv->Print(std::string("injected.eps").c_str());

  return;
}
