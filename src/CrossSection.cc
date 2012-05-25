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
  xsec = linear(mass, xsec_);
  if(ecms_==8){
    scale_.clear(); seven2EightTeV();
    xsec*= linear(mass, scale_);
  }
  return xsec;
}

float
CrossSection::linear(float mass, std::map<float, float>& map){
  float value = 0;
  if(!(mass<map.begin()->first || map.rbegin()->first<mass)){
    float lowerBound = map.lower_bound(mass)->first<mass ? map.lower_bound(mass)->first : mass;
    float upperBound = map.upper_bound(mass)->first;
    
    if(lowerBound == mass){
      value = map.lower_bound(mass)->second;
    }
    else if(upperBound == mass){
      value = map.upper_bound(mass)->second;
    }
    else{
      // apply simple linear extrapolation
      value = map.lower_bound(mass)->second + (map.upper_bound(mass)->second - map.lower_bound(mass)->second)*(mass - lowerBound)/(upperBound - lowerBound);
    }
  }
  return value;
}
