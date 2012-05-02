#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"


PlotLimits::PlotLimits(const char* output, const edm::ParameterSet& cfg) : output_(output), 
  dataset_(cfg.getParameter<std::string>("dataset")),
  xaxis_(cfg.getParameter<std::string>("xaxis")), 
  yaxis_(cfg.getParameter<std::string>("yaxis")), 
  mssm_ (cfg.getParameter<bool  >("mssm")), 
  png_  (cfg.getParameter<bool  >("png" )), 
  pdf_  (cfg.getParameter<bool  >("pdf" )), 
  txt_  (cfg.getParameter<bool  >("txt" )), 
  root_ (cfg.getParameter<bool  >("root")), 
  min_  (cfg.getParameter<double>("min" )), 
  max_  (cfg.getParameter<double>("max" )), 
  log_  (cfg.getParameter<int   >("log") ), 
  verbosity_(cfg.getParameter<unsigned int>("verbosity")),
  outputLabel_(cfg.getParameter<std::string>("outputLabel")) 
{
  bins_=cfg.getParameter<std::vector<double> >("masspoints");
  for(unsigned int i=0; i<bins_.size(); ++i) valid_.push_back(true);
}

void 
PlotLimits::prepareSimple(const char* directory, std::vector<double>& values, const char* filename)
{ 
  for(unsigned int imass=0; imass<bins_.size(); ++imass){
    double value=-1.;
    std::string buffer = std::string(filename);
    std::string filehead = buffer.substr(0, buffer.find("$MASS"));
    std::string filetail = buffer.substr(buffer.find("$MASS")+5, std::string::npos);
    TString fullpath(TString::Format("%s/%d/%smH%d%s.root", directory, (int)bins_[imass], filehead.c_str(), (int)bins_[imass], filetail.c_str()));
    if(verbosity_>0) std::cout << "INFO: opening file " << fullpath << std::endl;
    TFile* file = new TFile(fullpath); 
    if(file->IsZombie()){
      if(verbosity_>0){
	std::cout << "INFO: file not found: " << fullpath  << std::endl
		  << "      leave value at -1. to invalidate" << std::endl;
      }
      valid_[imass]=false;
    }
    else{
      TTree* limit = (TTree*) file->Get("limit");
      if(!limit){
	if(verbosity_>0){
	  std::cout << "INFO: tree not found: limit" << std::endl
		    << "      leave value at -1. to invalidate" << std::endl; 
	}
	valid_[imass]=false;
      }
      else{
	double x; 
	limit->SetBranchAddress("limit", &x);
	int nevent = limit->GetEntries();
	for(int i=0; i<nevent; ++i){
	  limit->GetEvent(i);
	  value = x;
	}
      }
      file->Close();
    }
    values.push_back(value);
  }
  return;
}

