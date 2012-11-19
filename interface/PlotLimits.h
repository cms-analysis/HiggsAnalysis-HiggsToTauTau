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

   This is a class for drawing the official plots for HiggsToTauTau limits. It is instantiated from
   the tool plot that can be found in the bin directory of this package. The class requires a layout
   file in the style of CMSSW cfi python files to pick up certain layout parameters and a particular
   directory structure containing the limit output files (as provided by combine) as input to pick
   up the limit results from there. The input directory should point to the head directory containing
   all mass points as subdirectories. In the subdirectories the limits ouptut files from combine
   looked for. This structure can be achieved automatically when using the other (wrapper) tools
   for limit calculation provided in the same package. Pre-defined layout files can be found in the
   python/layout sub-directory of this package.

   Depending on the layout the class provides plots for SM limits (on signal strength), on the MSSM
   cross section (in pb) or on the MSSM parameter tanb. The output consists of:

    - a plot in png format
    - a plot in pdf format
    - a machiene readable txt file containing the observed and expected limit and the uncertainty
      bands
    - a tex file containing the observed and expected limit and the uncertainty bands
    - a root output file with name limit_mssm/sm.root containing the observed and expected limit
      and uncertainty bands in TGraph format.

    in the directory in which the tool plot has been executed. The names of the png/pdf/txt/tex output
    files will be derived from the laypout and from the input directory. The output in the
    limits_mssm/sm.root file will be updated in case a file with similar file is already present in
    the directory where the tool plot has been executed or the file will be created otherwise. In the
    limits_mssm/sm.root the limits for a given input directory will be safed in a directory
    corresponding to the name of the input directory. The file is suited for further processing with
    the macro compareLimits.C in the macros directory of the same package. For more details on how
    to run the tool plot have a look in the bin dorectory of this package or just execute the tool
    w/o any aditional arguments given.
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
  /// print tabulated limits to a txt file, for inner band, outer band, expected and observed, w/o inner and outer band
  void print(const char* filename, TGraph* expected, TGraph* observed, const char* type="txt");
  /// print tabulated limits to a txt file, for inner band, outer band, expected and observed, with inner and outer band
  void print(const char* filename, TGraphAsymmErrors* outerBand, TGraphAsymmErrors* innerBand, TGraph* expected, TGraph* observed, const char* type="txt");
  /// plot limits on canvas, print out png, pdf, txt, root formats if desired
  void plot(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed=0);
  /// plot limits for tanb on canvas, print out png, pdf, txt, root formats if desired
  void plotTanb(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed=0, const char* directory="");
  /// plot bestfit values for different parameters dependend on mass
  void plotMDF(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed=0, const char* directory="");
  /// plot significance in linear scale and w/o band
  void plotSignificance(TCanvas& canv, TGraph* expected, TGraph* observed=0);

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
  /// fill a single vector of values according to 1sigma from MaxLikelihoodFit limits;
  void prepareMaxLikelihood(const char* directory, std::vector<double>& values, const char* filename, float ConLevel);
  /// fill a single vector of values from a file filename; ; in case files do not exists
  /// or were corrupted for a given mass point the initial value of -1. will be filled
  /// the member functions fillCentral and fillBand should check for values of -1. and
  /// take these mass points out of consideration
  void prepareSimple(const char* directory, std::vector<double>& values, const char* filename);
  /// fill officially approved limits for LP2011 (NOTE: these are cross section also for MSSM)
  void prepareHIG_11_020(std::vector<double>& values, const char* type, bool xsec, double mass, bool initial);
  /// fill officially approved limits for HIG-11-029 paper (NOTE: these are direct limits on tanb for MSSM)
  void prepareHIG_11_029(std::vector<double>& values, const char* type, double mass, bool initial);
  /// fill officially approved limits for HIG-12-018 PAS and HIG-12-028 paper (NOTE: these are only SM limits)
  void prepareHIG_12_018(std::vector<double>& values, const char* type, double mass, bool initial);
  /// fill officially approved limits for HIG-12-032 PAS (NOTE: these are only SM limits)
  void prepareHIG_12_032(std::vector<double>& values, const char* type, double mass, bool initial);


  /// fill the mA-tanb20-xsec curve (only for mA mssm 8TeV mhmax mu=200GeV)
  void xs_mA_tanb1_mhmax200_8TeV(TGraph* graph);
  // fill the mA-tanb20-xsec curve (only for mA mssm 8TeV mhmax mu=200GeV)
  void xs_mA_tanb5_mhmax200_8TeV(TGraph* graph);
  /// fill the mA-tanb20-xsec curve (only for mA mssm 8TeV mhmax mu=200geV)
  void xs_mA_tanb20_mhmax200_8TeV(TGraph* graph);
  /// fill the mA-tanb50-xsec curve (only for mA mssm 8TeV mhmax mu=200GeV)
  void xs_mA_tanb50_mhmax200_8TeV(TGraph* graph);
  /// fill the mA-tanb50-xsec curve (only for mA mssm 8TeV mhmax mu=200GeV)
  void xs_mA_tanb70_mhmax200_8TeV(TGraph* graph);

  /// fill the mA-tanb20-xsec curve (only for mA mssm 7TeV mhmax mu=-400GeV)
  void xs_mA_tanb1_mhmax_neg400_7TeV(TGraph* graph);
  /// fill the mA-tanb20-xsec curve (only for mA mssm 7TeV mhmax mu=-400GeV)
  void xs_mA_tanb5_mhmax_neg400_7TeV(TGraph* graph);
  /// fill the mA-tanb20-xsec curve (only for mA mssm 7TeV mhmax mu=-400geV)
  void xs_mA_tanb20_mhmax_neg400_7TeV(TGraph* graph);
  /// fill the mA-tanb50-xsec curve (only for mA mssm 7TeV mhmax mu=-400GeV)
  void xs_mA_tanb50_mhmax_neg400_7TeV(TGraph* graph);
  /// fill the mA-tanb50-xsec curve (only for mA mssm 7TeV mhmax mu=-400GeV)
  void xs_mA_tanb70_mhmax_neg400_7TeV(TGraph* graph);

  /// fill the mA-tanb20-xsec curve (only for mA mssm 7TeV mhmax mu=200GeV)
  void xs_mA_tanb1_mhmax200_7TeV(TGraph* graph);
  /// fill the mA-tanb20-xsec curve (only for mA mssm 7TeV mhmax mu=200GeV)
  void xs_mA_tanb5_mhmax200_7TeV(TGraph* graph);
  /// fill the mA-tanb20-xsec curve (only for mA mssm 7TeV mhmax mu=200geV)
  void xs_mA_tanb20_mhmax200_7TeV(TGraph* graph);
  /// fill the mA-tanb50-xsec curve (only for mA mssm 7TeV mhmax mu=200GeV)
  void xs_mA_tanb50_mhmax200_7TeV(TGraph* graph);
  /// fill the mA-tanb50-xsec curve (only for mA mssm 7TeV mhmax mu=200GeV)
  void xs_mA_tanb70_mhmax200_7TeV(TGraph* graph); 

  /// fill the mA-tanb20-xsec curve (only for mA mssm 7TeV mhmax mu=800GeV)
  void xs_mA_tanb1_mhmax800_7TeV(TGraph* graph);
  /// fill the mA-tanb20-xsec curve (only for mA mssm 7TeV mhmax mu=800GeV)
  void xs_mA_tanb5_mhmax800_7TeV(TGraph* graph);
  /// fill the mA-tanb20-xsec curve (only for mA mssm 7TeV mhmax mu=800geV)
  void xs_mA_tanb20_mhmax800_7TeV(TGraph* graph);
  /// fill the mA-tanb50-xsec curve (only for mA mssm 7TeV mhmax mu=800GeV)
  void xs_mA_tanb50_mhmax800_7TeV(TGraph* graph);
  /// fill the mA-tanb50-xsec curve (only for mA mssm 7TeV mhmax mu=800GeV)
  void xs_mA_tanb70_mhmax800_7TeV(TGraph* graph); 

  /// fill the mA-tanb20-xsec curve (only for mA mssm 7TeV nomix mu=200GeV)
  void xs_mA_tanb1_nomix200_7TeV(TGraph* graph);
  /// fill the mA-tanb20-xsec curve (only for mA mssm 7TeV nomix mu=200GeV)
  void xs_mA_tanb5_nomix200_7TeV(TGraph* graph);
  /// fill the mA-tanb20-xsec curve (only for mA mssm 7TeV nomix mu=200geV)
  void xs_mA_tanb20_nomix200_7TeV(TGraph* graph);
  /// fill the mA-tanb50-xsec curve (only for mA mssm 7TeV nomix mu=200GeV)
  void xs_mA_tanb50_nomix200_7TeV(TGraph* graph);
  /// fill the mA-tanb50-xsec curve (only for mA mssm 7TeV nomix mu=200GeV)
  void xs_mA_tanb70_nomix200_7TeV(TGraph* graph); 

  /*
    Limits for comparison
  */
  /// fill the LEP exclusion plot
  void limitsLEP(TGraph* graph);
  /// fill the LEP exclusion plot (low tanb free space)
  void limitsLEP2(TGraph* graph); 
  /// fill the limits from the CMS hww SM Higgs search
  void limitsHWW(TGraph* graph, const char* type);
  /// fill the limits from the CMS hgg SM Higgs search
  void limitsHGG(TGraph* graph, const char* type);

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
  /// center of mass energy (7, 8, 78 for combined)
  int ecms_;
  /// print out png format?
  bool png_;
  /// print out pdf format?
  bool pdf_;
  /// print out txt format?
  bool txt_;
  /// print out root format?
  bool root_;
  /// print the +/- 2 sigma band?
  bool outerband_;
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
  /// print higgs125 bands?
  bool higgs125_bands;
  /// POI of multidimfit
  std::string POI_;
  /// whether or not we have signal injection
  bool isInjected_;
  /// whether or not this is significance
  bool isSignificance_;
  /// binning for limits
  std::vector<double> bins_;
  /// check whether mass point is available or not
  std::vector<bool> valid_;
  /// mass for which a limit has been calculated (needed for plotting of HIG-XX-YYY results)
  std::vector<double> masses_;
};

