#include <iostream>
#include "TFile.h"
#include "TH1F.h"
#include "TLegend.h"

void addNuisance(std::string iFileName,std::string iChannel,std::string iBkg,std::string iEnergy,std::string iName,std::string iDir) { 
  std::cout << "======> " << iDir << "/" << iBkg << " -- " << iFileName << std::endl;  
  TFile *lFile = new TFile(iFileName.c_str(),"UPDATE");
  TH1F  *lH0   = (TH1F*) lFile->Get((iDir+"/"+iBkg).c_str());
  std::string lNuisance =  iBkg+"_"+"CMS_scale_"+iName+"_" + iChannel + "_" + iEnergy;
  double lInt = lH0->Integral();
  TH1F *lHCUp   = (TH1F*) lH0->Clone((lNuisance+"Up"  ).c_str());
  TH1F *lHCDown = (TH1F*) lH0->Clone((lNuisance+"Down").c_str());
  //Add 2% shift
  //for(int i0 = 0; i0 < lH0->GetNbinsX()+1; i0++) { 
  //  double pUpCorr       = 1.0;
  //  if(lH0->GetBinCenter(i0) > 0 && lH0->GetBinWidth(i0-1)) pUpCorr = 1.-2./lH0->GetBinWidth(i0-1);
  //  double pAntiUpCorr   = 1-pUpCorr; 
  //  lH0    ->SetBinContent(i0,pUpCorr*lH0->GetBinContent(i0)  +pAntiUpCorr  *lH0->GetBinContent(i0-1)); 
  // }
  //And the motherfucking shapes
  for(int i0 = 0; i0 < lH0->GetNbinsX()+1; i0++) { 
    double pDownCorr     = 1.0;
    if(lH0->GetBinCenter(i0) > 0 && lH0->GetBinWidth(i0-1)) pDownCorr = 1.-2./lH0->GetBinWidth(i0-1);
    double pAntiDownCorr = 1-pDownCorr; 

    double pUpCorr       = 1.0;
    if(lH0->GetBinCenter(i0) > 0 && lH0->GetBinWidth(i0+1)) pUpCorr = 1.-2./lHCUp->GetBinWidth(i0+1);
    double pAntiUpCorr   = 1-pUpCorr; 

    lHCUp  ->SetBinContent(i0,pUpCorr*lH0->GetBinContent(i0)  +pAntiUpCorr  *lH0->GetBinContent(i0+1));
    lHCDown->SetBinContent(i0,pDownCorr*lH0->GetBinContent(i0)+pAntiDownCorr*lH0->GetBinContent(i0-1)); 
  }
  lH0    ->Scale(lInt           /lH0    ->Integral());
  lHCUp  ->Scale(lH0->Integral()/lHCUp  ->Integral());
  lHCDown->Scale(lH0->Integral()/lHCDown->Integral());
  lFile->cd(iDir.c_str());
  //lH0    ->Write();//TObject::kOverWrite); 
  lHCUp  ->Write(); 
  lHCDown->Write(); 
  lFile->Close();
}
void addAllNuisance(std::string iFileName="htt_mt.inputs-sm-8TeV.root",std::string iChannel="muTau",std::string iBkg="ZL",std::string iEnergy="8TeV",std::string iName="shift",bool iVBF=false) { 
  addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_0jet_low");
  addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_0jet_high");
  addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_boost_low");
  addNuisance          (iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_boost_high");
  if(iVBF)  addNuisance(iFileName,iChannel,iBkg,iEnergy,iName,iChannel+"_vbf");
}
