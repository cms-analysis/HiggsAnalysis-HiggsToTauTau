#include <iostream>

#include "TFile.h"
#include "TH1F.h"

float integrate(TH1F* hist){
  float value = 0;
  for(int i=0; i<hist->GetNbinsX(); ++i){
    value+=hist->GetBinContent(i+1)*hist->GetBinWidth(i+1);
  }
  return value;
}

void yield(const char* filename, const char* sample="")
{
  TFile* file = TFile::Open(filename);
  TH1F*  data = (TH1F*)file->Get("data_obs" );
  //TH1F*  BG   = (TH1F*)file->Get("Ztt");
  TH1F*  BG   = (TH1F*)file->Get("errorBand");
  TH1F*  ggH  = (TH1F*)file->Get("ggH");
  TH1F*  qqH  = (TH1F*)file->Get("qqH");
  TH1F*  VH   = (TH1F*)file->Get("VH" );

  //std::cout << "File: " << filename << std::endl;
  //std::cout << "data_obs:             Summed BG:" << std::endl;
  //std::cout << integrate(data) << "          " << integrate(BG) << std::endl;

  float norm = integrate(ggH)-integrate(BG );
  std::cout << "File: " << filename << std::endl;
  std::cout << "ggH:             qqH:                  VH:                  cmb(signal):" << std::endl;
  std::cout << (integrate(ggH)-integrate(qqH)) / norm
	    << "          " 
	    << (integrate(qqH)-integrate(VH )) / norm
	    << "          " 
	    << (integrate(VH )-integrate(BG )) / norm
	    << "          " 
	    << integrate(ggH)-integrate(BG ) 
	    << std::endl;
}
