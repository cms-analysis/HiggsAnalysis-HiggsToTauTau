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
   \class   rescale2SM4 rescale2SM4.C "HiggsAnalysis/HiggsToTauTau/macros/rescale2SM4.C"

   \brief   macro to rescale histogram based limit inputs from SM to four fermion model

   Macro to rescale all signal components in a given input file for limit calculations 
   from SM to SM4 exploiting the official tools provided by Matt Snowball. All 
   directories in the given file will be searched for histograms. All histograms that 
   start with 'Higgs', 'GGH', 'BBH', 'SM', 'VH', 'VBF' will be scaled from SM for SM4. 
   All other histograms remain unscaled. The macro iterates only through one level of 
   folders. These folders are expected to contain all histograms. Function arguments 
   are: 
   
   armed    : update rescaled hyistograms in file
   filename : input file that is supposed to hold the histograms to be scaled
   mass     : single mass, for which the rescaling is supposed to be done. When left 
              to be -1 all masses between 110 and 145 are rescaled in one go. 
*/

int
match(const char *string, char *pattern)
{
  int status;
  regex_t re;
  if(regcomp(&re, pattern, REG_EXTENDED|REG_NOSUB) != 0) {
    return 0;      /* report error */
  }
  status = regexec(&re, string, 0, NULL, 0);
  regfree(&re);
  if (status != 0) {
    return 0 ;      /* report error */
  }
  return 1 ;
}

void rescale2SM4(bool armed, const char* filename, double mass=-1)
{
  unsigned int debug = 1;
  for(unsigned int mdx=110; mdx<146; ++mdx){
    if( mass>0 && mdx!=mass ){ continue; }
    if( debug>0 ){
      std::cout << "file  = " << filename << std::setw(10);
      std::cout << "mass  = " << mdx      << std::setw(10);
      std::cout << "armed = " << armed    << std::endl;
    }
    TFile* file = new TFile(filename, "update");
    TIter nextDirectory(file->GetListOfKeys());
    TKey* idir;
    while((idir = (TKey*)nextDirectory())){
      if( idir->IsFolder() ){
	file->cd(); // make sure to start in directory head 
	if( debug>1 ){ std::cout << "Found directory: " << idir->GetName() << std::endl; }
	if( std::string(idir->GetName())=="emu_b"   || 
	    std::string(idir->GetName())=="emu_nob" || 
	    std::string(idir->GetName())=="emu_X" ){
	  if( debug>1 ){ std::cout << "skip non SM directory..." << std::endl; }
	  continue;
	}
	if( file->GetDirectory(idir->GetName()) ){
	  file->cd(idir->GetName()); // change to sub-directory
	  TIter next(gDirectory->GetListOfKeys());
	  TKey* iobj;
	  while((iobj = (TKey*)next())){
	    if(debug>2){ std::cout << " ...found object: " << iobj->GetName() << std::endl; }
	    // why does \\w*_\\d+ not work to catch them all?!?
	    if( match(iobj->GetName(), "ggH"  ) || 
		match(iobj->GetName(), "qqH"  ) || 
		match(iobj->GetName(), "VH"   ) ){
	      TH1F* h = (TH1F*)file->Get(TString::Format("%s/%s", idir->GetName(), iobj->GetName()));
	      if( debug>2 ){ std::cout << "...old scale : " << h->Integral() << std::endl; }
	      HiggsCSandWidth smx; HiggsCSandWidthSM4 sm4; int type = 0;
	      if( match(iobj->GetName(), (char*)std::string(TString::Format("ggH%3.0d"    , mdx)).c_str() ) ){ type = 1; }
	      if( match(iobj->GetName(), (char*)std::string(TString::Format("qqH%3.0d"    , mdx)).c_str() ) ){ type = 2; }
	      if( match(iobj->GetName(), (char*)std::string(TString::Format("VH%3.0d"     , mdx)).c_str() ) ){ type = 3; }
	      if( type==0 ) { /*std::cout << "not supported process" << std::endl;*/ continue; }
	      float smxXS = type==1 ? smx.HiggsCS(type, mdx, 7, true) : 0.; float smxBR = type==1 ? smx.HiggsBR(2, mdx, true) : 0.; 
	      float sm4XS = type==1 ? sm4.HiggsCS(type, mdx, 7, true) : 0.; float sm4BR = type==1 ? sm4.HiggsBR(2, mdx, true) : 0.;
	      if( debug>1 ){
		std::cout << "  --  hist  = " << std::setw(10) << h->GetName() << std::endl
			  << "  --  type  = " << std::setw(10) << type << std::endl
			  << "  --  mass  = " << std::setw(10) << mdx << std::endl
			  << "  --  SM    = " << std::setw(10) << smxXS*smxBR << " (BR = " << smxBR << ")"  << std::endl
			  << "  --  SM4   = " << std::setw(10) << sm4XS*sm4BR << " (BR = " << sm4BR << ")"  << std::endl
			  << "  --  scale = " << std::setw(10) << (type==1 ? sm4XS*sm4BR/(smxXS*smxBR) : 0) << std::endl
			  << std::endl;
	      }
	      if( type==1 ){ h->Scale(sm4XS*sm4BR/(smxXS*smxBR)); }
	      if( type==2 ){ h->Scale(0.); }
	      if( type==3 ){ h->Scale(0.); }
	      
	      if( debug>2 ){ std::cout << "...new scale : " << h->Integral() << std::endl; }
	      if( armed ){ h->Write(iobj->GetName()); }
	    }
	  }
	}
      }
    }
    file->Close();
  }
  return;
}
