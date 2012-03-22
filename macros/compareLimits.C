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

bool
channel(std::string& label){
  return (label==std::string("cmb")        ||
	  label==std::string("htt")        ||
	  label==std::string("vhtt")       ||
	  label==std::string("incl")       ||
	  label==std::string("boost")      ||
	  label==std::string("vbf")        ||
	  label==std::string("hgg")        ||	  
	  label==std::string("hww")        ||
	  label==std::string("ggH")        ||
	  label==std::string("bbH")        ||
	  label==std::string("nomix+200")  ||
	  label==std::string("nomix-200")  ||
	  label==std::string("mhmax+200")  ||
	  label==std::string("mhmax-200")  ||
	  label==std::string("HIG-11-020") ||
	  label==std::string("HIG-11-029")
	  );
}

std::string legendEntry(const std::string& channel){
  std::string title;
  if(channel==std::string("emu"       )) title = std::string("e#mu");
  if(channel==std::string("etau"      )) title = std::string("e#tau_{h}");
  if(channel==std::string("mutau"     )) title = std::string("#mu#tau_{h}");
  if(channel==std::string("mumu"      )) title = std::string("#mu#mu");
  if(channel==std::string("vhtt"      )) title = std::string("VH#rightarrow#tau#tau+lep (vhtt)");
  if(channel==std::string("htt"       )) title = std::string("(e#mu + e#tau_{h} + #mu#tau)");
  if(channel==std::string("cmb"       )) title = std::string("Combined");
  if(channel==std::string("incl"      )) title = std::string("Inclusive");
  if(channel==std::string("vbf"       )) title = std::string("0/1-Jet+VBF");
  if(channel==std::string("boost"     )) title = std::string("0/1-Jet+Boost");
  if(channel==std::string("hgg"       )) title = std::string("H#rightarrow#gamma#gamma");
  if(channel==std::string("hww"       )) title = std::string("H#rightarrowWW#rightarrow 2lep 2#nu");
  if(channel==std::string("ggH"       )) title = std::string("gg#rightarrowH");
  if(channel==std::string("bbH"       )) title = std::string("bb#rightarrowHbb");
  if(channel==std::string("nomix+200" )) title = std::string("no mixing (#mu=+200 GeV)");
  if(channel==std::string("nomix-200" )) title = std::string("no mixing (#mu=-200 GeV)");
  if(channel==std::string("mhmax+200" )) title = std::string("m_{h, max} (#mu=+200 GeV)");
  if(channel==std::string("mhmax-200" )) title = std::string("m_{h, max} (#mu=-200 GeV)");
  if(channel==std::string("HIG-11-020")) title = std::string("Combined");
  if(channel==std::string("HIG-11-029")) title = std::string("Combined");
  return title;
}

