#include <iostream>
#include <iomanip>
#include <fstream>
#include <vector>
#include <TROOT.h>
#include <TSystem.h>
#include <TFile.h>
#include <TH1.h>
#include <TF1.h>
#include <TString.h>
#include <TBenchmark.h>
#include "TCanvas.h"
#include "TAxis.h"
#include "TDirectory.h"
#include "TLegend.h"
#include "TMatrix.h"
#include "TMatrixDSym.h"
#include "TMatrixDSymEigen.h"
#include "TVectorD.h"
#include "TVectorF.h"
#include "TVector.h"
#include "TVectorT.h"
#include "TVector3.h"
#include "TIterator.h"
#include "TFitResult.h"

using namespace std;

TString defineName(TString category){
  
  TString name;
  if (category=="muTau_nobtag")
    name = "mt_nobtag";
  if (category=="muTau_btag")
    name = "mt_btag";
  if (category=="muTau_boost_high")
    name = "mt_boost_high";
  if (category=="muTau_btag_low")
    name = "mt_btag_low";
  if (category=="muTau_btag_high")
    name = "mt_btag_high";

  if (category=="eleTau_nobtag")
    name = "et_nobtag";
  if (category=="eleTau_btag")
    name = "et_btag";
  if (category=="eleTau_boost_high")
    name = "et_boost_high";
  if (category=="eleTau_btag_low")
    name = "et_bag_low";
  if (category=="eleTau_btag_high")
    name = "et_btag_high";

  return name;
}
TH1F* convert(TF1* f, TH1F* hIn, double xmin_fit){

  TH1F* hOut = (TH1F*)hIn->Clone();
  hOut->Reset();

  //First normalize to the initial integral in fitting region
  int binToSplit = 0;
  for (unsigned int ibin=1; ibin<hOut->GetNbinsX()+1; ++ibin){
    double xlow = hOut->GetBinLowEdge(ibin);
    double xhigh = hOut->GetBinLowEdge(ibin+1);
    if (xlow <= xmin_fit && xhigh > xmin_fit)
      binToSplit=ibin;
    
    if (xlow<xmin_fit){
      hOut->SetBinContent(ibin,0);
      hOut->SetBinError(ibin,0);
    }
    else {
	hOut->SetBinContent(ibin,f->Integral(xlow,xhigh));
    }
  }

  hOut->Scale(hIn->Integral(binToSplit, hIn->GetNbinsX()+1)/hOut->Integral(1,hIn->GetNbinsX()+1));

  //Now set remaining bins
  for (unsigned int ibin=1; ibin<hOut->GetNbinsX()+1; ++ibin){
    double xlow = hOut->GetBinLowEdge(ibin);
    double xhigh = hOut->GetBinLowEdge(ibin+1);

    if (xlow<xmin_fit) {
      hOut->SetBinContent(ibin,hIn->GetBinContent(ibin));
      hOut->SetBinError(ibin,hIn->GetBinError(ibin));
    }
  }
  return hOut;
}

TH1F* convertWithEnvelope(TF1* f0, TF1* f1, TF1* f2, TF1* f3, TF1* f4, 
			  TH1F* hIn, double xmin_fit, 
			  bool moreThanOneFunc, bool isUp){

  TH1F* hOut = (TH1F*)hIn->Clone();
  hOut->Reset();

  //First normalize to the initial integral in fitting region
  int binToSplit = 0;
  for (unsigned int ibin=1; ibin<hOut->GetNbinsX()+1; ++ibin){
    double xlow = hOut->GetBinLowEdge(ibin);
    double xhigh = hOut->GetBinLowEdge(ibin+1);
    if (xlow <= xmin_fit && xhigh > xmin_fit)
      binToSplit=ibin;
    
    if (xlow<xmin_fit){
      hOut->SetBinContent(ibin,0);
      hOut->SetBinError(ibin,0);
    }
    else {
      if (!moreThanOneFunc)
	//This is not correct
	hOut->SetBinContent(ibin,f0->Integral(xlow,xhigh));
      else {
	double val0 = f0->Integral(xlow,xhigh);
	double val1 = f1->Integral(xlow,xhigh);
	double val2 = f2->Integral(xlow,xhigh);
	double val3 = f3->Integral(xlow,xhigh);
	double val4 = f4->Integral(xlow,xhigh);
	double newVal = 0;
	if (isUp) 
	  newVal = TMath::Max(TMath::Max(TMath::Max(val1,val2),val3),val4);
	else
	  newVal = TMath::Min(TMath::Min(TMath::Min(val1,val2),val3),val4);
	//	cout << "1 newVal " << newVal << endl;
	//	cout << "2 Max " << TMath::Max(TMath::Max(TMath::Max(val1,val2),val3),val4) << endl;
	//	cout << "3 Min " << TMath::Min(TMath::Min(TMath::Min(val1,val2),val3),val4) << endl;
	//	cout << "4 values " << val1 << " " << val2 << " " << val3 << " " << val4 << endl;
	hOut->SetBinContent(ibin,newVal);
      }
    }
  }

  hOut->Scale(hIn->Integral(binToSplit, hIn->GetNbinsX()+1)/hOut->Integral(1,hIn->GetNbinsX()+1));

  //Now set remaining bins
  for (unsigned int ibin=1; ibin<hOut->GetNbinsX()+1; ++ibin){
    double xlow = hOut->GetBinLowEdge(ibin);
    double xhigh = hOut->GetBinLowEdge(ibin+1);

    if (xlow<xmin_fit) {
      hOut->SetBinContent(ibin,hIn->GetBinContent(ibin));
      hOut->SetBinError(ibin,hIn->GetBinError(ibin));
    }
  }
  return hOut;
}

