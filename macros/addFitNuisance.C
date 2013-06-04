#include <iostream>
#include "TFile.h"
#include "TH1F.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "RooRealVar.h"                                                                                                                                                                                   
#include "RooDataHist.h"                                                                                                                                                                                  
#include "RooDataSet.h"                                                                                                                                                                                   
#include "RooHistPdf.h"                                                                                                                                                                                   
#include "RooGenericPdf.h"
#include "RooFitResult.h"
#include "TMatrixDSym.h"
#include "TMatrixDSymEigen.h"


TH1F* rebin(TH1F* iH,int iNBins,double *iAxis) { 
  TH1F *lH = new TH1F(iH->GetTitle(),iH->GetName(),iNBins,iAxis);
  lH->SetName (iH->GetName());
  lH->SetTitle(iH->GetName());
  for(int i0 = 0; i0 < iH->GetNbinsX()+1; i0++) {
    int    lNBin = lH->GetXaxis()->FindBin(iH->GetXaxis()->GetBinCenter(i0));
    double lVal  = iH->GetBinContent(i0);
    double lErr  = iH->GetBinError  (i0);
    double lOldV = lH->GetBinContent(lNBin);
    double lOldE = lH->GetBinError  (lNBin);
    lH->SetBinContent(lNBin,lVal+lOldV);
    lH->SetBinError  (lNBin,sqrt(lOldE*lOldE+lErr*lErr));
  }
  return lH;
}
TH1F * merge(std::string iName,double iMergePoint,TH1F *iH,TH1F *iFunc) {
  cout << "====> Name " << iName << endl;
  TH1F *lH = (TH1F*) iH->Clone(iName.c_str());
  lH->SetName(iName.c_str());
  lH->SetFillStyle(0);
  int lMergeBin = iH->GetXaxis()->FindBin(iMergePoint);
  double lVal  = iH->GetBinContent(lMergeBin);
  iFunc->Scale(lVal/iFunc->GetBinContent(lMergeBin));
  for(int i0 = 0;         i0 < lMergeBin;         i0++) lH->SetBinContent(i0,iH->GetBinContent(i0));
  for(int i0 = lMergeBin; i0 < iH->GetNbinsX()+1; i0++) lH->SetBinContent(i0,iFunc->GetBinContent(i0));
  return lH;
}
void addNuisance(std::string iFileName,std::string iChannel,std::string iBkg,std::string iEnergy,std::string iName,std::string iDir,bool iRebin=false) { 
  std::cout << "======> " << iDir << "/" << iBkg << " -- " << iFileName << std::endl;  
  TFile *lFile = new TFile(iFileName.c_str(),"UPDATE");
  TH1F  *lH0   = (TH1F*) lFile->Get((iDir+"/"+iBkg).c_str());
  TH1F  *lData = (TH1F*) lFile->Get((iDir+"/data_obs").c_str());
  //Define the fit function
  RooRealVar lM("m","m" ,0,5000);
  RooRealVar lA("a","a" ,0.02,  0,1.);
  RooRealVar lB("b","b" ,0.0 , -0.5,0.5);
  RooDataHist *pH0  =  new RooDataHist("Data","Data" ,RooArgList(lM),lH0);
  RooGenericPdf lFit("genPdf","exp(-a*m/(1+b*sqrt(m)))",RooArgList(lM,lA,lB));
  RooFitResult *lRFit   = 0;
  double lFirst = 200;
  double lLast  = 1200;
  lRFit = lFit.fitTo(*pH0,RooFit::Save(kTRUE),RooFit::Range(lFirst,lLast),RooFit::Strategy(2));//,RooFit::Minos());//,RooFit::Strategy(2));                                                                  //Make the shape nuisances
  TMatrixDSym lCovMatrix   = lRFit->covarianceMatrix();
  TMatrixD  lEigVecs(2,2);    lEigVecs = TMatrixDSymEigen(lCovMatrix).GetEigenVectors();
  TVectorD  lEigVals(2);      lEigVals = TMatrixDSymEigen(lCovMatrix).GetEigenValues();

  cout << " Ve---> " << lEigVecs(0,0) << " -- " << lEigVecs(1,0) << " -- " << lEigVecs(0,1) << " -- " << lEigVecs(1,1) << endl;
  cout << " Co---> " << lCovMatrix(0,0) << " -- " << lCovMatrix(1,0) << " -- " << lCovMatrix(0,1) << " -- " << lCovMatrix(1,1) << endl;
  double lACentral = lA.getVal();
  double lBCentral = lB.getVal();
  lEigVals(0) = sqrt(lEigVals(0));
  lEigVals(1) = sqrt(lEigVals(1));
  
  TH1F* lH     = (TH1F*) lFit.createHistogram("fit" ,lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));
  lA.setVal(lACentral + lEigVals(0)*lEigVecs(0,0));
  lB.setVal(lBCentral + lEigVals(0)*lEigVecs(1,0));
  TH1F* lHUp   = (TH1F*) lFit.createHistogram("Up"  ,lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));
  lA.setVal(lACentral - lEigVals(0)*lEigVecs(0,0));
  lB.setVal(lBCentral - lEigVals(0)*lEigVecs(1,0));
  TH1F* lHDown = (TH1F*) lFit.createHistogram("Down",lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));

  lA.setVal(lACentral + lEigVals(1)*lEigVecs(0,1));
  lB.setVal(lBCentral + lEigVals(1)*lEigVecs(1,1));
  TH1F* lHUp1   = (TH1F*) lFit.createHistogram("Up1",lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));
  lA.setVal(lACentral - lEigVals(1)*lEigVecs(0,1));
  lB.setVal(lBCentral - lEigVals(1)*lEigVecs(1,1));
  TH1F* lHDown1 = (TH1F*) lFit.createHistogram("Down1",lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));
  lFirst = 200;
  std::string lNuisance1 =  iBkg+"_"+"CMS_"+iName+"1_" + iChannel + "_" + iEnergy;
  std::string lNuisance2 =  iBkg+"_"+"CMS_"+iName+"2_" + iChannel + "_" + iEnergy;
  lHUp    = merge(lNuisance1 + "Up"   ,lFirst,lH0,lHUp);
  lHDown  = merge(lNuisance1 + "Down" ,lFirst,lH0,lHDown);
  lHUp1   = merge(lNuisance2 + "Up"   ,lFirst,lH0,lHUp1);
  lHDown1 = merge(lNuisance2 + "Down" ,lFirst,lH0,lHDown1);
  lH      = merge(lH0->GetName()      ,lFirst,lH0,lH);
  
  if(iRebin) { 
    double lAxis[32]={0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300,325,350,400,500,700,1000,1500};
    lH0     = rebin(lH0    ,31,lAxis);
    lH      = rebin(lH     ,31,lAxis);
    lHUp    = rebin(lHUp   ,31,lAxis);
    lHDown  = rebin(lHDown ,31,lAxis);
    lHUp1   = rebin(lHUp1  ,31,lAxis);
    lHDown1 = rebin(lHDown1,31,lAxis);
  }

  lFile->cd(iDir.c_str());
  lH     ->Write();//TObject::kOverWrite); 
  lHUp   ->Write(); 
  lHDown ->Write(); 
  lHUp1  ->Write(); 
  lHDown1->Write(); 

  /* Debug Plots
  lH     ->SetLineColor(kBlue);
  lHUp   ->SetLineColor(kRed);
  lHDown ->SetLineColor(kRed);
  lHUp1  ->SetLineColor(kBlue);
  lHDown1->SetLineColor(kBlue);
  TCanvas *lC0 = new TCanvas("Can","Can",800,600);
  lH0->Draw();
  lH     ->Draw("hist sames");
  lHUp   ->Draw("hist sames");
  lHDown ->Draw("hist sames");
  lHUp1  ->Draw("hist sames");
  lHDown1->Draw("hist sames");
  lC0->SetLogy();
  */
  lFile->Close();
  return;
}
void addFitNuisance(std::string iFileName="htt_tt.inputs-sm-8TeV.root",std::string iChannel="tauTau",std::string iBkg="QCD",std::string iEnergy="8TeV",std::string iName="shift",std::string iCategory="8", bool iRebin=true) { 
  // Also possible old MSSM categorization (for testing)
  if(iCategory=="0") addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_0jet_low",iRebin);
  if(iCategory=="1") addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_0jet_high",iRebin);
  if(iCategory=="2") addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_boost_low",iRebin);
  if(iCategory=="3") addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_boost_high",iRebin);
  if(iCategory=="6") addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_btag_low",iRebin);
  if(iCategory=="7") addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_btag_high",iRebin);
  if(iCategory=="8") addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_nobtag",iRebin);
  if(iCategory=="9") addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_btag",iRebin);
}
