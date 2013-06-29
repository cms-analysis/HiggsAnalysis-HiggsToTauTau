double 
read_value(const char* path, const char* value, bool isBG) 
{ 
  TFile* file = new TFile(TString::Format("%s/out/mlfit.root", path));
  TTree* tree = (TTree*) file->FindObjectAny(isBG ? "tree_fit_b" : "tree_fit_sb");
  double val  = 0; tree->SetBranchAddress(value, &val); tree->GetEntry(0);				
  return val;
}

void 
mlfit_result(const char* path, const char* value="nll_min") 
{ 
  TFile* outFile = new TFile(TString::Format("%s/mlfit_result.root", path),"RECREATE");
  TTree *outTree = new TTree("tree_fit_sb","tree_fit_sb");
  float val_s = 0; outTree->Branch(value, &val_s, TString::Format("%s/F", value));
  float val_b = 0; outTree->Branch(TString::Format("%s_b", value), &val_b, TString::Format("%s_b/F", value));
  val_s = read_value(path, value, false);
  val_b = read_value(path, value, true );
  outFile->cd();
  outTree->Fill ();
  outTree->Write();
}


