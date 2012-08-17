# Setup environment variables for HTT limit packages
#
# Usage: 
#    source environment.sh
#
# In particular, put the scripts directory into the PATH,
# so we don't need to recompile to pick up changes.

export PATH=$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/scripts:$PATH

# Compile necessary macros
pushd $CMSSW_BASE/src
root -b -q HiggsAnalysis/HiggsToTauTau/macros/compareLimits.C+  
root -b -q HiggsAnalysis/HiggsToTauTau/macros/blindData.C+  
popd
