 #include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

/// This is the core plotting routine that can also be used within
/// root macros. It is therefore not element of the PlotLimits class.
void plottingHypoTest(TCanvas& canv, TGraphAsymmErrors* plain, TGraphAsymmErrors* innerBand, TGraphAsymmErrors* outerBand, TGraph* expected, TGraph* observed, std::map<double, TGraphAsymmErrors*> higgsBands, std::map<std::string, TGraph*> comparisons, std::string& xaxis, std::string& yaxis, std::string& theory, double min=0., double max=50., bool log=false, bool transparent=false, bool expectedOnly=false, bool plotOuterBand=true);

struct myclass {
  bool operator() (int i,int j) { return (i<j);}
} myobject;

void
PlotLimits::plotHypoTest(TCanvas& canv, const char* directory)
{
  //different MSSM scenarios
  std::string extralabel_ = "";
  const char* model;
  if(theory_=="MSSM m_{h}^{max} scenario") {extralabel_= "mhmax-"; model = "mhmax-mu+200";}
  if(theory_=="MSSM m_{h}^{mod-} scenario") {extralabel_= "mhmodm-"; model = "mhmodm";}
  if(theory_=="MSSM m_{h}^{mod+} scenario") {extralabel_= "mhmodp-"; model = "mhmodp";}
  if(theory_=="MSSM low m_{H} scenario") {extralabel_= "lowmH-"; model = "lowmH";}
  if(theory_=="MSSM lightstau scenario") {extralabel_= "lightstau1"; model = "lighstau1";}
  if(theory_=="MSSM tauphobic scenario") {extralabel_= "tauphobic-"; model = "tauphobic";}

  // set up styles
  SetStyle();
 
  TGraph* expected = 0;
  TGraphAsymmErrors* innerBand = 0;
  TGraphAsymmErrors* outerBand = 0;
  TGraph* observed = 0;

  innerBand = new TGraphAsymmErrors();
  outerBand = new TGraphAsymmErrors();
  expected = new TGraph();
  observed = new TGraph();
  for(unsigned int imass=0, ipoint=0; imass<bins_.size(); ++imass){
    // buffer mass value
    float mass = bins_[imass];

    TString fullpath = TString::Format("%s/%d/HypothesisTest.root", directory, (int)mass);
    std::cout << "open file: " << fullpath << std::endl;

    TFile* file_ = TFile::Open(fullpath); if(!file_){ std::cout << "--> TFile is corrupt: skipping masspoint." << std::endl; continue; }
    TTree* limit = (TTree*) file_->Get("tree"); if(!limit){ std::cout << "--> TTree is corrupt: skipping masspoint." << std::endl; continue; }
    double tanb, exp, obs, plus1sigma, minus1sigma, plus2sigma, minus2sigma;
    limit->SetBranchAddress("tanb", &tanb );  
    limit->SetBranchAddress("minus2sigma", &minus2sigma);
    limit->SetBranchAddress("minus1sigma", &minus1sigma);
    limit->SetBranchAddress("expected", &exp);
    limit->SetBranchAddress("plus1sigma", &plus1sigma); 
    limit->SetBranchAddress("plus2sigma", &plus2sigma);  
    limit->SetBranchAddress("observed", &obs);  
    int nevent = limit->GetEntries();   
    //Drawing variable tanb with no graphics option.
    //variable tanb stored in array fV1 (see TTree::Draw)
    limit->Draw("tanb","","goff");
    Int_t *index = new Int_t[nevent];
    //sort array containing tanb in decreasing order
    //The array index contains the entry numbers in decreasing order in respect to tanb
    TMath::Sort(nevent,limit->GetV1(),index);
    Int_t excluded_idx_minus2sigma=-999;
    Int_t excluded_idx_minus1sigma=-999;
    Int_t excluded_idx_exp=-999; 
    Int_t excluded_idx_plus1sigma=-999;
    Int_t excluded_idx_plus2sigma=-999;
    Int_t excluded_idx_obs=-999;
    Int_t notexcluded_idx_minus2sigma=-999;
    Int_t notexcluded_idx_minus1sigma=-999;
    Int_t notexcluded_idx_exp=-999; 
    Int_t notexcluded_idx_plus1sigma=-999;
    Int_t notexcluded_idx_plus2sigma=-999;
    Int_t notexcluded_idx_obs=-999;
    double highminus2sigma=0, highminus1sigma=0, highexpected=0, highplus1sigma=0, highplus2sigma=0, highobserved=0;
    bool not_minus2sigma_excluded_bool=true, not_minus1sigma_excluded_bool=true, not_exp_excluded_bool=true, not_plus1sigma_excluded_bool=true, not_plus2sigma_excluded_bool=true, not_obs_excluded_bool=true;
    for(int i=0; i<nevent; ++i){
      limit->GetEvent(index[i]);
      //std::cout<< index[i] << " " << tanb << " " << minus2sigma << " " << minus1sigma << " " << exp << " " << plus1sigma  << " " << plus2sigma << " " << obs << " " << std::endl;
      if(i==0){
	highminus2sigma=(minus2sigma+0.95)*tanb;
	highminus1sigma=(minus1sigma+0.95)*tanb;
	highexpected   =(exp+0.95        )*tanb;
	highplus1sigma =(plus1sigma+0.95 )*tanb;
	highplus2sigma =(plus2sigma+0.95 )*tanb;
	highobserved   =(obs+0.95        )*tanb;		  
	//std::cout<< tanb << " " << highminus2sigma << " " << highminus1sigma << " " << highexpected  << " " << highplus1sigma << " " << highplus2sigma << " " << highobserved << std::endl;	
      }

      // -2sigma
      if(minus2sigma < 0.05 && not_minus2sigma_excluded_bool) {
	excluded_idx_minus2sigma = index[i]; 
	if(index[i+1]<nevent){
	  notexcluded_idx_minus2sigma = index[i+1]; // case in between
	}
	else{
	 notexcluded_idx_minus2sigma = index[i];  // case all excluded
	}
      }
      else not_minus2sigma_excluded_bool=false;

      // -1sigma
      if(minus1sigma < 0.05 && not_minus1sigma_excluded_bool) {
	excluded_idx_minus1sigma = index[i]; 
	if(index[i+1]<nevent){
	  notexcluded_idx_minus1sigma = index[i+1]; // case in between
	}
	else{
	 notexcluded_idx_minus1sigma = index[i];  // case all excluded
	}
      }
      else not_minus1sigma_excluded_bool=false;

      // exp
      if(exp < 0.05 && not_exp_excluded_bool) {
	excluded_idx_exp = index[i]; 
	if(index[i+1]<nevent){
	  notexcluded_idx_exp = index[i+1]; // case in between
	}
	else{
	 notexcluded_idx_exp = index[i];  // case all excluded
	}
      }
      else not_exp_excluded_bool=false;

      // +1sigma
      if(plus1sigma < 0.05 && not_plus1sigma_excluded_bool) {
	excluded_idx_plus1sigma = index[i]; 
	if(index[i+1]<nevent){
	  notexcluded_idx_plus1sigma = index[i+1]; // case in between
	}
	else{
	 notexcluded_idx_plus1sigma = index[i];  // case all excluded
	}
      }
      else not_plus1sigma_excluded_bool=false;

      // +2sigma
      if(plus2sigma < 0.05 && not_plus2sigma_excluded_bool) {
	excluded_idx_plus2sigma = index[i]; 
	if(index[i+1]<nevent){
	  notexcluded_idx_plus2sigma = index[i+1]; // case in between
	}
	else{
	 notexcluded_idx_plus2sigma = index[i];  // case all excluded
	}
      }
      else not_plus2sigma_excluded_bool=false;

      // obs
      if(obs < 0.05 && not_obs_excluded_bool) {
	excluded_idx_obs = index[i]; 
	if(index[i+1]<nevent){
	 notexcluded_idx_obs = index[i+1]; // case in between
	} 
	else{
	  notexcluded_idx_obs = index[i];  // case all excluded
	}    
      }
      else not_obs_excluded_bool=false;
    }
    //------------------expected
    double excluded_exp=0;
    if(excluded_idx_exp == -999){                     //case nothing excluded
      excluded_exp=highexpected;
    }
    else if(excluded_idx_exp == notexcluded_idx_exp){ // case all excluded
      limit->GetEvent(excluded_idx_exp);
      excluded_exp=3;//tanb;
    }
    else{                                             // case in between
      limit->GetEvent(excluded_idx_exp);
      double x_up=tanb;
      double y_up=exp;
      limit->GetEvent(notexcluded_idx_exp);
      double x_down=tanb;
      double y_down=exp;
      excluded_exp=(0.05-y_up)/(y_down-y_up)*(x_down-x_up)+x_up; 
    }   
    expected->SetPoint(ipoint, mass, excluded_exp);
    //std::cout<< "expected " << ipoint << " " << mass << " " << excluded_exp << std::endl;

    //-----------------2sigma band
    double excluded_minus2sigma=0;
    if(excluded_idx_minus2sigma == -999){                     //case nothing excluded
      excluded_minus2sigma=highminus2sigma;
    }
    else if(excluded_idx_minus2sigma == notexcluded_idx_minus2sigma){ // case all excluded
      limit->GetEvent(excluded_idx_minus2sigma);
      excluded_minus2sigma=2;//tanb;
    }
    else{                                             // case in between
      limit->GetEvent(excluded_idx_minus2sigma);
      double x_up=tanb;
      double y_up=minus2sigma;
      limit->GetEvent(notexcluded_idx_minus2sigma);
      double x_down=tanb;
      double y_down=minus2sigma;
      excluded_minus2sigma=(0.05-y_up)/(y_down-y_up)*(x_down-x_up)+x_up; 
    }   
    //std::cout<< "minus2sigma " << ipoint << " " << mass << " " << excluded_minus2sigma << std::endl;
    double excluded_plus2sigma=0;
    if(excluded_idx_plus2sigma == -999){                     //case nothing excluded
      excluded_plus2sigma=highplus2sigma;
    }
    else if(excluded_idx_plus2sigma == notexcluded_idx_plus2sigma){ // case all excluded
      limit->GetEvent(excluded_idx_plus2sigma);
      excluded_plus2sigma=5;//tanb;
    }
    else{                                             // case in between
      limit->GetEvent(excluded_idx_plus2sigma);
      double x_up=tanb;
      double y_up=plus2sigma;
      limit->GetEvent(notexcluded_idx_plus2sigma);
      double x_down=tanb;
      double y_down=plus2sigma;
      excluded_plus2sigma=(0.05-y_up)/(y_down-y_up)*(x_down-x_up)+x_up; 
    }   
    outerBand->SetPoint      (ipoint, mass, excluded_exp);
    outerBand->SetPointEYhigh(ipoint, excluded_plus2sigma-excluded_exp);
    outerBand->SetPointEYlow (ipoint, excluded_exp-excluded_minus2sigma);
    //std::cout<< "plus2sigma " << ipoint << " " << mass << " " << excluded_plus2sigma << std::endl;

    //-----------------1sigma band
    double excluded_minus1sigma=0;
    if(excluded_idx_minus1sigma == -999){                     //case nothing excluded
      excluded_minus1sigma=highminus1sigma;
    }
    else if(excluded_idx_minus1sigma == notexcluded_idx_minus1sigma){ // case all excluded
      limit->GetEvent(excluded_idx_minus1sigma);
      excluded_minus1sigma=2.5;//tanb;
    }
    else{                                             // case in between
      limit->GetEvent(excluded_idx_minus1sigma);
      double x_up=tanb;
      double y_up=minus1sigma;
      limit->GetEvent(notexcluded_idx_minus1sigma);
      double x_down=tanb;
      double y_down=minus1sigma;
      excluded_minus1sigma=(0.05-y_up)/(y_down-y_up)*(x_down-x_up)+x_up; 
    }   
    //std::cout<< "minus1sigma " << ipoint << " " << mass << " " << excluded_minus1sigma << std::endl;
    double excluded_plus1sigma=0;
    if(excluded_idx_plus1sigma == -999){                     //case nothing excluded
      excluded_plus1sigma=highplus1sigma;
    }
    else if(excluded_idx_plus1sigma == notexcluded_idx_plus1sigma){ // case all excluded
      limit->GetEvent(excluded_idx_plus1sigma);
      excluded_plus1sigma=4;//tanb;
    }
    else{                                             // case in between
      limit->GetEvent(excluded_idx_plus1sigma);
      double x_up=tanb;
      double y_up=plus1sigma;
      limit->GetEvent(notexcluded_idx_plus1sigma);
      double x_down=tanb;
      double y_down=plus1sigma;
      excluded_plus1sigma=(0.05-y_up)/(y_down-y_up)*(x_down-x_up)+x_up; 
    }   
    innerBand->SetPoint      (ipoint, mass, excluded_exp);
    innerBand->SetPointEYhigh(ipoint, excluded_plus1sigma-excluded_exp);
    innerBand->SetPointEYlow (ipoint, excluded_exp-excluded_minus1sigma);
    //std::cout<< "plus1sigma " << ipoint << " " << mass << " " << excluded_plus1sigma << std::endl;
  
    //------------------observed
    double excluded_obs=0;
    if(excluded_idx_obs == -999){                     // case nothing excluded
      excluded_obs=highobserved;
    }
    else if(excluded_idx_obs == notexcluded_idx_obs){ // case all excluded
      limit->GetEvent(excluded_idx_exp);
      excluded_exp=3;//tanb;
    }
    else{                                             // case in between
      limit->GetEvent(excluded_idx_obs);
      double x_up=tanb;
      double y_up=obs;
      limit->GetEvent(notexcluded_idx_obs);
      double x_down=tanb;
      double y_down=obs;
      excluded_obs=(0.05-y_up)/(y_down-y_up)*(x_down-x_up)+x_up; //tanb_ges=(exp_ges-exp_up)/(exp_down-exp_up)*(tanb_down-tanb_up)+tanb_up ; exp_ges = 0.05
    }  
    observed->SetPoint(ipoint, mass, excluded_obs);
    //std::cout<< "observed " << ipoint << " " << mass << " " << excluded_obs << std::endl;

    ipoint++;
  }

  // create plain background
  TGraphAsymmErrors* plain=0;
  if(observed){
    plain=new TGraphAsymmErrors();
    plain->SetPoint(0, observed->GetX()[0], 100.);
    plain->SetPointEYlow (0, 0);
    plain->SetPointEYhigh(0, 100); 
    for(unsigned int imass=0, ipoint=0; imass<bins_.size(); ++imass){
      if(valid_[imass] && observed->GetX()[ipoint]>10){
	plain->SetPoint(ipoint+1, observed->GetX()[ipoint], observed->GetY()[ipoint]); 
	plain->SetPointEYlow (ipoint+1, 0);
 	plain->SetPointEYhigh(ipoint+1, 100);
	//std::cout << ipoint << " " << observed->GetN() << " " << observed->GetX()[ipoint] << std::endl;
	++ipoint;
      }
    }
    plain->SetPoint(observed->GetN(), observed->GetX()[observed->GetN()-1], 100.);
    plain->SetPointEYlow (observed->GetN(), 0);
    plain->SetPointEYhigh(observed->GetN(), 100); 
  }
   
   // create plots for additional comparisons
  std::map<std::string, TGraph*> comparisons; TGraph* comp=0;
  if(arXiv_1211_6956_){ comp = new TGraph(), arXiv_1211_6956 (comp); comp->SetName("arXiv_1211_6956" ); comparisons[std::string("ATLAS H#rightarrow#tau#tau (4.8/fb)")] = comp;}
  if(arXiv_1204_2760_){ comp = new TGraph(); arXiv_1204_2760 (comp); comp->SetName("arXiv_1204_2760" ); comparisons[std::string("ATLAS H^{+} (4.6/fb)")               ] = comp;}
  //if(arXiv_1302_2892_){ comp = new TGraph(); arXiv_1302_2892 (comp); comp->SetName("arXiv_1302_2892" ); comparisons[std::string("CMS bbH#rightarrow 3b (4.8/fb)")     ] = comp;}
  if(arXiv_1302_2892_){ comp = new TGraph(); arXiv_1302_2892 (comp); comp->SetName("arXiv_1302_2892" ); comparisons[std::string("CMS #phi#rightarrowb#bar{b}")     ] = comp;}
  if(arXiv_1205_5736_){ comp = new TGraph(); arXiv_1205_5736 (comp); comp->SetName("arXiv_1205_5736" ); comparisons[std::string("CMS H^{+} (2/fb)")                   ] = comp;}
  if(HIG_12_052_     ){ comp = new TGraph(); HIG_12_052_lower(comp); comp->SetName("HIG_12_052_lower"); comparisons[std::string("CMS H^{+} (2-4.9/fb)")               ] = comp;}
  if(HIG_12_052_     ){ comp = new TGraph(); HIG_12_052_upper(comp); comp->SetName("HIG_12_052_upper"); comparisons[std::string("EMPTY")                              ] = comp;}

  // setup contratins from Higgs mass
  std::map<double, TGraphAsymmErrors*> higgsBands;
  if(higgs125_){
    higgsBands[3] = higgsConstraint(directory, 125., 3., model);
    //higgsBands[2] = higgsConstraint(directory, 125., 2., model);
    //higgsBands[1] = higgsConstraint(directory, 125., 1., model);
    //for(unsigned int deltaM=0; deltaM<3; ++deltaM){
    //  higgsBands[3-deltaM] = higgsConstraint(directory, 125., 4-deltaM, model);
    //}
  }

  // do the plotting
  plottingHypoTest(canv, plain, innerBand, outerBand, expected, observed, higgsBands, comparisons, xaxis_, yaxis_, theory_, min_, max_, log_, transparent_, expectedOnly_, outerband_); 
  /// setup the CMS Preliminary
  //CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);
  TPaveText* cmsprel  = new TPaveText(0.145, 0.835+0.06, 0.145+0.30, 0.835+0.16, "NDC");
  cmsprel->SetBorderSize(   0 );
  cmsprel->SetFillStyle(    0 );
  cmsprel->SetTextAlign(   12 );
  cmsprel->SetTextSize ( 0.03 );
  cmsprel->SetTextColor(    1 );
  cmsprel->SetTextFont (   62 );
  cmsprel->AddText(dataset_.c_str());
  cmsprel->Draw();

  // write results to files
  if(png_){
    canv.Print(std::string(output_).append("_").append(extralabel_).append(label_).append(".png").c_str());
  }
  if(pdf_){
    canv.Print(std::string(output_).append("_").append(extralabel_).append(label_).append(".pdf").c_str());
    canv.Print(std::string(output_).append("_").append(extralabel_).append(label_).append(".eps").c_str());
  }
  if(txt_){
    print(std::string(output_).append("_").append(extralabel_).append(label_).c_str(), outerBand, innerBand, expected, observed, "txt");
    print(std::string(output_).append("_").append(extralabel_).append(label_).c_str(), outerBand, innerBand, expected, observed, "tex");
  }
  if(root_){
    TFile* output = new TFile(std::string("limits_").append(extralabel_).append(label_).append(".root").c_str(), "update");
    if(!output->cd(output_.c_str())){
      output->mkdir(output_.c_str());
      output->cd(output_.c_str());
    }
    if(observed){ 
      observed ->Write("observed" );
    }
    expected ->Write("expected" );
    //innerBand->Write("innerBand");
    //outerBand->Write("outerBand");
    // auxiliary graphs
    //if(plain) plain->Write("plain");
    output->Close();
  }
  return;
}
