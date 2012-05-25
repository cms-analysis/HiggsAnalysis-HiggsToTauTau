#include <stdlib.h>

#include "TString.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/CrossSection.h"

int main(int argc, char* argv[]) 
{
  // parse arguments
  if( argc < 3 ){
    std::cout << "Usage : " << argv[0] << " [process] [mH] [Ecms]\n example: " 
	      << argv[0] << " ggH 120 [7]" << std::endl;
    return 0;
  }
  float ecms = 7; /// ecms in TeV
  if( argc == 4){
    ecms = atof(argv[3]);
  }
  /*
    Implementation
  */
  CrossSection scan(ecms);
  std::cout << "mH    = " << argv[2] << std::endl;
  std::cout << "proc  = " << argv[1] << std::endl;
  std::cout << "value = " << scan.evaluate(argv[1], atof(argv[2])) << std::endl;
  return scan.evaluate(argv[1], atof(argv[2]));
}
