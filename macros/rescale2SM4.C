#include <map>
#include <string>
#include <vector>
#include <iomanip>
#include <iostream>

#include <regex.h>
#include <sys/types.h>

#include <TH1.h>
#include <TH1F.h>
#include <TKey.h>
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

std::map<const char*, const char*>
httDictionary()
{
  std::map<const char*, const char*> dict_;
  // signal names
  dict_["ggH" ] = "ggH";
  dict_["qqH" ] = "qqH";
  dict_["VH"  ] = "VH";
  return dict_;
}

std::vector<std::string>
signalList(const char* dirName="", const char* pattern="", unsigned int debug=0)
{
  std::vector<std::string> histnames;
  TIter next(gDirectory->GetListOfKeys());
  TKey* iobj;
  unsigned int idx=0;
  while((iobj = (TKey*)next())){
    if(iobj->IsFolder()) continue;
    if(debug>2){ std::cout << "[" << ++idx << "] ...Found object: " << iobj->GetName() << " of type: " << iobj->GetClassName() << std::endl; }
    std::string fullpath(dirName); 
    fullpath += fullpath == std::string("") ? "" : "/"; fullpath += iobj->GetName();
    // why does \\w*_\\d+ not work to catch them all?!?
    if(std::string(pattern).empty()){
      std::map<const char*, const char*> dict = httDictionary();
      for(std::map<const char*, const char*>::const_iterator name = dict.begin(); name!=dict.end(); ++name){
	if(match(iobj->GetName(), (char*)name->first)){
	  histnames.push_back(fullpath);
	}
      }
    }
    else if(!std::string(pattern).empty() && match(iobj->GetName(), (char*)pattern)){
      histnames.push_back(fullpath);
    }
  }
  return histnames;
}

void rescale2SM4(bool armed, const char* filename, double mass=-1)
{
  unsigned int debug = 1;
  std::vector<std::string> histnames; histnames.clear();
  if( debug>0 ){
    std::cout << "file  = " << filename << std::setw(10);
    std::cout << "mass  = " << mass     << std::setw(10);
    std::cout << "armed = " << armed    << std::endl;
  }
  TFile* file = new TFile(filename, "update");
  TIter nextDirectory(file->GetListOfKeys());
  std::vector<std::string> buffer; TKey* idir;
  while((idir = (TKey*)nextDirectory())){
    buffer.clear();
    if( idir->IsFolder() ){
      file->cd(); // make sure to start in directory head 
      if( debug>1 ){ std::cout << "Found directory: " << idir->GetName() << std::endl; }
      if( file->GetDirectory(idir->GetName()) ){
	file->cd(idir->GetName()); // change to sub-directory
	buffer = signalList(idir->GetName(), "", debug);
      }
      // append to the vector of histograms to be rescaled
      for(std::vector<std::string>::const_iterator elem=buffer.begin(); elem!=buffer.end(); ++elem){
	histnames.push_back(*elem);
      }
      if(debug>1){
	std::cout << "added " << buffer.size() << " elements to histnames [" << histnames.size() << "] for directory " << idir->GetName() << std::endl;
      }
    }
  }
  // pick up histograms which are not kept in an extra folder
  file->cd(); buffer.clear();
  buffer = signalList("", "", debug);
  // append to the vector of histograms to be rescaled
  for(std::vector<std::string>::const_iterator elem=buffer.begin(); elem!=buffer.end(); ++elem){
    histnames.push_back(*elem);
  }
  if(debug>1){
    std::cout << "added " << buffer.size() << " elements to histnames [" << histnames.size() << "] for file head" << std::endl;
  }

  HiggsCSandWidth smx; HiggsCSandWidthSM4 sm4;
  for(std::vector<std::string>::const_iterator hist=histnames.begin(); hist!=histnames.end(); ++hist){
    int type = 0;
    // determine mass from hostogram name
    std::string strippedName = (hist->find("/")!=std::string::npos ? hist->substr(hist->find("/")+1) : *hist);
    std::string massName;
    if(strippedName.find("ggH")!=std::string::npos) {
      massName = strippedName.substr(3, 3); type = 1;
    }
    if(strippedName.find("qqH")!=std::string::npos) {
      massName = strippedName.substr(3, 3); type = 2;
    }
    if(strippedName.find("VH" )!=std::string::npos) {
      massName = strippedName.substr(2, 3); type = 3;
    }
    if( type==0 ) { 
      std::cout << "not supported process" << std::endl; 
      continue; 
    }
    else {

      file->cd();
      float mdx = atof(massName.c_str());
      TH1F* h = (TH1F*)file->Get(hist->c_str());
      float smxXS = type==1 ? smx.HiggsCS(type, mdx, 7, true) : 0.; float smxBR = smx.HiggsBR(2, mdx, true); 
      float sm4XS = type==1 ? sm4.HiggsCS(type, mdx, 7, true) : 0.; float sm4BR = sm4.HiggsBR(2, mdx, true);
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
      //scaling old style
      //if( type==2 ){ h->Scale(sm4BR/smxBR); }
      //if( type==3 ){ h->Scale(sm4BR/smxBR); }
      // scaling new style
      if( type==2 ){ h->Scale(0.); }
      if( type==3 ){ h->Scale(0.); }
      if(armed){
	if(hist->find("/")!=std::string::npos){
	  file->cd(hist->substr(0, hist->find("/")).c_str());
	}
	else{
	  file->cd();
	}
	h->Write(strippedName.c_str(), TObject::kOverwrite); 
      }
    }
  }
  file->Close();
  return;
}

