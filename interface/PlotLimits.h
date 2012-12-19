#ifndef PlotLimits_h
#define PlotLimits_h

#include <map>
#include <math.h>
#include <vector>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <algorithm>

#include "TH2F.h"
#include "TROOT.h"
#include "TMath.h"
#include "TTree.h"
#include "TFile.h"
#include "TAxis.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TPaveText.h"
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
   all mass points as sub-directories. In the sub-directories the limits ouptut files from combine
   are looked for. This structure can be achieved automatically when using the other (wrapper) tools
   for limit calculation provided in the same package (i.e. limit.py and auxiliary tools for this 
   tool). Pre-defined layout files can be found in the python/layout sub-directory of this package.

   Depending on the layout the class provides plots for SM limits (on signal strength), on the MSSM
   cross section (in pb) or on the MSSM parameter tanb. Unless configured otherwise the output consists 
   of:

    - a plot in png format
    - a plot in eps format
    - a plot in pdf format
    - a txt file containing the observed and expected limit and the uncertainty bands
    - a tex file containing the observed and expected limit and the uncertainty bands
    - a root output file containing the observed and expected limit and uncertainty bands in TGraph 
      format.

    in the directory in which the tool plot has been executed. The names of the png/pdf/txt/tex output
    files will be derived from the laypout and from the input directory. The output in the
    root file will be updated in case a file with similar name is already present in the directory 
    where the tool plot has been executed or the file will be created otherwise. In the root file 
    the limits for a given input directory will be safed in a directory corresponding to the name of 
    the input directory. The file is suited for further processing with the macro compareLimits.C in 
    the macros directory of the same package. For more details on how to run the tool plot have a look 
    in the bin dorectory of this package or just execute the tool w/o any aditional arguments given.
*/

class PlotLimits {

 public:
  /// constructor from cfg file
  PlotLimits(const char* output, const edm::ParameterSet& cfg);
  /// default destructor
  ~PlotLimits() {};

  /// fill the central value either for observed or expected
  TGraph* fillCentral(const char* directory, TGraph* plot, const char* filename);
  /// fill the +/-1sigma and +/-2sigma uncertainty band
  TGraphAsymmErrors* fillBand(const char* directory, TGraphAsymmErrors* plot, const char* method, bool innerBand);
  /// print tabulated limits to a txt file, for inner band, outer band, expected and observed, w/o inner and outer band
  void print(const char* filename, TGraph* expected, TGraph* observed, const char* type="txt");
  /// print tabulated limits to a txt file, for inner band, outer band, expected and observed, with inner and outer band
  void print(const char* filename, TGraphAsymmErrors* outerBand, TGraphAsymmErrors* innerBand, TGraph* expected, TGraph* observed, const char* type="txt");
  /// print tabulated limits to a txt file, for inner band, outer band, expected and observed, with inner and outer band
  void print(const char* filename, std::string& xval, std::string& yval, TGraph* contour, const char* type="txt");
  /// automatic maximum determination for TGraphs (used for several options)
  float maximum(TGraph* graph); 
  /// make a fillable TGraph out of a non-fillable TGraph that comes out of a contour plot (used for option scan2D)
  TGraph* convexGraph(TGraph* graph);
  /// print 1d uncertainties for a given CL to file (used by scan-2d)
  void band1D(ostream& out, std::string& xval, std::string& yval, TGraph* bestFit, TGraph* band, float xoffset, float yoffset, std::string CL);
  /// fill a graph for the contraints of the H(125) resonance in the mA-tanb exclusion plane (used for option tanb)
  TGraphAsymmErrors* higgsConstraint(const char* directory, double mass=125., double deltaM=1.);
  /// plot limits on canvas, print out png, pdf, txt, root formats if desired
  void plotLimit(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed=0);
  /// plot limits for tanb on canvas, print out png, pdf, txt, root formats if desired
  void plotTanb(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed=0, const char* directory="");
  /// plot bestfit values for different parameters dependend on mass on canvas, print out png, pdf, txt, root formats if desired 
  void plotSignalStrength(TCanvas& canv, TGraphAsymmErrors* innerBand, TGraph* central, const char* directory="");
  /// plot significance on canvas, print out png, pdf, txt, root formats if desired  
  void plotSignificance(TCanvas& canv, TGraph* expected, TGraph* observed=0);
  /// plot 2d-scans for several masses on canvases, print out png, pdf, txt, root formats if desired  
  void plot2DScan(TCanvas& canv, const char* directory="");

