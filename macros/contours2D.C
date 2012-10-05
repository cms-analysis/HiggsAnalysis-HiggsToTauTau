#include <iostream>

#include "TROOT.h"
#include "TTree.h"
#include "TFile.h"
#include "TGraph.h"
#include "TString.h"

TGraph* bestFit(TTree *t, TString x, TString y) {
    t->Draw(y+":"+x, "quantileExpected == 1");
    TGraph *gr0 = (TGraph*) gROOT->FindObject("Graph")->Clone();
    gr0->SetMarkerStyle(34); gr0->SetMarkerSize(2.0);
    return gr0;
}

TGraph* expValue(double x0 = 0.0, double y0 = 0.0) {
    TGraph* ret = new TGraph(1);
    ret->SetPoint(0, x0, y0);
    ret->SetMarkerStyle(29); ret->SetMarkerSize(4.0);
    ret->SetMarkerColor(4);
    return ret;
}

TGraph* contour2D(TTree *t, TString x, TString y, double pmin, double pmax, TGraph *bestFit) {
    int n = t->Draw(y+":"+x, Form("%f <= quantileExpected && quantileExpected <= %f && quantileExpected != 1",pmin,pmax));
    std::cout << "Drawing for " << Form("%f <= quantileExpected && quantileExpected <= %f && quantileExpected != 1",pmin,pmax) << " yielded " << n << " points." << std::endl;
    TGraph *gr = (TGraph*) gROOT->FindObject("Graph")->Clone();

    Double_t x0 = bestFit->GetX()[0], y0 = bestFit->GetY()[0];
    Double_t *xi = gr->GetX(), *yi = gr->GetY();
    //int n = gr->GetN();
    for (int i = 0; i < n; ++i) { xi[i] -= x0; yi[i] -= y0; }
    gr->Sort(&TGraph::CompareArg);
    for (int i = 0; i < n; ++i) { xi[i] += x0; yi[i] += y0; }
    gr->SetPoint(n, xi[0], yi[0]);
    return gr;
}

void contours2D(const char *name, double para1=0., double para2=0., string typ="ggHbbH", int mass=120) {
  TFile* file68_ = TFile::Open(TString::Format("higgsCombineTest68CL.MultiDimFit.mH%d.root", mass), "READ"); TTree *tree68_ = (TTree*) file68_->Get("limit");
  TFile* file95_ = TFile::Open(TString::Format("higgsCombineTest68CL.MultiDimFit.mH%d.root", mass), "READ"); TTree *tree95_ = (TTree*) file95_->Get("limit");

  TGraph *grExp = expValue(para1, para2);
  TGraph *grFit = new TGraph();
  TGraph *gr68  = new TGraph();
  TGraph *gr95  = new TGraph();
  if(typ=="ggHbbH")
    {
      std::cout<< "typ " << typ << std::endl;
      grFit = bestFit(tree68_, "r_ggH", "r_bbH"); 
      gr68  = contour2D(tree68_, "r_ggH", "r_bbH", 0.310, 1, grFit);
      gr95  = contour2D(tree95_, "r_ggH", "r_bbH", 0.049, 1, grFit);
    }
  else if(typ=="ggHqqH")
    {
      std::cout<< "typ " << typ << std::endl;
      grFit = bestFit(tree68_, "r_ggH", "r_qqH"); 
      gr68  = contour2D(tree68_, "r_ggH", "r_qqH", 0.310, 1, grFit);
      gr95  = contour2D(tree95_, "r_ggH", "r_qqH", 0.049, 1, grFit);
    }
  else if(typ=="cVcF")
    {
      std::cout<< "typ " << typ << std::endl;
      grFit = bestFit(tree68_, "CV", "CF"); 
      gr68  = contour2D(tree68_, "CV", "CF", 0.310, 1, grFit);
      gr95  = contour2D(tree95_, "CV", "CF", 0.049, 1, grFit);
    }
  else 
    {
      std::cout<< "Unknow typ " << typ << ". Possible typs: ggHbbH, ggHqqH, cVcF !" << std::endl;
    }


  gr68->SetLineWidth(3); gr68->SetLineStyle(1); gr68->SetLineColor(4);
  gr95->SetLineWidth(3); gr95->SetLineStyle(7); gr95->SetLineColor(4);
      
  TFile *file = TFile::Open(Form("%s.root", name), "RECREATE");
  file->cd();
  grFit->SetName(Form("%s_fit" , name)); gFile->WriteTObject(grFit);
  gr68 ->SetName(Form("%s_cl68", name)); gFile->WriteTObject(gr68 );
  gr95 ->SetName(Form("%s_cl95", name)); gFile->WriteTObject(gr95 );
  grExp->SetName(Form("%s_exp" , name)); gFile->WriteTObject(grExp);
  file->Close();  

  file68_->Close();
  file95_->Close();
}
