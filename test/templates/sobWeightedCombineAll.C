/*
INSTRU
CTIONS:
-Execute from this directory:
HiggsAnalysis/HiggsToTauTau/test

-In there you need 3 directories:
HiggsAnalysis/HiggsToTauTau/test/root/ (input root-cards)
HiggsAnalysis/HiggsToTauTau/test/datacards/ (.txt data-cards)
HiggsAnalysis/HiggsToTauTau/test/fitresults/ (mlfit result for the pulls in a file called mlfit_sm.txt)

-Run the following commands to generate the root files containing the postfit histograms:
python produce_macros.py  -a sm -c 'mt, et, em' -u 1 -p "7TeV 8TeV"
python produce_macros.py  -a sm -c 'tt' -u 1 -p "8TeV"
sed -i 's/bool log=false/bool log=false/g' *.C
sed -i 's/BLIND_DATA = true/BLIND_DATA = false/g' *.C
python run_macros.py  -a sm -c 'mt, et, em'  -p "7TeV 8TeV"
python run_macros.py  -a sm -c 'tt'  -p "8TeV"


-Now one can execute this combineAll.C macro
root -b /PATH/sobWeightedCombineAll.C
-it relies on another macro sobWeightedCombine.C being at the same PATH
-one needs to make sure to update the muvalue below to the result from the fit to Data


Authors: Jose Benitez, Lorenzo Bianchini 
*/

#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"
#include "HiggsAnalysis/HiggsToTauTau/test/templates/sobWeightedCombine.C"
#include "HiggsAnalysis/HiggsToTauTau/test/templates/sobWeightedCombineMSSM.C"

#define NMAXINPUT 65

void sobCombine(TString name, TString* Input,const char* dataset , const char* channel, const char* cat, int weight=1, float muValue=1.0, bool log=false, int mass=125, int tanb=0)
{
  if(tanb==0){
    sobWeightedCombine(Input,name,weight,muValue);
    /*                                     |-> mu value from the fit to Data
			 |     |     |->option to apply or not apply weights
			 |     |-> name for this plot
			 |->array of input postfit root files 
    */
    sobWeightedPlot(name,dataset,channel,cat,log,mass,tanb);
  }
  else{
    sobWeightedCombineMSSM(Input,name,weight,muValue);
    /*                                     |-> mu value from the fit to Data
			 |     |     |->option to apply or not apply weights
			 |     |-> name for this plot
			 |->array of input postfit root files 
    */
    sobWeightedPlotMSSM(name,dataset,channel,cat,log,mass,tanb);
  }
}

