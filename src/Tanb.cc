#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

/// This is the core plotting routine that can also be used within
/// root macros. It is therefore not element of the PlotLimits class.
void plottingTanb(TCanvas& canv, TGraphAsymmErrors* plain, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed, TGraph* lowerLEP, TGraph* upperLEP, std::map<double, TGraphAsymmErrors*> higgsBands, std::string& xaxis, std::string& yaxis, double min=0., double max=50., bool log=false);

TGraphAsymmErrors*  
PlotLimits::higgsConstraint(const char* directory, double mass, double deltaM)
{
  TGraphAsymmErrors* graph = new TGraphAsymmErrors();
  for(unsigned int imass=0, ipoint=0; imass<bins_.size(); ++imass){
    std::string line;
    bool filled = false;
    float tanb, mh, mA, mH, upperTanb=-1., lowerTanb=-1.;
    ifstream higgs (TString::Format("%s/%d/higgs_mass.dat", directory, (int)bins_[imass]));
    if(higgs.is_open()){
      while(higgs.good()){
	getline(higgs,line);
	sscanf(line.c_str(),"%f %f %f %f", &tanb, &mh, &mA, &mH);
	if(fabs(mh-mass)<deltaM){
	  if(!filled){
	    graph->SetPoint(ipoint, bins_[imass], tanb); graph->SetPointEYlow(ipoint, 0.);
	    ipoint++; filled = true;
	    lowerTanb=tanb;
	  }
	  upperTanb=tanb;
	}
      }
      if(upperTanb>0){
	graph->SetPointEYhigh(ipoint-1, upperTanb-lowerTanb);
      }
    }
    higgs.close();
  }
  return graph;
}

void
PlotLimits::plotTanb(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed, const char* directory)
{
  // set up styles
  SetStyle();

  // create plain background
  TGraphAsymmErrors* plain=0;
  if(observed){
    plain=new TGraphAsymmErrors();
    plain->SetPoint(0, observed->GetX()[0], 100.);
    plain->SetPointEYlow (0, 0);
    plain->SetPointEYhigh(0, 100); 
    for(unsigned int imass=0, ipoint=0; imass<bins_.size(); ++imass){
      if(valid_[imass]){
	plain->SetPoint(ipoint+1, observed->GetX()[ipoint], observed->GetY()[ipoint]); 
	plain->SetPointEYlow (ipoint+1, 0);
 	plain->SetPointEYhigh(ipoint+1, 100);
	++ipoint;
      }
    }
  }

  // create LEP exclusion plot
  TGraph* upperLEP = new TGraph();
  upperLEPLimits(upperLEP);

  TGraph* lowerLEP = new TGraph();
  lowerLEPLimits(lowerLEP);

  // setup contratins from Higgs mass
  std::map<double, TGraphAsymmErrors*> higgsBands;
  if(higgs125_){
    for(unsigned int deltaM=0; deltaM<3; ++deltaM){
      higgsBands[3-deltaM] = higgsConstraint(directory, 125., 4-deltaM);
    }
  }
  
  // do the plotting 
  plottingTanb(canv, plain, innerBand, outerBand, expected, observed, lowerLEP, upperLEP, higgsBands, xaxis_, yaxis_, min_, max_, log_);
  /// setup the CMS Preliminary
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
    print(std::string(output_).append("_").append(label_).c_str(), outerBand, innerBand, expected, observed, "txt");
    print(std::string(output_).append("_").append(label_).c_str(), outerBand, innerBand, expected, observed, "tex");
  }
  if(root_){
    TFile* output = new TFile(std::string("limits_").append(label_).append(".root").c_str(), "update");
    if(!output->cd(output_.c_str())){
      output->mkdir(output_.c_str());
      output->cd(output_.c_str());
    }
    if(observed){ 
      observed ->Write("observed" );
    }
    expected ->Write("expected" );
    innerBand->Write("innerBand");
    outerBand->Write("outerBand");
    output->Close();
  }
  return;
}

