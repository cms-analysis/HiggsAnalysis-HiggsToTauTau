#include <vector>

#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"
#include "FWCore/PythonParameterSet/interface/MakeParameterSets.h"

void help()
{
  std::cout << "description: executable to make official Higgs2Tau plots." << std::endl;
  return;
}

int main(int argc, char* argv[]) 
{
  std::vector<std::string> types;
  types.push_back(std::string("CLs"));
  types.push_back(std::string("tanb"));
  types.push_back(std::string("bayesian"));
  types.push_back(std::string("asymptotic"));
  types.push_back(std::string("HIG-11-020"));
  types.push_back(std::string("HIG-11-029"));
  types.push_back(std::string("significance"));

  // parse arguments
  if ( argc < 3 ) {
    std::cout << "Usage : " << argv[0] << " [limit-type] [layout.py] [target-dir]" << std::endl;
    return 0;
  }
  if( std::find(types.begin(), types.end(), std::string(argv[1])) == types.end() ){
    std::cout << " Error: The specified limit type (" << argv[1] << ")"
	      << " is not supported. Available limit types are:" << std::endl;
    for( std::vector<std::string>::const_iterator type = types.begin(); type!=types.end(); ++type ){
      std::cout << "  - " << *type << std::endl;
    }
    exit(0);
  }
  if( !edm::readPSetsFrom(argv[2])->existsAs<edm::ParameterSet>("layout") ){
    std::cout << " Error: ParameterSet 'layout' is missing in your configuration file" << std::endl; exit(0);
  }
  bool mssm = edm::readPSetsFrom(argv[2])->getParameter<edm::ParameterSet>("layout").getParameter<bool>("mssm");

  /// get intput directory up to one before mass points
  const char* directory ((std::string(argv[1]).find("HIG")==std::string::npos) ? argv[3] : argv[1]);
  /// chop off the prepended directories if needed for out
  std::string out(std::string(directory).substr(std::string(directory).rfind("/")+1));
  PlotLimits plot(out.c_str(), edm::readPSetsFrom(argv[2])->getParameter<edm::ParameterSet>("layout"));

  /*
    Implementations
  */

  if( std::string(argv[1]) == std::string("CLs") ){
    /*
    Plotting of CLs type limits 
    */
    /// observed limit 
    TGraph* observed  = new TGraph();
    plot.fillCentral(directory, observed, "higgsCombineTest.HybridNew.$MASS");
    /// expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral(directory, expected, "higgsCombineTest.HybridNew.$MASS.quant0.500");
    /// 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand(directory, outer, "CLs", false);
    /// 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand(directory, inner, "CLs", true);
    /// make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plot(*canv, inner, outer, expected, observed);
  }
  if( std::string(argv[1]) == std::string("tanb") ){
    /*
      Plotting of CLs or asymptotic limits in tanb style
    */
    /// observed limit 
    TGraph* observed  = new TGraph();
    plot.fillCentral(directory, observed, "higgsCombineTest.HybridNew.$MASS");
    /// expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral(directory, expected, "higgsCombineTest.HybridNew.$MASS.quant0.500");
    /// 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand(directory, outer, "CLs", false);
    /// 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand(directory, inner, "CLs", true);
    /// make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotTanb(*canv, inner, outer, expected, observed);
  }
  if( std::string(argv[1]) == std::string("bayesian") ){
    /// observed limit 
    TGraph* observed  = new TGraph();
    plot.fillCentral(directory, observed, "higgsCombineTest.MarkovChainMC.$MASS");
    /// expected limit (for Bayesian 'median' and 'mean' are sensible parameters)
    TGraph* expected  = new TGraph();
    plot.fillCentral(directory, expected, "median");
    /// 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand(directory, inner, "Bayesian", true);
    /// 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand(directory, outer, "Bayesian", false);
    /// make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plot(*canv, inner, outer, expected, observed);
  }
  if( std::string(argv[1]) == std::string("significance") ){
    /// observed limit (remains empty for this execise)
    //TGraph* observed  = new TGraph();
    /// expected limit (for Bayesian 'median' and 'mean' are sensible parameters)
    TGraph* expected  = new TGraph();
    plot.fillCentral(directory, expected, "median");
    /// 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand(directory, inner, "Bayesian", true);
    /// 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand(directory, outer, "Bayesian", false);
    /// make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plot(*canv, inner, outer, expected);
  }
  if( std::string(argv[1]) == std::string("asymptotic") ){
    /// expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral(directory, expected, "asym-expected");
    /// 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand(directory, inner, "Asymptotic", true);
    /// 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand(directory, outer, "Asymptotic", false);
    /// observed limit 
    TGraph* observed  = new TGraph();
    plot.fillCentral(directory, observed, "asym-observed");
    /// make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plot(*canv, inner, outer, expected, observed);
    //plot.plot(*canv, inner, outer, expected);
  }
  if( std::string(argv[1]) == std::string("HIG-11-020") ){
    /// observed limit 
    TGraph* observed  = new TGraph();
    plot.fillCentral("HIG-11-020", observed, "HIG-11-020-observed");
    /// expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral("HIG-11-020", expected, "HIG-11-020-expected");
    /// 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand("HIG-11-020", inner, "HIG-11-020", true);
    /// 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand("HIG-11-020", outer, "HIG-11-020", false);
    /// make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    //plot.plot(*canv, inner, outer, expected, observed);  
    plot.plotTanb(*canv, inner, outer, expected, observed);  
  }
  if( std::string(argv[1]) == std::string("HIG-11-029") ){
    /// observed limit 
    TGraph* observed  = new TGraph();
    plot.fillCentral("HIG-11-029", observed, "HIG-11-029-observed");
    /// expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral("HIG-11-029", expected, "HIG-11-029-expected");
    /// 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand("HIG-11-029", inner, "HIG-11-029", true);
    /// 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand("winter11", outer, "HIG-11-029", false);
    /// make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    if(mssm){
      plot.plotTanb(*canv, inner, outer, expected, observed);
    }
    else{
      plot.plot(*canv, inner, outer, expected, observed);
    }
  }
  return 0;
}