void sobWeightedCombineAll(float muValue=1.10, bool log=false, int mass=125, int tanb=0)
{
  SetStyle();

  TString All_SM[NMAXINPUT]; 
  //vbf
//  All_SM[ 0]="ee_vbf_postfit_7TeV_LIN";
//  All_SM[ 1]="ee_vbf_postfit_8TeV_LIN";
  All_SM[ 0]="emu_vbf_loose_postfit_7TeV_LIN";
  All_SM[ 1]="emu_vbf_loose_postfit_8TeV_LIN";
  All_SM[ 2]="emu_vbf_tight_postfit_8TeV_LIN";
  All_SM[ 3]="eleTau_vbf_postfit_7TeV_LIN";
  All_SM[ 4]="eleTau_vbf_loose_postfit_8TeV_LIN";
  All_SM[ 5]="eleTau_vbf_tight_postfit_8TeV_LIN"; 
  All_SM[ 6]="mumu_vbf_postfit_7TeV_LIN";
  All_SM[ 7]="mumu_vbf_postfit_8TeV_LIN";
  All_SM[ 8]="muTau_vbf_postfit_7TeV_LIN";
  All_SM[ 9]="muTau_vbf_loose_postfit_8TeV_LIN";
  All_SM[10]="muTau_vbf_tight_postfit_8TeV_LIN"; 
  All_SM[11]="tauTau_vbf_postfit_8TeV_LIN";
  //1jet
//  All_SM[14]="ee_1jet_low_postfit_7TeV_LIN";
//  All_SM[15]="ee_1jet_low_postfit_8TeV_LIN";
//  All_SM[16]="ee_1jet_high_postfit_7TeV_LIN";
//  All_SM[17]="ee_1jet_high_postfit_8TeV_LIN";
  All_SM[12]="emu_1jet_low_postfit_7TeV_LIN";
  All_SM[13]="emu_1jet_low_postfit_8TeV_LIN";
  All_SM[14]="emu_1jet_high_postfit_7TeV_LIN";
  All_SM[15]="emu_1jet_high_postfit_8TeV_LIN";
  All_SM[16]="eleTau_1jet_medium_postfit_7TeV_LIN";
  All_SM[17]="eleTau_1jet_medium_postfit_8TeV_LIN";
  All_SM[18]="eleTau_1jet_high_mediumhiggs_postfit_7TeV_LIN";
  All_SM[19]="eleTau_1jet_high_mediumhiggs_postfit_8TeV_LIN"; 
//  All_SM[26]="mumu_1jet_low_postfit_7TeV_LIN";
//  All_SM[27]="mumu_1jet_low_postfit_8TeV_LIN";
//  All_SM[28]="mumu_1jet_high_postfit_7TeV_LIN";
//  All_SM[29]="mumu_1jet_high_postfit_8TeV_LIN";
  All_SM[20]="muTau_1jet_medium_postfit_7TeV_LIN";
  All_SM[21]="muTau_1jet_medium_postfit_8TeV_LIN";
  All_SM[22]="muTau_1jet_high_lowhiggs_postfit_7TeV_LIN";
  All_SM[23]="muTau_1jet_high_lowhiggs_postfit_8TeV_LIN"; 
  All_SM[24]="muTau_1jet_high_mediumhiggs_postfit_7TeV_LIN";
  All_SM[25]="muTau_1jet_high_mediumhiggs_postfit_8TeV_LIN"; 
  All_SM[26]="tauTau_1jet_high_mediumhiggs_postfit_8TeV_LIN";
  All_SM[27]="tauTau_1jet_high_highhiggs_postfit_8TeV_LIN";
  //0jet
//  All_SM[38]="ee_0jet_low_postfit_7TeV_LIN";
//  All_SM[39]="ee_0jet_low_postfit_8TeV_LIN";
//  All_SM[40]="ee_0jet_high_postfit_7TeV_LIN";
//  All_SM[41]="ee_0jet_high_postfit_8TeV_LIN";
  All_SM[28]="emu_0jet_low_postfit_7TeV_LIN";
  All_SM[29]="emu_0jet_low_postfit_8TeV_LIN";
  All_SM[30]="emu_0jet_high_postfit_7TeV_LIN";
  All_SM[31]="emu_0jet_high_postfit_8TeV_LIN";
  All_SM[32]="eleTau_0jet_low_postfit_7TeV_LIN";
  All_SM[33]="eleTau_0jet_low_postfit_8TeV_LIN";
  All_SM[34]="eleTau_0jet_medium_postfit_7TeV_LIN";
  All_SM[35]="eleTau_0jet_medium_postfit_8TeV_LIN"; 
  All_SM[36]="eleTau_0jet_high_postfit_7TeV_LIN";
  All_SM[37]="eleTau_0jet_high_postfit_8TeV_LIN"; 
//  All_SM[52]="mumu_0jet_low_postfit_7TeV_LIN";
//  All_SM[53]="mumu_0jet_low_postfit_8TeV_LIN";
//  All_SM[54]="mumu_0jet_high_postfit_7TeV_LIN";
//  All_SM[55]="mumu_0jet_high_postfit_8TeV_LIN"; 
  All_SM[38]="muTau_0jet_low_postfit_7TeV_LIN";
  All_SM[39]="muTau_0jet_low_postfit_8TeV_LIN";
  All_SM[40]="muTau_0jet_medium_postfit_7TeV_LIN";
  All_SM[41]="muTau_0jet_medium_postfit_8TeV_LIN"; 
  All_SM[42]="muTau_0jet_high_postfit_7TeV_LIN";
  All_SM[43]="muTau_0jet_high_postfit_8TeV_LIN";  
  //mt soft
  All_SM[44]="muTau_soft_0jet_low_postfit_8TeV_LIN";
  All_SM[45]="muTau_soft_0jet_medium_postfit_8TeV_LIN";
  All_SM[46]="muTau_soft_0jet_high_postfit_8TeV_LIN";
  All_SM[47]="muTau_soft_1jet_medium_postfit_8TeV_LIN";
  All_SM[48]="muTau_soft_1jet_high_postfit_8TeV_LIN";
  All_SM[49]="muTau_soft_vbf_postfit_8TeV_LIN";
  
  TString EMETMTTT_1JET_VBF_SM[NMAXINPUT]; 
  //vbf
  EMETMTTT_1JET_VBF_SM[ 0]="emu_vbf_loose_postfit_7TeV_LIN";
  EMETMTTT_1JET_VBF_SM[ 1]="emu_vbf_loose_postfit_8TeV_LIN";
  EMETMTTT_1JET_VBF_SM[ 2]="emu_vbf_tight_postfit_8TeV_LIN";
  EMETMTTT_1JET_VBF_SM[ 3]="eleTau_vbf_postfit_7TeV_LIN";
  EMETMTTT_1JET_VBF_SM[ 4]="eleTau_vbf_loose_postfit_8TeV_LIN";
  EMETMTTT_1JET_VBF_SM[ 5]="eleTau_vbf_tight_postfit_8TeV_LIN"; 
  EMETMTTT_1JET_VBF_SM[ 6]="muTau_vbf_postfit_7TeV_LIN";
  EMETMTTT_1JET_VBF_SM[ 7]="muTau_vbf_loose_postfit_8TeV_LIN";
  EMETMTTT_1JET_VBF_SM[ 8]="muTau_vbf_tight_postfit_8TeV_LIN"; 
  EMETMTTT_1JET_VBF_SM[ 9]="tauTau_vbf_postfit_8TeV_LIN";
  //1jet
  EMETMTTT_1JET_VBF_SM[10]="emu_1jet_low_postfit_7TeV_LIN";
  EMETMTTT_1JET_VBF_SM[11]="emu_1jet_low_postfit_8TeV_LIN";
  EMETMTTT_1JET_VBF_SM[12]="emu_1jet_high_postfit_7TeV_LIN";
  EMETMTTT_1JET_VBF_SM[13]="emu_1jet_high_postfit_8TeV_LIN";
  EMETMTTT_1JET_VBF_SM[14]="eleTau_1jet_medium_postfit_7TeV_LIN";
  EMETMTTT_1JET_VBF_SM[15]="eleTau_1jet_medium_postfit_8TeV_LIN";
  EMETMTTT_1JET_VBF_SM[16]="eleTau_1jet_high_mediumhiggs_postfit_7TeV_LIN";
  EMETMTTT_1JET_VBF_SM[17]="eleTau_1jet_high_mediumhiggs_postfit_8TeV_LIN"; 
  EMETMTTT_1JET_VBF_SM[18]="muTau_1jet_medium_postfit_7TeV_LIN";
  EMETMTTT_1JET_VBF_SM[19]="muTau_1jet_medium_postfit_8TeV_LIN";
  EMETMTTT_1JET_VBF_SM[20]="muTau_1jet_high_lowhiggs_postfit_7TeV_LIN";
  EMETMTTT_1JET_VBF_SM[21]="muTau_1jet_high_lowhiggs_postfit_8TeV_LIN"; 
  EMETMTTT_1JET_VBF_SM[22]="muTau_1jet_high_mediumhiggs_postfit_7TeV_LIN";
  EMETMTTT_1JET_VBF_SM[23]="muTau_1jet_high_mediumhiggs_postfit_8TeV_LIN"; 
  EMETMTTT_1JET_VBF_SM[24]="tauTau_1jet_high_mediumhiggs_postfit_8TeV_LIN";
  EMETMTTT_1JET_VBF_SM[25]="tauTau_1jet_high_highhiggs_postfit_8TeV_LIN";

  TString EE_SM[NMAXINPUT];
  EE_SM[ 0]="ee_vbf_postfit_7TeV_LIN";
  EE_SM[ 1]="ee_vbf_postfit_8TeV_LIN";
  EE_SM[ 2]="ee_1jet_low_postfit_7TeV_LIN";
  EE_SM[ 3]="ee_1jet_low_postfit_8TeV_LIN";
  EE_SM[ 4]="ee_1jet_high_postfit_7TeV_LIN";
  EE_SM[ 5]="ee_1jet_high_postfit_8TeV_LIN";
  EE_SM[ 6]="ee_0jet_low_postfit_7TeV_LIN";
  EE_SM[ 7]="ee_0jet_low_postfit_8TeV_LIN";
  EE_SM[ 8]="ee_0jet_high_postfit_7TeV_LIN";
  EE_SM[ 9]="ee_0jet_high_postfit_8TeV_LIN";

  TString EMu_SM[NMAXINPUT];
  EMu_SM[ 0]="emu_vbf_loose_postfit_7TeV_LIN";
  EMu_SM[ 1]="emu_vbf_loose_postfit_8TeV_LIN";
  EMu_SM[ 2]="emu_vbf_tight_postfit_8TeV_LIN";
  EMu_SM[ 3]="emu_1jet_low_postfit_7TeV_LIN";
  EMu_SM[ 4]="emu_1jet_low_postfit_8TeV_LIN";
  EMu_SM[ 5]="emu_1jet_high_postfit_7TeV_LIN";
  EMu_SM[ 6]="emu_1jet_high_postfit_8TeV_LIN";
  EMu_SM[ 7]="emu_0jet_low_postfit_7TeV_LIN";
  EMu_SM[ 8]="emu_0jet_low_postfit_8TeV_LIN";
  EMu_SM[ 9]="emu_0jet_high_postfit_7TeV_LIN";
  EMu_SM[10]="emu_0jet_high_postfit_8TeV_LIN";

  TString ETau_SM[NMAXINPUT];
  ETau_SM[ 0]="eleTau_vbf_postfit_7TeV_LIN";
  ETau_SM[ 1]="eleTau_vbf_loose_postfit_8TeV_LIN";
  ETau_SM[ 2]="eleTau_vbf_tight_postfit_8TeV_LIN"; 
  ETau_SM[ 3]="eleTau_1jet_medium_postfit_7TeV_LIN";
  ETau_SM[ 4]="eleTau_1jet_medium_postfit_8TeV_LIN";
  ETau_SM[ 5]="eleTau_1jet_high_mediumhiggs_postfit_7TeV_LIN";
  ETau_SM[ 6]="eleTau_1jet_high_mediumhiggs_postfit_8TeV_LIN"; 
  ETau_SM[ 7]="eleTau_0jet_low_postfit_7TeV_LIN";
  ETau_SM[ 8]="eleTau_0jet_low_postfit_8TeV_LIN";
  ETau_SM[ 9]="eleTau_0jet_medium_postfit_7TeV_LIN";
  ETau_SM[10]="eleTau_0jet_medium_postfit_8TeV_LIN"; 
  ETau_SM[11]="eleTau_0jet_high_postfit_7TeV_LIN";
  ETau_SM[12]="eleTau_0jet_high_postfit_8TeV_LIN"; 

  TString MuMu_SM[NMAXINPUT];
  MuMu_SM[ 0]="mumu_vbf_postfit_7TeV_LIN";
  MuMu_SM[ 1]="mumu_vbf_postfit_8TeV_LIN";
  MuMu_SM[ 2]="mumu_1jet_low_postfit_7TeV_LIN";
  MuMu_SM[ 3]="mumu_1jet_low_postfit_8TeV_LIN";
  MuMu_SM[ 4]="mumu_1jet_high_postfit_7TeV_LIN";
  MuMu_SM[ 5]="mumu_1jet_high_postfit_8TeV_LIN";
  MuMu_SM[ 6]="mumu_0jet_low_postfit_7TeV_LIN";
  MuMu_SM[ 7]="mumu_0jet_low_postfit_8TeV_LIN";
  MuMu_SM[ 8]="mumu_0jet_high_postfit_7TeV_LIN";
  MuMu_SM[ 9]="mumu_0jet_high_postfit_8TeV_LIN"; 
  
  TString MuTau_SM[NMAXINPUT];
  MuTau_SM[ 0]="muTau_vbf_postfit_7TeV_LIN";
  MuTau_SM[ 1]="muTau_vbf_loose_postfit_8TeV_LIN";
  MuTau_SM[ 2]="muTau_vbf_tight_postfit_8TeV_LIN"; 
  MuTau_SM[ 3]="muTau_1jet_medium_postfit_7TeV_LIN";
  MuTau_SM[ 4]="muTau_1jet_medium_postfit_8TeV_LIN";
  MuTau_SM[ 5]="muTau_1jet_high_lowhiggs_postfit_7TeV_LIN";
  MuTau_SM[ 6]="muTau_1jet_high_lowhiggs_postfit_8TeV_LIN"; 
  MuTau_SM[ 7]="muTau_1jet_high_mediumhiggs_postfit_7TeV_LIN";
  MuTau_SM[ 8]="muTau_1jet_high_mediumhiggs_postfit_8TeV_LIN"; 
  MuTau_SM[ 9]="muTau_0jet_low_postfit_7TeV_LIN";
  MuTau_SM[10]="muTau_0jet_low_postfit_8TeV_LIN";
  MuTau_SM[11]="muTau_0jet_medium_postfit_7TeV_LIN";
  MuTau_SM[12]="muTau_0jet_medium_postfit_8TeV_LIN"; 
  MuTau_SM[13]="muTau_0jet_high_postfit_7TeV_LIN";
  MuTau_SM[14]="muTau_0jet_high_postfit_8TeV_LIN";
  
  TString MuTauSoft_SM[NMAXINPUT];
  MuTau_SM[ 0]="muTau_vbf_postfit_7TeV_LIN";
  MuTau_SM[ 1]="muTau_vbf_loose_postfit_8TeV_LIN";
  MuTau_SM[ 2]="muTau_vbf_tight_postfit_8TeV_LIN"; 
  MuTau_SM[ 3]="muTau_1jet_medium_postfit_7TeV_LIN";
  MuTau_SM[ 4]="muTau_1jet_medium_postfit_8TeV_LIN";
  MuTau_SM[ 5]="muTau_1jet_high_lowhiggs_postfit_7TeV_LIN";
  MuTau_SM[ 6]="muTau_1jet_high_lowhiggs_postfit_8TeV_LIN"; 
  MuTau_SM[ 7]="muTau_1jet_high_mediumhiggs_postfit_7TeV_LIN";
  MuTau_SM[ 8]="muTau_1jet_high_mediumhiggs_postfit_8TeV_LIN"; 
  MuTau_SM[ 9]="muTau_0jet_low_postfit_7TeV_LIN";
  MuTau_SM[10]="muTau_0jet_low_postfit_8TeV_LIN";
  MuTau_SM[11]="muTau_0jet_medium_postfit_7TeV_LIN";
  MuTau_SM[12]="muTau_0jet_medium_postfit_8TeV_LIN"; 
  MuTau_SM[13]="muTau_0jet_high_postfit_7TeV_LIN";
  MuTau_SM[14]="muTau_0jet_high_postfit_8TeV_LIN";
  MuTau_SM[15]="muTau_soft_0jet_low_postfit_8TeV_LIN";
  MuTau_SM[16]="muTau_soft_0jet_medium_postfit_8TeV_LIN";
  MuTau_SM[17]="muTau_soft_0jet_high_postfit_8TeV_LIN";
  MuTau_SM[18]="muTau_soft_1jet_medium_postfit_8TeV_LIN";
  MuTau_SM[19]="muTau_soft_1jet_high_postfit_8TeV_LIN";
  MuTau_SM[20]="muTau_soft_vbf_postfit_8TeV_LIN";



  TString TauTau_SM[NMAXINPUT];
  TauTau_SM[ 0]="tauTau_vbf_postfit_8TeV_LIN";
  TauTau_SM[ 1]="tauTau_1jet_high_mediumhiggs_postfit_8TeV_LIN";
  TauTau_SM[ 2]="tauTau_1jet_high_highhiggs_postfit_8TeV_LIN";
  




  TString All_MSSM[NMAXINPUT];
  All_MSSM[0]="emu_nobtag_postfit_7TeV_LIN";
  All_MSSM[1]="emu_nobtag_postfit_8TeV_LIN";
  All_MSSM[2]="emu_btag_postfit_7TeV_LIN";
  All_MSSM[3]="emu_btag_postfit_8TeV_LIN"; 
  All_MSSM[4]="eleTau_nobtag_postfit_7TeV_LIN";
  All_MSSM[5]="eleTau_nobtag_postfit_8TeV_LIN";
  All_MSSM[6]="eleTau_btag_postfit_7TeV_LIN";
  All_MSSM[7]="eleTau_btag_postfit_8TeV_LIN";
  All_MSSM[8]="muTau_nobtag_postfit_7TeV_LIN";
  All_MSSM[9]="muTau_nobtag_postfit_8TeV_LIN";
  All_MSSM[10]="muTau_btag_postfit_7TeV_LIN";
  All_MSSM[11]="muTau_btag_postfit_8TeV_LIN";
  All_MSSM[12]="tauTau_nobtag_postfit_8TeV_LIN";
  All_MSSM[13]="tauTau_btag_postfit_8TeV_LIN";
  //All_MSSM[14]="mumu_nobtag_postfit_7TeV_LIN";
  //All_MSSM[15]="mumu_nobtag_postfit_8TeV_LIN";
  //All_MSSM[16]="mumu_btag_postfit_7TeV_LIN";
  //All_MSSM[17]="mumu_btag_postfit_8TeV_LIN";

  TString EMu_MSSM[NMAXINPUT];
  EMu_MSSM[0]="emu_nobtag_postfit_7TeV_LIN";
  EMu_MSSM[1]="emu_nobtag_postfit_8TeV_LIN";
  EMu_MSSM[2]="emu_btag_postfit_7TeV_LIN";
  EMu_MSSM[3]="emu_btag_postfit_8TeV_LIN";

  TString ETau_MSSM[NMAXINPUT];
  ETau_MSSM[0]="eleTau_nobtag_postfit_7TeV_LIN";
  ETau_MSSM[1]="eleTau_nobtag_postfit_8TeV_LIN";
  ETau_MSSM[2]="eleTau_btag_postfit_7TeV_LIN";
  ETau_MSSM[3]="eleTau_btag_postfit_8TeV_LIN";

  TString MuMu_MSSM[NMAXINPUT];
  MuMu_MSSM[0]="mumu_nobtag_postfit_7TeV_LIN";
  MuMu_MSSM[1]="mumu_nobtag_postfit_8TeV_LIN";
  MuMu_MSSM[2]="mumu_btag_postfit_7TeV_LIN";
  MuMu_MSSM[3]="mumu_btag_postfit_8TeV_LIN";

  TString MuTau_MSSM[NMAXINPUT];
  MuTau_MSSM[0]="muTau_nobtag_postfit_7TeV_LIN";
  MuTau_MSSM[1]="muTau_nobtag_postfit_8TeV_LIN";
  MuTau_MSSM[2]="muTau_btag_postfit_7TeV_LIN";
  MuTau_MSSM[3]="muTau_btag_postfit_8TeV_LIN";

  TString TauTau_MSSM[NMAXINPUT];
  TauTau_MSSM[0]="tauTau_nobtag_postfit_7TeV_LIN";
  TauTau_MSSM[1]="tauTau_nobtag_postfit_8TeV_LIN";
  TauTau_MSSM[2]="tauTau_btag_postfit_7TeV_LIN";
  TauTau_MSSM[3]="tauTau_btag_postfit_8TeV_LIN";
  

  TString dataset="CMS Preliminary,  H#rightarrow#tau#tau,  4.9 fb^{-1} at 7 TeV, 19.8 fb^{-1} at 8 TeV";

    sobCombine("All_SM", All_SM, dataset, "ee, e#mu, e#tau_{h}, #mu#mu, #mu#tau_{h}, #tau_{h}#tau_{h}" , "", 1, muValue);
    sobCombine("EMETMTTT_1JET_VBF_SM", EMETMTTT_1JET_VBF_SM, dataset, "e#mu, e#tau_{h}, #mu#tau_{h}, #tau_{h}#tau_{h}" , "", 1, muValue); //no ee, mm, 0jet here - some fixes needed
  //  sobCombine("EE_SM", EE_SM, dataset, "ee" , "", 1, muValue);
    sobCombine("EMu_SM", EMu_SM, dataset, "e#mu" , "", 1, muValue);
    sobCombine("ETau_SM", ETau_SM, dataset, "e#tau_{h}" , "", 1, muValue);
  //  sobCombine("MuMu_SM", MuMu_SM, dataset, " #mu#mu" , "", 1, muValue);
    sobCombine("MuTau_SM", MuTau_SM, dataset, "#mu#tau_{h}" , "", 1, muValue);
    sobCombine("TauTau_SM", TauTau_SM, dataset, "#tau_{h}#tau_{h}" , "", 1, muValue);

  // sobCombine("All_MSSM", All_MSSM, dataset, "#scale[1]e#mu_{h}, #scale[1]e#tau_{h}, #scale[1]{#mu}#mu_{h}, #scale[1]{#mu}#tau_{h}, #tau_{h}#tau_{h}" , "", 1, muValue, log, mass, tanb);
  // sobCombine("All_MSSM", All_MSSM, dataset, "e#mu_{h}, e#tau_{h}, #mu#tau_{h}, #tau_{h}#tau_{h}" , "", 1, muValue, log, mass, tanb); 
  // sobCombine("EMu_MSSM", EMu_MSSM, dataset, "e#mu_{h}" , "", 1, muValue, log, mass, tanb);
  // sobCombine("ETau_MSSM", ETau_MSSM, dataset, "e#tau_{h}" , "", 1, muValue, log, mass, tanb);
  // sobCombine("MuMu_MSSM", MuMu_MSSM, dataset, "#mu#mu" , "", 1, muValue, log, mass, tanb);
  // sobCombine("MuTau_MSSM", MuTau_MSSM, dataset, "#mu#tau_{h}" , "", 1, muValue, log, mass, tanb);
  // sobCombine("TauTau_MSSM", TauTau_MSSM, dataset, "#tau_{h}#tau_{h}" , "", 1, muValue, log, mass, tanb);

  gROOT->ProcessLine(".q");
}
 
