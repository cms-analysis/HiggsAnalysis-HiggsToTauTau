#include <string>
#include <vector>
#include <regex.h>
#include <cstdlib>
#include <iostream>
#include <algorithm>

#include <TKey.h>
#include <TH1F.h>
#include <TFile.h>
#include <TROOT.h>
#include <TString.h>
#include <TLegend.h>
#include <TPaveText.h>
#include <TCollection.h>


/**
   \class   rescalSignal rescaleSignal.C "HiggsAnalysis/HiggsToTauTau/macros/rescaleSignal.C"

   \brief   macro to rescale the individual signal components for histogram based limit inputs to an arbitary value.

   Macro to rescale all signal components in a given input file for limit calculations
   The macro searches the head of the file and the next level of histogram directories 
   from the head of the file on. All directories in the given layer will be searched for 
   histograms. All histograms that fullfill a given PATTERN will be scaled by a factor 
   SCALE. If the process is data_obs the rescaled integral is scaled to correspond to an 
   integer value to fulfill the requirements of the Higgs combination tool combine. All 
   other histograms remain the same. The macro iterates only through one level of folders. 
   These folders are expected to contain only histograms. If armed=false, the rescaled 
   histograms are written to a file with extension '_scaled'.

   Function arguments are:
   
   armed    : update rescaled histograms in file
   scale    : scale tp be applied
   filename : input file that is supposed to host the histograms to be scaled
   pattern  : the pattern that the histograms to be scale should fullfill; in case
              that the pattern is an empty string all patterns that follow the naming 
              conventions used throughout the Higgs2Tau group are searched for.
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

void 
rescaleSignal(bool armed, double scale, const char* filename, const char* pattern="", unsigned int debug=0)
{
  std::vector<TString> paths, dirs;
  TFile* old_file = new TFile(filename, "Read");
  TIter nextDirectory(old_file->GetListOfKeys());
  TKey* idir;
  // collect all folder and histogram names
  while((idir = (TKey*)nextDirectory())){
    old_file->cd();
    if(idir->IsFolder()){
      dirs.push_back(idir->GetName());
      if(debug>1){ std::cout << "found directory: " << idir->GetName() << std::endl; }
      if(old_file->GetDirectory(idir->GetName())){
	old_file->cd(idir->GetName());
	TIter next(gDirectory->GetListOfKeys());
	TKey* iobj;
	while((iobj = (TKey*)next())){
	  if(debug>2){ std::cout << " ...found object: " << iobj->GetName() << std::endl; }
	  TString path = TString::Format("%s/%s", idir->GetName(), iobj->GetName());
	  if(!std::count(paths.begin(), paths.end(), path)){ 
	    paths.push_back(path);
	  }
	}
      }
    }    
  }
  // setup directory structure in new file
  TFile* new_file = new TFile(TString::Format("%s_scaled", filename), "Update");
  for(std::vector<TString>::const_iterator dir = dirs.begin(); dir!=dirs.end(); ++dir){
    if(debug>1){ std::cout << " ...creating directory: " << *dir << std::endl; }
    new_file->mkdir(*dir);
  } 
  // do the rescaling and write new object to file
  for(std::vector<TString>::const_iterator path = paths.begin(); path!=paths.end(); ++path){ 
    if(debug>2){ std::cout << "...getting histogram: " << *path << std::endl; }
    TH1F* h = (TH1F*)old_file->Get(*path);
    std::string histname(*path);
    if(histname.find("/")!=std::string::npos){
      //std::cout << "hist name should be:" << histname.substr(histname.find("/")+1,std::string::npos) << std::endl;
      h->SetName(histname.substr(histname.find("/")+1,std::string::npos).c_str());
    }
    if(match(h->GetName(), (char*)pattern)){
      if(debug>1){ std::cout << "...[" << h->GetName() << "]: " << "old scale : " << h->Integral() << std::endl; }
      h->Scale(scale);  
      if(std::string(*path).find("data_obs")!=std::string::npos){
	if (h->Integral() > 0)  h->Scale((int)h->Integral()/h->Integral());
      }
      if(debug>1){ std::cout << "...[" << h->GetName() << "]: " << "new scale : " << h->Integral() << std::endl; }
    }
    std::string str = std::string(*path);
    std::string dir = str.substr(0, str.find("/"));
    std::string hist = str.substr(str.find("/")+1, std::string::npos);
    new_file->cd();;
    new_file->cd(dir.c_str());
    h->Write(hist.c_str(), TObject::kOverwrite); 
  }
  old_file->Close();
  new_file->Close();
  if(armed){
    system(TString::Format("mv %s_scaled %s", filename, filename));
  }
  return;
}
