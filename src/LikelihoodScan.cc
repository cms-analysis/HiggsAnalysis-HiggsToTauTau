#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

/// This is the core plotting routine that can also be used within
/// root macros. It is therefore not element of the PlotLimits class.
void plotting1DScan(TCanvas& canv, TH1F* plot1D, std::string& xaxis, std::string& yaxis, std::string& masslabel, int mass, double max, int lowerBin, int upperBin, bool log);

/*
void 
PlotLimits::band1D(ostream& out, std::string& xval, std::string& yval, TGraph* bestFit, TGraph* band, float xoffset, float yoffset, std::string CL)
{
  float xmin = -1, xmax = -1.;
  float ymin = -1, ymax = -1.; 
  for(int i=0; i<band->GetN(); ++i){
    if(xmin<0 || band->GetX()[i]<xmin){
      xmin = band->GetX()[i];
    }
    if(xmax<0 || band->GetX()[i]>xmax){
      xmax = band->GetX()[i];
    }
    if(ymin<0 || band->GetY()[i]<ymin){
      ymin = band->GetY()[i];
    }
    if(ymax<0 || band->GetY()[i]>ymax){
      ymax = band->GetY()[i];
    }
  }
  xmin-=xoffset, xmax-=xoffset; ymin-=yoffset, ymax-=yoffset;
  out << std::setw(3) << " " << xval << " :"
      << std::setw(5) << " " << std::fixed << std::setprecision(3) << bestFit->GetX()[0]
      << std::setw(4) << "-" << std::fixed << std::setprecision(3) << TMath::Abs(xmin-bestFit->GetX()[0])
      << "/+" << std::fixed  << std::setprecision(3) << xmax-bestFit->GetX()[0]
      << " " << CL << std::endl;

  out << std::setw(3) << " " << yval << " :"
      << std::setw(5) << " " << std::fixed << std::setprecision(3) << bestFit->GetY()[0]
      << std::setw(4) << "-" << std::fixed << std::setprecision(3) << TMath::Abs(ymin-bestFit->GetY()[0]>0 ? bestFit->GetY()[0] : ymin-bestFit->GetY()[0])
      << "/+" << std::fixed  << std::setprecision(3) << ymax-bestFit->GetY()[0]
      << " " << CL << std::endl;
}
*/

