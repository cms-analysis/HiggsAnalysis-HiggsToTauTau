
#include <TFile.h>
#include <TDirectory.h>
#include <TList.h>
#include <TKey.h>
#include <TString.h>
#include <TH1.h>
#include <TFormula.h>
#include <TMath.h>
#include <TROOT.h>

#include <string>
#include <vector>
#include <iostream>
#include <iomanip>
#include <assert.h>

void addShapeUncertaintyToHistogram(TH1* histogram, const std::string& directoryName, const std::string& nuissanceName, TFormula* uncertaintyFormula)
{
  std::cout << "<addShapeUncertaintyToHistogram>: histogramName = " << histogram->GetName() << std::endl;
  std::string buffer = std::string(histogram->GetName());
  std::string histogramName = buffer.substr(0,buffer.find("_fine_binning"));
  std::string histogramPostfix = (buffer.find("_fine_binning")==std::string::npos) ?  std::string() : std::string("_fine_binning");
  std::cout << "Name: " << histogramName << " -- postfix: " << histogramPostfix << std::endl;

  std::string histogramName_up = Form("%s_%sUp%s", histogramName.data(), nuissanceName.data(), histogramPostfix.data());
  TH1* histogram_up = (TH1*)histogram->Clone(histogramName_up.data());
  std::string histogramName_down = Form("%s_%sDown%s", histogramName.data(), nuissanceName.data(), histogramPostfix.data());
  TH1* histogram_down = (TH1*)histogram->Clone(histogramName_down.data());

  int numBins = histogram->GetNbinsX();
  for ( int iBin = 1; iBin <= numBins; ++iBin ) {
    double binContent = histogram->GetBinContent(iBin);
    double binError = histogram->GetBinError(iBin);
    double binCenter = histogram->GetBinCenter(iBin);
    double uncertaintyValue = uncertaintyFormula->Eval(binCenter);

    histogram_up->SetBinContent(iBin, binContent*(1. + uncertaintyValue));
    histogram_up->SetBinError(iBin, binError*(1. + uncertaintyValue));

    histogram_down->SetBinContent(iBin, binContent*(1. - uncertaintyValue));
    histogram_down->SetBinError(iBin, binError*(1. - uncertaintyValue));
  }

  histogram_up->Write();
  histogram_down->Write();
}

void walkThroughFile(TDirectory* file_or_directory, const std::string& directoryName, const std::string& process, const std::string& nuissanceName, TFormula* uncertaintyFormula)
{
  std::cout << "<walkThroughFile>: processing directory = " << directoryName << std::endl;
  file_or_directory->cd();
  TList* keys = file_or_directory->GetListOfKeys();
  int numKeys = keys->GetLast() + 1;
  for ( int iKey = 0; iKey < numKeys; ++iKey ) {
    TKey* key = dynamic_cast<TKey*>(keys->At(iKey));
    if ( !key ) continue;
    std::string objName = key->GetName();
    std::string objType = key->ReadObj()->ClassName();
    std::cout << "key #" << iKey << ": name = " << objName << ", type = " << objType << std::endl;
    if ( objType == "TDirectoryFile" ) {
      TDirectoryFile* subDirectory = dynamic_cast<TDirectoryFile*>(key->ReadObj());
      assert(subDirectory);
      std::string subDirectoryName = directoryName;
      if ( subDirectoryName.length() > 0 ) subDirectoryName.append("/");
      subDirectoryName.append(objName);
      walkThroughFile(subDirectory, subDirectoryName, process, nuissanceName, uncertaintyFormula);
    } else if ( objType.find("TH1") != std::string::npos && objName.find(process) == 0 && objName.find("_") == std::string::npos ) { // CV: only process histogram for "central value"
      TH1* histogram = dynamic_cast<TH1*>(key->ReadObj());
      assert(histogram);
      addShapeUncertaintyToHistogram(histogram, directoryName, nuissanceName, uncertaintyFormula);
    } else if (  objType.find("TH1") != std::string::npos && objName == process+std::string("_fine_binning") ){
      TH1* histogram = dynamic_cast<TH1*>(key->ReadObj());
      assert(histogram);
      addShapeUncertaintyToHistogram(histogram, directoryName, nuissanceName, uncertaintyFormula);
    }
  }
}

int addShapeUncertainty(const std::string& inputFileName = "htt_mt.inputs-mssm-7TeV-0_ImperialDEBUG.root", 
			const std::string& process = "W", 
			const std::string& nuissanceName = "tailShape", 
			const std::string& uncertaintyFormula_string = "0.3*x/1500.")
{
  TFormula* uncertaintyFormula = new TFormula("uncertaintyFormula", uncertaintyFormula_string.data());
  
  //TFile* inputFile = new TFile(inputFileName.data());
  TFile* inputFile = new TFile(inputFileName.data(), "UPDATE");
  walkThroughFile(inputFile, "", process, nuissanceName, uncertaintyFormula);
  delete inputFile;
  
  delete uncertaintyFormula;

  return 0;
}
