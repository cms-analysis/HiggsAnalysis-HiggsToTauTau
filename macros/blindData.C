#include <map>
#include <string>
#include <vector>
#include <iostream>

#include <TKey.h>
#include <TH1F.h>
#include <TFile.h>
#include <TROOT.h>
#include <TMath.h>
#include <TRandom3.h>
#include <TCollection.h>

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"


/**
   \class   blindData blindData.C "HiggsAnalysis/HiggsToTauTau/macros/blindData.C"

   \brief   macro to replace data_obs by the exact expectation from all indicated background and potentially signal histograms.

   Macro to replace the data_obs histogram by the exact expectation from all indicated 
   background and potantially signal histograms. The list of background and signal 
   histograms and the input file have to be given as agruments. The macro will survery
   the input file for one directory layer according to the conventions for htt limit 
   combinations and in this directory structire search for the data_obs histogram and 
   the indicated background (and signal) historams. The data_obs histogram will be 
   reset and refilled by the sum of all indicated background (and signal) histograms.
   
   The macro can be used to inject signal for a given mass into the data_obs. To obtain 
   the expected signal only from background just pass an empty string for the signal 
   samples as argument. In case you intend to inject signal keep in mind that you should 
   have scaled the signal of you input file by the corresponding cross section to obtain 
   a proper yield estimate for the signal. 

   Function arguments are:
   
   filename               : input file that is supposed to keep the input histograms
   background_patterns    : list of background samples (should be separated by comma 
                            or whitespaces)
   signal_patterns        : list of signal samples (should be separated by comma or 
                            whitespaces)
   armed                  : write modified data_obs histograms back to file
*/

void randomize(TH1F* hist, unsigned int seed, unsigned int debug=0.)
{
  TRandom3* rnd = new TRandom3(seed); 
  for(int idx=0; idx<hist->GetNbinsX(); ++idx){
    if(debug>0){
      std::cout << "[" << idx+1 << "] : " << "mean=" << hist->GetBinContent(idx+1) << "  rnd=" << rnd->Poisson(hist->GetBinContent(idx+1)) << std::endl;  
    }
    hist->SetBinContent(idx+1, rnd->Poisson(hist->GetBinContent(idx+1)));
    hist->SetBinError(idx+1, TMath::Sqrt(rnd->Poisson(hist->GetBinContent(idx+1))));
  }
  delete rnd;
}

bool inPatterns(const std::string& test, const char* patterns)
{
  std::vector<std::string> samples;
  string2Vector(cleanupWhitespaces(patterns), samples);
  for(std::vector<std::string>::const_iterator sample = samples.begin(); sample!=samples.end(); ++sample){
    if(test == *sample) return true;
  }
  return false;
}

void blindData(const char* filename, const char* background_patterns="Fakes, EWK, ttbar, Ztt", const char* signal_patterns="ggH125, qqH125, VH125", bool armed=false, int rnd=-1, float signal_scale=1., unsigned int debug=1)
{
  /// prepare input parameters
  std::vector<std::string> signals;
  string2Vector(cleanupWhitespaces(signal_patterns), signals);
  std::vector<std::string> samples;
  string2Vector(cleanupWhitespaces(background_patterns), samples);
  samples.insert(samples.end(), signals.begin(), signals.end());

  TKey* idir;
  TH1F* buffer = 0;
  TH1F* blind_data_obs = 0;
  TFile* file = new TFile(filename, "update");
  TIter nextDirectory(file->GetListOfKeys());
  //std::vector<TH1F*> hists;
  while((idir = (TKey*)nextDirectory())){
    if( idir->IsFolder() ){
      file->cd(); // make sure to start in directory head 
      if( debug>0 ){ std::cout << "Found directory: " << idir->GetName() << std::endl; }
      if( file->GetDirectory(idir->GetName()) ){
	file->cd(idir->GetName()); // change to sub-directory
	buffer = (TH1F*)file->Get((std::string(idir->GetName())+"/data_obs").c_str()); blind_data_obs = (TH1F*)buffer->Clone("data_obs");
	//if( debug>0 ){ std::cout << "Old scale of blinded data_obs: " << blind_data_obs->Integral() << std::endl; }
	blind_data_obs->Reset();
	for(std::vector<std::string>::const_iterator sample = samples.begin(); sample!=samples.end(); ++sample){
	  if( debug>0 ){ std::cout << "Looking for histogram: " << (std::string(idir->GetName())+"/"+(*sample)) << std::endl; }
	  buffer = (TH1F*)file->Get((std::string(idir->GetName())+"/"+(*sample)).c_str()); 
	  if(inPatterns(*sample, signal_patterns)) {
	    if( debug>1 ){
	      std::cout << " scale signal sample " << *sample << " by scale " << signal_scale << std::endl;
	    }
	    buffer->Scale(signal_scale);
	  }
	  blind_data_obs->Add(buffer);
	}
	if(rnd>=0){
	  // randomize histogram; this will automatically have integer integral
	  randomize(blind_data_obs, rnd, debug);
	}
	else{
	  // use expected mean with signal injected
	  blind_data_obs->Scale((int)blind_data_obs->Integral()/blind_data_obs->Integral());
	  if( debug>1 ){ std::cout << "New scale of blinded data_obs: " << blind_data_obs->Integral() << std::endl; }
	}
	std::cout << "data_obs yield: " << idir->GetName() << "   " << blind_data_obs->Integral() << std::endl;
	if(armed){
	  std::cout << "Writing to file: " << blind_data_obs->GetName() << std::endl;
	  blind_data_obs->Write("data_obs", TObject::kOverwrite); 
	}
      }
    }
  }
  file->Close();
  return;
}

