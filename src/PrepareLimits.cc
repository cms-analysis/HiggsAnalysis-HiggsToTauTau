#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

void
PlotLimits::prepareByFitOutput(const char* directory, std::vector<double>& values, const char* filename, const char* treename, const char* branchname)
{
  for(unsigned int imass=0; imass<bins_.size(); ++imass){
    double value=-1.;
    TString fullpath(TString::Format("%s/%d/%s.root", directory, (int)bins_[imass], filename));
    if(verbosity_>0) std::cout << "INFO: opening file " << fullpath << std::endl;
    TFile* file = new TFile(fullpath);
    if(file->IsZombie()){
      if(verbosity_>0){ std::cout << "INFO: file not found: " << fullpath  << std::endl; }
      valid_[imass]=false;
    }
    else{
      TTree* limit = (TTree*) file->Get(treename);
      if(!limit){
	if(verbosity_>0){ std::cout << "INFO: tree 'limit' not found: limit" << std::endl; }
	valid_[imass]=false;
      }
      else{
	double x;
	limit->SetBranchAddress(branchname, &x);
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
PlotLimits::prepareByFile(const char* directory, std::vector<double>& values, const char* filename, const char* low_tanb /*=""*/)
{
  for(unsigned int imass=0; imass<bins_.size(); ++imass){
    double value=-1.;
    std::string buffer = std::string(filename);
    std::string filehead = buffer.substr(0, buffer.find("$MASS"));
    std::string filetail = buffer.substr(buffer.find("$MASS")+5, std::string::npos);
    TString fullpath(TString::Format("%s/%d/%s%d%s.root", directory, (int)bins_[imass], filehead.c_str(), (int)bins_[imass], filetail.c_str()));
    if(verbosity_>0) std::cout << "INFO: opening file " << fullpath << std::endl;
    TFile* file = new TFile(fullpath);
    if(file->IsZombie()){
      if(verbosity_>0){ std::cout << "INFO: file not found: " << fullpath  << std::endl; }
      valid_[imass]=false;
    }
    else{
      if(std::string(low_tanb)==std::string("low")){
	TTree* limit = (TTree*) file->Get("limit");
	if(!limit){
	  if(verbosity_>0){ std::cout << "INFO: tree 'limit' not found: limit" << std::endl; }
	  valid_[imass]=false;
	}
	else{
	  double x;
	  limit->SetBranchAddress("lowlimit", &x);
	  int nevent = limit->GetEntries();
	  for(int i=0; i<nevent; ++i){
	    limit->GetEvent(i);
	    value = x;
	  }
	}
	file->Close();
      }   
      else{
	TTree* limit = (TTree*) file->Get("limit");
	if(!limit){
	  if(verbosity_>0){ std::cout << "INFO: tree 'limit' not found: limit" << std::endl; }
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
    }
    values.push_back(value); 
  }
  return;
}

void
PlotLimits::prepareByToy(const char* directory, std::vector<double>& values, const char* type)
{
  for(unsigned int imass=0; imass<bins_.size(); ++imass){
    // buffer mass
    float mass = bins_[imass];

    double value=-1.;
    TString fullpath(TString::Format("%s/%d/batch_collected_%s.root", directory, (int)mass, label_.c_str()));
    if(verbosity_>0) std::cout << "INFO: opening file " << fullpath << std::endl;
    TFile* file = new TFile(fullpath);
    if(file->IsZombie()){
      if(verbosity_>0){ std::cout << "INFO: file not found: " << fullpath  << std::endl; }
      valid_[imass]=false;
    }
    else{
      TTree* limit = (TTree*) file->Get("limit");
      if(!limit){
	if(verbosity_>0){ std::cout << "INFO: tree not found: limit" << std::endl; }
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
	  // fill for median determination
	  limits.push_back(x);
	  // mean(x)
	  mean +=1./(i+1)*(x-mean);
	  // mean(x**2)
	  var  +=1./(i+1)*(x*x-var);
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
	// we therefore use quantiles here for +/-1 and +/-2 sigma. The
	// mean remains as is.
	if(std::string(type)==std::string("MEAN")){ value= mean; }
	else if(std::string(type)==std::string("+2SIGMA")){ value= limits[(int)(0.975*limits.size())];}//+2*sqrt(var);}
	else if(std::string(type)==std::string("+1SIGMA")){ value= limits[(int)(0.840*limits.size())];}//+1*sqrt(var);}
	else if(std::string(type)==std::string( "MEDIAN")){ value= limits[(int)(0.500*limits.size())];}
	else if(std::string(type)==std::string("-1SIGMA")){ value= limits[(int)(0.160*limits.size())];}//-1*sqrt(var);}
	else if(std::string(type)==std::string("-2SIGMA")){ value= limits[(int)(0.027*limits.size())];}//-2*sqrt(var);}
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
PlotLimits::prepareByValue(const char* directory, std::vector<double>& values, const char* filename, float ConLevel)
{
  for(unsigned int imass=0; imass<bins_.size(); ++imass){
    // buffer mass
    float mass = bins_[imass];
    double value=-1.;
    std::string buffer = std::string(filename);
    std::string filehead = buffer.substr(0, buffer.find("$MASS"));
    std::string filetail = buffer.substr(buffer.find("$MASS")+5, std::string::npos);
    TString fullpath(TString::Format("%s/%d/%s%d%s.root", directory, (int)mass, filehead.c_str(), (int)mass, filetail.c_str()));
    if(verbosity_>0) std::cout << "INFO: opening file " << fullpath << std::endl;
    TFile* file = new TFile(fullpath);
    if(file->IsZombie()){
      if(verbosity_>0){ std::cout << "INFO: file not found: " << fullpath  << std::endl; }
      valid_[imass]=false;
    }
    else{
      TTree* limit = (TTree*) file->Get("limit");
      if(!limit){
	if(verbosity_>0){ std::cout << "INFO: tree not found: limit" << std::endl; }
	valid_[imass]=false;
      }
      else{
	double x; float y;
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
