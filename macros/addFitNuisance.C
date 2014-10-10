#include <iostream>
#include <TROOT.h>
#include <TFile.h>
#include <TKey.h>
#include <TF1.h>
#include <TFitResult.h>
#include <TFitResultPtr.h>
#include <TH1F.h>
#include <TMath.h>
#include <TPaveText.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <RooBinning.h>                                                                                                                                                               
#include <RooPlot.h>                                                                                                                                                               
#include <RooRealVar.h>   
#include <RooConstVar.h>  
#include <RooDataHist.h>   
#include <RooDataSet.h>    
#include <RooHistPdf.h>     
#include <RooGenericPdf.h>
#include <RooGaussian.h>
#include <RooFitResult.h>
#include <RooCmdArg.h>
#include <TMatrixDSym.h>
#include <TMatrixDSymEigen.h>
#include <TGraphAsymmErrors.h>

using namespace RooFit;

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
  std::cout << "====> Merging " << iName << std::endl;
  TH1F *lH = (TH1F*) iH->Clone(iName.c_str());
  lH->SetFillStyle(0);
  int lMergeBin = iH->GetXaxis()->FindBin(iMergePoint);
  //double lVal  = iH->GetBinContent(lMergeBin);
  //iFunc->Scale(lVal/iFunc->GetBinContent(lMergeBin));
  std::cout << "iH->Integral(lMergeBin, iH->GetXaxis()->FindBin(1500)) = " << iH->Integral(lMergeBin, iH->GetXaxis()->FindBin(1500)) << std::endl;
  std::cout << "iFunc->Integral(lMergeBin, iFunc->GetXaxis()->FindBin(1500)) = " << iFunc->Integral(lMergeBin, iFunc->GetXaxis()->FindBin(1500)) << std::endl;
  iFunc->Scale( (iH->Integral(lMergeBin, iH->GetXaxis()->FindBin(1500))) / (iFunc->Integral(lMergeBin, iFunc->GetXaxis()->FindBin(1500)) )); // felix - last fit bin = 1500; this approach seems to work much better
  for(int i0 = 0;         i0 < lMergeBin;         i0++) lH->SetBinContent(i0,iH->GetBinContent(i0));
  for(int i0 = lMergeBin; i0 < iH->GetNbinsX()+1; i0++) lH->SetBinContent(i0,iFunc->GetBinContent(iFunc->GetXaxis()->FindBin(lH->GetXaxis()->GetBinCenter(i0))));
  for(int i0 = 0;         i0 < iH->GetNbinsX()+1; i0++) {
    std::cout << "bin #" << i0 << " (x = " << lH->GetBinCenter(i0) << ") = " << lH->GetBinContent(i0) << std::endl;
  }
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
   //if(iH1->GetBinContent(i0) > 0)  std::cout << "unc" << lXVal << " -- " << sqrt(lXVal)/(iH1->GetBinContent(i0)) << std::endl;
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
  std::cout << "====> makeHist " << iName << std::endl;
  TH1F *lH = (TH1F*) iH->Clone(iName.c_str());
  for(int i0 = 0; i0 < lH->GetNbinsX()+1; i0++) {
    std::cout << "bin #" << i0 << " (x = " << lH->GetBinCenter(i0) << ") = " << iFit->Eval(lH->GetXaxis()->GetBinCenter(i0)) << std::endl;
  }
  for(int i0 = 0; i0 < lH->GetNbinsX()+1; i0++) lH->SetBinContent(i0,iFit->Eval(lH->GetXaxis()->GetBinCenter(i0)));
  for(int i0 = 0; i0 < lH->GetNbinsX()+1; i0++) lH->SetBinContent(i0,lH->GetBinContent(i0)*lH->GetXaxis()->GetBinWidth(i0));
  for(int i0 = 0; i0 < lH->GetNbinsX()+1; i0++) lH->SetBinError (i0,lH->GetBinError   (i0)*lH->GetXaxis()->GetBinWidth(i0));
  return lH;
}
//I would recommend to use the other version of the fit code
void addVarBinNuisance(const std::string& iFileName, 
		       const std::string& iChannel, const std::string& iBkg, const std::string& iEnergy, const std::string& iName, const std::string& iDir,
		       bool iRebin = true, int iFitModel = 0, double iFirst = 200, double iLast = 1500) 
{ 
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
  TCanvas *lC0 = new TCanvas("Can","Can",800,750);
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
TH1F* makeHist2(const std::string& histogramName, TH1F* histogram_original, double par0, double par1, int fitModel, double xMin_fit, double xMax, double x0, 
		double& sf, double k = 1, TH1F* template_central = 0, double* sf_central = 0)
{
  //std::cout << "<makeHist2>:" << std::endl;
  //std::cout << " histogramName = " << histogramName << std::endl; 
  //std::cout << " par0 = " << par0 << ", par1 = " << par1 << std::endl;
  //std::cout << " range = " << xMin_fit << ".." << xMax << std::endl;
  
  TF1* tempFit = 0;
  if ( fitModel == 0 ) {
    tempFit = new TF1("tempFit", "TMath::Exp(-(x - [2])/([0] + 0.001*[1]*(x - ([2] + [3]))))", xMin_fit, xMax);
    tempFit->SetParameter(0, par0);
    tempFit->SetParameter(1, par1);
    tempFit->SetParameter(2, xMin_fit);
    tempFit->SetParameter(3, x0);
  } else if ( fitModel == 1 ) {
    tempFit = new TF1("tempFit", "TMath::Exp(-(x - [2])/([0]*(1.0 + 0.001*[1]*(x - ([2] + [3])))))", xMin_fit, xMax);
    tempFit->SetParameter(0, par0);
    tempFit->SetParameter(1, par1);
    tempFit->SetParameter(2, xMin_fit);
    tempFit->SetParameter(3, x0);
  } else {
    std::cerr << "Fit model = " << fitModel << " not supported !!" << std::endl;
    assert(0);
  }
  //std::cout << "tempFit = " << tempFit->GetTitle() << std::endl;
  //for ( double x = xMin_fit; x < xMax; x += 100. ) {
  //  std::cout << "tempFit(" << x << ") = " << tempFit->Eval(x) << std::endl;
  //}

  TH1F* histogram_fitted = (TH1F*)histogram_original->Clone(histogramName.c_str());
  histogram_fitted->Reset();
  if ( !histogram_fitted->GetSumw2N() ) histogram_fitted->Sumw2();
  double integral_original = histogram_original->Integral(histogram_original->FindBin(xMin_fit), histogram_original->FindBin(xMax));
  double tempFit_integral = tempFit->Integral(xMin_fit, xMax);
  //std::cout << "integral: original = " << integral_original << ", fit = " << tempFit_integral << std::endl;
  sf = integral_original/tempFit_integral;
  //std::cout << "sf = " << sf << std::endl;
  if ( sf_central ) { // CV: if this line is enabled the fit parameter uncertainties will affect not only the shape, but also the yield
    if ( sf > 0.5*(*sf_central) ) sf = (*sf_central);
  }
  TAxis* xAxis = histogram_original->GetXaxis();
  for ( int iBin = 1; iBin <= xAxis->GetNbins(); ++iBin ) {
    double binCenter   = xAxis->GetBinCenter(iBin);
    double binEdgeLow  = xAxis->GetBinLowEdge(iBin);
    double binEdgeHigh = xAxis->GetBinUpEdge(iBin);
    if ( binCenter > xMin_fit ) {
      const double epsilon = 1.e-6;
      if ( binEdgeHigh < (xMax + epsilon) ) {
	if ( k != 1. && template_central ) histogram_fitted->SetBinContent(iBin, k*sf*tempFit->Integral(binEdgeLow, binEdgeHigh) - (k - 1.)*template_central->GetBinContent(iBin));
	else histogram_fitted->SetBinContent(iBin, sf*tempFit->Integral(binEdgeLow, binEdgeHigh));
      } else {
	histogram_fitted->SetBinContent(iBin, 0.);
      }
    } else {
      histogram_fitted->SetBinContent(iBin, histogram_original->GetBinContent(iBin));
      histogram_fitted->SetBinError(iBin, histogram_original->GetBinError(iBin));
    }
    //std::cout << "bin #" << iBin << " (x = " << histogram_fitted->GetBinCenter(iBin) << ": " << histogram_fitted->GetBinContent(iBin) << " +/- " << histogram_fitted->GetBinError(iBin) << std::endl;
  }
  histogram_fitted->SetBinContent(0, histogram_original->GetBinContent(0));
  histogram_fitted->SetBinError(0, histogram_original->GetBinError(0));
  histogram_fitted->SetBinContent(xAxis->GetNbins() + 1, 0.);

  return histogram_fitted;
}
void fixHist(TH1* histogram_template, double xMin_fit, const TH1* histogram_coarse_binning)
{
  TAxis* xAxis_template = histogram_template->GetXaxis();
  TAxis* xAxis_coarse_binning = histogram_coarse_binning->GetXaxis();
  int numBins = xAxis_coarse_binning->GetNbins();
  for ( int iBin = 1; iBin <= numBins; ++iBin ) {
    double xLowEdge_template = xAxis_template->GetBinLowEdge(iBin);
    double xCenter_template = xAxis_template->GetBinCenter(iBin);
    double xUpEdge_template = xAxis_template->GetBinUpEdge(iBin);
    if ( xCenter_template > xMin_fit ) continue;

    double xLowEdge_coarse_binning = xAxis_coarse_binning->GetBinLowEdge(iBin);
    double xCenter_coarse_binning = xAxis_coarse_binning->GetBinCenter(iBin);
    double xUpEdge_coarse_binning = xAxis_coarse_binning->GetBinUpEdge(iBin);
    if ( xCenter_coarse_binning > xMin_fit ) continue;

    if ( TMath::Abs(xLowEdge_template - xLowEdge_coarse_binning) < 1.e-3*(xLowEdge_template + xLowEdge_coarse_binning) &&
	 TMath::Abs(xUpEdge_template  - xUpEdge_coarse_binning)  < 1.e-3*(xUpEdge_template  + xUpEdge_coarse_binning)  ) {
      histogram_template->SetBinContent(iBin, histogram_coarse_binning->GetBinContent(iBin));
      histogram_template->SetBinError(iBin, histogram_coarse_binning->GetBinError(iBin));
    }
  }
}

int addNuisance(const std::string& iFileName, 
		const std::string& iChannel, const std::string& iBkg, const std::string& iEnergy, const std::string& iName, const std::string& iDir, 
		int iVerbose = false, bool iVarBin = false, int iFitModel = 1, int iErrorOption = 0, double iFirst = 150, double iLast = 1500, bool addUncerts = true, bool iTestMode = false) 
{
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
  std::cout << "fn = " << fn << std::endl;
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
  //lRFit = lFit->chi2FitTo(*pH0,Save(kTRUE),Range(lFirst,lLast));
  lRFit = lFit->fitTo(*pH0,Save(kTRUE),Range(lFirst,lLast),Strategy(0)); 
  
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
  std::cout << " Eigenvectors ---> " << lEigVecs(0,0) << " -- " << lEigVecs(1,0) << " -- " << lEigVecs(0,1) << " -- " << lEigVecs(1,1) << std::endl;
  std::cout << " Covariance matrix ---> " << lCovMatrix(0,0) << " -- " << lCovMatrix(1,0) << " -- " << lCovMatrix(0,1) << " -- " << lCovMatrix(1,1) << std::endl;
  double lACentral = lA.getVal();
  double lBCentral = lB.getVal();
  lEigVals(0) = sqrt(lEigVals(0));
  lEigVals(1) = sqrt(lEigVals(1));
  std::cout << "Eigenvalues ===> " << lEigVals(0) << " -- " << lEigVals(1) << std::endl;
    
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
  std::cout << "Values for central hist: " << " A: " << lA.getVal() << " B: " << lB.getVal() << std::endl;
  lM.setRange(0,2000);
  
  double mcentral=(-1 * lA.getVal() / lB.getVal() );
  std::cout << "mcentral = " << mcentral << std::endl;
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
  
  if(iVerbose) std::cout << "Values for shift 1 up hist: " << " A: " << lA.getVal() << " B: " << lB.getVal() << std::endl;
  lM.setRange(0,2000);
  
  double mshift1up=(-1 * lA.getVal() / lB.getVal() );
  std::cout << "mshift1up = " << mshift1up << std::endl;
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
  TF1* tempFit = new TF1("tempFit","TMath::Exp(-(x-[0])/([1]+0.001*[2]*(x-[0])))",0.,2000.);
  tempFit->SetParameter(0, iFirst);
  tempFit->SetParameter(1, lA.getVal());
  tempFit->SetParameter(2, lB.getVal());
  for(int i0 = 1; i0 <= lH0->GetNbinsX()+1; i0++) {
    std::cout << "bin #" << i0 << " (x = " << lH0->GetBinCenter(i0) << ") = " << tempFit->Eval(lH0->GetXaxis()->GetBinCenter(i0)) << std::endl;
  }

  lA.setVal(lACentral - lEigVals(0)*lEigVecs(0,0));
  lB.setVal(lBCentral - lEigVals(0)*lEigVecs(1,0));
  
  //SHIFT1DOWN HISTOGRAM   
  
  if(iVerbose) std::cout << "Values for shift 1 down hist: " << " A: " << lA.getVal() << " B: " << lB.getVal() << std::endl;
  lM.setRange(0,2000);
  
  double mshift1down=(-1 * lA.getVal() / lB.getVal() );
  std::cout << "mshift1down = " << mshift1down << std::endl;
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
  
  if(iVerbose) std::cout << "Values for shift 2 up hist: " << " A: " << lA.getVal() << " B: " << lB.getVal() << std::endl;
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
  
  if(iVerbose) std::cout << "Values for shift 2 down hist: " << " A: " << lA.getVal() << " B: " << lB.getVal() << std::endl;
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
  std::cout << "I1 = " << I1 << ", I2 = " << I2 << ", I3 = " << I3 << ", I4 = " << I4 << std::endl;

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

    TCanvas *lC0Fine = new TCanvas("CanFine","CanFine",800,750);
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
    leg2 = new TLegend(0.7, 0.64, 0.89, 0.88); 
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

  TCanvas *lC0 = new TCanvas("Can","Can",800,750);
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
  leg1 = new TLegend(0.7, 0.64, 0.89, 0.88); 
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
  TCanvas* c1 = new TCanvas("c1","c1",800,750);
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
void checkForInfinitePoints2(int fitModel, double xMin_fit, double xMax_fit, double x0, const std::string& central_or_shift, double par0, double par1, bool& flag, double& xInfinitePoint, bool silent = false)
{
  if ( fitModel == 0 ) {
    xInfinitePoint = xMin_fit + x0 - par0/(0.001*par1);
  } else if ( fitModel == 1 ) {
    xInfinitePoint = xMin_fit + x0 - 1.0/(0.001*par1);
  } else {
    std::cerr << "Fit model = " << fitModel << " not supported !!" << std::endl;
    assert(0);
  }
  if ( !silent) {
    std::cout << "Parameter values for " << central_or_shift << " histogram: par0 = " << par0 << ", par1 = " << par1 << std::endl;
    std::cout << central_or_shift << ": xInfinitePoint = " << xInfinitePoint << std::endl;
  }
  if ( xInfinitePoint > xMin_fit && xInfinitePoint < xMax_fit ) {
    if ( !silent) {
      std::cout << "===============================================================================" << std::endl;
      std::cout << "Infinite point found in " << central_or_shift << " histogram at mass of " << xInfinitePoint << "." << std::endl;
      std::cout << "Truncating the histogram before that point, setting all bins after to zero." << std::endl;
      std::cout << "===============================================================================" << std::endl;
    }
    flag = true;
  } else {
    if ( xInfinitePoint < xMin_fit) xInfinitePoint = 1.e+6; // CV: no need to worry if infinite point is outside fitted range
    flag = false;
  }
}
void refitShift(const std::string& fitFunction_formula, double par0, double dpar0, double par1, double dpar1, double xMin_fit, double xMax_fit,
		const RooRealVar& x, RooDataHist& fitData, double& par0_refitted, double& par1_refitted)
{
  std::cout << "<refitShift>:" << std::endl;
  std::cout << " fitFunction_formula = " << fitFunction_formula << std::endl;
  std::cout << " par0 = " << par0 << ", dpar0 = " << dpar0 << std::endl;
  std::cout << " par1 = " << par1 << ", dpar1 = " << dpar1 << std::endl;
  std::cout << " range = " << xMin_fit << ".." << xMax_fit << std::endl;
  TString fitFunction_formula_modified = fitFunction_formula.data();
  fitFunction_formula_modified.ReplaceAll("par0", Form("(%f + %f*TMath::Sign(-1,alpha)*(1. - TMath::Power(2., TMath::Abs(alpha))))", par0, dpar0));
  fitFunction_formula_modified.ReplaceAll("par1", Form("(%f + %f*TMath::Sign(-1,alpha)*(1. - TMath::Power(2., TMath::Abs(alpha))))", par1, dpar1));
  std::cout << " fitFunction_formula(modified) = " << fitFunction_formula_modified << std::endl;
  RooRealVar alpha("alpha", "alpha", 0., -10., 10.);
  RooGenericPdf* tempFitFunction = new RooGenericPdf("tempFitFunction", fitFunction_formula_modified.Data(), RooArgList(x, alpha));
  RooConstVar constraint_mean("constraint_mean", "constraint_mean", 0.);
  RooConstVar constraint_width("constraint_width", "constraint_width", 3.);
  RooGaussian constraint_gaussian("constraint_gaussian", "constraint_gaussian", alpha, constraint_mean, constraint_width);
  RooFitResult* tempFitResult = tempFitFunction->fitTo(fitData, Save(kTRUE), SumW2Error(kTRUE), Strategy(0), ExternalConstraints(constraint_gaussian));
  std::cout << "alpha = " << alpha.getVal() << std::endl;
  par0_refitted = par0 + alpha.getVal()*dpar0;
  par1_refitted = par1 + alpha.getVal()*dpar1;
  std::cout << "par0(refitted) = " << par0_refitted << std::endl;
  std::cout << "par1(refitted) = " << par1_refitted << std::endl;
  delete tempFitFunction;
  delete tempFitResult;
}
void zeroBinsForChi2(const std::string& histogram1Name, TH1* histogram1, const std::string& histogram2Name, TH1* histogram2, double xMin_fit, double xMax_fit, bool silent = false)
{
  // for the chi2 probability, remove bins with no entry in the original template as this screws up the chi2 calculation
  for ( int iBin = histogram1->FindBin(xMin_fit); iBin <= histogram1->GetNbinsX(); ++iBin ) {
    const double epsilon = 1.e-8;
    if ( histogram1->GetBinContent(iBin) < epsilon ||
	 histogram2->GetBinContent(iBin) < epsilon ) {
      histogram1->SetBinContent(iBin, 0.);
      histogram1->SetBinError(iBin, 0.);
      histogram2->SetBinContent(iBin, 0.);
      histogram2->SetBinError(iBin, 0.);
    }
    if ( !silent ) {
      std::cout << "bin #" << iBin << " (x = " << histogram1->GetBinCenter(iBin) << "):" 
		<< " " << histogram1Name << " = " <<  histogram1->GetBinContent(iBin) << " +/- " << histogram1->GetBinError(iBin) << ","
		<< " " << histogram2Name << " = " <<  histogram2->GetBinContent(iBin) << " +/- " << histogram2->GetBinError(iBin) << std::endl;
    }
  }  
}
void scaleHistogramToMaxChi2Difference(const TH1* histogram, const TH1* template_central, double pChi2_central, 
				       TH1* template_shift, const std::string& central_or_shift, double xMin_fit, double xMax_fit, double maxChi2_relative)
{
  TH1F* histogram_cloned = (TH1F*)histogram->Clone(); 
  TH1F* template_shift_cloned  = (TH1F*)template_shift->Clone(); 
  const double epsilon = 1.e-1;
  for ( int iBin = 1; iBin < histogram_cloned->FindBin(xMin_fit + epsilon); ++iBin ) {
    histogram_cloned->SetBinContent(iBin, 0.);
    histogram_cloned->SetBinError(iBin, 0.);
    template_shift_cloned->SetBinContent(iBin, 0.);
    template_shift_cloned->SetBinError(iBin, 0.);
  }
  double sf_difference_shift = 1.;
  zeroBinsForChi2("", histogram_cloned, "", template_shift_cloned, xMin_fit, xMax_fit, true);
  double pChi2_shift = histogram_cloned->Chi2Test(template_shift_cloned, "WW");
  std::cout << "sf_difference_shift = " << sf_difference_shift << ": pChi2_central = " << pChi2_central << ", pChi2_shift = " << pChi2_shift << std::endl;
  int numIterations = 0;
  const int maxIterations = 100;
  while ( pChi2_shift < (maxChi2_relative*pChi2_central) && numIterations < maxIterations ) {
    sf_difference_shift *= 0.9;    
    for ( int iBin = histogram_cloned->FindBin(xMin_fit); iBin <= histogram_cloned->GetNbinsX(); ++iBin ) {
      double binContent_central = template_central->GetBinContent(iBin);
      double binContent_shift = template_shift->GetBinContent(iBin);
      template_shift_cloned->SetBinContent(iBin, (1. - sf_difference_shift)*binContent_central + sf_difference_shift*binContent_shift);
    }
    zeroBinsForChi2("", histogram_cloned, "", template_shift_cloned, xMin_fit, xMax_fit, true);
    pChi2_shift = histogram_cloned->Chi2Test(template_shift_cloned, "WW");
    std::cout << "sf_difference_shift = " << sf_difference_shift << ": pChi2_central = " << pChi2_central << ", pChi2_shift = " << pChi2_shift << std::endl;
    ++numIterations;
  }
  if ( sf_difference_shift != 1. ) {
     for ( int iBin = histogram_cloned->FindBin(xMin_fit + epsilon); iBin <= histogram_cloned->GetNbinsX(); ++iBin ) {
      double binContent_central = template_central->GetBinContent(iBin);
      double binContent_shift = template_shift->GetBinContent(iBin);
      template_shift->SetBinContent(iBin, (1. - sf_difference_shift)*binContent_central + sf_difference_shift*binContent_shift);
    }
    std::cout << "reducing " << central_or_shift << " to improve p(Chi^2): sf_difference_shift = " << sf_difference_shift << std::endl;
  }
}
int addNuisance2(const std::string& inputFileName, 
		 const std::string& channel, const std::string& process, const std::string& sqrtS, const std::string& label, const std::string& directory, 
		 int verbosity = false, bool addVarBin = false, int fitModel = 0, int errorOption = 0, double xMin_fit = 150., double xMax_fit = 1500., bool addUncertainties = true, bool testMode = false) 
{
  std::cout << "<addNuisance2>:" << std::endl;
  std::cout << " inputFile = " << inputFileName << ": directory = " << directory << "/" << process << std::endl;
  std::cout << " range = " << xMin_fit << ".." << xMax_fit << " (addVarBin = " << addVarBin << ")" << std::endl;
  std::cout << " fitModel = " << fitModel << std::endl;
  
  if ( addVarBin ) {
    addVarBinNuisance(inputFileName, channel, process, sqrtS, label, directory, true, fitModel, xMin_fit, xMax_fit);
    return 1;
  }

  if ( !verbosity ) {
    RooMsgService::instance().setStreamStatus(0, false);
    RooMsgService::instance().setStreamStatus(1, false);
    RooMsgService::instance().setSilentMode(true);
  }

  // Load histogram that is to be fitted
  TFile* inputFile = new TFile(inputFileName.c_str());
  std::cout << " inputFile = " << inputFile << std::endl;
  TString histogramName_fine_binning = directory + "/" + process;
  TH1F* histogram_fine_binning = (TH1F*)inputFile->Get(histogramName_fine_binning.Data());
  std::cout << " histogram(fine_binning) = " << histogram_fine_binning << std::endl;
  TString histogramName_coarse_binning = histogramName_fine_binning;
  histogramName_coarse_binning.ReplaceAll("_fine_binning", "");
  TH1F* histogram_coarse_binning = (TH1F*)inputFile->Get(histogramName_coarse_binning.Data());
  std::cout << " histogram(coarse_binning) = " << histogram_coarse_binning << std::endl;
  if ( !(histogram_fine_binning && histogram_coarse_binning) ) {
    std::cerr << "Failed to load histograms !!" << std::endl;
    assert(0);
  }

  // Copy bins within fitted range into temporary data structures used as input for the fit
  std::vector<double> x_values;
  std::vector<double> xErr_values;
  std::vector<double> y_values;
  std::vector<double> yErr_values;  
  TAxis* xAxis_fine_binning = histogram_fine_binning->GetXaxis();
  int numBins_fine_binning = xAxis_fine_binning->GetNbins();
  double sumBinContents = 0.;
  double sumBinErrors2 = 0.;
  for ( int iBin = 1; iBin <= numBins_fine_binning; ++iBin ) {
    double binContent = histogram_fine_binning->GetBinContent(iBin);
    sumBinContents += binContent;
    double binError = histogram_fine_binning->GetBinError(iBin);
    sumBinErrors2 += (binError*binError);
  }
  //std::cout << "sumBinContents = " << sumBinContents << std::endl;
  //std::cout << "sqrt(sumBinErrors2) = " << TMath::Sqrt(sumBinErrors2) << std::endl;
  double numEvents = ( sumBinContents > 0. ) ? 
    TMath::Power(sumBinContents/TMath::Sqrt(sumBinErrors2), 2.) : 1.;
  double avWeight = sumBinContents/numEvents;
  for ( int iBin = 1; iBin <= numBins_fine_binning; ++iBin ) {
    double binCenter  = xAxis_fine_binning->GetBinCenter(iBin);
    double binWidth   = xAxis_fine_binning->GetBinWidth(iBin);
    double binContent = histogram_fine_binning->GetBinContent(iBin);
    double binError   = histogram_fine_binning->GetBinError(iBin);
    if ( binCenter > xMin_fit && binCenter < xMax_fit ) {
      double x_value = binCenter;
      double xErr_value = 0.5*binWidth;
      x_values.push_back(x_value);
      xErr_values.push_back(xErr_value);
      // CV: set empty bins to low binContent with uncertainty corresponding to single event weight,
      //     in order not to bias fit by including upward fluctuating bins, but excluding downward fluctuating bins from the fit
      double y_value = binContent;
      if ( y_value < 1.e-2*avWeight ) {
	y_value = 1.e-2*avWeight;
      }
      // CV: set binError to at least >= 1 avWeight,
      //     to account for empty bins as well as for fluctuations in event weights, e.g. in "stitched" W+jets sample
      double yErr_value = TMath::Sqrt(binError*binError + avWeight*avWeight);
      y_values.push_back(y_value);
      yErr_values.push_back(yErr_value);
      //std::cout << "bin #" << iBin << ": x = " << x_values.back() << " +/- " << xErr_values.back() << ", y = " << y_values.back() << " +/- " << yErr_values.back() << std::endl;
    }
  }
  
  int numBins_fitted = x_values.size();
  TGraphAsymmErrors* graph = new TGraphAsymmErrors(numBins_fitted);
  for ( int iBin_fitted = 0; iBin_fitted < numBins_fitted; ++iBin_fitted ) {
    const double yMin = 1.e-9;
    double log_y_value = TMath::Log(TMath::Max(yMin, y_values.at(iBin_fitted)));
    graph->SetPoint(iBin_fitted, x_values.at(iBin_fitted), log_y_value);
    //graph->SetPoint(iBin_fitted, x.at(iBin_fitted), y.at(iBin_fitted));
    double log_yErrUp_value   = TMath::Log(TMath::Max(yMin, y_values.at(iBin_fitted) + yErr_values.at(iBin_fitted))) - log_y_value;
    double log_yErrDown_value = log_y_value - TMath::Log(TMath::Max(yMin, y_values.at(iBin_fitted) - yErr_values.at(iBin_fitted)));
    //std::cout << "bin #" << iBin_fitted << ":" 
    //	        << " x = " << x_values.at(iBin_fitted) << " +/- " << xErr_values.at(iBin_fitted) << "," 
    //	        << " y = " << y_values.at(iBin_fitted) << " +/- " << yErr_values.at(iBin_fitted) 
    //	        << " (logy = " << log_y_value << " + " << log_yErrUp_value << " - " << log_yErrDown_value << ")" << std::endl;
    graph->SetPointError(iBin_fitted, xErr_values.at(iBin_fitted), xErr_values.at(iBin_fitted), log_yErrDown_value, log_yErrUp_value);
    //graph->SetPointError(iBin_fitted, xErr_values.at(iBin_fitted), xErr_values.at(iBin_fitted), yErr_values.at(iBin_fitted), yErr_values.at(iBin_fitted));    
  }

  // Define the fit function
  double x0 = 0.;
  std::string fitFunction_formula;
  if ( fitModel == 0 ) {
    x0 = 0.;
    fitFunction_formula = Form("TMath::Exp(-(x - %1.0f)/(par0 + 0.001*par1*(x - (%1.0f + %1.0f))))", xMin_fit, xMin_fit, x0);
  } else if ( fitModel == 1 ) {
    x0 = 200.;
    //x0 = 0.;
    //double norm = 0.;
    //for ( int iBin = 1; iBin <= numBins_fine_binning; ++iBin ) {
    //  double binContent = histogram_fine_binning->GetBinContent(iBin);
    //  double binCenter  = xAxis_fine_binning->GetBinCenter(iBin);
    //  if ( binCenter > xMin_fit && binCenter < xMax_fit ) {
    //	  x0 += (binContent*binCenter);
    //	  norm += binContent;
    //  }
    //}
    //if ( norm > 0. ) {
    //  x0 /= norm;
    //  x0 -= xMin_fit;
    //  x0 *= 2.;
    //}
    fitFunction_formula = Form("TMath::Exp(-(x - %1.0f)/(par0*(1.0 + 0.001*par1*(x - (%1.0f + %1.0f)))))", xMin_fit, xMin_fit, x0);
  } else {
    std::cerr << "Fit model = " << fitModel << " not supported !!" << std::endl;
    assert(0);
  }
  std::cout << "fitFunction = " << fitFunction_formula << std::endl;
  RooRealVar x("x", "x", xMin_fit, xMax_fit);
  RooDataHist fitData("fitData", "fitData", RooArgList(x), histogram_fine_binning);
  RooRealVar par0("par0", "par0", 1.e+2, 0., 1.e+3);
  RooRealVar par1("par1", "par1", 1., -1.e+4, 1.e+4);
  RooGenericPdf* fitFunction = new RooGenericPdf("genPdf", fitFunction_formula.data(), RooArgList(x, par0, par1));
  RooFitResult* fitResult = fitFunction->fitTo(fitData, Save(kTRUE), SumW2Error(kTRUE), Strategy(0)); 
  std::cout << "fit has finished:" << std::endl;
  std::cout << " status = " << fitResult->status() << ", qual(cov) " <<  fitResult->covQual() << ":" << std::endl;
  std::cout << " par0 = " << par0.getVal() << ", par1 = " << par1.getVal() << std::endl;
  //if ( fitResult->covQual() >= 3 ) {
    std::cout << " cov:" << std::endl; 
    fitResult->covarianceMatrix().Print();
    std::cout << " correlation:" << std::endl; 
    fitResult->correlationMatrix().Print();
  //}
  
  //if ( !(fitResult->status() == 0 && fitResult->covQual() >= 2) ) {
  if ( !(fitResult->status() == 0) ) {
    std::cerr << "=================================================================================" << std::endl;
    std::cerr << "Tail fit has not succeeded. Datacard and uncertainty files will *not* be altered." << std::endl;
    std::cerr << "=================================================================================" << std::endl;
    return 1;
  }

  double par0_central = par0.getVal();
  double par1_central = par1.getVal();
  TMatrixDSym covMatrix = fitResult->covarianceMatrix();

  TMatrixD EigenVectors(2,2);
  EigenVectors = TMatrixDSymEigen(covMatrix).GetEigenVectors();
  std::cout << "Eigenvectors =  { " << EigenVectors(0,0) << ", " << EigenVectors(1,0) << " }, { " << EigenVectors(0,1) << ", " << EigenVectors(1,1) << " }" << std::endl;
  TVectorD EigenValues(2);  
  EigenValues = TMatrixDSymEigen(covMatrix).GetEigenValues();
  EigenValues(0) = TMath::Sqrt(EigenValues(0));
  EigenValues(1) = TMath::Sqrt(EigenValues(1));
  std::cout << "Eigenvalues = " << EigenValues(0) << ", " << EigenValues(1) << std::endl;
  
  // convert fitResult into histograms
  //double xMax = xAxis->GetXmax();
  double xMax = xMax_fit;

  double k = 1.;

  bool hasInfinitePoint_central = false;
  double xInfinitePoint_central = -1.;
  checkForInfinitePoints2(fitModel, xMin_fit, xMax, x0, "central", par0_central, par1_central, hasInfinitePoint_central, xInfinitePoint_central);
  double sf_central;
  TH1F* template_central = makeHist2(
          histogram_fine_binning->GetName(), histogram_fine_binning, par0_central, par1_central, fitModel, 
	  xMin_fit, TMath::Min(xMax, xInfinitePoint_central), x0, sf_central);
  double integral_central = template_central->Integral(template_central->FindBin(xMin_fit), template_central->FindBin(xMax));

  double xMax_finite = xMin_fit + 0.5*(xMax - xMin_fit);
  //double xMax_finite = xMax_fit;

  std::string nuisance1Name = process + "_" + "CMS_" + label + "1_" + directory + "_" + sqrtS + "_" + process;
  
  double par0_shift1Up = par0_central + EigenValues(0)*EigenVectors(0,0);
  double par1_shift1Up = par1_central + EigenValues(0)*EigenVectors(1,0);
  bool hasInfinitePoint_shift1Up = false;
  double xInfinitePoint_shift1Up = -1.;
  checkForInfinitePoints2(fitModel, xMin_fit, xMax, x0, "shift1Up", par0_shift1Up, par1_shift1Up, hasInfinitePoint_shift1Up, xInfinitePoint_shift1Up);
  if ( errorOption == 1 && hasInfinitePoint_shift1Up ) {
    double sf_EigenValue_shift1Up = 1.;
    do { 
      par0_shift1Up = par0_central + sf_EigenValue_shift1Up*EigenValues(0)*EigenVectors(0,0);
      par1_shift1Up = par1_central + sf_EigenValue_shift1Up*EigenValues(0)*EigenVectors(1,0);
      checkForInfinitePoints2(fitModel, xMin_fit, xMax_finite, x0, "shift1Up", par0_shift1Up, par1_shift1Up, hasInfinitePoint_shift1Up, xInfinitePoint_shift1Up, true);
      sf_EigenValue_shift1Up *= 0.9;
    } while ( hasInfinitePoint_shift1Up );
    std::cout << "reducing shift1Up to avoid infinite point: sf_EigenValue_shift1Up = " << sf_EigenValue_shift1Up << std::endl;
  } else if ( errorOption == 2 ) {
    double par0_shift1Up_refitted, par1_shift1Up_refitted;
    refitShift(fitFunction_formula, par0_shift1Up, EigenVectors(0,1), par1_shift1Up, EigenVectors(1,1), xMin_fit, xMax_fit,
	       x, fitData, par0_shift1Up_refitted, par1_shift1Up_refitted);
    par0_shift1Up = par0_shift1Up_refitted;
    par1_shift1Up = par1_shift1Up_refitted;
    checkForInfinitePoints2(fitModel, xMin_fit, xMax_finite, x0, "shift1Up", par0_shift1Up, par1_shift1Up, hasInfinitePoint_shift1Up, xInfinitePoint_shift1Up);
    //k = 1.5;
  }
  double sf_shift1Up;
  TH1F* template_shift1Up = makeHist2(
          nuisance1Name + "Up", histogram_fine_binning, par0_shift1Up, par1_shift1Up, fitModel, 
	  xMin_fit, TMath::Min(xMax, xInfinitePoint_shift1Up), x0, sf_shift1Up, k, template_central, &sf_central);
  double integral_shift1Up = template_shift1Up->Integral(template_shift1Up->FindBin(xMin_fit), template_shift1Up->FindBin(xMax));

  double par0_shift1Down = par0_central - EigenValues(0)*EigenVectors(0,0);
  double par1_shift1Down = par1_central - EigenValues(0)*EigenVectors(1,0);
  bool hasInfinitePoint_shift1Down = false;
  double xInfinitePoint_shift1Down = -1.;
  checkForInfinitePoints2(fitModel, xMin_fit, xMax, x0, "shift1Down", par0_shift1Down, par1_shift1Down, hasInfinitePoint_shift1Down, xInfinitePoint_shift1Down);
  if ( errorOption == 1 && hasInfinitePoint_shift1Down ) {
    double sf_EigenValue_shift1Down = 1.;
    do { 
      par0_shift1Down = par0_central - sf_EigenValue_shift1Down*EigenValues(0)*EigenVectors(0,0);
      par1_shift1Down = par1_central - sf_EigenValue_shift1Down*EigenValues(0)*EigenVectors(1,0);
      checkForInfinitePoints2(fitModel, xMin_fit, xMax_finite, x0, "shift1Down", par0_shift1Down, par1_shift1Down, hasInfinitePoint_shift1Down, xInfinitePoint_shift1Down, true);
      sf_EigenValue_shift1Down *= 0.9;
    } while ( hasInfinitePoint_shift1Down );
    std::cout << "reducing shift1Down to avoid infinite point: sf_EigenValue_shift1Down = " << sf_EigenValue_shift1Down << std::endl;
  } else if ( errorOption == 2 ) {
    double par0_shift1Down_refitted, par1_shift1Down_refitted;
    refitShift(fitFunction_formula, par0_shift1Down, EigenVectors(0,1), par1_shift1Down, EigenVectors(1,1), xMin_fit, xMax_fit,
	       x, fitData, par0_shift1Down_refitted, par1_shift1Down_refitted);
    par0_shift1Down = par0_shift1Down_refitted;
    par1_shift1Down = par1_shift1Down_refitted;
    checkForInfinitePoints2(fitModel, xMin_fit, xMax_finite, x0, "shift1Down", par0_shift1Down, par1_shift1Down, hasInfinitePoint_shift1Down, xInfinitePoint_shift1Down);
    //k = 1.5;
  }
  double sf_shift1Down;
  TH1F* template_shift1Down = makeHist2(
          nuisance1Name + "Down", histogram_fine_binning, par0_shift1Down, par1_shift1Down, fitModel, 
	  xMin_fit, TMath::Min(xMax_fit, xInfinitePoint_shift1Down), x0, sf_shift1Down, k, template_central, &sf_central);
  double integral_shift1Down = template_shift1Down->Integral(template_shift1Down->FindBin(xMin_fit), template_shift1Down->FindBin(xMax));
  
  std::string nuisance2Name = process + "_" + "CMS_" + label + "2_" + directory + "_" + sqrtS + "_" + process;

  double par0_shift2Up = par0_central + EigenValues(1)*EigenVectors(0,1);
  double par1_shift2Up = par1_central + EigenValues(1)*EigenVectors(1,1);
  bool hasInfinitePoint_shift2Up = false;
  double xInfinitePoint_shift2Up = -1.;
  checkForInfinitePoints2(fitModel, xMin_fit, xMax, x0, "shift2Up", par0_shift2Up, par1_shift2Up, hasInfinitePoint_shift2Up, xInfinitePoint_shift2Up);
  if ( errorOption == 1 && hasInfinitePoint_shift2Up ) {
    double sf_EigenValue_shift2Up = 1.;
    do { 
      par0_shift2Up = par0_central + sf_EigenValue_shift2Up*EigenValues(1)*EigenVectors(0,1);
      par1_shift2Up = par1_central + sf_EigenValue_shift2Up*EigenValues(1)*EigenVectors(1,1);
      checkForInfinitePoints2(fitModel, xMin_fit, xMax_finite, x0, "shift2Up", par0_shift2Up, par1_shift2Up, hasInfinitePoint_shift2Up, xInfinitePoint_shift2Up, true);
      sf_EigenValue_shift2Up *= 0.9;
    } while ( hasInfinitePoint_shift2Up );
    std::cout << "reducing shift2Up to avoid infinite point: sf_EigenValue_shift2Up = " << sf_EigenValue_shift2Up << std::endl;
  } else if ( errorOption == 2 ) {
    double par0_shift2Up_refitted, par1_shift2Up_refitted;
    refitShift(fitFunction_formula, par0_shift2Up, EigenVectors(0,0), par1_shift2Up, EigenVectors(1,0), xMin_fit, xMax_fit,
	       x, fitData, par0_shift2Up_refitted, par1_shift2Up_refitted);
    par0_shift2Up = par0_shift2Up_refitted;
    par1_shift2Up = par1_shift2Up_refitted;
    checkForInfinitePoints2(fitModel, xMin_fit, xMax_finite, x0, "shift2Up", par0_shift2Up, par1_shift2Up, hasInfinitePoint_shift2Up, xInfinitePoint_shift2Up);
    //k = 1.5;
  }
  double sf_shift2Up;
  TH1F* template_shift2Up = makeHist2(
          nuisance2Name + "Up", histogram_fine_binning, par0_shift2Up, par1_shift2Up, fitModel, 
	  xMin_fit, TMath::Min(xMax, xInfinitePoint_shift2Up), x0, sf_shift2Up, k, template_central, &sf_central);
  double integral_shift2Up = template_shift2Up->Integral(template_shift2Up->FindBin(xMin_fit), template_shift2Up->FindBin(xMax));

  double par0_shift2Down = par0_central - EigenValues(1)*EigenVectors(0,1);
  double par1_shift2Down = par1_central - EigenValues(1)*EigenVectors(1,1);
  bool hasInfinitePoint_shift2Down = false;
  double xInfinitePoint_shift2Down = -1.;
  checkForInfinitePoints2(fitModel, xMin_fit, xMax, x0, "shift2Down", par0_shift2Down, par1_shift2Down, hasInfinitePoint_shift2Down, xInfinitePoint_shift2Down);
  if ( errorOption == 1 && hasInfinitePoint_shift2Down ) {
    double sf_EigenValue_shift2Down = 1.;
    do { 
      par0_shift2Down = par0_central - sf_EigenValue_shift2Down*EigenValues(1)*EigenVectors(0,1);
      par1_shift2Down = par1_central - sf_EigenValue_shift2Down*EigenValues(1)*EigenVectors(1,1);
      checkForInfinitePoints2(fitModel, xMin_fit, xMax_finite, x0, "shift2Down", par0_shift2Down, par1_shift2Down, hasInfinitePoint_shift2Down, xInfinitePoint_shift2Down, true);
      sf_EigenValue_shift2Down *= 0.9;
    } while ( hasInfinitePoint_shift2Down );
    std::cout << "reducing shift2Down to avoid infinite point: sf_EigenValue_shift2Down = " << sf_EigenValue_shift2Down << std::endl;
  } else if ( errorOption == 2 ) {
    double par0_shift2Down_refitted, par1_shift2Down_refitted;
    refitShift(fitFunction_formula, par0_shift2Down, EigenVectors(0,0), par1_shift2Down, EigenVectors(1,0), xMin_fit, xMax_fit,
	       x, fitData, par0_shift2Down_refitted, par1_shift2Down_refitted);
    par0_shift2Down = par0_shift2Down_refitted;
    par1_shift2Down = par1_shift2Down_refitted;
    checkForInfinitePoints2(fitModel, xMin_fit, xMax_finite, x0, "shift2Down", par0_shift2Down, par1_shift2Down, hasInfinitePoint_shift2Down, xInfinitePoint_shift2Down);
    //k = 1.5;
  }
  double sf_shift2Down;
  TH1F* template_shift2Down = makeHist2(
	  nuisance2Name + "Down", histogram_fine_binning, par0_shift2Down, par1_shift2Down, fitModel, 
	  xMin_fit, TMath::Min(xMax, xInfinitePoint_shift2Down), x0, sf_shift2Down, k, template_central, &sf_central);
  double integral_shift2Down = template_shift2Down->Integral(template_shift2Down->FindBin(xMin_fit), template_shift2Down->FindBin(xMax));

  double integral_orgiginal = histogram_fine_binning->Integral(histogram_fine_binning->FindBin(xMin_fit), histogram_fine_binning->FindBin(xMax));
  std::cout << "Integrals:" 
	    << " original = " << integral_orgiginal << ","
	    << " central = " << integral_central << ","
	    << " shift1Up = " << integral_shift1Up << ", shift1Down = " << integral_shift1Down << ","
	    << " shift2Up = " << integral_shift2Up << ", shift2Down = " << integral_shift2Down << std::endl;

  // check if the shift "Up"/"Down" histograms are integrable. If not terminate the script here.
  if ( addUncertainties && 
       !(TMath::Finite(integral_central) && TMath::Finite(integral_shift1Up) && TMath::Finite(integral_shift1Down) && TMath::Finite(integral_shift2Up) && TMath::Finite(integral_shift2Down)) ) {
    std::cerr << "===============================================================================" << std::endl;
    std::cerr << "Tail fit has succeeded, but 1 or more of the shift up/down histograms is not integrable." << std::endl;
    std::cerr << "Script will terminate here without altering datacard. Turn on --verbose option to see the problem histogram." << std::endl; 
    std::cerr << "===============================================================================" << std::endl;
    return 1;
  }

  // rebin the histograms   
  int numBins_coarse_binning = histogram_coarse_binning->GetNbinsX();
  double* binning_coarse_binning = getAxis(histogram_coarse_binning);
  histogram_fine_binning = rebin(histogram_fine_binning,  numBins_coarse_binning, binning_coarse_binning);
  template_central = rebin(template_central, numBins_coarse_binning, binning_coarse_binning);
  fixHist(template_central, xMin_fit, histogram_coarse_binning);
  template_shift1Up = rebin(template_shift1Up, numBins_coarse_binning, binning_coarse_binning);
  fixHist(template_shift1Up, xMin_fit, histogram_coarse_binning);
  template_shift1Down = rebin(template_shift1Down, numBins_coarse_binning, binning_coarse_binning);
  fixHist(template_shift1Down, xMin_fit, histogram_coarse_binning);
  template_shift2Up = rebin(template_shift2Up, numBins_coarse_binning, binning_coarse_binning);
  fixHist(template_shift2Up, xMin_fit, histogram_coarse_binning);
  template_shift2Down = rebin(template_shift2Down, numBins_coarse_binning, binning_coarse_binning);
  fixHist(template_shift2Down, xMin_fit, histogram_coarse_binning);

  // clone the fit result and original template for computing the chi2 and KS probability of the fit
  TH1F* histogram_cloned = (TH1F*)histogram_coarse_binning->Clone(Form("%s_cloned", histogram_coarse_binning->GetName())); 
  TH1F* template_central_cloned  = (TH1F*)template_central->Clone(Form("%s_cloned", template_central->GetName())); 
  const double epsilon = 1.e-1;
  for ( int iBin = 1; iBin < histogram_cloned->FindBin(xMin_fit + epsilon); ++iBin ) {
    histogram_cloned->SetBinContent(iBin, 0.);
    histogram_cloned->SetBinError(iBin, 0.);
    template_central_cloned->SetBinContent(iBin, 0.);
    template_central_cloned->SetBinError(iBin, 0.);
  }
  // compute the KS probability
  double pKS_central = histogram_cloned->KolmogorovTest(template_central_cloned);
  std::cout << "p(KS) = " << pKS_central << std::endl;
  // for the chi2 probability, remove bins with no entry in the original template as this screws up the chi2 calculation
  zeroBinsForChi2("histogram", histogram_cloned, "template_central", template_central_cloned, xMin_fit, xMax_fit);
  double pChi2_central = histogram_cloned->Chi2Test(template_central_cloned, "WW");
  std::cout << "p(Chi^2) = " << pChi2_central << std::endl;
  if ( verbosity ) {
    std::cout << "==========================================================================================================" << std::endl;
    std::cout << "Result of chi2 probability test: " << pChi2_central << ", KS probability test: " << pKS_central << std::endl;
    std::cout << "==========================================================================================================" << std::endl;
  }
  delete histogram_cloned;
  delete template_central_cloned;

  if ( errorOption == 1 ) {
    scaleHistogramToMaxChi2Difference(histogram_coarse_binning, template_central, pChi2_central, template_shift1Up,   "shift1Up",   xMin_fit, xMax_fit, 0.05);
    scaleHistogramToMaxChi2Difference(histogram_coarse_binning, template_central, pChi2_central, template_shift1Down, "shift1Down", xMin_fit, xMax_fit, 0.05);
    scaleHistogramToMaxChi2Difference(histogram_coarse_binning, template_central, pChi2_central, template_shift2Up,   "shift2Up",   xMin_fit, xMax_fit, 0.05);
    scaleHistogramToMaxChi2Difference(histogram_coarse_binning, template_central, pChi2_central, template_shift2Down, "shift2Down", xMin_fit, xMax_fit, 0.05);
  }

  // we do not need bin errors for bins that are within the range of the tail-fit (the tail-fit replaces bin-by-bin error!),
  // therefore we set all errors to 0. This saves us from modifying the add_bbb_error.py script 
  // in which we otherwise would have to include an option for adding bbb only to bins that are within specific ranges.
  int iBin_merge = xAxis_fine_binning->FindBin(xMin_fit);
  for ( int iBin = iBin_merge; iBin <= numBins_fine_binning; ++iBin ) {
    template_central->SetBinError(iBin, 0.);
    template_shift1Up->SetBinError(iBin, 0.);
    template_shift1Down->SetBinError(iBin, 0.);
    template_shift2Up->SetBinError(iBin, 0.);
    template_shift2Down->SetBinError(iBin, 0.);
  }

  // save the new templates to the datacard ROOT file
  TFile* outputFile = new TFile("Output.root", "RECREATE");
  cloneFile(outputFile, inputFile, directory + "/" + process);
  outputFile->cd(directory.c_str());
  template_central->Write();
  if ( addUncertainties ) {
    template_shift1Up->Write(); 
    template_shift1Down->Write(); 
    template_shift2Up->Write(); 
    template_shift2Down->Write(); 
  }

  // make control plot showing shift "Up"/"Down" and central templates, rebinned as in datacard
  TCanvas* canvas = new TCanvas("canvas", "canvas", 800, 750);
  canvas->Divide(1,2); 
  canvas->cd();  
  canvas->cd(1)->SetPad(0,0.2,1.0,1.0); 
  gPad->SetLeftMargin(0.2); 
  gPad->SetLogy();
  
  histogram_fine_binning->SetTitle("");
  histogram_fine_binning->SetStats(false);
  histogram_fine_binning->SetLineWidth(1); 
  histogram_fine_binning->SetMarkerStyle(kFullCircle);
  histogram_fine_binning->Scale(1.0, "width");
  histogram_fine_binning->Draw();

  TAxis* xAxis_original = histogram_fine_binning->GetXaxis();
  xAxis_original->SetTitle("m_{#tau#tau} [GeV]");
  xAxis_original->SetTitleSize(0.05);

  TAxis* yAxis_original = histogram_fine_binning->GetYaxis();
  yAxis_original->SetTitle("dN/dm_{#tau#tau} [1/GeV]");
  yAxis_original->SetTitleSize(0.05);
  yAxis_original->SetTitleOffset(1.2);
  yAxis_original->SetLabelSize(0.0275);
  
  template_central->SetStats(false);
  template_central->SetLineColor(kGreen+2);
  template_central->Scale(1.0,"width");
  template_central->Draw("hist sames");

  template_shift1Up->SetStats(false);
  template_shift1Up->SetLineColor(kRed);
  template_shift1Up->SetLineStyle(9);
  template_shift1Up->Scale(1.0,"width");
  template_shift1Up->Draw("hist sames");

  template_shift1Down->SetStats(false);
  template_shift1Down->SetLineColor(kRed+2);
  template_shift1Down->SetLineStyle(3);
  template_shift1Down->SetLineWidth(2);
  template_shift1Down->Scale(1.0,"width");
  template_shift1Down->Draw("hist sames");

  template_shift2Up->SetStats(false);
  template_shift2Up->SetLineColor(kBlue);
  template_shift2Up->SetLineStyle(9);
  template_shift2Up->Scale(1.0,"width");
  template_shift2Up->Draw("hist sames");

  template_shift2Down->SetStats(false);
  template_shift2Down->SetLineColor(kBlue+2);
  template_shift2Down->SetLineStyle(3);
  template_shift2Down->SetLineWidth(2);
  template_shift2Down->Scale(1.0,"width");
  template_shift2Down->Draw("hist sames");
  
  TLegend* legend = new TLegend(0.7, 0.64, 0.89, 0.88); 
  legend->SetBorderSize( 0 );
  legend->SetFillStyle ( 1001 );
  legend->SetFillColor (kWhite);
  legend->AddEntry(histogram_fine_binning,  "original",     "PL");
  legend->AddEntry(template_central,    "central fit",  "L");
  legend->AddEntry(template_shift1Up,   "shift1 Up",    "L");
  legend->AddEntry(template_shift1Down, "shift1 Down",  "L");
  legend->AddEntry(template_shift2Up,   "shift2 Up",    "L");
  legend->AddEntry(template_shift2Down, "shift2 Down",  "L");
  legend->Draw("same");
  
  TPaveText* text = new TPaveText(0.20, 0.90, 0.50, 0.99, "NDC");
  text->SetBorderSize(0);
  text->SetFillStyle(0);
  text->SetTextAlign(12);
  text->SetTextSize(0.05);
  text->SetTextColor(1);
  text->SetTextFont(62);
  text->AddText(TString::Format("P(#chi^{2})=%1.5f, P(KS)=%1.5f", pChi2_central, pKS_central));
  text->Draw();
  
  canvas->cd(2)->SetPad(0,0,1.0,0.2); 
  gPad->SetLeftMargin(0.2);
  drawDifference(histogram_fine_binning, template_central, template_shift1Up, template_shift1Down, template_shift2Up, template_shift2Down);

  canvas->Update();
  canvas->SaveAs((process + "_" + "CMS_" + label + "_" + directory + "_" + sqrtS +"_Rebin.png").c_str());
  canvas->SaveAs((process + "_" + "CMS_" + label + "_" + directory + "_" + sqrtS +"_Rebin.pdf").c_str());

  delete canvas;

  delete inputFile;
  delete outputFile;

  if ( testMode ) {
    std::cout << "Running in test mode. Script will exit now without altering datacard or uncertainty files." << std::endl;
    return 1;
  }
  
  return 0;
}
int addFitNuisance(const std::string& inputFileName, 
		   const std::string& channel, const std::string& process, const std::string& sqrtS, const std::string& label, const std::string& category,
		   double xMin_fit = 150., double xMax_fit = 1500., 
		   int fitOption = 0, int fitModel = 0, int errorOption = 0, 
		   int verbose = false, bool addVarBin = false, bool addUncertainties = true, bool testMode = false) 
{
  typedef int (*addNuisancePtr)(const std::string&, const std::string&, const std::string&, const std::string&, const std::string&, const std::string&, int, bool, int, int, double, double, bool, bool);
  addNuisancePtr functionToCall = 0;
  if ( fitOption == 0 ) {
    functionToCall = &addNuisance;
  } else if ( fitOption == 1 ) {
    functionToCall = &addNuisance2;
  } else {
    std::cerr << "Fit option = " << fitOption << " not supported !!" << std::endl;
  }
  assert(functionToCall);
  std::string directory;
  if      ( category==  "0" ) directory = channel + "_0jet_low";
  else if ( category==  "1" ) directory = channel + "_0jet_high";
  else if ( category==  "2" ) directory = channel + "_boost_low";
  else if ( category==  "3" ) directory = channel + "_boost_high";
  else if ( category==  "6" ) directory = channel + "_btag_low";
  else if ( category==  "7" ) directory = channel + "_btag_high";
  else if ( category==  "8" ) directory = channel + "_nobtag";
  else if ( category==  "9" ) directory = channel + "_btag";
  else if ( category== "10" ) directory = channel + "_nobtag_low";
  else if ( category== "11" ) directory = channel + "_nobtag_medium";
  else if ( category== "12" ) directory = channel + "_nobtag_high";
  else if ( category== "13" ) directory = channel + "_btag_low";
  else if ( category== "14" ) directory = channel + "_btag_high";
  else {
    std::cerr << "Category = " << category << " not supported !!" << std::endl;
  }
  assert(directory != "");
  return (*functionToCall)(inputFileName, channel, process, sqrtS, label, directory, verbose, addVarBin, fitModel, errorOption, xMin_fit, xMax_fit, addUncertainties, testMode);
}
