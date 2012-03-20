#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/PythonParameterSet/interface/MakeParameterSets.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HorizontalMorphing.h"


int main(int argc, char* argv[]) 
{
  // parse arguments
  if ( argc < 2 ) {
    std::cout << "Usage : " << argv[0] << " [parameters.py]" << std::endl;
    return 0;
  }
  
  if( !edm::readPSetsFrom(argv[1])->existsAs<edm::ParameterSet>("horizontalMorphing") ){
    std::cout << " ERROR: ParametersSet 'process' is missing in your configuration file" << std::endl; exit(0);
  }
  
  HorizontalMorphing morphing(edm::readPSetsFrom(argv[1])->getParameter<edm::ParameterSet>("horizontalMorphing"));
  morphing.process();
  return 0;
}
