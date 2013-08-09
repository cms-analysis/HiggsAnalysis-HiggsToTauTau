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
#include <Riostream.h>
#include <TH1F.h>

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"
#include "HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"

static const double MARKER_SIZE = 1.3;  // 0.7



TH1F* ConvertGraphToHisto(TGraph *pGraph){
  // takes data from a graph, determines binning and fills data into histogram
  Int_t NPoints = pGraph->GetN();
  Double_t BinLimits[NPoints+1];
  // sort graph
  pGraph->Sort();
  // determine lower limit of histogram: half the distance to next point
  Double_t x0,x1,y;
  pGraph->GetPoint(0,x0,y);
  pGraph->GetPoint(1,x1,y);
  Double_t Distance = TMath::Abs(x0-x1);
  BinLimits[0] = x0 - Distance/2.;
  // now set upper limits for all the other points
  for (Int_t k = 0 ; k<NPoints-1;k++){
    pGraph->GetPoint(k,x0,y);
    pGraph->GetPoint(k+1,x1,y);
    Distance = TMath::Abs(x0-x1);
    BinLimits[k+1] = x0 + Distance/2.;}
  // for the last point set upper limit similar to first point:
  pGraph->GetPoint(NPoints-2,x0,y);
  pGraph->GetPoint(NPoints-1,x1,y);
  Distance = TMath::Abs(x0-x1);
  BinLimits[NPoints] = x1 + Distance/2.;
  // now we know the binning and can create the histogram:
  TString Name = "ConvertedHisto"; 
  // make name unique 
  Name+= rand();
  TH1F *ThisHist = new TH1F(Name,"",NPoints,BinLimits);
  // now fill the histogram
  for (Int_t i = 0; i<pGraph->GetN();i++){
    Double_t xi,yi;
    pGraph->GetPoint(i,xi,yi);
    ThisHist->SetBinContent(i+1,yi);}
  return ThisHist;
}

