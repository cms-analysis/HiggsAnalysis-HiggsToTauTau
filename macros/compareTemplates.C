#include <iostream>

#include <TH1F.h>
#include <TFile.h>
#include <TMath.h>
#include <TROOT.h>
#include <TString.h>
#include <TSystem.h>
#include <Rtypes.h>

#include <TAxis.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TAttLine.h>
#include <TPaveText.h>

#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"


/**
   \class   compareTemplates compareTemplates.C "HiggsAnalysis/HiggsToTauTau/macros/compareTemplates.C"

   \brief   macro to compare the templates of two inputs files that go into the limit calculation 

   This is a macro to compare the templates of two inputs that go into the limit calculation. It has been
   introduced to facilitate the synchonization between different groups. Use it like: 

   root -l
   .x HiggsAnalysis/HiggsAnalysis/HiggsToTauTau/macros/compareTemplates.C+(...)

   Running the macro will result in a plot comparing the two histograms directly (if configured such, the 
   shapes of both histograms will be normalized to 1.) and in a second plot containing the ratio of the 
   comparing histograms wrt to the referecne histogram. For the ratio histogram errors are treated by 
   TH1F::Divide(). A few rudimentary arguments to configre the output can be passed on to the macro (as 
   described below).

   Function arguments are: 
   
   REFERENCEFILE   (const char*)           the name and full path to the reference inputs file to which 
                                           the templates should be compared (must be given).

   COMPAREFILE     (const char*)           the name and full path to the files from which the templates 
                                           should be comparec with the reference (must be given). 

   CATEGORY        (const char*)           the name of the category, corresponding to the directory in 
                                           the file where to find the histograms, to be compared (must 
					   be given). NOTE that the CATEGORY name is expected to be the 
					   same in both files. 

   SAMPLE          (const char*)           name of the sample, corresponding to the histogram name to be 
                                           compared (must be given).

   MIN             (float)                 minimum of the comparison plot. Optional, default is 0. 

   MAX             (float)                 maximum of the comparison plot. Optional, default is 100.

   LOG             (bool)                  plot in log scale or not. Options, default is false.

   SHAPEONLY       (bool)                  do only shape compariosn or shape and normalization. Optional
                                           default is false (corresponding to shape+normalization). 

   LABEL           (const char*)           Label that can be added by the user. This label will appear on 
                                           the top of the comparison histogram. Optional, default is "".

   All outputs are printed to COMPARISON_versus_REFERENCE.eps/.png/.pdf (for the direct comparison file) 
   and , COMPARISON_versus_REFERENCE_ratio.eps/.png/.pdf (for the ratio of the two histograms), where 
   COMPARISON corresponds to the name of the comparison file (COMPAREFILE) and REFERENCE corresponds to 
   the name fo the reference file (REFERENCEFILE) as described above. 

   DISCLAIMER:

   The macro checks for the existance of the required histograms in each file and stops immediately if one
   of the histograms is not found. It does not explicitly check fo the equal number of bins of the required 
   histograms. As this macro is supposed to check synchronization it is assumed that the groups comparing 
   their histogram templates managed to sync on the the names, categories and binnings of their templaes 
   beforehand. 
*/

TH1F*
get(TFile* file, TString path, bool dropErrors=false)
{
  TH1F* hist = (TH1F*)file->Get(path);
  if(!hist){
    std::cout << "ERROR: " 
	      << "required sample: " << path << " does not exist in file: " << file->GetName() << std::endl;
    exit(1);
  }
  if(dropErrors){
    for(int ibin=0; ibin<hist->GetNbinsX(); ++ibin){
      hist->SetBinError(ibin+1, 0.);
    }
  }
  return hist;
}