void
PlotLimits::plot1DScan(TCanvas& canv, const char* directory)
{
  // set up styles
  SetStyle();
  
  // pick up boundaries of the scan from .scan file in masses directory. This
  // requires that you have run limits.py beforehand with option --multidim-fit
  char type[20]; 
  float first, second;
  int points=0;
  float xmin, xmax;
  for(unsigned int imass=0; imass<bins_.size(); ++imass){
    // buffer mass value
    float mass = bins_[imass];
    if(verbosity_>2){ std::cout << mass << std::endl; }
    std::string line; 
    ifstream file(TString::Format("%s/%d/.scan", directory, (int)mass));
    if(file.is_open()){
      while( file.good() ){
	getline(file,line);
	sscanf(line.c_str(),"%s : %f %f", type, &first, &second);
	if(std::string(type)==std::string("points")){ points = int(first); }
	if(std::string(type)==std::string("r")){ xmin = first; xmax = second; }
      }
      file.close();
    }
    if(verbosity_>1){
      std::cout << "mass: " << mass << ";" << " points: " << points << ";"
		<< " r : " << xmin << " -- " << xmax << ";" 
		<< std::endl;
    }

    // tree scan
    char* label = model_.empty() ? (char*)"Test" : (char*)model_.c_str();// int i=0;
    //while(label[i]){ label[i]=putchar(toupper(label[i])); ++i; } std::cout << " : ";
    TString fullpath = TString::Format("%s/%d/higgsCombine%s.MultiDimFit.mH%d.root", directory, (int)mass, label, (int)mass);
    std::cout << "open file: " << fullpath << std::endl;
    TFile* file_ = TFile::Open(fullpath); if(!file_){ std::cout << "--> TFile is corrupt: skipping masspoint." << std::endl; continue; }
    TTree* limit = (TTree*) file_->Get("limit"); if(!limit){ std::cout << "--> TTree is corrupt: skipping masspoint." << std::endl; continue; }
    float nll, x;
    float nbins = points;
    bool validValue = false;
    int lowerBin = 0; int upperBin = nbins;
    TH1F* scan1D = new TH1F("scan1D", "", nbins, xmin, xmax);
    float nll_min = limit->GetMinimum("deltaNLL");
    limit->SetBranchAddress("deltaNLL", &nll );
    limit->SetBranchAddress(std::string("r").c_str() , &x);
    int nevent = limit->GetEntries();
    for(int i=0; i<nevent; ++i){
      limit->GetEvent(i);
      //std::cout << "bin:" << scan1D->FindBin(x) << " -- r=" << x << " -- NLL=" << nll << std::endl; 
      if(scan1D->GetBinContent(scan1D->FindBin(x))==0){
	// catch small negative values that might occure due to rounding
	if(fabs(nll-nll_min)>50){
	  if(validValue){
	    lowerBin = scan1D->FindBin(x);
	  }
	  else{
	    upperBin = scan1D->FindBin(x);
	  }
	}
	else{
	  validValue=true;
	  scan1D->Fill(x, fabs(nll-nll_min));
	}
      }
    }
    // determine bestfit graph 
    float bestFit=-1.; 
    float buffer=0., bestX=-999.;
    bool start=false;
    for(int i=0; i<nevent; ++i){
      limit->GetEvent(i);
      buffer=scan1D->GetBinContent(scan1D->FindBin(x));
      if(buffer>0.3) start=true;
      if ((bestFit<0 || bestFit>buffer) && start==true){
	//std::cout << "update bestFit coordinates: " << std::endl;
	//std::cout << "-->old: x=" << bestX << " value=" << bestFit << std::endl;
	// adjust best fit to granularity of scan; we do this to prevent artefacts 
	// when quoting the 1d uncertainties of the scan. For the plotting this 
	// does not play a role. 
	bestX=scan1D->GetXaxis()->GetBinCenter(scan1D->GetXaxis()->FindBin(x)); 
	bestFit=buffer; 
	//std::cout << "-->new: x=" << bestX << " y=" << bestY << " value=" << bestFit << std::endl;
      }
    }
    //  if(verbosity_>0){
    //    std::cout << "Bestfit value from likelihood-scan:" << std::endl;
    //    std::cout << "x=" << bestX << " value=" << bestFit << std::endl;
    //  }
    TGraph* bestfit = new TGraph();
    bestfit->SetPoint(0, bestX, 0);
    // find quantileExpected values
    float plus_2sigma_below=-99,  plus_2sigma_above=-99,  plus_2sigma_below_x=-99,  plus_2sigma_above_x=-99;
    float minus_2sigma_below=-99, minus_2sigma_above=-99, minus_2sigma_below_x=-99, minus_2sigma_above_x=-99;
    float plus_1sigma_below=-99,  plus_1sigma_above=-99,  plus_1sigma_below_x=-99,  plus_1sigma_above_x=-99;
    float minus_1sigma_below=-99, minus_1sigma_above=-99, minus_1sigma_below_x=-99, minus_1sigma_above_x=-99;
    for(int i=0; i<nevent; ++i){
      if (i+1==nevent) break;
      limit->GetEvent(i);
      double nll_first=nll-nll_min;
      limit->GetEvent(i+1);
      double nll_second=nll-nll_min;
      if( fabs(nll_first-nll_second)>25 ) continue;
      limit->GetEvent(i);
      if (nll-nll_min>1.92 && x<bestX) {
	limit->GetEvent(i+1);	
	if (nll-nll_min<1.92 && x<bestX) {
	  limit->GetEvent(i);   minus_2sigma_above=nll-nll_min; minus_2sigma_above_x=x;
	  limit->GetEvent(i+1); minus_2sigma_below=nll-nll_min; minus_2sigma_below_x=x;
	}
      }
      limit->GetEvent(i);
      if (nll-nll_min>0.5 && x<bestX) {
	limit->GetEvent(i+1);	
	if (nll-nll_min<0.5 && x<bestX) {
	  limit->GetEvent(i);   minus_1sigma_above=nll-nll_min; minus_1sigma_above_x=x;
	  limit->GetEvent(i+1); minus_1sigma_below=nll-nll_min; minus_1sigma_below_x=x;
	}
      }
      limit->GetEvent(i);
      if (nll-nll_min<0.5 && x>bestX) {
	limit->GetEvent(i+1);	
	if (nll-nll_min>0.5 && x>bestX) {
	  limit->GetEvent(i);   plus_1sigma_below=nll-nll_min; plus_1sigma_below_x=x;
	  limit->GetEvent(i+1); plus_1sigma_above=nll-nll_min; plus_1sigma_above_x=x;
	}
      }
      limit->GetEvent(i);
      if (nll-nll_min<1.92 && x>bestX) {
	limit->GetEvent(i+1);	
	if (nll-nll_min>1.92 && x>bestX) {
	  limit->GetEvent(i);   plus_2sigma_below=nll-nll_min; plus_2sigma_below_x=x; 
	  limit->GetEvent(i+1); plus_2sigma_above=nll-nll_min; plus_2sigma_above_x=x;
	}
      }
    }
    // calculate linear interpolation to get 95CL or 68CL and
    // build the MaximumLikelihood root output for bestfit plots  
    TString newfullpath = TString::Format("%s/%d/higgsCombineTest.MaxLikelihoodFit.mH%d.root", directory, (int)mass, (int)mass);
    TFile *newfile_ = new TFile(newfullpath, "RECREATE"); 
    TTree *newlimit = new TTree("limit", "limit"); 
    double l; float quantile_expected;
    newlimit->Branch("quantileExpected", &quantile_expected);
    newlimit->Branch("limit", &l);
    float CL_p025=-99, CL_p16=-99, CL_p84=-99, CL_p975=-99;
    int new_nevent=0;
    if (minus_2sigma_above>0 && minus_2sigma_below>0) {
      CL_p025= ( 1.92*(minus_2sigma_above_x - minus_2sigma_below_x) - minus_2sigma_below*minus_2sigma_above_x + minus_2sigma_above*minus_2sigma_below_x) / (minus_2sigma_above-minus_2sigma_below);
      newlimit->GetEvent(new_nevent);
      quantile_expected=0.025;
      l=CL_p025;
      newlimit->Fill();
      new_nevent++;
	}
    if (minus_1sigma_above>0 && minus_1sigma_below>0) {
      CL_p16= ( 0.5*(minus_1sigma_above_x - minus_1sigma_below_x) - minus_1sigma_below*minus_1sigma_above_x + minus_1sigma_above*minus_1sigma_below_x) / (minus_1sigma_above-minus_1sigma_below);
      newlimit->GetEvent(new_nevent);
      quantile_expected=0.16;
      l=CL_p16;
      newlimit->Fill();
      new_nevent++;
    }
    quantile_expected=-1;
    l=bestX;
    newlimit->Fill();
    new_nevent++;
    if (plus_1sigma_above>0 && plus_1sigma_below>0) {
      CL_p84= ( 0.5*(plus_1sigma_above_x - plus_1sigma_below_x) - plus_1sigma_below*plus_1sigma_above_x + plus_1sigma_above*plus_1sigma_below_x) / (plus_1sigma_above-plus_1sigma_below);
      newlimit->GetEvent(new_nevent);
      quantile_expected=0.84;
      l=CL_p84;
      newlimit->Fill();
      new_nevent++;
    }
    if (plus_2sigma_above>0 && plus_2sigma_below>0) {
      CL_p975= ( 1.92*(plus_2sigma_above_x - plus_2sigma_below_x) - plus_2sigma_below*plus_2sigma_above_x + plus_2sigma_above*plus_2sigma_below_x) / (plus_2sigma_above-plus_2sigma_below);
      newlimit->GetEvent(new_nevent);
      quantile_expected=0.975;
      l=CL_p975;
      newlimit->Fill();
    }
    if(verbosity_>0){
      std::cout << "quantileExpected values for likelihood-scan:" << std::endl;
      std::cout << "minus_2sigma = " << CL_p025 << std::endl;
      std::cout << "minus_1sigma = " << CL_p16 << std::endl;
      std::cout << "medium = " << bestX << std::endl; 
      std::cout << "plus_1sigma = " << CL_p84 << std::endl;
      std::cout << "plus_2sigma = " << CL_p975 << std::endl;
    }
    newfile_->Write();
    newfile_->Close();
    // do the plotting
    std::string masslabel = mssm_ ? std::string("m_{#phi}") : std::string("m_{H}");
    plotting1DScan(canv, scan1D, xaxis_, yaxis_, masslabel, mass, max_, lowerBin, upperBin, log_);    
    // add the CMS Preliminary stamp
    CMSPrelim(dataset_.c_str(), "", 0.160, 0.835);
    //CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);
    // print 1d band
    //ofstream scanOut;  
    //scanOut.open(TString::Format("%s/%d/multi-dim.fitresult", directory, (int)mass));
    //scanOut << " --- MultiDimFit ---" << std::endl;
    //scanOut << "best fit parameter values and uncertainties from NLL scan:" << std::endl;
    //band1D(scanOut, xval, yval, bestfit, graph68, (xmax-xmin)/nbins/2, (ymax-ymin)/nbins/2, "(68%)");

    if(png_){
      canv.Print(TString::Format("%s-%s-%d.png", output_.c_str(), label_.c_str(), (int)mass));
    }
    if(pdf_){
      canv.Print(TString::Format("%s-%s-%d.pdf", output_.c_str(), label_.c_str(), (int)mass));
      canv.Print(TString::Format("%s-%s-%d.eps", output_.c_str(), label_.c_str(), (int)mass));
    }
    if(txt_){
      TString path;
      path = TString::Format("%s_%s_%s-%d-CL68", output_.c_str(), label_.c_str(), model_.c_str(), (int)mass);
      //print(path, xval, yval, graph68, "txt"); print(path, xval, yval, graph68, "tex");
      path = TString::Format("%s_%s_%s-%d-CL95", output_.c_str(), label_.c_str(), model_.c_str(), (int)mass);
      //print(path, xval, yval, graph95, "txt"); print(path, xval, yval, graph95, "tex");
    }
    if(root_){
      TFile* output = new TFile("likelihood-scan.root", "update");
      if(!output->cd(output_.c_str())){
	output->mkdir(output_.c_str());
	output->cd(output_.c_str());
      }
      if(bestfit){ bestfit->Write(TString::Format("bestfit_%d", (int)mass)); }
      scan1D->Write(TString::Format("plot1D_%d", (int)mass));
      output->Close();
    }
  }
  return;
  }
