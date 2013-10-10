#include <vector>
#include <sstream>
#include <iostream>
#include <iterator>

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

// add a parameter to a parameter set, in a string key=value format.
void addParameter(edm::ParameterSet& pset, const std::string& key, const std::string& value) {
  std::cout << "Updating parameter " << key << " to " << value << " in layout." << std::endl;
  if (pset.existsAs<int>(key))
    pset.addParameter<int>(key, StringToNumber<int>(value));
  else if (pset.existsAs<unsigned int>(key))
    pset.addParameter<unsigned int>(key, StringToNumber<unsigned int>(value));
  else if (pset.existsAs<bool>(key)){
    if(StringToNumber<unsigned int>(value)==0){
      pset.addParameter<bool>(key, true);
    }
    else{
      pset.addParameter<bool>(key, true);
    }
  }
  else if (pset.existsAs<double>(key))
    pset.addParameter<double>(key, StringToNumber<double>(value));
  else if (pset.existsAs<std::vector<double> >(key)){
    std::stringstream stream(value);
    std::vector<double> values((std::istream_iterator<double>(stream)), std::istream_iterator<double>());
    pset.addParameter<std::vector<double> >(key, values);
  }
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
  // show full CLs cross section limits 
  types.push_back(std::string("--CLs"));
  // show limits in mA-tanb (from full CLs or from asymptotic)
  types.push_back(std::string("--tanb"));
  // show bayesian cross section limits
  types.push_back(std::string("--bayesian"));
  // show asymptotic cross section limits with signal injected
  types.push_back(std::string("--injected"));
  // show frequentist significances with signal injected
  types.push_back(std::string("--injected-sig"));
  // show frequentist pvalue with signal injected
  types.push_back(std::string("--injected-pval"));
  // show asymptotic cross section (times BR) limits
  types.push_back(std::string("--asymptotic"));
  // show significances with bands (run with toys)
  types.push_back(std::string("--significance"));
  // show significances w/o bands, frequentist
  types.push_back(std::string("--significance-frequentist"));
  // show frequentist p-values w/o bands
  types.push_back(std::string("--pvalue-frequentist"));
  // show goodnes of fit estimate
  types.push_back(std::string("--goodness-of-fit"));
  // show signal strength as function of mH/mA as determined from a 1d maxlikelihood fit 
  types.push_back(std::string("--max-likelihood"));
  // show signal strength as function of mH/mA as determined from a 2d maxlikelihood fit 
  types.push_back(std::string("--likelihood-scan"));
  // show 2D scans (still in developement)
  types.push_back(std::string("--likelihood-scan-mass"));
  types.push_back(std::string("--mass-estimate"));
  // show 2D scans (still in developement)
  types.push_back(std::string("--multidim-fit"));
  // show limits as of HIG-11-020
  types.push_back(std::string("--HIG-11-020"));
  // show limits as of HIG-11-029
  types.push_back(std::string("--HIG-11-029"));
  // show limits as of HIG-12-018
  types.push_back(std::string("--HIG-12-018"));
  // show limits as of HIG-12-032
  types.push_back(std::string("--HIG-12-032"));
  // show limits as of HIG-12-043
  types.push_back(std::string("--HIG-12-043"));
  // show limits as of HIG-12-050
  types.push_back(std::string("--HIG-12-050"));
  // show limits as of HIG-13-004
  types.push_back(std::string("--HIG-13-004"));

  // parse arguments
  if(argc<3){
    std::cout << "Usage : " << argv[0] << " [limit-type] [layout.py] [target-dir] [option1=value1 [option2=value2] ...]" << std::endl;
    return 0;
  }
  if( std::find(types.begin(), types.end(), std::string(argv[1])) == types.end()){
    std::cout << " ERROR: The specified limit type (" << argv[1] << ")"
	      << " is not supported. Available limit types are:" << std::endl;
    for( std::vector<std::string>::const_iterator type = types.begin(); type!=types.end(); ++type ){
      std::cout << "  " << *type << std::endl;
    }
    exit(0);
  }
  if(!edm::readPSetsFrom(argv[2])->existsAs<edm::ParameterSet>("layout")){
    std::cout << " ERROR: ParameterSet 'layout' is missing in your configuration file" << std::endl; exit(0);
  }
  edm::ParameterSet layout =  edm::readPSetsFrom(argv[2])->getParameterSet("layout");

  // define number of required parameters
  int REQUIRED = (std::string(argv[1]).find("HIG")==std::string::npos) ? 4 : 3;
  // get intput directory up to one before mass points
  const char* directory((std::string(argv[1]).find("HIG")==std::string::npos) ? argv[3] : argv[1]);
  std::string directory_string(directory);
  // chop off the prepended directories if needed for out
  if(directory_string.rfind("/")+1 == directory_string.length()){
    directory_string = directory_string.substr(0, directory_string.rfind("/"));
  }
  else{
    directory_string = directory_string.substr(2, std::string::npos);
  }
  std::string out(directory_string.substr(directory_string.rfind("/")+1));

  // update layout with overridden options
  if(argc>REQUIRED){
    for(int i=REQUIRED; i<argc; ++i){
      std::string argument(argv[i]);
      size_t equals_pos = argument.find("=");
      if(equals_pos == std::string::npos){
        std::cerr << "I don't understand the layout override: " << argument <<
          " The format should be key=value" << std::endl;
        exit(1);
      }
      std::string key = argument.substr(0, equals_pos);
      std::string value = argument.substr(equals_pos+1, argument.length() - equals_pos+1);
      addParameter(layout, key, value);
    }
  }
  bool mssm = layout.existsAs<bool>("mssm") ? layout.getParameter<bool>("mssm") : false;
  bool expectedOnly = layout.existsAs<bool>("expectedOnly") ? layout.getParameter<bool>("expectedOnly") : false;
  
  /*
    Implementations
  */
  PlotLimits plot(out.c_str(), layout);
  if(std::string(argv[1]) == std::string("--CLs")){
    // observed limit
    TGraph* observed  = 0;
    if(!expectedOnly){
      observed = new TGraph();
      plot.fillCentral(directory, observed, "higgsCombineTest.HybridNew.mH$MASS");
    }
    // expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral(directory, expected, "higgsCombineTest.HybridNew.mH$MASS.quant0.500");
    // 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand(directory, outer, "CLs", false);
    // 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand(directory, inner, "CLs", true);
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotLimit(*canv, inner, outer, expected, observed);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--tanb") ){
    // observed limit
    TGraph* observed  = 0;
    if(!expectedOnly){
      observed = new TGraph();
      plot.fillCentral(directory, observed, "higgsCombineTest.HybridNew.mH$MASS");
    }
    // expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral(directory, expected, "higgsCombineTest.HybridNew.mH$MASS.quant0.500");
    // 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand(directory, outer, "CLs", false);
    // 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand(directory, inner, "CLs", true);

    // low observed limit
    TGraph* observed_low  = 0;
    if(!expectedOnly){
      observed_low = new TGraph();
      plot.fillCentral(directory, observed_low, "higgsCombineTest.HybridNew.mH$MASS", "low");
    }
    // low expected limit
    TGraph* expected_low  = new TGraph();
    plot.fillCentral(directory, expected_low, "higgsCombineTest.HybridNew.mH$MASS.quant0.500", "low");
    // low 2-sigma uncertainty band
    TGraphAsymmErrors* outer_low  = new TGraphAsymmErrors();
    plot.fillBand(directory, outer_low, "CLs", false, "low");
    // low 1-sigma uncertainty band
    TGraphAsymmErrors* inner_low  = new TGraphAsymmErrors();
    plot.fillBand(directory, inner_low, "CLs", true, "low");

    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotTanb(*canv, inner, inner_low, outer, outer_low, expected, expected_low, observed, observed_low, directory);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--bayesian") ){
    // observed limit
    TGraph* observed  = 0;
    if(!expectedOnly){
      observed = new TGraph();
      // fill based on single value in single file as for CLs
      plot.fillCentral(directory, observed, "higgsCombineTest.MarkovChainMC.mH$MASS");
    }
    // expected limit (for --bayesian 'MEDIAN' and 'MEAN' are sensible parameters)
    TGraph* expected  = new TGraph();
    plot.fillCentral(directory, expected, "MEDIAN");
    // 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand(directory, inner, "TOYBASED", true);
    // 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand(directory, outer, "TOYBASED", false);
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotLimit(*canv, inner, outer, expected, observed);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--injected") ){
    // observed limit
    TGraph* observed  = 0;
    if(!expectedOnly){
      observed = new TGraph();
      plot.fillCentral(directory, observed, "higgsCombine-obs.Asymptotic.mH$MASS");
    }
    // expected limit (for --injected 'MEDIAN' and 'MEAN' are sensible parameters)
    TGraph* expected  = new TGraph();
    plot.fillCentral(directory, expected, "MEDIAN");
    // 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand(directory, inner, "TOYBASED", true);
    // 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand(directory, outer, "TOYBASED", false);
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotLimit(*canv, inner, outer, expected, observed);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--injected-sig") ){
    // observed limit
    TGraph* observed  = 0;
    if(!expectedOnly){
      observed = new TGraph();
      plot.fillCentral(directory, observed, "higgsCombineSIG-obs.ProfileLikelihood.mH$MASS");
    }
    // expected limit (for --injected 'MEDIAN' and 'MEAN' are sensible parameters)
    TGraph* expected  = new TGraph();
    plot.fillCentral(directory, expected, "higgsCombineSIG-exp.ProfileLikelihood.mH$MASS");
    // 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand(directory, inner, "TOYBASED", true);
    // 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand(directory, outer, "TOYBASED", false);
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotSignificance(*canv, inner, outer, expected, observed);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--injected-pval") ){
    // observed limit
    TGraph* observed  = 0;
    if(!expectedOnly){
      observed = new TGraph();
      plot.fillCentral(directory, observed, "higgsCombinePVAL-obs.ProfileLikelihood.mH$MASS");
    }
    // expected limit (for --injected 'MEDIAN' and 'MEAN' are sensible parameters)
    TGraph* expected  = new TGraph();
    plot.fillCentral(directory, expected, "higgsCombinePVAL-exp.ProfileLikelihood.mH$MASS");
    // 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand(directory, inner, "TOYBASED", true);
    // 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand(directory, outer, "TOYBASED", false);
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotPValue(*canv, inner, outer, expected, observed);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--asymptotic") ){
    // observed limit
    TGraph* observed  = 0;
    if(!expectedOnly){
      observed = new TGraph();
      plot.fillCentral(directory, observed, "higgsCombine-obs.Asymptotic.mH$MASS");
    }
    // expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral(directory, expected, "higgsCombine-exp.Asymptotic.mH$MASS");
    // 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand(directory, inner, "higgsCombine-exp.Asymptotic.mH$MASS", true);
    // 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand(directory, outer, "higgsCombine-exp.Asymptotic.mH$MASS", false);
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotLimit(*canv, inner, outer, expected, observed);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--significance") ){
    // observed limit
    TGraph* observed  = 0;
    if(!expectedOnly){
      observed = new TGraph();
      plot.fillCentral(directory, observed, "higgsCombineTest.ProfileLikelihood.mH$MASS");
    }
    TGraph* expected  = new TGraph();
    plot.fillCentral(directory, expected, "MEDIAN");
    // 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand(directory, inner, "TOYBASED", true);
    // 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand(directory, outer, "TOYBASED", false);
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotSignificance(*canv, inner, outer, expected, observed);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--significance-frequentist") ){
    // observed significance
    TGraph* observed  = 0;
    if(!expectedOnly){
      observed  = new TGraph();
      plot.fillCentral(directory, observed, "higgsCombineSIG-obs.ProfileLikelihood.mH$MASS");
    }
    // expected significance
    TGraph* expected  = new TGraph();
    plot.fillCentral(directory, expected, "higgsCombineSIG-exp.ProfileLikelihood.mH$MASS");
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotSignificance(*canv, 0, 0, expected, observed);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--pvalue-frequentist") ){
    // observed p-value
    TGraph* observed  = new TGraph();
    plot.fillCentral(directory, observed, "higgsCombinePVAL-obs.ProfileLikelihood.mH$MASS");
    // expected p-value
    TGraph* expected  = new TGraph();
    plot.fillCentral(directory, expected, "higgsCombinePVAL-exp.ProfileLikelihood.mH$MASS");
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotPValue(*canv, 0, 0, expected, observed);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--max-likelihood") ){
    // central value
    TGraph* central  = new TGraph();
    plot.fillCentral(directory, central, "higgsCombineTest.MaxLikelihoodFit.mH$MASS");
    // 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand(directory, inner, "higgsCombineTest.MaxLikelihoodFit.mH$MASS", true);
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotLimit(*canv, inner, 0, central, 0);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--goodness-of-fit") ){
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Goodness of fit", 600, 600);
    plot.plotGoodnessOfFit(*canv, directory);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--likelihood-scan") ){
     // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    //plot.plotSignalStrength(*canv, innerBand, central, directory);
    plot.plot1DScan(*canv, directory);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--likelihood-scan-mass") ){
    // Likelihood
    TGraph* observed  = new TGraph(); //not needed for plot1DScan
    plot.fillCentral(directory, observed, "NLL");
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotMassScan(*canv, observed);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--mass-estimate") ){
    // Likelihood
    TGraph* observed  = new TGraph(); //not needed for plot1DScan
    plot.fillCentral(directory, observed, "NLL");
    TGraph* expected = new TGraph();
    plot.fillCentral(directory, expected, "MEDIAN");
    // 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand(directory, inner, "TOYBASED", true);
    // 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand(directory, outer, "TOYBASED", false);
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotMassEstimate(*canv, inner, outer, expected, observed);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--multidim-fit") ){
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plot2DScan(*canv, directory);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--HIG-11-020") ){
    // observed limit
    TGraph* observed  = 0;
    if(!expectedOnly){
      observed = new TGraph();
      plot.fillCentral("HIG-11-020", observed, "HIG-11-020-obs");
    }
    // expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral("HIG-11-020", expected, "HIG-11-020-exp");
    // 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand("HIG-11-020", inner, "HIG-11-020", true);
    // 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand("HIG-11-020", outer, "HIG-11-020", false);
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    // plots the layout corresponding to cross section limits
    //plot.plot(*canv, inner, outer, expected, observed);
    // plots the layout corresponding to the direct tanb limits
    plot.plotTanb(*canv, inner, 0, outer, 0, expected, 0, observed, 0);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--HIG-11-029") ){
    // observed limit
    TGraph* observed  = 0;
    if(!expectedOnly){
      observed = new TGraph();
      plot.fillCentral("HIG-11-029", observed, "HIG-11-029-obs");
    }
    // expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral("HIG-11-029", expected, "HIG-11-029-exp");
    // 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand("HIG-11-029", inner, "HIG-11-029", true);
    // 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand("HIG-11-029", outer, "HIG-11-029", false);
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    if(mssm){
      plot.plotTanb(*canv, inner, 0, outer, 0, expected, 0, observed, 0);
    }
    else{
      plot.plotLimit(*canv, inner, outer, expected, observed);
    }
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--HIG-12-018") ){
    // observed limit
    TGraph* observed  = 0;
    if(!expectedOnly){
      observed = new TGraph();
      plot.fillCentral("HIG-12-018", observed, "HIG-12-018-obs");
    }
    // expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral("HIG-12-018", expected, "HIG-12-018-exp");
    // 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand("HIG-12-018", inner, "HIG-12-018", true);
    // 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand("HIG-12-018", outer, "HIG-12-018", false);
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotLimit(*canv, inner, outer, expected, observed);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--HIG-12-032") ){
    // observed limit
    TGraph* observed  = 0;
    if(!expectedOnly){
      observed = new TGraph();
      plot.fillCentral("HIG-12-032", observed, "HIG-12-032-obs");
    }
    // expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral("HIG-12-032", expected, "HIG-12-032-exp");
    // 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand("HIG-12-032", inner, "HIG-12-032", true);
    // 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand("HIG-12-032", outer, "HIG-12-032", false);
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotLimit(*canv, inner, outer, expected, observed);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--HIG-12-043") ){
    // observed limit
    TGraph* observed  = 0;
    if(!expectedOnly){
      observed = new TGraph();
      plot.fillCentral("HIG-12-043", observed, "HIG-12-043-obs");
    }
    // expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral("HIG-12-043", expected, "HIG-12-043-exp");
    // 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand("HIG-12-043", inner, "HIG-12-043", true);
    // 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand("HIG-12-043", outer, "HIG-12-043", false);
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotLimit(*canv, inner, outer, expected, observed);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--HIG-12-050") ){
    // observed limit
    TGraph* observed  = 0;
    if(!expectedOnly){
      observed = new TGraph();
      plot.fillCentral("HIG-12-050", observed, "HIG-12-050-obs");
    }
    // expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral("HIG-12-050", expected, "HIG-12-050-exp");
    // 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand("HIG-12-050", inner, "HIG-12-050", true);
    // 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand("HIG-12-050", outer, "HIG-12-050", false);
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotTanb(*canv, inner, 0, outer, 0, expected, 0, observed, 0);
  }
  // -----------------------------------------------------------------------------------------------------------------------
  if( std::string(argv[1]) == std::string("--HIG-13-004") ){
    // observed limit
    TGraph* observed  = 0;
    if(!expectedOnly){
      observed = new TGraph();
      plot.fillCentral("HIG-13-004", observed, "HIG-13-004-obs");
    }
    // expected limit
    TGraph* expected  = new TGraph();
    plot.fillCentral("HIG-13-004", expected, "HIG-13-004-exp");
    // 1-sigma uncertainty band
    TGraphAsymmErrors* inner  = new TGraphAsymmErrors();
    plot.fillBand("HIG-13-004", inner, "HIG-13-004", true);
    // 2-sigma uncertainty band
    TGraphAsymmErrors* outer  = new TGraphAsymmErrors();
    plot.fillBand("HIG-13-004", outer, "HIG-13-004", false);
    // make the plot
    SetStyle();
    TCanvas* canv = new TCanvas("canv", "Limits", 600, 600);
    plot.plotLimit(*canv, inner, outer, expected, observed);
  }
  return 0;
}
