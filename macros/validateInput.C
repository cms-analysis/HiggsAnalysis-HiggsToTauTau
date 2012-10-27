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
   \class   validateInput validateInput.C "HiggsAnalysis/HiggsToTauTau/macros/validateInput.C"

   \brief   macro to perform some minimal validation of the histograms in a root input file.
*/

void
validateFolder(TFile* file, const char* folder="", int level=-1)
{
  TIter next(gDirectory->GetListOfKeys());
  TKey* iobj;
  unsigned int idx=0;
  while((iobj = (TKey*)next())){
    if(iobj->IsFolder()) continue;
    if(level>1){ std::cout << "[" << ++idx << "] ...Found object: " << iobj->GetName() << " of type: " << iobj->GetClassName() << std::endl; }
    std::string fullpath(folder); 
    fullpath += (fullpath == std::string("")) ? "" : "/"; fullpath += iobj->GetName();
    TH1F* h = (TH1F*)file->Get(fullpath.c_str());
    if(h->Integral() == 0){
      std::cout << "----- E R R O R ----- : histogram has 0 integral please fix this: --> " << fullpath << std::endl; 
    }
  }
  return;
}

void validateInput(const char* filename, int level=0)
{
  TFile* file = new TFile(filename, "update");
  TIter nextDirectory(file->GetListOfKeys());
  TKey* idir;
  while((idir = (TKey*)nextDirectory())){
    file->cd();
    if( idir->IsFolder() ){
      if( level>-1 ){ std::cout << "Found directory: " << idir->GetName() << std::endl; }
      file->cd(idir->GetName());
      validateFolder(file, idir->GetName(), level);
    }
    else{
      if( level> 0 ){ std::cout << "Found histogram: " << idir->GetName() << std::endl; }
      if( level>-1 ){ 
	TH1F* h = (TH1F*)file->Get(idir->GetName());
	if(h->Integral() == 0){
	  std::cout << "----- E R R O R ----- : histogram has 0 integral please fix this: --> " << idir->GetName() << std::endl; 
	}
      }
    }
  }
  file->Close();
  return;
}
