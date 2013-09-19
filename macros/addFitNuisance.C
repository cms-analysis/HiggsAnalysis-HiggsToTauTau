#include <iostream>
#include "TROOT.h"
#include "TFile.h"
#include "TKey.h"
#include "TF1.h"
#include "TFitResult.h"
#include "TFitResultPtr.h"
#include "TH1F.h"
#include "TMath.h"
#include "TPaveText.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "RooBinning.h"                                                                                                                                                               
#include "RooPlot.h"                                                                                                                                                               
#include "RooRealVar.h"   
#include "RooDataHist.h"   
#include "RooDataSet.h"    
#include "RooHistPdf.h"     
#include "RooGenericPdf.h"
#include "RooFitResult.h"
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
      if(pFullName == iSkipHist || pFullName == iSkipHist2) {
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
  cout << "====> Merging " << iName << endl;
  TH1F *lH = (TH1F*) iH->Clone(iName.c_str());
  lH->SetFillStyle(0);
  int lMergeBin = iH->GetXaxis()->FindBin(iMergePoint);
  //double lVal  = iH->GetBinContent(lMergeBin);
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
  lHDiffL ->SetLineColor(iHL ->GetLineColor());
  lHDiffL ->SetLineStyle(iHL ->GetLineStyle());
  lHDiffL ->SetLineWidth(iHL ->GetLineWidth());
  lHDiffH ->SetLineColor(iHH ->GetLineColor());
  lHDiffH ->SetLineStyle(iHH ->GetLineStyle());
  lHDiffH ->SetLineWidth(iHH ->GetLineWidth());
  lHDiffL1->SetLineColor(iHL1->GetLineColor());
  lHDiffL1->SetLineStyle(iHL1->GetLineStyle());
  lHDiffL1->SetLineWidth(iHL1->GetLineWidth());
  lHDiffH1->SetLineColor(iHH1->GetLineColor());
  lHDiffH1->SetLineStyle(iHH1->GetLineStyle());
  lHDiffH1->SetLineWidth(iHH1->GetLineWidth());
  TH1F *lXHDiff1 = new TH1F((lName+"XDiff1").c_str(),(lName+"XDiff1").c_str(),iH0->GetNbinsX(),iH0->GetXaxis()->GetXmin(),iH0->GetXaxis()->GetXmax());
  TH1F *lXHDiff2 = new TH1F((lName+"XDiff2").c_str(),(lName+"XDiff2").c_str(),iH0->GetNbinsX(),iH0->GetXaxis()->GetXmin(),iH0->GetXaxis()->GetXmax());
  int i1 = 0;
  lXHDiff1->SetLineWidth(1); lXHDiff1->SetLineColor(kGreen+2);
  lXHDiff2->SetLineWidth(1); lXHDiff2->SetLineColor(kGreen+2);

  lXHDiff1->SetTitle(0);  
  lXHDiff1->GetYaxis()->SetTitle("Ratio");
  lXHDiff1->GetYaxis()->SetRangeUser(0.2,1.8);
  lXHDiff1->GetYaxis()->SetTitleOffset(0.3);
  lXHDiff1->GetYaxis()->SetTitleSize(0.2);
  lXHDiff1->GetYaxis()->SetLabelSize(0.11);
  lXHDiff1->GetXaxis()->SetLabelSize(0);
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
    if(iH1->GetBinContent(i0) > 0) lHDiff->SetBinError(i0,iH0->GetBinError(i0) /(iH1->GetBinContent(i0)) );
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
int addNuisance(std::string iFileName,std::string iChannel,std::string iBkg,std::string iEnergy,std::string iName,std::string iDir,bool iVerbose=false,bool iVarBin=false,int iFitModel=1,double iFirst=150,double iLast=1500,bool addUncerts=true,bool iTestMode=false) {
  if (!iVerbose) {
    RooMsgService::instance().setStreamStatus(0,false);
    RooMsgService::instance().setStreamStatus(1,false);
    RooMsgService::instance().setSilentMode(true);
  }
  std::cout << "======> " << iDir << "/" << iBkg << " -- " << iFileName << std::endl;  
  if(iVarBin) addVarBinNuisance(iFileName,iChannel,iBkg,iEnergy,iName,iDir,true,iFitModel,iFirst,iLast);
  if(iVarBin) return 1;

  TFile *lFile = new TFile(iFileName.c_str());
  TH1F  *lH0   = (TH1F*) lFile->Get((iDir+"/"+iBkg).c_str());
  TH1F  *lData = (TH1F*) lFile->Get((iDir+"/data_obs").c_str());

  //Define the fit function
  RooRealVar lM("m","m" ,0,5000);   //lM.setBinning(lBinning);
  RooRealVar lA("a","a" ,50,  0.1,200);
  RooRealVar lB("b","b" ,50 , -10500,10500); //lB.setConstant(kTRUE);
  RooDataHist *pH0  =  new RooDataHist("Data","Data" ,RooArgList(lM),lH0);
  TString iStr = TString::Format("%.0f",iFirst);
  //std::cout << iStr << std::endl;
  TString fn = "exp(-(m-"+iStr+")/(a+0.001*b*(m-"+iStr+")))";
  //std::cout << fn << std::endl;
  RooGenericPdf *lFit  = 0; lFit = new RooGenericPdf("genPdf",fn,RooArgList(lM,lA,lB));
  if(iFitModel == 1) lFit = new RooGenericPdf("genPdf","exp(-a*pow(m,b))",RooArgList(lM,lA,lB));
  if(iFitModel == 1) {lA.setVal(0.3); lB.setVal(0.5);}
  if(iFitModel == 2) lFit = new RooGenericPdf("genPdf","a*exp(b*m)",RooArgList(lM,lA,lB));
  if(iFitModel == 3) lFit = new RooGenericPdf("genPdf","a/pow(m,b)",RooArgList(lM,lA,lB));
  if(iFitModel == 4) lFit = new RooGenericPdf("genPdf","a*pow(m,b)",RooArgList(lM,lA,lB));
  if(iFitModel == 5) lFit = new RooGenericPdf("genPdf","a*exp(pow(m,b))",RooArgList(lM,lA,lB));
  RooFitResult  *lRFit = 0;
  double lFirst = iFirst;
  double lLast  = iLast;
  //lRFit = lFit->chi2FitTo(*pH0,RooFit::Save(kTRUE),RooFit::Range(lFirst,lLast));
  lRFit = lFit->fitTo(*pH0,RooFit::Save(kTRUE),RooFit::Range(lFirst,lLast),RooFit::Strategy(0)); 
  
  //std::cout << lRFit->status() << " " <<  lRFit->covQual() << std::endl;
  if(!(lRFit->status()==0 && lRFit->covQual()==3))
  {
      std::cerr << "===============================================================================" << std::endl;
      std::cerr << "Tail fit has not succeeded. Datacard and uncertainty files will not be altered." << std::endl;
      std::cerr << "===============================================================================" << std::endl;
      return 1;
  }

  TMatrixDSym lCovMatrix   = lRFit->covarianceMatrix(); 
  TMatrixD  lEigVecs(2,2);    lEigVecs = TMatrixDSymEigen(lCovMatrix).GetEigenVectors();
  TVectorD  lEigVals(2);      lEigVals = TMatrixDSymEigen(lCovMatrix).GetEigenValues();
  cout << " Eigenvectors ---> " << lEigVecs(0,0) << " -- " << lEigVecs(1,0) << " -- " << lEigVecs(0,1) << " -- " << lEigVecs(1,1) << endl;
  cout << " Covariance matrix ---> " << lCovMatrix(0,0) << " -- " << lCovMatrix(1,0) << " -- " << lCovMatrix(0,1) << " -- " << lCovMatrix(1,1) << endl;
  double lACentral = lA.getVal();
  double lBCentral = lB.getVal();
  lEigVals(0) = sqrt(lEigVals(0));
  lEigVals(1) = sqrt(lEigVals(1));
  cout << "Eigenvalues ===> " << lEigVals(0) << " -- " << lEigVals(1) << endl;
    
  lM.setRange(lFirst,2000);
  lA.removeRange();
  lB.removeRange();

  //GENERATION OF SHIFT UP/DOWN HISTOGRAMS

  //Add some flags for possible infinite points in the histograms. 
  bool flagcentral=false;  
  bool flag1up=false;  
  bool flag1down=false;  
  bool flag2up=false;  
  bool flag2down=false; 
    
  //CENTRAL HISTOGRAM   
  cout << "Values for central hist: " << " A: " << lA.getVal() << " B: " << lB.getVal() << endl;
  lM.setRange(0,2000);
  
  double mcentral=(-1 * lA.getVal() / lB.getVal() );
  if(iFitModel==0 && lFirst < mcentral && mcentral < 2000)
  {
      flagcentral=true;
      std::cout << "===============================================================================" << std::endl;
      std::cout << "Infinite point found in central histogram at mass of " << mcentral << ". Truncating the histogram before that point, setting all bins after to zero." << std::endl;
      std::cout << "===============================================================================" << std::endl;
      lM.setRange(0,lH0->GetBinLowEdge(lH0->FindBin(mcentral)));
  }
  TH1F* lH=0, *lHtemp=0;
  if(!flagcentral) lH = (TH1F*) lFit->createHistogram("fit" ,lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));
  else lHtemp=(TH1F*) lFit->createHistogram("fit" ,lM,RooFit::Binning(lH0->FindBin(mcentral),lH0->GetXaxis()->GetXmin(),lH0->GetBinLowEdge(lH0->FindBin(mcentral))));
  
  //SHIFT1UP HISTOGRAM   
  
  lA.setVal(lACentral + lEigVals(0)*lEigVecs(0,0));
  lB.setVal(lBCentral + lEigVals(0)*lEigVecs(1,0));
  
  if(iVerbose) cout << "Values for shift 1 up hist: " << " A: " << lA.getVal() << " B: " << lB.getVal() << endl;
  lM.setRange(0,2000);
  
  double mshift1up=(-1 * lA.getVal() / lB.getVal() );
  
  if(iFitModel == 0 && lFirst < mshift1up && mshift1up < 2000)
  {
      flag1up=true;
      std::cout << "===============================================================================" << std::endl;
      std::cout << "Infinite point found in shift 1 up histogram at mass of " << mshift1up << ". Truncating the histogram before that point, setting all bins after to zero." << std::endl;
      std::cout << "===============================================================================" << std::endl;
      lM.setRange(0,lH0->GetBinLowEdge(lH0->FindBin(mshift1up)));
  }
  TH1F* lHUp=0, *lHUptemp=0;
  if(!flag1up) lHUp= (TH1F*) lFit->createHistogram("Up"  ,lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));
  else lHUptemp=(TH1F*) lFit->createHistogram("Up" ,lM,RooFit::Binning((lH0->FindBin(mshift1up))-1,lH0->GetXaxis()->GetXmin(),lH0->GetBinLowEdge(lH0->FindBin(mshift1up))));

  lA.setVal(lACentral - lEigVals(0)*lEigVecs(0,0));
  lB.setVal(lBCentral - lEigVals(0)*lEigVecs(1,0));
  
  //SHIFT1DOWN HISTOGRAM   
  
  if(iVerbose) cout << "Values for shift 1 down hist: " << " A: " << lA.getVal() << " B: " << lB.getVal() << endl;
  lM.setRange(0,2000);
  
  double mshift1down=(-1 * lA.getVal() / lB.getVal() );
  
  if(iFitModel == 0 && lFirst < mshift1down && mshift1down < 2000)
  {
      flag1down=true;
      std::cout << "===============================================================================" << std::endl;
      std::cout << "Infinite point found in shift 1 down histogram at mass of " << mshift1down << ". Truncating the histogram before that point, setting all bins after to zero." << std::endl;
      std::cout << "===============================================================================" << std::endl;
      lM.setRange(0,lH0->GetBinLowEdge(lH0->FindBin(mshift1down)));
  }
  TH1F* lHDown=0, *lHDowntemp=0;
  if(!flag1down) lHDown = (TH1F*) lFit->createHistogram("Down",lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));
  else lHDowntemp=(TH1F*) lFit->createHistogram("Down" ,lM,RooFit::Binning(lH0->FindBin(mshift1down),lH0->GetXaxis()->GetXmin(),lH0->GetBinLowEdge(lH0->FindBin(mshift1down))));

  lA.setVal(lACentral + lEigVals(1)*lEigVecs(0,1));
  lB.setVal(lBCentral + lEigVals(1)*lEigVecs(1,1));
  
  //SHIFT2UP HISTOGRAM   
  
  if(iVerbose) cout << "Values for shift 2 up hist: " << " A: " << lA.getVal() << " B: " << lB.getVal() << endl;
  lM.setRange(0,2000);
  
  double mshift2up=(-1 * lA.getVal() / lB.getVal() );
  
  if(iFitModel==0 && lFirst < mshift2up && mshift2up < 2000)
  {
      flag2up=true;
      std::cout << "===============================================================================" << std::endl;
      std::cout << "Infinite point found in shift 2 up histogram at mass of " << mshift2up << ". Truncating the histogram before that point, setting all bins after to zero." << std::endl;
      std::cout << "===============================================================================" << std::endl;
      lM.setRange(0,lH0->GetBinLowEdge(lH0->FindBin(mshift2up)));
  }
  TH1F* lHUp1=0, *lHUp1temp=0;
  if(!flag2up) lHUp1   = (TH1F*) lFit->createHistogram("Up1",lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));
  else lHUp1temp=(TH1F*) lFit->createHistogram("Up1" ,lM,RooFit::Binning(lH0->FindBin(mshift2up),lH0->GetXaxis()->GetXmin(),lH0->GetBinLowEdge(lH0->FindBin(mshift2up))));
  
  lA.setVal(lACentral - lEigVals(1)*lEigVecs(0,1));
  lB.setVal(lBCentral - lEigVals(1)*lEigVecs(1,1));
  
  //SHIFT2DOWN HISTOGRAM   
  
  if(iVerbose) cout << "Values for shift 2 down hist: " << " A: " << lA.getVal() << " B: " << lB.getVal() << endl;
  lM.setRange(0,2000);
  
  double mshift2down=(-1 * lA.getVal() / lB.getVal() );
  
  if( iFitModel == 0 && lFirst < mshift2down && mshift2down < 2000)
  {
      flag2down=true;
      std::cout << "===============================================================================" << std::endl;
      std::cout << "Infinite point found in shift 2 down histogram at mass of " << mshift2down << ". Truncating the histogram before that point, setting all bins after to zero." << std::endl;
      std::cout << "===============================================================================" << std::endl;
      lM.setRange(0,lH0->GetBinLowEdge(lH0->FindBin(mshift2down)));
  }
  TH1F* lHDown1=0, *lHDown1temp=0;
  if(!flag2down) lHDown1= (TH1F*) lFit->createHistogram("Down1",lM,RooFit::Binning(lH0->GetNbinsX(),lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax()));
  else lHDown1temp=(TH1F*) lFit->createHistogram("Down1" ,lM,RooFit::Binning(lH0->FindBin(mshift2down),lH0->GetXaxis()->GetXmin(),lH0->GetBinLowEdge(lH0->FindBin(mshift2down))));
 
 //IF FLAGS HAVE BEEN SET, MERGE WITH EMPTY HISTOGRAM TO FILL THE EMPTY BINS AFTER TRUNCATION POINT
  if(flagcentral)
  {
      TH1F* base0 = new TH1F("base0", "base0", lH0->GetNbinsX(), lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax() );
      for(int i=1; i<=lHtemp->GetNbinsX(); i++)
      {
          base0->Fill(lHtemp->GetBinCenter(i),lHtemp->GetBinContent(i));
      }
      lH=base0;
      lM.setRange(lFirst,2000);
  }
  if(flag1up)
  {
      TH1F* base1 = new TH1F("base1", "base1", lH0->GetNbinsX(), lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax() );
      for(int i=1; i<=lHUptemp->GetNbinsX(); i++)
      {
          base1->Fill(lHUptemp->GetBinCenter(i),lHUptemp->GetBinContent(i));
      }
      lHUp=base1;
      lM.setRange(lFirst,2000);
  }
  if(flag1down)
  {
      TH1F* base2 = new TH1F("base2", "base2", lH0->GetNbinsX(), lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax() );
      for(int i=1; i<=lHDowntemp->GetNbinsX(); i++)
      {
          base2->Fill(lHDowntemp->GetBinCenter(i),lHDowntemp->GetBinContent(i));
      }
      lHDown=base2;
      lM.setRange(lFirst,2000);
  }
  if(flag2up)
  {
      TH1F* base3 = new TH1F("base3", "base3", lH0->GetNbinsX(), lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax() );
      for(int i=1; i<=lHUp1temp->GetNbinsX(); i++)
      {
          base3->Fill(lHUp1temp->GetBinCenter(i),lHUp1temp->GetBinContent(i));
      }
      lHUp1=base3;
      lM.setRange(lFirst,2000);
  }
  if(flag2down)
  {
      TH1F* base4 = new TH1F("base4", "base4", lH0->GetNbinsX(), lH0->GetXaxis()->GetXmin(),lH0->GetXaxis()->GetXmax() );
      for(int i=1; i<=lHDown1temp->GetNbinsX(); i++)
      {
          base4->Fill(lHDown1temp->GetBinCenter(i),lHDown1temp->GetBinContent(i));
      }
      lHDown1=base4;
      lM.setRange(lFirst,2000);
  }

  std::string lNuisance1 =  iBkg+"_"+"CMS_"+iName+"1_" + iDir + "_" + iEnergy + "_" + iBkg;
  std::string lNuisance2 =  iBkg+"_"+"CMS_"+iName+"2_" + iDir + "_" + iEnergy + "_" + iBkg;
  lHUp    = merge(lNuisance1 + "Up"   ,lFirst,lH0,lHUp);
  lHDown  = merge(lNuisance1 + "Down" ,lFirst,lH0,lHDown);
  lHUp1   = merge(lNuisance2 + "Up"   ,lFirst,lH0,lHUp1);
  lHDown1 = merge(lNuisance2 + "Down" ,lFirst,lH0,lHDown1);
  lH      = merge(lH0->GetName()      ,lFirst,lH0,lH);

  
  
  double I1=lHUp->Integral(lHUp->FindBin(lFirst), lHUp->FindBin(2000));  
  double I2=lHDown->Integral(lHDown->FindBin(lFirst), lHDown->FindBin(2000));  
  double I3=lHUp1->Integral(lHUp1->FindBin(lFirst), lHUp1->FindBin(2000));  
  double I4=lHDown1->Integral(lHDown1->FindBin(lFirst), lHDown1->FindBin(2000)); 
  

  //If verbosity is set make plot showing the shift up/down/central functions prior to rebinning
  if(iVerbose)
  {
    lH0->SetStats(0);
    lH->SetStats(0);
    lHUp->SetStats(0);
    lHDown->SetStats(0);
    lHUp1->SetStats(0);
    lHDown1->SetStats(0);
    lH0    ->SetLineWidth(1); lH0->SetMarkerStyle(kFullCircle);
    lH     ->SetLineColor(kGreen+2);
    lHUp   ->SetLineColor(kRed);
    lHUp   ->SetLineStyle(9);
    lHDown ->SetLineColor(kRed+2);
    lHDown ->SetLineStyle(3);
    lHDown ->SetLineWidth(2);
    lHUp1  ->SetLineColor(kBlue);
    lHUp1  ->SetLineStyle(9);
    lHDown1->SetLineColor(kBlue+2);
    lHDown1->SetLineStyle(3);
    lHDown1->SetLineWidth(2);
    lH0->SetTitle(0);
    lH0->GetXaxis()->SetTitle("m_{#tau#tau} [GeV]");
    lH0->GetXaxis()->SetTitleSize(0.05);
    lH0->GetYaxis()->SetTitle("dN/dm_{#tau#tau} [1/GeV]");
    lH0->GetYaxis()->SetTitleSize(0.05);
    lH0->GetYaxis()->SetTitleOffset(1.2);
    lH0->GetYaxis()->SetLabelSize(0.0275);

    TCanvas *lC0Fine = new TCanvas("CanFine","CanFine",800,600);
    lC0Fine->Divide(1,2); lC0Fine->cd();  lC0Fine->cd(1)->SetPad(0,0.2,1.0,1.0); gPad->SetLeftMargin(0.2) ; 
    lH0    ->Scale(1.0,"width");
    lH     ->Scale(1.0,"width");
    lHUp   ->Scale(1.0,"width");
    lHDown ->Scale(1.0,"width");
    lHUp1  ->Scale(1.0,"width");
    lHDown1->Scale(1.0,"width");
    lH0->Draw();
    lH     ->Draw("hist sames");
    lHUp   ->Draw("hist sames");
    lHDown ->Draw("hist sames");
    lHUp1  ->Draw("hist sames");
    lHDown1->Draw("hist sames");
    gPad->SetLogy();
  
    TLegend* leg2;
    /// setup the CMS Preliminary
    leg2 = new TLegend(0.6, 0.65, 0.9, 0.89); 
    leg2->SetBorderSize( 0 );
    leg2->SetFillStyle ( 1001 );
    leg2->SetFillColor (kWhite);
    leg2->AddEntry( lH0 , "original",  "PL" );
    leg2->AddEntry( lH , "central fit",  "L" );
    leg2->AddEntry( lHUp , "shift1 up",  "L" );
    leg2->AddEntry( lHDown , "shift1 down",  "L" );
    leg2->AddEntry( lHUp1 , "shift2 up",  "L" );
    leg2->AddEntry( lHDown1 , "shift2 down",  "L" );
    leg2->Draw("same");
  
    lC0Fine->cd(2)->SetPad(0,0,1.0,0.2); gPad->SetLeftMargin(0.2) ;
    drawDifference(lH0,lH,lHUp,lHDown,lHUp1,lHDown1);
    lH0->SetStats(0);
    lC0Fine->Update();
    lC0Fine->SaveAs((iBkg+"_"+"CMS_"+iName+"1_" + iDir + "_" + iEnergy+"_Finebin.png").c_str());
    lC0Fine->SaveAs((iBkg+"_"+"CMS_"+iName+"1_" + iDir + "_" + iEnergy+"_Finebin.pdf").c_str());

  }
  
  //Check if the shift up/down histograms are integrable. If not terminate the script here.
  if(addUncerts && (I1 != I1 || I2 != I2 || I3 != I3 || I4 != I4))
  {
      std::cerr << "===============================================================================" << std::endl;
      std::cerr << "Tail fit has succeeded, but 1 or more of the shift up/down histograms is not integrable." << std::endl;
      std::cerr << "Script will terminate here without altering datacard. Turn on --verbose option to see the problem histogram." << std::endl; 
      std::cerr << "===============================================================================" << std::endl;
      return 1;
  }

    
  //Rebin the histograms   
  const int lNBins = lData->GetNbinsX();
  double *lAxis    = getAxis(lData);
  lH0     = rebin(lH0    ,lNBins,lAxis);
  lH      = rebin(lH     ,lNBins,lAxis);
  lHUp    = rebin(lHUp   ,lNBins,lAxis);
  lHDown  = rebin(lHDown ,lNBins,lAxis);
  lHUp1   = rebin(lHUp1  ,lNBins,lAxis);
  lHDown1 = rebin(lHDown1,lNBins,lAxis);
 
  //Clone the fit result and original template for computing the chi2 and KS probability of the fit
  TH1F *lHclone = (TH1F*) lH->Clone(); 
  TH1F *lH0clone =(TH1F*) lH0->Clone(); 
  for(unsigned i=1; i<lData->FindBin(lFirst); i++)
  {
       lHclone->SetBinContent(i, 0.0);
       lH0clone->SetBinContent(i, 0.0);
       lHclone->SetBinError(i, 0.0);
       lH0clone->SetBinError(i, 0.0);
  }
  //Compute the KS probability
 double kstest=lHclone->KolmogorovTest(lH0clone);
 //For the chi2 probability, remove bins with no entry in the original template as this screws up the chi2 calculation
  for(unsigned i=lData->FindBin(lFirst); i<=lData->FindBin(2000); i++)
  {
       if(lH0clone->GetBinContent(i)==0)
       {
            lHclone->SetBinContent(i, 0.0);
            //lH0clone->SetBinContent(i, 0.0);
            lHclone->SetBinError(i, 0.0);
            lH0clone->SetBinError(i, 0.0);
       }
  }
 double chi2test= lHclone->Chi2Test(lH0clone, "WW");

 if(iVerbose)
 {
    std::cout << "==========================================================================================================" << std::endl;
    std::cout << "Result of chi2 probability test: " <<  chi2test << ", KS probability test: " << kstest << std::endl;
    std::cout << "==========================================================================================================" << std::endl;
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
    
  //Save the rebinned templates to the datacard root file

  TFile *lOutFile =new TFile("Output.root","RECREATE");
  cloneFile(lOutFile,lFile,iDir+"/"+iBkg);
  lOutFile->cd(iDir.c_str());
  lH->Write();
  if(addUncerts){
    lHUp   ->Write(); 
    lHDown ->Write(); 
    lHUp1  ->Write(); 
    lHDown1->Write(); 
  }

  // Make the plot showing shift up/down/central templates, rebinned as in datacard

  lH0->SetStats(0);
  lH->SetStats(0);
  lHUp->SetStats(0);
  lHDown->SetStats(0);
  lHUp1->SetStats(0);
  lHDown1->SetStats(0);
  lH0    ->SetLineWidth(1); lH0->SetMarkerStyle(kFullCircle);
  lH     ->SetLineColor(kGreen+2);
  lHUp   ->SetLineColor(kRed);
  lHUp   ->SetLineStyle(9);
  lHDown ->SetLineColor(kRed+2);
  lHDown ->SetLineStyle(3);
  lHDown ->SetLineWidth(2);
  lHUp1  ->SetLineColor(kBlue);
  lHUp1  ->SetLineStyle(9);
  lHDown1->SetLineColor(kBlue+2);
  lHDown1->SetLineStyle(3);
  lHDown1->SetLineWidth(2);
  lH0->SetTitle(0);
  lH0->GetXaxis()->SetTitle("m_{#tau#tau} [GeV]");
  lH0->GetXaxis()->SetTitleSize(0.05);
  lH0->GetYaxis()->SetTitle("dN/dm_{#tau#tau} [1/GeV]");
  lH0->GetYaxis()->SetTitleSize(0.05);
  lH0->GetYaxis()->SetTitleOffset(1.2);
  lH0->GetYaxis()->SetLabelSize(0.0275);

  TCanvas *lC0 = new TCanvas("Can","Can",800,600);
  lC0->Divide(1,2); lC0->cd();  lC0->cd(1)->SetPad(0,0.2,1.0,1.0); gPad->SetLeftMargin(0.2) ; 
  lH0    ->Scale(1.0,"width");
  lH     ->Scale(1.0,"width");
  lHUp   ->Scale(1.0,"width");
  lHDown ->Scale(1.0,"width");
  lHUp1  ->Scale(1.0,"width");
  lHDown1->Scale(1.0,"width");
  lH0->Draw();
  lH     ->Draw("hist sames");
  lHUp   ->Draw("hist sames");
  lHDown ->Draw("hist sames");
  lHUp1  ->Draw("hist sames");
  lHDown1->Draw("hist sames");
  gPad->SetLogy();
  
  TLegend* leg1;
  /// setup the CMS Preliminary
  leg1 = new TLegend(0.6, 0.65, 0.9, 0.89); 
  leg1->SetBorderSize( 0 );
  leg1->SetFillStyle ( 1001 );
  leg1->SetFillColor (kWhite);
  leg1->AddEntry( lH0 , "original",  "PL" );
  leg1->AddEntry( lH , "central fit",  "L" );
  leg1->AddEntry( lHUp , "shift1 up",  "L" );
  leg1->AddEntry( lHDown , "shift1 down",  "L" );
  leg1->AddEntry( lHUp1 , "shift2 up",  "L" );
  leg1->AddEntry( lHDown1 , "shift2 down",  "L" );
  leg1->Draw("same");
  
  TPaveText* stat1 = new TPaveText(0.20, 0.90, 0.50, 0.99, "NDC");
  stat1->SetBorderSize(   0 );
  stat1->SetFillStyle(    0 );
  stat1->SetTextAlign(   12 );
  stat1->SetTextSize ( 0.05 );
  stat1->SetTextColor(    1 );
  stat1->SetTextFont (   62 );
  stat1->AddText(TString::Format("P(#chi^{2})=%.5f, P(KS)=%.5f", chi2test, kstest));
  stat1->Draw();
  
  lC0->cd(2)->SetPad(0,0,1.0,0.2); gPad->SetLeftMargin(0.2) ;
  drawDifference(lH0,lH,lHUp,lHDown,lHUp1,lHDown1);
  lH0->SetStats(0);
  lC0->Update();
  lC0->SaveAs((iBkg+"_"+"CMS_"+iName+"1_" + iDir + "_" + iEnergy+"_Rebin.png").c_str());
  lC0->SaveAs((iBkg+"_"+"CMS_"+iName+"1_" + iDir + "_" + iEnergy+"_Rebin.pdf").c_str());

  //Make additional output plots of shift up and down histos if verbosity is set  

  if(iVerbose)
  {
 
    TCanvas *lC1 = new TCanvas("Can1","Can1",800,600);
    lHUp->Draw();
    //gPad->SetLogy();
    lC1->SaveAs((iBkg+"_"+"CMS_"+iName+"1_" + iDir + "_" + iEnergy+"_Shift1Up.png").c_str());
    lC1->SaveAs((iBkg+"_"+"CMS_"+iName+"1_" + iDir + "_" + iEnergy+"_Shift1Up.pdf").c_str());
      
    TCanvas *lC2 = new TCanvas("Can2","Can2",800,600);
    lHDown->Draw();
    // gPad->SetLogy();
    lC2->SaveAs((iBkg+"_"+"CMS_"+iName+"1_" + iDir + "_" + iEnergy+"_Shift1Down.png").c_str());
    lC2->SaveAs((iBkg+"_"+"CMS_"+iName+"1_" + iDir + "_" + iEnergy+"_Shift1Down.pdf").c_str());
      
    TCanvas *lC3 = new TCanvas("Can3","Can3",800,600);
    lHUp1->Draw();
    // gPad->SetLogy();
    lC3->SaveAs((iBkg+"_"+"CMS_"+iName+"1_" + iDir + "_" + iEnergy+"_Shift2Up.png").c_str());
    lC3->SaveAs((iBkg+"_"+"CMS_"+iName+"1_" + iDir + "_" + iEnergy+"_Shift2Up.pdf").c_str());
      
    TCanvas *lC4 = new TCanvas("Can4","Can4",800,600);
    lHDown1->Draw();
    // gPad->SetLogy();
    lC4->SaveAs((iBkg+"_"+"CMS_"+iName+"1_" + iDir + "_" + iEnergy+"_Shift2Down.png").c_str());
    lC4->SaveAs((iBkg+"_"+"CMS_"+iName+"1_" + iDir + "_" + iEnergy+"_Shift2Down.pdf").c_str());
 }
  

  lA.setVal(lACentral);  
  lB.setVal(lBCentral);  

  lM.setRange(lFirst,2000); 
  TCanvas* c1 = new TCanvas("c1","c1",600,600);
  RooPlot* mframe = lM.frame(RooFit::Name("mframe"),RooFit::Title("Tail fit in fit range"));
  pH0->plotOn(mframe, RooFit::Name("data"), RooFit::MarkerColor(kBlack));
  lFit->plotOn(mframe, RooFit::Name("model"), RooFit::DrawOption("L"), RooFit::Range(lFirst,2000));
  lFit->plotOn(mframe, RooFit::Components(*lFit), RooFit::LineColor(kRed), RooFit::Range(lFirst,2000));
  mframe->GetYaxis()->SetRangeUser(0,lH0->GetBinContent(lH0->FindBin(lFirst)));
  mframe->Draw();
  Double_t chi2 = mframe->chiSquare();
  Double_t ndoff = mframe->GetNbinsX();
  std::cout << "==========================================================================================================" << std::endl;
  std::cout << "Goodness of fit: " << chi2/ndoff << " with statistics in fit range: " << lH0->Integral(lH0->FindBin(lFirst),lH0->FindBin(2000)) << std::endl;
  std::cout << "==========================================================================================================" << std::endl;
 
 //If verbosity is set also output the fit function just in the tail fit range, no log scale 
 if(iVerbose) c1->SaveAs((iBkg+"_"+"CMS_"+iName+"1_" + iDir + "_" + iEnergy+"_Function.png").c_str());
 if(iVerbose) c1->SaveAs((iBkg+"_"+"CMS_"+iName+"1_" + iDir + "_" + iEnergy+"_Function.pdf").c_str());

 if(iTestMode)
 {
     std::cout << "Running in test mode. Script will exit now without altering datacard or uncertainty files." << std::endl;
     return 1;
 }

  return 0;
}

