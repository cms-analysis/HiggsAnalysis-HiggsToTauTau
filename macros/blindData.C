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
#include <TRegexp.h>
#include <TString.h>
#include <TCollection.h>

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"


/**
   \class   blindData blindData.C "HiggsAnalysis/HiggsToTauTau/macros/blindData.C"

   \brief   macro to replace data_obs by the exact expectation from all indicated background and potentially signal histograms.

   Macro to replace the data_obs histogram by the exact expectation from all indicated 
   background and potantially signal histograms. The list of background and signal 
   histograms and the input file have to be given as agruments. The macro will survery
   the input file for one directory layer according to the conventions for htt limit 
   combinations and in this directory structure search for the data_obs histogram and 
   the indicated background (and signal) historams. The data_obs histogram will be 
   reset and refilled by the sum of all indicated background (and signal) histograms.
   The bin-wise uncertainties will be set up the sqrt(N) of the corresponding bin 
   content to give for proper uncertainties, when the signal strength is calculated 
   based on the blinded data_obs histogram.

   The macro can be used to inject signal for a given mass into the data_obs. To obtain 
   the expected signal only from background just pass an empty string for the signal 
   samples as argument. In case you intend to inject signal keep in mind that you should 
   have scaled the signal of your input file by the corresponding cross section to obtain 
   a proper yield estimate for the signal. 

   The input od data_obs can be randomized according to a Poissonian distributrion. If 
   no signal nor background samples are given as function arguments the content of data_obs 
   will be randomized based on the existing content. This can be used to do toy studies 
   based on the actual observation in data. 

   Function arguments are:
   
   filename               : input file that is supposed to keep the input histograms
   background_patterns    : list of background samples (should be separated by comma 
                            or whitespaces).
   signal_patterns        : list of signal samples (should be separated by comma or 
                            whitespaces).
   directory_patterns     : give a list of directory\ies to which the blinding should be 
                            applied only or '*' to apply it to all directories. 
   armed                  : write modified data_obs histograms back to file.
   rnd                    : randomized the content of data_obs with given integer value 
                            as random seed. If -1 is given data_obs is not randomized. 
   signal_scale           : in case you want to add signal into the content of data_obs 
                            you can give an arbitary scale here. 1 corresponds to the 
			    SM case. 
   outputLabel            : if non empty and armed is true the output of data_obs (only!)
                            will be written to a new output file with postfix outputLabel. 
			    If armed and outputLabel is an empty string (a) new data_obs
			    histogram(s) with name(s) data_obs_asimov will be added to the 
			    inputfile.
   data_obs               : indicate special histogram names for data_obs if necessary.
   debug                  : invoke several debug output levels. 
*/

void adjustUncerts(TH1F* hist){
  for(int idx=0; idx<hist->GetNbinsX(); ++idx){
    hist->SetBinError(idx+1, TMath::Sqrt(hist->GetBinContent(idx+1)));    
  }
}

void randomize(TRandom3* rnd, TH1F* hist, unsigned int debug=0.)
{
  for(int idx=0; idx<hist->GetNbinsX(); ++idx){
    float value = rnd->Poisson(hist->GetBinContent(idx+1));
    // --------------------------------- DEBUG > 2 ------------------------------- //
    if(debug>2){ std::cout << "[" << idx+1 << "] : " << "mean=" << hist->GetBinContent(idx+1) << "  rnd=" << value << std::endl;  }
    hist->SetBinContent(idx+1, value); hist->SetBinError(idx+1, TMath::Sqrt(value));
  }
  // make sure there is no rounding error, and the total is really an integer.
  if(hist->Integral() != 0){
    hist->Scale(TMath::Nint(hist->Integral())/hist->Integral());
  }
}

bool inPatterns(const std::string& test, const char* patterns)
{
  std::vector<std::string> samples;
  string2Vector(cleanupWhitespaces(patterns), samples);
  for(std::vector<std::string>::const_iterator sample = samples.begin(); sample!=samples.end(); ++sample){
    TRegexp matcher(sample->c_str(), true);  // true = make it "glob-style" i.e. "*" instead of ".*"
    if(TString(test).Index(matcher) > -1){
      return true;
    }
  }
  return false;
}

