#include <cstdlib>
#include "HiggsAnalysis/HiggsToTauTau/interface/CrossSection.h"

float 
CrossSection::evaluate(const char* process, float mass)
{
  float xsec=0.;
  xsec_.clear();
  std::string proc(process);
  if(proc == std::string("ggH")){ ggH(); }
  else if(proc == std::string("qqH")){ qqH(); }
  else if(proc == std::string("WH" )){ WH (); }
  else if(proc == std::string("ZH" )){ ZH (); }
  else if(proc == std::string("ttH")){ ttH(); }
  else if(proc == std::string("BR" )){ BR (); }
  else { 
    std::cerr 
      << "This proc is not implemented or does not exist: " << proc << std::endl
      << "Available proc's are: ggH, qqH, WH, ZH, ttH, BR " << std::endl;
    exit(0);
  }

  if(!(mass<xsec_.begin()->first || xsec_.rbegin()->first<mass)){
    float lowerBound = xsec_.lower_bound(mass)->first<mass ? xsec_.lower_bound(mass)->first : mass;
    float upperBound = xsec_.upper_bound(mass)->first;

    if(lowerBound == mass){
      xsec = xsec_.lower_bound(mass)->second;
    }
    else if(upperBound == mass){
      xsec = xsec_.upper_bound(mass)->second;
    }
    else{
      // apply simple linear extrapolation
      xsec = xsec_.lower_bound(mass)->second + (xsec_.upper_bound(mass)->second - xsec_.lower_bound(mass)->second)*(mass - lowerBound)/(upperBound - lowerBound);
    }
  }
  return xsec;
}