int addFitNuisance(std::string iFileName="test.root",std::string iChannel="muTau",std::string iBkg="W",std::string iEnergy="8TeV",std::string iName="shift",std::string iCategory="9",double iFirst=150,double iLast=1500,int iFitModel=1,bool iVerbose=true,bool iVarBin=false,bool addUncerts=true,bool iTestMode=false) { 
  // Also possible old MSSM categorization (for testing)
  if(iCategory=="0") return addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_0jet_low"  ,iVerbose,iVarBin,iFitModel,iFirst,iLast,addUncerts,iTestMode);
  if(iCategory=="1") return addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_0jet_high" ,iVerbose,iVarBin,iFitModel,iFirst,iLast,addUncerts,iTestMode);
  if(iCategory=="2") return addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_boost_low" ,iVerbose,iVarBin,iFitModel,iFirst,iLast,addUncerts,iTestMode);
  if(iCategory=="3") return addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_boost_high",iVerbose,iVarBin,iFitModel,iFirst,iLast,addUncerts,iTestMode);
  if(iCategory=="6") return addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_btag_low"  ,iVerbose,iVarBin,iFitModel,iFirst,iLast,addUncerts,iTestMode);
  if(iCategory=="7") return addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_btag_high" ,iVerbose,iVarBin,iFitModel,iFirst,iLast,addUncerts,iTestMode);
  if(iCategory=="8") return addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_nobtag"    ,iVerbose,iVarBin,iFitModel,iFirst,iLast,addUncerts,iTestMode);
  if(iCategory=="9") return addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_btag"      ,iVerbose,iVarBin,iFitModel,iFirst,iLast,addUncerts,iTestMode);
  return 0;
}
