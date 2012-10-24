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

static const double MARKER_SIZE = 1.3;  // 0.7

bool
channel(std::string& label){
  return (label==std::string("cmb")        ||
	  label==std::string("htt")        ||
	  label==std::string("htt+")       ||
	  label==std::string("vhtt")       ||
	  label==std::string("whtt")       ||
	  label==std::string("zhtt")       ||
	  label==std::string("whhh")       ||
	  label==std::string("incl")       ||
	  label==std::string("0jet")       ||
	  label==std::string("2jet")       ||
	  label==std::string("boost")      ||
	  label==std::string("vbf")        ||
	  label==std::string("hgg")        ||	  
	  label==std::string("hww")        ||
	  label==std::string("tt")         ||
	  label==std::string("ltt") 	   ||
	  label==std::string("llt") 	   ||
	  label==std::string("4l") 	   ||
	  label==std::string("hzz4l")      ||
	  label==std::string("hzz2l2q")    ||
	  label==std::string("hzz2l2q")    ||
	  label==std::string("hzz2l2t")    ||
	  label==std::string("hzz2l2n")    ||
	  label==std::string("ggH")        ||
	  label==std::string("bbH")        ||
	  label==std::string("test-0")     ||
	  label==std::string("test-1")     ||
	  label==std::string("test-2")     ||
	  label==std::string("test-3")     ||
	  label==std::string("test-4")     ||
	  label==std::string("test-5")     ||
	  label==std::string("cmb-5fb")    ||
	  label==std::string("hpa-5fb")    ||
	  label==std::string("hpa-10fb")   ||
	  label==std::string("saeff")      ||
	  label==std::string("gluph")      ||
	  label==std::string("nomix-200")  ||
	  label==std::string("nomix+200")  ||
	  label==std::string("mhmax-400")  ||
	  label==std::string("mhmax-200")  ||
	  label==std::string("mhmax+200")  ||
	  label==std::string("mhmax+400")  ||
	  label==std::string("mhmax+600")  ||
	  label==std::string("mhmax+800")  ||
	  label==std::string("MSSM-7TeV")  ||
	  label==std::string("MSSM-8TeV")  ||
	  label==std::string("HIG-11-020") ||
	  label==std::string("HIG-11-029") ||
	  label==std::string("HIG-12-018") ||
	  label==std::string("HIG-12-032")
	  );
}