TH1F* convertNew(TF1* f, TH1F* hIn, double xmin_fit, bool moreThanOneFunc, bool isUp, TF1* f0=0, TF1* f2=0){

  TH1F* hOut = (TH1F*)hIn->Clone();
  hOut->Reset();

  //First normalize to the initial integral in fitting region
  int binToSplit = 0;
  for (unsigned int ibin=1; ibin<hOut->GetNbinsX()+1; ++ibin){
    double xlow = hOut->GetBinLowEdge(ibin);
    double xhigh = hOut->GetBinLowEdge(ibin+1);
    if (xlow <= xmin_fit && xhigh > xmin_fit)
      binToSplit=ibin;
    
    if (xlow<xmin_fit){
      hOut->SetBinContent(ibin,0);
      hOut->SetBinError(ibin,0);
    }
    else {
      if (!moreThanOneFunc)
	hOut->SetBinContent(ibin,f->Integral(xlow,xhigh));
      else {
	double val0 = f0->Integral(xlow,xhigh);
	double deltaVal1 = f->Integral(xlow,xhigh)-val0;
	double deltaVal2 = f2->Integral(xlow,xhigh)-val0;
	double newVal = val0 + sqrt(deltaVal1*deltaVal1 + deltaVal2*deltaVal2);
	if (!isUp) {
	  newVal = val0 - sqrt(deltaVal1*deltaVal1 + deltaVal2*deltaVal2);
	  cout << val0 << " " <<sqrt(deltaVal1*deltaVal1 + deltaVal2*deltaVal2)<< " " << newVal << endl;
	}
	//	if (hOut->GetBinCenter(ibin)==450)
	//	hOut->SetBinError(ibin,0);
	hOut->SetBinContent(ibin,newVal);
      }
    }
  }

  hOut->Scale(hIn->Integral(binToSplit, hIn->GetNbinsX()+1)/hOut->Integral(1,hIn->GetNbinsX()+1));

  //Now set remaining bins
  for (unsigned int ibin=1; ibin<hOut->GetNbinsX()+1; ++ibin){
    double xlow = hOut->GetBinLowEdge(ibin);
    double xhigh = hOut->GetBinLowEdge(ibin+1);

    if (xlow<xmin_fit) {
      hOut->SetBinContent(ibin,hIn->GetBinContent(ibin));
      hOut->SetBinError(ibin,hIn->GetBinError(ibin));
    }
  }
  return hOut;
}

void computeError(TH1F* h) {

  double weightAvg = 0;
  if (h->GetEntries()!=0) 
    weightAvg = h->Integral(0,h->GetNbinsX()+1)/h->GetEntries();
  //  cout << "Average weight " << weightAvg << endl;
  for (int i=1; i<=h->GetNbinsX(); ++i){
    double weight =0;
    if (h->GetBinContent(i)>0){
      weight = h->GetBinError(i)*h->GetBinError(i)/h->GetBinContent(i);
      //      cout << "weight " << weight << " "  << (weight-weightAvg)<< endl;
      //      cout << "Bin content " << h->Integral(i,i) << endl;
      //      cout << "Bin error before " << h->GetBinError(i) << endl;

      //      h->SetBinError(i, sqrt(h->GetBinError(i)*h->GetBinError(i)
      //      			     +
      //			     (weight-weightAvg)*(weight-weightAvg)));
      double error = sqrt((h->GetBinError(i)*h->GetBinError(i))/(h->GetBinContent(i)*h->GetBinContent(i))
			  +((weight-weightAvg)*(weight-weightAvg))/(weight*weight));
      
      //Fix when error is more than 100%
      if (error>1.0)
	error = 1.0;
      h->SetBinError(i, h->GetBinContent(i)*error);
      //      cout << "Bin error After " << h->GetBinError(i) << endl;
    }
  }
}