bool
channel(std::string& label){
  return (label==std::string("std")        ||
	  label==std::string("pruneds0p3")     ||
	  label==std::string("pruneds0p2")     ||
	  label==std::string("pruneds05p1")     ||
	  label==std::string("bin-by-bin-BBs0") ||
	  label==std::string("bin-by-bin-BBs05") ||
	  label==std::string("bbb")        ||
	  label==std::string("cmb")        ||
	  label==std::string("cmb+")       ||
	  label==std::string("htt")        ||
	  label==std::string("vhtt")       ||
	  label==std::string("0jet")       ||
	  label==std::string("2jet")       ||
	  label==std::string("boost")      ||
	  label==std::string("btag")       ||
	  label==std::string("nobtag")     ||
	  label==std::string("vbf")        ||
	  label==std::string("tt")         ||
	  label==std::string("em")         ||
	  label==std::string("et")         ||
	  label==std::string("mt")         ||
	  label==std::string("mm")         ||
	  label==std::string("ee")         ||
	  label==std::string("ggH")        ||
	  label==std::string("bbH")        ||
	  label==std::string("mvis")       ||
	  label==std::string("test-0")     ||
	  label==std::string("test-1")     ||
	  label==std::string("test-2")     ||
	  label==std::string("test-3")     ||
	  label==std::string("test-4")     ||
	  label==std::string("test-5")     ||
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
  if(channel==std::string("std"       )) title = std::string("no bbb");
  if(channel==std::string("pruneds05p1"   )) title = std::string("bbb stat>0.05 pruned<0.1");
  if(channel==std::string("pruneds0p2"    )) title = std::string("bbb stat>0 pruned<0.2");
  if(channel==std::string("pruneds0p3"    )) title = std::string("bbb stat>0 pruned<0.3");
  if(channel==std::string("bin-by-bin-BBs0"       )) title = std::string("merged bbb stat>0");
  if(channel==std::string("bin-by-bin-BBs05"      )) title = std::string("merged bbb stat>0.05");
  if(channel==std::string("bbb"       )) title = std::string("full bbb");
  if(channel==std::string("em"        )) title = std::string("e#mu");
  if(channel==std::string("et"        )) title = std::string("e#tau_{h}");
  if(channel==std::string("mt"        )) title = std::string("#mu#tau_{h}");
  if(channel==std::string("tt"        )) title = std::string("#tau_{h}#tau_{h}");
  if(channel==std::string("mm"        )) title = std::string("#mu#mu");
  if(channel==std::string("ee"        )) title = std::string("ee");
  if(channel==std::string("vhtt"      )) title = std::string("VH#rightarrow#tau#tau+l(l)");
  if(channel==std::string("htt"       )) title = std::string("e#mu+e#tau_{h}+#mu#tau_{h}+#mu#mu");
  if(channel==std::string("cmb"       )) title = std::string("Combined(H#rightarrow#tau#tau)");
  if(channel==std::string("cmb+"      )) title = std::string("H#rightarrow#tau#tau + VH#rightarrow#tau#tau+l(l)");
  if(channel==std::string("0jet"      )) title = std::string("0 jet");
  if(channel==std::string("2jet"      )) title = std::string("V(jj)H(#tau#tau)");
  if(channel==std::string("vbf"       )) title = std::string("2 jet (VBF)");
  if(channel==std::string("boost"     )) title = std::string("1 jet");
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

void compareLimitsRelative(const char* filename, const char* channelstr, bool expected, bool observed, const char* type, double minimum=0., double maximum=20., bool log=false, const char* label="CMS Preliminary,  H#rightarrow#tau#tau,  4.9 fb^{-1} at 7 TeV, 19.8 fb^{-1} at 8 TeV", bool legendOnRight=true, bool legendOnTop=true)
{
  SetStyle();

  std::map<std::string, unsigned int> colors;
  colors["std"        ] = kMagenta;
  colors["pruneds0p3"     ] = kGreen;
  colors["pruneds0p2"     ] = kOrange;
  colors["pruneds05p1"     ] = kRed;
  colors["bin-by-bin-BBs0"        ] = kBlue;
  colors["bin-by-bin-BBs05"        ] = kCyan;
  colors["bbb"        ] = kBlack;
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
  colors["ee"         ] = kCyan;
  colors["tt"         ] = kMagenta+3;
  colors["vhtt"       ] = kCyan-6;
  colors["cmb"        ] = kBlack;
  colors["cmb+"       ] = kBlack; //kGray+2;
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

  std::cout << " *******************************************************************************************************\n"
	    << " * Usage     : root -l                                                                                  \n"
	    << " * .x HiggsAnalysis/HiggsToTauTau/macros/compareLimitsRelative.C+(file,chn,exp,obs,type,min,max,log)    \n"
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
  std::vector<TH1F*> hobs, hexp;
  for(unsigned i=0; i<channels.size(); ++i){
    if(observed) hobs.push_back(ConvertGraphToHisto(get<TGraph>(inputFile, std::string(channels[i]).append("/observed").c_str()))); 
    if(expected) hexp.push_back(ConvertGraphToHisto(get<TGraph>(inputFile, std::string(channels[i]).append("/expected").c_str()))); 
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
      if(std::string(type) == std::string("mssm-tanb")) hexp[i]->GetYaxis()->SetRangeUser(minimum,maximum);

      // format y-axis
      std::string y_title;
      y_title = std::string("relative difference to no bbb");
      hexp[i]->GetYaxis()->SetTitle(y_title.c_str());
      hexp[i]->GetYaxis()->SetLabelFont(62);
      hexp[i]->GetYaxis()->SetTitleOffset(1.05);
      hexp[i]->GetYaxis()->SetLabelSize(0.03);
    }
    hexp[i]->Add(hexp[hexp.size()-1], -1); hexp[i]->Divide(hexp[hexp.size()-1]); hexp[i]->Scale(-1);
    hexp[i]->SetLineStyle(11.);
    hexp[i]->SetLineWidth( 3.); 
    hexp[i]->SetLineColor(colors.find(channels[i])->second);
    hexp[i]->SetMarkerStyle(20);
    hexp[i]->SetMarkerSize(MARKER_SIZE);
    hexp[i]->SetMarkerColor(colors.find(channels[i])->second);
    hexp[i]->Draw(firstPlot ? "PL" : "PLsame");
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
      if(std::string(type) == std::string("mssm-tanb")) hobs[i]->GetYaxis()->SetRangeUser(minimum,maximum);
      
      // format y-axis
      std::string y_title;
      y_title = std::string("relative difference to no bbb");
      hobs[i]->GetYaxis()->SetTitle(y_title.c_str());
      hobs[i]->GetYaxis()->SetLabelFont(62);
      hobs[i]->GetYaxis()->SetTitleOffset(1.05);
      hobs[i]->GetYaxis()->SetLabelSize(0.03);
    }
    hobs[i]->Add(hobs[hobs.size()-1], -1); hobs[i]->Divide(hobs[hexp.size()-1]); hobs[i]->Scale(-1);
    hobs[i]->SetLineStyle(11.);
    hobs[i]->SetLineWidth( 3.); 
    hobs[i]->SetLineColor(colors.find(channels[i])->second);
    hobs[i]->SetMarkerStyle(20);
    hobs[i]->SetMarkerSize(MARKER_SIZE);
    hobs[i]->SetMarkerColor(colors.find(channels[i])->second);
    hobs[i]->Draw(firstPlot ? "PL" : "PLsame");
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
	  leg1 = new TLegend(firstLeg ? 0.20 : 0.20, hobs.size()<5 ? 0.90-0.08*hobs.size() : 0.6, firstLeg ? 0.63 : 0.60, 0.90);
       }
    }
    else{
      /// setup the CMS Preliminary
      if(std::string(type) == std::string("mssm-tanb")){
	CMSPrelim(label, "", 0.15, 0.835);
	leg1 = new TLegend(legendOnRight?0.60:0.20, hobs.size()<5 ? (legendOnTop?0.90:0.20)-0.06*hobs.size() : (legendOnTop?0.6:0.4), legendOnRight?0.94:0.45, (legendOnTop?0.90:0.20));
	   }
      else{
	CMSPrelim(label, "", 0.15, 0.835);
	leg1 = new TLegend(legendOnRight ? 0.50 : 0.20, hobs.size()<5 ? 0.90-0.08*hobs.size() : 0.6, legendOnRight ? 0.94 : 0.64, 0.90);
      }
    }
    leg1->SetBorderSize( 0 );
    leg1->SetFillStyle ( 1001 );
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
	leg0 = new TLegend(legendOnRight ? 0.20 : 0.20, hexp.size()<5 ? 0.75-0.08*hexp.size() : 0.6, legendOnRight ? 0.94 : 0.63, 0.75);
      }
    }
    else{
      /// setup the CMS Preliminary
      if(std::string(type) == std::string("mssm-tanb")){
	CMSPrelim(label, "", 0.15, 0.835);
	leg0 = new TLegend(legendOnRight?0.60:0.20, hexp.size()<5 ? (legendOnTop?0.90:0.40)-0.04*hexp.size() : (legendOnTop?0.6:0.2), legendOnRight?0.94:0.45, (legendOnTop?0.90:0.40));
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
  canv1->Print(std::string("singleLimits").append(expected ? "_expected" : "").append(observed ? "_observed" : "").append(std::string(type).find("mssm")!=std::string::npos ? "_mssm.eps" : "_sm.eps").c_str());
  return;
}

