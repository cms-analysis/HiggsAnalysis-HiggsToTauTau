#include <iostream>
#include "TROOT.h"
#include "TFile.h"
#include "TMath.h"
#include "TKey.h"
#include "TF1.h"
#include "TFitResult.h"
#include "TFitResultPtr.h"
#include "TH1F.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "RooBinning.h"                                                                                                                                                               
#include "RooRealVar.h"   
#include "RooDataHist.h"   
#include "RooDataSet.h"    
#include "RooHistPdf.h"     
#include "RooGenericPdf.h"
#include "RooGaussian.h"
#include "RooAddPdf.h"
#include "RooFitResult.h"
#include "RooMCStudy.h"
#include "RooPlot.h"
#include "TMatrixDSym.h"
#include "TMatrixDSymEigen.h"

//Clone the file excluding the histogram (code stolen from Rene Brun)
void copyDir(TDirectory *source,std::string iSkipHist,bool iFirst=true) { 
  //copy all objects and subdirs of directory source as a subdir of the current directory   
  TDirectory *savdir = gDirectory;
  TDirectory *adir   = savdir;
  if(!iFirst) adir   = savdir->mkdir(source->GetName());
  if(!iFirst) adir->cd();
  //loop on all entries of this directory
  TKey *key;
  TIter nextkey(source->GetListOfKeys());
  while ((key = (TKey*)nextkey())) {
    const char *classname = key->GetClassName();
    TClass *cl = gROOT->GetClass(classname);
    if (!cl) continue;
    if (cl->InheritsFrom(TDirectory::Class())) {
      source->cd(key->GetName());
      TDirectory *subdir = gDirectory;
      adir->cd();
      copyDir(subdir,iSkipHist,false);
      adir->cd();
    } else {
      source->cd();
      TObject *obj = key->ReadObj();
      std::string pFullName = std::string(adir->GetName())+"/"+std::string(obj->GetName());
      std::string iSkipHist2 = iSkipHist;
      std::string fine_binning = "_fine_binning";
      iSkipHist2.replace(iSkipHist2.find(fine_binning), fine_binning.length(),"");
      if(pFullName.find(iSkipHist) != std::string::npos || pFullName.find(iSkipHist2) != std::string::npos) {
	continue;
      }
      adir->cd();
      obj->Write();
      delete obj;
    }
  }
  adir->SaveSelf(kTRUE);
  savdir->cd();
}
void cloneFile(TFile *iOutputFile,TFile *iReadFile,std::string iSkipHist) {
  //copy all objects and subdirs of directory source as a subdir of the current directory   
  iOutputFile->cd();
  copyDir(iReadFile,iSkipHist);
}  
//Rebin the histogram
TH1F* rebin(TH1F* iH,int iNBins,double *iAxis) { 
  std::string lTmp = "tmp"; //Added to avoid Root output errors
  TH1F *lH = new TH1F(lTmp.c_str(),lTmp.c_str(),iNBins,iAxis);
  for(int i0 = 0; i0 < iH->GetNbinsX()+1; i0++) {
    int    lNBin = lH->GetXaxis()->FindBin(iH->GetXaxis()->GetBinCenter(i0));
    double lVal  = iH->GetBinContent(i0);
    double lErr  = iH->GetBinError  (i0);
    double lOldV = lH->GetBinContent(lNBin);
    double lOldE = lH->GetBinError  (lNBin);
    lH->SetBinContent(lNBin,lVal+lOldV);
    lH->SetBinError  (lNBin,sqrt(lOldE*lOldE+lErr*lErr));
  }
  std::string lName2 = iH->GetName();
  std::string fine_binning = "_fine_binning";
  lName2.replace(lName2.find(fine_binning),fine_binning.length(),"");
  lH->SetName (lName2.c_str());
  lH->SetTitle(lName2.c_str());
  delete iH;
  return lH;
}
//Merge Histogram with function histogram
TH1F * merge(std::string iName,double iMergePoint,TH1F *iH,TH1F *iFunc) {
  cout << "====> Name " << iName << " -- " << iFunc << " -- " << iH << endl;
  TH1F *lH = (TH1F*) iH->Clone(iName.c_str());
  lH->SetFillStyle(0);
  int lMergeBin = iH->GetXaxis()->FindBin(iMergePoint);
  double lVal  = iH->GetBinContent(lMergeBin);
  //iFunc->Scale(lVal/iFunc->GetBinContent(lMergeBin));
  iFunc->Scale( (iH->Integral(lMergeBin, iH->GetXaxis()->FindBin(1500))) / (iFunc->Integral(lMergeBin, iFunc->GetXaxis()->FindBin(1500)) )); // felix - last fit bin = 1500; this approach seems to work much better
  for(int i0 = 0;         i0 < lMergeBin;         i0++) lH->SetBinContent(i0,iH->GetBinContent(i0));
  for(int i0 = lMergeBin; i0 < iH->GetNbinsX()+1; i0++) lH->SetBinContent(i0,iFunc->GetBinContent(iFunc->GetXaxis()->FindBin(lH->GetXaxis()->GetBinCenter(i0))));
  lH->SetName(iName.c_str());
  return lH;
}
//Difference plotting
void drawDifference(TH1* iH0,TH1 *iH1,TH1 *iHH=0,TH1 *iHL=0,TH1 *iHH1=0,TH1 *iHL1=0) {
  std::string lName = std::string(iH0->GetName());
  TH1F *lHDiff   = (TH1F*) iH0->Clone("Diff");
  TH1F *lHDiffH  = (TH1F*) iH0->Clone("DiffH");
  TH1F *lHDiffL  = (TH1F*) iH0->Clone("DiffL"); 
  TH1F *lHDiffH1 = (TH1F*) iH0->Clone("DiffH1");
  TH1F *lHDiffL1 = (TH1F*) iH0->Clone("DiffL1"); 
  lHDiff  ->SetFillColor(kViolet); lHDiff->SetFillStyle(1001); lHDiff->SetLineWidth(1);
  lHDiffL ->SetLineWidth(1); lHDiffL ->SetLineColor(iHL ->GetLineColor());
  lHDiffH ->SetLineWidth(1); lHDiffH ->SetLineColor(iHH ->GetLineColor());
  lHDiffL1->SetLineWidth(1); lHDiffL1->SetLineColor(iHL1->GetLineColor());
  lHDiffH1->SetLineWidth(1); lHDiffH1->SetLineColor(iHH1->GetLineColor());
  TH1F *lXHDiff1 = new TH1F((lName+"XDiff1").c_str(),(lName+"XDiff1").c_str(),iH0->GetNbinsX(),iH0->GetXaxis()->GetXmin(),iH0->GetXaxis()->GetXmax());
  TH1F *lXHDiff2 = new TH1F((lName+"XDiff2").c_str(),(lName+"XDiff2").c_str(),iH0->GetNbinsX(),iH0->GetXaxis()->GetXmin(),iH0->GetXaxis()->GetXmax());
  int i1 = 0;
  lXHDiff1->SetLineWidth(2); lXHDiff1->SetLineColor(kRed);
  lXHDiff2->SetLineWidth(2); lXHDiff2->SetLineColor(kRed);

  lXHDiff1->GetYaxis()->SetTitle("Ratio");
  lXHDiff1->GetYaxis()->SetRangeUser(0.2,1.8);
  lXHDiff1->GetYaxis()->SetTitleOffset(0.4);
  lXHDiff1->GetYaxis()->SetTitleSize(0.2);
  lXHDiff1->GetYaxis()->SetLabelSize(0.11);
  for(int i0 = 0; i0 < lHDiff->GetNbinsX()+1; i0++) {
    double lXCenter = lHDiff->GetBinCenter(i0);
    double lXVal     = iH0   ->GetBinContent(i0);
    double lXValH    = iHH   ->GetBinContent(i0);
    double lXValL    = iHL   ->GetBinContent(i0);
    double lXValH1   = iHH1  ->GetBinContent(i0);
    double lXValL1   = iHL1  ->GetBinContent(i0);
    lXHDiff1->SetBinContent(i0, 1.0);
    lXHDiff2->SetBinContent(i0, 1.0);
    while(iH1->GetBinCenter(i1) < lXCenter) {i1++;}
    if(iH1->GetBinContent(i0) > 0) lHDiff->SetBinContent(i0,lXVal      /(iH1->GetBinContent(i0)));
    if(iH1->GetBinContent(i0) > 0) lHDiff->SetBinError  (i0,sqrt(lXVal)/(iH1->GetBinContent(i0)));
    if(iH1->GetBinContent(i0) > 0) lHDiffL->SetBinContent(i0,lXValL/(iH1->GetBinContent(i0)));
    if(iH1->GetBinContent(i0) > 0) lHDiffH->SetBinContent(i0,lXValH/(iH1->GetBinContent(i0)));
    if(iH1->GetBinContent(i0) > 0) lHDiffL1->SetBinContent(i0,lXValL1/(iH1->GetBinContent(i0)));
    if(iH1->GetBinContent(i0) > 0) lHDiffH1->SetBinContent(i0,lXValH1/(iH1->GetBinContent(i0)));
   //if(iH1->GetBinContent(i0) > 0)  cout << "unc" << lXVal << " -- " << sqrt(lXVal)/(iH1->GetBinContent(i0)) << endl;
  }
  lHDiff->SetMarkerStyle(kFullCircle);
  //lHDiff->Draw("EP");
  
  lXHDiff1->SetStats(0);
  lXHDiff2->SetStats(0);
  lHDiff->SetStats(0);
  lHDiffH->SetStats(0);
  lHDiffL->SetStats(0);
  lHDiffH1->SetStats(0);
  lHDiffL1->SetStats(0);

  lXHDiff1->Draw("hist");
  lXHDiff2->Draw("hist sames");
  lHDiff->Draw("EP sames");
  lHDiffH ->Draw("hist sames");
  lHDiffL ->Draw("hist sames");
  lHDiffH1->Draw("hist sames");
  lHDiffL1->Draw("hist sames");
}
//Get Axis from a TH1F
double * getAxis(TH1F *iH) { 
  const int lNHBins = iH->GetNbinsX(); 
  double *lX = new double[lNHBins+1];
  for(int i0 = 1; i0 < iH->GetNbinsX()+2; i0++) { 
    lX[i0-1] = iH->GetXaxis()->GetBinLowEdge(i0);
  }
  return lX;
}
//Make a histogram from a TF1
TH1F* makeHist(TF1 *iFit,TH1F *iH,std::string iName) { 
  TH1F *lH = (TH1F*) iH->Clone(iName.c_str());
  for(int i0 = 0; i0 < lH->GetNbinsX()+1; i0++) lH->SetBinContent(i0,iFit->Eval(lH->GetXaxis()->GetBinCenter(i0)));
  for(int i0 = 0; i0 < lH->GetNbinsX()+1; i0++) lH->SetBinContent(i0,lH->GetBinContent(i0)*lH->GetXaxis()->GetBinWidth(i0));
  for(int i0 = 0; i0 < lH->GetNbinsX()+1; i0++) lH->SetBinError (i0,lH->GetBinError   (i0)*lH->GetXaxis()->GetBinWidth(i0));
  return lH;
}
//I would recommend to use the other version of the fit code
void addVarBinNuisance(std::string iFileName,std::string iChannel,std::string iBkg,std::string iEnergy,std::string iName,std::string iDir,bool iRebin=true,int iFitModel=0,double iFirst=200,double iLast=1500) { 
  std::cout << "======> " << iDir << "/" << iBkg << " -- " << iFileName << std::endl;  
  TFile *lFile = new TFile(iFileName.c_str());
  TH1F  *lH0   = (TH1F*) lFile->Get((iDir+"/"+iBkg).c_str());
  TH1F  *lData = (TH1F*) lFile->Get((iDir+"/data_obs").c_str());
  
  for(int i0 = 0; i0 < lH0->GetNbinsX()+1; i0++) lH0->SetBinContent(i0,lH0->GetBinContent(i0)/lH0->GetXaxis()->GetBinWidth(i0));
  for(int i0 = 0; i0 < lH0->GetNbinsX()+1; i0++) lH0->SetBinError  (i0,lH0->GetBinError  (i0)/lH0->GetXaxis()->GetBinWidth(i0));
  //Define the fit function
  double lFirst = iFirst;
  double lLast  = iLast;
  //TF1 *lFit = new TF1("Fit","[2]*exp(-x/([0]+[1]*x))",0,5000);
  TF1 *lFit = new TF1("expspec","[2]*exp(-x/([0]+[1]*x))",0,5000);
  if(iFitModel == 1) lFit  = new TF1("expspec","[2]*exp(-[0]*pow(x,[1]))",0,5000);
  lFit->SetParLimits(2,0,10000000); lFit->SetParameter(2,lH0->Integral()); 
  lFit->SetParLimits(0,  0,100);    lFit->SetParameter(0,20);
  lFit->SetParLimits(1,-10,10);     lFit->SetParameter(1,0);
  if(iFitModel == 1) lFit->SetParameter(0,0.3);
  if(iFitModel == 2) lFit->SetParameter(1,0.5);
  
  //TFitResultPtr  lFitPtr = lH0->Fit("expspec","SEWL","IR",lFirst,lLast);
  TFitResultPtr  lFitPtr = lH0->Fit("expspec","SER","R",lFirst,lLast);
  TMatrixDSym lCovMatrix   = lFitPtr->GetCovarianceMatrix();
  TMatrixD  lEigVecs(3,3);    lEigVecs = TMatrixDSymEigen(lCovMatrix).GetEigenVectors();
  TVectorD  lEigVals(3);      lEigVals = TMatrixDSymEigen(lCovMatrix).GetEigenValues();
  double lACentral = lFit->GetParameter(0); 
  double lBCentral = lFit->GetParameter(1);
  lEigVals(0) = sqrt(lEigVals(1));
  lEigVals(1) = sqrt(lEigVals(2));

  for(int i0 = 0; i0 < lH0->GetNbinsX()+1; i0++) lH0->SetBinContent(i0,lH0->GetBinContent(i0)*lH0->GetXaxis()->GetBinWidth(i0));
  for(int i0 = 0; i0 < lH0->GetNbinsX()+1; i0++) lH0->SetBinError  (i0,lH0->GetBinError  (i0)*lH0->GetXaxis()->GetBinWidth(i0));

  lEigVecs(0,0) = lEigVecs(0,1);
  lEigVecs(1,0) = lEigVecs(1,1);
  lEigVecs(0,1) = lEigVecs(0,2);
  lEigVecs(1,1) = lEigVecs(1,2);
  
  TH1F* lH     = makeHist(lFit,lH0,"Def");
  lFit->SetParameter(0,lACentral + lEigVals(0)*lEigVecs(0,0));
  lFit->SetParameter(1,lBCentral + lEigVals(0)*lEigVecs(1,0));
  TH1F* lHUp   = makeHist(lFit,lH0,"Up");
  lFit->SetParameter(0,lACentral - lEigVals(0)*lEigVecs(0,0));
  lFit->SetParameter(1,lBCentral - lEigVals(0)*lEigVecs(1,0));
  TH1F* lHDown = makeHist(lFit,lH0,"Down");

  lFit->SetParameter(0,lACentral + lEigVals(1)*lEigVecs(0,1));
  lFit->SetParameter(1,lBCentral + lEigVals(1)*lEigVecs(1,1));
  TH1F* lHUp1   = makeHist(lFit,lH0,"Up1");
  lFit->SetParameter(0,lACentral - lEigVals(1)*lEigVecs(0,1));
  lFit->SetParameter(1,lBCentral - lEigVals(1)*lEigVecs(1,1));
  TH1F* lHDown1 = makeHist(lFit,lH0,"Down1");
  
  //lFirst = 200;
  std::string lNuisance1 =  iBkg+"_"+"CMS_"+iName+"1_" + iChannel + "_" + iEnergy;
  std::string lNuisance2 =  iBkg+"_"+"CMS_"+iName+"2_" + iChannel + "_" + iEnergy;
  lHUp    = merge(lNuisance1 + "Up"   ,lFirst,lH0,lHUp);
  lHDown  = merge(lNuisance1 + "Down" ,lFirst,lH0,lHDown);
  lHUp1   = merge(lNuisance2 + "Up"   ,lFirst,lH0,lHUp1);
  lHDown1 = merge(lNuisance2 + "Down" ,lFirst,lH0,lHDown1);
  lH      = merge(lH0->GetName()      ,lFirst,lH0,lH);  
  if(iRebin) { 
    const int lNBins = lData->GetNbinsX();
    double *lAxis    = getAxis(lData);
    lH0     = rebin(lH0    ,lNBins,lAxis);
    lH      = rebin(lH     ,lNBins,lAxis);
    lHUp    = rebin(lHUp   ,lNBins,lAxis);
    lHDown  = rebin(lHDown ,lNBins,lAxis);
    lHUp1   = rebin(lHUp1  ,lNBins,lAxis);
    lHDown1 = rebin(lHDown1,lNBins,lAxis);
  }
  TFile *lOutFile =new TFile("Output.root","RECREATE");
  cloneFile(lOutFile,lFile,iDir+"/"+iBkg);
  lOutFile->cd(iDir.c_str());
  lH     ->Write();
  lHUp   ->Write(); 
  lHDown ->Write(); 
  lHUp1  ->Write(); 
  lHDown1->Write(); 

  // Debug Plots
  lH0    ->SetLineWidth(1); lH0->SetMarkerStyle(kFullCircle);
  lH     ->SetLineColor(kGreen);
  lHUp   ->SetLineColor(kRed);
  lHDown ->SetLineColor(kRed);
  lHUp1  ->SetLineColor(kBlue);
  lHDown1->SetLineColor(kBlue);
  TCanvas *lC0 = new TCanvas("Can","Can",800,600);
  lC0->Divide(1,2); lC0->cd();  lC0->cd(1)->SetPad(0,0.2,1.0,1.0); gPad->SetLeftMargin(0.2) ;  
  lH0->Draw();
  lH     ->Draw("hist sames");
  lHUp   ->Draw("hist sames");
  lHDown ->Draw("hist sames");
  lHUp1  ->Draw("hist sames");
  lHDown1->Draw("hist sames");
  gPad->SetLogy();
  lC0->cd(2)->SetPad(0,0,1.0,0.2); gPad->SetLeftMargin(0.2) ;
  drawDifference(lH0,lH,lHUp,lHDown,lHUp1,lHDown1);
  lC0->SaveAs((iBkg+"_"+"CMS_"+iName+"1_" + iDir + "_" + iEnergy+".png").c_str());
  //lFile->Close();
  return;
}
void addNuisance(std::string iFileName,std::string iChannel,std::string iBkg,std::string iEnergy,std::string iName,std::string iDir,bool iRebin=true,bool iVarBin=false,int iFitModel=1,double iFirst=150,double iLast=1500) { 
  std::cout << "======> " << iDir << "/" << iBkg << " -- " << iFileName << std::endl;  
  if(iVarBin) addVarBinNuisance(iFileName,iChannel,iBkg,iEnergy,iName,iDir,iRebin,iFitModel,iFirst,iLast);
  if(iVarBin) return;

  TFile *lFile = new TFile(iFileName.c_str());
  TH1F  *lH0   = (TH1F*) lFile->Get((iDir+"/"+iBkg).c_str());
  TH1F  *lData = (TH1F*) lFile->Get((iDir+"/data_obs").c_str());

  //Define the fit function
  RooRealVar lM("m","m" ,0,5000);   //lM.setBinning(lBinning);
  RooRealVar lA("a","a" ,50,  0.1,200);
  RooRealVar lB("b","b" ,50 , -10500,10500); //lB.setConstant(kTRUE);
  RooDataHist *pH0  =  new RooDataHist("Data","Data" ,RooArgList(lM),lH0);
  TString iStr = TString::Format("%.0f",iFirst);
  TString fn = "exp(-(m-"+iStr+")/(a+0.001*b*(m-"+iStr+")))";
  RooGenericPdf *lFit  = 0; lFit = new RooGenericPdf("genPdf",fn,RooArgList(lM,lA,lB));
  if(iFitModel == 1) lFit = new RooGenericPdf("genPdf","exp(-a*pow(m,0.001*b))",RooArgList(lM,lA,lB));
  if(iFitModel == 1) {lA.setVal(0.3); lB.setVal(0.5);}
  if(iFitModel == 2) lFit = new RooGenericPdf("genPdf","a*exp(0.001*b*m)",RooArgList(lM,lA,lB));
  if(iFitModel == 3) lFit = new RooGenericPdf("genPdf","a/pow(m,0.001*b)",RooArgList(lM,lA,lB));
  RooFitResult  *lRFit = 0;
  double lFirst = iFirst;
  double lLast  = iLast;
  //lRFit = lFit->chi2FitTo(*pH0,RooFit::Save(kTRUE),RooFit::Range(lFirst,lLast));
  lRFit = lFit->fitTo(*pH0,RooFit::Save(kTRUE),RooFit::Range(lFirst,lLast),RooFit::Strategy(0)); 
  TMatrixDSym lCovMatrix   = lRFit->covarianceMatrix(); 
  TMatrixD  lEigVecs(2,2);    lEigVecs = TMatrixDSymEigen(lCovMatrix).GetEigenVectors();
  TVectorD  lEigVals(2);      lEigVals = TMatrixDSymEigen(lCovMatrix).GetEigenValues();
  cout << " Ve---> " << lEigVecs(0,0) << " -- " << lEigVecs(1,0) << " -- " << lEigVecs(0,1) << " -- " << lEigVecs(1,1) << endl;
  cout << " Co---> " << lCovMatrix(0,0) << " -- " << lCovMatrix(1,0) << " -- " << lCovMatrix(0,1) << " -- " << lCovMatrix(1,1) << endl;
  double lACentral = lA.getVal();
  double lBCentral = lB.getVal();
  lEigVals(0) = sqrt(lEigVals(0));
  lEigVals(1) = sqrt(lEigVals(1));
  cout << "===> " << lEigVals(0) << " -- " << lEigVals(1) << endl;
  
  TH1F* lH     = (TH1F*) lFit->createHistogram("fit" ,lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));
  lA.setVal(lACentral + lEigVals(0)*lEigVecs(0,0));
  lB.setVal(lBCentral + lEigVals(0)*lEigVecs(1,0));
  TH1F* lHUp   = (TH1F*) lFit->createHistogram("Up"  ,lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));
  lA.setVal(lACentral - lEigVals(0)*lEigVecs(0,0));
  lB.setVal(lBCentral - lEigVals(0)*lEigVecs(1,0));
  TH1F* lHDown = (TH1F*) lFit->createHistogram("Down",lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));

  lA.setVal(lACentral + lEigVals(1)*lEigVecs(0,1));
  lB.setVal(lBCentral + lEigVals(1)*lEigVecs(1,1));
  TH1F* lHUp1   = (TH1F*) lFit->createHistogram("Up1",lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));
  lA.setVal(lACentral - lEigVals(1)*lEigVecs(0,1));
  lB.setVal(lBCentral - lEigVals(1)*lEigVecs(1,1));
  TH1F* lHDown1 = (TH1F*) lFit->createHistogram("Down1",lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));

  std::string lNuisance1 =  iBkg+"_"+"CMS_"+iName+"1_" + iChannel + "_" + iEnergy;
  std::string lNuisance2 =  iBkg+"_"+"CMS_"+iName+"2_" + iChannel + "_" + iEnergy;
  lHUp    = merge(lNuisance1 + "Up"   ,lFirst,lH0,lHUp);
  lHDown  = merge(lNuisance1 + "Down" ,lFirst,lH0,lHDown);
  lHUp1   = merge(lNuisance2 + "Up"   ,lFirst,lH0,lHUp1);
  lHDown1 = merge(lNuisance2 + "Down" ,lFirst,lH0,lHDown1);
  lH      = merge(lH0->GetName()      ,lFirst,lH0,lH);

  if(iRebin) { 
    const int lNBins = lData->GetNbinsX();
    double *lAxis    = getAxis(lData);
    lH0     = rebin(lH0    ,lNBins,lAxis);
    lH      = rebin(lH     ,lNBins,lAxis);
    lHUp    = rebin(lHUp   ,lNBins,lAxis);
    lHDown  = rebin(lHDown ,lNBins,lAxis);
    lHUp1   = rebin(lHUp1  ,lNBins,lAxis);
    lHDown1 = rebin(lHDown1,lNBins,lAxis);
  }

  // we dont need this bin errors since we do not use them (fit tails replaces bin-by-bin error!), therefore i set all errors to 0, this also saves us from modifying the add_bbb_error.py script in which I otherwise would have to include a option for adding bbb only in specific ranges
  int lMergeBin = lH->GetXaxis()->FindBin(iFirst);
  for(int i0 = lMergeBin; i0 < lH->GetNbinsX()+1; i0++){
    lH->SetBinError  (i0,0);
    lHUp->SetBinError  (i0,0);
    lHDown->SetBinError  (i0,0);
    lHUp1->SetBinError  (i0,0);
    lHDown1->SetBinError  (i0,0);
  }


  TFile *lOutFile =new TFile("Output.root","RECREATE");
  cloneFile(lOutFile,lFile,iDir+"/"+iBkg);
  lOutFile->cd(iDir.c_str());
  lH     ->Write();
  lHUp   ->Write(); 
  lHDown ->Write(); 
  lHUp1  ->Write(); 
  lHDown1->Write(); 

  // Debug Plots
  lH0->SetStats(0);
  lH->SetStats(0);
  lHUp->SetStats(0);
  lHDown->SetStats(0);
  lHUp1->SetStats(0);
  lHDown1->SetStats(0);
  lH0    ->SetLineWidth(1); lH0->SetMarkerStyle(kFullCircle);
  lH     ->SetLineColor(kGreen);
  lHUp   ->SetLineColor(kRed);
  lHDown ->SetLineColor(kRed);
  lHUp1  ->SetLineColor(kBlue);
  lHDown1->SetLineColor(kBlue);
  TCanvas *lC0 = new TCanvas("Can","Can",800,600);
  lC0->Divide(1,2); lC0->cd();  lC0->cd(1)->SetPad(0,0.2,1.0,1.0); gPad->SetLeftMargin(0.2) ; 
  lH0->Draw();
  lH     ->Draw("hist sames");
  lHUp   ->Draw("hist sames");
  lHDown ->Draw("hist sames");
  lHUp1  ->Draw("hist sames");
  lHDown1->Draw("hist sames");
  gPad->SetLogy();
  
  TLegend* leg1;
  /// setup the CMS Preliminary
  leg1 = new TLegend(0.7, 0.80, 1, 1); 
  leg1->SetBorderSize( 0 );
  leg1->SetFillStyle ( 1001 );
  leg1->SetFillColor (kWhite);
  leg1->AddEntry( lH0 , "orignal",  "PL" );
  leg1->AddEntry( lH , "cental fit",  "L" );
  leg1->AddEntry( lHUp , "shift1 up",  "L" );
  leg1->AddEntry( lHDown , "shift1 down",  "L" );
  leg1->AddEntry( lHUp1 , "shift2 up",  "L" );
  leg1->AddEntry( lHDown1 , "shift2 down",  "L" );
  leg1->Draw("same");


  lC0->cd(2)->SetPad(0,0,1.0,0.2); gPad->SetLeftMargin(0.2) ;
  drawDifference(lH0,lH,lHUp,lHDown,lHUp1,lHDown1);
  lH0->SetStats(0);
  lC0->Update();
  lC0->SaveAs((iBkg+"_"+"CMS_"+iName+"1_" + iDir + "_" + iEnergy+".png").c_str());
  //lFile->Close();
  return;
}
void addNuisanceWithToys(std::string iFileName,std::string iChannel,std::string iBkg,std::string iEnergy,std::string iName,std::string iDir,bool iRebin=true,bool iVarBin=false,int iFitModel=1,int iFitModel1=1,double iFirst=150,double iLast=1500,std::string iSigMass="800",double iSigScale=0.1,int iNToys=1000) { 
  std::cout << "======> " << iDir << "/" << iBkg << " -- " << iFileName << std::endl;  
  if(iVarBin) std::cout << "option not implemented yet!";
  if(iVarBin) return;
  //double lFirst = 200;
  //double lLast  = 1500;
  double lFirst = iFirst;
  double lLast  = iLast;

 // if (!iVerbose) {
    RooMsgService::instance().setStreamStatus(0,false);
    RooMsgService::instance().setStreamStatus(1,false);
    RooMsgService::instance().setSilentMode(true);
 // }
  std::cout << "===================================================================================================================================================" <<std::endl;
  std::cout << "Using Initial fit model: " << iFitModel << ", fitting range: " << iFirst << "-" << iLast << " , using alternative fit model: " << iFitModel1 << std::endl; 
  std::cout << "===================================================================================================================================================" <<std::endl;

  TFile *lFile = new TFile(iFileName.c_str());
  TH1F  *lH0   = (TH1F*) lFile->Get((iDir+"/"+iBkg).c_str());
  TH1F  *lData = (TH1F*) lFile->Get((iDir+"/data_obs").c_str());
  TH1F  *lSig = 0;

  // for now, use bbH signal for testing in b-tag and ggH in no-btag
  if(iDir.find("_btag") != std::string::npos) lSig = (TH1F*)lFile->Get((iDir+"/bbH"+iSigMass+"_fine_binning").c_str());
  else lSig = (TH1F*)lFile->Get((iDir+"/ggH"+iSigMass+"_fine_binning").c_str());

  TH1F *lH0Clone = (TH1F*)lH0->Clone("lH0Clone");     // binning too fine as of now? start by rebinning
  TH1F *lDataClone = (TH1F*)lData->Clone("lDataClone");   
  TH1F *lSigClone = (TH1F*)lSig->Clone("lSigClone");  
 // lH0Clone->Rebin(2);
 // lDataClone->Rebin(2);
 // lSigClone->Rebin(2);

  lSig->Rebin(10);  

  TString iStr = TString::Format("%.0f",iFirst);
  TString fn = "exp(-(m-"+iStr+")/(a+0.001*b*(m-"+iStr+")))";
  TString iStr1 = TString::Format("%.0f",iFirst);
  TString fn1 = "exp(-(m-"+iStr+")/(a1+0.001*b1*(m-"+iStr+")))";
  
  
  //Define the fit function
  RooRealVar lM("m","m" ,0,5000);
  lM.setRange(lFirst,lLast);
  RooRealVar lA("a","a" ,50,  0.1,200);
  RooRealVar lB("b","b" ,50 , -10500,10500);
  RooRealVar lA1("a1","a1" ,50,  0.1, 200);
  RooRealVar lB1("b1","b1" ,50 , -10500,10500);

  RooDataHist *pH0  =  new RooDataHist("Data","Data" ,RooArgList(lM),lH0);
  double lNB0 = lH0->Integral(lH0->FindBin(lFirst),lH0->FindBin(lLast));
  double lNSig0 = lSig->Integral(lSig->FindBin(lFirst),lSig->FindBin(lLast));
 //lNB0=500;
// lNSig0=500;
 lSig->Scale(iSigScale*lNB0/lNSig0);                                         // scale signal to iSigScale*(Background yield), could try other options
 lNSig0 = lSig->Integral(lSig->FindBin(lFirst),lSig->FindBin(lLast));        // readjust norm of signal hist   
  
  //Generate the "default" fit model 

  RooGenericPdf *lFit  = 0; lFit = new RooGenericPdf("genPdf",fn,RooArgList(lM,lA,lB));
  if(iFitModel == 1) lFit = new RooGenericPdf("genPdf","exp(-a*pow(m,0.001*b))",RooArgList(lM,lA,lB));
  if(iFitModel == 1) {lA.setVal(0.3); lB.setVal(0.5);}
  if(iFitModel == 2) lFit = new RooGenericPdf("genPdf","a*exp(0.001*b*m)",RooArgList(lM,lA,lB));
  //if(iFitModel == 2) {lA.setVal(0.01); lA.setRange(0,10); }
  if(iFitModel == 3) lFit = new RooGenericPdf("genPdf","a/pow(m,0.001*b)",RooArgList(lM,lA,lB));
 
  // Generate the alternative model
  
  RooGenericPdf *lFit1  = 0; lFit1 = new RooGenericPdf("genPdf",fn1,RooArgList(lM,lA1,lB1));
  if(iFitModel1 == 1) lFit1 = new RooGenericPdf("genPdf","exp(-a1*pow(m,0.001*b1))",RooArgList(lM,lA1,lB1));
  if(iFitModel1 == 1) {lA1.setVal(0.3); lB1.setVal(0.5);}
  if(iFitModel1 == 2) lFit1 = new RooGenericPdf("genPdf","a1*exp(0.001*b1*m)",RooArgList(lM,lA1,lB1));
  //if(iFitModel1 == 2) {lA1.setVal(0.01); lA1.setRange(0,10); }
  if(iFitModel1 == 3) lFit1 = new RooGenericPdf("genPdf","a1/pow(m,0.001*b1)",RooArgList(lM,lA1,lB1));
  
  //=============================================================================================================================================
  //Perform the tail fit and generate the shift up and down histograms
  //=============================================================================================================================================

  RooFitResult  *lRFit = 0;
  lRFit = lFit->fitTo(*pH0,RooFit::Save(kTRUE),RooFit::Range(lFirst,lLast),RooFit::Strategy(0)); 
  TMatrixDSym lCovMatrix   = lRFit->covarianceMatrix(); 
  TMatrixD  lEigVecs(2,2);    lEigVecs = TMatrixDSymEigen(lCovMatrix).GetEigenVectors();
  TVectorD  lEigVals(2);      lEigVals = TMatrixDSymEigen(lCovMatrix).GetEigenValues();
  cout << " Ve---> " << lEigVecs(0,0) << " -- " << lEigVecs(1,0) << " -- " << lEigVecs(0,1) << " -- " << lEigVecs(1,1) << endl;
  cout << " Co---> " << lCovMatrix(0,0) << " -- " << lCovMatrix(1,0) << " -- " << lCovMatrix(0,1) << " -- " << lCovMatrix(1,1) << endl;
  double lACentral = lA.getVal();
  double lBCentral = lB.getVal();
  lEigVals(0) = sqrt(lEigVals(0));
  lEigVals(1) = sqrt(lEigVals(1));
  cout << "===> " << lEigVals(0) << " -- " << lEigVals(1) << endl;
  
  TH1F* lH     = (TH1F*) lFit->createHistogram("fit" ,lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));

  lA.setVal(lACentral + lEigVals(0)*lEigVecs(0,0));
  lB.setVal(lBCentral + lEigVals(0)*lEigVecs(1,0));
  TH1F* lHUp   = (TH1F*) lFit->createHistogram("Up"  ,lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));

  lA.setVal(lACentral - lEigVals(0)*lEigVecs(0,0));
  lB.setVal(lBCentral - lEigVals(0)*lEigVecs(1,0));
  TH1F* lHDown = (TH1F*) lFit->createHistogram("Down",lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));

  lA.setVal(lACentral + lEigVals(1)*lEigVecs(0,1));
  lB.setVal(lBCentral + lEigVals(1)*lEigVecs(1,1));
  TH1F* lHUp1   = (TH1F*) lFit->createHistogram("Up1",lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));

  lA.setVal(lACentral - lEigVals(1)*lEigVecs(0,1));
  lB.setVal(lBCentral - lEigVals(1)*lEigVecs(1,1));
  TH1F* lHDown1 = (TH1F*) lFit->createHistogram("Down1",lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));

  std::string lNuisance1 =  iBkg+"_"+"CMS_"+iName+"1_" + iChannel + "_" + iEnergy;
  std::string lNuisance2 =  iBkg+"_"+"CMS_"+iName+"2_" + iChannel + "_" + iEnergy;
  lHUp    = merge(lNuisance1 + "Up"   ,lFirst,lH0,lHUp);
  lHDown  = merge(lNuisance1 + "Down" ,lFirst,lH0,lHDown);
  lHUp1   = merge(lNuisance2 + "Up"   ,lFirst,lH0,lHUp1);
  lHDown1 = merge(lNuisance2 + "Down" ,lFirst,lH0,lHDown1);
  lH      = merge(lH0->GetName()      ,lFirst,lH0,lH);

  //=============================================================================================================================================
  //=============================================================================================================================================
  
  //Set the variables A and B to the final central values from the tail fit

  lA.setVal(lACentral);
  lB.setVal(lBCentral);
 // lA.removeRange();
 // lB.removeRange();
 
  //Generate the background pdf corresponding to the final result of the tail fit
 
 RooGenericPdf *lFitFinal  = 0; lFitFinal = new RooGenericPdf("genPdf",fn,RooArgList(lM,lA,lB));
  if(iFitModel == 1) lFitFinal = new RooGenericPdf("genPdf","exp(-a*pow(m,0.001*b))",RooArgList(lM,lA,lB));
  //if(iFitModel == 2) lFitFinal = new RooGenericPdf("genPdf","a*exp(b*m)",RooArgList(lM,lA,lB));
  if(iFitModel == 2) lFitFinal = new RooGenericPdf("genPdf","exp(0.001*b*m)",RooArgList(lM,lB));
  if(iFitModel == 3) lFitFinal = new RooGenericPdf("genPdf","1/pow(m,0.001*b)",RooArgList(lM,lB));
  if(iFitModel == 4) lFitFinal = new RooGenericPdf("genPdf","exp(a+0.001*b*m)",RooArgList(lA,lM,lB));



  //=============================================================================================================================================
  //Perform the tail fit with the alternative fit function (once initially, before allowing tail fit to float in toy fit).
  //=============================================================================================================================================

  RooFitResult  *lRFit1 = 0;
 //lRFit1=lFit1->fitTo(*pH0,RooFit::Save(kTRUE),RooFit::Range(iFirst,iLast),RooFit::Strategy(0));  
 lRFit1=lFit1->fitTo(*pH0,RooFit::Save(kTRUE),RooFit::Range(200,1500),RooFit::Strategy(0));  
  
  //Generate the background pdf corresponding to the result of the alternative tail fit

  RooGenericPdf *lFit1Final  = 0; lFit1Final = new RooGenericPdf("genPdf",fn1,RooArgList(lM,lA1,lB1));
  if(iFitModel1 == 1) lFit1Final = new RooGenericPdf("genPdf","exp(-a1*pow(m,0.001*b1))",RooArgList(lM,lA1,lB1));
  if(iFitModel1 == 2) lFit1Final = new RooGenericPdf("genPdf","exp(0.001*b1*m)",RooArgList(lM,lB1));
  if(iFitModel1 == 3) lFit1Final = new RooGenericPdf("genPdf","1/pow(m,0.001*b1)",RooArgList(lM,lB1));
  if(iFitModel1 == 4) lFit1Final = new RooGenericPdf("genPdf","exp(a1+0.001*b1*m)",RooArgList(lM,lA1,lB1));

 // lA1.removeRange();
 // lB1.removeRange();
  
  //=============================================================================================================================================

  //Define RooRealVar for the normalization of the signal and background, starting from the initial integral of the input histograms

  lM.setRange(300,1500);  

  RooRealVar lNB("nb","nb",lNB0,0,10000);
  RooRealVar lNSig("nsig","nsig",lNSig0,-1000,1000);

  //Define a PDF for the signal histogram lSig
  
  RooDataHist  *pS      = new RooDataHist("sigH","sigH",RooArgList(lM),lSig);
  RooHistPdf   *lSPdf   = new RooHistPdf ("sigPdf","sigPdf",lM,*pS);
 
  //Define generator and fit functions for the RooMCStudy

  RooAddPdf    *lGenMod = new RooAddPdf  ("genmod","genmod",RooArgList(*lFitFinal ,*lSPdf),RooArgList(lNB,lNSig));
  RooAddPdf    *lFitMod = new RooAddPdf  ("fitmod","fitmod",RooArgList(*lFit1Final,*lSPdf),RooArgList(lNB,lNSig));

  //Generate plot of the signal and background models going into the toy generation   

  RooPlot* plot=lM.frame();
  lGenMod->plotOn(plot);
  lGenMod->plotOn(plot,RooFit::Components(*lSPdf),RooFit::LineColor(2));
  TCanvas* lC11 = new TCanvas("pdf","pdf",600,600) ;
  lC11->cd();
  plot->Draw();
  lC11->SaveAs(("SBModel_"+iBkg+"_" + iDir + "_" + iEnergy+".pdf").c_str());

  std::cout << "===================================================================================================================================================" <<std::endl;
  std::cout << "FIT PARAMETERS BEFORE ROOMCSTUDY: lA: " << lA.getVal() << " lB: " << lB.getVal() << " lA1: " << lA1.getVal() << " lB1: " << lB1.getVal() << std::endl;  
  std::cout << "===================================================================================================================================================" <<std::endl;


  RooMCStudy   *lToy    = new RooMCStudy(*lGenMod,lM,RooFit::FitModel(*lFitMod),RooFit::Binned(kTRUE),RooFit::Silence(),RooFit::Extended(kTRUE),RooFit::Verbose(kTRUE),RooFit::FitOptions(RooFit::Save(kTRUE),RooFit::Strategy(0)));

  // Generate and fit iNToys toy samples
  
  std::cout << "Number of background events: " << lNB0 << " Number of signal events: " << lNSig0 << " Sum: " << lNB0+lNSig0 << std::endl;
  
  //=============================================================================================================================================
  // Generate and fit toys
  //============================================================================================================================================= 
   
    lToy->generateAndFit(iNToys,lNB0+lNSig0,kTRUE);

  std::cout << "===================================================================================================================================================" <<std::endl;
  std::cout << "FIT PARAMETERS AFTER ROOMCSTUDY: lA: " << lA.getVal() << " lB: " << lB.getVal() << " lA1: " << lA1.getVal() << " lB1: " << lB1.getVal() << std::endl;  
  std::cout << "===================================================================================================================================================" <<std::endl;
  

  //=============================================================================================================================================
  // Generate plots relevant to the toy fit
  //=============================================================================================================================================

  RooPlot* lFrame1 = lToy->plotPull(lNSig,-5,5,100,kTRUE);
  lFrame1->SetTitle("distribution of pulls on signal yield from toys");
  lFrame1->SetXTitle("N_{sig} pull");
  
  TCanvas* lC00 = new TCanvas("pulls","pulls",600,600) ;
  lC00->cd();
  lFrame1->GetYaxis()->SetTitleOffset(1.2); 
  lFrame1->GetXaxis()->SetTitleOffset(1.0); 
  lFrame1->Draw() ;
  lC00->SaveAs(("sig_pulls_toyfits_"+iBkg+"_" + iDir + "_" + iEnergy+".png").c_str());