void divideByBinWidth(TH1F* h) {

  for (int i=1; i<=h->GetNbinsX(); ++i){
    h->SetBinContent(i, h->GetBinContent(i)/h->GetBinWidth(i));
    h->SetBinError(i, h->GetBinError(i)/h->GetBinWidth(i));
    //    if (i==h->GetNbinsX()) {
    //      h->SetBinContent(i, h->GetBinContent(i)/h->GetBinWidth(i));
    //      h->SetBinError(i, h->GetBinError(i)/h->GetBinWidth(i));
    //    }
  }
}

void makeFits(TString fileName, 
	      TString directory,
	      TString hName,
	      double xmin_fit,
	      double xmax_fit,
	      int isDatacard,
	      char* fitFormulaMain,
	      char* fitFormulaAlt,
	      char* fitFormulaAlt2,
	      TString energy){

  bool debug = true;//false;
  double goodChi2 = 1.5;

  if (debug)
    cout << "========= Now fitting ========= " << directory << " " << hName << endl;
  
  char* fitFormula = fitFormulaMain;

  //  SetStyle();
  TFile* file = TFile::Open(fileName);
  TDirectory* dir;
  TH1F* h;
  if (isDatacard==1){
    dir = (TDirectory*)file->Get(directory);
    dir->cd();
    h = (TH1F*)dir->Get(hName);  
  }else
    h = (TH1F*)file->Get(hName);  
  
  //  computeError(h);

  TF1* f11 = new TF1("f11",fitFormula,xmin_fit,xmax_fit);
  f11->SetParameter(0,h->Integral(10,20));
  f11->SetParameter(1,-0.3);
  f11->SetParameter(2,0.5);

  TH1F* hDensity = (TH1F*)h->Clone();
  divideByBinWidth(hDensity);

  TCanvas* c1 = new TCanvas("c1");
  c1->SetLogy(1);
  hDensity->Draw("e1p");
  cout << "Test fit " << endl;
  hDensity->Fit(f11,"","",xmin_fit,xmax_fit);  
  cout << "Fit " << endl;
  hDensity->Fit(f11,"","",xmin_fit,xmax_fit);
  f11->SetLineColor(kBlack);
  f11->Draw("same");

  double chisquare =  f11->GetChisquare()/f11->GetNDF();
  if (f11->GetNDF()!=0) 
      cout << "Goodness of fit ======= " << chisquare << endl;

  int numberOfPars = f11->GetNpar(); 
  std::vector<double> initialPars;
  std::vector<double> initialParErrors;
  bool parHasLargeUnc = false;
  bool tryAnotherFit = false;
  bool tryThirdFit = false;
  bool fittingDidNotWork = false;
  for (int ipar=0; ipar<numberOfPars; ++ipar){
    double par = f11->GetParameter(ipar);
    double parerror = f11->GetParError(ipar);
    initialPars.push_back(par);
    initialParErrors.push_back(parerror);
    if (TMath::Abs(parerror/par)>0.5){
      parHasLargeUnc = true;
    }
  }

  if (chisquare > goodChi2)
    tryAnotherFit = true;

  //======== If the parameter(s) of fit are comaptible with zero
  //======== Redifine fit with simpler function
  //  if (parHasLargeUnc) {
  if (tryAnotherFit) {
    if (debug) 
      cout << "+++++++++++++ Redifining fit " << endl;
    parHasLargeUnc = false;
    tryAnotherFit = false;
    fitFormula = fitFormulaAlt;
    if (debug)
      cout << "fit function " << fitFormula << endl;
    f11 = new TF1("f11",fitFormula,xmin_fit,xmax_fit);
    hDensity->Fit(f11,"","",xmin_fit,xmax_fit);
    chisquare =  f11->GetChisquare()/f11->GetNDF();
    if (f11->GetNDF()!=0) 
      cout << "Goodness of fit ======= " << chisquare << endl;

    numberOfPars = f11->GetNpar(); 
    initialPars.clear();
    initialParErrors.clear();
    for (int ipar=0; ipar<numberOfPars; ++ipar){
      double par = f11->GetParameter(ipar);
      double parerror = f11->GetParError(ipar);
      initialPars.push_back(par);
      initialParErrors.push_back(parerror);
      if (ipar>0) {
	if (TMath::Abs(parerror/par)>0.5){
	  parHasLargeUnc = true;
	}
      }
      if ( chisquare > goodChi2 )
	tryThirdFit = true;
    }
  
    //Try third fit
    //    if (parHasLargeUnc && tryThirdFit || chisquare > 2) {
    if (tryThirdFit) {
      if (debug)
	cout << "+++++++++++++ Redifining fit third times " << endl;
      parHasLargeUnc = false;
      tryThirdFit = false;
      fitFormula = fitFormulaAlt2;
      if (debug) 
	cout << "fit function " << fitFormula << endl;
      f11 = new TF1("f11",fitFormula,xmin_fit,xmax_fit);
      hDensity->Fit(f11,"","",xmin_fit,xmax_fit);
      chisquare =  f11->GetChisquare()/f11->GetNDF();
      if (f11->GetNDF()!=0) 
	cout << "Goodness of fit ======= " << chisquare << endl;
      
      numberOfPars = f11->GetNpar(); 
      initialPars.clear();
      initialParErrors.clear();
      for (int ipar=0; ipar<numberOfPars; ++ipar){
	double par = f11->GetParameter(ipar);
	double parerror = f11->GetParError(ipar);
	initialPars.push_back(par);
	initialParErrors.push_back(parerror);
	if (TMath::Abs(parerror/par)>1.){
	  parHasLargeUnc = true;
	  fittingDidNotWork = true;
	}
      }
    }
  }
  
  double par0 = initialPars[0];
  f11->FixParameter(0,par0);
  TFitResultPtr fitRes=hDensity->Fit(f11,"S","",xmin_fit,xmax_fit);
  TMatrixDSym cov = fitRes->GetCovarianceMatrix();
  cov.Print();
  
  if (f11->GetNDF()!=0) 
    cout << f11->GetChisquare()/f11->GetNDF() << endl;
  
  int parToVary = numberOfPars-1;
  TMatrixDSym covNew(parToVary);
  for (int ix=0; ix<parToVary; ++ix){
    for (int iy=0; iy<parToVary; ++iy){
      covNew(ix,iy) = cov(ix+1, iy+1);
    }
  }
  cout << endl << endl;
  covNew.Print();
  cout << endl << endl;
  
  int numFitParameter = covNew.GetNrows();
  //Find the Eigenvectors and Eigen value of the covariance matrix
  TMatrixDSymEigen eigencov = covNew;  
  //Get the matrix of Eigen vector
  const TMatrixD eigenvector_matrix = eigencov.GetEigenVectors();
  const TVectorD eigenvalues = eigencov.GetEigenValues();
  
  std::vector<TVectorD*> eigenvectors;
  if (debug)
    cout << "eigenvector_matrix.GetNrows() " <<  eigenvector_matrix.GetNrows() << endl;
  for ( int i = 0; i < eigenvector_matrix.GetNrows(); ++i ) {
    TVectorD* eigenvector = new TVectorD(eigenvector_matrix.GetNrows());
    for ( int j = 0; j < eigenvector_matrix.GetNrows(); ++j ) {
      (*eigenvector)(j) =  eigenvector_matrix(j, i);
    }
    eigenvectors.push_back(eigenvector);
    std::cout << "EigenValue #" << i << " = " << eigenvalues(i) << ": EigenVector = { ";
    for ( int j = 0; j < eigenvector_matrix.GetNrows(); ++j ) {
      std::cout << (*eigenvector)(j);
      if ( j < (eigenvector_matrix.GetNrows() - 1) ) std::cout << ",";
    }
    std::cout << " }" << std::endl;
  }
  
  std::vector<TF1*> systFunctions;
  std::vector<TString> names;
  for( int i = 0; i < numFitParameter; ++i ) {
    //Get the i-th Eigenvector
    const TVectorD& eigenvector = (*eigenvectors[i]);
    //Compute norm of i-th Eigenvector
    double norm = eigenvector.Norm2Sqr();
    //Get the Eigenvalue associate to i-th Eigenvector
    double eigenvalue = eigenvalues[i];
    //Compute uncertainty on fit parameter
    double sigma = sqrt(TMath::Abs(eigenvalue));
    if (debug)
      cout << i << " norm " << norm << " " << eigenvalue << " +/- " << sigma << endl;
    //Compute unit vector in direction of i-th Eigenvector
    TVectorD eigenvector_unit = (1./norm)*eigenvector;
    if (debug)
      cout << i << " eigenvector " << eigenvector[i] << "; unit eigenvector " << eigenvector_unit[i] <<endl;
    
    //    Vary parameters up 
    std::vector<double> upPars;
    for (int j=1;j<initialPars.size();++j){
      double newParUp = initialPars[j] + sigma*eigenvector_unit[j-1];
      upPars.push_back(newParUp);
    }
    TString f12UpName = Form("Par%iUp", i);
    TF1* f12Up = new TF1(f12UpName.Data(),fitFormula,xmin_fit,xmax_fit);
    f12Up->FixParameter(0, par0); 
    for (int j=1;j<initialPars.size();++j){
      f12Up->FixParameter(j,upPars[j-1]);
    }
    if (i==0) {
      f12Up->SetLineColor(kBlue);
    }else{
      f12Up->SetLineColor(kRed);
    }
    f12Up->Draw("same");
    systFunctions.push_back(f12Up);
    names.push_back(f12UpName);
    
    //    Vary parameters down
    std::vector<double> downPars;
    for (int j=1;j<initialPars.size();++j){
      double newParDown = initialPars[j] - sigma*eigenvector_unit[j-1];
      downPars.push_back(newParDown);
    }
    TString f12DownName = Form("Par%iDown", i);
    TF1* f12Down = new TF1(f12DownName.Data(),fitFormula,xmin_fit,xmax_fit);
    f12Down->SetParameter(0, f11->GetParameter(0)); 
    for (int j=1;j<initialPars.size();++j){
      f12Down->SetParameter(j,downPars[j-1]);
    }
    if (i==0){
      f12Down->SetLineColor(kBlue);
      f12Down->SetLineStyle(2);
    } else {
      f12Down->SetLineColor(kRed);
      f12Down->SetLineStyle(2);
    }
    f12Down->Draw("same");
    systFunctions.push_back(f12Down);
    names.push_back(f12DownName);
    
    if (debug) {
      for (int j=1;j<initialPars.size();++j){
	cout << " _________ " << j << endl;
	cout << "Initial " << initialPars[j] << endl;
	cout << "Up   " << upPars[j-1] << endl;
	cout << "Down " << downPars[j-1] << endl;      
      }
    }
  }
  
  if (debug) {
    c1->Print("Fits_withCorr/"+directory+"_"+hName+"_"+energy+"_fit_log.gif");
    
    cout << "Number of fit functions " << systFunctions.size() << endl;
    cout << "Order of functions is such: " << endl;
    cout << "[0] -- par1 Up" << endl;
    cout << "[1] -- par1 Down" << endl;
    cout << "[2] -- par2 Up" << endl;
    cout << "[3] -- par2 Down" << endl;
    cout << "Etc......" << endl;
  }
  
  //Now convert functions to histograms 
  //and store in root file
  TFile* out = new TFile(directory+"_"+hName+".root","recreate"); 
  h->SetName(hName+"_Initial");
  h->SetTitle(hName+"_Initial");
  h->Write();
  h->SetLineColor(1);
  
  //First convert nominal fit into histogram
  TH1F* hCentral = convert(f11, h, 200);
  hCentral->SetName(hName);
  hCentral->SetTitle(hName);
  hCentral->Write();
  
  hCentral->SetLineColor(1);
  hCentral->SetMarkerSize(1.5);
  hCentral->SetMarkerStyle(5);
  h->DrawNormalized();
  hCentral->DrawNormalized("same");
  //Now conver systematic fits into histos
  std::vector<TH1F*> histos;
  TString catname = defineName(directory);
  for (int ifun=0; ifun<systFunctions.size(); ++ifun){
    TF1* thisFunc = systFunctions[ifun];
    TH1F* thisHisto = convert(thisFunc, h, 200);
    TString thisHistoName = hName+"_"+catname+"_"+energy+"_"+hName+"fit"+names[ifun];
    thisHisto->SetName(thisHistoName);
    thisHisto->SetTitle(thisHistoName);
    thisHisto->Write();
    thisHisto->SetLineColor(ifun+1);
    thisHisto->DrawNormalized("same");
  }
  out->Close();
  
  if (debug)
    c1->Print("Fits_withCorr/"+directory+"_"+hName+"_"+energy+"_histo.gif");
}

