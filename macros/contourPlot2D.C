#include <iostream>

#include "TROOT.h"
#include "TTree.h"
#include "TFile.h"
#include "TGraph.h"
#include "TString.h"
#include "TLegend.h"
#include "TCanvas.h"

#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"

void contourPlot2D(const char* path, const char* name, float xMax=20., float yMax=20., string typ="ggHbbH")
{
  SetStyle();

  TFile* file_ = TFile::Open(path);
  TGraph* exp  = (TGraph*) file_->Get(Form("%s_exp" , name));
  TGraph* cl68 = (TGraph*) file_->Get(Form("%s_cl68", name));
  TGraph* cl95 = (TGraph*) file_->Get(Form("%s_cl95", name));
  TGraph* fit  = (TGraph*) file_->Get(Form("%s_fit" , name));
  
  TCanvas* canv = new TCanvas("canv", "canv", 600, 600);
  canv->SetGridx(); canv->SetGridy();
  TH1F* hr = canv->DrawFrame(0., 0., xMax, yMax);
  if(typ=="ggHbbH")
    {
      hr->SetXTitle("#sigma(gg#rightarrow #phi)  (pb)");
    }
  else if(typ=="ggHqqH")
    {
      hr->SetXTitle("#sigma(gg#rightarrow H)  (pb)");
    }
  else if(typ=="cVcF")
    {
      hr->SetXTitle("#bf{cV}");
    }
  else
    {
      std::cout<< "Unknow typ " << typ << ". Possible typs: ggHbbH, ggHqqH, cVcF !" << std::endl;
    }
  hr->GetXaxis()->SetLabelFont(62);
  hr->GetXaxis()->SetTitleFont(62);
  hr->GetXaxis()->SetTitleColor(1);
  hr->GetXaxis()->SetTitleOffset(1.05);
  if(typ=="ggHbbH")
    {
      hr->SetYTitle("#bf{#sigma(gg#rightarrow bb#phi)  (pb)}");
    }
  else if(typ=="ggHqqH")
    {
      hr->SetYTitle("#bf{#sigma(qq#rightarrow H)  (pb)}");
    }
  else if(typ=="cVcF")
    {
      hr->SetYTitle("#bf{cF}");
    }
  else
    {
      std::cout<< "Unknow typ " << typ << ". Possible typs: ggHbbH, ggHqqH, cVcF !" << std::endl;
    }
  hr->GetYaxis()->SetNdivisions(505);
  hr->GetYaxis()->SetLabelFont(62);
  hr->GetYaxis()->SetTitleSize(0.05);
  hr->GetYaxis()->SetTitleOffset(1.35);
  hr->GetYaxis()->SetLabelSize(0.05);

  exp->SetMarkerSize(3.);
  exp->SetMarkerColor(2);
  exp ->Draw();
  cl95->Draw("Lsame");
  cl68->Draw("Lsame");
  fit->SetMarkerSize(3.);
  fit->SetMarkerColor(4);
  fit ->Draw("Psame");
  exp ->Draw("Psame");

  /// add the proper legend
  TLegend* leg = new TLegend(0.48, 0.70, 0.90, 0.90);
  leg->SetBorderSize( 0 );
  leg->SetFillStyle ( 0 );
  leg->SetFillColor (kWhite);
  //leg->SetHeader( "95% CL Limits" );
  leg->AddEntry( exp , "expected" ,  "P" );
  leg->AddEntry( fit , "best fit" ,  "P" );
  leg->AddEntry( cl68, "68% CL contour" ,  "L" );
  leg->AddEntry( cl95, "95% CL contour" ,  "L" );
  leg->Draw("same");

  canv->Print(Form("%s.png", name));
  canv->Print(Form("%s.eps", name));
  canv->Print(Form("%s.pdf", name));
}
