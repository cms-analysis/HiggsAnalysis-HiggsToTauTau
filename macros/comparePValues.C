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
#include "Math/ProbFunc.h"

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"
#include "HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"

static const double MARKER_SIZE = 1.3;  // 0.7

bool
channel(std::string& label){
  return (label==std::string("cmb")        ||
	  label==std::string("htt")        ||
	  label==std::string("vhtt")       ||
	  label==std::string("0jet")       ||
	  label==std::string("1jet")       ||
	  label==std::string("2jet")       ||
	  label==std::string("boost")      ||
	  label==std::string("vbf")        ||
	  label==std::string("btag")       ||
	  label==std::string("nobtag")     ||
	  label==std::string("tt")         ||
	  label==std::string("em")         ||
	  label==std::string("et")         ||
	  label==std::string("mt")         ||
	  label==std::string("mm")         ||
	  label==std::string("ee")         ||
	  label==std::string("ggH")        ||
	  label==std::string("bbH")        ||
	  label==std::string("mvis")       ||
	  label==std::string("HIG-11-020") ||
	  label==std::string("HIG-11-029") ||
	  label==std::string("HIG-12-018") ||
	  label==std::string("HIG-12-032") ||
	  label==std::string("HIG-12-043") ||
	  label==std::string("HIG-12-050")
	  );
}

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
  if(channel==std::string("0jet"      )) title = std::string("1-Jet");
  if(channel==std::string("2jet"      )) title = std::string("2-Jet (VBF)");
  if(channel==std::string("vbf"       )) title = std::string("2-Jet (VBF)");
  if(channel==std::string("boost"     )) title = std::string("1-Jet");
  if(channel==std::string("btag"      )) title = std::string("B-Tag");
  if(channel==std::string("nobtag"    )) title = std::string("No B-Tag");
  if(channel==std::string("ggH"       )) title = std::string("gg#rightarrow#phi (bbH profiled)");
  if(channel==std::string("bbH"       )) title = std::string("gg#rightarrowbb#phi (ggH profiled)");
  if(channel==std::string("HIG-11-020")) title = std::string("HIG-11-020 (1.6 fb^{-1})");
  if(channel==std::string("HIG-11-029")) title = std::string("HIG-11-029 (4.9 fb^{-1})");
  if(channel==std::string("HIG-12-018")) title = std::string("HIG-12-018 (10 fb^{-1})");
  if(channel==std::string("HIG-12-032")) title = std::string("HIG-12-032 (5-10 fb^{-1})");
  if(channel==std::string("HIG-12-043")) title = std::string("HIG-12-043 (17 fb^{-1})");
  if(channel==std::string("HIG-12-050")) title = std::string("HIG-12-050 (17 fb^{-1})"); 
  return title;
}

