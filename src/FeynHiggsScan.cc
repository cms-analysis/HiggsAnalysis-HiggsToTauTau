#include "HiggsAnalysis/HiggsToTauTau/interface/FeynHiggsScan.h"

FeynHiggsScan::FeynHiggsScan(const char* fileName, const char* treeName, unsigned int n_tanb, double min_tanb, double max_tanb, unsigned int n_mA, double min_mA, double max_mA) :
  verbose_(false), minTanb_(min_tanb), maxTanb_(max_tanb), stepTanb_((max_tanb-min_tanb)/n_tanb), minMA_(min_mA), maxMA_(max_mA), stepMA_((max_mA-min_mA)/n_mA)
{
  // book TH2F for check that filling went OK
  hscan_    = new TH2F("hscan"    , "hscan"    , n_mA, min_mA, max_mA, n_tanb, min_tanb, max_tanb);
  // book TH2F for projections
  hproject_ = new TH2F("hproject" , "hproject" , n_mA, min_mA, max_mA, n_tanb, min_tanb, max_tanb);
  // open input file
  file_= TFile::Open(fileName, "read");
  // get input tree
  tree_ = (TTree*) file_->Get(treeName);
}

FeynHiggsScan::~FeynHiggsScan()
{
  delete hscan_;
  delete hproject_;
  file_->Close();  
}

TH2F* 
FeynHiggsScan::project(const std::string& var)
{
  read(var); 
  hscan_->Clear(); hproject_->Clear();
  unsigned int nevent = tree_->GetEntries();
  if(verbose_){ std::cout << "tree size = " << nevent << std::endl; }
  for(unsigned int idx=0; idx<nevent; ++idx){
    tree_->GetEvent(idx);
    if(verbose_){ std::cout << "tanb = " << tanb_ << "  |  mA = " << mA_ << std::endl; }
    hscan_->Fill(mA_+stepMA_/2., tanb_+stepTanb_/2., 1.);
    hproject_->Fill(mA_+stepMA_/2., tanb_+stepTanb_/2., var_);
  }
  return hproject_;
}

float
FeynHiggsScan::get(const char* variable, const char* model, const char* type, float mA, float tanb)
{
  float result = -999.;
  std::string varname(std::string(type)+"_"+std::string(model)+"_"+std::string(variable));
  TH2F* hist = project(varname); 
  if( minMA_<=mA && mA<maxMA_ && minTanb_<=tanb && tanb<maxTanb_){
    result = hist->GetBinContent(hist->FindBin(mA, tanb));
  }
  return result;
}

void
FeynHiggsScan::book(const std::string& var)
{
  std::string ext(var+"/F");
  tree_->Branch( "tanb"      , &tanb_ , "tanb/F"    );
  tree_->Branch( "mA"        , &mA_   , "mA/F"      );
  tree_->Branch( var.c_str() , &var_  , ext.c_str() );
}

void
FeynHiggsScan::read(const std::string& var)
{
  tree_->SetBranchAddress( "tanb"      , &tanb_ );
  tree_->SetBranchAddress( "mA"        , &mA_   );
  tree_->SetBranchAddress( var.c_str() , &var_  );
}

