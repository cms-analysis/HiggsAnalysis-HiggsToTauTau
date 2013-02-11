#include "TH1F.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TPaveText.h"

void
plotting1DScan(TCanvas& canv, TH1F* plot1D, std::string& xaxis, std::string& yaxis, std::string& masslabel, int mass, double max, int lowerBin, int upperBin, bool log=false)
{
  // set up styles
  canv.cd();
  canv.SetGridx(1);
  canv.SetGridy(1);
  canv.SetRightMargin(0.14);
  if(log){ 
    canv.SetLogy(1); 
  }
  
  plot1D->SetXTitle(xaxis.c_str());
  plot1D->GetXaxis()->SetLabelFont(62);
  plot1D->GetXaxis()->SetTitleColor(1);
  plot1D->GetXaxis()->SetTitleOffset(1.05);
  plot1D->SetYTitle(yaxis.c_str());
  plot1D->GetYaxis()->SetLabelFont(62);
  plot1D->GetYaxis()->SetTitleSize(0.05);
  plot1D->GetYaxis()->SetTitleOffset(1.4);
  plot1D->GetYaxis()->SetLabelSize(0.05);
  plot1D->GetXaxis()->SetRange(lowerBin+1, upperBin);
  plot1D->SetMinimum( 0.);
  if(max>0){
    plot1D->SetMaximum(max);
  }
  else{
    plot1D->SetMaximum(1.3*plot1D->GetMaximum());
  }
  plot1D->SetLineWidth(3.); 
  plot1D->SetLineColor(kBlack); 
  plot1D->Draw();
  
  TLegend* leg = new TLegend(0.50, 0.81, 0.92, 0.90);
  leg->SetBorderSize( 0 );
  leg->SetFillStyle ( 0 );
  leg->SetFillColor (kWhite);
  leg->AddEntry(plot1D, "Likelihood scan", "L");
  leg->Draw("same");
  
  TString label = TString::Format("%s = %d GeV", masslabel.c_str(), mass);
  TPaveText* textlabel = new TPaveText(0.18, 0.81, 0.50, 0.90, "NDC");
  textlabel->SetBorderSize(   0 );
  textlabel->SetFillStyle (   0 );
  textlabel->SetTextAlign (  12 );
  textlabel->SetTextSize  (0.04 );
  textlabel->SetTextColor (   1 );
  textlabel->SetTextFont  (  62 );
  textlabel->AddText(label);
  textlabel->Draw();
  
  canv.RedrawAxis();
  return;
}

