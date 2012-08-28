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

   \brief   macro to rescale the lumi for histogram based limit inputs for limi calculation.

    Macro to rescale input files for limit calculations to an arbitrary luminosity. 
    The original luminosty has to be known. All directories in the given file will
    be searched for histograms. All histograms will be scaled to the new lumi. For
    histograms with name 'data_obs' the new yield will be scaled to an integer value
    to satisfy the combine limit calculation tool. The macro iterates only through
    one level of folders. These folders are expected to contain only histograms.
    Function arguments are the filename which is supposed to keep the input histo-
    grams for the limit calculation and a boolean to indicate whether the rescaled
    histograms should already be written to file, or whether this is just a test
    run.
*/

void rescaleLumi(const char* filename, float oldLumi=4.9, float newLumi=10., bool armed=false, unsigned int debug=0)
{
  //float        oldLumi  = 4.9;
  //float        newLumi  = 10.;
  //unsigned int debug    = 2;

  TFile* file = new TFile(filename, "update");
  TIter nextDirectory(file->GetListOfKeys());
  TKey* idir;
  std::vector<TString> paths;
  // collect all histogram names
  while((idir = (TKey*)nextDirectory())){
    if(idir->IsFolder()){
      file->cd(); // make sure to start in directory head 
      if(debug>0){ std::cout << "Found directory: " << idir->GetName() << std::endl; }
      if(file->GetDirectory(idir->GetName())){
	file->cd(idir->GetName()); // change to sub-directory
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
  // do the rescaling
  for(std::vector<TString>::const_iterator path = paths.begin(); path!=paths.end(); ++path){
    TH1F* h = (TH1F*)file->Get(*path);
    if(debug>1){ std::cout << "histogram: " << *path << std::endl; }
    if(debug>1){ std::cout << "...old scale : " << h->Integral() << std::endl; }
    h->Scale(newLumi/oldLumi);
    if(std::string(h->GetName()).find("data_obs")!=std::string::npos){
      if (h->Integral() > 0)
	h->Scale((int)h->Integral()/h->Integral());
    }
    if(debug>1){ std::cout << "...new scale : " << h->Integral() << std::endl; }
    if(armed){
      std::string str = std::string(*path);
      std::string dir = str.substr(0, str.find("/"));
      std::string hist = str.substr(str.find("/")+1, std::string::npos);
      file->cd();
      file->cd(dir.c_str());
      h->Write(hist.c_str()); 
    }
  }
  file->Close();
  return;
}
