#include "mssm_xs_tools.h"
#include "mssm_xs_tools.C"

#include "TString.h"
#include "TGraph.h"

void tanb2xsec(const char* filename, const char* directory="HIG-12-050", const char* graph="observed", bool verbose=true)
{
  mssm_xs_tools mssm;
  mssm.SetInput("HiggsAnalysis/HiggsToTauTau/data/out.mhmax-mu+200-7TeV-tanbHigh-nnlo.root"); //mssm.help();

  /// open input file  
  TFile* inputFile = new TFile(filename, "update");
  TGraph* limit = (TGraph*)inputFile->Get(TString::Format("%s/%s", directory, graph));
  for(int idx=0; idx<limit->GetN(); ++idx){
    float mA = limit->GetX()[idx]; float tanb = limit->GetY()[idx];
    float xsec_limit = mssm.Give_Xsec_ggFA(mA, tanb)*mssm.Give_BR_A_tautau(mA, tanb)/1000. + mssm.GiveXsec_Santander_A(mA, tanb)*mssm.Give_BR_A_tautau(mA, tanb)/1000.;
    if(verbose){
      std::cout << "Limit on cross section [" << mA << "]: " << xsec_limit << " pb" << std::endl;
    }
    limit->SetPoint(idx, limit->GetX()[idx], xsec_limit);
  }
  inputFile->cd(directory);
  limit->Write(graph);
  inputFile->Close();
  return;
}