std::string legendEntry(const std::string& channel){
  std::string title;
  if(channel==std::string("emu"       )) title = std::string("e#mu");
  if(channel==std::string("em"        )) title = std::string("e#mu");
  if(channel==std::string("etau"      )) title = std::string("e#tau_{h}");
  if(channel==std::string("et"        )) title = std::string("e#tau_{h}");
  if(channel==std::string("mutau"     )) title = std::string("#mu#tau_{h}");
  if(channel==std::string("mt"        )) title = std::string("#mu#tau_{h}");
  if(channel==std::string("tautau"    )) title = std::string("#tau_{h}#tau_{h} (5 fb^{-1})");
  if(channel==std::string("tt"        )) title = std::string("#tau_{h}#tau_{h} (5 fb^{-1})");
  if(channel==std::string("mumu"      )) title = std::string("#mu#mu");
  if(channel==std::string("mm"        )) title = std::string("#mu#mu");
  if(channel==std::string("vhtt"      )) title = std::string("VH#rightarrow#tau#tau+l(l)");
  if(channel==std::string("whtt"      )) title = std::string("WH#rightarrow#tau_{l}#tau_{l}+l");
  if(channel==std::string("zhtt"      )) title = std::string("ZH#rightarrow#tau_{l}#tau_{l}+ll");
  if(channel==std::string("whhh"      )) title = std::string("WH#rightarrow#tau_{h}#tau_{h}+#mu");
  if(channel==std::string("htt"       )) title = std::string("e#mu+e#tau_{h}+#mu#tau_{h}+#mu#mu");
  if(channel==std::string("htt+"      )) title = std::string("e#mu+e#tau_{h}+#mu#tau_{h}+#mu#mu+#tau_{h}#tau_{h}");
  if(channel==std::string("cmb"       )) title = std::string("Combined");
  if(channel==std::string("incl"      )) title = std::string("Inclusive");
  if(channel==std::string("0jet"      )) title = std::string("0-Jet");
  if(channel==std::string("2jet"      )) title = std::string("V(jj)H(#tau#tau)");
  if(channel==std::string("vbf"       )) title = std::string("VBF");
  if(channel==std::string("boost"     )) title = std::string("Boost");
  if(channel==std::string("btag"      )) title = std::string("Btag");
  if(channel==std::string("hgg"       )) title = std::string("H#rightarrow#gamma#gamma");
  if(channel==std::string("hww"       )) title = std::string("H#rightarrowWW#rightarrow2l2#nu");
  if(channel==std::string("ltt"       )) title = std::string("WH#rightarrow#tau_{h}#tau_{h}+l");
  if(channel==std::string("llt"       )) title = std::string("WH#rightarrow#tau_{h}+2l (10 fb^{-1})");
  if(channel==std::string("4l"        )) title = std::string("ZH#rightarrow2l2#tau (10 fb^{-1})");
  if(channel==std::string("hzz4l"     )) title = std::string("H#rightarrowZZ#rightarrow4l");
  if(channel==std::string("hzz2l2q"   )) title = std::string("H#rightarrowZZ#rightarrow2l2q");
  if(channel==std::string("hzz2l2t"   )) title = std::string("H#rightarrowZZ#rightarrow2l2#tau");
  if(channel==std::string("hzz2l2n"   )) title = std::string("H#rightarrowZZ#rightarrow2l2#nu");
  if(channel==std::string("ggH"       )) title = std::string("gg#rightarrowH");
  if(channel==std::string("bbH"       )) title = std::string("bb#rightarrowHbb");
  if(channel==std::string("test-0"    )) title = std::string("Limit on 2011 Data");
  if(channel==std::string("test-1"    )) title = std::string("Limit on 2012 Data");
  if(channel==std::string("test-2"    )) title = std::string("Test-2");
  if(channel==std::string("test-3"    )) title = std::string("Test-3");
  if(channel==std::string("test-4"    )) title = std::string("Test-4");
  if(channel==std::string("test-5"    )) title = std::string("Test-5");
  if(channel==std::string("cmb-5fb"   )) title = std::string("All channels (5 fb^{-1})");
  if(channel==std::string("hpa-5fb"   )) title = std::string("HPA analyses (5 fb^{-1})");
  if(channel==std::string("hpa-10fb"  )) title = std::string("HPA analyses (10 fb^{-1})");
  if(channel==std::string("saeff"     )) title = std::string("small #alpha_{eff}");
  if(channel==std::string("gluph"     )) title = std::string("gluo-phobic");
  if(channel==std::string("nomix-200" )) title = std::string("no mixing (#mu=-200 GeV)");
  if(channel==std::string("nomix+200" )) title = std::string("no mixing (#mu=+200 GeV)");
  if(channel==std::string("mhmax-400" )) title = std::string("m_{h, max} (#mu=-400 GeV)");
  if(channel==std::string("mhmax-200" )) title = std::string("m_{h, max} (#mu=-200 GeV)");
  if(channel==std::string("mhmax+200" )) title = std::string("m_{h, max} (#mu=+200 GeV)");
  if(channel==std::string("mhmax+400" )) title = std::string("m_{h, max} (#mu=+400 GeV)");
  if(channel==std::string("mhmax+600" )) title = std::string("m_{h, max} (#mu=+600 GeV)");
  if(channel==std::string("mhmax+800" )) title = std::string("m_{h, max} (#mu=+800 GeV)");
  if(channel==std::string("MSSM-7TeV" )) title = std::string("ICHEP 7 TeV (4.9 fb^{-1})");
  if(channel==std::string("MSSM-8TeV" )) title = std::string("ICHEP 8 TeV (5.1 fb^{-1})");
  if(channel==std::string("HIG-11-020")) title = std::string("HIG-11-020 (1.6 fb^{-1})");
  if(channel==std::string("HIG-11-020")) title = std::string("HIG-11-020 (1.6 fb^{-1})");
  if(channel==std::string("HIG-11-029")) title = std::string("HIG-11-029 (4.9 fb^{-1})");
  if(channel==std::string("HIG-12-018")) title = std::string("HIG-12-018 (10 fb^{-1})");
  if(channel==std::string("HIG-12-032")) title = std::string("HIG-12-032 (5-10 fb^{-1})");
  if(channel==std::string("20121023.cmb_mssm_78TeV_cmb"       )) title = std::string("Combined");
  return title;
}