void 
PlotLimits::prepareAsymptotic(const char* directory, std::vector<double>& values, const char* type)
{
  for(unsigned int imass=0; imass<bins_.size(); ++imass){
    double value=-1.;
    TString fullpath;
    if(std::string(type)==std::string("observed")){
      fullpath = TString::Format("%s/%d/higgsCombine-obs.Asymptotic.mH%d.root", directory, (int)bins_[imass], (int)bins_[imass]);
    }
    else{
      fullpath = TString::Format("%s/%d/higgsCombine-exp.Asymptotic.mH%d.root", directory, (int)bins_[imass], (int)bins_[imass]);
    }
    if(verbosity_>0){
      std::cout << "INFO: type is " << type << std::endl;
      std::cout << "INFO: opening file " << fullpath << std::endl;
    }
    TFile* file = new TFile(fullpath); 
    if(file->IsZombie()){
      if(verbosity_>0){
	std::cout << "INFO: file not found: " << fullpath  << std::endl
		  << "       leave value at -1. to invalidate" << std::endl;
      }
      valid_[imass]=false;
    }
    else{
      TTree* limit = (TTree*) file->Get("limit");
      if(!limit){
	if(verbosity_>0){
	  std::cout << "ERROR: tree not found: limit" << std::endl
		    << "       leave value at -1. to invalidate" << std::endl; 
	}
	valid_[imass]=false;
      }
      else{
	double x; 
	std::vector<double> limits;
	limit->SetBranchAddress("limit", &x);
	int nevent = limit->GetEntries();
	// for asymptotic it can happen that the pre-fit does not converge and 
	// that the tree does exist but it is empty. We also need to catch this 
	// case here
	if(nevent<=0){
	  valid_[imass]=false;
	}
	for(int i=0; i<nevent; ++i){
	  limit->GetEvent(i);
	  // we have six options: observed, -2sigma, -1sigma, median, +1sigma, 
	  // +2sigma; for observed the tree has only one entry and the loop 
	  // ends here automatically, else we break after the corresponding
	  // entry
	  value = x;
	  // for asymptotic it can happen that the limit calculation does not 
	  // come to a result due to difficulties with the pre-fit. In this 
	  // cases expected and observed limit are 0. We also need to catch 
	  // this case here  
	  if(value<=0){
	    std::cout << "invalidate MASS " << imass << std::endl;
	    valid_[imass]=false;
	  }
	  else{
	    limits.push_back(x);
	  }
	}
	std::sort(limits.begin(), limits.end());
	if(std::string(type)==std::string("observed")){ 
	  if(limits.size()<=0) {
	    if(verbosity_>1){
	      std::cout << "INFO: no observed limit for this file and masspoint. Masspoint invalidated" << std::endl;
	    }
	    valid_[imass]=false;
	  }
	  else{
	    value=limits[0]; 
	  }
	}
	else{
	  if(limits.size()<5){
	    if(verbosity_>1){
	      std::cout << "INFO: not all quantiles available for uncertainty bands for this file and masspoint. Masspoint invalidated" << std::endl;
	    }
	    valid_[imass]=false;
	  }
	  else{
	    if(std::string(type)==std::string("-2sigma" )){ value=limits[0]; }
	    if(std::string(type)==std::string("-1sigma" )){ value=limits[1]; }
	    if(std::string(type)==std::string("median"  )){ value=limits[2]; }
	    if(std::string(type)==std::string("+1sigma" )){ value=limits[3]; }
	    if(std::string(type)==std::string("+2sigma" )){ value=limits[4]; }	  
	  }
	}
      }
      file->Close();
    }
    values.push_back(value);
  }
  return;
}

void 
PlotLimits::prepareBayesian(const char* directory, std::vector<double>& values, const char* type)
{
  for(unsigned int imass=0; imass<bins_.size(); ++imass){
    double value=-1.;
    TString fullpath(TString::Format("%s/%d/batch_collected.root", directory, (int)bins_[imass]));
    if(verbosity_>0) std::cout << "INFO: opening file " << fullpath << std::endl;
    TFile* file = new TFile(fullpath);
    if(file->IsZombie()){
      if(verbosity_>0){
	std::cout << "INFO: file not found: " << fullpath  << std::endl
		  << "      leave value at -1. to invalidate" << std::endl;
      }
      valid_[imass]=false;
    }
    else{
      TTree* limit = (TTree*) file->Get("limit");
      if(!limit){
	if(verbosity_>0){
	  std::cout << "INFO: tree not found: limit" << std::endl
		    << "      leave value at -1. to invalildate" << std::endl; 
	}
	valid_[imass]=false;
      }
      else{           
	double x;
	double mean=0, var=0;
	// vector for simple median determination
	std::vector<double> limits;
	limit->SetBranchAddress("limit", &x);
	int nevent = limit->GetEntries();
	for(int i=0; i<nevent; ++i){
	  limit->GetEvent(i);
	  if(x<999999){
	    // fill for median determination
	    limits.push_back(x);
	    // mean(x)
	    mean +=1./(i+1)*(x-mean);
	    // mean(x**2)
	    var  +=1./(i+1)*(x*x-var);
	  }
	}
	// var = mean(x**2)-mean(x)**2
	var-= mean*mean;
	// sort for quantile determination
	std::sort(limits.begin(), limits.end());

	/*
	for(unsigned int i=0; i<limits.size(); ++i){
	  var+=1./limits.size()*(limits[i]-mean)*(limits[i]-mean);
	}
	*/

	// using standard deviations can result in bands that span below 0
	// we therefore use quantiles here for +/-1 ans +/-2 sigma also for 
	// bayesian; the measn remains as it is 
	if(std::string(type)==std::string("mean"   ) ){ value= mean; }
	else if(std::string(type)==std::string("+2sigma") ){ value= limits[(int)(0.975*limits.size())];}//+2*sqrt(var);}                
	else if(std::string(type)==std::string("+1sigma") ){ value= limits[(int)(0.840*limits.size())];}//+1*sqrt(var);}
	else if(std::string(type)==std::string("median" ) ){ value= limits[(int)(0.500*limits.size())];} 
	else if(std::string(type)==std::string("-1sigma") ){ value= limits[(int)(0.160*limits.size())];}//-1*sqrt(var);}
	else if(std::string(type)==std::string("-2sigma") ){ value= limits[(int)(0.027*limits.size())];}//-2*sqrt(var);}
	else{
	  std::cout << "ERROR: picked wrong type. Available types are: +2sigma, +1sigma, mean, median, -1sigma, -2sigma" << std::endl
		    << "       for the moment I'll stop here" << std::endl;
	  exit(1);
	}
      }
      file->Close();
    }
    values.push_back(value);
  }
  return;
}