inline void
PlotLimits::prepareHIG_11_020(std::vector<double>& values, const char* type, bool xsec, double mass, bool initial)
{
  if(mssm_){
    if(std::string(type)==std::string("observed")){
      if(xsec){
	// xsec limits
	if(mass== 90) {values.push_back(14.076); if(initial) masses_.push_back(mass);}
	if(mass==100) {values.push_back( 7.995); if(initial) masses_.push_back(mass);}
	if(mass==120) {values.push_back( 4.501); if(initial) masses_.push_back(mass);}
	if(mass==130) {values.push_back( 4.095); if(initial) masses_.push_back(mass);}
	if(mass==140) {values.push_back( 3.834); if(initial) masses_.push_back(mass);}
	if(mass==160) {values.push_back( 3.103); if(initial) masses_.push_back(mass);}
	if(mass==180) {values.push_back( 2.296); if(initial) masses_.push_back(mass);}
	if(mass==200) {values.push_back( 2.353); if(initial) masses_.push_back(mass);}
	if(mass==250) {values.push_back( 1.700); if(initial) masses_.push_back(mass);}
	if(mass==300) {values.push_back( 1.227); if(initial) masses_.push_back(mass);}
	if(mass==400) {values.push_back( 0.600); if(initial) masses_.push_back(mass);}
	if(mass==450) {values.push_back( 0.416); if(initial) masses_.push_back(mass);}
	if(mass==400) {values.push_back( 0.335); if(initial) masses_.push_back(mass);}
      }
      else{
	// tanb limits
	if(mass== 90) {values.push_back(8.50 ); if(initial) masses_.push_back(mass);}
	if(mass==100) {values.push_back(7.92 ); if(initial) masses_.push_back(mass);}
	if(mass==120) {values.push_back(8.67 ); if(initial) masses_.push_back(mass);}
	if(mass==130) {values.push_back(7.78 ); if(initial) masses_.push_back(mass);}
	if(mass==140) {values.push_back(10.99); if(initial) masses_.push_back(mass);}
	if(mass==160) {values.push_back(12.69); if(initial) masses_.push_back(mass);}
	if(mass==180) {values.push_back(14.00); if(initial) masses_.push_back(mass);}
	if(mass==200) {values.push_back(17.66); if(initial) masses_.push_back(mass);}
	if(mass==250) {values.push_back(24.46); if(initial) masses_.push_back(mass);}
	if(mass==300) {values.push_back(31.68); if(initial) masses_.push_back(mass);}
	if(mass==400) {values.push_back(44.82); if(initial) masses_.push_back(mass);}
	if(mass==450) {values.push_back(50.62); if(initial) masses_.push_back(mass);}
	if(mass==500) {values.push_back(59.53); if(initial) masses_.push_back(mass);}
      }
    }
    else if (std::string(type)==std::string("+2sigma")){
      if(xsec){
	// xsec limits
	if(mass== 90) {values.push_back(34.598); }
	if(mass==100) {values.push_back(24.746); }
	if(mass==120) {values.push_back(11.224); }
	if(mass==130) {values.push_back( 9.260); }
	if(mass==140) {values.push_back( 6.884); }
	if(mass==160) {values.push_back( 5.011); }
	if(mass==180) {values.push_back( 3.504); }
	if(mass==200) {values.push_back( 2.916); }
	if(mass==250) {values.push_back( 1.848); }
	if(mass==300) {values.push_back( 1.279); }
	if(mass==400) {values.push_back( 0.736); }
	if(mass==450) {values.push_back( 0.579); }
	if(mass==500) {values.push_back( 0.457); }
      }
      else{
	// tanb limits
	if(mass== 90) {values.push_back(13.33); }
	if(mass==100) {values.push_back(13.90); }
	if(mass==120) {values.push_back(13.86); }
	if(mass==130) {values.push_back(13.16); }
	if(mass==140) {values.push_back(14.81); }
	if(mass==160) {values.push_back(16.13); }
	if(mass==180) {values.push_back(17.20); }
	if(mass==200) {values.push_back(19.64); }
	if(mass==250) {values.push_back(25.48); }
	if(mass==300) {values.push_back(32.29); }
	if(mass==400) {values.push_back(49.22); }
	if(mass==450) {values.push_back(58.79); }
	if(mass==500) {values.push_back(69.25); }
      }
    }
    else if (std::string(type)==std::string("+1sigma")){
      if(xsec){
	/// xsec limits
	if(mass== 90) {values.push_back(24.864); }
	if(mass==100) {values.push_back(18.287); }
	if(mass==120) {values.push_back( 8.397); }
	if(mass==130) {values.push_back( 6.899); }
	if(mass==140) {values.push_back( 5.134); }
	if(mass==160) {values.push_back( 3.718); }
	if(mass==180) {values.push_back( 2.616); }
	if(mass==200) {values.push_back( 2.190); }
	if(mass==250) {values.push_back( 1.351); }
	if(mass==300) {values.push_back( 0.955); }
	if(mass==400) {values.push_back( 0.538); }
	if(mass==450) {values.push_back( 0.416); }
	if(mass==500) {values.push_back( 0.335); }
      }
      else{
	// tanb limits
	if(mass== 90) {values.push_back(11.31); }
	if(mass==100) {values.push_back(11.99); }
	if(mass==120) {values.push_back(12.02); }
	if(mass==130) {values.push_back(11.05); }
	if(mass==140) {values.push_back(12.77); }
	if(mass==160) {values.push_back(13.91); }
	if(mass==180) {values.push_back(14.92); }
	if(mass==200) {values.push_back(17.06); }
	if(mass==250) {values.push_back(21.88); }
	if(mass==300) {values.push_back(28.14); }
	if(mass==400) {values.push_back(42.65); }
	if(mass==450) {values.push_back(50.62); }
	if(mass==500) {values.push_back(59.53); }
      }
    }
    else if(std::string(type)==std::string("expected")){
      if(xsec){
	// xsec limits
	if(mass== 90) {values.push_back(17.802); if(initial) masses_.push_back(mass);}
	if(mass==100) {values.push_back(12.569); if(initial) masses_.push_back(mass);}
	if(mass==120) {values.push_back( 6.001); if(initial) masses_.push_back(mass);}
	if(mass==130) {values.push_back( 4.823); if(initial) masses_.push_back(mass);}
	if(mass==140) {values.push_back( 3.655); if(initial) masses_.push_back(mass);}
	if(mass==160) {values.push_back( 2.630); if(initial) masses_.push_back(mass);}
	if(mass==180) {values.push_back( 1.883); if(initial) masses_.push_back(mass);}
	if(mass==200) {values.push_back( 1.543); if(initial) masses_.push_back(mass);}
	if(mass==250) {values.push_back( 0.957); if(initial) masses_.push_back(mass);}
	if(mass==300) {values.push_back( 0.661); if(initial) masses_.push_back(mass);}
	if(mass==400) {values.push_back( 0.376); if(initial) masses_.push_back(mass);}
	if(mass==450) {values.push_back( 0.294); if(initial) masses_.push_back(mass);}
	if(mass==500) {values.push_back( 0.254); if(initial) masses_.push_back(mass);}
      }
      else{
	// tanb limtis
	if(mass== 90) {values.push_back(9.56 ); if(initial) masses_.push_back(mass);}
	if(mass==100) {values.push_back(9.96 ); if(initial) masses_.push_back(mass);}
	if(mass==120) {values.push_back(10.12); if(initial) masses_.push_back(mass);}
	if(mass==130) {values.push_back(8.75 ); if(initial) masses_.push_back(mass);}
	if(mass==140) {values.push_back(10.71); if(initial) masses_.push_back(mass);}
	if(mass==160) {values.push_back(11.69); if(initial) masses_.push_back(mass);}
	if(mass==180) {values.push_back(12.67); if(initial) masses_.push_back(mass);}
	if(mass==200) {values.push_back(14.37); if(initial) masses_.push_back(mass);}
	if(mass==250) {values.push_back(18.56); if(initial) masses_.push_back(mass);}
	if(mass==300) {values.push_back(23.75); if(initial) masses_.push_back(mass);}
	if(mass==400) {values.push_back(36.32); if(initial) masses_.push_back(mass);}
	if(mass==450) {values.push_back(43.41); if(initial) masses_.push_back(mass);}
	if(mass==500) {values.push_back(52.65); if(initial) masses_.push_back(mass);}
      }
    }
    else if (std::string(type)==std::string("-1sigma")){
      if(xsec){
	// xsec limits
	if(mass== 90) {values.push_back(12.360); }
	if(mass==100) {values.push_back( 8.644); }
	if(mass==120) {values.push_back( 4.062); }
	if(mass==130) {values.push_back( 3.381); }
	if(mass==140) {values.push_back( 2.619); }
	if(mass==160) {values.push_back( 1.877); }
	if(mass==180) {values.push_back( 1.323); }
	if(mass==200) {values.push_back( 1.119); }
	if(mass==250) {values.push_back( 0.701); }
	if(mass==300) {values.push_back( 0.470); }
	if(mass==400) {values.push_back( 0.264); }
	if(mass==450) {values.push_back( 0.213); }
	if(mass==500) {values.push_back( 0.213); }
      }
      else{
	// tanb limits
	if(mass== 90) {values.push_back(7.98 ); }
	if(mass==100) {values.push_back(8.23 ); }
	if(mass==120) {values.push_back(8.19 ); }
	if(mass==130) {values.push_back(6.68 ); }
	if(mass==140) {values.push_back(8.95 ); }
	if(mass==160) {values.push_back(9.87 ); }
	if(mass==180) {values.push_back(10.66); }
	if(mass==200) {values.push_back(12.31); }
	if(mass==250) {values.push_back(16.03); }
	if(mass==300) {values.push_back(20.37); }
	if(mass==400) {values.push_back(31.13); }
	if(mass==450) {values.push_back(37.77); }
	if(mass==500) {values.push_back(48.74); }
      }
    }
    else if (std::string(type)==std::string("-2sigma")){
      if(xsec){
	// xsec limits
	if(mass== 90) {values.push_back( 9.211); }
	if(mass==100) {values.push_back( 6.216); }
	if(mass==120) {values.push_back( 2.891); }
	if(mass==130) {values.push_back( 2.579); }
	if(mass==140) {values.push_back( 1.912); }
	if(mass==160) {values.push_back( 1.450); }
	if(mass==180) {values.push_back( 0.945); }
	if(mass==200) {values.push_back( 0.703); }
	if(mass==250) {values.push_back( 0.518); }
	if(mass==300) {values.push_back( 0.368); }
	if(mass==400) {values.push_back( 0.213); }
	if(mass==450) {values.push_back( 0.132); }
	if(mass==500) {values.push_back( 0.172); }
      }
      else{
	// tanb limits
	if(mass== 90) {values.push_back(6.85 ); }
	if(mass==100) {values.push_back(6.95 ); }
	if(mass==120) {values.push_back(6.65 ); }
	if(mass==130) {values.push_back(5.14 ); }
	if(mass==140) {values.push_back(7.43 ); }
	if(mass==160) {values.push_back(8.64 ); }
	if(mass==180) {values.push_back(9.07 ); }
	if(mass==200) {values.push_back(9.84 ); }
	if(mass==250) {values.push_back(13.92); }
	if(mass==300) {values.push_back(18.30); }
	if(mass==400) {values.push_back(28.40); }
	if(mass==450) {values.push_back(30.95); }
	if(mass==500) {values.push_back(44.45); }
      }
    }
    else{
      std::cout << "ERROR: picked wrong type. Available types are: +2sigma, +1sigma, mean, median, -1sigma, -2sigma" << std::endl
		<< "       for the moment I'll stop here" << std::endl;
      exit(1);
    }
  }
  else{
    if(std::string(type)==std::string("observed")){
      if(mass==110) {values.push_back( 5.984); if(initial) masses_.push_back(mass);}
      if(mass==150) {values.push_back( 7.018); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back( 7.618); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back( 7.106); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back(10.029); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back(10.352); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back(12.415); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back(17.923); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("+2sigma")){
      if(mass==110) {values.push_back(10.971); }
      if(mass==115) {values.push_back(11.788); }
      if(mass==120) {values.push_back(11.099); }
      if(mass==125) {values.push_back(11.190); }
      if(mass==130) {values.push_back(12.661); }
      if(mass==135) {values.push_back(14.527); }
      if(mass==140) {values.push_back(17.831); }
      if(mass==145) {values.push_back(24.432); }
    }
    else if(std::string(type)==std::string("+1sigma")){
      if(mass==110) {values.push_back( 7.839); }
      if(mass==115) {values.push_back( 8.663); }
      if(mass==120) {values.push_back( 8.010); }
      if(mass==125) {values.push_back( 8.108); }
      if(mass==130) {values.push_back( 9.178); }
      if(mass==135) {values.push_back(10.558); }
      if(mass==140) {values.push_back(12.944); }
      if(mass==145) {values.push_back(17.708); }
    }
    else if(std::string(type)==std::string("expected")){
      if(mass==110) {values.push_back( 5.402); if(initial) masses_.push_back(mass);}
      if(mass==115) {values.push_back( 6.139); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back( 5.606); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back( 5.706); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back( 6.439); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back( 7.430); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 9.124); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back(12.534); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("-1sigma")){
      if(mass==110) {values.push_back( 3.911); }
      if(mass==115) {values.push_back( 4.443); }
      if(mass==120) {values.push_back( 4.013); }
      if(mass==125) {values.push_back( 3.997); }
      if(mass==130) {values.push_back( 4.563); }
      if(mass==135) {values.push_back( 5.401); }
      if(mass==140) {values.push_back( 6.522); }
      if(mass==145) {values.push_back( 8.975); }
    }
    else if(std::string(type)==std::string("-2sigma")){
      if(mass==110) {values.push_back( 3.114); }
      if(mass==115) {values.push_back( 3.342); }
      if(mass==120) {values.push_back( 3.110); }
      if(mass==125) {values.push_back( 3.117); }
      if(mass==130) {values.push_back( 3.440); }
      if(mass==135) {values.push_back( 4.209); }
      if(mass==140) {values.push_back( 5.210); }
      if(mass==145) {values.push_back( 7.148); }
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
PlotLimits::prepareHIG_11_029(std::vector<double>& values, const char* type, double mass, bool initial)
{
  if(mssm_){
    if(std::string(type)==std::string("observed")){
      if(mass== 90) {values.push_back(12.246); if(initial) masses_.push_back(mass);}
      if(mass==100) {values.push_back(11.799); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back( 9.842); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back( 9.026); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 8.031); if(initial) masses_.push_back(mass);}
      if(mass==160) {values.push_back( 7.113); if(initial) masses_.push_back(mass);}
      if(mass==180) {values.push_back( 7.504); if(initial) masses_.push_back(mass);}
      if(mass==200) {values.push_back( 8.464); if(initial) masses_.push_back(mass);}
      if(mass==250) {values.push_back(13.755); if(initial) masses_.push_back(mass);}
      if(mass==300) {values.push_back(20.943); if(initial) masses_.push_back(mass);}
      if(mass==350) {values.push_back(29.124); if(initial) masses_.push_back(mass);}
      if(mass==400) {values.push_back(37.298); if(initial) masses_.push_back(mass);}
      if(mass==450) {values.push_back(45.178); if(initial) masses_.push_back(mass);}
      if(mass==500) {values.push_back(51.904); if(initial) masses_.push_back(mass);}
    }
    else if (std::string(type)==std::string("-2sigma")){
      if(mass== 90) {values.push_back( 5.194); }
      if(mass==100) {values.push_back( 6.492); }
      if(mass==120) {values.push_back( 4.500); }
      if(mass==130) {values.push_back( 5.369); }
      if(mass==140) {values.push_back( 5.615); }
      if(mass==160) {values.push_back( 5.574); }
      if(mass==180) {values.push_back( 6.747); }
      if(mass==200) {values.push_back( 7.845); }
      if(mass==250) {values.push_back(10.327); }
      if(mass==300) {values.push_back(13.469); }
      if(mass==350) {values.push_back(17.660); }
      if(mass==400) {values.push_back(21.923); }
      if(mass==450) {values.push_back(25.008); }
      if(mass==500) {values.push_back(30.315); }
    }
    else if (std::string(type)==std::string("-1sigma")){
      if(mass== 90) {values.push_back( 7.009); }
      if(mass==100) {values.push_back( 7.450); }
      if(mass==120) {values.push_back( 6.475); }
      if(mass==130) {values.push_back( 6.710); }
      if(mass==140) {values.push_back( 6.628); }
      if(mass==160) {values.push_back( 6.986); }
      if(mass==180) {values.push_back( 8.140); }
      if(mass==200) {values.push_back( 9.118); }
      if(mass==250) {values.push_back(12.344); }
      if(mass==300) {values.push_back(15.704); }
      if(mass==350) {values.push_back(20.093); }
      if(mass==400) {values.push_back(24.298); }
      if(mass==450) {values.push_back(29.164); }
      if(mass==500) {values.push_back(35.739); }
    }
    else if(std::string(type)==std::string("expected")){
      if(mass== 90) {values.push_back( 8.371); if(initial) masses_.push_back(mass);}
      if(mass==100) {values.push_back( 8.777); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back( 8.087); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back( 7.847); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 7.901); if(initial) masses_.push_back(mass);}
      if(mass==160) {values.push_back( 8.514); if(initial) masses_.push_back(mass);}
      if(mass==180) {values.push_back( 9.533); if(initial) masses_.push_back(mass);}
      if(mass==200) {values.push_back(10.519); if(initial) masses_.push_back(mass);}
      if(mass==250) {values.push_back(13.923); if(initial) masses_.push_back(mass);}
      if(mass==300) {values.push_back(18.378); if(initial) masses_.push_back(mass);}
      if(mass==350) {values.push_back(23.025); if(initial) masses_.push_back(mass);}
      if(mass==400) {values.push_back(27.886); if(initial) masses_.push_back(mass);}
      if(mass==450) {values.push_back(33.264); if(initial) masses_.push_back(mass);}
      if(mass==500) {values.push_back(40.510); if(initial) masses_.push_back(mass);}
    }
    else if (std::string(type)==std::string("+1sigma")){
      if(mass== 90) {values.push_back(10.605); }
      if(mass==100) {values.push_back(10.828); }
      if(mass==120) {values.push_back( 9.889); }
      if(mass==130) {values.push_back( 9.691); }
      if(mass==140) {values.push_back( 9.692); }
      if(mass==160) {values.push_back(10.419); }
      if(mass==180) {values.push_back(11.324); }
      if(mass==200) {values.push_back(12.811); }
      if(mass==250) {values.push_back(16.765); }
      if(mass==300) {values.push_back(21.415); }
      if(mass==350) {values.push_back(26.939); }
      if(mass==400) {values.push_back(32.449); }
      if(mass==450) {values.push_back(38.800); }
      if(mass==500) {values.push_back(47.145); }
    }
    else if (std::string(type)==std::string("+2sigma")){
      if(mass== 90) {values.push_back(12.836); }
      if(mass==100) {values.push_back(13.418); }
      if(mass==120) {values.push_back(11.957); }
      if(mass==130) {values.push_back(11.453); }
      if(mass==140) {values.push_back(11.557); }
      if(mass==160) {values.push_back(12.453); }
      if(mass==180) {values.push_back(13.762); }
      if(mass==200) {values.push_back(14.989); }
      if(mass==250) {values.push_back(19.373); }
      if(mass==300) {values.push_back(24.471); }
      if(mass==350) {values.push_back(31.113); }
      if(mass==400) {values.push_back(37.293); }
      if(mass==450) {values.push_back(44.728); }
      if(mass==500) {values.push_back(55.000); }
    }
    else{
      std::cout << "ERROR: picked wrong type. Available types are: +2sigma, +1sigma, mean, median, -1sigma, -2sigma" << std::endl
		<< "       for the moment I'll stop here" << std::endl;
      exit(1);
    }
  }
  else{ // SM Winter11 results
    if(std::string(type)==std::string("observed")){
      if(mass==110) {values.push_back( 3.20); if(initial) masses_.push_back(mass);}
      if(mass==115) {values.push_back( 3.19); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back( 3.62); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back( 4.27); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back( 5.08); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back( 5.39); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 5.46); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back( 7.00); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("+2sigma")){
      if(mass==110) {values.push_back( 6.63); }
      if(mass==115) {values.push_back( 5.86); }
      if(mass==120) {values.push_back( 6.07); }
      if(mass==125) {values.push_back( 6.01); }
      if(mass==130) {values.push_back( 6.43); }
      if(mass==135) {values.push_back( 7.87); }
      if(mass==140) {values.push_back( 7.99); }
      if(mass==145) {values.push_back(10.70); }
    }
    else if(std::string(type)==std::string("+1sigma")){
      if(mass==110) {values.push_back( 4.76); }
      if(mass==115) {values.push_back( 4.23); }
      if(mass==120) {values.push_back( 4.33); }
      if(mass==125) {values.push_back( 4.38); }
      if(mass==130) {values.push_back( 4.72); }
      if(mass==135) {values.push_back( 5.77); }
      if(mass==140) {values.push_back( 5.85); }
      if(mass==145) {values.push_back( 7.65); }
    }
    else if(std::string(type)==std::string("expected")){
      if(mass==110) {values.push_back( 3.30); if(initial) masses_.push_back(mass);}
      if(mass==115) {values.push_back( 2.97); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back( 3.03); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back( 3.05); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back( 3.31); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back( 4.06); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 4.17); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back( 5.45); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("-1sigma")){
      if(mass==110) {values.push_back( 2.36); }
      if(mass==115) {values.push_back( 2.13); }
      if(mass==120) {values.push_back( 2.17); }
      if(mass==125) {values.push_back( 2.19); }
      if(mass==130) {values.push_back( 2.37); }
      if(mass==135) {values.push_back( 2.96); }
      if(mass==140) {values.push_back( 2.99); }
      if(mass==145) {values.push_back( 3.97); }
    }
    else if(std::string(type)==std::string("-2sigma")){
      if(mass==110) {values.push_back( 1.83); }
      if(mass==115) {values.push_back( 1.61); }
      if(mass==120) {values.push_back( 1.65); }
      if(mass==125) {values.push_back( 1.75); }
      if(mass==130) {values.push_back( 1.82); }
      if(mass==135) {values.push_back( 2.25); }
      if(mass==140) {values.push_back( 2.39); }
      if(mass==145) {values.push_back( 3.06); }
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
PlotLimits::prepareHIG_12_018(std::vector<double>& values, const char* type, double mass, bool initial)
{
  if(mssm_){
    std::cout << "HIG-12-018 contained only SM limits" << std::endl;
    exit(1);
  }
  else{
    if(std::string(type)==std::string("observed")){
      if(mass==110) {values.push_back(1.21); if(initial) masses_.push_back(mass);}
      if(mass==115) {values.push_back( 1.2); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back(1.19); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back(1.06); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back( 1.2); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back(1.81); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 2.2); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back(3.36); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("+2sigma")){
      if(mass==110) {values.push_back(2.52); }
      if(mass==115) {values.push_back(2.47); }
      if(mass==120) {values.push_back(2.41); }
      if(mass==125) {values.push_back(2.36); }
      if(mass==130) {values.push_back(2.48); }
      if(mass==135) {values.push_back(2.84); }
      if(mass==140) {values.push_back(3.33); }
      if(mass==145) {values.push_back(4.35); }
    }
    else if(std::string(type)==std::string("+1sigma")){
      if(mass==110) {values.push_back( 1.9); }
      if(mass==115) {values.push_back(1.86); }
      if(mass==120) {values.push_back(1.81); }
      if(mass==125) {values.push_back(1.78); }
      if(mass==130) {values.push_back(1.87); }
      if(mass==135) {values.push_back(2.14); }
      if(mass==140) {values.push_back(2.51); }
      if(mass==145) {values.push_back(3.28); }
    }
    else if(std::string(type)==std::string("expected")){
      if(mass==110) {values.push_back(1.37); if(initial) masses_.push_back(mass);}
      if(mass==115) {values.push_back(1.34); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back( 1.3); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back(1.28); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back(1.34); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back(1.54); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 1.8); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back(2.36); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("-1sigma")){
      if(mass==110) {values.push_back(0.987); }
      if(mass==115) {values.push_back(0.964); }
      if(mass==120) {values.push_back(0.942); }
      if(mass==125) {values.push_back(0.925); }
      if(mass==130) {values.push_back( 0.97); }
      if(mass==135) {values.push_back( 1.11); }
      if(mass==140) {values.push_back(  1.3); }
      if(mass==145) {values.push_back(  1.7); }
    }
    else if(std::string(type)==std::string("-2sigma")){
      if(mass==110) {values.push_back(0.742); }
      if(mass==115) {values.push_back(0.725); }
      if(mass==120) {values.push_back(0.708); }
      if(mass==125) {values.push_back(0.695); }
      if(mass==130) {values.push_back(0.729); }
      if(mass==135) {values.push_back(0.835); }
      if(mass==140) {values.push_back(0.979); }
      if(mass==145) {values.push_back( 1.28); }
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
PlotLimits::prepareHIG_12_032(std::vector<double>& values, const char* type, double mass, bool initial)
{
  if(mssm_){
    std::cout << "HIG-12-032 contained only SM limits" << std::endl;
    exit(1);
  }
  else{
    if(std::string(type)==std::string("observed")){
      if(mass==110) {values.push_back(0.939); if(initial) masses_.push_back(mass);}
      if(mass==115) {values.push_back( 1.01); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back(    1); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back( 1.01); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back( 1.09); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back( 1.53); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back( 1.78); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back( 2.32); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("+2sigma")){
      if(mass==110) {values.push_back(2.33); }
      if(mass==115) {values.push_back( 2.3); }
      if(mass==120) {values.push_back(2.23); }
      if(mass==125) {values.push_back(2.24); }
      if(mass==130) {values.push_back(2.36); }
      if(mass==135) {values.push_back(2.66); }
      if(mass==140) {values.push_back(3.24); }
      if(mass==145) {values.push_back(3.76); }
    }
    else if(std::string(type)==std::string("+1sigma")){
      if(mass==110) {values.push_back(1.75); }
      if(mass==115) {values.push_back(1.73); }
      if(mass==120) {values.push_back(1.68); }
      if(mass==125) {values.push_back(1.69); }
      if(mass==130) {values.push_back(1.77); }
      if(mass==135) {values.push_back(   2); }
      if(mass==140) {values.push_back(2.44); }
      if(mass==145) {values.push_back(2.83); }
    }
    else if(std::string(type)==std::string("expected")){
      if(mass==110) {values.push_back(1.26); if(initial) masses_.push_back(mass);}
      if(mass==115) {values.push_back(1.25); if(initial) masses_.push_back(mass);}
      if(mass==120) {values.push_back(1.21); if(initial) masses_.push_back(mass);}
      if(mass==125) {values.push_back(1.21); if(initial) masses_.push_back(mass);}
      if(mass==130) {values.push_back(1.28); if(initial) masses_.push_back(mass);}
      if(mass==135) {values.push_back(1.44); if(initial) masses_.push_back(mass);}
      if(mass==140) {values.push_back(1.76); if(initial) masses_.push_back(mass);}
      if(mass==145) {values.push_back(2.04); if(initial) masses_.push_back(mass);}
    }
    else if(std::string(type)==std::string("-1sigma")){
      if(mass==110) {values.push_back(0.911); }
      if(mass==115) {values.push_back(0.899); }
      if(mass==120) {values.push_back(0.871); }
      if(mass==125) {values.push_back(0.877); }
      if(mass==130) {values.push_back(0.922); }
      if(mass==135) {values.push_back( 1.04); }
      if(mass==140) {values.push_back( 1.27); }
      if(mass==145) {values.push_back( 1.47); }
    }
    else if(std::string(type)==std::string("-2sigma")){
      if(mass==110) {values.push_back(0.685); }
      if(mass==115) {values.push_back(0.676); }
      if(mass==120) {values.push_back(0.655); }
      if(mass==125) {values.push_back(0.659); }
      if(mass==130) {values.push_back(0.693); }
      if(mass==135) {values.push_back(0.782); }
      if(mass==140) {values.push_back(0.954); }
      if(mass==145) {values.push_back( 1.11); }
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
PlotLimits::limitsLEP(TGraph* graph)
{
 /*  graph->SetPoint( 0, 80      ,   0.    ); */
/*   graph->SetPoint( 1, 91      , 100.    ); */
/*   graph->SetPoint( 2, 91.8    , 30.02624); */
/*   graph->SetPoint( 3, 91.845  , 22.07032); */
/*   graph->SetPoint( 4, 91.845  , 17.12491); */
/*   graph->SetPoint( 5, 91.84523, 13.64727); */
/*   graph->SetPoint( 6, 92.61388, 11.94143); */
/*   graph->SetPoint( 7, 93.38253, 10.03852); */
/*   graph->SetPoint( 8, 94.91982, 9.021481); */
/*   graph->SetPoint( 9, 95.68846, 8.107481); */
/*   graph->SetPoint(10, 97.22578, 7.141608); */
/*   graph->SetPoint(11, 99.5317 , 6.680381); */
/*   graph->SetPoint(12, 103.375 , 7.189448); */
/*   graph->SetPoint(13, 104.1436, 7.841313); */
/*   graph->SetPoint(14, 106.4496, 8.326916); */
/*   graph->SetPoint(15, 109.5242, 8.609568); */
/*   graph->SetPoint(16, 112.5988, 8.438845); */
/*   graph->SetPoint(17, 115.6733, 8.107481); */
/*   graph->SetPoint(18, 118.748 , 7.384029); */
/*   graph->SetPoint(19, 122.5912, 6.547911); */
/*   graph->SetPoint(20, 126.4344, 5.963618); */
/*   graph->SetPoint(21, 131.815 , 5.359424); */
/*   graph->SetPoint(22, 138.7328, 4.752558); */
/*   graph->SetPoint(23, 144.1134, 4.445624); */
/*   graph->SetPoint(24, 149.4939, 4.186368); */
/*   graph->SetPoint(25, 156.4118, 3.968637); */
/*   graph->SetPoint(26, 164.8669, 3.687628); */
/*   graph->SetPoint(27, 177.1653, 3.472575); */
/*   graph->SetPoint(28, 187.9264, 3.29197 ); */
/*   graph->SetPoint(29, 203.2994, 3.141663); */
/*   graph->SetPoint(30, 221.7469, 2.978266); */
/*   graph->SetPoint(31, 241.7318, 2.861322); */
/*   graph->SetPoint(32, 261.7167, 2.767383); */
/*   graph->SetPoint(33, 283.2388, 2.676528); */
/*   graph->SetPoint(34, 304.761 , 2.641027); */
/*   graph->SetPoint(35, 334.7383, 2.554322); */
/*   graph->SetPoint(36, 357.0292, 2.50367 ); */
/*   graph->SetPoint(37, 383.9319, 2.48701 ); */
/*   graph->SetPoint(38, 420.8271, 2.454023); */
/*   graph->SetPoint(39, 452.3417, 2.421473); */
/*   graph->SetPoint(40, 487.6996, 2.405361); */
/*   graph->SetPoint(41, 550     , 2.405361); */
/*   graph->SetPoint(42, 600     , 2.405361); */
/*   graph->SetPoint(43, 700     , 2.405361); */
/*   graph->SetPoint(44, 800     , 2.405361); */
/*   graph->SetPoint(45, 900     , 2.405361); */
/*   graph->SetPoint(46,1000     , 2.405361); */
/*   graph->SetPoint(47,1100     , 0.      ); */
  graph->SetPoint( 0,  80     ,   0.    );
  graph->SetPoint( 1,  88     , 100.    );
  graph->SetPoint( 2,  90     ,   7.    );
  graph->SetPoint( 3,  95     ,   5.3   );
  graph->SetPoint( 4,  97     ,   5.    );
  graph->SetPoint( 5, 107     ,   4.3   );
  graph->SetPoint( 6, 112     ,   5.    );
  graph->SetPoint( 7, 115     ,   5.3   );
  graph->SetPoint( 8, 122.3   ,   5.    );
  graph->SetPoint( 9, 133.3   ,   4.3   );
  graph->SetPoint(10, 150     ,   3.25  );
  graph->SetPoint(11, 200     ,   2.25  );
  graph->SetPoint(12, 250     ,   1.92  );
  graph->SetPoint(13, 300     ,   1.8   );
  graph->SetPoint(14, 350     ,   1.65  );
  graph->SetPoint(15, 400     ,   1.58  );
  graph->SetPoint(16, 450     ,   1.53  );
  graph->SetPoint(17, 500     ,   1.51  );
  graph->SetPoint(18, 550     ,   1.51  );
  graph->SetPoint(19, 600     ,   1.51  );
  graph->SetPoint(20, 700     ,   1.51  );
  graph->SetPoint(21, 800     ,   1.51  );
  graph->SetPoint(22, 900     ,   1.51  );
  graph->SetPoint(23,1000     ,   1.51  );
  graph->SetPoint(24,1100     ,   0.    );
}

inline void
PlotLimits::limitsLEP2(TGraph* graph)
{
  graph->SetPoint( 0, 246.4   ,   0     );
  graph->SetPoint( 1, 243.3   ,   0.2   ); //246.3, 0.4
  graph->SetPoint( 2, 241     ,   0.3   ); //239  , 0.43
  graph->SetPoint( 3, 240     ,   0.45  ); //239   , 0.45
  graph->SetPoint( 4, 250     ,   0.53  );
  graph->SetPoint( 5, 259.3   ,   0.6   );
  graph->SetPoint( 6, 300     ,   0.7   );
  graph->SetPoint( 7, 350     ,   0.78  );
  graph->SetPoint( 8, 400     ,   0.8   );
  graph->SetPoint( 9, 450     ,   0.82  );
  graph->SetPoint(10, 500     ,   0.83  );
  graph->SetPoint(11, 550     ,   0.835 );
  graph->SetPoint(12, 600     ,   0.835 );
  graph->SetPoint(13, 700     ,   0.835 );
  graph->SetPoint(14, 800     ,   0.835 );
  graph->SetPoint(15, 900     ,   0.835 );
  graph->SetPoint(16,1000     ,   0.835 );
  graph->SetPoint(17,1100     ,   0.    ); 
}

inline void
PlotLimits::limitsHWW(TGraph* graph, const char* type)
{
  // SM limits from mssm_scan/limits/hww-ggH-80_cmb.txt
  if(std::string(type) == std::string("mH-calc-observed")){
    graph->SetPoint( 0,    109.,  0.);
    graph->SetPoint( 1,    110.,  3.38225);
    graph->SetPoint( 2,    120.,  3.33689);
    graph->SetPoint( 3,    130.,  3.60196);
    graph->SetPoint( 4,    140.,  4.02634);
    graph->SetPoint( 5,    150.,  4.72674);
    graph->SetPoint( 6,    160.,  4.55731);
    graph->SetPoint( 7,    170.,  3.83059);
    graph->SetPoint( 8,    180.,  1.75057);
    graph->SetPoint( 9,    190.,  1.50956);
    graph->SetPoint(10,    200.,  1.40033);
    graph->SetPoint(11,    210.,  1.18681);
    graph->SetPoint(12,    220.,  0.);
  }
  if(std::string(type) == std::string("mh-calc-observed")){
    graph->SetPoint( 0,    299.,  100.);
    graph->SetPoint( 1,    300.,  68.2543);
    graph->SetPoint( 2,    310.,  51.8195);
    graph->SetPoint( 3,    320.,  36.6748);
    graph->SetPoint( 4,    330.,  29.4003);
    graph->SetPoint( 5,    340.,  20.5134);
    graph->SetPoint( 6,    350.,  15.5764);
    graph->SetPoint( 7,    360.,  12.826 );
    graph->SetPoint( 8,    370.,  11.8543);
    graph->SetPoint( 9,    380.,  11.6148);
    graph->SetPoint(10,    390.,  11.3927);
    graph->SetPoint(11,    400.,  11.1863);
    graph->SetPoint(12,    420.,  10.138 );
    graph->SetPoint(13,    440.,  8.97407);
    graph->SetPoint(14,    460.,  8.40751);
    graph->SetPoint(15,    480.,  7.74917);
    graph->SetPoint(16,    500.,  7.41296);
    graph->SetPoint(17,    600.,  100.);
  }
  if(std::string(type) == std::string("mH-calc-expected")){
    graph->SetPoint( 0,    109.,  0.);
    graph->SetPoint( 1,    110.,  4.43408);
    graph->SetPoint( 2,    120.,  4.19092);
    graph->SetPoint( 3,    130.,  4.03061);
    graph->SetPoint( 4,    140.,  4.5167 );
    graph->SetPoint( 5,    150.,  5.51353);
    graph->SetPoint( 6,    160.,  5.96611);
    graph->SetPoint( 7,    170.,  4.75407);
    graph->SetPoint( 8,    180.,  1.80079);
    graph->SetPoint( 9,    190.,  1.49742);
    graph->SetPoint(10,    200.,  1.20681);
    graph->SetPoint(11,    201.,  0.);
  }
  if(std::string(type) == std::string("mh-calc-expected")){
    graph->SetPoint( 0,    229.,  100.);
    graph->SetPoint( 1,    230.,  69.6779);
    graph->SetPoint( 2,    240.,  38.3278);
    graph->SetPoint( 3,    250.,  18.6929);
    graph->SetPoint( 4,    260.,  12.906 );
    graph->SetPoint( 5,    270.,  12.6501);
    graph->SetPoint( 6,    280.,  12.4176);
    graph->SetPoint( 7,    290.,  12.2052);
    graph->SetPoint( 8,    300.,  12.013 );
    graph->SetPoint( 9,    310.,  9.94112);
    graph->SetPoint(10,    320.,  8.71568);
    graph->SetPoint(11,    330.,  7.94683);
    graph->SetPoint(12,    340.,  7.33191);
    graph->SetPoint(13,    350.,  6.85379);
    graph->SetPoint(14,    360.,  6.52922);
    graph->SetPoint(15,    370.,  6.23077);
    graph->SetPoint(16,    380.,  5.98355);
    graph->SetPoint(17,    390.,  5.88916);
    graph->SetPoint(18,    400.,  5.8017 );
    graph->SetPoint(19,    420.,  5.64466);
    graph->SetPoint(20,    440.,  5.17429);
    graph->SetPoint(21,    460.,  4.99136);
    graph->SetPoint(22,    480.,  4.93035);
    graph->SetPoint(23,    500.,  4.87645);
    graph->SetPoint(24,    600.,  4.87645);
  }
  if(std::string(type) == std::string("mH-card-observed")){
    //graph->SetPoint( 0,    109.,  0.);
    graph->SetPoint( 0,    110.,  3.03841);
    graph->SetPoint( 1,    130.,  3.1014);
    graph->SetPoint( 2,    140.,  3.3715);
    graph->SetPoint( 3,    160.,  4.4757);
    graph->SetPoint( 4,    180.,  2.5000);
    //graph->SetPoint( 6,    181.,  0.);
  }
  if(std::string(type) == std::string("mh-card-observed")){
    graph->SetPoint( 0,    249.,  100.);
    graph->SetPoint( 1,    350.,  18.9019);
    graph->SetPoint( 2,    400.,  9.95543);
    graph->SetPoint( 3,    420.,  8.78951);
    graph->SetPoint( 4,    440.,  8.11802);
    graph->SetPoint( 5,    460.,  7.60743);
    graph->SetPoint( 6,    480.,  7.20204);
    graph->SetPoint( 7,    500.,  6.87757);
    graph->SetPoint( 8,    600.,  6.87757);
  }
  if(std::string(type) == std::string("mH-card-expected")){
    graph->SetPoint( 0,    109.,  0.);
    graph->SetPoint( 1,    110.,  3.94633);
    graph->SetPoint( 2,    130.,  3.73262);
    graph->SetPoint( 3,    140.,  4.08404);
    graph->SetPoint( 4,    160.,  5.78038);
    graph->SetPoint( 5,    180.,  3.67754);
    graph->SetPoint( 6,    181.,  0.);
  }
  if(std::string(type) == std::string("mh-card-expected")){
    graph->SetPoint( 0,    249.,  100.);
    graph->SetPoint( 1,    350.,  5.22267);
    graph->SetPoint( 2,    400.,  4.5463 );
    graph->SetPoint( 3,    420.,  4.3583);
    graph->SetPoint( 4,    440.,  4.20262);
    graph->SetPoint( 5,    460.,  4.15352);
    graph->SetPoint( 6,    480.,  4.10953);
    graph->SetPoint( 7,    500.,  4.06225);
    graph->SetPoint( 8,    600.,  4.06225);
  }
}

inline void
PlotLimits::limitsHGG(TGraph* graph, const char* type)
{
}

inline void
PlotLimits::xs_mA_tanb1_mhmax_neg400_7TeV(TGraph* graph)
{
graph->SetPoint( 0, 90  ,4.80307   );
graph->SetPoint( 1, 100  ,3.87551   );
graph->SetPoint( 2, 120  ,2.61046   );
graph->SetPoint( 3, 130  ,2.16925   );
graph->SetPoint( 4, 140  ,1.81367   );
graph->SetPoint( 5, 160  ,1.2828   );
graph->SetPoint( 6, 180  ,0.904498   );
graph->SetPoint( 7, 200  ,0.359691   );
graph->SetPoint( 8, 250  ,0.0976372   );
graph->SetPoint( 9, 300  ,0.062742   );
graph->SetPoint( 10, 350  ,0.000472232   );
graph->SetPoint( 11, 400  ,0.000277136   );
graph->SetPoint( 12, 450  ,0.000134055   );
graph->SetPoint( 13, 500  ,6.90396e-05   );
graph->SetPoint( 14, 600  ,2.12344e-05   );
graph->SetPoint( 15, 700  ,7.37143e-06   );
graph->SetPoint( 16, 800  ,2.80665e-06   );
graph->SetPoint( 17, 900  ,1.15955e-06   );
graph->SetPoint( 18, 1000  ,5.14158e-07   );

}

inline void
PlotLimits::xs_mA_tanb5_mhmax_neg400_7TeV(TGraph* graph)
{
graph->SetPoint( 0, 90  ,2.32305   );
graph->SetPoint( 1, 100  ,1.53361   );
graph->SetPoint( 2, 120  ,0.753824   );
graph->SetPoint( 3, 130  ,0.554302   );
graph->SetPoint( 4, 140  ,0.418388   );
graph->SetPoint( 5, 160  ,0.254376   );
graph->SetPoint( 6, 180  ,0.166085   );
graph->SetPoint( 7, 200  ,0.113526   );
graph->SetPoint( 8, 250  ,0.0524249   );
graph->SetPoint( 9, 300  ,0.0319469   );
graph->SetPoint( 10, 350  ,0.00921486   );
graph->SetPoint( 11, 400  ,0.00450532   );
graph->SetPoint( 12, 450  ,0.00200219   );
graph->SetPoint( 13, 500  ,0.00102333   );
graph->SetPoint( 14, 600  ,0.000306398   );
graph->SetPoint( 15, 700  ,7.19243e-05   );
graph->SetPoint( 16, 800  ,2.2862e-05   );
graph->SetPoint( 17, 900  ,8.44571e-06   );
graph->SetPoint( 18, 1000  ,3.50141e-06   );
}

inline void
PlotLimits::xs_mA_tanb20_mhmax_neg400_7TeV(TGraph* graph)
{
graph->SetPoint( 0, 90  ,40.4336   );
graph->SetPoint( 1, 100  ,26.6349   );
graph->SetPoint( 2, 120  ,12.8694   );
graph->SetPoint( 3, 130  ,9.32656   );
graph->SetPoint( 4, 140  ,6.90928   );
graph->SetPoint( 5, 160  ,4.00192   );
graph->SetPoint( 6, 180  ,2.4559   );
graph->SetPoint( 7, 200  ,1.57281   );
graph->SetPoint( 8, 250  ,0.596854   );
graph->SetPoint( 9, 300  ,0.260086   );
graph->SetPoint( 10, 350  ,0.125146   );
graph->SetPoint( 11, 400  ,0.0649239   );
graph->SetPoint( 12, 450  ,0.034977   );
graph->SetPoint( 13, 500  ,0.0199692   );
graph->SetPoint( 14, 600  ,0.00712755   );
graph->SetPoint( 15, 700  ,0.00226592   );
graph->SetPoint( 16, 800  ,0.000870576   );
graph->SetPoint( 17, 900  ,0.000365894   );
graph->SetPoint( 18, 1000  ,0.00016698   );
}

inline void
PlotLimits::xs_mA_tanb50_mhmax_neg400_7TeV(TGraph* graph)
{
graph->SetPoint( 0, 90  ,279.175   );
graph->SetPoint( 1, 100  ,184.21   );
graph->SetPoint( 2, 120  ,89.2618   );
graph->SetPoint( 3, 130  ,64.769   );
graph->SetPoint( 4, 140  ,48.0361   );
graph->SetPoint( 5, 160  ,27.8782   );
graph->SetPoint( 6, 180  ,17.1404   );
graph->SetPoint( 7, 200  ,11.0041   );
graph->SetPoint( 8, 250  ,4.19605   );
graph->SetPoint( 9, 300  ,1.84756   );
graph->SetPoint( 10, 350  ,0.899265   );
graph->SetPoint( 11, 400  ,0.471202   );
graph->SetPoint( 12, 450  ,0.260718   );
graph->SetPoint( 13, 500  ,0.151063   );
graph->SetPoint( 14, 600  ,0.0561115   );
graph->SetPoint( 15, 700  ,0.022326   );
graph->SetPoint( 16, 800  ,0.00971551   );
graph->SetPoint( 17, 900  ,0.00449688   );
graph->SetPoint( 18, 1000  ,0.00219469   );

}

inline void
PlotLimits::xs_mA_tanb70_mhmax_neg400_7TeV(TGraph* graph)
{
graph->SetPoint( 0,  90  ,599.978   );
graph->SetPoint( 1, 100  ,395.818   );
graph->SetPoint( 2, 120  ,191.742   );
graph->SetPoint( 3, 130  ,139.111   );
graph->SetPoint( 4, 140  ,103.157   );
graph->SetPoint( 5, 160  ,59.8538   );
graph->SetPoint( 6, 180  ,36.7901   );
graph->SetPoint( 7, 200  ,23.6164   );
graph->SetPoint( 8, 250  ,9.00233   );
graph->SetPoint( 9, 300  ,3.96518   );
graph->SetPoint( 10, 350  ,1.93059   );
graph->SetPoint( 11, 400  ,1.01199   );
graph->SetPoint( 12, 450  ,0.560808   );
graph->SetPoint( 13, 500  ,0.325159   );
graph->SetPoint( 14, 600  ,0.121105   );
graph->SetPoint( 15, 700  ,0.0493351   );
graph->SetPoint( 16, 800  ,0.0217936   );
graph->SetPoint( 17, 900  ,0.0102215   );
graph->SetPoint( 18, 1000  ,0.00503768   );

}


inline void
PlotLimits::xs_mA_tanb1_mhmax200_7TeV(TGraph* graph)
{
  graph->SetPoint( 0,  90,   5.03737      );
  graph->SetPoint( 1, 100,   4.05932      );
  graph->SetPoint( 2, 120,   2.72635      );
  graph->SetPoint( 3, 130,   2.26197      );
  graph->SetPoint( 4, 140,   1.88807      );
  graph->SetPoint( 5, 160,   0.0850906    );
  graph->SetPoint( 6, 180,   0.049619     );
  graph->SetPoint( 7, 200,   0.0335455    );
  graph->SetPoint( 8, 250,   0.0059505    );
  graph->SetPoint( 9, 300,   0.00304282   );
  graph->SetPoint(10, 350,   0.00043453   ); 
  graph->SetPoint(11, 400,   0.000246734  );
  graph->SetPoint(12, 450,   0.000119678  );
  graph->SetPoint(13, 500,   6.17626e-05  );
  graph->SetPoint(14, 600,   1.82368e-05  );
  graph->SetPoint(15, 700,   6.30971e-06  );  
  graph->SetPoint(16, 800,   2.46535e-06  );
  graph->SetPoint(17, 900,   1.04774e-06  );
  graph->SetPoint(18,1000,   4.74643e-07  );
}

inline void
PlotLimits::xs_mA_tanb5_mhmax200_7TeV(TGraph* graph)
{
  graph->SetPoint( 0,  90,   2.32008      );
  graph->SetPoint( 1, 100,   1.53305      );
  graph->SetPoint( 2, 120,   0.755909     );
  graph->SetPoint( 3, 130,   0.557006     );
  graph->SetPoint( 4, 140,   0.421449     );
  graph->SetPoint( 5, 160,   0.257686     );
  graph->SetPoint( 6, 180,   0.119339     );
  graph->SetPoint( 7, 200,   0.0727759    );
  graph->SetPoint( 8, 250,   0.0204587    );
  graph->SetPoint( 9, 300,   0.00531448   );
  graph->SetPoint(10, 350,   0.00394508   ); 
  graph->SetPoint(11, 400,   0.00178724   );
  graph->SetPoint(12, 450,   0.000840864  );
  graph->SetPoint(13, 500,   0.000421924  );
  graph->SetPoint(14, 600,   0.000107309  );
  graph->SetPoint(15, 700,   3.53824e-056 );  
  graph->SetPoint(16, 800,   1.35272e-05  );
  graph->SetPoint(17, 900,   5.68732e-06  );
  graph->SetPoint(18,1000,   2.5632e-06   );
}

inline void
PlotLimits::xs_mA_tanb20_mhmax200_7TeV(TGraph* graph)
{
  graph->SetPoint( 0,  90,  39.6771      );
  graph->SetPoint( 1, 100,  26.0723      );
  graph->SetPoint( 2, 120,  12.5467      );
  graph->SetPoint( 3, 130,   9.07742     );
  graph->SetPoint( 4, 140,   6.71448     );
  graph->SetPoint( 5, 160,   3.87902     );
  graph->SetPoint( 6, 180,   2.34993     );
  graph->SetPoint( 7, 200,   1.48495     );
  graph->SetPoint( 8, 250,   0.534015    );
  graph->SetPoint( 9, 300,   0.203777    );
  graph->SetPoint(10, 350,   0.0800728   ); 
  graph->SetPoint(11, 400,   0.0401585   );
  graph->SetPoint(12, 450,   0.0207661   );
  graph->SetPoint(13, 500,   0.0111621   );
  graph->SetPoint(14, 600,   0.00335704  );
  graph->SetPoint(15, 700,   0.00123363  );  
  graph->SetPoint(16, 800,   0.000509851 );
  graph->SetPoint(17, 900,   0.000228426 );
  graph->SetPoint(18,1000,   0.000108744 );
}

inline void
PlotLimits::xs_mA_tanb50_mhmax200_7TeV(TGraph* graph)
{
  graph->SetPoint( 0,  90, 256.219       );
  graph->SetPoint( 1, 100, 168.231       );
  graph->SetPoint( 2, 120,  80.8628      );
  graph->SetPoint( 3, 130,  58.4781      );
  graph->SetPoint( 4, 140,  43.2407      );
  graph->SetPoint( 5, 160,  24.967       );
  graph->SetPoint( 6, 180,  15.2534      );
  graph->SetPoint( 7, 200,   9.73877     );
  graph->SetPoint( 8, 250,   3.65872     );
  graph->SetPoint( 9, 300,   1.57715     );
  graph->SetPoint(10, 350,   0.720407    ); 
  graph->SetPoint(11, 400,   0.371131    );
  graph->SetPoint(12, 450,   0.20122     );
  graph->SetPoint(13, 500,   0.113781    );
  graph->SetPoint(14, 600,   0.0394261   );
  graph->SetPoint(15, 700,   0.0155948   );  
  graph->SetPoint(16, 800,   0.0067519   );
  graph->SetPoint(17, 900,   0.00312654  );
  graph->SetPoint(18,1000,   0.00152628  );
}

inline void
PlotLimits::xs_mA_tanb70_mhmax200_7TeV(TGraph* graph)
{
  graph->SetPoint( 0,  90, 516.275       );
  graph->SetPoint( 1, 100, 230.585       );
  graph->SetPoint( 2, 120, 162.234       );
  graph->SetPoint( 3, 130, 117.195       );
  graph->SetPoint( 4, 140,  86.5736      );
  graph->SetPoint( 5, 160,  49.9037      );
  graph->SetPoint( 6, 180,  30.4588      );
  graph->SetPoint( 7, 200,  19.4482      );
  graph->SetPoint( 8, 250,   7.32204     );
  graph->SetPoint( 9, 300,   3.18955     );
  graph->SetPoint(10, 350,   1.48791     ); 
  graph->SetPoint(11, 400,   0.770453    );
  graph->SetPoint(12, 450,   0.42099     );
  graph->SetPoint(13, 500,   0.240205    );
  graph->SetPoint(14, 600,   0.0855247   );
  graph->SetPoint(15, 700,   0.0343697   );  
  graph->SetPoint(16, 800,   0.0150405   );
  graph->SetPoint(17, 900,   0.00701982  );
  graph->SetPoint(18,1000,   0.00344803  );
}

inline void
PlotLimits::xs_mA_tanb1_mhmax800_7TeV(TGraph* graph)
{
graph->SetPoint( 0, 90  ,5.26838   );
graph->SetPoint( 1, 100  ,4.23768   );
graph->SetPoint( 2, 120  ,2.83353   );
graph->SetPoint( 3, 130  ,2.34489   );
graph->SetPoint( 4, 140  ,1.95184   );
graph->SetPoint( 5, 160  ,1.36695   );
graph->SetPoint( 6, 180  ,0.951279   );
graph->SetPoint( 7, 200  ,0.339962   );
graph->SetPoint( 8, 250  ,0.091157   );
graph->SetPoint( 9, 300  ,0.0540866   );
graph->SetPoint( 10, 350  ,0.000475197   );
graph->SetPoint( 11, 400  ,0.000285472   );
graph->SetPoint( 12, 450  ,0.000139443   );
graph->SetPoint( 13, 500  ,7.21663e-05   );
graph->SetPoint( 14, 600  ,2.23476e-05   );
graph->SetPoint( 15, 700  ,7.98852e-06   );
graph->SetPoint( 16, 800  ,3.16665e-06   );
graph->SetPoint( 17, 900  ,1.35749e-06   );
graph->SetPoint( 18, 1000  ,6.15838e-07   );

}

inline void
PlotLimits::xs_mA_tanb5_mhmax800_7TeV(TGraph* graph)
{
graph->SetPoint( 0, 90  ,2.32955   );
graph->SetPoint( 1, 100  ,1.54028   );
graph->SetPoint( 2, 120  ,0.761272   );
graph->SetPoint( 3, 130  ,0.561889   );
graph->SetPoint( 4, 140  ,0.425964   );
graph->SetPoint( 5, 160  ,0.261615   );
graph->SetPoint( 6, 180  ,0.172752   );
graph->SetPoint( 7, 200  ,0.120225   );
graph->SetPoint( 8, 250  ,0.0576789   );
graph->SetPoint( 9, 300  ,0.0373539   );
graph->SetPoint( 10, 350  ,0.00976149   );
graph->SetPoint( 11, 400  ,0.00506873   );
graph->SetPoint( 12, 450  ,0.0024361   );
graph->SetPoint( 13, 500  ,0.00127598   );
graph->SetPoint( 14, 600  ,0.000408693   );
graph->SetPoint( 15, 700  ,0.000150669   );
graph->SetPoint( 16, 800  ,6.12865e-05   );
graph->SetPoint( 17, 900  ,2.68422e-05   );
graph->SetPoint( 18, 1000  ,1.18524e-05   );
}

inline void
PlotLimits::xs_mA_tanb20_mhmax800_7TeV(TGraph* graph)
{
graph->SetPoint( 0, 90  ,41.5584   );
graph->SetPoint( 1, 100  ,27.1783   );
graph->SetPoint( 2, 120  ,12.977   );
graph->SetPoint( 3, 130  ,9.35791   );
graph->SetPoint( 4, 140  ,6.90182   );
graph->SetPoint( 5, 160  ,3.9672   );
graph->SetPoint( 6, 180  ,2.41665   );
graph->SetPoint( 7, 200  ,1.54115   );
graph->SetPoint( 8, 250  ,0.579724   );
graph->SetPoint( 9, 300  ,0.252114   );
graph->SetPoint( 10, 350  ,0.121513   );
graph->SetPoint( 11, 400  ,0.0659882   );
graph->SetPoint( 12, 450  ,0.0362412   );
graph->SetPoint( 13, 500  ,0.0208969   );
graph->SetPoint( 14, 600  ,0.00770634   );
graph->SetPoint( 15, 700  ,0.00315525   );
graph->SetPoint( 16, 800  ,0.00139658   );
graph->SetPoint( 17, 900  ,0.000656724   );
graph->SetPoint( 18, 1000  ,0.000314867   );

}

inline void
PlotLimits::xs_mA_tanb50_mhmax800_7TeV(TGraph* graph)
{
graph->SetPoint( 0, 90  ,356.647   );
graph->SetPoint( 1, 100  ,227.659   );
graph->SetPoint( 2, 120  ,104.658   );
graph->SetPoint( 3, 130  ,74.334   );
graph->SetPoint( 4, 140  ,54.0963   );
graph->SetPoint( 5, 160  ,30.4034   );
graph->SetPoint( 6, 180  ,18.1268   );
graph->SetPoint( 7, 200  ,11.4103   );
graph->SetPoint( 8, 250  ,4.18741   );
graph->SetPoint( 9, 300  ,1.79255   );
graph->SetPoint( 10, 350  ,0.853802   );
graph->SetPoint( 11, 400  ,0.444065   );
graph->SetPoint( 12, 450  ,0.242635   );
graph->SetPoint( 13, 500  ,0.139138   );
graph->SetPoint( 14, 600  ,0.0509553   );
graph->SetPoint( 15, 700  ,0.020774   );
graph->SetPoint( 16, 800  ,0.00916726   );
graph->SetPoint( 17, 900  ,0.00430025   );
graph->SetPoint( 18, 1000  ,0.00210121   );
}

inline void
PlotLimits::xs_mA_tanb70_mhmax800_7TeV(TGraph* graph)
{
graph->SetPoint( 0, 90  ,960.554   );
graph->SetPoint( 1, 100  ,585.653   );
graph->SetPoint( 2, 120  ,252.015   );
graph->SetPoint( 3, 130  ,174.615   );
graph->SetPoint( 4, 140  ,124.429   );
graph->SetPoint( 5, 160  ,67.5959   );
graph->SetPoint( 6, 180  ,39.0852   );
graph->SetPoint( 7, 200  ,24.1445   );
graph->SetPoint( 8, 250  ,8.55757   );
graph->SetPoint( 9, 300  ,3.57701   );
graph->SetPoint( 10, 350  ,1.67373   );
graph->SetPoint( 11, 400  ,0.854872   );
graph->SetPoint( 12, 450  ,0.461855   );
graph->SetPoint( 13, 500  ,0.262287   );
graph->SetPoint( 14, 600  ,0.0945951   );
graph->SetPoint( 15, 700  ,0.0381161   );
graph->SetPoint( 16, 800  ,0.0166618   );
graph->SetPoint( 17, 900  ,0.00775409   );
graph->SetPoint( 18, 1000  ,0.00377436   );
}

inline void
PlotLimits::xs_mA_tanb1_mhmax200_8TeV(TGraph* graph)
{
  graph->SetPoint( 0,  90,   6.29776      );
  graph->SetPoint( 1, 100,   5.10649      );
  graph->SetPoint( 2, 120,   3.4696       );
  graph->SetPoint( 3, 130,   2.89448      );
  graph->SetPoint( 4, 140,   2.42866      );
  graph->SetPoint( 5, 160,   0.110562     );
  graph->SetPoint( 6, 180,   0.065083     );
  graph->SetPoint( 7, 200,   0.0443984    );
  graph->SetPoint( 8, 250,   0.00804336   );
  graph->SetPoint( 9, 300,   0.00419446   );
  graph->SetPoint(10, 350,   0.000610095  ); 
  graph->SetPoint(11, 400,   0.00035264   );
  graph->SetPoint(12, 450,   0.000174092  );
  graph->SetPoint(13, 500,   9.14083e-05  );
  graph->SetPoint(14, 600,   2.79148e-05  );
  graph->SetPoint(15, 700,   9.97944e-06  );  
  graph->SetPoint(16, 800,   4.02823e-06  );
  graph->SetPoint(17, 900,   1.76803e-06  );
  graph->SetPoint(18,1000,   8.27238e-07  );
}

inline void
PlotLimits::xs_mA_tanb5_mhmax200_8TeV(TGraph* graph)
{
  graph->SetPoint( 0,  90,   2.92386      );
  graph->SetPoint( 1, 100,   1.9484       );
  graph->SetPoint( 2, 120,   0.975688     );
  graph->SetPoint( 3, 130,   0.724179     );
  graph->SetPoint( 4, 140,   0.551404     );
  graph->SetPoint( 5, 160,   0.341302     );
  graph->SetPoint( 6, 180,   0.159729     );
  graph->SetPoint( 7, 200,   0.098293     );
  graph->SetPoint( 8, 250,   0.0281775    );
  graph->SetPoint( 9, 300,   0.00743153   );
  graph->SetPoint(10, 350,   0.00556961   ); 
  graph->SetPoint(11, 400,   0.00257001   );
  graph->SetPoint(12, 450,   0.00123146   );
  graph->SetPoint(13, 500,   0.000629016  );
  graph->SetPoint(14, 600,   0.000165679  );
  graph->SetPoint(15, 700,   5.65292e-05  );  
  graph->SetPoint(16, 800,   2.23601e-05  );
  graph->SetPoint(17, 900,   9.72377e-06  );
  graph->SetPoint(18,1000,   4.53274e-06  );
}

inline void
PlotLimits::xs_mA_tanb20_mhmax200_8TeV(TGraph* graph)
{
  graph->SetPoint( 0,  90,  49.836       );
  graph->SetPoint( 1, 100,  33.0219      );
  graph->SetPoint( 2, 120,  16.1375      );
  graph->SetPoint( 3, 130,  11.7591      );
  graph->SetPoint( 4, 140,   8.75759     );
  graph->SetPoint( 5, 160,   5.12514     );
  graph->SetPoint( 6, 180,   3.14237     );
  graph->SetPoint( 7, 200,   2.00832     );
  graph->SetPoint( 8, 250,   0.741488    );
  graph->SetPoint( 9, 300,   0.289943    );
  graph->SetPoint(10, 350,   0.116522    ); 
  graph->SetPoint(11, 400,   0.0596247   );
  graph->SetPoint(12, 450,   0.0314678   );
  graph->SetPoint(13, 500,   0.0172561   );
  graph->SetPoint(14, 600,   0.0053973   );
  graph->SetPoint(15, 700,   0.00206059  );  
  graph->SetPoint(16, 800,   0.000884066 );
  graph->SetPoint(17, 900,   0.000410902 );
  graph->SetPoint(18,1000,   0.000202822 );
}

inline void
PlotLimits::xs_mA_tanb50_mhmax200_8TeV(TGraph* graph)
{
  graph->SetPoint( 0,  90, 321.752       );
  graph->SetPoint( 1, 100, 213.021       );
  graph->SetPoint( 2, 120, 103.972       );
  graph->SetPoint( 3, 130,  75.7267      );
  graph->SetPoint( 4, 140,  56.3766      );
  graph->SetPoint( 5, 160,  32.9719      );
  graph->SetPoint( 6, 180,  20.386       );
  graph->SetPoint( 7, 200,  13.1633      );
  graph->SetPoint( 8, 250,   5.07616     );
  graph->SetPoint( 9, 300,   2.2417      );
  graph->SetPoint(10, 350,   1.04757     ); 
  graph->SetPoint(11, 400,   0.55137     );
  graph->SetPoint(12, 450,   0.305267    );
  graph->SetPoint(13, 500,   0.176171    );
  graph->SetPoint(14, 600,   0.0635114   );
  graph->SetPoint(15, 700,   0.0261058   );  
  graph->SetPoint(16, 800,   0.0117348   );
  graph->SetPoint(17, 900,   0.00563758  );
  graph->SetPoint(18,1000,   0.00285359  );
}

inline void
PlotLimits::xs_mA_tanb70_mhmax200_8TeV(TGraph* graph)
{
  graph->SetPoint( 0,  90, 648.309       );
  graph->SetPoint( 1, 100, 428.512       );
  graph->SetPoint( 2, 120, 208.592       );
  graph->SetPoint( 3, 130, 151.757       );
  graph->SetPoint( 4, 140, 112.869       );
  graph->SetPoint( 5, 160,  65.9007      );
  graph->SetPoint( 6, 180,  40.7057      );
  graph->SetPoint( 7, 200,  26.2853      );
  graph->SetPoint( 8, 250,  10.1578      );
  graph->SetPoint( 9, 300,   4.53294     );
  graph->SetPoint(10, 350,   2.16329     ); 
  graph->SetPoint(11, 400,   1.1446      );
  graph->SetPoint(12, 450,   0.6387      );
  graph->SetPoint(13, 500,   0.371947    );
  graph->SetPoint(14, 600,   0.137788    );
  graph->SetPoint(15, 700,   0.0575433   );  
  graph->SetPoint(16, 800,   0.0261445   );
  graph->SetPoint(17, 900,   0.0126598   );
  graph->SetPoint(18,1000,   0.00644764  );
}

inline void
PlotLimits::xs_mA_tanb1_nomix200_7TeV(TGraph* graph)
{
  graph->SetPoint( 0,  90,   1.8          ); //number interpolated
  graph->SetPoint( 1, 100,   0.777065     );
  graph->SetPoint( 2, 120,   0.570059     );
  graph->SetPoint( 3, 130,   0.432182     );
  graph->SetPoint( 4, 140,   0.337103     );
  graph->SetPoint( 5, 160,   0.219854     );
  graph->SetPoint( 6, 180,   0.0870783    );
  graph->SetPoint( 7, 200,   0.0546187    );
  graph->SetPoint( 8, 250,   0.0157798    );
  graph->SetPoint( 9, 300,   0.00431867   );
  graph->SetPoint(10, 350,   0.00310969   ); 
  graph->SetPoint(11, 400,   0.00141805   );
  graph->SetPoint(12, 450,   0.000661938  );
  graph->SetPoint(13, 500,   0.000331838  );
  graph->SetPoint(14, 600,   8.50743e-05  );
  graph->SetPoint(15, 700,   2.79244e-05  );  
  graph->SetPoint(16, 800,   1.06313e-05  );
  graph->SetPoint(17, 900,   4.4507e-06   );
  graph->SetPoint(18,1000,   1.99744e-06  );
}

inline void
PlotLimits::xs_mA_tanb5_nomix200_7TeV(TGraph* graph)
{
  graph->SetPoint( 0,  90,   2.32335      ); //number interpolated
  graph->SetPoint( 1, 100,   1.53421      );
  graph->SetPoint( 2, 120,   0.755294     );
  graph->SetPoint( 3, 130,   0.556054     );
  graph->SetPoint( 4, 140,   0.420324     );
  graph->SetPoint( 5, 160,   0.256454     );
  graph->SetPoint( 6, 180,   0.118953     );
  graph->SetPoint( 7, 200,   0.0724268    );
  graph->SetPoint( 8, 250,   0.0202821    );
  graph->SetPoint( 9, 300,   0.00526867   );
  graph->SetPoint(10, 350,   0.00389071   ); 
  graph->SetPoint(11, 400,   0.00176561   );
  graph->SetPoint(12, 450,   0.000830987  );
  graph->SetPoint(13, 500,   0.000416989  );
  graph->SetPoint(14, 600,   0.000106047  );
  graph->SetPoint(15, 700,   3.49724e-05  );  
  graph->SetPoint(16, 800,   1.33739e-05  );
  graph->SetPoint(17, 900,   5.62468e-06  );
  graph->SetPoint(18,1000,   2.53594e-06  );
}

inline void
PlotLimits::xs_mA_tanb20_nomix200_7TeV(TGraph* graph)
{
  graph->SetPoint( 0,  90,  39.9296      );
  graph->SetPoint( 1, 100,  26.2436      );
  graph->SetPoint( 2, 120,  12.6331      );
  graph->SetPoint( 3, 130,   9.14097     );
  graph->SetPoint( 4, 140,   6.76233     );
  graph->SetPoint( 5, 160,   3.90732     );
  graph->SetPoint( 6, 180,   2.36931     );
  graph->SetPoint( 7, 200,   1.49863     );
  graph->SetPoint( 8, 250,   0.540856    );
  graph->SetPoint( 9, 300,   0.208179    );
  graph->SetPoint(10, 350,   0.0826232   ); 
  graph->SetPoint(11, 400,   0.0415116   );
  graph->SetPoint(12, 450,   0.0215237   );
  graph->SetPoint(13, 500,   0.0116003   );
  graph->SetPoint(14, 600,   0.00351274  );
  graph->SetPoint(15, 700,   0.00129491  );  
  graph->SetPoint(16, 800,   0.000536177 );
  graph->SetPoint(17, 900,   0.000240537 );
  graph->SetPoint(18,1000,   0.000114627 );
}

inline void
PlotLimits::xs_mA_tanb50_nomix200_7TeV(TGraph* graph)
{
  graph->SetPoint( 0,  90, 256.262       );
  graph->SetPoint( 1, 100, 168.474       );
  graph->SetPoint( 2, 120,  81.15        );
  graph->SetPoint( 3, 130,  58.7365      );
  graph->SetPoint( 4, 140,  43.4647      );
  graph->SetPoint( 5, 160,  25.1287      );
  graph->SetPoint( 6, 180,  15.3756      );
  graph->SetPoint( 7, 200,   9.82855     );
  graph->SetPoint( 8, 250,   3.70346     );
  graph->SetPoint( 9, 300,   1.60293     );
  graph->SetPoint(10, 350,   0.740298    ); 
  graph->SetPoint(11, 400,   0.382646    );
  graph->SetPoint(12, 450,   0.208256    );
  graph->SetPoint(13, 500,   0.118237    );
  graph->SetPoint(14, 600,   0.0414199   );
  graph->SetPoint(15, 700,   0.0164817   );  
  graph->SetPoint(16, 800,   0.00716251  );
  graph->SetPoint(17, 900,   0.00332492  );
  graph->SetPoint(18,1000,   0.00162586  );
}

inline void
PlotLimits::xs_mA_tanb70_nomix200_7TeV(TGraph* graph)
{
  graph->SetPoint( 0,  90, 509.157       );
  graph->SetPoint( 1, 100, 228.45        );
  graph->SetPoint( 2, 120, 161.029       );
  graph->SetPoint( 3, 130, 116.516       );
  graph->SetPoint( 4, 140,  86.1967      );
  graph->SetPoint( 5, 160,  49.8097      );
  graph->SetPoint( 6, 180,  30.4804      );
  graph->SetPoint( 7, 200,  19.4975      );
  graph->SetPoint( 8, 250,   7.3701      );
  graph->SetPoint( 9, 300,   3.22151     );
  graph->SetPoint(10, 350,   1.51899     ); 
  graph->SetPoint(11, 400,   0.789342    );
  graph->SetPoint(12, 450,   0.432966    );
  graph->SetPoint(13, 500,   0.248024    );
  graph->SetPoint(14, 600,   0.0892303   );
  graph->SetPoint(15, 700,   0.0360703   );  
  graph->SetPoint(16, 800,   0.0158435   );
  graph->SetPoint(17, 900,   0.00741254  );
  graph->SetPoint(18,1000,   0.00364665  );
}
#endif