void 
compareTemplates(const char* referenceFile, const char* compareFile, const char* category, const char* sample, float min=0, float max=1000, bool log=true, bool shapeOnly=false, const char* label="")
{
  // defining the common canvas, axes pad styles
  SetStyle(); gStyle->SetLineStyleString(11,"20 10");

  TFile* refFile = new TFile(referenceFile); TFile* cmpFile = new TFile(compareFile);
  TH1F* cmpHist  = get(cmpFile, TString::Format("%s/%s", category, sample)); 
  TH1F* refHist  = get(refFile, TString::Format("%s/%s", category, sample)); 

  if(shapeOnly){
    cmpHist->Scale(1./cmpHist->Integral());
    refHist->Scale(1./refHist->Integral());
  }
 
  TH1F* auxHist  = (TH1F*)refHist->Clone("auxHist");
  for(int ibin=0; ibin<auxHist->GetNbinsX(); ++ibin){
    auxHist->SetBinError(ibin+1, 0.);
  }

  /*
    compare samples directly
  */
  TCanvas* canv = MakeCanvas("canv", "histograms", 600, 600);
  canv->SetGridx(1); canv->SetGridy(1); if(log) canv->SetLogy(1);
  canv->cd();
  refHist->GetYaxis()->SetTitle("Events");
  refHist->GetYaxis()->SetTitleOffset(1.3);
  refHist->GetYaxis()->CenterTitle();

  refHist->SetNdivisions(505);
  refHist->SetMinimum(min);
  refHist->SetMaximum(max);
  refHist->SetLineColor(kBlue);
  refHist->SetLineWidth(3.);
  refHist->SetMarkerColor(kBlue);
  refHist->SetMarkerStyle(22.);
  refHist->SetMarkerSize(1.3);
  refHist->SetFillColor(kBlue);
  refHist->SetFillStyle(3005.);
  refHist->Draw();

  auxHist->SetLineColor(kBlue);
  auxHist->SetLineWidth(3.);
  auxHist->SetFillColor(kBlue);
  auxHist->SetFillStyle(3005.);
  auxHist->Draw("same");

  cmpHist->SetLineColor(kRed);
  cmpHist->SetLineWidth(3.);
  cmpHist->SetMarkerColor(kRed);
  cmpHist->SetMarkerStyle(23.);
  cmpHist->SetMarkerSize(1.3);
  cmpHist->Draw("same");

  TPaveText* text  = new TPaveText(0.15, 0.90, 0.90, 0.99, "NDC");
  text->SetBorderSize(   0 );
  text->SetFillStyle(    0 );
  text->SetTextAlign(   12 );
  text->SetTextSize ( 0.032 );
  text->SetTextColor(    1 );
  text->SetTextFont (   42 );
  text->AddText(label);
  text->Draw();

  TLegend* leg = new TLegend(0.5, 0.8, 0.9, 0.90);
  SetLegendStyle(leg);
  leg->AddEntry(refHist, "Reference"  , "PLF" );
  leg->AddEntry(cmpHist, "Comparison" , "PL" );
  leg->Draw();

  /*
    compare plot ratio of the two samples
  */
  TCanvas* ratio = MakeCanvas("ratio", "histograms", 600, 300);
  ratio->SetLogy(0); ratio->SetGridx(1); ratio->SetGridy(1);
  ratio->cd();
  // refLine line
  TH1F* refLine = (TH1F*)auxHist->Clone("refLine"); refLine->Clear();
  for(int ibin=0; ibin<auxHist->GetNbinsX(); ++ibin){
    refLine->SetBinContent(ibin+1, 1);
  }
  refLine->SetMinimum(0);
  refLine->SetMaximum(2);
  refLine->SetFillStyle(0);
  refLine->GetYaxis()->SetTitle("cmp/ref");
  refLine->GetYaxis()->SetTitleOffset(0.8);
  refLine->GetYaxis()->CenterTitle();
  refLine->Draw();

  TH1F* cmpLine = (TH1F*)cmpHist->Clone("cmpLine"); cmpLine->Divide(refHist);
  cmpLine->Draw("same");

  /*
    prepare output
  */
  std::string newName = std::string(referenceFile).substr(0, std::string(referenceFile).find(".root"));
  newName+="_versus_"+std::string(compareFile).substr(0, std::string(compareFile).find(".root"));
  canv ->Print(TString::Format("%s.png"      , newName.c_str())); 
  canv ->Print(TString::Format("%s.pdf"      , newName.c_str())); 
  canv ->Print(TString::Format("%s.eps"      , newName.c_str())); 
  ratio->Print(TString::Format("%s_ratio.png", newName.c_str())); 
  ratio->Print(TString::Format("%s_ratio.pdf", newName.c_str())); 
  ratio->Print(TString::Format("%s_ratio.eps", newName.c_str())); 
}