TGraph* 
PlotLimits::fillCentral(const char* directory, TGraph* plot, const char* filename)
{ 
  std::vector<double> central;
  if(std::string(filename)==std::string("median") || std::string(filename)==std::string("mean")){
    prepareBayesian(directory, central, filename);
  }
  else if(std::string(filename)==std::string("asym-observed")){
    prepareAsymptotic(directory, central, "observed");
  }
  else if(std::string(filename)==std::string("asym-expected")){
    prepareAsymptotic(directory, central, "median");
  }
  else if(std::string(filename)==std::string("HIG-11-020-observed")){
    prepareHIG_11_020(central, "observed", false);
  }
  else if(std::string(filename)==std::string("HIG-11-020-expected")){
    prepareHIG_11_020(central, "expected", false);
  }
  else if(std::string(filename)==std::string("HIG-11-029-observed")){
    prepareHIG_11_029(central, "observed");
  }
  else if(std::string(filename)==std::string("HIG-11-029-expected")){
    prepareHIG_11_029(central, "expected");
  }
  else{
    prepareSimple(directory, central, filename);
  }
  for(unsigned int imass=0, ipoint=0; imass<bins_.size(); ++imass){
    if(valid_[imass]){
      plot->SetPoint(ipoint, bins_[imass], central[imass]);
      ++ipoint; // only add valid mass points to the TGraph
    }
    if(verbosity_>1){
      // second verbosity level
      std::cout << "INFO: central [" << bins_[imass] << "] = " << central[imass] << "[" << (valid_[imass] ? "OK]" : "FAILED]") << std::endl;
    }
  }
  return plot;
}

