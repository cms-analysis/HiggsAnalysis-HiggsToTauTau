#include <map>
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
   \class   rescalSignal renameSignal.C "HiggsAnalysis/HiggsToTauTau/macros/renameSignal.C"

   \brief   macro to rename the signal component(s) for histogram based limit inputs for limi calculation to the standard naming scheme agreed upon in the HiggsCombination Group.

   Macro to rename all signal components in a given input file for limit calculations
   to the naming scheme agreed upon in the HiggsCombination Group. This naming scheme
   is: ggH, qqH, VH (WH, ZH), ttH. 

   The macro searches the head of the file and the next level of histogram directories 
   from the head of the file on. All directories in the given layer will be searched for 
   histograms. All histograms that fullfill a given PATTERN will be renamed. If the 
   PATTERN is empty all histograms that that followed the old grown htt conventions will 
   be renamed accordingly. All other histograms remain the same name. The macro iterates 
   only through one level of folders. These folders are expected to contain only 
   histograms. Function arguments are:
   
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

std::map<const char*, const char*>
httDictionary()
{
  std::map<const char*, const char*> dict_;
  // emu names
  dict_["Higgs_gf_sm_" ] = "ggH";
  dict_["Higgs_vbf_sm_"] = "qqH";
  // etau/mutau names
  dict_["SM"           ] = "ggH";
  dict_["VBF"          ] = "qqH";
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

const char*
rename(std::string hist, const char* pattern, const char* name)
{
  std::string new_name;
  if(hist.find(pattern)!=std::string::npos){
    std::string old_name = hist.substr(hist.find("/")+1);
    new_name = old_name.substr(0, old_name.find(pattern));
    new_name+= name;
    new_name+= old_name.substr(old_name.find(pattern)+std::string(pattern).size());
  }
  return new_name.c_str();
}

void renameSignal(const char* filename, const char* pattern="", const char* name="", bool armed=false, unsigned int debug=0)
{
  std::vector<std::string> histnames; histnames.clear();
  if( debug>0 ){
    std::cout << "file    = " << filename << std::endl;
    std::cout << "pattern = " << pattern  << std::endl;
    std::cout << "name    = " << name     << std::endl;
    std::cout << "armed   = " << armed    << std::endl;
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
      // append to the vector of histograms to be renamed
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
  buffer = signalList("", pattern, debug);
  // append to the vector of histograms to be renamed
  for(std::vector<std::string>::const_iterator elem=buffer.begin(); elem!=buffer.end(); ++elem){
    histnames.push_back(*elem);
  }
  if(debug>1){
    std::cout << "added " << buffer.size() << " elements to histnames [" << histnames.size() << "] for file head" << std::endl;
  }

  if(std::string(pattern).empty()){
    std::map<const char*, const char*> dict = httDictionary();
    for(std::map<const char*, const char*>::const_iterator htt = dict.begin(); htt!=dict.end(); ++htt){
      for(std::vector<std::string>::const_iterator hist=histnames.begin(); hist!=histnames.end(); ++hist){
	// cut off directory names to prevent that the pattern is matched to those
	if(hist->substr(hist->find("/")+1).find(htt->first)!=std::string::npos){
	  file->cd();
	  TH1F* h = (TH1F*)file->Get(hist->c_str());
	  if(debug>1){
	    std::cout << "search string is : " << htt->first << std::endl;
	    std::cout << "...folder        : " << hist->substr(0, hist->find("/")).c_str() << std::endl;
	    std::cout << "...old name      : " << *hist << std::endl; 
	    std::cout << "...new name      : " << rename(*hist, htt->first, htt->second) << std::endl; 
	  }
	  if(armed){
	    if(hist->find("/")!=std::string::npos){
	      file->cd(hist->substr(0, hist->find("/")).c_str());
	    }
	    else{
	      file->cd();
	    }
	    h->Write(rename(*hist, htt->first, htt->second)); 
	  }
	}
      }
    }
  }
  else{
    for(std::vector<std::string>::const_iterator hist=histnames.begin(); hist!=histnames.end(); ++hist){
      file->cd();
      TH1F* h = (TH1F*)file->Get(hist->c_str());
      if(debug>1){
	std::cout << "search string is : " << pattern << std::endl;
	std::cout << "...folder        : " << hist->substr(0, hist->find("/")).c_str() << std::endl;
	std::cout << "...old name      : " << *hist << std::endl; 
	std::cout << "...new name      : " << rename(*hist, pattern, name) << std::endl; 
      }
      if(armed){
	if(hist->find("/")!=std::string::npos){
	  file->cd(hist->substr(0, hist->find("/")).c_str());
	}
	else{
	  file->cd();
	}
	h->Write(rename(*hist, pattern, name)); 
      }
    }
  }
  file->Close();
  return;
}

