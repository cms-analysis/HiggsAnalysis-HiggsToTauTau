#include <stdlib.h>

#include "TString.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/FeynHiggsScan.h"

int main(int argc, char* argv[]) 
{
  // parse arguments
  if( argc < 6 ){
    std::cout << "Usage : " << argv[0] << " [type] [model] [process] [mA] [tanb] [option]       \n "
	      << " [option] : should consist of a key word and a value separated by a '='-sign. \n "
	      << "            keywords can be 'uncertainty' or 'model'. No spaces are allowed   \n "
	      << "            between keyword and value. Possible values for the options are:   \n "
	      << "            - uncertainty=mu- \n "
	      << "            - uncertainty=mu+ \n "
	      << "            - model=mhmax-7TeV\n "
	      << "            - model=mhmax-8TeV\n "
	      << "            - model=nomix-7TeV\n "
	      << "            - model=saeff-7TeV\n "
	      << "            - model=gluph-7TeV\n "
	      << "At the moment uncertainties are not fully supported. A set of examples is     \n "
	      << "given below:                                                                  \n "            
	      << " - " << argv[0] << " xs sm ggH 120 5 uncertainty=mu+    \n "
	      << " - " << argv[0] << " xs sm ggH 120 5 model=saeff-7TeV   \n ";
    return 0;
  }
  std::string model("mhmax-7TeV");
  if( argc > 6 ){
    if( std::string(argv[6]).find("model=")!=std::string::npos ){
      model = std::string(argv[6]).substr(std::string(argv[6]).find("=")+1);
    }
  }
  std::string uncertainty;
  if( argc > 6 ){
    if( std::string(argv[6]).find("uncertainty=")!=std::string::npos ){
      uncertainty+="_"+std::string(argv[6]).substr(std::string(argv[6]).find("=")+1);
    }
  }
  /*
    Implementation
  */
  if(atof(argv[5])<10){
    TString path = TString::Format("%s/src/HiggsAnalysis/HiggsToTauTau/data/feyn-higgs-mssm-scan-%s-fine.root", getenv("CMSSW_BASE"), model.c_str());
    //std::string path(getenv("CMSSW_BASE")+std::string("/src/HiggsAnalysis/HiggsToTauTau/data/feyn-higgs-mssm-scan-mhmax-fine.root"));
    FeynHiggsScan scan(path, TString::Format("mssm_scan%s", uncertainty.c_str()), 90, 1., 10., 96., 50., 1010.);
    std::cout << "tanb   = " << argv[5] << std::endl;
    std::cout << "mA     = " << argv[4] << std::endl;
    std::cout << "mH     = " << scan.mH(atof(argv[4]), atof(argv[5])) << std::endl;
    std::cout << "mh     = " << scan.mh(atof(argv[4]), atof(argv[5])) << std::endl;
    std::cout << "var    = " << argv[1] << "_" << argv[2] << "_" << argv[3] << std::endl;
    std::cout << "value  = " << scan.get(argv[3], argv[2], argv[1], atof(argv[4]), atof(argv[5])) << std::endl;
    return scan.get(argv[3], argv[2], argv[1], atof(argv[4]), atof(argv[5]));
  }
  else{
    TString path = TString::Format("%s/src/HiggsAnalysis/HiggsToTauTau/data/feyn-higgs-mssm-scan-%s.root", getenv("CMSSW_BASE"), model.c_str());
    //std::string path(getenv("CMSSW_BASE")+std::string("/src/HiggsAnalysis/HiggsToTauTau/data/feyn-higgs-mssm-scan-mhmax.root"));
    FeynHiggsScan scan(path, TString::Format("mssm_scan%s", uncertainty.c_str()), 70, 1., 71., 96., 50., 1010.);
    std::cout << "tanb   = " << argv[5] << std::endl;
    std::cout << "mA     = " << argv[4] << std::endl;
    std::cout << "mH     = " << scan.mH(atof(argv[4]), atof(argv[5])) << std::endl;
    std::cout << "mh     = " << scan.mh(atof(argv[4]), atof(argv[5])) << std::endl;
    std::cout << "var    = " << argv[1] << "_" << argv[2] << "_" << argv[3] << std::endl;
    std::cout << "value  = " << scan.get(argv[3], argv[2], argv[1], atof(argv[4]), atof(argv[5])) << std::endl;
    return scan.get(argv[3], argv[2], argv[1], atof(argv[4]), atof(argv[5]));
  }
}