TGraphAsymmErrors* 
PlotLimits::fillBand(const char* directory, TGraphAsymmErrors* plot, const char* method, bool innerBand)
{ 
  std::vector<double> upper, lower, expected;

  if(std::string(method) == std::string("Bayesian")){
    prepareBayesian(directory, expected, "median");
    prepareBayesian(directory, upper, innerBand ? "+1sigma" : "+2sigma");
    prepareBayesian(directory, lower, innerBand ? "-1sigma" : "-2sigma");
  }
  else if(std::string(method) == std::string("Asymptotic")){
    prepareAsymptotic(directory, expected, "median");
    prepareAsymptotic(directory, upper, innerBand ? "+1sigma" : "+2sigma");
    prepareAsymptotic(directory, lower, innerBand ? "-1sigma" : "-2sigma");
  }
  else if(std::string(method) == std::string("CLs")){
    prepareCLs(directory, expected, ".quant0.500");
    prepareCLs(directory, upper, innerBand ? ".quant0.840" : ".quant0.975");
    prepareCLs(directory, lower, innerBand ? ".quant0.160" : ".quant0.027");
  }
  else if(std::string(method) == std::string("HIG-11-020")){
    bool xsec = false;
    prepareHIG_11_020(expected, "expected", xsec);
    prepareHIG_11_020(upper, innerBand ? "+1sigma" : "+2sigma", xsec);
    prepareHIG_11_020(lower, innerBand ? "-1sigma" : "-2sigma", xsec);
  }
  else if(std::string(method) == std::string("HIG-11-029")){
    prepareHIG_11_029(expected, "expected");
    prepareHIG_11_029(upper, innerBand ? "+1sigma" : "+2sigma");
    prepareHIG_11_029(lower, innerBand ? "-1sigma" : "-2sigma");
  }
  else{
    std::cout << "ERROR: chose wrong method to fill uncertainty band. Available methods are: Bayesian, CLs" 
	      << "       for the moment I'll stop here" << std::endl;
    exit(1); 
  }

  for(unsigned int imass=0, ipoint=0; imass<bins_.size(); ++imass){
    if(valid_[imass]){
      plot->SetPoint(ipoint, bins_[imass], expected[imass]);
      plot->SetPointEYhigh(ipoint, upper[imass] - expected[imass]);
      plot->SetPointEYlow (ipoint, expected[imass] - lower[imass]);
      ++ipoint; // only add valid mass points to the TGraph
    }
    if(verbosity_>1){
      // second verbosity level
      std::cout << "INFO: Calculating " << (innerBand ? "inner" : "outer") << " uncertainty band" << std::endl;
      std::cout << "INFO: upper    [" << bins_[imass] << "] = " << " (" << upper[imass] << ") " << "[" << (valid_[imass] ? "OK]" : "FAILED]") << std::endl;
      std::cout << "INFO: expected [" << bins_[imass] << "] = " << expected[imass]          << "[" << (valid_[imass] ? "OK]" : "FAILED]") << std::endl;
      std::cout << "INFO: lower    [" << bins_[imass] << "] = " << " (" << lower[imass] << ") " << "[" << (valid_[imass] ? "OK]" : "FAILED]") << std::endl;
    }
  }
  return plot;
}

void 
PlotLimits::print(const char* filename, TGraphAsymmErrors* outerBand, TGraphAsymmErrors* innerBand, TGraph* expected, TGraph* observed, const char* type)
{
  if(std::string(type) == std::string("tex")){
    ofstream file;  
    file.open (std::string(filename).append(".tex").c_str());
    file 
      << std::endl << "\\hline" << std::endl << "     "
      << "   " << std::setw(15) << std::right << "    $m_{X}$"
      << " & " << std::setw(15) << std::right << "$-2\\sigma$"
      << " & " << std::setw(15) << std::right << "$-1\\sigma$"
      << " & " << std::setw(15) << std::right << "     Median"
      << " & " << std::setw(15) << std::right << "$+1\\sigma$"
      << " & " << std::setw(15) << std::right << "$+2\\sigma$"
      << " & " << std::setw(15) << std::right << "Obs. Limit [pb]"
      << std::right << "  \\\\"
      << std::endl << "\\hline" << std::endl;
    for(int imass=0; imass<expected->GetN(); ++imass){
      file 
	<< "   " << std::setw(15) << std::setprecision(3) << std::right << expected->GetX()[imass] << "~\\GeV"
	<< " & " << std::setw(15) << std::setprecision(3) << std::right << expected->GetY()[imass] - outerBand->GetEYlow()[imass]
	<< " & " << std::setw(15) << std::setprecision(3) << std::right << expected->GetY()[imass] - innerBand->GetEYlow()[imass]
	<< " & " << std::setw(15) << std::setprecision(3) << std::right << expected->GetY()[imass]
	<< " & " << std::setw(15) << std::setprecision(3) << std::right << expected->GetY()[imass] + innerBand->GetEYhigh()[imass]
	<< " & " << std::setw(15) << std::setprecision(3) << std::right << expected->GetY()[imass] + outerBand->GetEYhigh()[imass];
      if(observed){
	file
	  << " & " << std::setw(15) << std::right << observed->GetY()[imass];
      }
      file
	<< std::right << "  \\\\"
	<< std::endl << "\\hline" << std::endl;
    }
    file.close();
  }
  if(std::string(type) == std::string("txt")){
    ofstream file;  
    file.open (std::string(filename).append(".txt").c_str());
    file 
      << "#"
      << "   " << std::setw(15) << std::right << "         mX"
      << "   " << std::setw(15) << std::right << "   -2 sigma"
      << "   " << std::setw(15) << std::right << "   -1 sigma"
      << "   " << std::setw(15) << std::right << "     Median"
      << "   " << std::setw(15) << std::right << "   +1 sigma"
      << "   " << std::setw(15) << std::right << "   +2 sigma"
      << "   " << std::setw(15) << std::right << "Obs. Limit [pb]"
      << std::endl;
    for(int imass=0; imass<expected->GetN(); ++imass){
      file 
	<< "   " << std::setw(15) << std::setprecision(3) << std::right << expected->GetX()[imass] 
	<< "   " << std::setw(15) << std::setprecision(3) << std::right << expected->GetY()[imass] - outerBand->GetEYlow()[imass]
	<< "   " << std::setw(15) << std::setprecision(3) << std::right << expected->GetY()[imass] - innerBand->GetEYlow()[imass]
	<< "   " << std::setw(15) << std::setprecision(3) << std::right << expected->GetY()[imass]
	<< "   " << std::setw(15) << std::setprecision(3) << std::right << expected->GetY()[imass] + innerBand->GetEYhigh()[imass]
	<< "   " << std::setw(15) << std::setprecision(3) << std::right << expected->GetY()[imass] + outerBand->GetEYhigh()[imass];
      if(observed){
	file
	  << "   " << std::setw(15) << std::right << observed->GetY()[imass];
      }
      file
	<< std::endl;
    }
    file.close();
  }
}

