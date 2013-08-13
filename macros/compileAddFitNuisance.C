{
  gROOT->ProcessLine(".include $ROOFITSYS/include");
  gROOT->ProcessLine(".L $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/macros/addFitNuisance.C+");
}
