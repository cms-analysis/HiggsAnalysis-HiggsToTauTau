#include <stdlib.h>

#include "TString.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/FeynHiggsScan.h"

int main(int argc, char* argv[]) 
{
  // parse arguments
  if( argc < 3 ){
    std::cout << "Usage : " << argv[0] << " [type] [process] [mH] [uncertainty]\n example: " 
	      << argv[0] << " xs ggA 120 [mu+]" << std::endl;
    return 0;
  }
  std::string uncertainty;
  if( argc > 4 ){
    uncertainty+="_"+std::string(argv[4]);
  }
  /*
    Implementation
  */
  std::string path(getenv("CMSSW_BASE")+std::string("/src/HiggsAnalysis/HiggsToTauTau/data/feyn-higgs-sm-scan.root"));
  FeynHiggsScan scan(path.c_str(), TString::Format("mssm_scan%s", uncertainty.c_str()), 1, 1., 2., 951, 50, 1000.);
  std::cout << "mA     = " << argv[3] << std::endl;
  std::cout << "var    = " << argv[1] << "_sm_" << argv[2] << std::endl;
  std::cout << "value  = " << scan.get(argv[2], "sm", argv[1], atof(argv[3]), 1.) << std::endl;
  return scan.get(argv[2], "sm", argv[1], atof(argv[3]), 1.);
}
