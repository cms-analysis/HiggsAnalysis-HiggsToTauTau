#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"
#include "HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"

double getMinNLL(double iMass) { 
  std::stringstream pSS; pSS << " massscan/" << iMass << "/mlfit.root";
  TFile *lFile = new TFile(pSS.str().c_str());
  if(lFile == 0) return 1000.;
  TTree *lTree = (TTree*) lFile->FindObjectAny("tree_fit_sb");
  if(lTree == 0) return 1000.;
  double lNLL=  0; lTree->SetBranchAddress("nll_min",&lNLL); 
  lTree->GetEntry(0);				
  double lFNLL = lNLL;
  lFile->Close();
  cout << " ===> " << lFNLL << endl;
  return lFNLL;
}
void makeMuVMassPlot(bool iUseWWType = true,double iMassStep=5,bool iDebug=false,bool iFillGaps=true) { 
  SetStyle();
  TCanvas *lCan = new TCanvas("A","A",600,600);
  // lCan->SetGridx(1);
  //lCan->SetGridy(1);
  //lCan->SetRightMargin(0.14);

  double *lTX1 = new double[2];
  double *lTX2 = new double[2];
  double lMinNLL = 1000;
  double lVMin = 0;
  double *lMin = new double[36];     
  //if(!iUseWWType) for(int i0 = 0; i0 < 36; i0++) { lMin[i0] = getMinNLL(110+i0*iMassStep); if(lMin[i0] < lVMin) {lVMin = lMin[i0]; lTX1[0] = 110+i0*1.;}}
  if(!iUseWWType) for(int i0 = 0; i0 < 8; i0++) { lMin[i0] = getMinNLL(110+i0*iMassStep); if(lMin[i0] < lVMin) {lVMin = lMin[i0]; lTX1[0] = 110+i0*5.;}}

  TFile *lFile = new TFile("/afs/cern.ch/work/r/rlane/public/forPhil/cmbLikelihoodScan.root");//afs/cern.ch/user/p/pharris/public/massscan/cmb+.root");
  TTree *lTree = lFile->FindObjectAny("limit");
  TH2F *lH = new TH2F("2D","2D",int(35/iMassStep),109.5,145.5,50,0.,2.);
  float  lNLL  = 0; lTree->SetBranchAddress("nll"     ,&lNLL);
  float  lMNLL = 0; lTree->SetBranchAddress("deltaNLL",&lMNLL);
  double lMH   = 0; lTree->SetBranchAddress("mh"      ,&lMH);
  float  lR    = 0; lTree->SetBranchAddress("r"       ,&lR);
  
  if(iUseWWType) { 
    for(int i0 = 0; i0 < lTree->GetEntries(); i0++) { 
      lTree->GetEntry(i0);
      if(lR < 0.1 && lR > -0.1)  lMin[int(lMH-110)] = -lMNLL;
    }
    lVMin = 10000;
    for(int i0 = 0; i0 < lTree->GetEntries(); i0++) { 
      lTree->GetEntry(i0);
      double pMin =  lMin[int(lMH-110)] + lMNLL;
      if(pMin < lVMin) {lVMin = pMin; lTX1[0] = lMH;}
    }
  }
  for(int i0 = 0; i0 < lTree->GetEntries(); i0++) { 
    lTree->GetEntry(i0);
    //if(lMH == 125) continue;
    lNLL = 0.; //lMin  = 0.;
    lH->SetBinContent(lH->GetXaxis()->FindBin(lMH),lH->GetYaxis()->FindBin(lR),(lMNLL+lMin[int(lMH-110)]-lVMin)); 
    //cout << lMH << " " << lR << " -- " << (lMNLL+lMin[lH->GetXaxis()->FindBin(lMH)-1]-lVMin)  << " -- " << lVMin << endl;
    if(lMH == lTX1[0] && lMNLL < lMinNLL) {lMinNLL = lMNLL; lTX2[0] = lR;}
  }
  //Fill in Empty Bins
  double lPrev = -1;
  for(int i0 = 0; i0 < lH->GetNbinsX()+1; i0++) { 
    for(int i1 = 0; i1 < lH->GetNbinsY()+1; i1++) { 
      if(lH->GetBinContent(i0,i1) != 0) lPrev = lH->GetBinContent(i0,i1); 
      if(lH->GetBinContent(i0,i1) != 0) continue;
      if(iFillGaps) lH->SetBinContent(i0,i1,lPrev);
    }    
  }
  TH2F* lHC = lH->Clone("2D_v2");
  double lCont[3];
  lCont[0] = 1.17; 
  lCont[1] = 3.0;
  lCont[2] = 9.0;
  if(!iDebug) lHC->SetContour(2,lCont);
  //lCan->SetLogz();
  if(!iDebug) lHC->Draw("cont z list");
  //return;
  lCan->Update();
  lHC->Draw("colz");
  if(iDebug) return;

  //Smoothing and Interpolation crap
  TObjArray *lContours = (TObjArray*)gROOT->GetListOfSpecials()->FindObject("contours");
  int lTotalConts = lContours->GetSize();
  //Graph Ranges and labels
  double *lTX = new double[2]; lTX[0] = 110;  lTX[1] = 145; 
  double *lTY = new double[2]; lTY[0] = -0.5; lTY[1] = 2.5;
  TGraph *lFirst = new TGraph(2,lTX,lTY); lFirst->SetLineColor(kWhite);
  lFirst->GetXaxis()->SetRangeUser(110,148);
  lFirst->Draw("al"); lFirst->SetTitle("");
  lH->GetYaxis()->SetRangeUser(-0.5,2.5);
  lFirst->GetXaxis()->SetTitle("m_{H}[GeV]");
  lFirst->GetXaxis()->SetTitleOffset(1.0);
  lFirst->GetYaxis()->SetTitle("#mu_{best-fit}");
  lFirst->GetYaxis()->SetTitleOffset(1.2);

  lFirst->GetXaxis()->SetLabelFont(62);
  lFirst->GetXaxis()->SetLabelSize(0.045);
  lFirst->GetXaxis()->SetLabelOffset(0.015);
  lFirst->GetXaxis()->SetTitleFont(62);
  lFirst->GetXaxis()->SetTitleColor(1);
  lFirst->GetXaxis()->SetTitleOffset(1.05);
  // format y axis
  lFirst->GetYaxis()->SetLabelFont(62);
  lFirst->GetYaxis()->SetTitleSize(0.05);
  lFirst->GetYaxis()->SetTitleOffset(1.30);
  lFirst->GetYaxis()->SetLabelSize(0.045);
  //lFirst->SetNdivisions(505);


  lH->GetXaxis()->SetTitle("m_{H}[GeV]");
  lH->GetXaxis()->SetTitleOffset(1.0);
  lH->GetYaxis()->SetTitle("#mu_{best-fit}");
  lH->GetYaxis()->SetTitleOffset(1.2);

  //Best Fit point
  lTX1[1] = lTX1[0]; lTX2[1] = lTX2[1]+0.001;
  TGraph *lSecond = new TGraph(1,lTX1,lTX2); lSecond->SetMarkerStyle(34); lSecond->SetMarkerSize(3.5);
  
  TLegend *lL = new TLegend(0.65,0.15,0.85,0.35); lL->SetBorderSize(0); lL->SetFillColor(0); lL->SetFillStyle(0); 

  //Go through the array of contours and take the points on the curve
  for(i0 = 0; i0 < lTotalConts; i0++){
    pContLevel = (TList*)lContours->At(lTotalConts-1.-i0);
    // Get first graph from list on curves on this level
    std::vector<double> lX; 
    std::vector<double> lY; 
    pCurv = (TGraph*)pContLevel->First();
    for(int i1 = 0; i1 < pContLevel->GetSize(); i1++){
      for(int i2  = 0; i2 < pCurv->GetN(); i2++) {lX.push_back(pCurv->GetX()[i2]); lY.push_back(pCurv->GetY()[i2]);}
      pCurv->SetLineColor(kBlack);//kGreen+i0);
      pCCurv = (TGraph*)pCurv->Clone();
      if(i0 == 0) pCCurv->SetFillColor(0);
      if(i0 == 1) pCCurv->SetFillColor(0);
      pCCurv->SetLineWidth(3);
      pCCurv->GetXaxis()->SetRangeUser(0,3.0);
      pCurv = (TGraph*)pContLevel->After(pCurv); // Get Next graph
    }
    //Build a graph that are all of the points on the curve
    TGraph *lTotal = new TGraph(lX.size(),&lX[0],&lY[0]);
    lTotal->SetLineWidth(3);
    lTotal->SetFillColor(kGreen+i0*2);
    lTotal->SetFillStyle(1001);
    
    //Build a top and bottom curve 
    bool pSwitch = false;
    int  pSign   = -1.;   if(lTotal->GetX()[0] > lTotal->GetX()[1]) pSign = 1;
    double pXOld = lTotal->GetX()[lTotal->GetN()-1];
    std::vector<double> pXLeft;
    std::vector<double> pXRight;
    std::vector<double> pYLeft;
    std::vector<double> pYRight;
    for(int iX = 0; iX < lTotal->GetN(); iX++) { 
      double pX = lTotal->GetX()[iX];
      if(pSign*pX > pSign*pXOld ) {pSwitch = !pSwitch; pSign *= -1;}
      if(!pSwitch) {pXLeft.push_back(lTotal->GetX()[iX]); pYLeft.push_back(lTotal->GetY()[iX]); }
      if(pSwitch) {pXRight.push_back(lTotal->GetX()[iX]); pYRight.push_back(lTotal->GetY()[iX]); }
      pXOld = pX;
    }
    TGraph *lLeftTotal  = new TGraph(pXLeft.size() ,&pXLeft[0],&pYLeft[0]);
    TGraph *lRightTotal = new TGraph(pXRight.size(),&pXRight[0],&pYRight[0]);
    lLeftTotal->SetLineColor(kRed);
    lRightTotal->SetLineColor(kBlue);
    lLeftTotal->SetLineStyle(kDashed);
    lRightTotal->SetLineStyle(kDashed);
    //lLeftTotal->Draw("l");
    //lRightTotal->Draw("l");
    
    //Smooth the Curves
    TGraphSmooth *lGS0 = new TGraphSmooth("normal");
    TGraphSmooth *lGS1 = new TGraphSmooth("normal");
    TGraph *lSmooth0 = lGS0->SmoothSuper(lRightTotal,"",0.,0.);
    TGraph *lSmooth1 = lGS1->SmoothSuper(lLeftTotal,"",0.,0.) ;
    lSmooth0->Draw("l");
    lSmooth1->Draw("l");
    std::vector<double> pXSmooth;
    std::vector<double> pYSmooth;
    std::vector<double> pXSmooth1;
    std::vector<double> pYSmooth1;
    for(int iX = 0; iX < lSmooth0->GetN(); iX++) {pXSmooth.push_back(lSmooth0->GetX()[iX]);                    pYSmooth.push_back(lSmooth0->GetY()[iX]);}
    for(int iX = 0; iX < lSmooth1->GetN(); iX++) {pXSmooth.push_back(lSmooth1->GetX()[lSmooth1->GetN()-iX-1]); pYSmooth.push_back(lSmooth1->GetY()[lSmooth1->GetN()-iX-1]);}

    for(int iX = 0; iX < lSmooth0->GetN(); iX++) {pXSmooth1.push_back(lSmooth0->GetX()[iX]);                    pYSmooth1.push_back(lSmooth0->GetY()[iX]);}
    for(int iX = 0; iX < lSmooth1->GetN(); iX++) {pXSmooth1.push_back(lSmooth1->GetX()[lSmooth1->GetN()-iX-1]); pYSmooth1.push_back(lSmooth1->GetY()[lSmooth1->GetN()-iX-1]);}
    //if(i0 == 1) {pXSmooth1.push_back(lSmooth1->GetX()[0]); pYSmooth1.push_back(lSmooth1->GetY()[0]);}
    TGraph *pSmoothShape  = new TGraph(pXSmooth.size() ,&pXSmooth [0],&pYSmooth [0]);
    TGraph *pSmoothShape1 = new TGraph(pXSmooth1.size(),&pXSmooth1[0],&pYSmooth1[0]);
    //Reoint them with a line
    if(i0 == 1) {TLine  *lLine = new TLine(pXSmooth1[0],pYSmooth1[0],pXSmooth1[pXSmooth1.size()-1],pYSmooth1[pYSmooth1.size()-1]); lLine->Draw();}
    pSmoothShape1->SetLineColor(kBlack);
    pSmoothShape1->SetLineWidth(2);
    pSmoothShape->SetFillColor(kGreen+i0*2);
    pSmoothShape->SetFillStyle(1001);
    pSmoothShape->Draw("lf");
    pSmoothShape1->Draw("l");
    if(i0 == 0) lL->AddEntry(lTotal,"95% CL","lf");
    if(i0 == 1) lL->AddEntry(lTotal,"68% CL","lf");
  }
  lL->AddEntry(lSecond,"BestFit","p");
  lSecond->Draw("lp");
  lL->Draw();
  
  //Final touchs
  std::string masslabel = "m_{H}"; double mass = 125;
  TString label = TString::Format("%s = 135 GeV", masslabel.c_str());//, 125.);
  TPaveText* textlabel = new TPaveText(0.18, 0.81, 0.50, 0.90, "NDC");
  textlabel->SetBorderSize(   0 );
  textlabel->SetFillStyle (   0 );
  textlabel->SetTextAlign (  12 );
  textlabel->SetTextSize  (0.04 );
  textlabel->SetTextColor (   1 );
  textlabel->SetTextFont  (  62 );
  textlabel->AddText(label);
  //textlabel->Draw();
  //CMSPrelim("Preliminary, #sqrt{s}=7-8 TeV, L=24.3 fb^{-1}, H#rightarrow#tau#tau", "", 0.145, 0.835);
  CMSPrelim("CMS Preliminary, H#rightarrow#tau#tau, 4.9 fb^{-1} at 7 TeV, 19.7 fb^{-1} at 8 TeV", "", 0.145, 0.835);
  gPad->RedrawAxis();
  lCan->Update();

  lCan->SaveAs("cmb+_muvmass.png");
  lCan->SaveAs("cmb+_muvmass.pdf");
  lCan->SaveAs("cmb+_muvmass.eps");
  lCan->SaveAs("cmb+_muvmass.C");
}


