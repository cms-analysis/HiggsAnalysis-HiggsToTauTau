#include <iostream>

#include "TROOT.h"
#include "TTree.h"
#include "TFile.h"
#include "TGraph.h"
#include "TString.h"

TGraph* expValue(double x0 = 0.0, double y0 = 0.0) {
    TGraph* ret = new TGraph(1);
    ret->SetPoint(0, x0, y0);
    ret->SetMarkerStyle(29); ret->SetMarkerSize(4.0);
    ret->SetMarkerColor(4);
    return ret;
}

TGraph* bestFit(TTree *t, TString x, TString y, TString selection) {
    t->Draw(y+":"+x, selection);
    TGraph *gr0 = (TGraph*) gROOT->FindObject("Graph")->Clone();
    gr0->SetMarkerStyle(34); gr0->SetMarkerSize(2.0);
    return gr0;
}

TGraph* contour(TTree *t, TString x, TString y, TString selection, TGraph *bestFit) {
  int n = t->Draw(y+":"+x, selection);
  std::cout << "Drawing for " << selection << " yielded " << n << " points." << std::endl;
  TGraph *gr = (TGraph*) gROOT->FindObject("Graph")->Clone();
    Double_t x0 = bestFit->GetX()[0], y0 = bestFit->GetY()[0];
  Double_t *xi = gr->GetX(), *yi = gr->GetY();
  for (int i = 0; i < n; ++i) { xi[i] -= x0; yi[i] -= y0; }
  gr->Sort(&TGraph::CompareArg);
  for (int i = 0; i < n; ++i) { xi[i] += x0; yi[i] += y0; }
  gr->SetPoint(n, xi[0], yi[0]);
  return gr;
}

void contours2D(std::string path, std::string outputName, std::string x="r_ggH", std::string y="r_bbH", std::string method="minos", std::string mass="120", double xExp=0., double yExp=0.) 
{
  std::cout << " *******************************************************************************************************\n"
	    << " * Usage     : root -l                                                                                  \n"
	    << " *             .x MitLimits/Higgs2Tau/macros/contours2D.C+(path, out, x, y, method, mass, xExp, yExp)   \n"
	    << " *                                                                                                      \n"
	    << " * Arguments :  + path        string        path to the input files.                                    \n"
	    << " *              + output      string        name of the output file. TGraphs in the output file will    \n"
	    << " *                                          have the same names with endings _fit, _cl68, _cl95, _exp   \n"
	    << " *              + x           string        branch to be drawn on x-axis. Possible names are 'r_ggH',   \n"
	    << " *                                          'r_bbH', 'r_qqH', 'CF' 'CV', depending on the model that    \n"
	    << " *                                          has been used to do the fit.                                \n"
	    << " *              + y           string        branch to be drawn on x-axis. Possible names are 'r_ggH',   \n"
	    << " *                                          'r_bbH', 'r_qqH', 'CF' 'CV', depending on the model that    \n"
	    << " *                                          has been used to do the fit.                                \n"
	    << " *              + method      string        method that has been used to determin the contours. Options \n"
	    << " *                                          are 'minos' (default) and 'scan'. Note that scan needs to   \n"
	    << " *                                          be tuned depending on the number of scan points to give     \n"
	    << " *                                          smooth contours. The current tuning is for 40*40 points     \n"
	    << " *              + mass        string        mass point for which to do the scan (for file opening).     \n"
	    << " *                                                                                                      \n"
	    << " *              + xExp        double        x value for expected signal.                                \n"
	    << " *              + yExp        double        y value for expected signal.                                \n"
	    << " *                                                                                                      \n"
	    << " *******************************************************************************************************\n";
  
  std::vector<TFile*> files_; 
  std::vector<TTree*> trees_;

  if(method  == "minos"){
    files_.push_back(TFile::Open(TString::Format("%s/higgsCombineCL68.MultiDimFit.mH%s.root", path.c_str(), mass.c_str()), "READ")); trees_.push_back((TTree*) files_.back()->Get("limit"));
    files_.push_back(TFile::Open(TString::Format("%s/higgsCombineCL95.MultiDimFit.mH%s.root", path.c_str(), mass.c_str()), "READ")); trees_.push_back((TTree*) files_.back()->Get("limit"));
  }
  else if(method == "scan"){
    files_.push_back(TFile::Open(TString::Format("%s/higgsCombineScan.MultiDimFit.mH%s.root", path.c_str(), mass.c_str()), "READ")); trees_.push_back((TTree*) files_.back()->Get("limit"));
  }
  else{
    std::cout<< "Unknow method " << method << ". Available methods: minos, scan." << std::endl;
  }

  TGraph *grExp = expValue(xExp, yExp);
  TGraph *grFit = bestFit(trees_.front(), x, y, method=="minos" ? "quantileExpected==1" : "deltaNLL==0"); 
  TGraph *gr68  = contour(trees_.front(), x, y, method=="minos" ? "0.31 <=quantileExpected && quantileExpected<=1.0 && quantileExpected!=1.0" : "0.8<=deltaNLL && deltaNLL<=1.  ", grFit);
  TGraph *gr95  = contour(trees_.back (), x, y, method=="minos" ? "0.049<=quantileExpected && quantileExpected<=1.0 && quantileExpected!=1.0" : "1.5<=deltaNLL && deltaNLL<=1.92", grFit);

  gr68->SetLineWidth(3); gr68->SetLineStyle(1); gr68->SetLineColor(4);
  gr95->SetLineWidth(3); gr95->SetLineStyle(7); gr95->SetLineColor(4);

  TFile *file = TFile::Open(Form("%s.root", outputName.c_str()), "RECREATE");
  file->cd();
  grFit->SetName(Form("%s_fit" , outputName.c_str())); gFile->WriteTObject(grFit);
  gr68 ->SetName(Form("%s_cl68", outputName.c_str())); gFile->WriteTObject(gr68 );
  gr95 ->SetName(Form("%s_cl95", outputName.c_str())); gFile->WriteTObject(gr95 );
  grExp->SetName(Form("%s_exp" , outputName.c_str())); gFile->WriteTObject(grExp);
  file->Close();  

  for(std::vector<TFile*>::const_iterator f=files_.begin(); f!=files_.end(); ++f){
    (*f)->Close();
  }
}
