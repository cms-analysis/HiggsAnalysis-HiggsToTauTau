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
  else if(!background(proc)){
    std::cerr 
      << "This proc is not implemented or does not exist: " << proc << std::endl
      << "Available proc's are: ggH, qqH, WH, ZH, ttH, BR " << std::endl;
    exit(0);
  }
  if(background(proc)){
    // for backround processes return the scale to 
    // different ecms. Therefore xsec should be 1.
    xsec = 1.;
  }
  else{
    xsec = linear(mass, xsec_);
  }
  if(proc != std::string("BR")){
    // do not apply any scaling to BR's
    if(ecms_!=7){
      scale_.clear(); seven2xxxTeV();
      if(background(proc)){
	xsec*= scaleBG_[proc];
      }
      else{
	xsec*= linear(mass, scale_);
      }
    }
  }
  return xsec;
}

float
CrossSection::linear(float mass, std::map<float, float>& map){
  float value = 0;
  if(!(mass<map.begin()->first || map.rbegin()->first<mass)){
    float lowerBound = map.lower_bound(mass)->first == mass ? mass : (--map.lower_bound(mass))->first;
    float upperBound = map.upper_bound(mass)->first;
    //std::cout << "mass : " << mass << " - lowerBound : " << lowerBound << " - upperBound : " << upperBound << std::endl;

    if(lowerBound == mass){
      //std::cout << "mass matches lower bound:" << mass << std::endl;
      value = map.lower_bound(mass)->second;
    }
    else if(upperBound == mass){
      //std::cout << "mass matches upper bound:" << mass << std::endl;
      value = map.upper_bound(mass)->second;
    }
    else{
      // apply simple linear extrapolation
      float upperValue = map.upper_bound(mass)->second;
      float lowerValue = (--map.lower_bound(mass))->second;
      //std::cout << "interpolate: " << lowerValue << "+" 
      //	<< (upperValue - lowerValue)*(mass - lowerBound)/(upperBound - lowerBound)
      //	<< std::endl;
      value = lowerValue + (upperValue - lowerValue)*(mass - lowerBound)/(upperBound - lowerBound);
    }
  }
  return value;
}