/*  RooPlot* lFrame2 = lToy->plotParam(lA1);
  lFrame2->SetTitle("distribution of values of parameter 1 (a) after toy fit");
  lFrame2->SetXTitle("Parameter 1 (a)");
  TCanvas* lC01 = new TCanvas("valA","valA",600,600) ;
  lFrame2->Draw() ;
  lC01->SaveAs(("valA_toyfits_"+iBkg+"_" + iDir + "_" + iEnergy+".png").c_str());
*/
  RooPlot* lFrame3 = lToy->plotParam(lB1);
  lFrame3->SetTitle("distribution of values of parameter 2 (b) after toy fit");
  lFrame3->SetXTitle("Parameter 2 (b)");
  TCanvas* lC02 = new TCanvas("valB","valB",600,600) ;
  lFrame3->Draw() ;
  lC02->SaveAs(("valB_toyfits_"+iBkg+"_" + iDir + "_" + iEnergy+".png").c_str());
  
  RooPlot* lFrame6 = lToy->plotNLL(0,1000,100);
  lFrame6->SetTitle("-log(L)");
  lFrame6->SetXTitle("-log(L)");
  TCanvas* lC05 = new TCanvas("logl","logl",600,600) ;
  lFrame6->Draw() ;
  lC05->SaveAs(("logL_toyfits_"+iBkg+"_" + iDir + "_" + iEnergy+".png").c_str());

  RooPlot* lFrame7 = lToy->plotParam(lNSig);
  lFrame7->SetTitle("distribution of values of N_{sig} after toy fit");
  lFrame7->SetXTitle("N_{sig}");
  TCanvas* lC06 = new TCanvas("Nsig","Nsig",600,600) ;
  lFrame7->Draw() ;
  lC06->SaveAs(("NSig_toyfits_"+iBkg+"_" + iDir + "_" + iEnergy+".png").c_str());
  
  RooPlot* lFrame8 = lToy->plotParam(lNB);
  lFrame8->SetTitle("distribution of values of N_{bkg} after toy fit");
  lFrame8->SetXTitle("N_{bkg}");
  TCanvas* lC07 = new TCanvas("Nbkg","Nbkg",600,600) ;
  lFrame8->Draw() ;
  lC07->SaveAs(("Nbkg_toyfits_"+iBkg+"_" + iDir + "_" + iEnergy+".png").c_str());
 

  if(iRebin) { 
    const int lNBins = lData->GetNbinsX();
    double *lAxis    = getAxis(lData);
    lH0     = rebin(lH0    ,lNBins,lAxis);
    lH      = rebin(lH     ,lNBins,lAxis);
    lHUp    = rebin(lHUp   ,lNBins,lAxis);
    lHDown  = rebin(lHDown ,lNBins,lAxis);
    lHUp1   = rebin(lHUp1  ,lNBins,lAxis);
    lHDown1 = rebin(lHDown1,lNBins,lAxis);
  }

  // we dont need this bin errors since we do not use them (fit tails replaces bin-by-bin error!), therefore i set all errors to 0, this also saves us from modifying the add_bbb_error.py script in which I otherwise would have to include a option for adding bbb only in specific ranges
  int lMergeBin = lH->GetXaxis()->FindBin(iFirst);
  for(int i0 = lMergeBin; i0 < lH->GetNbinsX()+1; i0++){
    lH->SetBinError  (i0,0);
    lHUp->SetBinError  (i0,0);
    lHDown->SetBinError  (i0,0);
    lHUp1->SetBinError  (i0,0);
    lHDown1->SetBinError  (i0,0);
  }


  TFile *lOutFile =new TFile("Output.root","RECREATE");
  cloneFile(lOutFile,lFile,iDir+"/"+iBkg);
  lOutFile->cd(iDir.c_str());
  lH     ->Write();
  lHUp   ->Write(); 
  lHDown ->Write(); 
  lHUp1  ->Write(); 
  lHDown1->Write(); 

  // Debug Plots
  lH0->SetStats(0);
  lH->SetStats(0);
  lHUp->SetStats(0);
  lHDown->SetStats(0);
  lHUp1->SetStats(0);
  lHDown1->SetStats(0);
  lH0    ->SetLineWidth(1); lH0->SetMarkerStyle(kFullCircle);
  lH     ->SetLineColor(kGreen);
  lHUp   ->SetLineColor(kRed);
  lHDown ->SetLineColor(kRed);
  lHUp1  ->SetLineColor(kBlue);
  lHDown1->SetLineColor(kBlue);
  TCanvas *lC0 = new TCanvas("Can","Can",800,600);
  lC0->Divide(1,2); lC0->cd();  lC0->cd(1)->SetPad(0,0.2,1.0,1.0); gPad->SetLeftMargin(0.2) ; 
  lH0->Draw();
  lH     ->Draw("hist sames");
  lHUp   ->Draw("hist sames");
  lHDown ->Draw("hist sames");
  lHUp1  ->Draw("hist sames");
  lHDown1->Draw("hist sames");
  gPad->SetLogy();
  
  TLegend* leg1;
  /// setup the CMS Preliminary
  leg1 = new TLegend(0.7, 0.80, 1, 1); 
  leg1->SetBorderSize( 0 );
  leg1->SetFillStyle ( 1001 );
  leg1->SetFillColor (kWhite);
  leg1->AddEntry( lH0 , "orignal",  "PL" );
  leg1->AddEntry( lH , "cental fit",  "L" );
  leg1->AddEntry( lHUp , "shift1 up",  "L" );
  leg1->AddEntry( lHDown , "shift1 down",  "L" );
  leg1->AddEntry( lHUp1 , "shift2 up",  "L" );
  leg1->AddEntry( lHDown1 , "shift2 down",  "L" );
  leg1->Draw("same");


  lC0->cd(2)->SetPad(0,0,1.0,0.2); gPad->SetLeftMargin(0.2) ;
  drawDifference(lH0,lH,lHUp,lHDown,lHUp1,lHDown1);
  lH0->SetStats(0);
  lC0->Update();
  lC0->SaveAs((iBkg+"_"+"CMS_"+iName+"1_" + iDir + "_" + iEnergy+".png").c_str());
  //lFile->Close();
  return;
}
//void addFitNuisance(std::string iFileName="test.root",std::string iChannel="muTau",std::string iBkg="W",std::string iEnergy="8TeV",std::string iName="shift",std::string iCategory="9",double iFirst=150,int iFitModel=1,bool iVarBin=true,bool iRebin=true) { 
void addFitNuisanceBiasStudy(std::string iFileName="test.root",std::string iChannel="emu",std::string iBkg="ttbar_fine_binning",std::string iEnergy="8TeV",std::string iName="shift",std::string iCategory="9",double iFirst=150,double iLast=1500,int iFitModel=0,int iFitModel1=0,bool iVarBin=false,bool iRebin=false,std::string iSigMass="800",double iSigScale=0.1,int iNToys=1000) { 
  // Also possible old MSSM categorization (for testing)
  if(iCategory=="0") addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_0jet_low"  ,iRebin,iVarBin,iFitModel,iFirst);
  if(iCategory=="1") addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_0jet_high" ,iRebin,iVarBin,iFitModel,iFirst);
  if(iCategory=="2") addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_boost_low" ,iRebin,iVarBin,iFitModel,iFirst);
  if(iCategory=="3") addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_boost_high",iRebin,iVarBin,iFitModel,iFirst);
  if(iCategory=="6") addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_btag_low"  ,iRebin,iVarBin,iFitModel,iFirst);
  if(iCategory=="7") addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_btag_high" ,iRebin,iVarBin,iFitModel,iFirst);
  if(iCategory=="8") addNuisanceWithToys          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_nobtag"    ,iRebin,iVarBin,iFitModel,iFitModel1,iFirst,iLast,iSigMass,iSigScale,iNToys); // run toys with injected signal
  if(iCategory=="9") addNuisanceWithToys          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_btag"      ,iRebin,iVarBin,iFitModel,iFitModel1,iFirst,iLast,iSigMass,iSigScale,iNToys); // run toys with injected signal
}
