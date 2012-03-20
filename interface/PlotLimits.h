#ifndef PlotLimits_h
#define PlotLimits_h

#include <math.h>
#include <vector> 
#include <fstream>
#include <iomanip>
#include <iostream>
#include <algorithm>

#include "TTree.h"
#include "TFile.h"
#include "TAxis.h"
#include "TGraph.h"
#include "TColor.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TPaveLabel.h"
#include "TGraphAsymmErrors.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"

/**
   \class   Plotlimits PlotLimits.h "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

   \brief   Class to draw official plots for HiggsToTauTau limits

   To follow soon 
*/

class PlotLimits {
  
 public:
  /// contructor from cfg file (not yet implemented)
  PlotLimits(const char* output, const edm::ParameterSet& cfg);
  ///default destructor
  ~PlotLimits() {};

  /// fill LP plots for SM or MSSM
  TGraphAsymmErrors* fillLP2011(TGraphAsymmErrors* graph, bool mssm, bool inner);
  /// fill the central value either for observed or expected
  TGraph* fillCentral(const char* directory, TGraph* plot, const char* filename);  
  /// fill the +/-1sigma and +/-2sigma uncertainty band
  TGraphAsymmErrors* fillBand(const char* directory, TGraphAsymmErrors* plot, const char* method, bool innerBand);
  /// print tabulated limits to a txt file, for inner band, outer band, expected and observed
  void print(const char* filename, TGraphAsymmErrors* outerBand, TGraphAsymmErrors* innerBand, TGraph* expected, TGraph* observed, const char* type="txt");
  /// plot limits on canvas, print out png, pdf, txt, root formats if desired 
  void plot(TCanvas& canv, TGraphAsymmErrors* outerBand, TGraphAsymmErrors* innerBand, TGraph* expected, TGraph* observed=0);
  /// plot limits for tanb on canvas, print out png, pdf, txt, root formats if desired 
  void plotTanb(TCanvas& canv, TGraphAsymmErrors* outerBand, TGraphAsymmErrors* innerBand, TGraph* expected, TGraph* observed=0);

 private:
  /// fill a single vector of values according to 2sigma, 1sigma, median or observed 
  /// from Asymptotic limits 
  void prepareAsymptotic(const char* directory, std::vector<double>& values, const char* type);
  /// fill a single vector of values according to 2sigma, 1sigma, mean or median from 
  /// Bayesian limits; in case files do not exists or were corrupted for a given mass
  /// point the initial value of -1. will be filled the member functions fillCentral 
  /// and fillBand should check for values of -1. and take these mass points out of 
  /// consideration  
  void prepareBayesian(const char* directory, std::vector<double>& values, const char* type);
  /// fill a single vector of values according to 2sigma, 1sigma or median from CLs 
  /// limits; 
  void prepareCLs(const char* directory, std::vector<double>& values, const char* type) { 
    prepareSimple(directory, values, std::string("higgsCombineTest.HybridNew.$MASS").append(type).c_str()); 
  };
  // fill a single vector of values from a file filename; ; in case files do not exists 
  /// or were corrupted for a given mass point the initial value of -1. will be filled 
  /// the member functions fillCentral and fillBand should check for values of -1. and 
  /// take these mass points out of consideration
  void prepareSimple(const char* directory, std::vector<double>& values, const char* filename);
  /// fill officially approved limits for LP2011 (NOTE: these are cross section also for MSSM)
  void prepareHIG_11_020(std::vector<double>& values, const char* type);
  /// fill officially approved limits for HIG-11-029 paper (NOTE: these are direct limits on tanb for MSSM)
  void prepareHIG_11_029(std::vector<double>& values, const char* type);
  