void
blinding(TRandom3* rnd, TFile* inputFile, TFile* outputFile, std::string dir, std::string hist, std::vector<std::string> samples, const char* signal_patterns, double signal_scale, bool armed, unsigned int debug)
{
  if(!dir.empty()){ dir+='/'; }
  TH1F* buffer = (TH1F*)inputFile->Get((dir+hist).c_str());
  if(!buffer){
    // --------------------------------- DEBUG > 0 ------------------------------- //
    if(debug>0){ std::cout << "WARNING: Did not find data_obs histogram of type " << hist << " in directory " << dir << ". Directory will be skipped." << std::endl; }
    return;
  }
  TH1F* blind_data_obs = (TH1F*)buffer->Clone(hist.c_str()); 
  if(!samples.empty()){
    blind_data_obs->Reset();
    for(std::vector<std::string>::const_iterator sample = samples.begin(); sample!=samples.end(); ++sample){
      // ------------------------------- DEBUG > 1 ------------------------------- //
      if( debug>1 ){ std::cerr << "Looking for histogram: " << (dir+(*sample)) << std::endl; }
      buffer = (TH1F*)inputFile->Get((dir+(*sample)).c_str()); 
      if (!buffer) {
	std::cerr << "ERROR : Could not get histogram " << dir+(*sample) << ". Histogram will be skipped from asimov dataset." << std::endl;
	continue;
      }
      if(inPatterns(*sample, signal_patterns)) {
	// ----------------------------- DEBUG > 1 ------------------------------- //
	if( debug>1 ){ std::cerr << "INFO  : Scale signal sample " << *sample << " by scale " << signal_scale << std::endl; }
	buffer->Scale(signal_scale);
      }
      blind_data_obs->Add(buffer);
      // ------------------------------- DEBUG > 1 ------------------------------- //
      if (debug > 1){ std::cerr << "INFO  : Adding: " << buffer->GetName() << " -- " << buffer->Integral() << " --> New value: " << blind_data_obs->Integral() << std::endl; }
    }
  }
  else{
    std::cout << "INFO  : Data are not blinded." << std::endl;
  }
  if(rnd){
    // randomize histogram; this will automatically have integer integral
    std::cout << "-- R A N D O M I Z I N G --" << std::endl;
    randomize(rnd, blind_data_obs, debug);
  }
  else{
    // use expected mean with signal injected
    blind_data_obs->Scale(TMath::Nint(blind_data_obs->Integral())/blind_data_obs->Integral());
    // adjust uncertainties
    adjustUncerts(blind_data_obs);
  }
  std::cout << "INFO  : New data_obs yield in dir (" << dir << "):   " << blind_data_obs->Integral() << std::endl;
  if(armed){
    // --------------------------------- DEBUG > 1 ------------------------------- //
    if (debug > 1){ std::cerr << "INFO  : Writing to file: " << blind_data_obs->GetName() << std::endl; }
    if(outputFile){
      // write to a dedicated new file with name output in case output has been specified
      outputFile->mkdir(dir.c_str()); outputFile->cd(dir.c_str());
      blind_data_obs->Write(hist.c_str()); 
    }
    else{
      // add new data_obs as old data_obs_asimov in the inputfile otherwise
      inputFile->cd(dir.c_str());
      blind_data_obs->Write((hist.append(std::string("_asimov"))).c_str(), TObject::kOverwrite); 
    }
  }
}

void blindData(const char* filename, const char* background_patterns="Fakes, EWK, ttbar, Ztt", const char* signal_patterns="ggH125, qqH125, VH125", const char* directory_patterns="*", bool armed=false, int seed=-1, float signal_scale=1., const char* outputLabel="", const char* data_obs="data_obs", unsigned int debug=1)
{
  /// init random seed
  TRandom3* rnd = 0;
  if(seed>0){
    rnd = new TRandom3(); 
    rnd->SetSeed(seed);
  }
  /// prepare input parameters
  std::vector<std::string> signals;
  string2Vector(cleanupWhitespaces(signal_patterns), signals);
  std::vector<std::string> samples;
  string2Vector(cleanupWhitespaces(background_patterns), samples);
  samples.insert(samples.end(), signals.begin(), signals.end());

  // in case data_obs is supposed to be written to an extra output file open
  // the file, otherwise the data_obs in the input file will be overwritten
  TFile* outputFile = 0; 
  std::string out(filename);
  if(!std::string(outputLabel).empty()){
    outputFile = new TFile((out.substr(0, out.rfind("."))+"_"+outputLabel+".root").c_str(), "update"); 
  }

  TKey* idir;
  TFile* inputFile = new TFile(filename, "update");
  TIter nextDirectory(inputFile->GetListOfKeys());
  while((idir = (TKey*)nextDirectory())){
    if(idir->IsFolder()){
      inputFile->cd(); // make sure to start in directory head 
      // ------------------------------- DEBUG > 0 ------------------------------- //
      if(debug>0){ std::cerr << "Found directory: " << idir->GetName() << std::endl; }
      // check if we want to muck w/ this directory. For the vhtt case, we 
      // have different background types in the same root file, so we have 
      // to run blindData twice.
      if(!inPatterns(std::string(idir->GetName()), directory_patterns)) {
	// ----------------------------- DEBUG > 0 ------------------------------- //
        if(debug>0){ std::cerr << "WARNING: Skipping directory: " << idir->GetName() << ". No match found in pattern: " << directory_patterns << std::endl; }
        continue;
      }
      if(inputFile->GetDirectory(idir->GetName())){
	inputFile->cd(idir->GetName()); // change to sub-directory
	blinding(rnd, inputFile, outputFile, idir->GetName(), data_obs, samples, signal_patterns, signal_scale, armed, debug);
      }
    }
  }
  blinding(rnd, inputFile, outputFile, "", data_obs, samples, signal_patterns, signal_scale, armed, debug);
  inputFile->Close();
  if(outputFile){
    outputFile->Close();
  }
  if(rnd){ delete rnd; }
  return;
}

