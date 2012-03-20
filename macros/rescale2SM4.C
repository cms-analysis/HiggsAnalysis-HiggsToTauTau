#include <string>
#include <vector>
#include <iostream>

#include <regex.h>
#include <sys/types.h>

#include <TKey.h>
#include <TH1F.h>
#include <TFile.h>
#include <TROOT.h>
#include <TString.h>
#include <TLegend.h>
#include <TPaveText.h>
#include <TCollection.h>

#include "HiggsCSandWidth.h"
#include "HiggsCSandWidthSM4.h"

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
      std::cout << "file  = " << filename << std::endl;
      std::cout << "mass  = " << mdx      << std::endl;
      std::cout << "armed = " << armed    << std::endl;
    }
    TFile* file = new TFile(filename, "update");
    TIter nextDirectory(file->GetListOfKeys());
    TKey* idir;
    while((idir = (TKey*)nextDirectory())){
      if( idir->IsFolder() ){
	file->cd(); // make sure to start in directory head 
	if( debug>0 ){ std::cout << "Found directory: " << idir->GetName() << std::endl; }
	if( std::string(idir->GetName())=="emu_b"   || 
	    std::string(idir->GetName())=="emu_nob" || 
	    std::string(idir->GetName())=="emu_X" ){ 
	  std::cout << "skip non SM directory..." << std::endl; 
	  continue;
	}
	if( file->GetDirectory(idir->GetName()) ){
	  file->cd(idir->GetName()); // change to sub-directory
	  TIter next(gDirectory->GetListOfKeys());
	  TKey* iobj;
	  while((iobj = (TKey*)next())){
	    if(debug>1){ std::cout << " ...found object: " << iobj->GetName() << std::endl; }
	    // why does \\w*_\\d+ not work to catch them all?!?
	    if( match(iobj->GetName(), "Higgs") || 
		match(iobj->GetName(), "GGH"  ) || 
		match(iobj->GetName(), "BBH"  ) || 
		match(iobj->GetName(), "VBF"  ) || 
		match(iobj->GetName(), "VH"   ) || 
		match(iobj->GetName(), "SM"   ) ){
	      TH1F* h = (TH1F*)file->Get(TString::Format("%s/%s", idir->GetName(), iobj->GetName()));
	      if( debug>1 ){ std::cout << "...old scale : " << h->Integral() << std::endl; }
	      
	      HiggsCSandWidth smx; HiggsCSandWidthSM4 sm4; int type = 0;
	      if( match(iobj->GetName(), (char*)std::string(TString::Format("gf_sm_%3.0d" , mdx)).c_str() ) ){ type = 1; }
	      if( match(iobj->GetName(), (char*)std::string(TString::Format("vbf_sm_%3.0d", mdx)).c_str() ) ){ type = 2; }
	      if( match(iobj->GetName(), (char*)std::string(TString::Format("SM%3.0d"     , mdx)).c_str() ) ){ type = 1; }
	      if( match(iobj->GetName(), (char*)std::string(TString::Format("VBF%3.0d"    , mdx)).c_str() ) ){ type = 2; }
	      if( match(iobj->GetName(), (char*)std::string(TString::Format("VH%3.0d"     , mdx)).c_str() ) ){ type = 3; }
	      if( type==0 ) { /*std::cout << "not supported process" << std::endl;*/ continue; }
	      float smxBR = smx.HiggsWidth(2, mdx)/smx.HiggsWidth(0, mdx); 
	      float sm4BR = sm4.HiggsWidth(2, mdx)/sm4.HiggsWidth(0, mdx);
	      if( debug>0 ){
		std::cout << "  --  hist  = " << iobj->GetName() 
			  << "  --  type  = " << type 
			  << "  --  SM    = " << (type==1 ? smx.HiggsCS(type, mdx, 7)*smxBR : smxBR) 
			  << "  --  SM4   = " << (type==1 ? sm4.HiggsCS(type, mdx, 7)*sm4BR : sm4BR)
			  << "  --  scale = " << (type==1 ? sm4.HiggsCS(type, mdx, 7)*sm4BR/(smx.HiggsCS(type, mdx, 7)*smxBR) : sm4BR/smxBR)
			  << std::endl;
	      }
	      if( type==1 ){ h->Scale(sm4.HiggsCS(type, mdx, 7)*sm4BR/(smx.HiggsCS(type, mdx, 7)*smxBR)); }
	      if( type==2 ){ h->Scale(sm4BR/smxBR); }
	      if( type==3 ){ h->Scale(sm4BR/smxBR); }
	      
	      if( debug>1 ){ std::cout << "...new scale : " << h->Integral() << std::endl; }
	      if( armed ){ h->Write(); }
	    }
	  }
	}
      }
    }
    file->Close();
  }
  return;
}
