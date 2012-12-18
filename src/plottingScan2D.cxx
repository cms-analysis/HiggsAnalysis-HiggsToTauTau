#include "TH2F.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TPaveText.h"

void
plotting2DScan(TCanvas& canv, TH2F* plot2D, TGraph* graph95, TGraph* graph68, TGraph* bestfit, std::string& xaxis, std::string& yaxis, std::string& masslabel, int mass, double xmin, double xmax, double ymin, double ymax, bool temp=false, bool log=false)
{
  // set up styles
  canv.cd();
  canv.SetGridx(1);
  canv.SetGridy(1);
  canv.SetRightMargin(0.14);
  if(log){ 
    canv.SetLogz(1); 
  }
  
  plot2D->SetXTitle(xaxis.c_str());
  if(xmax>0){
    plot2D->GetXaxis()->SetRange(plot2D->GetXaxis()->FindBin(xmin), plot2D->GetXaxis()->FindBin(xmax)-1);
  }
  plot2D->GetXaxis()->SetLabelFont(62);
  plot2D->GetXaxis()->SetTitleColor(1);
  plot2D->GetXaxis()->SetTitleOffset(1.05);
  plot2D->SetYTitle(yaxis.c_str());
  if(ymax>0){
    plot2D->GetYaxis()->SetRange(plot2D->GetYaxis()->FindBin(ymin), plot2D->GetYaxis()->FindBin(ymax)-1);
  }
  plot2D->GetYaxis()->SetLabelFont(62);
  plot2D->GetYaxis()->SetTitleSize(0.05);
  plot2D->GetYaxis()->SetTitleOffset(1.4);
  plot2D->GetYaxis()->SetLabelSize(0.05);
  plot2D->SetZTitle("#bf{#Delta NLL}");
  plot2D->GetZaxis()->SetLabelFont(62);
  plot2D->GetZaxis()->SetTitleSize(0.04);
  plot2D->GetZaxis()->SetTitleOffset(1.03);
  plot2D->GetZaxis()->SetLabelSize(0.04);
  plot2D->SetMinimum(0.);
  plot2D->Draw("colz");
  
  /// draw contours for 95% CL
  if(!temp){
    graph95->SetLineStyle(11); 
    graph95->SetLineColor(kBlack);
    graph95->SetLineWidth(3); 
    graph95->SetFillColor(kBlue-10);
    graph95->Draw("cfsame"); 
    graph95->Draw("contsame");
  }
  else{
    graph95->SetLineStyle(11); 
    graph95->SetLineColor(kBlack); 
    graph95->SetLineWidth(3);
    graph95->Draw("contsame");
  }
  /// draw contours for 68% CL
  if(!temp){ 
    graph68->SetLineStyle(11); 
    graph68->SetLineColor(kBlack); 
    graph68->SetLineWidth(3);
    graph68->SetFillColor(kBlue-8);
    graph68->Draw("cfsame"); 
    graph68->Draw("contsame");
  }
  else{
    graph68->SetLineStyle(1); 
    graph68->SetLineColor(kBlack); 
    graph68->SetLineWidth(3);
    graph68->Draw("contsame");
  }
  /// draw best fit
  bestfit->SetMarkerStyle(34);
  bestfit->SetMarkerSize(3.0);
  bestfit->SetMarkerColor(kBlack);
  bestfit->Draw("Psame");
  
  TLegend* leg = new TLegend(0.60, 0.70, 0.90, 0.90);
  leg->SetBorderSize( 0 );
  leg->SetFillStyle ( 0 );
  leg->SetFillColor (kWhite);
  leg->AddEntry(graph95, "95% CL", temp ? "L" : "FL");
  leg->AddEntry(graph68, "68% CL", temp ? "L" : "FL");
  leg->AddEntry(bestfit, "Best fit", "P");
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