void 
PlotLimits::plot(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed)
{
  // set up styles
  SetStyle();

  canv.cd();
  canv.SetGridx(1);
  canv.SetGridy(1);

  // draw a frame to define the range
  TH1F* hr = canv.DrawFrame(outerBand->GetX()[0]-.01, min_, outerBand->GetX()[outerBand->GetN()-1]+.01, max_);
  hr->SetXTitle(xaxis_.c_str());
  hr->GetXaxis()->SetLabelFont(62);
  hr->GetXaxis()->SetLabelSize(0.045);
  hr->GetXaxis()->SetLabelOffset(0.015);
  hr->GetXaxis()->SetTitleFont(62);
  hr->GetXaxis()->SetTitleColor(1);
  hr->GetXaxis()->SetTitleOffset(1.05);
  hr->SetYTitle(yaxis_.c_str());
  hr->GetYaxis()->SetLabelFont(62);
  hr->GetYaxis()->SetTitleSize(0.05);
  hr->GetYaxis()->SetTitleOffset(1.30);
  hr->GetYaxis()->SetLabelSize(0.045);
  if(log_){ canv.SetLogy(1); }

  // create the unit line
  TGraph* unit = new TGraph();
  for(unsigned int imass=0, ipoint=0; imass<bins_.size(); ++imass){
    if(valid_[imass]){
      unit->SetPoint(ipoint, bins_[imass], 1.); ++ipoint;
    }
  }

  outerBand->SetLineColor(kBlack);
  //outerBand->SetLineStyle(11);
  outerBand->SetLineWidth(1.);
  outerBand->SetFillColor(kYellow);
  outerBand->Draw("3");

  innerBand->SetLineColor(kBlack);
  //innerBand->SetLineStyle(11);
  innerBand->SetLineWidth(1.);
  innerBand->SetFillColor(kGreen);
  innerBand->Draw("3same");

  expected->SetLineColor(kRed);
  expected->SetLineWidth(3);
  expected->SetLineStyle(1);
  expected->Draw("L");

  if(!mssm_){
    unit->SetLineColor(kBlue);
    unit->SetLineWidth(3.);
    unit->Draw("Lsame");
  }

  if(observed){
    observed->SetMarkerStyle(20);
    observed->SetMarkerSize(1.0);
    observed->SetMarkerColor(kBlack);
    observed->SetLineWidth(3.);
    observed->Draw("PLsame");
  }
  /// setup the CMS Preliminary
  CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);

  /// add the proper legend
  TLegend* leg = new TLegend(mssm_ ? 0.5625 : 0.18, 0.70, mssm_ ? 1.00 : 0.605, 0.90);
  leg->SetBorderSize( 0 );
  leg->SetFillStyle ( 1001 );
  //leg->SetFillStyle ( 0 );
  leg->SetFillColor (kWhite);
  //leg->SetHeader( "95% CL Limits" );
  if(observed){ leg->AddEntry( observed , "observed",  "PL" );}
  leg->AddEntry( expected , "expected"             ,  "L" );
  leg->AddEntry( innerBand, "#pm 1#sigma expected" ,  "F" );
  leg->AddEntry( outerBand, "#pm 2#sigma expected" ,  "F" );
  leg->Draw("same");
  //canv.RedrawAxis("g");
  canv.RedrawAxis();

  /*
  TPaveText * channel = new TPaveText(0.81, 0.85, 0.90, 0.90, "NDC");
  channel->SetBorderSize(   0 );
  channel->SetFillStyle(    0 );
  channel->SetTextAlign(   12 );
  channel->SetTextSize ( 0.04 );
  channel->SetTextColor(    1 );
  channel->SetTextFont (   62 );
  channel->AddText("H #rightarrow #tau #tau");
  channel->Draw();
  */

  if(png_){
    canv.Print(std::string(output_).append("_").append(outputLabel_).append(".png").c_str());
    canv.Print(std::string(output_).append("_").append(outputLabel_).append(".pdf").c_str());
    canv.Print(std::string(output_).append("_").append(outputLabel_).append(".eps").c_str());
  }
  if(txt_){
    print(std::string(output_).append("_").append(outputLabel_).c_str(), outerBand, innerBand, expected, observed, "txt");
    print(std::string(output_).append("_").append(outputLabel_).c_str(), outerBand, innerBand, expected, observed, "tex");
  }
  if(root_){
    TFile* output = new TFile(std::string("limits_").append(outputLabel_).append(".root").c_str(), "update");
    if(!output->cd(output_.c_str())){
      output->mkdir(output_.c_str());
      output->cd(output_.c_str());
    }
    if(observed){ observed ->Write("observed" );}
    expected ->Write("expected" );
    innerBand->Write("innerBand");
    outerBand->Write("outerBand");
    output->Close();
  }
  return;
}