void makeFitsSimple(TString fileName, 
		    TString directory,
		    TString hName,
		    double xmin_fit,
		    double xmax_fit,
		    int isDatacard,
		    char* fitFormulaMain,
		    char* fitFormulaAlt,
		    char* fitFormulaAlt2,
		    TString energy){
  
  bool debug = true;//false;
  double goodChi2 = 1.5;

  if (debug)
    cout << "========= Now fitting ========= " << directory << " " << hName << endl;
  
  char* fitFormula = fitFormulaMain;

  //  SetStyle();
  TFile* file = TFile::Open(fileName);
  TDirectory* dir;
  TH1F* h;
  if (isDatacard==1){
    dir = (TDirectory*)file->Get(directory);
    dir->cd();
    h = (TH1F*)dir->Get(hName);  
  }else
    h = (TH1F*)file->Get(hName);  
  
  TCanvas* c = new TCanvas("c");
  h->Draw();
  c->Print("test.gif");

  //  computeError(h);

  TF1* f11 = new TF1("f11",fitFormula,xmin_fit,xmax_fit);
  f11->SetParameter(0,h->Integral(10,20));
  f11->SetParameter(1,-0.3);
  f11->SetParameter(2,0.5);

  TH1F* hDensity = (TH1F*)h->Clone();
  divideByBinWidth(hDensity);

  TCanvas* c1 = new TCanvas("c1");
  c1->SetLogy(1);
  hDensity->Draw("e1p");
  cout << "Test fit " << endl;
  hDensity->Fit(f11,"","",xmin_fit,xmax_fit);  
  cout << "Fit " << endl;
  hDensity->Fit(f11,"","",xmin_fit,xmax_fit);
  f11->SetLineColor(kBlack);
  f11->Draw("same");

  double chisquare =  f11->GetChisquare()/f11->GetNDF();
  if (f11->GetNDF()!=0) 
      cout << "Goodness of fit ======= " << chisquare << endl;

  int numberOfPars = f11->GetNpar(); 
  std::vector<double> initialPars;
  std::vector<double> initialParErrors;
  bool parHasLargeUnc = false;
  bool tryAnotherFit = false;
  bool tryThirdFit = false;
  bool fittingDidNotWork = false;
  for (int ipar=0; ipar<numberOfPars; ++ipar){
    double par = f11->GetParameter(ipar);
    double parerror = f11->GetParError(ipar);
    initialPars.push_back(par);
    initialParErrors.push_back(parerror);
    if (TMath::Abs(parerror/par)>0.5){
      parHasLargeUnc = true;
    }
  }

  if (chisquare > goodChi2)
    tryAnotherFit = true;
  
  //======== If chiSquare is large 
  //======== Redifine fit with simpler function
  //  if (parHasLargeUnc || chisquare > 2) {
  if (tryAnotherFit){
    if (debug) 
      cout << "+++++++++++++ Redifining fit second times " << endl;
    parHasLargeUnc = false;
    tryAnotherFit = false;
    fitFormula = fitFormulaAlt;
    if (debug)
      cout << "fit function " << fitFormula << endl;
    f11 = new TF1("f11",fitFormula,xmin_fit,xmax_fit);
    hDensity->Fit(f11,"","",xmin_fit,xmax_fit);
    chisquare =  f11->GetChisquare()/f11->GetNDF();
    if (f11->GetNDF()!=0) 
      cout << "Goodness of fit ======= " << chisquare << endl;

    numberOfPars = f11->GetNpar(); 
    initialPars.clear();
    initialParErrors.clear();
    for (int ipar=0; ipar<numberOfPars; ++ipar){
      double par = f11->GetParameter(ipar);
      double parerror = f11->GetParError(ipar);
      initialPars.push_back(par);
      initialParErrors.push_back(parerror);
      if (ipar>0) {
	if (TMath::Abs(parerror/par)>0.5){
	  parHasLargeUnc = true;
	}
      }
      if ( chisquare > goodChi2)
	tryThirdFit = true;
    }
    //  }
    
    //Try third fit
    if (tryThirdFit) {
      if (debug) 
	cout << "+++++++++++++ Redifining fit third times " << endl;
      parHasLargeUnc = false;
      tryThirdFit = false;
      fitFormula = fitFormulaAlt2;
      if (debug)
	cout << "fit function " << fitFormula << endl;
      f11 = new TF1("f11",fitFormula,xmin_fit,xmax_fit);
      hDensity->Fit(f11,"","",xmin_fit,xmax_fit);
      chisquare =  f11->GetChisquare()/f11->GetNDF();
      if (f11->GetNDF()!=0) 
	cout << "Goodness of fit ======= " << chisquare << endl;
      
      numberOfPars = f11->GetNpar(); 
      initialPars.clear();
      initialParErrors.clear();
      for (int ipar=0; ipar<numberOfPars; ++ipar){
	double par = f11->GetParameter(ipar);
	double parerror = f11->GetParError(ipar);
	initialPars.push_back(par);
	initialParErrors.push_back(parerror);
	if (TMath::Abs(parerror/par)>1.){
	  parHasLargeUnc = true;
	  fittingDidNotWork = true;
	}
      }
    }
  }

  double par0 = initialPars[0];
  f11->FixParameter(0,par0);

  //
  TF1* f11Up1 = new TF1("f11Up1",fitFormula,xmin_fit,xmax_fit);
  TF1* f11Up2 = new TF1("f11Up2",fitFormula,xmin_fit,xmax_fit);
  TF1* f11Down1 = new TF1("f11Down1",fitFormula,xmin_fit,xmax_fit);
  TF1* f11Down2 = new TF1("f11Down2",fitFormula,xmin_fit,xmax_fit);
  
  
  std::vector<TF1*> systFunctions;
  if (initialPars.size()==2) { //Function has two parameters
    //Fix the first one and vary up/down the second one
    double par = initialPars[1];
    double parErr = initialParErrors[1];
    f11Up1->FixParameter(0,par0); 
    f11Up1->FixParameter(1,par+parErr);
    f11Down1->FixParameter(0,par0);
    f11Down1->FixParameter(1,par-parErr);
    f11Up1->SetLineColor(2);
    f11Down1->SetLineColor(2);
    f11Down1->SetLineStyle(2);
    f11Up1->Draw("same");
    f11Down1->Draw("same");
    systFunctions.push_back(f11Up1);
    systFunctions.push_back(f11Down1);
  }
    
  if (initialPars.size()==3){ //Function has three parameters
    for (int j=1;j<initialPars.size();++j){
      //Vary first parameter
      if (j==1){
	double par1 = initialPars[1];
	double par1Err = initialParErrors[1];
	double par2 = initialPars[2];
	double par2Err = initialParErrors[2];
	f11Up1->FixParameter(0,par0); 
	f11Up1->FixParameter(1,par1+par1Err);
	f11Up1->FixParameter(2,par2);
	f11Down1->FixParameter(0,par0);
	f11Down1->FixParameter(1,par1-par1Err);
	f11Down1->FixParameter(2,par2);
	f11Up1->SetLineColor(2);
	f11Down1->SetLineColor(2);
	f11Down1->SetLineStyle(2);
	f11Up1->Draw("same");
	f11Down1->Draw("same");
	systFunctions.push_back(f11Up1);
	systFunctions.push_back(f11Down1);
      }
      if (j==2){
	double par1 = initialPars[1];
	double par1Err = initialParErrors[1];
	double par2 = initialPars[2];
	double par2Err = initialParErrors[2];
	f11Up2->FixParameter(0,par0); 
	f11Up2->FixParameter(1,par1);
	f11Up2->FixParameter(2,par2+par2Err);
	f11Down2->FixParameter(0,par0);
	f11Down2->FixParameter(1,par1);
	f11Down2->FixParameter(2,par2-par2Err);
	f11Up2->SetLineColor(4);
	f11Down2->SetLineColor(4);
	f11Down2->SetLineStyle(2);
	f11Up2->Draw("same");
	f11Down2->Draw("same");
	systFunctions.push_back(f11Up2);
	systFunctions.push_back(f11Down2);
      }
    }
  }

  if (debug) {
    c1->Print("Fits/"+directory+"_"+hName+"_"+energy+"_fit_log.gif");
  }

  //Now convert functions to histograms 
  //and store in root file


  TFile* out = new TFile(directory+"_"+hName+".root","recreate"); 

  //First convert nominal fit into histogram
  TH1F* hCentral = convert(f11, h, xmin_fit); //200
  hCentral->SetName(hName);
  hCentral->SetTitle(hName);
  hCentral->Write();
  
  hCentral->SetLineColor(1);
  hCentral->SetMarkerSize(1.5);
  hCentral->SetMarkerStyle(5);

  h->SetLineColor(1);

  TCanvas* c2 = new TCanvas("c2");
  h->DrawNormalized();
  hCentral->DrawNormalized("same");
  //Now conver systematic fits into histos
  std::vector<TH1F*> histos;
  TString catname = defineName(directory);
  if (systFunctions.size()==2) {
    for (int ifun=0; ifun<systFunctions.size(); ++ifun){
      TF1* thisFunc = systFunctions[ifun];
      /*
      if (ifun==0){
	thisFunc->SetName("fitFuncPar1Up");
	thisFunc->SetTitle("fitFuncPar1Up");
      }else{
	thisFunc->SetName("fitFuncPar1Down");
	thisFunc->SetTitle("fitFuncPar1Down");
      }
      */
      TH1F* thisHisto = convert(thisFunc, h, xmin_fit); //200);
      if (ifun==0){
	thisHisto->SetName(hName+"_fitParUp");
	thisHisto->SetTitle(hName+"_fitParUp");
      }else{
	thisHisto->SetName(hName+"_fitParDown");
	thisHisto->SetTitle(hName+"_fitParDown");
      }

      thisHisto->Write();   
      thisHisto->SetLineColor(ifun+2);
      thisHisto->DrawNormalized("same");
      //      thisFunc->Write();
      
    }
  }

  if (systFunctions.size()==4) {
    /*
    systFunctions[0]->SetName("fitFuncPar1Up");
    systFunctions[0]->SetTitle("fitFuncPar1Up");
    systFunctions[1]->SetName("fitFuncPar1Down");
    systFunctions[1]->SetTitle("fitFuncPar1Down");

    systFunctions[2]->SetName("fitFuncPar2Up");
    systFunctions[2]->SetTitle("fitFuncPar2Up");
    systFunctions[3]->SetName("fitFuncPar2Down");
    systFunctions[3]->SetTitle("fitFuncPar2Down");
    */
      
    TH1F* thisHistoUp = convertWithEnvelope(f11, 
					    systFunctions[0],systFunctions[1],
					    systFunctions[2],systFunctions[3],
					    h, xmin_fit, true, true);
    TString thisHistoName = hName+"_"+catname+"_"+energy+"_"+hName+"fitParUp";
    thisHistoUp->SetName(thisHistoName);
    thisHistoUp->SetTitle(thisHistoName);
    thisHistoUp->Write();
    thisHistoUp->SetLineColor(2);
    thisHistoUp->DrawNormalized("same");
    cout << endl << endl << endl;

    TH1F* thisHistoDown = convertWithEnvelope(f11, 
					      systFunctions[0],systFunctions[1],
					      systFunctions[2],systFunctions[3],
					      h, xmin_fit, true, false);
    thisHistoName = hName+"_"+catname+"_"+energy+"_"+hName+"fitParDown";
    thisHistoDown->SetName(thisHistoName);
    thisHistoDown->SetTitle(thisHistoName);
    thisHistoDown->Write();
    thisHistoDown->SetLineColor(3);
    thisHistoDown->DrawNormalized("same");  
    /*
    systFunctions[0]->Write();
    systFunctions[1]->Write();
    systFunctions[2]->Write();
    systFunctions[3]->Write();
    */
    cout << endl << endl << endl;

  }

  h->SetName(hName+"_Initial");
  h->SetTitle(hName+"_Initial");
  h->Write();
  out->Close();
  
  if (debug) 
    c2->Print("Fits/"+directory+"_"+hName+"_"+energy+"_histo.gif");
  
}

