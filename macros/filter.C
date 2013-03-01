double getMinNLL(std::string iChannel, double iMass,bool iBackground) { 
  std::stringstream pSS; pSS << iChannel << "/" << iMass << "/out/mlfit.root";
  TFile *lFile = new TFile(pSS.str().c_str());
  TTree *lTree = (TTree*) lFile->FindObjectAny("tree_fit_sb");
  if(iBackground) lTree = (TTree*) lFile->FindObjectAny("tree_fit_b");
  double lNLL=  0; lTree->SetBranchAddress("nll_min",&lNLL); 
  lTree->GetEntry(0);				
  double lFNLL = lNLL;
  //lFile->Close();
  //  cout << " ===> " << lFNLL << endl;
  return lFNLL;
}
void filter(double iMass=110,std::string iChannel) { 
  TFile *lFile = new TFile("Output.root","RECREATE");
  TTree *lTree = new TTree("tree_fit_sb","tree_fit_sb");
  float lNLLSB = 0; lTree->Branch("nll_min"  ,&lNLLSB,"lNLLSB/F");
  float lNLLB  = 0; lTree->Branch("nll_min_b",&lNLLB ,"lNLLB/F");
  lNLLSB = getMinNLL(iChannel,iMass,false);
  lNLLB  = getMinNLL(iChannel,iMass,true);
  lFile->cd();
  lTree->Fill();
  lTree->Write();
}


