#include <string>
#include <vector>
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
   \class   rescaleLumi rescaleLumi.C "HiggsAnalysis/HiggsToTauTau/macros/rescaleLumi.C"

   \brief   macro to rescale the lumi for histogram based inputs for limit calculation.

    Macro to rescale input files for limit calculations to an arbitrary luminosity. 
    The original luminosty has to be known. All directories in the given file will
    be searched for histograms. All histograms will be scaled to the new lumi. For
    histograms with name 'data_obs' the new yield will be scaled to an integer value
    to satisfy the combine limit calculation tool requirementss. The macro iterates 
    only through one level of folders. These folders are expected to contain only 
    histograms. Function arguments are the filename which is supposed to keep the 
    input histograms for the limit calculation the old and the new lumi. A new root 
    file will be written out with file extension *_rescaled 
*/

void rescaleLumi(const char* filename, float oldLumi=4.9, float newLumi=12., unsigned int debug=0)
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
      if(debug>0){ std::cout << "Found directory: " << idir->GetName() << std::endl; }
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
    if(debug>2){ std::cout << " ...created directory: " << *dir << std::endl; }
    new_file->mkdir(*dir);
  } 
  // do the rescaling and write new object to file
  for(std::vector<TString>::const_iterator path = paths.begin(); path!=paths.end(); ++path){ 
    TH1F* h = (TH1F*)old_file->Get(*path);
    if(debug>1){ std::cout << "histogram: " << *path << std::endl; }
    if(debug>1){ std::cout << "...old scale : " << h->Integral() << std::endl; }
    h->Scale(newLumi/oldLumi);  
    if(std::string(*path).find("data_obs")!=std::string::npos){
      if (h->Integral() > 0)  h->Scale((int)h->Integral()/h->Integral());
    }
    if(debug>1){ std::cout << "...new scale : " << h->Integral() << std::endl; }
    std::string str = std::string(*path);
    std::string dir = str.substr(0, str.find("/"));
    std::string hist = str.substr(str.find("/")+1, std::string::npos);
    new_file->cd();;
    new_file->cd(dir.c_str());
    h->Write(hist.c_str()); 
  }
  old_file->Close();
  new_file->Close();
  return;
}
