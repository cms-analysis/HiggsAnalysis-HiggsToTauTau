#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

/// This is the core plotting routine that can also be used within
/// root macros. It is therefore not element of the PlotLimits class.
void plottingSignalStrength(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraph* central, TGraph* unit, std::string& xaxis, std::string& yaxis, std::string signal, double min, double max, bool log=false, bool legendOnRight=false);

void
PlotLimits::plotSignalStrength(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraph* central, const char* directory)
{
  // set up styles
  SetStyle();
  // create the unit line
  TGraph* unit=0;
  if(!mssm_){
    unit = new TGraph();
    for(unsigned int imass=0, ipoint=0; imass<bins_.size(); ++imass){
      if(valid_[imass]){
	unit->SetPoint(ipoint, bins_[imass], 1.); ++ipoint;
      }
    }
  }

  // pick up final results; this requires that they have been 
  // produced beforehand using limit.py --multidim-fit
  char type[20]; 
  for(unsigned int imass=0, ipoint=0; imass<bins_.size(); ++imass){
    // buffer mass value
    float mass = bins_[imass];
    if(verbosity_>2){ std::cout << mass << std::endl; }

    std::string line;
    std::string fullpath;
    float bestfit, bestfitDown, bestfitUp;
    fullpath = TString::Format("%s/%d/multi-dim.fitresult", directory, (int)mass);
    ifstream multidim (fullpath.c_str());
    if(multidim.is_open()){
      while( multidim.good() ){
	getline (multidim,line);
	sscanf (line.c_str(),"%s :    %f   %f/%f (68%%)", type, &bestfit, &bestfitDown, &bestfitUp);
	if(std::string(type)==signal_){
	  central  ->SetPoint(ipoint, mass, bestfit);
	  innerBand->SetPoint(ipoint, mass, bestfit);
	  innerBand->SetPointEYlow (ipoint, fabs(bestfitDown));
	  innerBand->SetPointEYhigh(ipoint, fabs(bestfitUp));
	  ipoint++;
	}
      }
      multidim.close();
    }
  }
  // do the plotting 
  plottingSignalStrength(canv, innerBand, central, unit, xaxis_, yaxis_, signal_, min_, max_, log_, mssm_);
  // setup the CMS Preliminary
  CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);
  // write results to files
  if(png_){
    canv.Print(std::string(output_).append("_").append(label_).append(".png").c_str());
  }
  if(pdf_){
    canv.Print(std::string(output_).append("_").append(label_).append(".pdf").c_str());
    canv.Print(std::string(output_).append("_").append(label_).append(".eps").c_str());
  }
  if(txt_){
    print(std::string(output_).append("_").append(label_).c_str(), 0, innerBand, central, 0, "txt");
    print(std::string(output_).append("_").append(label_).c_str(), 0, innerBand, central, 0, "tex");
  }
  if(root_){
    TFile* output = new TFile(std::string("limits_").append(label_).append(".root").c_str(), "update");
    if(!output->cd(output_.c_str())){
      output->mkdir(output_.c_str());
      output->cd(output_.c_str());
    }
    central  ->Write("bestFit" );
    innerBand->Write("innerBand");
    output->Close();
  }
  return;
}