void compareLimits(const char* filename, const char* channelstr, bool expected, bool observed, const char* type, double maximum=20.)
{
  SetStyle();

  std::map<std::string, unsigned int> colors;
  colors["incl"      ] = kBlue;
  colors["vbf"       ] = kRed;
  colors["boost"     ] = kGreen;
  colors["emu"       ] = kBlue;
  colors["etau"      ] = kRed;
  colors["mutau"     ] = kGreen;
  colors["mumu"      ] = kMagenta;
  colors["vhtt"      ] = kMagenta+2;
  colors["cmb"       ] = kBlack;
  colors["htt"       ] = kGray+2;
  colors["hgg"       ] = kRed;
  colors["hww"       ] = kGreen;
  colors["ggH"       ] = kRed;
  colors["bbH"       ] = kBlue;
  colors["nomix+200" ] = kBlue;
  colors["nomix-200" ] = kBlue-10;
  colors["mhmax+200" ] = kBlack;
  colors["mhmax-200" ] = kGray+1;
  colors["HIG-11-020"] = kBlack;
  colors["HIG-11-029"] = kBlack;

  std::cout << " ****************************************************************************************************\n"
	    << " * Usage     : root -l                                                                               \n"
	    << " *             .x MitLimits/Higgs2Tau/macros/compareLimits.C+(file, chn, exp, obs, type, max)        \n"
	    << " *                                                                                                   \n"
	    << " * Arguments :  + file     const char*      full path to the input file                              \n"
	    << " *              + chn      const char*      list of channels; choose between: 'cmb', 'htt', 'emu',   \n"
	    << " *                                          'etau', 'mutau', 'mumu', 'vhtt', 'hgg', 'hww', 'ggH',    \n"
	    << " *                                          'bbH', 'nomix+/-200', 'mhmax+/-200'                      \n"
	    << " *                                          The list should be comma separated and may contain       \n"
	    << " *                                          whitespaces                                              \n"
	    << " *              + exp       bool            compare expected limits                                  \n"
	    << " *              + obs       bool            compare observed limits                                  \n"
	    << " *              + mssm      const char*     type of plot; choose between 'sm-xsec', 'mssm-xsec' and  \n"
	    << " *                                          'mssm-tanb'                                              \n"
	    << " *              + max       double          maximumof the plot (default is 20.)                      \n"
	    << " *                                                                                                   \n"
	    << " ****************************************************************************************************\n";

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
      if(std::string(type) == std::string("mssm-xsec")){
	canv1->SetLogy(1);
	hexp[i]->SetMaximum(maximum);
	hexp[i]->SetMinimum(0.05);
      }
      else{
	hexp[i]->SetMaximum(maximum);
	hexp[i]->SetMinimum(0.);
      }
      
      // format x-axis
      std::string x_title;
      if(std::string(type).find("mssm")!=std::string::npos){
	x_title = std::string("m_{A} [GeV]");
      }
      else{
	x_title = std::string("m_{H} [GeV]");
      }
      hexp[i]->GetXaxis()->SetTitle(x_title.c_str());
      hexp[i]->GetXaxis()->SetLabelFont(62);
      hexp[i]->GetXaxis()->SetTitleFont(62);
      hexp[i]->GetXaxis()->SetTitleColor(1);
      hexp[i]->GetXaxis()->SetTitleOffset(1.05);
      
      // format y-axis
      std::string y_title;
      if( std::string(type) == std::string("mssm-xsec") ){
	y_title = std::string("#sigma(#phi#rightarrow#tau#tau)_{95% CL} [pb]");
      }
      else if(  std::string(type) == std::string("mssm-tanb")  ){
	y_title = std::string("#bf{tan#beta}");
      }
      else{
	y_title = std::string("#sigma(H#rightarrow#tau#tau)_{95% CL} / #sigma(H#rightarrow#tau#tau)_{SM}");
      }
      hexp[i]->GetYaxis()->SetTitle(y_title.c_str());
      hexp[i]->GetYaxis()->SetLabelFont(62);
      hexp[i]->GetYaxis()->SetTitleOffset(1.05);
      hexp[i]->GetYaxis()->SetLabelSize(0.03);
      hexp[i]->GetXaxis()->SetLimits(hexp[i]->GetX()[0]-.1, hexp[i]->GetX()[hexp[i]->GetN()-1]+.1);
    }
    hexp[i]->SetLineStyle(11.);
    hexp[i]->SetLineWidth( 3.); 
    hexp[i]->SetLineColor(colors.find(channels[i])->second);
    hexp[i]->SetMarkerStyle(20);
    hexp[i]->SetMarkerSize(1.3);
    hexp[i]->SetMarkerColor(colors.find(channels[i])->second);
    hexp[i]->Draw(firstPlot ? "APL" : "PLsame");
    firstPlot=false;
  }
  for(unsigned int i=0; i<hobs.size(); ++i){
    if(firstPlot){
      if(std::string(type) == std::string("mssm-xsec")){
	canv1->SetLogy(1);
	hobs[i]->SetMaximum(maximum);
	hobs[i]->SetMinimum(0.05);
      }
      else{
	hobs[i]->SetMaximum(maximum);
	hobs[i]->SetMinimum(0.);
      }
      
      // format x-axis
      std::string x_title;
      if(std::string(type).find("mssm")!=std::string::npos){
	x_title = std::string("m_{A} [GeV]");
      }
      else{
	x_title = std::string("m_{H} [GeV]");
      }
      hobs[i]->GetXaxis()->SetTitle(x_title.c_str());
      hobs[i]->GetXaxis()->SetLabelFont(62);
      hobs[i]->GetXaxis()->SetTitleFont(62);
      hobs[i]->GetXaxis()->SetTitleColor(1);
      hobs[i]->GetXaxis()->SetTitleOffset(1.05);
      
      // format y-axis
      std::string y_title;
      if( std::string(type) == std::string("mssm-xsec") ){
	y_title = std::string("#sigma(#phi#rightarrow#tau#tau)_{95% CL} [pb]");
      }
      else if(  std::string(type) == std::string("mssm-tanb")  ){
	y_title = std::string("#bf{tan#beta}");
      }
      else{
	y_title = std::string("#sigma(H#rightarrow#tau#tau)_{95% CL} / #sigma(H#rightarrow#tau#tau)_{SM}");
      }
      hobs[i]->GetYaxis()->SetTitle(y_title.c_str());
      hobs[i]->GetYaxis()->SetLabelFont(62);
      hobs[i]->GetYaxis()->SetTitleOffset(1.05);
      hobs[i]->GetYaxis()->SetLabelSize(0.03);
      hobs[i]->GetXaxis()->SetLimits(hobs[i]->GetX()[0]-.1, hobs[i]->GetX()[hobs[i]->GetN()-1]+.1);
    }
    hobs[i]->SetLineWidth( 3.); 
    hobs[i]->SetLineColor(colors.find(channels[i])->second);
    hobs[i]->SetMarkerStyle(20);
    hobs[i]->SetMarkerSize(1.3);
    hobs[i]->SetMarkerColor(colors.find(channels[i])->second);
    hobs[i]->Draw(firstPlot ? "APL" : "PLsame");
    firstPlot=false;
  }
  canv1->RedrawAxis();

  bool firstLeg=true;
  if(observed){
    TLegend* leg1;
    if(expected && observed){
      /// setup the CMS Preliminary
      if (firstLeg) CMSPrelim(" Preliminary #sqrt{s} = 7 TeV, L = 4.6 fb^{-1}", "", 0.15, 0.835);
      leg1 = new TLegend(firstLeg ? 0.60 : 0.20, hobs.size()<5 ? 0.90-0.06*hobs.size() : 0.6, firstLeg ? 0.93 : 0.60, 0.90);
    }
    else{
      /// setup the CMS Preliminary
      CMSPrelim(" Preliminary #sqrt{s} = 7 TeV, L = 4.6 fb^{-1}", "", 0.15, 0.835);
      leg1 = new TLegend(0.50, hobs.size()<5 ? 0.90-0.06*hobs.size() : 0.6, 0.93, 0.90);
    }
    leg1->SetBorderSize( 0 );
    leg1->SetFillStyle ( 0 );
    leg1->SetFillColor ( 0 );
    leg1->SetFillColor (kWhite);
    leg1->SetHeader( "Observed Limit" );
    for(unsigned int i=0; i<hobs.size(); ++i){
      leg1->AddEntry( hobs[i] , channel(channels[i]) ? legendEntry(channels[i]).c_str() : legendEntry(channels[i]).append("-Channel").c_str(),  "PL" );
    }
    leg1->Draw("same");
    firstLeg=false;
  }
  if(expected){
    TLegend* leg0;
    if(expected && observed){
      /// setup the CMS Preliminary
      if (firstLeg) CMSPrelim(" Preliminary #sqrt{s} = 7 TeV, L = 4.6 fb^{-1}", "", 0.15, 0.835);
      leg0 = new TLegend(firstLeg ? 0.60 : 0.20, hexp.size()<5 ? 0.90-0.06*hexp.size() : 0.8, firstLeg ? 0.94 : 0.60, 0.90);
    }
    else{
      /// setup the CMS Preliminary
      CMSPrelim(" Preliminary #sqrt{s} = 7 TeV, L = 4.6 fb^{-1}", "", 0.15, 0.835);
      leg0 = new TLegend(0.50, hexp.size()<5 ? 0.90-0.06*hexp.size() : 0.6, 0.94, 0.90);
    }
    leg0->SetBorderSize( 0 );
    leg0->SetFillStyle ( 0 );
    leg0->SetFillColor (kWhite);
    leg0->SetHeader( "Expected Limit" );
    for(unsigned int i=0; i<hexp.size(); ++i){
      leg0->AddEntry( hexp[i] , channel(channels[i]) ? legendEntry(channels[i]).c_str() : legendEntry(channels[i]).append("-Channel").c_str(),  "PL" );
    }
    leg0->Draw("same");
    firstLeg=false;
  }
  canv1->Print(std::string("singleLimits").append(expected ? "_expected" : "").append(observed ? "_observed" : "").append(std::string(type).find("mssm")!=std::string::npos ? "_mssm.png" : "_sm.png").c_str());
  canv1->Print(std::string("singleLimits").append(expected ? "_expected" : "").append(observed ? "_observed" : "").append(std::string(type).find("mssm")!=std::string::npos ? "_mssm.pdf" : "_sm.pdf").c_str());
  return;
}
