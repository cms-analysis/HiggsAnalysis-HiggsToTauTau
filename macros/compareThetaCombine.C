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

static const double MARKER_SIZE = 0.7;  // 0.7

bool
channel(std::string& label){
  return (label==std::string("cmb")        ||
	  label==std::string("cmb-mvis")   ||
	  label==std::string("cmb-ichep")  ||
	  label==std::string("cmb+")       ||
	  label==std::string("htt")        ||
	  label==std::string("htt+")       ||
	  label==std::string("vhtt")       ||
	  label==std::string("whtt")       ||
	  label==std::string("zhtt")       ||
	  label==std::string("whhh")       ||
	  label==std::string("incl")       ||
	  label==std::string("0jet")       ||
	  label==std::string("0jet-mvis")  ||
	  label==std::string("0jet-ichep") ||
	  label==std::string("2jet")       ||
	  label==std::string("boost")      ||
	  label==std::string("boost+0jet") ||
	  label==std::string("boost-mvis") ||
	  label==std::string("boost-ichep")||
	  label==std::string("btag")       ||
	  label==std::string("nobtag")     ||
	  label==std::string("vbf")        ||
	  label==std::string("vbf_0jet")   ||
	  label==std::string("vbf-mvis")   ||
	  label==std::string("vbf-ichep")  ||
	  label==std::string("hgg")        ||	  
	  label==std::string("hww")        ||
	  label==std::string("hbb")        ||	  
	  label==std::string("hmm")        ||
	  label==std::string("tt")         ||
	  label==std::string("tt-mvis")    ||
	  label==std::string("tt-ichep")   ||
	  label==std::string("em")         ||
	  label==std::string("em-mvis")    ||
	  label==std::string("em-ichep")   ||
	  label==std::string("et")         ||
	  label==std::string("et-mvis")    ||
	  label==std::string("et-ichep")   ||
	  label==std::string("mt")         ||
	  label==std::string("mt-mvis")    ||
	  label==std::string("mt-ichep")   ||
	  label==std::string("mm")         ||
	  label==std::string("mm-mvis")    ||
	  label==std::string("mm-ichep")   ||
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
	  label==std::string("mvis")       ||
	  label==std::string("ichep")      ||
	  label==std::string("test-0")     ||
	  label==std::string("test-1")     ||
	  label==std::string("test-2")     ||
	  label==std::string("test-3")     ||
	  label==std::string("test-4")     ||
	  label==std::string("test-5")     ||
	  label==std::string("old")        ||
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
	  label==std::string("HIG-12-032") ||
	  label==std::string("HIG-12-043") ||
	  label==std::string("HIG-12-050")
	  );
}

