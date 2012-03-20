#ifndef FeynHiggsScan_h
#define FeynHiggsScan_h

#include <map>
#include <string>
#include <utility>
#include <iostream>

#include "TH1F.h"
#include "TH2F.h"
#include "TFile.h"
#include "TTree.h"
#include "TStyle.h"
#include "TString.h"
#include "TCanvas.h"

/**
   \class   FeynHiggsScan FeynHiggsScan.h "HiggsAnalysis/HiggsToTauTau/interface/FeynHiggsScan.h"

   \brief   Class to return pre-calculated values for cross sections and branching ratios from FeynHiggs

   To follow soon 
*/

class FeynHiggsScan {

 public:
  /// default constructor
  FeynHiggsScan(const char* fileName, const char* treeName, unsigned int n_tanb, double offset_tanb, double step_tanb, unsigned int n_mA, double offset_mA, double step_mA);
  /// default destructor
  ~FeynHiggsScan();

  /// get cross section ot br from tree for given value of mA and tanb
  float get(const char* variable, const char* model, const char* type, float mA, float tanb);
  /// production cross section for mH for given mA and tanb 
  float xsec(const char* variable, const char* model, double mA, double tanb) {return get(variable, model, "xs", mA, tanb); };
  /// production cross section for mH for given mA and tanb 
  float br(const char* variable, const char* model, double mA, double tanb) {return get(variable, model, "br", mA, tanb); };

 private:
  /// book branches for all variables or a subset of them
  void book(const std::string& var);
  /// set branch addresses for all variables or a subset of them 
  void read(const std::string& var);
  /// loop tree project the information of interest out and return int in form of a 2d histogram
  TH2F* project(const std::string& var);
  
 private:
  /// verbosity level
  bool verbose_;
  /// min and max of tanb scan
  double minTanb_, maxTanb_, stepTanb_;
  /// min and max of mA scan
  double minMA_, maxMA_, stepMA_;
  /// input file containing cross section and BR information
  TFile* file_;
  /// input tree containing cross section and BR information
  TTree* tree_;
  /// 2d projection of the information of interst 
  TH2F* hproject_;
  /// 2d conrtrol plot to make sure that the scan went OK
  TH2F* hscan_;

  /// input parameters 
  float tanb_, mA_, var_;
};

#endif