void compareLimits(const char* filename, const char* channelstr, bool expected, bool observed, const char* type, double minimum=0., double maximum=20., bool log=false, const char* label=" Preliminary, H#rightarrow#tau#tau, #sqrt{s} = 7-8 TeV, L=17 fb^{-1}", bool legendOnRight = true)
{
  SetStyle();

  std::map<std::string, unsigned int> colors;
  colors["incl"      ] = kBlue;
  colors["0jet"      ] = kBlue;
  colors["2jet"      ] = kMagenta;
  colors["vbf"       ] = kRed;
  colors["boost"     ] = kGreen;
  colors["btag"      ] = kRed;
  colors["emu"       ] = kBlue;
  colors["em"        ] = kBlue;
  colors["etau"      ] = kRed;
  colors["et"        ] = kRed;
  colors["mutau"     ] = kGreen;
  colors["mt"        ] = kGreen;
  colors["mumu"      ] = kMagenta;
  colors["mm"        ] = kMagenta;
  colors["tautau"    ] = kOrange;
  colors["tt"        ] = kOrange;
  colors["vhtt"      ] = kMagenta+2;
  colors["whtt"      ] = kMagenta+0;
  colors["zhtt"      ] = kCyan+2;
  colors["whhh"      ] = kBlue;
  colors["cmb"       ] = kBlack;
  colors["htt"       ] = kBlack;
  colors["htt+"      ] = kBlue;
  colors["hgg"       ] = kRed;
  colors["hww"       ] = kGreen;
  colors["4l"        ] = kGreen;
  colors["llt"       ] = kRed;
  colors["ltt"       ] = kBlue;
  colors["hzz4l"     ] = kBlue;
  colors["hzz2l2q"   ] = kMagenta;
  colors["hzz2l2q+"  ] = kMagenta;
  colors["hzz2l2t"   ] = kOrange;
  colors["hzz2l2n"   ] = kPink;
  colors["ggH"       ] = kRed;
  colors["bbH"       ] = kBlue;
  colors["test-0"    ] = kBlue+2;
  colors["test-1"    ] = kRed+2;
  colors["test-2"    ] = kGreen;
  colors["test-3"    ] = kRed+2;
  colors["test-4"    ] = kBlue;
  colors["test-5"    ] = kViolet-6;
  colors["cmb-5fb"   ] = kBlue;
  colors["hpa-5fb"   ] = kRed;
  colors["hpa-10fb"  ] = kBlack;
  colors["saeff"     ] = kGreen;
  colors["gluph"     ] = kOrange-3;
  colors["nomix-200" ] = kBlue-10;
  colors["nomix+200" ] = kBlue +2;
  colors["mhmax-400" ] = kGray +2;
  colors["mhmax-200" ] = kGray +1;
  colors["mhmax+200" ] = kMagenta+ 4;
  colors["mhmax+400" ] = kMagenta+ 3;
  colors["mhmax+600" ] = kMagenta- 2;
  colors["mhmax+800" ] = kMagenta-10;
  colors["MSSM-7TeV" ] = kBlue+2;
  colors["MSSM-8TeV" ] = kBlue+4;
  colors["HIG-11-020"] = kBlue+2;
  colors["HIG-11-029"] = kRed+2;
  colors["HIG-12-018"] = kBlue;
  colors["HIG-12-032"] = kRed+2;
  colors["20121023.cmb_mssm_78TeV_cmb"] = kBlack;

  std::cout << " *******************************************************************************************************\n"
	    << " * Usage     : root -l                                                                                  \n"
	    << " *             .x MitLimits/Higgs2Tau/macros/compareLimits.C+(file, chn, exp, obs, type, min, max, log) \n"
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
      if(std::string(type) == std::string("mssm-xsec")){
	if(log){ canv1->SetLogy(1); }
	hexp[i]->SetMaximum(maximum);
	hexp[i]->SetMinimum(minimum);
      }
      else{
	if(log){ canv1->SetLogy(1); }
	hexp[i]->SetMaximum(maximum);
	hexp[i]->SetMinimum(minimum);
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
      if(std::string(type) == std::string("mssm-tanb")) hexp[i]->GetYaxis()->SetRangeUser(0,70);

      // format y-axis
      std::string y_title;
      if( std::string(type) == std::string("mssm-xsec") ){
	y_title = std::string("#sigma(#phi#rightarrow#tau#tau)_{95% CL} [pb]");
      }
      else if(  std::string(type) == std::string("mssm-tanb")  ){
	y_title = std::string("#bf{tan#beta}");
      }
      else{
	//y_title = std::string("#sigma(H#rightarrow#tau#tau)_{95% CL} / #sigma(H#rightarrow#tau#tau)_{SM}");
	y_title = std::string("95% CL limit on #sigma/#sigma_{SM}");
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
    hexp[i]->SetMarkerSize(MARKER_SIZE);
    hexp[i]->SetMarkerColor(colors.find(channels[i])->second);
    hexp[i]->Draw(firstPlot ? "APL" : "PLsame");
    //hexp[i]->Draw(firstPlot ? "AL" : "Lsame");
    firstPlot=false;
  }
  for(unsigned int i=0; i<hobs.size(); ++i){
    if(firstPlot){
      if(std::string(type) == std::string("mssm-xsec")){
	if(log){ canv1->SetLogy(1); }
	hobs[i]->SetMaximum(maximum);
	hobs[i]->SetMinimum(minimum);
      }
      else{
	if(log){ canv1->SetLogy(1); }
	hobs[i]->SetMaximum(maximum);
	hobs[i]->SetMinimum(minimum);
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
      if(std::string(type) == std::string("mssm-tanb")) hexp[i]->GetYaxis()->SetRangeUser(0,70);
      
      // format y-axis
      std::string y_title;
      if( std::string(type) == std::string("mssm-xsec") ){
	y_title = std::string("#sigma(#phi#rightarrow#tau#tau)_{95% CL} [pb]");
      }
      else if(  std::string(type) == std::string("mssm-tanb")  ){
	y_title = std::string("#bf{tan#beta}");
      }
      else{
	//y_title = std::string("#sigma(H#rightarrow#tau#tau)_{95% CL} / #sigma(H#rightarrow#tau#tau)_{SM}");
	y_title = std::string("#sigma(H)_{95% CL} / #sigma(H)_{SM}");
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
    hobs[i]->SetMarkerSize(MARKER_SIZE);
    hobs[i]->SetMarkerColor(colors.find(channels[i])->second);
    hobs[i]->Draw(firstPlot ? "APL" : "PLsame");
    //hobs[i]->Draw(firstPlot ? "AL" : "Lsame");
    firstPlot=false;
  }
  canv1->RedrawAxis();

  bool firstLeg=true;
  if(observed){
    TLegend* leg1;
    if(expected && observed){
      /// setup the CMS Preliminary
       if(std::string(type) == std::string("mssm-tanb")){
	  if (firstLeg) CMSPrelim(label, "", 0.15, 0.835);
	  leg1 = new TLegend(firstLeg ? 0.60 : 0.20, hobs.size()<5 ? 0.20-0.06*hobs.size() : 0.4, firstLeg ? 0.93 : 0.60, 0.20);
       }
       else{
	  if (firstLeg) CMSPrelim(label, "", 0.15, 0.835);
	  leg1 = new TLegend(firstLeg ? 0.50 : 0.20, hobs.size()<5 ? 0.90-0.06*hobs.size() : 0.6, firstLeg ? 0.93 : 0.60, 0.90);
       }
    }
    else{
      /// setup the CMS Preliminary
       if(std::string(type) == std::string("mssm-tanb")){
	  CMSPrelim(label, "", 0.15, 0.835);
	  leg1 = new TLegend(firstLeg ? 0.60 : 0.20, hobs.size()<5 ? 0.20-0.06*hobs.size() : 0.4, firstLeg ? 0.93 : 0.63, 0.20);
       }
       else{
	  CMSPrelim(label, "", 0.15, 0.835);
	  leg1 = new TLegend(firstLeg ? 0.50 : 0.20, hobs.size()<5 ? 0.90-0.06*hobs.size() : 0.6, firstLeg ? 0.93 : 0.63, 0.90);
       }
    }
    leg1->SetTextSize(0.02);
    leg1->SetBorderSize( 0 );
    leg1->SetFillStyle ( 1001 );
    leg1->SetFillColor ( 0 );
    leg1->SetFillColor (kWhite);
    leg1->SetHeader( "#bf{Observed Limit}" );
    for(unsigned int i=0; i<hobs.size(); ++i){
      // skip one of the two split options
      if(channels[i] == std::string("hzz2l2q+")){ continue; }
      leg1->AddEntry( hobs[i] , channel(channels[i]) ? legendEntry(channels[i]).c_str() : legendEntry(channels[i]).append("-Channel").c_str(),  "PL" );
    }
    leg1->Draw("same");
    firstLeg=false;
  }
  if(expected){
    TLegend* leg0;
    if(expected && observed){
      /// setup the CMS Preliminary
      if(std::string(type) == std::string("mssm-tanb")){
	CMSPrelim(label, "", 0.15, 0.835);
	leg0 = new TLegend(legendOnRight ? 0.60 : 0.20, hexp.size()<5 ? 0.20-0.06*hexp.size() : 0.4, legendOnRight ? 0.94 : 0.63, 0.20);
      }
      else{
	CMSPrelim(label, "", 0.15, 0.835);
	leg0 = new TLegend(legendOnRight ? 0.50 : 0.20, hexp.size()<5 ? 0.90-0.06*hexp.size() : 0.6, legendOnRight ? 0.94 : 0.63, 0.90);
      }
    }
    else{
      /// setup the CMS Preliminary
      if(std::string(type) == std::string("mssm-tanb")){
	CMSPrelim(label, "", 0.15, 0.835);
	leg0 = new TLegend(legendOnRight ? 0.60 : 0.20, hexp.size()<5 ? 0.20-0.06*hexp.size() : 0.4, legendOnRight ? 0.94 : 0.63, 0.20);
	   }
      else{
	CMSPrelim(label, "", 0.15, 0.835);
	leg0 = new TLegend(legendOnRight ? 0.50 : 0.20, hexp.size()<5 ? 0.90-0.06*hexp.size() : 0.6, legendOnRight ? 0.94 : 0.63, 0.90);
      }
    }
    if(std::string(type) == std::string("mssm-tanb")) {leg0->SetTextSize(0.03);}
    leg0->SetBorderSize( 0 );
    leg0->SetFillStyle ( 1001 );
    leg0->SetFillColor (kWhite);
    leg0->SetHeader( "#bf{Expected Limit}" );
    for(unsigned int i=0; i<hexp.size(); ++i){
      // skip one of the two split options
      if(channels[i] == std::string("hzz2l2q+")){ continue; }
      leg0->AddEntry( hexp[i] , channel(channels[i]) ? legendEntry(channels[i]).c_str() : legendEntry(channels[i]).append("-Channel").c_str(),  "PL" );
    }
    leg0->Draw("same");
    firstLeg=false;
  }
  canv1->Print(std::string("singleLimits").append(expected ? "_expected" : "").append(observed ? "_observed" : "").append(std::string(type).find("mssm")!=std::string::npos ? "_mssm.png" : "_sm.png").c_str());
  canv1->Print(std::string("singleLimits").append(expected ? "_expected" : "").append(observed ? "_observed" : "").append(std::string(type).find("mssm")!=std::string::npos ? "_mssm.pdf" : "_sm.pdf").c_str());
  canv1->Print(std::string("singleLimits").append(expected ? "_expected" : "").append(observed ? "_observed" : "").append(std::string(type).find("mssm")!=std::string::npos ? "_mssm.pdf" : "_sm.eps").c_str());
  return;
}