std::string legendEntry(const std::string& channel){
  std::string title;
  if(channel==std::string("emu"       )) title = std::string("e#mu");
  if(channel==std::string("em"        )) title = std::string("e#mu");
  if(channel==std::string("em-mvis"   )) title = std::string("e#mu (with m_{vis})");
  if(channel==std::string("em-ichep"  )) title = std::string("e#mu (HCP on ICHEP dataset)");
  if(channel==std::string("etau"      )) title = std::string("e#tau_{h}");
  if(channel==std::string("et"        )) title = std::string("e#tau_{h}");
  if(channel==std::string("et-mvis"   )) title = std::string("e#tau_{h} (with m_{vis})");
  if(channel==std::string("et-ichep"  )) title = std::string("e#tau_{h} (HCP in ICHEP dataset)");
  if(channel==std::string("mutau"     )) title = std::string("#mu#tau_{h}");
  if(channel==std::string("mt"        )) title = std::string("#mu#tau_{h}");
  if(channel==std::string("mt-mvis"   )) title = std::string("#mu#tau_{h} (with m_{vis})");
  if(channel==std::string("mt-ichep"  )) title = std::string("#mu#tau_{h} (HCP on ICHEP dataset)");
  if(channel==std::string("tautau"    )) title = std::string("#tau_{h}#tau_{h}");
  if(channel==std::string("tt"        )) title = std::string("#tau_{h}#tau_{h}");
  if(channel==std::string("tt-mvis"   )) title = std::string("#tau_{h}#tau_{h} (with m_{vis})");
  if(channel==std::string("tt-ichep"  )) title = std::string("#tau_{h}#tau_{h} (HCP on ICHEP dataset)");
  if(channel==std::string("mumu"      )) title = std::string("#mu#mu");
  if(channel==std::string("mm"        )) title = std::string("#mu#mu");
  if(channel==std::string("mm-mvis"   )) title = std::string("#mu#mu (with m_{vis})");
  if(channel==std::string("mm-ichep"  )) title = std::string("#mu#mu (HCP on ICHEP dataset)");
  if(channel==std::string("vhtt"      )) title = std::string("VH#rightarrow#tau#tau+l(l)");
  if(channel==std::string("whtt"      )) title = std::string("WH#rightarrow#tau_{l}#tau_{l}+l");
  if(channel==std::string("zhtt"      )) title = std::string("ZH#rightarrow#tau_{l}#tau_{l}+ll");
  if(channel==std::string("whhh"      )) title = std::string("WH#rightarrow#tau_{h}#tau_{h}+#mu");
  if(channel==std::string("htt"       )) title = std::string("e#mu+e#tau_{h}+#mu#tau_{h}+#mu#mu");
  if(channel==std::string("htt+"      )) title = std::string("e#mu+e#tau_{h}+#mu#tau_{h}+#mu#mu+#tau_{h}#tau_{h}");
  if(channel==std::string("cmb"       )) title = std::string("Combined");
  if(channel==std::string("cmb-mvis"  )) title = std::string("Combined (with m_{vis})");
  if(channel==std::string("cmb-ichep" )) title = std::string("Combined (HCP on ICHEP dataset)");
  if(channel==std::string("cmb+"      )) title = std::string("H#rightarrow#tau#tau + VH#rightarrow#tau#tau+l");
  if(channel==std::string("incl"      )) title = std::string("Inclusive");
  if(channel==std::string("0jet"      )) title = std::string("0-Jet");
  if(channel==std::string("0jet-mvis" )) title = std::string("0-Jet (with m_{vis})");
  if(channel==std::string("0jet-ichep")) title = std::string("0-Jet (HCP on ICHEP dataset)");
  if(channel==std::string("2jet"      )) title = std::string("V(jj)H(#tau#tau)");
  if(channel==std::string("vbf"       )) title = std::string("2-Jet (VBF) ICHEP analysis");
  if(channel==std::string("vbf+0jet"  )) title = std::string("2-Jet (VBF)");
  if(channel==std::string("vbf-mvis"  )) title = std::string("2-Jet (VBF) (with m_{vis})");
  if(channel==std::string("vbf-ichep" )) title = std::string("2-Jet (VBF) HCP analysis");
  if(channel==std::string("boost"     )) title = std::string("1-Jet");
  if(channel==std::string("boost+0jet")) title = std::string("1-Jet");
  if(channel==std::string("boost-mvis")) title = std::string("1-Jet (with m_{vis})");
  if(channel==std::string("boost-ichep")) title = std::string("1-Jet (HCP on ICHEP dataset)");
  if(channel==std::string("btag"      )) title = std::string("B-Tag");
  if(channel==std::string("nobtag"    )) title = std::string("No B-Tag");
  if(channel==std::string("hgg"       )) title = std::string("H#rightarrow#gamma#gamma");
  if(channel==std::string("hww"       )) title = std::string("H#rightarrowWW#rightarrow2l2#nu");
  if(channel==std::string("hmm"       )) title = std::string("H#rightarrow#mu#mu");
  if(channel==std::string("hbb"       )) title = std::string("H#rightarrowbb");
  if(channel==std::string("ltt"       )) title = std::string("WH#rightarrow#tau_{h}#tau_{h}+l");
  if(channel==std::string("llt"       )) title = std::string("WH#rightarrow#tau_{h}+2l");
  if(channel==std::string("4l"        )) title = std::string("ZH#rightarrow2l2#tau");
  if(channel==std::string("ltt"       )) title = std::string("WH#rightarrow#tau_{h}#tau_{h}");
  if(channel==std::string("llt"       )) title = std::string("WH#rightarrow#tau_{h}+2l (10 fb^{-1})");
  if(channel==std::string("4l"        )) title = std::string("ZH#rightarrow2l2#tau (10 fb^{-1})");
  if(channel==std::string("hzz4l"     )) title = std::string("H#rightarrowZZ#rightarrow4l");
  if(channel==std::string("hzz2l2q"   )) title = std::string("H#rightarrowZZ#rightarrow2l2q");
  if(channel==std::string("hzz2l2t"   )) title = std::string("H#rightarrowZZ#rightarrow2l2#tau");
  if(channel==std::string("hzz2l2n"   )) title = std::string("H#rightarrowZZ#rightarrow2l2#nu");
  if(channel==std::string("ggH"       )) title = std::string("gg#rightarrow#phi (bbH profiled)");
  if(channel==std::string("bbH"       )) title = std::string("gg#rightarrowbb#phi (ggH profiled)");
  if(channel==std::string("mvis"      )) title = std::string("Visible mass");
  if(channel==std::string("ichep"     )) title = std::string("On ICHEP dataset");
  if(channel==std::string("test-0"    )) title = std::string("gg#rightarrow#phi (bbH set to 0)");
  if(channel==std::string("test-1"    )) title = std::string("gg#rightarrowbb#phi (ggH set to 0)");
  if(channel==std::string("test-2"    )) title = std::string("gg#rightarrowbb#phi (w/o prefit)");
  if(channel==std::string("test-3"    )) title = std::string("gg#rightarrow#phi (w/o prefit)");
  if(channel==std::string("test-4"    )) title = std::string("Test-4");
  if(channel==std::string("test-5"    )) title = std::string("Test-5");
  if(channel==std::string("old"       )) title = std::string("Old Limit");
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
  if(channel==std::string("HIG-12-043")) title = std::string("HIG-12-043 (17 fb^{-1})");
  if(channel==std::string("HIG-12-050")) title = std::string("HIG-12-050 (17 fb^{-1})");
  return title;
}