void 
PlotLimits::plotTanb(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed)
{
  // set up styles
  //SetStyle();

  // setup the CMS colors
  TColor* obs = new TColor(1501, 0.463, 0.867, 0.957);
  TColor* lep = new TColor(1502, 0.494, 0.694, 0.298);

  canv.cd();
  canv.SetGridx(1);
  canv.SetGridy(1);

  // draw a frame to define the range
  TH1F* hr = canv.DrawFrame(outerBand->GetX()[0]-.1, min_, outerBand->GetX()[outerBand->GetN()-1]+.1, max_);
  hr->SetXTitle(xaxis_.c_str());
  hr->GetXaxis()->SetLabelFont(62);
  hr->GetXaxis()->SetTitleFont(62);
  hr->GetXaxis()->SetTitleColor(1);
  hr->GetXaxis()->SetTitleOffset(1.05);
  hr->SetYTitle(yaxis_.c_str());
  hr->GetYaxis()->SetLabelFont(62);
  hr->GetYaxis()->SetTitleSize(0.05);
  hr->GetYaxis()->SetTitleOffset(1.12);
  hr->GetYaxis()->SetLabelSize(0.05);
  if(log_){ canv.SetLogy(1); }

  // create plain background
  TGraph* plain = new TGraph();
  plain->SetPoint(0, 80., 100.);
  for(unsigned int imass=0, ipoint=0; imass<bins_.size(); ++imass){
    if(valid_[imass]){
      plain->SetPoint(ipoint+1, observed->GetX()[ipoint], observed->GetY()[ipoint]); ++ipoint;
    }
  }
  plain->SetPoint(bins_.size()+1, 550, 100.);

  // create LEP exclusion plot
  TGraph* LEP = new TGraph(); 
  limitsLEP(LEP); 
  LEP->SetFillStyle(1001.);
  LEP->SetFillColor(lep->GetNumber());
  LEP->SetLineColor(lep->GetNumber());
  LEP->SetLineStyle(1.);
  LEP->SetLineWidth(4.);
  LEP->Draw("F");

  //
  // --- 80% ggH CL Limits from H->WW moriond12 combination
  //
  /*
  TGraph* HWWmH = new TGraph(); 
  limitsHWW(HWWmH, "mH-calc-observed");
  HWWmH->SetFillStyle( 3010);
  HWWmH->SetFillColor(kBlue);
  HWWmH->SetLineColor(kBlue);
  HWWmH->SetLineStyle(   1.);
  HWWmH->SetLineWidth(   3.);
  //HWW->SetLineWidth( -903);
  HWWmH->Draw("Fsame");
  HWWmH->Draw("Lsame");

  //TGraph* HWWmH_ = new TGraph(); 
  //limitsHWW(HWWmH_, "mH-card-observed");
  //HWWmH_->SetMarkerStyle(20.);
  //HWWmH_->SetMarkerColor(kBlack);
  //HWWmH_->Draw("psame");

  TGraph* HWWmh = new TGraph();
  limitsHWW(HWWmh, "mh-calc-observed");
  HWWmh->SetFillStyle( 3010);
  HWWmh->SetFillColor(kBlue);
  HWWmh->SetLineColor(kBlue);
  HWWmh->SetLineStyle(   1.);
  HWWmh->SetLineWidth(   3.);
  //HWW->SetLineWidth( -903);
  HWWmh->Draw("Fsame");
  HWWmh->Draw("Lsame");

  //TGraph* HWWmh_ = new TGraph(); 
  //limitsHWW(HWWmh_, "mh-card-observed");
  //HWWmh_->SetMarkerStyle(20.);
  //HWWmh_->SetMarkerColor(kBlack);
  //HWWmh_->Draw("psame");
  */

  plain->SetFillStyle(1001.);
  plain->SetFillColor(obs->GetNumber());
  plain->Draw("Fsame");

  if(observed){
    observed->SetMarkerStyle(20);
    observed->SetMarkerSize(1.0);
    observed->SetMarkerColor(kBlack);
    observed->SetLineWidth(3.);
    observed->Draw("Lsame");
  }

  int jpoint=0;
  TGraph* outerHigh = new TGraph();
  TGraph* innerHigh = new TGraph();
  TGraph* outerLow  = new TGraph();
  TGraph* innerLow  = new TGraph();
  TGraph* innerAuxH = new TGraph();
  TGraph* innerAuxL = new TGraph();
  for(unsigned int imass=0, ipoint=0; imass<bins_.size(); ++imass){
    if(valid_[imass]){
      outerHigh->SetPoint(ipoint, outerBand->GetX()[ipoint], outerBand->GetY()[ipoint]+outerBand->GetEYhigh()[ipoint]);
      innerHigh->SetPoint(ipoint, innerBand->GetX()[ipoint], innerBand->GetY()[ipoint]+innerBand->GetEYhigh()[ipoint]); 
      outerLow ->SetPoint(ipoint, outerBand->GetX()[ipoint], outerBand->GetY()[ipoint]-outerBand->GetEYlow ()[ipoint]);
      innerLow ->SetPoint(ipoint, innerBand->GetX()[ipoint], innerBand->GetY()[ipoint]-innerBand->GetEYlow ()[ipoint]); 
      ++ipoint;
      if(innerBand->GetX()[ipoint]>350){
	innerAuxH->SetPoint(jpoint, innerBand->GetX()[ipoint], innerBand->GetY()[ipoint]+innerBand->GetEYhigh()[ipoint]); 
	innerAuxL->SetPoint(jpoint, innerBand->GetX()[ipoint], innerBand->GetY()[ipoint]-innerBand->GetEYlow ()[ipoint]); 
	//std::cout << jpoint << " " << innerBand->GetX()[ipoint] << " " << innerBand->GetY()[ipoint]-innerBand->GetEYlow ()[ipoint] << std::endl;
	++jpoint;
      }
    }
  }
  innerAuxL->SetPoint(jpoint+1, 550, 40.);

  outerHigh->SetLineStyle(11);
  outerHigh->SetLineColor(kGray+1);
  outerHigh->Draw("Lsame");

  innerHigh->SetFillStyle(3005);
  innerHigh->SetFillColor(kGray+1);
  innerHigh->SetLineColor(kGray+1);
  innerHigh->SetLineWidth(-902);
  innerHigh->Draw("Lsame");

  /*
  innerAuxH->SetFillStyle(3005);
  innerAuxH->SetFillColor(kGray+1);
  innerAuxH->SetLineColor(kGray+1);
  innerAuxH->SetLineWidth(-1202);
  innerAuxH->Draw("Lsame");

  innerAuxL->SetFillStyle(3005);
  innerAuxL->SetFillColor(kGray+1);
  innerAuxL->SetLineColor(kGray+1);
  innerAuxL->SetLineWidth( 1202);
  innerAuxL->Draw("Lsame");
  */

  innerLow ->SetFillStyle(3005);
  innerLow ->SetFillColor(kGray+1);
  innerLow ->SetLineColor(kGray+1);
  innerLow ->SetLineWidth( 902);
  innerLow ->Draw("Lsame");

  outerLow ->SetLineStyle(11);
  outerLow ->SetLineColor(kGray+1);
  outerLow ->Draw("Lsame");

  expected->SetLineColor(kGray+2);
  expected->SetLineWidth(3);
  expected->SetLineStyle(1);
  expected->Draw("L");

  /// setup the CMS Preliminary
  CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);

  TPaveText * theory = new TPaveText(0.3, 0.185, 0.9, 0.255, "NDC");
  theory->SetBorderSize(   0 );
  theory->SetFillStyle(    0 );
  theory->SetTextAlign(   12 );
  theory->SetTextSize ( 0.04 );
  theory->SetTextColor(    1 );
  theory->SetTextFont (   62 );
  theory->AddText("MSSM m_{h}^{max} scenario, M_{SUSY} = 1 TeV");
  theory->Draw();
    
  /// add the proper legend
  TLegend* leg = new TLegend(0.18, 0.70, 0.605, 0.90);
  leg->SetBorderSize( 0 );
  leg->SetFillStyle ( 0 );
  leg->SetFillColor (kWhite);
  //leg->SetHeader( "95% CL Limits" );
  if(observed){ leg->AddEntry( observed , "observed" ,  "L" );}
  leg->AddEntry( expected , "expected"               ,  "L" );
  leg->AddEntry( innerHigh, "#pm 1#sigma expected"   ,  "L" );
  leg->AddEntry( outerHigh, "#pm 2#sigma expected"   ,  "L" );
  //leg->AddEntry( HWWmH    , "H#rightarrowWW (80% CL)",  "LF");
  leg->AddEntry( LEP      , "LEP"                    ,  "F" );
  leg->Draw("same");
  //canv.RedrawAxis("g");
  canv.RedrawAxis();

  if(png_){
    canv.Print(std::string(output_).append("_").append(outputLabel_).append(".png").c_str());
    canv.Print(std::string(output_).append("_").append(outputLabel_).append(".pdf").c_str());
    canv.Print(std::string(output_).append("_").append(outputLabel_).append(".eps").c_str());
  }
  if(txt_){
    print(std::string(output_).append("_").append(outputLabel_).c_str(), outerBand, innerBand, expected, observed, "txt");
    print(std::string(output_).append("_").append(outputLabel_).c_str(), outerBand, innerBand, expected, observed, "tex");
  }
  if(root_){
    TFile* output = new TFile(std::string("limits_").append(outputLabel_).append(".root").c_str(), "update");
    if(!output->cd(output_.c_str())){
      output->mkdir(output_.c_str());
      output->cd(output_.c_str());
    }
    if(observed){ observed ->Write("observed" );}
    expected ->Write("expected" );
    innerBand->Write("innerBand");
    outerBand->Write("outerBand");
    output->Close();
  }
  return;
}