 private:
  /// output name and directory 
  /// name in root file
  std::string output_; 
  /// string for luminosity and cms label
  std::string dataset_;
  /// x-axis title?
  std::string xaxis_;
  /// y-axis title?
  std::string yaxis_;
  /// mssm or sm plots for LP11?
  bool mssm_;
  /// print out png format?
  bool png_;
  /// print out pdf format?
  bool pdf_;
  /// print out txt format?
  bool txt_;
  /// print out root format?
  bool root_;
  /// minimum for plotting
  double min_; 
  /// maximum for plotting
  double max_; 
  /// log scale for plotting
  int log_; 
  /// define verbosity level
  unsigned int verbosity_;
  /// additional output label 
  /// for png, pdf, txt 
  std::string outputLabel_;
  /// binning for limits
  std::vector<double> bins_;
  /// check whether mass point is available or not
  std::vector<bool> valid_; 
};

inline void
PlotLimits::prepareHIG_11_020(std::vector<double>& values, const char* type)
{
  if(mssm_){
    if(std::string(type)==std::string("observed")){
      values.push_back(14.076);
      values.push_back( 7.995);
      values.push_back( 4.501);
      values.push_back( 4.095);
      values.push_back( 3.834);
      values.push_back( 3.103);
      values.push_back( 2.296);
      values.push_back( 2.353);
      values.push_back( 1.700);
      values.push_back( 1.227);
      values.push_back( 0.600);
      values.push_back( 0.416);
      values.push_back( 0.335);
    }
    else if (std::string(type)==std::string("+2sigma")){
      values.push_back(34.598);
      values.push_back(24.746);
      values.push_back(11.224);
      values.push_back( 9.260);
      values.push_back( 6.884);
      values.push_back( 5.011);
      values.push_back( 3.504);
      values.push_back( 2.916);
      values.push_back( 1.848);
      values.push_back( 1.279);
      values.push_back( 0.736);
      values.push_back( 0.579);
      values.push_back( 0.457);
    }
    else if (std::string(type)==std::string("+1sigma")){
      values.push_back(24.864);
      values.push_back(18.287);
      values.push_back( 8.397);
      values.push_back( 6.899);
      values.push_back( 5.134);
      values.push_back( 3.718);
      values.push_back( 2.616);
      values.push_back( 2.190);
      values.push_back( 1.351);
      values.push_back( 0.955);
      values.push_back( 0.538);
      values.push_back( 0.416);
      values.push_back( 0.335);
    }
    else if(std::string(type)==std::string("expected")){
      values.push_back(17.802);
      values.push_back(12.569);
      values.push_back( 6.001);
      values.push_back( 4.823);
      values.push_back( 3.655);
      values.push_back( 2.630);
      values.push_back( 1.883);
      values.push_back( 1.543);
      values.push_back( 0.957);
      values.push_back( 0.661);
      values.push_back( 0.376);
      values.push_back( 0.294);
      values.push_back( 0.254);
    }
    else if (std::string(type)==std::string("-1sigma")){
      values.push_back(12.360);
      values.push_back( 8.644);
      values.push_back( 4.062);
      values.push_back( 3.381);
      values.push_back( 2.619);
      values.push_back( 1.877);
      values.push_back( 1.323);
      values.push_back( 1.119);
      values.push_back( 0.701);
      values.push_back( 0.470);
      values.push_back( 0.264);
      values.push_back( 0.213);
      values.push_back( 0.213);
    }
    else if (std::string(type)==std::string("-2sigma")){
      values.push_back( 9.211);
      values.push_back( 6.216);
      values.push_back( 2.891);
      values.push_back( 2.579);
      values.push_back( 1.912);
      values.push_back( 1.450);
      values.push_back( 0.945);
      values.push_back( 0.703);
      values.push_back( 0.518);
      values.push_back( 0.368);
      values.push_back( 0.213);
      values.push_back( 0.132);
      values.push_back( 0.172);
    }
    else{
      std::cout << "ERROR: picked wrong type. Available types are: +2sigma, +1sigma, mean, median, -1sigma, -2sigma" << std::endl
		<< "       for the moment I'll stop here" << std::endl;
      exit(1);
    }
  }
  else{
    if(std::string(type)==std::string("observed")){
      values.push_back( 5.984);
      values.push_back( 7.018);
      values.push_back( 7.618);
      values.push_back( 7.106);
      values.push_back(10.029);
      values.push_back(10.352);
      values.push_back(12.415);
      values.push_back(17.923);
    }
    else if(std::string(type)==std::string("+2sigma")){
      values.push_back(10.971);
      values.push_back(11.788);
      values.push_back(11.099);
      values.push_back(11.190);
      values.push_back(12.661);
      values.push_back(14.527);
      values.push_back(17.831);
      values.push_back(24.432);
    }
    else if(std::string(type)==std::string("+1sigma")){
      values.push_back( 7.839);
      values.push_back( 8.663);
      values.push_back( 8.010);
      values.push_back( 8.108);
      values.push_back( 9.178);
      values.push_back(10.558);
      values.push_back(12.944);
      values.push_back(17.708);
    }
    else if(std::string(type)==std::string("expected")){
      values.push_back( 5.402);
      values.push_back( 6.139);
      values.push_back( 5.606);
      values.push_back( 5.706);
      values.push_back( 6.439);
      values.push_back( 7.430);
      values.push_back( 9.124);
      values.push_back(12.534);
    }
    else if(std::string(type)==std::string("-1sigma")){
      values.push_back( 3.911);
      values.push_back( 4.443);
      values.push_back( 4.013);
      values.push_back( 3.997);
      values.push_back( 4.563);
      values.push_back( 5.401);
      values.push_back( 6.522);
      values.push_back( 8.975);
    }
    else if(std::string(type)==std::string("-2sigma")){
      values.push_back( 3.114);
      values.push_back( 3.342);
      values.push_back( 3.110);
      values.push_back( 3.117);
      values.push_back( 3.440);
      values.push_back( 4.209);
      values.push_back( 5.210);
      values.push_back( 7.148);
    }
    else{
      std::cout << "ERROR: picked wrong type. Available types are: +2sigma, +1sigma, mean, median, -1sigma, -2sigma" << std::endl
		<< "       for the moment I'll stop here" << std::endl;
      exit(1);
    }
  }
  return;
}