void comparePValues(const char* filename, const char* channelstr, bool expected, bool observed, double minimum=1e-8, double maximum=1., bool log=true, const char* label="CMS Preliminary,  H#rightarrow#tau#tau,  4.9 fb^{-1} at 7 TeV, 19.8 fb^{-1} at 8 TeV", double legx0=0.2, double legy0=0.2, double legx1=0.6, double legy1=0.4)
{
  SetStyle();

  std::map<std::string, unsigned int> colors;
  colors["0jet"       ] = kBlue;
  colors["1jet"       ] = kRed;
  colors["2jet"       ] = kMagenta;
  colors["vbf"        ] = kRed;
  colors["boost"      ] = kGreen;
  colors["btag"       ] = kRed; 
  colors["nobtag"     ] = kBlue; 
  colors["em"         ] = kBlue;
  colors["et"         ] = kRed;
  colors["mt"         ] = kGreen;
  colors["mm"         ] = kMagenta;
  colors["ee"         ] = kCyan;
  colors["tt"         ] = kMagenta+3;
  colors["vhtt"       ] = kCyan-6;
  colors["cmb"        ] = kBlack;
  colors["htt"        ] = kBlack;
  colors["ggH"        ] = kRed;
  colors["bbH"        ] = kBlue;
  colors["HIG-11-020" ] = kBlue+2;
  colors["HIG-11-029" ] = kRed+2;
  colors["HIG-12-018" ] = kBlue;
  colors["HIG-12-032" ] = kRed+2;
  colors["HIG-12-043" ] = kRed;
  colors["HIG-12-050" ] = kRed;

  std::cout << " *******************************************************************************************************\n"
	    << " * Usage     : root -l                                                                                  \n"
	    << " *             .x MitLimits/Higgs2Tau/macros/comparePValues.C+(file, chn, exp, obs, type, min, max, log)\n"
	    << " *                                                                                                      \n"
	    << " * Arguments :  + file     const char*      full path to the input file                                 \n"
	    << " *              + chn      const char*      list of channels; choose between: 'cmb', 'htt', 'emu',      \n"
	    << " *                                          'etau', 'mutau', 'mumu', 'vhtt', 'hgg', 'hww', 'ggH',       \n"
	    << " *                                          'bbH', 'nomix[-200, +200]', 'mhmax[-400, -200, +200]'       \n"
	    << " *                                          'mhmax[+400, +600, +800]', 'test-0...5', 'saeff', 'gluph'   \n"
	    << " *                                          The list should be comma separated and may contain          \n"
	    << " *                                          whitespaces                                                 \n"
	    << " *              + exp       bool            compare expected limits                                     \n"
	    << " *              + obs       bool            compare observed limits                                     \n"
	    << " *              + type      const char*     type of plot; choose between 'sm-xsec', 'mssm-xsec' and     \n"
	    << " *                                          'mssm-tanb'                                                 \n"
	    << " *              + max       double          maximum of the plot (default is 20.)                        \n"
	    << " *                                                                                                      \n"
	    << " *              + min       double          minimum of the plot (default is  0.)                        \n"
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
  std::vector<TGraph*> hobs, hexp;
  for(unsigned i=0; i<channels.size(); ++i){
    if(observed) hobs.push_back(get<TGraph>(inputFile, std::string(channels[i]).append("/observed").c_str()));
    if(expected) hexp.push_back(get<TGraph>(inputFile, std::string(channels[i]).append("/expected").c_str()));
  }

  /// do the drawing
  TCanvas* canv1 = new TCanvas("canv1", "Limit Comparison", 600, 600);
  canv1->cd();
  canv1->SetGridx(1);
  canv1->SetGridy(1);

  bool firstPlot=true;
  for(unsigned int i=0; i<hexp.size(); ++i){
    if(firstPlot){
	if(log){ canv1->SetLogy(1); }
	hexp[i]->SetMaximum(maximum);
	hexp[i]->SetMinimum(minimum);
      
      // format x-axis
      std::string x_title;
      x_title = std::string("m_{H} [GeV]");
      hexp[i]->GetXaxis()->SetTitle(x_title.c_str());
      hexp[i]->GetXaxis()->SetLabelFont(62);
      hexp[i]->GetXaxis()->SetTitleFont(62);
      hexp[i]->GetXaxis()->SetTitleColor(1);
      hexp[i]->GetXaxis()->SetTitleOffset(1.05);
      hexp[i]->GetXaxis()->SetLimits(hexp[i]->GetX()[0]-.1, hexp[i]->GetX()[hexp[i]->GetN()-1]+.1);

      // format y-axis
      std::string y_title;
      y_title = std::string("Local p-Value");
      hexp[i]->GetYaxis()->SetTitle(y_title.c_str());
      hexp[i]->GetYaxis()->SetLabelFont(62);
      hexp[i]->GetYaxis()->SetTitleOffset(1.05);
      hexp[i]->GetYaxis()->SetLabelSize(0.03);
    }
    hexp[i]->SetLineStyle(11.);
    hexp[i]->SetLineWidth( 3.); 
    hexp[i]->SetLineColor(colors.find(channels[i])->second);
    hexp[i]->SetMarkerStyle(20);
    hexp[i]->SetMarkerSize(MARKER_SIZE);
    hexp[i]->SetMarkerColor(colors.find(channels[i])->second);
    hexp[i]->Draw(firstPlot ? "APL" : "PLsame");
    firstPlot=false;
  }
  for(unsigned int i=0; i<hobs.size(); ++i){
    if(firstPlot){
      if(log){ canv1->SetLogy(1); }
      hobs[i]->SetMaximum(maximum);
      hobs[i]->SetMinimum(minimum);
      
      // format x-axis
      std::string x_title;
      x_title = std::string("m_{H} [GeV]");
      hobs[i]->GetXaxis()->SetTitle(x_title.c_str());
      hobs[i]->GetXaxis()->SetLabelFont(62);
      hobs[i]->GetXaxis()->SetTitleFont(62);
      hobs[i]->GetXaxis()->SetTitleColor(1);
      hobs[i]->GetXaxis()->SetTitleOffset(1.05);
      hobs[i]->GetXaxis()->SetLimits(hobs[i]->GetX()[0]-.1, hobs[i]->GetX()[hobs[i]->GetN()-1]+.1);
      // format y-axis
      std::string y_title;
      y_title = std::string("Local p-value");
      hobs[i]->GetYaxis()->SetTitle(y_title.c_str());
      hobs[i]->GetYaxis()->SetLabelFont(62);
      hobs[i]->GetYaxis()->SetTitleOffset(1.05);
      hobs[i]->GetYaxis()->SetLabelSize(0.03);
    }
    hobs[i]->SetLineStyle(11.);
    hobs[i]->SetLineWidth( 3.); 
    hobs[i]->SetLineColor(colors.find(channels[i])->second);
    hobs[i]->SetMarkerStyle(20);
    hobs[i]->SetMarkerSize(MARKER_SIZE);
    hobs[i]->SetMarkerColor(colors.find(channels[i])->second);
    hobs[i]->Draw(firstPlot ? "APL" : "PLsame");
    firstPlot=false;
  }
  canv1->RedrawAxis();

  // create the unit line
  TGraph* unit = new TGraph();
  for(int idx=0; idx<hexp[0]->GetN(); ++idx){
    unit->SetPoint(idx, hexp[0]->GetX()[idx], 1.);
  }
  // create sigma lines
  std::vector<TGraph*> sigmas;
  for(unsigned int isigma=0; isigma<5; ++isigma){
    TGraph* sigma = new TGraph();
    for(int idx=0; idx<hexp[0]->GetN(); ++idx){
      sigma->SetPoint(idx, hexp[0]->GetX()[idx], ROOT::Math::normal_cdf_c(isigma+1));
    }
    sigmas.push_back(sigma);
  }

  unit->SetLineColor(kBlue);
  unit->SetLineWidth(3.);
  unit->Draw("Lsame");

  for(std::vector<TGraph*>::const_iterator sigma = sigmas.begin(); sigma!=sigmas.end(); ++sigma){
    (*sigma)->SetLineColor(kRed);
    (*sigma)->SetLineWidth(3.);
    (*sigma)->Draw("Lsame");
  }

  /// 5 sigma
  TPaveText * sigma5 = new TPaveText(0.96, 0.25, 1.00, 0.30, "NDC");
  sigma5->SetBorderSize(   0 );
  sigma5->SetFillStyle(    0 );
  sigma5->SetTextAlign(   12 );
  sigma5->SetTextSize ( 0.04 );
  sigma5->SetTextColor( kRed );
  sigma5->SetTextFont (   62 );
  sigma5->AddText("5#sigma");
  sigma5->Draw("same");

  /// 4 sigma
  TPaveText * sigma4 = new TPaveText(0.96, 0.45, 1.00, 0.50, "NDC");
  sigma4->SetBorderSize(   0 );
  sigma4->SetFillStyle(    0 );
  sigma4->SetTextAlign(   12 );
  sigma4->SetTextSize ( 0.04 );
  sigma4->SetTextColor( kRed );
  sigma4->SetTextFont (   62 );
  sigma4->AddText("4#sigma");
  sigma4->Draw("same");

  /// 3 sigma
  TPaveText * sigma3 = new TPaveText(0.96, 0.61, 1.00, 0.66, "NDC");
  sigma3->SetBorderSize(   0 );
  sigma3->SetFillStyle(    0 );
  sigma3->SetTextAlign(   12 );
  sigma3->SetTextSize ( 0.04 );
  sigma3->SetTextColor( kRed );
  sigma3->SetTextFont (   62 );
  sigma3->AddText("3#sigma");
  sigma3->Draw("same");

  /// 2 sigma
  TPaveText * sigma2 = new TPaveText(0.96, 0.73, 1.00, 0.78, "NDC");
  sigma2->SetBorderSize(   0 );
  sigma2->SetFillStyle(    0 );
  sigma2->SetTextAlign(   12 );
  sigma2->SetTextSize ( 0.04 );
  sigma2->SetTextColor( kRed );
  sigma2->SetTextFont (   62 );
  sigma2->AddText("2#sigma");
  sigma2->Draw("same"); 

  /// 1 sigma
  TPaveText * sigma1 = new TPaveText(0.96, 0.82, 1.00, 0.87, "NDC");
  sigma1->SetBorderSize(   0 );
  sigma1->SetFillStyle(    0 );
  sigma1->SetTextAlign(   12 );
  sigma1->SetTextSize ( 0.04 );
  sigma1->SetTextColor( kRed );
  sigma1->SetTextFont (   62 );
  sigma1->AddText("1#sigma");
  sigma1->Draw("same");

  CMSPrelim(label, "", 0.15, 0.835);

  TLegend* leg0 = new TLegend(legx0, legy0, legx1, legy1);
  leg0->SetTextSize(0.03);
  leg0->SetBorderSize( 0 );
  leg0->SetFillStyle ( 1001 );
  leg0->SetFillColor (kWhite);
  if(observed){
    for(unsigned int i=0; i<hobs.size(); ++i){
      leg0->AddEntry( hobs[i] , channel(channels[i]) ? legendEntry(channels[i]).c_str() : legendEntry(channels[i]).append("-Channel").c_str(),  "PL" );
    }
  }
  if(expected){
    for(unsigned int i=0; i<hexp.size(); ++i){
      leg0->AddEntry( hexp[i] , channel(channels[i]) ? legendEntry(channels[i]).c_str() : legendEntry(channels[i]).append("-Channel").c_str(),  "PL" );
    }
  }
  leg0->Draw("same");

  canv1->Print(std::string("singlePValues").append(expected ? "_expected" : "").append(observed ? "_observed.png" : ".png").c_str());
  canv1->Print(std::string("singlePValues").append(expected ? "_expected" : "").append(observed ? "_observed.pdf" : ".pdf").c_str());
  canv1->Print(std::string("singlePValues").append(expected ? "_expected" : "").append(observed ? "_observed.eps" : ".eps").c_str());
  return;
}
