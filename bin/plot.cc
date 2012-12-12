#include <vector>
#include <sstream>

#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"
#include "FWCore/PythonParameterSet/interface/MakeParameterSets.h"

void help()
{
  std::cout << "description: executable to make official Higgs2Tau plots." << std::endl;
  return;
}


// http://www.cplusplus.com/articles/D9j2Nwbp/
template <typename T> T StringToNumber (const std::string& Text) {
  std::istringstream ss(Text);
  T result;
  ss >> result;
  return result;
}

// Add a parameter to parameterset, in a string key=value format.
void addParameter(edm::ParameterSet& pset, const std::string& key, const std::string& value) {
  std::cout << "Updating parameter " << key << " to " << value << " in layout." << std::endl;
  if (pset.existsAs<int>(key))
    pset.addParameter<int>(key, StringToNumber<int>(value));
  else if (pset.existsAs<unsigned int>(key))
    pset.addParameter<unsigned int>(key, StringToNumber<unsigned int>(value));
  else if (pset.existsAs<bool>(key))
    // We use 0 or 1 for bool
    pset.addParameter<unsigned int>(key, StringToNumber<unsigned int>(value));
  else if (pset.existsAs<double>(key))
    // We use 0 or 1 for bool
    pset.addParameter<double>(key, StringToNumber<double>(value));
  else if (pset.existsAs<std::string>(key))
    pset.addParameter<std::string>(key, StringToNumber<std::string>(value));
  else {
    std::cout << "Adding new parameter " << key << " to layout."  << std::endl;
    pset.addParameter<std::string>(key, StringToNumber<std::string>(value));
  }
}