void compareThetaCombine(const char* filename, const char* channelstr, double minimum=0., double maximum=20., bool log=false, const char* label=" Preliminary, H#rightarrow#tau#tau, L=24.3 fb^{-1}")
{
  SetStyle();

  std::map<std::string, unsigned int> colors;
  colors["incl"       ] = kBlue;
  colors["0jet"       ] = kBlue;
  colors["0jet-mvis"  ] = kBlue+2;
  colors["0jet-ichep" ] = kBlue+2;
  colors["2jet"       ] = kMagenta;
  colors["vbf"        ] = kRed;
  colors["vbf+0jet"   ] = kRed;
  colors["vbf-mvis"   ] = kRed+2;
  colors["vbf-ichep"  ] = kRed+2;
  colors["boost"      ] = kGreen;
  colors["boost+0jet" ] = kGreen;
  colors["boost-mvis" ] = kGreen+2;
  colors["boost-ichep"] = kGreen+2;
  colors["btag"       ] = kRed;
  colors["nobtag"     ] = kBlue;
  colors["emu"        ] = kBlue;
  colors["em"         ] = kBlue;
  colors["em-mvis"    ] = kBlue+2;
  colors["em-ichep"   ] = kBlue+2;
  colors["etau"       ] = kRed;
  colors["et"         ] = kRed;
  colors["et-mvis"    ] = kRed+2;
  colors["et-ichep"   ] = kRed+2;
  colors["mutau"      ] = kGreen;
  colors["mt"         ] = kGreen;
  colors["mt-mvis"    ] = kGreen+2;
  colors["mt-ichep"   ] = kGreen+2;
  colors["mumu"       ] = kMagenta;
  colors["mm"         ] = kMagenta;
  colors["mm-mvis"    ] = kMagenta+2;
  colors["mm-ichep"   ] = kMagenta+2;
  colors["tautau"     ] = kOrange;
  colors["tt"         ] = kOrange;
  colors["tt-mvis"    ] = kOrange+2;
  colors["tt-ichep"   ] = kOrange+2;
  colors["vhtt"       ] = kMagenta+2;
  colors["whtt"       ] = kMagenta+0;
  colors["zhtt"       ] = kCyan+2;
  colors["whhh"       ] = kBlue;
  colors["cmb"        ] = kBlack;
  colors["cmb-mvis"   ] = kGray+2;
  colors["cmb-ichep"  ] = kGray+3;
  colors["cmb+"       ] = kGray+2;
  colors["htt"        ] = kBlack;
  colors["htt+"       ] = kBlue;
  colors["hgg"        ] = kRed;
  colors["hww"        ] = kGreen;
  colors["hbb"        ] = kOrange;
  colors["hmm"        ] = kViolet;
  colors["4l"         ] = kGreen;
  colors["llt"        ] = kRed;
  colors["ltt"        ] = kBlue;
  colors["hzz4l"      ] = kBlue;
  colors["hzz2l2q"    ] = kMagenta;
  colors["hzz2l2q+"   ] = kMagenta;
  colors["hzz2l2t"    ] = kOrange;
  colors["hzz2l2n"    ] = kPink;
  colors["ggH"        ] = kRed;
  colors["bbH"        ] = kBlue;
  colors["mvis"       ] = kBlue+2;
  colors["ichep"      ] = kBlue+2;
  colors["test-0"     ] = kRed+2;
  colors["test-1"     ] = kGreen+2;
  colors["test-2"     ] = kGreen;
  colors["test-3"     ] = kRed+2;
  colors["test-4"     ] = kBlue;
  colors["test-5"     ] = kViolet-6;
  colors["old"        ] = kViolet-6;
  colors["cmb-5fb"    ] = kBlue;
  colors["hpa-5fb"    ] = kRed;
  colors["hpa-10fb"   ] = kBlack;
  colors["saeff"      ] = kGreen;
  colors["gluph"      ] = kOrange-3;
  colors["nomix-200"  ] = kBlue-10;
  colors["nomix+200"  ] = kBlue +2;
  colors["mhmax-400"  ] = kGray +2;
  colors["mhmax-200"  ] = kGray +1;
  colors["mhmax+200"  ] = kMagenta+ 4;
  colors["mhmax+400"  ] = kMagenta+ 3;
  colors["mhmax+600"  ] = kMagenta- 2;
  colors["mhmax+800"  ] = kMagenta-10;
  colors["MSSM-7TeV"  ] = kBlue+2;
  colors["MSSM-8TeV"  ] = kBlue+4;
  colors["HIG-11-020" ] = kBlue+2;
  colors["HIG-11-029" ] = kRed+2;
  colors["HIG-12-018" ] = kBlue;
  colors["HIG-12-032" ] = kRed+2;
  colors["HIG-12-043" ] = kBlack;
  colors["HIG-12-050" ] = kBlack;

  std::cout << " *******************************************************************************************************\n"
	    << " * Usage     : root -l                                                                                  \n"
	    << " *             .x MitLimits/Higgs2Tau/macros/compareLimits.C+(file, chn, min, max, log) \n"
	    << " *                                                                                                      \n"
	    << " * Arguments :  + file     const char*      full path to the input file                                 \n"
	    << " *              + chn      const char*      list of channels; choose between: 'cmb', 'htt', 'em',       \n"

	    << " *                                          'et', 'mt', 'mm', 'vhtt', 'hgg', 'hww', 'ggH',              \n"
	    << " *                                          'bbH', 'nomix[-200, +200]', 'mhmax[-400, -200, +200]'       \n"
	    << " *                                          'mhmax[+400, +600, +800]', 'test-0...5', 'saeff', 'gluph'   \n"
	    << " *                                          The list should be comma separated and may contain          \n"
	    << " *                                          whitespaces                                                 \n"
	    << " *                                                                                                      \n"
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
  std::vector<TH1F*> hexp;
  for(unsigned i=0; i<channels.size(); ++i){
    hexp.push_back(get<TH1F>(inputFile, std::string(channels[i]).append("/plot1D_125").c_str()));
  }

  /// do the drawing
  TCanvas* canv1 = new TCanvas("canv1", "Best Fit Comparison", 600, 600);
  canv1->cd();
  canv1->SetGridx(1);
  canv1->SetGridy(1);
 
  bool firstPlot=true;
  for(unsigned int i=0; i<hexp.size(); ++i){
    if(firstPlot){
      if(log){ canv1->SetLogy(1); }
      // format x-axis
      std::string x_title;
      //x_title = std::string("#sigma#timesBR/#sigma#timesBR_{SM}");
      x_title = std::string("#mu");
      hexp[i]->SetXTitle(x_title.c_str());
      hexp[i]->GetXaxis()->SetTitleFont(62);
      hexp[i]->GetXaxis()->SetLabelFont(62);
      hexp[i]->GetXaxis()->SetTitleColor(1);
      hexp[i]->GetXaxis()->SetTitleOffset(1.05);

      // format y-axis
      std::string y_title;
      y_title = std::string("nll"); 
      hexp[i]->SetYTitle(y_title.c_str());
      hexp[i]->GetXaxis()->SetTitleFont(62);
      hexp[i]->GetYaxis()->SetLabelFont(62);
      //hexp[i]->GetYaxis()->SetTitleSize(0.05);
      hexp[i]->GetYaxis()->SetTitleOffset(1.05);
      hexp[i]->GetYaxis()->SetLabelSize(0.03);

      hexp[i]->GetXaxis()->SetRangeUser(0, 2);

      hexp[i]->SetMaximum(maximum);
      hexp[i]->SetMinimum(minimum);
      }  
    hexp[i]->SetLineStyle(11.);
    hexp[i]->SetLineWidth(3.); 
    hexp[i]->SetLineColor(kBlue); 
    hexp[i]->SetMarkerStyle(20);
    hexp[i]->SetMarkerSize(MARKER_SIZE);
    hexp[i]->SetMarkerColor(kBlue);
    hexp[i]->Draw(firstPlot ? "PL": "PLsame");
    firstPlot=false;  
  }

  TGraph* theta_graph = new TGraph();
  int n=-1; // first entry is off
  ifstream in ("theta/htt/nll.txt");
  while (in) {
    string line;
    getline (in, line);
    if (!in) break;
    float x;
    float y;
    sscanf (line.c_str(),"%f %f", &x, &y); 
    //std::cout << n << " " << x << " " << y << std::endl;
    if(n>-1) theta_graph->SetPoint(n, x, y);
    n++;
  }
  theta_graph->SetLineStyle(11.);
  theta_graph->SetLineWidth( 3.); 
  theta_graph->SetLineColor(kRed);
  theta_graph->SetMarkerStyle(29);
  theta_graph->SetMarkerSize(MARKER_SIZE);
  theta_graph->SetMarkerColor(kRed);
  theta_graph->Draw("PLsame");

  canv1->RedrawAxis();


  TLegend* leg0;
  CMSPrelim(label, "", 0.15, 0.835);
  leg0 = new TLegend(0.30, 0.60, 0.70, 0.80);
  leg0->SetBorderSize( 0 );
  leg0->SetFillStyle ( 1001 );
  leg0->SetFillColor (kWhite);
  leg0->SetHeader( "nll scan" );
  for(unsigned int i=0; i<hexp.size(); ++i){
    leg0->AddEntry( hexp[i] , "combine",  "PL" );
  }
  leg0->AddEntry( theta_graph, "theta", "PL");
  leg0->Draw("same");
  
  canv1->Print(std::string("Theta-Combine").append("_sm.png").c_str());
  canv1->Print(std::string("Theta-Combine").append("_sm.pdf").c_str());
  canv1->Print(std::string("Theta-Combine").append("_sm.eps").c_str());
  return;
}
