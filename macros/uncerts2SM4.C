#include <string>
#include <vector>
#include <iomanip>
#include <iostream>

#include <regex.h>
#include <sys/types.h>

#include <TKey.h>
#include <TH1F.h>
#include <TFile.h>
#include <TROOT.h>
#include <TSystem.h>
#include <TString.h>
#include <TLegend.h>
#include <TPaveText.h>
#include <TCollection.h>

#include "HiggsAnalysis/HiggsToTauTau/interface/HiggsCSandWidth.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HiggsCSandWidthSM4.h"

/**
   \class   uncerts2SM4 uncerts2SM4.C "HiggsAnalysis/HiggsToTauTau/macros/uncerts2SM4.C"

   \brief   macro to determine the uncertainties of SM4 BR's as function of mH

   Macro to determine the uncertainties of SM4 BR's as function of mH exploiting the 
   official tools provided by Matt Snowball.
   
   mass     : single mass, for which the uncertainty should be determined.
*/

void uncerts2SM4(double mass)
{
  HiggsCSandWidthSM4 sm4;
  std::cout << " mass           " << mass << std::endl 
	    << " gamma_Hff      " << ((110<=mass && mass<146) ? sm4.HiggsBRErr_Hff    (2, mass, 7) : -1) << std::endl
	    << " gamma_HVV      " << ((110<=mass && mass<146) ? sm4.HiggsBRErr_HVV    (2, mass, 7) : -1) << std::endl
	    << " gamma_Hgluglu  " << ((110<=mass && mass<146) ? sm4.HiggsBRErr_Hgluglu(2, mass, 7) : -1) << std::endl
	    << std::endl;
  return;
}