void FitTails(TString mode = "mu", TString energy = "8TeV", TString file="htt_mt.inputs-mssm-8TeV-0.root") {
  int isDatacard = 1;
  char* fitFormulaExp1 = "[0]*exp([1]*TMath::Power(x,[2]))";
  //  char* fitFormulaExp2 = "[0]*exp([1]/(x+[2]))";
  char* fitFormulaExp2 = "[0]*exp([1]*x)";
  char* fitFormulaHyp = "[0]/TMath::Power(x,[1])";
  //  char* fitFormulaHyp = "1./([0]+[1]*x+[2]*x*x)";
  
  TString hName[3] = {"QCD", "W", "TT"};
  //TString hName[1] = {"W"};
  TString category[2] = {mode + "Tau_nobtag",
  			 mode + "Tau_btag"};
  //  TString category[1] = {mode + "Tau_btag"};
  
  //  double xmin_fit[3] = {120, 200, 200};
  double xmin_fit[3] = {150, 150, 150};
  double xmax_fit[3] = {1500, 1500, 1500};
  
  cout << mode << '\t' << file << endl;
  
  for(int icat = 0; icat < 2; ++icat) {
    // loop over categories
    TString cat = category[icat];
    for(int iname = 2; iname < 3; ++iname) {
      TString name = hName[iname];
      //      makeFitsSimple(file, cat, name, xmin_fit[iname], xmax_fit[iname], isDatacard, fitFormulaExp2, fitFormulaExp1, fitFormulaHyp, energy);
      makeFits(file, cat, name, xmin_fit[iname], xmax_fit[iname], isDatacard, fitFormulaExp1, fitFormulaExp2, fitFormulaHyp, energy);
      //      makeFits(file, cat, name, xmin_fit[iname], xmax_fit[iname], isDatacard, fitFormulaExp1, fitFormulaExp2, fitFormulaHyp, energy);
    }
  }
}