 private:
  /// fill a single vector of values according to 2sigma, 1sigma, median and observed from asymptotic limits
  void prepareAsymptotic(const char* directory, std::vector<double>& values, const char* type);
  /// fill a single vector of values according to 2sigma, 1sigma, mean or median from bayesian limits; in case files do not 
  /// exists or were corrupted for a given mass point the initial value of -1. will be filled, the member functions fillCentral
  /// and fillBand should check for values of -1. and take these mass points out of consideration.
  void prepareBayesian(const char* directory, std::vector<double>& values, const char* type);
  /// fill a single vector of values according to 2sigma, 1sigma or median from CLs limits;
  void prepareCLs(const char* directory, std::vector<double>& values, const char* type) {
    prepareSimple(directory, values, std::string("higgsCombineTest.HybridNew.$MASS").append(type).c_str());
  };
  /// fill a single vector of values according to 1sigma from the simple maximum likelihood fit of combine
  void prepareMaxLikelihood(const char* directory, std::vector<double>& values, const char* filename, float ConLevel);
  /// fill a single vector of values from a file filename. In case files do not exists or were corrupted for a given mass point 
  /// the initial value of -1. will be filled, the member functions fillCentral and fillBand should check for values of -1. and
  /// take these mass points out of consideration.
  void prepareSimple(const char* directory, std::vector<double>& values, const char* filename);
  /// fill officially approved limits for HIG-11-020 (NOTE: these are cross section limits also for MSSM)
  void prepareHIG_11_020(std::vector<double>& values, const char* type, bool xsec, double mass, bool initial);
  /// fill officially approved limits for HIG-11-029 (NOTE: these are direct limits on tanb for MSSM)
  void prepareHIG_11_029(std::vector<double>& values, const char* type, double mass, bool initial);
  /// fill officially approved limits for HIG-12-018 / HIG-12-028 (NOTE: these are only SM limits)
  void prepareHIG_12_018(std::vector<double>& values, const char* type, double mass, bool initial);
  /// fill officially approved limits for HIG-12-032 (NOTE: these are only SM limits)
  void prepareHIG_12_032(std::vector<double>& values, const char* type, double mass, bool initial);
  /// fill officially approved limits for HIG-12-043 (NOTE: these are only SM limits)
  void prepareHIG_12_043(std::vector<double>& values, const char* type, double mass, bool initial);
  /// fill officially approved limits for HIG-12-050 (NOTE: these are only MSSM limits)
  void prepareHIG_12_050(std::vector<double>& values, const char* type, double mass, bool initial);

  /*
    Limits for comparison
  */
  /// fill the LEP exclusion plot
  void upperLEPLimits(TGraph* graph);
  /// fill the LEP exclusion plot (low tanb free space)
  void lowerLEPLimits(TGraph* graph); 

 private:
  /// output name (will be used to derived directory name in root files)
  std::string output_;
  /// string for CMS preliminary stamp on officla plots
  std::string dataset_;
  /// string for x-axis title
  std::string xaxis_;
  /// string for y-axis title
  std::string yaxis_;
  /// minimum on y axis for plotting
  double min_;
  /// maximum on y axis for plotting
  double max_;
  /// log scale for plotting (depending on option can be on y axis on z axis)
  int log_;
  /// print out png format
  bool png_;
  /// print out pdf and eps format
  bool pdf_;
  /// print out txt format
  bool txt_;
  /// print out root format
  bool root_;
  /// additional output label for png, pdf, txt
  std::string label_;
  /// define verbosity level
  unsigned int verbosity_;

  /// indicate whether mssm or sm plots should be made (used fro several options)
  bool mssm_;
  /// indicate whether this is with signal injected or not (used for limit plotting)
  bool injected_;
  /// indicate whether the +/- 2 sigma should be shown or not (used for option tanb)
  bool outerband_;
  /// print constraint on mA-tanb plane from Higgs boson at 125 GeV? (used for option tanb)
  bool higgs125_;
  /// indicate signal component for signal strength plot from 2d-scan or fit (used for option max-likelihood)
  std::string signal_;
  /// indicate physics model (used for option scan-2d)
  std::string model_;
  /// indicate whether to make a temperatiure plot or not (used for option scan-2d)
  bool temp_;
  /// minimum for plotting as function of mass (used for option scan-2d)
  std::map<double,double> xmins_, ymins_;
  /// maximum for plotting as function of mass (used for option scan-2d)
  std::map<double,double> xmaxs_, ymaxs_;

  /// binning for limits
  std::vector<double> bins_;
  /// check whether mass point is available or not
  std::vector<bool> valid_;
  /// mass for which a limit has been calculated (needed for plotting of HIG-XX-YYY results)
  std::vector<double> masses_;
};

/// official limits from HIG-11-020
#include "HiggsAnalysis/HiggsToTauTau/interface/HIG-11-020.h"
/// official limits from HIG-11-029
#include "HiggsAnalysis/HiggsToTauTau/interface/HIG-11-029.h"
/// official limits from HIG-12-018
#include "HiggsAnalysis/HiggsToTauTau/interface/HIG-12-018.h"
/// official limits from HIG-12-032
#include "HiggsAnalysis/HiggsToTauTau/interface/HIG-12-032.h"
/// official limits from HIG-12-043
#include "HiggsAnalysis/HiggsToTauTau/interface/HIG-12-043.h"
/// official limits from HIG-12-050
#include "HiggsAnalysis/HiggsToTauTau/interface/HIG-12-050.h"

inline void
PlotLimits::upperLEPLimits(TGraph* graph)
{
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
PlotLimits::lowerLEPLimits(TGraph* graph)
{
  graph->SetPoint( 0, 246.4   ,   0     );
  graph->SetPoint( 1, 243.3   ,   0.2   );
  graph->SetPoint( 2, 241     ,   0.3   );
  graph->SetPoint( 3, 240     ,   0.45  );
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

#endif
