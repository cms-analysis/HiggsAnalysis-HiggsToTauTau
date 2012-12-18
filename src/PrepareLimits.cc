#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

void
PlotLimits::prepareSimple(const char* directory, std::vector<double>& values, const char* filename)
{
  for(unsigned int imass=0; imass<bins_.size(); ++imass){
    // buffer mass
    float mass = bins_[imass];

    double value=-1.;
    std::string buffer = std::string(filename);
    std::string filehead = buffer.substr(0, buffer.find("$MASS"));
    std::string filetail = buffer.substr(buffer.find("$MASS")+5, std::string::npos);
    TString fullpath(TString::Format("%s/%d/%smH%d%s.root", directory, (int)mass, filehead.c_str(), (int)mass, filetail.c_str()));
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
	  std::cout << "INFO: tree 'limit' not found in file: "
                    << filename << std::endl
		    << "      leave value at -1. to invalidate" << std::endl;
	}
	valid_[imass]=false;
      }
      else{
	if(buffer.find("MaxLikelihoodFit")!=std::string::npos){
	  double x; float y;
	  limit->SetBranchAddress("limit", &x);
	  limit->SetBranchAddress("quantileExpected", &y);
	  int nevent = limit->GetEntries();
	  for(int i=0; i<nevent; ++i){
	    limit->GetEvent(i);
	    if(y==0.5){ value = x; }
	  }
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
    // buffer mass
    float mass = bins_[imass];

    double value=-1.;
    TString fullpath;
    if(std::string(type)==std::string("observed")){
      fullpath = TString::Format("%s/%d/higgsCombine-obs.Asymptotic.mH%d.root", directory, (int)mass, (int)mass);
    }
    else{
      fullpath = TString::Format("%s/%d/higgsCombine-exp.Asymptotic.mH%d.root", directory, (int)mass, (int)mass);
    }
    if(verbosity_>0){
      std::cout << "INFO: type is " << type << std::endl;
      std::cout << "INFO: opening file " << fullpath << std::endl;
    }
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
    // buffer mass
    float mass = bins_[imass];

    double value=-1.;
    TString fullpath(TString::Format("%s/%d/batch_collected.root", directory, (int)mass));
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
	  if(0<x && x<999999){
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
	// we therefore use quantiles here for +/-1 and +/-2 sigma also for
	// bayesian; the mean remains as it is
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

void
PlotLimits::prepareMaxLikelihood(const char* directory, std::vector<double>& values, const char* filename, float ConLevel)
{
  for(unsigned int imass=0; imass<bins_.size(); ++imass){
    // buffer mass
    float mass = bins_[imass];

    double value=-1.;
    std::string buffer = std::string(filename);
    std::string filehead = buffer.substr(0, buffer.find("$MASS"));
    std::string filetail = buffer.substr(buffer.find("$MASS")+5, std::string::npos);
    TString fullpath(TString::Format("%s/%d/%smH%d%s.root", directory, (int)mass, filehead.c_str(), (int)mass, filetail.c_str()));
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
	float y;
	limit->SetBranchAddress("limit", &x);
	limit->SetBranchAddress("quantileExpected", &y);
	int nevent = limit->GetEntries();
	for(int i=0; i<nevent; ++i){
	  limit->GetEvent(i);
	  if(y==ConLevel){
	    value = x;
	  }
	}
      }
      file->Close();
    }
    values.push_back(value);
  }
  return;
}


