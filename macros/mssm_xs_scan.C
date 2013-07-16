#include <iostream>

#include "HiggsAnalysis/HiggsToTauTau/macros/mssm_xs_tools.h"
#include "HiggsAnalysis/HiggsToTauTau/macros/mssm_xs_tools.C"

#include "TTree.h"
#include "TFile.h"
#include "TAxis.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TPaveLabel.h"
#include "TGraphAsymmErrors.h"
#include <string>    

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"
#include "HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"

void 
mssm_xs_scan(char* path, double mA, double tanbmax)
{
  mssm_xs_tools xs;
  xs.SetInput(path);

  TGraph *SM = new TGraph();
  TGraph *ggH = new TGraph();
  TGraph *bbH = new TGraph();
  TGraph *ggA = new TGraph();
  TGraph *bbA = new TGraph();
  TGraph *ggh = new TGraph();
  TGraph *bbh = new TGraph();

  double xs_eff_ggH[4];
  double xs_eff_bbH[4];
  for(int tanb=1; tanb<=tanbmax; tanb++){

    SM->SetPoint(tanb-1, tanb, 1.21*1000);

    std::cout << "MSSM Cross Section [ggH]:" << std::endl;
    xs_eff_ggH[0] = xs.Give_Xsec_ggFA(mA, tanb)*xs.Give_BR_A_tautau(mA, tanb);
    std::cout << " -> xsec(ggA):\t" << xs.Give_Xsec_ggFA(mA, tanb) << "\t --- \t" << xs.Give_BR_A_tautau(mA, tanb) << std::endl;
    xs_eff_ggH[1] = xs.Give_Xsec_ggFH(mA, tanb)*xs.Give_BR_H_tautau(mA, tanb);
    std::cout << " -> xsec(ggH):\t" << xs.Give_Xsec_ggFH(mA, tanb) << "\t --- \t" << xs.Give_BR_H_tautau(mA, tanb) << std::endl;
    xs_eff_ggH[2] = xs.Give_Xsec_ggFh(mA, tanb)*xs.Give_BR_h_tautau(mA, tanb);
    std::cout << " -> xsec(ggh):\t" << xs.Give_Xsec_ggFh(mA, tanb) << "\t --- \t" << xs.Give_BR_h_tautau(mA, tanb) << std::endl;
    xs_eff_ggH[3] = (xs_eff_ggH[0]+xs_eff_ggH[1]+xs_eff_ggH[2]);//*1.237; 
    std::cout << "mA: "<< mA << "  tanb: "<<tanb<<" -> ggH_xsec(cmb):\t" << xs_eff_ggH[3] << std::endl;

    ggA->SetPoint(tanb-1, tanb, xs_eff_ggH[0]);
    ggH->SetPoint(tanb-1, tanb, xs_eff_ggH[1]);
    ggh->SetPoint(tanb-1, tanb, xs_eff_ggH[2]);

    std::cout << "MSSM Cross Section [bbH]:" << std::endl;
    xs_eff_bbH[0] = xs.GiveXsec_Santander_A(mA, tanb)*xs.Give_BR_A_tautau(mA, tanb);
    std::cout << " -> xsec(ggA):\t" << xs.GiveXsec_Santander_A(mA, tanb) << "\t --- \t" << xs.Give_BR_A_tautau(mA, tanb) << std::endl;
    xs_eff_bbH[1] = xs.GiveXsec_Santander_H(mA, tanb)*xs.Give_BR_H_tautau(mA, tanb);
    std::cout << " -> xsec(bbH):\t" << xs.GiveXsec_Santander_H(mA, tanb) << "\t --- \t" << xs.Give_BR_H_tautau(mA, tanb) << std::endl;
    xs_eff_bbH[2] = xs.GiveXsec_Santander_h(mA, tanb)*xs.Give_BR_h_tautau(mA, tanb);
    std::cout << " -> xsec(ggh):\t" << xs.GiveXsec_Santander_h(mA, tanb) << "\t --- \t" << xs.Give_BR_h_tautau(mA, tanb) << std::endl;
    xs_eff_bbH[3] = (xs_eff_bbH[0]+xs_eff_bbH[1]+xs_eff_bbH[2]);//*1.627;
    std::cout << "mA: "<< mA << "  tanb: "<<tanb<<"  -> bbH_xsec(cmb):\t" << xs_eff_bbH[3] << std::endl;
    std::cout << std::endl;

    bbA->SetPoint(tanb-1, tanb, xs_eff_bbH[0]);
    bbH->SetPoint(tanb-1, tanb, xs_eff_bbH[1]);
    bbh->SetPoint(tanb-1, tanb, xs_eff_bbH[2]);
    
  }
  /// do the drawing
  TCanvas* canv1 = new TCanvas("canv1", "xs*BR", 600, 600);
  canv1->cd();
  //canv1->SetGridx(1);
  //canv1->SetGridy(1);
  canv1->SetLogy(1);

  // draw a frame to define the range
  TH1F* hr=canv1->DrawFrame(ggA->GetX()[0]-.01, 0.0001, ggA->GetX()[ggA->GetN()-1]+.01, 10000);
  // format x axis
  hr->SetXTitle("tan#beta");
  hr->GetXaxis()->SetLabelSize(0.045);
  hr->GetXaxis()->SetTitleFont(62);
  hr->GetXaxis()->SetLabelFont(62);
  hr->GetXaxis()->SetTitleColor(1);
  hr->GetXaxis()->SetTitleOffset(1.08);
  // format y axis
  hr->SetYTitle("#sigma #times BR [fb]");
  hr->GetXaxis()->SetTitleFont(62);
  hr->GetYaxis()->SetLabelFont(62);
  hr->GetYaxis()->SetLabelSize(0.045);
  hr->GetYaxis()->SetTitleOffset(1.3);
  hr->GetXaxis()->SetTitleColor(1);
  hr->SetNdivisions(505, "X");

  ggA->Draw("PLsame");
  ggA->SetLineStyle(3.);
  ggA->SetLineWidth(2.); 
  ggA->SetLineColor(kBlue);
  ggA->SetMarkerStyle(23);
  ggA->SetMarkerSize(0);
  ggA->SetMarkerColor(kBlue);

  ggH->Draw("PLsame");
  ggH->SetLineStyle(2.);
  ggH->SetLineWidth(2.); 
  ggH->SetLineColor(kBlue);
  ggH->SetMarkerStyle(22);
  ggH->SetMarkerSize(0);
  ggH->SetMarkerColor(kBlue);

  ggh->Draw("PLsame");
  ggh->SetLineStyle(1.);
  ggh->SetLineWidth(2.); 
  ggh->SetLineColor(kBlue);
  ggh->SetMarkerStyle(20);
  ggh->SetMarkerSize(0);
  ggh->SetMarkerColor(kBlue);

  bbA->Draw("PLsame");
  bbA->SetLineStyle(3.);
  bbA->SetLineWidth(2.); 
  bbA->SetLineColor(kRed);
  bbA->SetMarkerStyle(23);
  bbA->SetMarkerSize(0);
  bbA->SetMarkerColor(kRed);

  bbH->Draw("PLsame");
  bbH->SetLineStyle(2.);
  bbH->SetLineWidth(2.); 
  bbH->SetLineColor(kRed);
  bbH->SetMarkerStyle(22);
  bbH->SetMarkerSize(0);
  bbH->SetMarkerColor(kRed);

  bbh->Draw("PLsame");
  bbh->SetLineStyle(1.);
  bbh->SetLineWidth(2.); 
  bbh->SetLineColor(kRed);
  bbh->SetMarkerStyle(20);
  bbh->SetMarkerSize(0);
  bbh->SetMarkerColor(kRed);

  SM->Draw("PLsame");
  SM->SetLineStyle(8.);
  SM->SetLineWidth(3.); 
  SM->SetLineColor(kGreen+1);
  SM->SetMarkerStyle(20);
  SM->SetMarkerSize(0);
  SM->SetMarkerColor(kGreen+1); 

  TLegend* leg0;
  /// setup the CMS Preliminary
  //std::ostringstream ss;
  //ss << mA;
  //std::string s(ss.str());
  std::string mass = std::to_string((int)mA);
  CMSPrelim(std::string("#sigma #times BR [fb],   m^{h}_{max} scenario,  m_{A} = " + mass + " GeV").c_str(), "", 0.15, 0.835);
  leg0 = new TLegend(0.68, 0.12, 0.90, 0.32); 
  leg0->SetBorderSize( 0 );
  leg0->SetFillStyle ( 1001 );
  leg0->SetFillColor (kWhite);
  //leg0->SetHeader( "#sigma #times BR" );
  leg0->AddEntry( SM,  "ggH_{SM} #rightarrow #tau#tau",  "PL" );
  leg0->AddEntry( ggh, "ggh #rightarrow #tau#tau",  "PL" );
  leg0->AddEntry( ggA, "ggA #rightarrow #tau#tau",  "PL" );
  leg0->AddEntry( ggH, "ggH #rightarrow #tau#tau",  "PL" );
  leg0->AddEntry( bbh, "bbh #rightarrow #tau#tau",  "PL" );
  leg0->AddEntry( bbA, "bbA #rightarrow #tau#tau",  "PL" );
  leg0->AddEntry( bbH, "bbH #rightarrow #tau#tau",  "PL" );
  leg0->Draw("same");
  
  canv1->Print("xsBR.png");
  canv1->Print("xsBR.pdf");
return;
}
