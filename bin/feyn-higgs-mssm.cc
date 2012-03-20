#include <stdlib.h>

#include "TString.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/FeynHiggsScan.h"

int main(int argc, char* argv[]) 
{
  // parse arguments
  if( argc < 6 ){
    std::cout << "Usage : " << argv[0] << " [type] [model] [process] [mA] [tanb] [uncertainty]\n example: " 
	      << argv[0] << " xs sm ggH 120 5 [mu+]" << std::endl;
    return 0;
  }
  std::string uncertainty;
  if( argc > 6 ){
    uncertainty+="_"+std::string(argv[6]);
  }

  /*
    Implementation
  */
  std::string path(getenv("CMSSW_BASE")+std::string("/src/HiggsAnalysis/HiggsToTauTau/data/feyn-higgs-mssm-scan.root"));
  FeynHiggsScan scan(path.c_str(), TString::Format("mssm_scan%s", uncertainty.c_str()), 70, 1., 71., 96., 50., 1010.);
  std::cout << "mA     = " << argv[4] << std::endl;
  std::cout << "tanb   = " << argv[5] << std::endl;
  std::cout << "var    = " << argv[1] << "_" << argv[2] << "_" << argv[3] << std::endl;
  std::cout << "value  = " << scan.get(argv[3], argv[2], argv[1], atof(argv[4]), atof(argv[5])) << std::endl;
  return scan.get(argv[3], argv[2], argv[1], atof(argv[4]), atof(argv[5]));
}