int main(int argc, char* argv[])
{
  std::vector<std::string> types;
  /// show full CLs cross section limits 
  types.push_back(std::string("CLs"));
  /// show limits in mA-tanb (from full CLs or from asymptotic)
  types.push_back(std::string("tanb"));
  /// show bayesian cross section limits
  types.push_back(std::string("bayesian"));
  /// show asymptotic cross section limits with signal injected
  types.push_back(std::string("injected"));
  /// show asymptotic cross section (times BR) limits
  types.push_back(std::string("asymptotic"));
  /// show limits as of HIG-11-020
  types.push_back(std::string("HIG-11-020"));
  /// show limits as of HIG-11-029
  types.push_back(std::string("HIG-11-029"));
  /// show limits as of HIG-12-018
  types.push_back(std::string("HIG-12-018"));
  /// show limits as of HIG-12-032
  types.push_back(std::string("HIG-12-032"));
  /// show limits as of HIG-12-043
  types.push_back(std::string("HIG-12-043"));
  /// show limits as of HIG-12-050
  types.push_back(std::string("HIG-12-050"));
  /// show significances with bands (run with toys)
  types.push_back(std::string("significance"));
  /// show signal strength as function of mH/mA as determined from a 1d maxlikelihood fit 
  types.push_back(std::string("maxlikelihood-fit"));
  /// show signal strength as function of mH/mA as determined from a 2d maxlikelihood fit 
  types.push_back(std::string("multidim-fit"));
  /// show 2D scans (still in developement)
  types.push_back(std::string("scan-2D"));

  // parse arguments
  if ( argc < 3 ) {
    std::cout << "Usage : " << argv[0] << " [limit-type] [layout.py] [target-dir] [option1=value1 [option2=value2]]" << std::endl;
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
  edm::ParameterSet layout =  edm::readPSetsFrom(argv[2])->getParameterSet("layout");

  // Update layout with overridden options
  if (argc > 4) {
    for (int i = 4; i < argc; ++i) {
      std::string argument(argv[i]);
      size_t equals_pos = argument.find("=");
      if (equals_pos == std::string::npos) {
        std::cerr << "I don't understand the layout override: " << argument <<
          " The format should be key=value" << std::endl;
        exit(1);
      }
      std::string key = argument.substr(0, equals_pos);
      std::string value = argument.substr(equals_pos+1, argument.length() - equals_pos+1);
      addParameter(layout, key, value);
    }
  }

  bool mssm = layout.getParameter<bool>("mssm");
  bool significance = layout.existsAs<bool>("significance") ? layout.getParameter<bool>("significance") : false;
  bool expected_only = layout.existsAs<bool>("expectedOnly") ? layout.getParameter<bool>("expectedOnly") : false;

  /// get intput directory up to one before mass points
  const char* directory ((std::string(argv[1]).find("HIG")==std::string::npos) ? argv[3] : argv[1]);
  std::string directory_string(directory);
  /// chop off the prepended directories if needed for out
  if(directory_string.rfind("/")+1 == directory_string.length()){
    directory_string = directory_string.substr(0, directory_string.rfind("/"));
  }
  std::string out(directory_string.substr(directory_string.rfind("/")+1));
  PlotLimits plot(out.c_str(), layout);

  /*
    Implementations (as dirty hardcoded list)
  */

  if( std::string(argv[1]) == std::string("CLs") ){
    /*
    Plotting of CLs type limits
    */
    /// observed limit
    TGraph* observed  = 0;
    if(!expected_only){
      observed = new TGraph();
      plot.fillCentral(directory, observed, "higgsCombineTest.HybridNew.$MASS");
    }
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
    TGraph* observed  = 0;
    if(!expected_only){
      observed = new TGraph();
      plot.fillCentral(directory, observed, "higgsCombineTest.HybridNew.$MASS");
    }
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
    plot.plotTanb(*canv, inner, outer, expected, observed, directory);
  }
  if( std::string(argv[1]) == std::string("bayesian") ){
    /// observed limit
    TGraph* observed  = 0;
    if(!expected_only){
      observed = new TGraph();
      plot.fillCentral(directory, observed, "higgsCombineTest.MarkovChainMC.$MASS");
    }
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
  if( std::string(argv[1]) == std::string("injected") ){
    /// observed limit
    TGraph* observed  = 0;
    if(!expected_only){
      observed = new TGraph();
      plot.fillCentral(directory, observed, "higgsCombine-obs.Asymptotic.$MASS");
    }
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
    /// observed limit
    TGraph* observed  = 0;
    if(!expected_only){
      observed = new TGraph();
      plot.fillCentral(directory, observed, "higgsCombineTest.ProfileLikelihood.$MASS");
    }
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
    if(significance){
      //plot.plot(*canv, inner, outer, expected, observed);
      plot.plotSignificance(*canv, expected, observed);
    }
    else{
      plot.plot(*canv, inner, outer, expected, observed);
    }
  }
  if( std::string(argv[1]) == std::string("asymptotic") ){
    /// observed limit
    TGraph* observed  = 0;
    if(!expected_only){
      observed = new TGraph();
      plot.fillCentral(directory, observed, "asym-observed");
    }
    /// expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral(directory, expected, "asym-expected");
    /// 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand(directory, inner, "Asymptotic", true);
    /// 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand(directory, outer, "Asymptotic", false);
    /// make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plot(*canv, inner, outer, expected, observed);
  }
  if( std::string(argv[1]) == std::string("maxlikelihood-fit") ){
    /// expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral(directory, expected, "higgsCombineTest.MaxLikelihoodFit.$MASS");
    /// 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand(directory, inner, "higgsCombineTest.MaxLikelihoodFit.$MASS", true);
    /// make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plot(*canv, inner, 0, expected, 0);
  }
  if( std::string(argv[1]) == std::string("multidim-fit") ){
    /// best fit
    TGraph* expected  = new TGraph();
    /// +/- 1 sigma to bestfit
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    /// make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotMDF(*canv, inner, 0, expected, 0, directory);
  }

  /// $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
  if( std::string(argv[1]) == std::string("scan-2D") ){
    /// make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plot2DScan(*canv, directory);
  }
  /// $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

  if( std::string(argv[1]) == std::string("HIG-11-020") ){
    /// observed limit
    TGraph* observed  = 0;
    if(!expected_only){
      observed = new TGraph();
      plot.fillCentral("HIG-11-020", observed, "HIG-11-020-observed");
    }
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
    /*
      plots the layout corresponding to cross sectino limits
    */
    //plot.plot(*canv, inner, outer, expected, observed);
    /*
      plots the layout corresponding to the direct tanb limits
    */
    plot.plotTanb(*canv, inner, outer, expected, observed);
  }
  if( std::string(argv[1]) == std::string("HIG-11-029") ){
    /// observed limit
    TGraph* observed  = 0;
    if(!expected_only){
      observed = new TGraph();
      plot.fillCentral("HIG-11-029", observed, "HIG-11-029-observed");
    }
    /// expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral("HIG-11-029", expected, "HIG-11-029-expected");
    /// 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand("HIG-11-029", inner, "HIG-11-029", true);
    /// 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand("HIG-11-029", outer, "HIG-11-029", false);
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
  if( std::string(argv[1]) == std::string("HIG-12-018") ){
    /// observed limit
    TGraph* observed  = 0;
    if(!expected_only){
      observed = new TGraph();
      plot.fillCentral("HIG-12-018", observed, "HIG-12-018-observed");
    }
    /// expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral("HIG-12-018", expected, "HIG-12-018-expected");
    /// 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand("HIG-12-018", inner, "HIG-12-018", true);
    /// 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand("HIG-12-018", outer, "HIG-12-018", false);
    /// make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plot(*canv, inner, outer, expected, observed);
  }
  if( std::string(argv[1]) == std::string("HIG-12-032") ){
    /// observed limit
    TGraph* observed  = 0;
    if(!expected_only){
      observed = new TGraph();
      plot.fillCentral("HIG-12-032", observed, "HIG-12-032-observed");
    }
    /// expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral("HIG-12-032", expected, "HIG-12-032-expected");
    /// 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand("HIG-12-032", inner, "HIG-12-032", true);
    /// 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand("HIG-12-032", outer, "HIG-12-032", false);
    /// make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plot(*canv, inner, outer, expected, observed);
  }
  if( std::string(argv[1]) == std::string("HIG-12-043") ){
    /// observed limit
    TGraph* observed  = 0;
    if(!expected_only){
      observed = new TGraph();
      plot.fillCentral("HIG-12-043", observed, "HIG-12-043-observed");
    }
    /// expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral("HIG-12-043", expected, "HIG-12-043-expected");
    /// 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand("HIG-12-043", inner, "HIG-12-043", true);
    /// 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand("HIG-12-043", outer, "HIG-12-043", false);
    /// make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plot(*canv, inner, outer, expected, observed);
  }
  if( std::string(argv[1]) == std::string("HIG-12-050") ){
    /// observed limit
    TGraph* observed  = 0;
    if(!expected_only){
      observed = new TGraph();
      plot.fillCentral("HIG-12-050", observed, "HIG-12-050-observed");
    }
    /// expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral("HIG-12-050", expected, "HIG-12-050-expected");
    /// 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand("HIG-12-050", inner, "HIG-12-050", true);
    /// 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand("HIG-12-050", outer, "HIG-12-050", false);
    /// make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotTanb(*canv, inner, outer, expected, observed);
  }
  return 0;
}
