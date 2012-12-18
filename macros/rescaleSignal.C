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


/**
   \class   rescalSignal rescaleSignal.C "HiggsAnalysis/HiggsToTauTau/macros/rescaleSignal.C"

   \brief   macro to rescale the signal component(s) for histogram based limit inputs for limi calculation to an arbitary value.

   Macro to rescale all signal components in a given input file for limit calculations
   The macro searches the head of the file and the next level of histogram directories 
   from the head of the file on. All directories in the given layer will be searched for 
   histograms. All histograms that fullfill a given PATTERN will be scaled by a factor 
   SCALE. If the PATTERN is empty all histograms that start with 'Higgs', 'GGH', 'BBH', 
   'SM', 'VH', 'VBF' will be scaled, according to the histogram conventions used within 
   the Higgs2Tau group. All other histograms remain the same. The macro iterates only 
   through one level of folders. These folders are expected to contain only histograms. 
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

bool
httSignal(const char* histName)
{
  return (match(histName, "Higgs") || 
	  match(histName, "GGH"  ) || 
	  match(histName, "BBH"  ) || 
	  match(histName, "VBF"  ) || 
	  match(histName, "ggH"  ) || 
	  match(histName, "qqH"  ) || 
	  match(histName, "VH"   ) || 
	  match(histName, "SM"   ));
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
    if(std::string(pattern).empty() && httSignal(iobj->GetName())){
      histnames.push_back(fullpath);
    }
    else if(!std::string(pattern).empty() && match(iobj->GetName(), (char*)pattern)){
      histnames.push_back(fullpath);
    }
  }
  return histnames;
}

void rescaleSignal(bool armed, double scale, const char* filename, const char* pattern="", unsigned int debug=0)
{
  std::vector<std::string> histnames; histnames.clear();
  if( debug>0 ){
    std::cout << "file  = " << filename << std::endl;
    std::cout << "scale = " << scale    << std::endl;
    std::cout << "armed = " << armed    << std::endl;
  }
  TFile* file = new TFile(filename, "update");
  TIter nextDirectory(file->GetListOfKeys());
  std::vector<std::string> buffer;
  TKey* idir;
  while((idir = (TKey*)nextDirectory())){
    buffer.clear();
    if( idir->IsFolder() ){
      file->cd(); // make sure to start in directory head 
      if( debug>0 ){ std::cout << "Found directory: " << idir->GetName() << std::endl; }
      if( file->GetDirectory(idir->GetName()) ){
	file->cd(idir->GetName()); // change to sub-directory
	buffer = signalList(idir->GetName(), pattern, debug);
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
  // pick up files which are not kept in an extra folder
  file->cd(); buffer.clear();
  buffer = signalList("", pattern, debug);
  // append to the vector of histograms to be rescaled
  for(std::vector<std::string>::const_iterator elem=buffer.begin(); elem!=buffer.end(); ++elem){
    histnames.push_back(*elem);
  }
  if(debug>1){
    std::cout << "added " << buffer.size() << " elements to histnames [" << histnames.size() << "] for file head" << std::endl;
  }

  for(std::vector<std::string>::const_iterator hist=histnames.begin(); hist!=histnames.end(); ++hist){
    file->cd();
    TH1F* h = (TH1F*)file->Get(hist->c_str());
    std::string histName;
    if(hist->find("/")!=std::string::npos){
      histName = hist->substr(hist->find("/")+1);
    }
    else{
      histName = *hist;
    }
    TH1F* hout = (TH1F*)h->Clone(histName.c_str());
    if(debug>1){
      std::cout << "...folder    : " << hist->substr(0, hist->find("/")).c_str() << std::endl;
      std::cout << "...histogram : " << hout->GetName () << " / " << hist->c_str() << std::endl; 
      std::cout << "...old scale : " << hout->Integral() << std::endl; 
    }
    hout->Scale(scale);
    if(match(pattern, "data")){
      //make sure to have an integer integral when rescaling data yields
      hout->Scale(int(hout->Integral())/hout->Integral());
    }
    if(debug>1){ 
      std::cout << "...new scale : " << hout->Integral() << std::endl; 
    }
    if(armed){
      if(hist->find("/")!=std::string::npos){
	file->cd(hist->substr(0, hist->find("/")).c_str());
      }
      else{
	file->cd();
      }
      if(debug>0){
	std::cout << "writing to file: " << hout->GetName() << std::endl;
      }
      hout->Write(hist->substr(hist->find("/")+1).c_str(), TObject::kOverwrite); 
    }
  }
  file->Close();
  return;
}
