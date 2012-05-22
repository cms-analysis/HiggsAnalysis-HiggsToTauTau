#include <stdlib.h>

#include "TString.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/CrossSection.h"

int main(int argc, char* argv[]) 
{
  // parse arguments
  if( argc < 3 ){
    std::cout << "Usage : " << argv[0] << " [process] [mH] \n example: " 
	      << argv[0] << " ggH 120" << std::endl;
    return 0;
  }
  /*
    Implementation
  */
  CrossSection scan;
  std::cout << "mH    = " << argv[2] << std::endl;
  std::cout << "proc  = " << argv[1] << std::endl;
  std::cout << "value = " << scan.evaluate(argv[1], atof(argv[2])) << std::endl;
  return scan.evaluate(argv[1], atof(argv[2]));
}
