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

void compareLimitsWithBand(const char* filename, const char* channelstr, double minimum=0., double maximum=5., const char* type="sm-xsec", bool log=false, const char* label="#scale[1.5]{CMS}   h,H,A#rightarrow#tau#tau                     19.7 fb^{-1} (8 TeV) + 4.9 fb^{-1} (7 TeV)", bool addExpected=true, bool addObserved=false, bool ggH=true)
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
	    << " *              + type      const char*     type of plot; choose between 'sm-xsec', 'mssm-xsec' and            \n"
	    << " *                                          'mssm-tanb'                                                        \n"
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
    if(i==1) observed.push_back(get<TGraph>(inputFile, std::string(channels[i]).append("/observed").c_str()));
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
  if((std::string(type) == std::string("mssm-xsec") || std::string(type) == std::string("mssm-tanb")) && log) canv->SetLogx(1); 
  canv->SetLogy(log);
  canv->cd();
  // canv->SetGridx(1);
//   canv->SetGridy(1);

  // for logx the label for x axis values below 100 needs to be slightly shifted to prevent 
  // the label from being printed into the canvas
  int shift_label = 1.;
  if((std::string(type) == std::string("mssm-xsec") || std::string(type) == std::string("mssm-tanb")) && log ){
    if(observed[0]) { observed[0]->GetX()[0] = observed[0]->GetX()[0]+0.01; }
    if(expected[0]->GetX()[0]<100.){ shift_label = -1.; }
  }
  // draw a frame to define the range
  TH1F* hr=canv->DrawFrame(expected[0]->GetX()[0]-shift_label*.01, minimum, expected[0]->GetX()[expected[0]->GetN()-1]+.01, maximum);
  std::string x_title;
  if(std::string(type) == std::string("mssm-tanb")){
    x_title = std::string("m_{A} [GeV]");
  }
  else if(std::string(type) == std::string("mssm-xsec")){
    x_title = std::string("m_{#phi} [GeV]");
  }
  else{
    x_title = std::string("m_{H} [GeV]");
  }
  hr->SetXTitle(x_title.c_str());
  hr->GetXaxis()->SetTitle(x_title.c_str());
  hr->GetXaxis()->SetLabelFont(62);
  hr->GetXaxis()->SetTitleFont(62);
  hr->GetXaxis()->SetTitleColor(1);
  hr->GetXaxis()->SetTitleOffset(1.05);
  if((std::string(type) == std::string("mssm-xsec") || std::string(type) == std::string("mssm-tanb")) && log){
    hr->GetXaxis()->SetNdivisions(50005, "X");
    hr->GetXaxis()->SetMoreLogLabels();
    hr->GetXaxis()->SetNoExponent();
    hr->GetXaxis()->SetLabelSize(0.040);
  }
  std::string y_title;
  if( std::string(type) == std::string("mssm-xsec") ){
    if(ggH) y_title = std::string("95% CL limit on #sigma#font[42]{(gg#phi)}#upoint#font[52]{B}#font[42]{(#phi#rightarrow#tau#tau)} [pb]");
    else y_title = std::string("95% CL limit on #sigma#font[42]{(bb#phi)}#upoint#font[52]{B}#font[42]{(#phi#rightarrow#tau#tau)} [pb]");
  }
  else if(  std::string(type) == std::string("mssm-tanb")  ){
    y_title = std::string("#bf{tan#beta}");
  }
  else{
    y_title = std::string("95% CL limit on #sigma/#sigma_{SM}");
  }
  hr->SetYTitle(y_title.c_str());
  hr->GetYaxis()->SetLabelFont(62);
  hr->GetYaxis()->SetTitleFont(62);
  hr->GetYaxis()->SetTitleOffset(1.05);
  hr->GetYaxis()->SetLabelSize(0.03);

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
    for(unsigned int idx=0; idx<expected.size(); ++idx){
      expected[idx]->SetLineColor(idx==0 ? kBlack : kRed+2);
      expected[idx]->SetLineWidth(3);
      expected[idx]->SetLineStyle(idx==0 ? 11 : 11);
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
  if( std::string(type) == std::string("sm-xsec") ) unit->Draw("Lsame");

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
    //observed[0]->Draw("PLsame");
  }
  /// setup the CMS Preliminary
  CMSPrelim(label, "", 0.145, 0.835);

  TGraph* SMexpectation = new TGraph();  
  //SMexpectation->SetPoint(0,125,0.2035*0.06319); //8TeV: bbH=0.2035 ggH=19.27         
  if(ggH) SMexpectation->SetPoint(0,125,49.47*0.06319); //14TeV: bbH=0.5805  ggH=49.47 
  else SMexpectation->SetPoint(0,125,0.5805*0.06319);
  SMexpectation->SetMarkerColor(kBlue);
  SMexpectation->SetMarkerSize(2.0);
  SMexpectation->SetMarkerStyle(34);
  if( std::string(type) == std::string("mssm-xsec") ) SMexpectation->Draw("PLsame");

  /// add the proper legend
  TLegend* leg = new TLegend(0.35, 0.65, 0.90, 0.90);
  if(std::string(type) == std::string("mssm-xsec")) leg = new TLegend(0.35, 0.70, 0.95, 0.90);
  leg->SetBorderSize( 0 );
  leg->SetFillStyle ( 1001 );
  //leg->SetTextSize ( 0.025 );
  leg->SetFillColor (kWhite);
  //leg->SetHeader( "95% CL Limits" );
  //leg->AddEntry( observed[0] , "observed 14TeV, 300/fb", "PL");
  leg->AddEntry( expected[0] , "Expected 14TeV, 300/fb",  "L" );
  leg->AddEntry( innerBand[0], "#pm 1#sigma Expected" ,  "F" );
  leg->AddEntry( outerBand[0], "#pm 2#sigma Expected" ,  "F" );
  leg->Draw("same");
  
  TLegend* leg0 = new TLegend(0.18, 0.22, 0.78, 0.34);
  leg0->SetBorderSize( 0 );
  leg0->SetFillStyle ( 1001 );
  //leg0->SetTextSize ( 0.025 );
  leg0->SetFillColor (kWhite);
  //leg0->AddEntry( observed[0] , "arXiv:1408.3316 observed (scaled to 14 TeV)",  "PL" );
  if(addExpected) { 
    leg0->AddEntry( expected[1] , "arXiv:1408.3316 expected",  "L" );
    leg0->AddEntry((TObject*)0, "(8 TeV scaled to 14 TeV)", "");
    //leg0->AddEntry((TObject*)0, "", "");
  }
  if(addObserved | addExpected) leg0->Draw("same");

  TLegend* leg1 = new TLegend(0.18, 0.15, 0.78, 0.19);
  leg1->SetBorderSize( 0 );
  leg1->SetFillStyle ( 1001 );
  //leg1->SetTextSize ( 0.025 );
  leg1->SetFillColor (kWhite);
  if( std::string(type) == std::string("mssm-xsec") && ggH)  leg1->AddEntry( SMexpectation, "gg #rightarrow h_{SM} (m_{H}=125 GeV, 14 TeV)" ,  "P" );
  if( std::string(type) == std::string("mssm-xsec") && !ggH) leg1->AddEntry( SMexpectation, "bb #rightarrow h_{SM} (m_{H}=125 GeV, 14 TeV)" ,  "P" );
  if(addObserved | addExpected) leg1->Draw("same");
  //canv.RedrawAxis("g");
  canv->RedrawAxis();

  canv->Print(std::string("CompareWithBand.png").c_str());
  canv->Print(std::string("CompareWithBand.pdf").c_str());
  canv->Print(std::string("CompareWithBand.eps").c_str());

  return;
}
