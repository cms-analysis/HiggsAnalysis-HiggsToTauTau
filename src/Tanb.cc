#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"
#include "vector"

/// This is the core plotting routine that can also be used within
/// root macros. It is therefore not element of the PlotLimits class.
void plottingTanb(TCanvas& canv, TGraphAsymmErrors* plain_1, TGraphAsymmErrors* plain_2, TGraphAsymmErrors* innerBand_1, TGraphAsymmErrors* innerBand_2, TGraphAsymmErrors* innerBand_3, TGraphAsymmErrors* outerBand_1, TGraphAsymmErrors* outerBand_2, TGraphAsymmErrors* outerBand_3, TGraph* expected_1, TGraph* expected_2, TGraph* expected_3, TGraph* observed_1, TGraph* observed_2, TGraph* observed_3, std::map<double, TGraphAsymmErrors*> higgsBands, std::map<std::string, TGraph*> comparisons, std::string& xaxis, std::string& yaxis, std::string& theory, double min=0., double max=50., bool log=false, bool transparent=false, bool expectedOnly=false, bool plotOuterBand=true, bool MSSMvsSM=true, std::string HIG="");

struct myclass {
  bool operator() (int i,int j) { return (i<j);}
} myobject;

void
PlotLimits::plotTanb(TCanvas& canv, const char* directory, std::string HIG)
{
  //separate between MSSMvsSM and MSSMvsBG
  double exclusion_=0;
  if(MSSMvsSM_) exclusion_=0.05;
  else exclusion_=1;
  //different MSSM scenarios
  std::string extralabel_ = "";
  const char* model;
  double tanbHigh, tanbLow, tanbLowHigh;
  if(theory_=="MSSM m_{h}^{max} scenario") {extralabel_= "mhmax-"; model = "mhmax-mu+200"; tanbHigh=60; tanbLow=0.5; tanbLowHigh=2;}
  if(theory_=="MSSM m_{h}^{mod-} scenario") {extralabel_= "mhmodm-"; model = "mhmodm"; tanbHigh=60; tanbLow=0.5; tanbLowHigh=2;}
  if(theory_=="MSSM m_{h}^{mod+} scenario") {extralabel_= "mhmodp-"; model = "mhmodp"; tanbHigh=60; tanbLow=0.5; tanbLowHigh=2;}
  if(theory_=="MSSM low m_{H} scenario") {extralabel_= "lowmH-"; model = "lowmH"; tanbHigh=9.5; tanbLow=1.5; tanbLowHigh=2;}
  if(theory_=="MSSM light stau scenario") {extralabel_= "lightstau1-"; model = "lightstau1"; tanbHigh=60; tanbLow=0.5; tanbLowHigh=3;}
  if(theory_=="MSSM tauphobic scenario") {extralabel_= "tauphobic-"; model = "tauphobic"; tanbHigh=50; tanbLow=0.5; tanbLowHigh=2;}
  if(theory_=="MSSM light stop scenario") {extralabel_= "lightstop-"; model = "lightstop"; tanbHigh=50; tanbLow=0.7; tanbLowHigh=2;}

  // set up styles
  SetStyle();
 
  TGraphAsymmErrors* plain_1=0;
  TGraphAsymmErrors* plain_2=0;
  plain_1 = new TGraphAsymmErrors();
  plain_2 = new TGraphAsymmErrors();

  TGraph* expected_1 = 0;
  TGraphAsymmErrors* innerBand_1 = 0;
  TGraphAsymmErrors* outerBand_1 = 0;
  TGraph* observed_1 = 0;
  expected_1 = new TGraph();
  innerBand_1 = new TGraphAsymmErrors();
  outerBand_1 = new TGraphAsymmErrors();
  observed_1 = new TGraph();

  TGraph* expected_2 = 0;
  TGraphAsymmErrors* innerBand_2 = 0;
  TGraphAsymmErrors* outerBand_2 = 0;
  TGraph* observed_2 = 0;
  expected_2 = new TGraph();
  innerBand_2 = new TGraphAsymmErrors();
  outerBand_2 = new TGraphAsymmErrors();
  observed_2 = new TGraph();

  TGraph* expected_3 = 0;
  TGraphAsymmErrors* innerBand_3 = 0;
  TGraphAsymmErrors* outerBand_3 = 0;
  TGraph* observed_3 = 0;
  expected_3 = new TGraph();
  innerBand_3 = new TGraphAsymmErrors();
  outerBand_3 = new TGraphAsymmErrors();
  observed_3 = new TGraph();

  if(HIG != ""){
    std::string HIG_save = HIG;
    // observed limit
    if(!expectedOnly_){
      PlotLimits::fillCentral(HIG_save.c_str(), observed_1, HIG_save.append("-obs").c_str()); HIG_save = HIG;
    }
    // expected limit
    PlotLimits::fillCentral(HIG_save.c_str(), expected_1, HIG_save.append("-exp").c_str()); HIG_save = HIG;
    // 1-sigma uncertainty band
    PlotLimits::fillBand(HIG_save.c_str(), innerBand_1, HIG_save.c_str(), true); HIG_save = HIG;
    // 2-sigma uncertainty band
    PlotLimits::fillBand(HIG_save.c_str(), outerBand_1, HIG_save.c_str(), false); HIG_save = HIG;
  }
  else{
  int ipoint_exp=0, ipoint_obs=0;
  for(unsigned int imass=0, ipoint=0; imass<bins_.size(); ++imass){
    // buffer mass value
    float mass = bins_[imass];
   
    ofstream exclusion;  // saves the exclusion limits within the directory so it can be used to throw toys only in regions near the exclusion limit
    exclusion.open(TString::Format("%s/%d/exclusion_%d.out", directory, (int)mass, (int)mass)); 

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
    std::vector<double> v_minus2sigma;
    std::vector<double> v_minus1sigma;
    std::vector<double> v_exp;
    std::vector<double> v_plus1sigma;
    std::vector<double> v_plus2sigma;
    std::vector<double> v_obs;
    double minus2sigma_a, minus1sigma_a, exp_a, plus1sigma_a, plus2sigma_a, obs_a, tanb_a; //to determine the crosspoints
    double minus2sigma_b, minus1sigma_b, exp_b, plus1sigma_b, plus2sigma_b, obs_b, tanb_b; //to determine the crosspoints
    int np_minus2sigma=0, np_minus1sigma=0, np_exp=0, np_plus1sigma=0, np_plus2sigma=0, np_obs=0; //to count up to 4 points for each. This points are used to create the asymmetric error graphs. Since at some masses there are cases for which scanning from top tanb to bottom tanb leads to exclusion cases like: excluded - not-excluded - excluded - notexcluded. So first point is always on top. Between first and second point there is a excluded region. Between second and third the region is not excluded and between third and fourth the region is once again excluded. If we just have a top exclusion we simple fix the points to tanb=0.5 (depending on the model), so that the graph is not visible. 
    for(int i=0; i<nevent; ++i){
      limit->GetEntry(index[i]);
      if (i==0) {
	v_minus2sigma.push_back(tanbHigh);
	if( minus2sigma>exclusion_ ) v_minus2sigma.push_back((minus2sigma+(1-exclusion_))*tanb);
	np_minus2sigma++;
	v_minus1sigma.push_back(tanbHigh);
        if( minus1sigma>exclusion_ ) v_minus1sigma.push_back((minus1sigma+(1-exclusion_))*tanb);
	np_minus1sigma++;
	v_exp.push_back(tanbHigh);
        if( exp>exclusion_ ) v_exp.push_back((exp+(1-exclusion_))*tanb);
	np_exp++;
	v_plus1sigma.push_back(tanbHigh);
	if( plus1sigma>exclusion_ ) v_plus1sigma.push_back((plus1sigma+(1-exclusion_))*tanb);
	np_plus1sigma++;
	v_plus2sigma.push_back(tanbHigh);
	if( plus2sigma>exclusion_ ) v_plus2sigma.push_back((plus2sigma+(1-exclusion_))*tanb);
	np_plus2sigma++;
	v_obs.push_back(tanbHigh);
	if( obs>exclusion_ ) v_obs.push_back((obs+(1-exclusion_))*tanb);
	np_obs++;
      }
      //std::cout<< "event i   " << tanb << ' ' << minus2sigma << ' ' << minus1sigma << ' ' << exp << ' ' << plus1sigma<< ' ' << plus2sigma<< ' ' << obs << std::endl;
      minus2sigma_a = minus2sigma;
      minus1sigma_a = minus1sigma;
      exp_a = exp;
      plus1sigma_a = plus1sigma;
      plus2sigma_a = plus2sigma;
      obs_a = obs;
      tanb_a = tanb;
      if(i+1<nevent){
	limit->GetEntry(index[i+1]);
	//std::cout<<"event i+1 "<< tanb << ' ' << minus2sigma << ' ' << minus1sigma << ' ' << exp << ' ' << plus1sigma<< ' ' << plus2sigma<< ' ' << obs << std::endl;
	minus2sigma_b = minus2sigma;
	minus1sigma_b = minus1sigma;
	exp_b = exp;
	plus1sigma_b = plus1sigma;
	plus2sigma_b = plus2sigma;
	obs_b = obs;
	tanb_b = tanb;
      }
      else { // for excluded at last tanb point we need a point at bottom
	minus2sigma_b = 999;
	minus1sigma_b = 999;
	exp_b = 999;
	plus1sigma_b = 999;
	plus2sigma_b = 999;
	obs_b = 999;	
	tanb_b = tanbLow;
      }
      limit->GetEvent(index[i]);
      // -2sigma
      if(minus2sigma_a == exclusion_) {v_minus2sigma.push_back(tanb_a);}
      if((minus2sigma_a < exclusion_ && minus2sigma_b > exclusion_) || (minus2sigma_a > exclusion_ && minus2sigma_b < exclusion_)) {
	double x_up=tanb_a;
	double y_up=minus2sigma_a;
	double x_down=tanb_b;
	double y_down=minus2sigma_b;
	v_minus2sigma.push_back( (exclusion_-y_up)/(y_down-y_up)*(x_down-x_up)+x_up ); 	
	//std::cout<< tanb << " -2sigma " << (exclusion_-y_up)/(y_down-y_up)*(x_down-x_up)+x_up << std::endl;  
	np_minus2sigma++;
      }
      // -1sigma
      if(minus1sigma_a == exclusion_) {v_minus1sigma.push_back(tanb_a);}
      if((minus1sigma_a < exclusion_ && minus1sigma_b > exclusion_) || (minus1sigma_a > exclusion_ && minus1sigma_b < exclusion_)) {
	double x_up=tanb_a;
	double y_up=minus1sigma_a;
	double x_down=tanb_b;
	double y_down=minus1sigma_b;
	v_minus1sigma.push_back( (exclusion_-y_up)/(y_down-y_up)*(x_down-x_up)+x_up ); 	
	//std::cout<< tanb << " -1sigma " << (exclusion_-y_up)/(y_down-y_up)*(x_down-x_up)+x_up << std::endl;  
	np_minus1sigma++;
      }
      // expected
      if(exp_a == exclusion_) {v_exp.push_back(tanb_a);}
      if((exp_a < exclusion_ && exp_b > exclusion_) || (exp_a > exclusion_ && exp_b < exclusion_)) {
	double x_up=tanb_a;
	double y_up=exp_a;
	double x_down=tanb_b;
	double y_down=exp_b;
	v_exp.push_back( (exclusion_-y_up)/(y_down-y_up)*(x_down-x_up)+x_up ); 	
	//std::cout<< tanb << " expected " << (exclusion_-y_up)/(y_down-y_up)*(x_down-x_up)+x_up << std::endl;  
	np_exp++;
      }
      // +1sigma
      if(plus1sigma_a == exclusion_) {v_plus1sigma.push_back(tanb_a);}
      if((plus1sigma_a < exclusion_ && plus1sigma_b > exclusion_) || (plus1sigma_a > exclusion_ && plus1sigma_b < exclusion_)) {
	double x_up=tanb_a;
	double y_up=plus1sigma_a;
	double x_down=tanb_b;
	double y_down=plus1sigma_b;
	v_plus1sigma.push_back( (exclusion_-y_up)/(y_down-y_up)*(x_down-x_up)+x_up ); 	
	//std::cout<< tanb << " +1sigma " << (exclusion_-y_up)/(y_down-y_up)*(x_down-x_up)+x_up << std::endl;  
	np_plus1sigma++;
      }
      // +2sigma
      if(plus2sigma_a == exclusion_) {v_plus2sigma.push_back(tanb_a);}
      if((plus2sigma_a < exclusion_ && plus2sigma_b > exclusion_) || (plus2sigma_a > exclusion_ && plus2sigma_b < exclusion_)) {
	double x_up=tanb_a;
	double y_up=plus2sigma_a;
	double x_down=tanb_b;
	double y_down=plus2sigma_b;
	v_plus2sigma.push_back( (exclusion_-y_up)/(y_down-y_up)*(x_down-x_up)+x_up ); 	
	//std::cout<< tanb << " +2sigma " << (exclusion_-y_up)/(y_down-y_up)*(x_down-x_up)+x_up << std::endl;  
	np_plus2sigma++;
      }
      // observed
      if(obs_a == exclusion_) {v_obs.push_back(tanb_a);}
      if((obs_a < exclusion_ && obs_b > exclusion_) || (obs_a > exclusion_ && obs_b < exclusion_)) {
	double x_up=tanb_a;
	double y_up=obs_a;
	double x_down=tanb_b;
	double y_down=obs_b;
	v_obs.push_back( (exclusion_-y_up)/(y_down-y_up)*(x_down-x_up)+x_up ); 	
	//std::cout<< tanb << " observed " << (exclusion_-y_up)/(y_down-y_up)*(x_down-x_up)+x_up << std::endl;  
	np_obs++;
      }
    }
    //number of points must be 4
    while(np_minus2sigma<4){
      if(v_minus2sigma[1]<tanbLowHigh) {
	v_minus2sigma.insert(v_minus2sigma.begin()+1, 2, tanbLowHigh );
	np_minus2sigma++;
	np_minus2sigma++;
      }
      else{
	v_minus2sigma.push_back( tanbLow );
	np_minus2sigma++;
      }
    }    
    while(np_minus1sigma<4){
      if(v_minus1sigma[1]<tanbLowHigh) {
	v_minus1sigma.insert(v_minus1sigma.begin()+1, 2, tanbLowHigh );
	np_minus1sigma++;
	np_minus1sigma++;
      }
      else{
	v_minus1sigma.push_back( tanbLow );
	np_minus1sigma++;
      }
    }    
    while(np_exp<4){
      v_exp.push_back( tanbLow );
      np_exp++;
    }    
    while(np_plus1sigma<4){
      if(v_plus1sigma[1]<tanbLowHigh) {
	v_plus1sigma.insert(v_plus1sigma.begin()+1, 2, tanbLowHigh );
	np_plus1sigma++;
	np_plus1sigma++;
      }
      else{
	v_plus1sigma.push_back( tanbLow );
	np_plus1sigma++;
      }
    } 
    while(np_plus2sigma<4){
      if(v_plus2sigma[1]<tanbLowHigh) {
	v_plus2sigma.insert(v_plus2sigma.begin()+1, 2, tanbLowHigh );
	np_plus2sigma++;
	np_plus2sigma++;
      }
      else{
	v_plus2sigma.push_back( tanbLow );
	np_plus2sigma++;
      }
    } 
    while(np_obs<4){
      v_obs.push_back( tanbLow );
      np_obs++;
    }
    
    /*for(unsigned int i=0; i<v_minus2sigma.size(); i++){
      std::cout << i << " -2sigma " << v_minus2sigma[i] <<std::endl;
    }
    for(unsigned int i=0; i<v_minus1sigma.size(); i++){
      std::cout << i << " -1sigma " << v_minus1sigma[i] <<std::endl;
    }
    for(unsigned int i=0; i<v_exp.size(); i++){
      std::cout << i << " exp " << v_exp[i] <<std::endl;
    }    
    for(unsigned int i=0; i<v_plus1sigma.size(); i++){
      std::cout << i << " +1sigma " << v_plus1sigma[i] <<std::endl;
    }  
    for(unsigned int i=0; i<v_plus2sigma.size(); i++){
      std::cout << i << " +2sigma " << v_plus2sigma[i] <<std::endl;
    }  
    for(unsigned int i=0; i<v_obs.size(); i++){
      std::cout << i << " obs " << v_obs[i] <<std::endl;
      }*/
    
    //fill the graphs 
    //expected - excluded region is by definition between cross point 1 and 2 and between 3 and 4
    expected_1->SetPoint(ipoint, mass, v_exp[1]);    
    if(np_exp>2){     
      expected_2->SetPoint(ipoint_exp, mass, v_exp[2]); 
      expected_3->SetPoint(ipoint_exp, mass, v_exp[3]);    
      ipoint_exp++;
    }
    //observed - excluded region is by definition between cross point 1 and 2 and between 3 and 4
    observed_1->SetPoint(ipoint, mass, v_obs[1]);  
    plain_1->SetPoint(ipoint, mass, v_obs[1]);
    plain_1->SetPointEYhigh(ipoint, v_obs[0]-v_obs[1]);
    plain_1->SetPointEYlow (ipoint, 0); 
    if(np_obs>2){
      observed_2->SetPoint(ipoint_obs, mass, v_obs[2]);
      observed_3->SetPoint(ipoint_obs, mass, v_obs[3]);        
      plain_2->SetPoint(ipoint_obs, mass, v_obs[3]);
      plain_2->SetPointEYhigh(ipoint_obs, v_obs[2]-v_obs[3]);
      plain_2->SetPointEYlow (ipoint_obs, 0); 
      ipoint_obs++;
    }
    //innerBand - around expected line at crosspoint 2, 3 and 4 we need the band => 3 points
    innerBand_1->SetPoint(ipoint, mass, v_exp[1]);
    innerBand_1->SetPointEYhigh(ipoint, v_plus1sigma[1]-v_exp[1]);
    innerBand_1->SetPointEYlow (ipoint, v_exp[1]-v_minus1sigma[1]); 
    innerBand_2->SetPoint(ipoint, mass, v_exp[2]);
    innerBand_2->SetPointEYhigh(ipoint, v_plus1sigma[2]-v_exp[2]);
    innerBand_2->SetPointEYlow (ipoint, v_exp[2]-v_minus1sigma[2]); 
    //outerBand - around expected line at crosspoint 2, 3 and 4 we need the band => 3 points
    outerBand_1->SetPoint(ipoint, mass, v_exp[1]);
    outerBand_1->SetPointEYhigh(ipoint, v_plus2sigma[1]-v_exp[1]);
    outerBand_1->SetPointEYlow (ipoint, v_exp[1]-v_minus2sigma[1]); 
    outerBand_2->SetPoint(ipoint, mass, v_exp[2]);
    outerBand_2->SetPointEYhigh(ipoint, v_plus2sigma[2]-v_exp[2]);
    outerBand_2->SetPointEYlow (ipoint, v_exp[2]-v_minus2sigma[2]);
 
    exclusion << int(mass) << " " << v_minus2sigma[1] << " " << v_minus1sigma[1] << " " << v_exp[1] << " " << v_plus1sigma[1] << " " << v_plus2sigma[1] << " " << v_obs[1] << std::endl; 
    double help_minus2sigma, help_minus1sigma, help_exp, help_plus1sigma, help_plus2sigma, help_obs;
    if (v_minus2sigma[2]<tanbLowHigh && v_minus2sigma[2]>tanbLow) help_minus2sigma=v_minus2sigma[2];
    else if (v_minus2sigma[2]==tanbLowHigh) help_minus2sigma=v_minus2sigma[3];
    else help_minus2sigma=v_minus2sigma[1];
    if (v_minus1sigma[2]<tanbLowHigh && v_minus1sigma[2]>tanbLow) help_minus1sigma=v_minus1sigma[2];
    else if (v_minus1sigma[2]==tanbLowHigh) help_minus1sigma=v_minus1sigma[3];
    else help_minus1sigma=v_minus1sigma[1];
    if (v_exp[2]!=tanbLow) help_exp=v_exp[2];
    else help_exp=v_exp[1];
    if (v_plus1sigma[2]<tanbLowHigh && v_plus1sigma[2]>tanbLow) help_plus1sigma=v_plus1sigma[2];
    else if (v_plus1sigma[2]==tanbLowHigh) help_plus1sigma=v_plus1sigma[3];
    else help_plus1sigma=v_plus1sigma[1];
    if (v_plus2sigma[2]<tanbLowHigh && v_plus2sigma[2]>tanbLow) help_plus2sigma=v_plus2sigma[2];
    else if (v_plus2sigma[2]==tanbLowHigh) help_plus2sigma=v_plus2sigma[3];
    else help_plus2sigma=v_plus2sigma[1];
    if (v_obs[2]!=tanbLow) help_obs=v_obs[2];
    else help_obs=v_obs[1];
    exclusion << int(mass) << " " << help_minus2sigma << " " << help_minus1sigma << " " << help_exp << " " << help_plus1sigma << " " << help_plus2sigma << " " << help_obs << std::endl; 
    exclusion.close();

    ipoint++;
  }
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
  plottingTanb(canv, plain_1, plain_2, innerBand_1, innerBand_2, innerBand_3, outerBand_1, outerBand_2, outerBand_3, expected_1, expected_2, expected_3, observed_1, observed_2, observed_3, higgsBands, comparisons, xaxis_, yaxis_, theory_, min_, max_, log_, transparent_, expectedOnly_, outerband_, MSSMvsSM_, HIG); 
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
    print(std::string(output_).append("_").append(extralabel_).append(label_).c_str(), outerBand_1, innerBand_1, expected_1, observed_1, outerBand_2, innerBand_2, expected_2, observed_2, tanbLow, tanbHigh, tanbLowHigh, "txt");
    print(std::string(output_).append("_").append(extralabel_).append(label_).c_str(), outerBand_1, innerBand_1, expected_1, observed_1, outerBand_2, innerBand_2, expected_2, observed_2, tanbLow, tanbHigh, tanbLowHigh, "tex");
  }
  if(root_){
    TFile* output = new TFile(std::string("limits_").append(extralabel_).append(label_).append(".root").c_str(), "update");
    if(!output->cd(output_.c_str())){
      output->mkdir(output_.c_str());
      output->cd(output_.c_str());
    }
    if(observed_1){ 
      observed_1 ->Write("observed" );
    }
    expected_1 ->Write("expected" );
    //innerBand->Write("innerBand");
    //outerBand->Write("outerBand");
    // auxiliary graphs
    //if(plain) plain->Write("plain");
    output->Close();
  }
  return;
}