inline void
PlotLimits::prepareHIG_11_029(std::vector<double>& values, const char* type)
{
  if(mssm_){
    if(std::string(type)==std::string("observed")){
      values.push_back(12.246);
      values.push_back(11.799);
      values.push_back( 9.842);
      values.push_back( 9.026);
      values.push_back( 8.031);
      values.push_back( 7.113);
      values.push_back( 7.504);
      values.push_back( 8.464);
      values.push_back(13.755);
      values.push_back(20.943);
      values.push_back(29.124);
      values.push_back(37.298);
      values.push_back(45.178);
      values.push_back(51.904);
    } 
    else if (std::string(type)==std::string("-2sigma")){
      values.push_back( 5.194);
      values.push_back( 6.492);
      values.push_back( 4.500);
      values.push_back( 5.369);
      values.push_back( 5.615);
      values.push_back( 5.574);
      values.push_back( 6.747);
      values.push_back( 7.845);
      values.push_back(10.327);
      values.push_back(13.469);
      values.push_back(17.660);
      values.push_back(21.923);
      values.push_back(25.008);
      values.push_back(30.315);
    }
    else if (std::string(type)==std::string("-1sigma")){
      values.push_back( 7.009);
      values.push_back( 7.450);
      values.push_back( 6.475);
      values.push_back( 6.710);
      values.push_back( 6.628);
      values.push_back( 6.986);
      values.push_back( 8.140);
      values.push_back( 9.118);
      values.push_back(12.344);
      values.push_back(15.704);
      values.push_back(20.093);
      values.push_back(24.298);
      values.push_back(29.164);
      values.push_back(35.739);
    }
    else if(std::string(type)==std::string("expected")){
      values.push_back( 8.371);
      values.push_back( 8.777);
      values.push_back( 8.087);
      values.push_back( 7.847);
      values.push_back( 7.901);
      values.push_back( 8.514);
      values.push_back( 9.533);
      values.push_back(10.519);
      values.push_back(13.923);
      values.push_back(18.378);
      values.push_back(23.025);
      values.push_back(27.886);
      values.push_back(33.264);
      values.push_back(40.510);
    }
    else if (std::string(type)==std::string("+1sigma")){
      values.push_back(10.605);
      values.push_back(10.828);
      values.push_back( 9.889);
      values.push_back( 9.691);
      values.push_back( 9.692);
      values.push_back(10.419);
      values.push_back(11.324);
      values.push_back(12.811);
      values.push_back(16.765);
      values.push_back(21.415);
      values.push_back(26.939);
      values.push_back(32.449);
      values.push_back(38.800);
      values.push_back(47.145);
    }
    else if (std::string(type)==std::string("+2sigma")){
      values.push_back(12.836);
      values.push_back(13.418);
      values.push_back(11.957);
      values.push_back(11.453);
      values.push_back(11.557);
      values.push_back(12.453);
      values.push_back(13.762);
      values.push_back(14.989);
      values.push_back(19.373);
      values.push_back(24.471);
      values.push_back(31.113);
      values.push_back(37.293);
      values.push_back(44.728);
      values.push_back(55.000);
    }
    else{
      std::cout << "ERROR: picked wrong type. Available types are: +2sigma, +1sigma, mean, median, -1sigma, -2sigma" << std::endl
		<< "       for the moment I'll stop here" << std::endl;
      exit(1);
    }
  }
  else{ // SM Winter11 results
    if(std::string(type)==std::string("observed")){
      values.push_back( 3.20);
      values.push_back( 3.19);
      values.push_back( 3.62);
      values.push_back( 4.27);
      values.push_back( 5.08);
      values.push_back( 5.39);
      values.push_back( 5.46);
      values.push_back( 7.00);
    }
    else if(std::string(type)==std::string("+2sigma")){
      values.push_back( 6.63);
      values.push_back( 5.86);
      values.push_back( 6.07);
      values.push_back( 6.01);
      values.push_back( 6.43);
      values.push_back( 7.87);
      values.push_back( 7.99);
      values.push_back(10.70);
    }
    else if(std::string(type)==std::string("+1sigma")){
      values.push_back( 4.76);
      values.push_back( 4.23);
      values.push_back( 4.33);
      values.push_back( 4.38);
      values.push_back( 4.72);
      values.push_back( 5.77);
      values.push_back( 5.85);
      values.push_back( 7.65);
    }
    else if(std::string(type)==std::string("expected")){
      values.push_back( 3.30);
      values.push_back( 2.97);
      values.push_back( 3.03);
      values.push_back( 3.05);
      values.push_back( 3.31);
      values.push_back( 4.06);
      values.push_back( 4.17);
      values.push_back( 5.45);
    }
    else if(std::string(type)==std::string("-1sigma")){
      values.push_back( 2.36);
      values.push_back( 2.13);
      values.push_back( 2.17);
      values.push_back( 2.19);
      values.push_back( 2.37);
      values.push_back( 2.96);
      values.push_back( 2.99);
      values.push_back( 3.97);
    }
    else if(std::string(type)==std::string("-2sigma")){
      values.push_back( 1.83);
      values.push_back( 1.61);
      values.push_back( 1.65);
      values.push_back( 1.75);
      values.push_back( 1.82);
      values.push_back( 2.25);
      values.push_back( 2.39);
      values.push_back( 3.06);
    }
    else{
      std::cout << "ERROR: picked wrong type. Available types are: +2sigma, +1sigma, mean, median, -1sigma, -2sigma" << std::endl
		<< "       for the moment I'll stop here" << std::endl;
      exit(1);
    }
  }
  return;
}

#endif
