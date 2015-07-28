#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"
#include <vector>
#include <TF1.h>
#include <TFitResult.h>
#include <TGraph2D.h>
#include <TSpline.h>
#include <TMath.h>

/// This is the core plotting routine that can also be used within
/// root macros. It is therefore not element of the PlotLimits class.
void plottingTanb(TCanvas& canv, TH2D* h2d, std::vector<TGraph*> minus2sigma, std::vector<TGraph*> minus1sigma, std::vector<TGraph*> expected, std::vector<TGraph*> plus1sigma, std::vector<TGraph*> plus2sigma, std::vector<TGraph*> observed, std::vector<TGraph*> injected, std::vector<std::vector<TGraph*>> higgsBands, std::map<std::string, TGraph*> comparisons, std::string& xaxis, std::string& yaxis, std::string& theory, double min=0., double max=50., bool log=false, bool transparent=false, bool expectedOnly=false, bool MSSMvsSM=true, std::string HIG="", bool Brazilian=false, bool azh=false);
void contour2D(TString xvar, int xbins, float xmin, float xmax, TString yvar, int ybins, float ymin, float ymax, float smx=1.0, float smy=1.0, TFile *fOut=0, TString name="contour2D");
TList* contourFromTH2(TH2 *h2in, double threshold, int minPoints=20, bool require_minPoints=true, double multip=1);

void CLsControlPlots(TGraph* graph_minus2sigma, TGraph* graph_minus1sigma, TGraph* graph_expected, TGraph* graph_plus1sigma, TGraph* graph_plus2sigma, TGraph* graph_observed, const char* directory, float mass, int max, int ymax, const char* model);

struct STestFunctor{
  STestFunctor() { sum = 0; }
  void operator() (TObject *aObj) {sum +=1;}
  int sum;
} stestfunctor;

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
  double tanbHigh=0, tanbLow=0, tanbLowHigh=0;
  tanbHigh=tanbLow+tanbLowHigh;
  if(theory_=="MSSM m_{h}^{max} scenario") {extralabel_= "mhmax-"; model = "mhmax-mu+200"; tanbHigh=60; tanbLow=0.5; tanbLowHigh=2;}
  if(theory_=="MSSM m_{h}^{mod-} scenario") {extralabel_= "mhmodm-"; model = "mhmodm"; tanbHigh=60; tanbLow=0.5; tanbLowHigh=2;}
  if(theory_=="MSSM m_{h}^{mod+} scenario") {extralabel_= "mhmodp-"; model = "mhmodp"; tanbHigh=60; tanbLow=0.5; tanbLowHigh=2;}
  if(theory_=="MSSM low-m_{H} scenario") {extralabel_= "lowmH-"; model = "lowmH"; tanbHigh=9.5; tanbLow=1.5; tanbLowHigh=2;}
  if(theory_=="MSSM light-stau scenario") {extralabel_= "lightstau1-"; model = "lightstau1"; tanbHigh=60; tanbLow=0.5; tanbLowHigh=3;}
  if(theory_=="MSSM #scale[1.3]{#bf{#tau}}-phobic scenario") {extralabel_= "tauphobic-"; model = "tauphobic"; tanbHigh=50; tanbLow=1.0; tanbLowHigh=2;}
  if(theory_=="MSSM light-stop scenario") {extralabel_= "lightstopmod-"; model = "lightstopmod"; tanbHigh=60; tanbLow=0.7; tanbLowHigh=2;}
  if(theory_=="MSSM low-tan#beta-high scenario") {extralabel_= "low-tb-high-"; model = "low-tb-high"; tanbHigh=9.5; tanbLow=0.5; tanbLowHigh=2;}
  if(theory_=="2HDM type-I") {extralabel_= "2HDMtyp1-"; model = "2HDMtyp1"; tanbHigh=10; tanbLow=1; tanbLowHigh=2;}
  if(theory_=="2HDM type-II") {extralabel_= "2HDMtyp2-"; model = "2HDMtyp2"; tanbHigh=10; tanbLow=1; tanbLowHigh=2;}

  // set up styles
  SetStyle();

  //vectors of graphs from the tanb-CLs control plots used for tex/txt printing
  std::vector<TGraph*> v_graph_minus2sigma;
  std::vector<TGraph*> v_graph_minus1sigma;
  std::vector<TGraph*> v_graph_expected;
  std::vector<TGraph*> v_graph_plus1sigma;
  std::vector<TGraph*> v_graph_plus2sigma;
  std::vector<TGraph*> v_graph_observed;
  float masses[50];

  int nxbins=0;
  int array_number=0;
  if(model==TString::Format("2HDMtyp1") || model==TString::Format("2HDMtyp2")) array_number = (int)((bins_[bins_.size()-1]-bins_[0])/0.02)+1;
  else if(model==TString::Format("lowmH")) array_number = 30;
  else array_number = (int)(bins_[bins_.size()-1]-bins_[0])/10+1; 
  Double_t xbins[array_number];
  
  if(model==TString::Format("lowmH")) {
    for(double mass=300; mass<3100+1; mass=mass+100){
      xbins[nxbins]=mass;
      nxbins++;
    }
    xbins[nxbins]=3100+1;
  }
  else if(model!=TString::Format("2HDMtyp1") && model!=TString::Format("2HDMtyp2")){
    for(float mass=bins_[0]; mass<bins_[bins_.size()-1]+1; mass=mass+10){
      xbins[nxbins]=mass;
      nxbins++;;
    }
    xbins[nxbins]=bins_[bins_.size()-1]+1;
  }
  else {
    for(double mass=bins_[0]; mass<bins_[bins_.size()-1]+0.01; mass=mass+0.02){
      xbins[nxbins]=mass;
      nxbins++;
    }
    xbins[nxbins]=bins_[bins_.size()-1]+0.01;
  }

  TH2D *plane_minus2sigma = 0, *plane_minus1sigma = 0, *plane_expected = 0, *plane_plus1sigma = 0, *plane_plus2sigma = 0, *plane_observed = 0;

  if(model!=TString::Format("lowmH")) {
    plane_minus2sigma = new TH2D("minus2sigma","minus2sigma", nxbins, xbins, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
    plane_minus1sigma = new TH2D("minus1sigma","minus1sigma", nxbins, xbins, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
    plane_expected    = new TH2D("expected","expected",       nxbins, xbins, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
    plane_plus1sigma  = new TH2D("plus1sigma","plus1sigma",   nxbins, xbins, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
    plane_plus2sigma  = new TH2D("plus2sigma","plus2sigma",   nxbins, xbins, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
    plane_observed    = new TH2D("observed","observed",       nxbins, xbins, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
  }
  else { 
    plane_minus2sigma = new TH2D("minus2sigma","minus2sigma", 29, 300, 3100, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
    plane_minus1sigma = new TH2D("minus1sigma","minus1sigma", 29, 300, 3100, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
    plane_expected    = new TH2D("expected",   "expected",    29, 300, 3100, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
    plane_plus1sigma  = new TH2D("plus1sigma","plus1sigma",   29, 300, 3100, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
    plane_plus2sigma  = new TH2D("plus2sigma","plus2sigma",   29, 300, 3100, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
    plane_observed    = new TH2D("observed","observed",       29, 300, 3100, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
  }


  for(int idx=1; idx<plane_minus2sigma->GetNbinsX()+1; idx++){
    for(int idy=1; idy<plane_minus2sigma->GetNbinsY()+1; idy++){
      plane_minus2sigma->SetBinContent(idx, idy, 1.1);
      plane_minus1sigma->SetBinContent(idx, idy, 1.1);
      plane_expected   ->SetBinContent(idx, idy, 1.1);
      plane_plus1sigma ->SetBinContent(idx, idy, 1.1);
      plane_plus2sigma ->SetBinContent(idx, idy, 1.1);
      plane_observed   ->SetBinContent(idx, idy, 1.1);
    }
  }
  
  TGraph2D* graph_minus2sigma_2d = 0;
  TGraph2D* graph_minus1sigma_2d = 0;
  TGraph2D* graph_expected_2d = 0;
  TGraph2D* graph_plus1sigma_2d = 0;
  TGraph2D* graph_plus2sigma_2d = 0;
  TGraph2D* graph_observed_2d =0;
  TH2D *minus2sigma_th2d =new TH2D("minus2sigma_th2d","minus2sigma_th2d",4*nxbins,xbins[0],xbins[nxbins-1],(int)((tanbHigh-tanbLow)*10-1),tanbLow,tanbHigh);
  TH2D *minus1sigma_th2d =new TH2D("minus1sigma_th2d","minus1sigma_th2d",4*nxbins,xbins[0],xbins[nxbins-1],(int)((tanbHigh-tanbLow)*10-1),tanbLow,tanbHigh);
  TH2D *expected_th2d =new TH2D("expected_th2d","expected_th2d",4*nxbins,xbins[0],xbins[nxbins-1],(int)((tanbHigh-tanbLow)*10-1),tanbLow,tanbHigh);
  TH2D *plus1sigma_th2d =new TH2D("plus1sigma_th2d","plus1sigma_th2d",4*nxbins,xbins[0],xbins[nxbins-1],(int)((tanbHigh-tanbLow)*10-1),tanbLow,tanbHigh);
  TH2D *plus2sigma_th2d =new TH2D("plus2sigma_th2d","plus2sigma_th2d",4*nxbins,xbins[0],xbins[nxbins-1],(int)((tanbHigh-tanbLow)*10-1),tanbLow,tanbHigh);
  TH2D *observed_th2d =new TH2D("observed_th2d","observed_th2d",4*nxbins,xbins[0],xbins[nxbins-1],(int)((tanbHigh-tanbLow)*10-1),tanbLow,tanbHigh);
  
  if(HIG != ""){
    std::cout << "NO LONGER SUPPORTED" << std::endl;
  }
  else{
    //2D Graphs 
    int kTwod=0;
    graph_minus2sigma_2d = new TGraph2D();
    graph_minus1sigma_2d = new TGraph2D();
    graph_expected_2d = new TGraph2D();
    graph_plus1sigma_2d = new TGraph2D();
    graph_plus2sigma_2d = new TGraph2D();
    graph_observed_2d = new TGraph2D();
    
    for(unsigned int imass=0; imass<bins_.size(); ++imass){
      // buffer mass value
      float mass = bins_[imass];    
      //control plots
      TGraph* graph_minus2sigma = new TGraph();
      TGraph* graph_minus1sigma = new TGraph();
      TGraph* graph_expected = new TGraph();
      TGraph* graph_plus1sigma = new TGraph();
      TGraph* graph_plus2sigma = new TGraph();
      TGraph* graph_observed = new TGraph();
      //log scale for plotting
      TGraph* graph_minus2sigma_log = new TGraph();
      TGraph* graph_minus1sigma_log = new TGraph();
      TGraph* graph_expected_log = new TGraph();
      TGraph* graph_plus1sigma_log = new TGraph();
      TGraph* graph_plus2sigma_log = new TGraph();
      TGraph* graph_observed_log = new TGraph();


      TString fullpath = TString::Format("%s/%d/HypothesisTest.root", directory, (int)mass);
      if (model==TString::Format("2HDMtyp1") || model==TString::Format("2HDMtyp2")){ 
	if(bins_[imass]!=(int)bins_[imass]) fullpath = TString::Format("%s/%0.1f/HypothesisTest.root", directory, bins_[imass]);
	else fullpath = TString::Format("%s/%d/HypothesisTest.root",directory,(int)mass);
      }
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
      //The array index contains the entry numbers in increasing order in respect to tanb
      TMath::Sort(nevent,limit->GetV1(),index,false); //changed from true (=default) =decreasing order
      int k=0; double xmax=0; double ymax=0; //stuff needed for fitting;
      // loop to find the crosspoint between low and high exclusion (tanbLowHigh)_observed   ->SetBinContent(plane_observed   ->GetXaxis()->FindBin(mass), plane_observed   ->GetYaxis()->FindBin(tanb), obs/exclusion_);
      for(int i=0; i<nevent; ++i){
	limit->GetEntry(index[i]);
	//filling control plots
	graph_minus2sigma->SetPoint(k, tanb, minus2sigma/exclusion_);
	graph_minus1sigma->SetPoint(k, tanb, minus1sigma/exclusion_);
	graph_expected   ->SetPoint(k, tanb, exp/exclusion_);
	graph_plus1sigma ->SetPoint(k, tanb, plus1sigma/exclusion_);
	graph_plus2sigma ->SetPoint(k, tanb, plus2sigma/exclusion_);
	graph_observed   ->SetPoint(k, tanb, obs/exclusion_);
	//filling plots for linear and spline fits (log makes the splines more stable)
	if(minus2sigma==0) minus2sigma=0.0001;
	if(minus1sigma==0) minus1sigma=0.0001;
	if(exp==0) exp=0.0001;
	if(plus1sigma==0) plus1sigma=0.0001;
	if(plus2sigma==0) plus2sigma=0.0001;
	if(obs==0) obs=0.0001;
	graph_minus2sigma_log->SetPoint(k, tanb, TMath::Log(minus2sigma/exclusion_));
	graph_minus1sigma_log->SetPoint(k, tanb, TMath::Log(minus1sigma/exclusion_));
	graph_expected_log   ->SetPoint(k, tanb, TMath::Log(exp/exclusion_));
	graph_plus1sigma_log ->SetPoint(k, tanb, TMath::Log(plus1sigma/exclusion_));
	graph_plus2sigma_log ->SetPoint(k, tanb, TMath::Log(plus2sigma/exclusion_));
	graph_observed_log   ->SetPoint(k, tanb, TMath::Log(obs/exclusion_));
	k++;      
	for(int j=0; j<graph_minus2sigma->GetN(); j++){ 
	  if(graph_minus2sigma->GetY()[j]>ymax && graph_minus2sigma->GetX()[j]>=1) {ymax=graph_minus2sigma->GetY()[j]; xmax=graph_minus2sigma->GetX()[j]; tanbLowHigh=xmax;} //tanb>=1 hardcoded to fix that point 	  
	}

	// Fill TH2D with calculated limit points
	if(FitMethod_==0 || FitMethod_==1 || FitMethod_==3 || FitMethod_==4){ //linear fit=0; spline=1; spline+linear=3; linear+spline=4
	  plane_minus2sigma->SetBinContent(plane_minus2sigma->GetXaxis()->FindBin(mass), plane_minus2sigma->GetYaxis()->FindBin(tanb), TMath::Log(minus2sigma/exclusion_));
	  plane_minus1sigma->SetBinContent(plane_minus1sigma->GetXaxis()->FindBin(mass), plane_minus1sigma->GetYaxis()->FindBin(tanb), TMath::Log(minus1sigma/exclusion_));
	  plane_expected   ->SetBinContent(plane_expected   ->GetXaxis()->FindBin(mass), plane_expected   ->GetYaxis()->FindBin(tanb), TMath::Log(exp/exclusion_));
	  plane_plus1sigma ->SetBinContent(plane_plus1sigma ->GetXaxis()->FindBin(mass), plane_plus1sigma ->GetYaxis()->FindBin(tanb), TMath::Log(plus1sigma/exclusion_));
	  plane_plus2sigma ->SetBinContent(plane_plus2sigma ->GetXaxis()->FindBin(mass), plane_plus2sigma ->GetYaxis()->FindBin(tanb), TMath::Log(plus2sigma/exclusion_));
	  plane_observed   ->SetBinContent(plane_observed   ->GetXaxis()->FindBin(mass), plane_observed   ->GetYaxis()->FindBin(tanb), TMath::Log(obs/exclusion_));
	}
	else if(FitMethod_==2){ //TGraph2D interpolation
	  graph_minus2sigma_2d->SetPoint(kTwod,mass,tanb,minus2sigma/exclusion_);
	  graph_minus1sigma_2d->SetPoint(kTwod,mass,tanb,minus1sigma/exclusion_);
	  graph_expected_2d->SetPoint(kTwod,mass,tanb,exp/exclusion_);
	  graph_plus1sigma_2d->SetPoint(kTwod,mass,tanb,plus1sigma/exclusion_);
	  graph_plus2sigma_2d->SetPoint(kTwod,mass,tanb,plus2sigma/exclusion_);
	  graph_observed_2d->SetPoint(kTwod,mass,tanb,obs/exclusion_);
	  kTwod++;
	}	
      }
      // if(mass==130) {
      // 	    TCanvas *c5 = new TCanvas("c5", "c5", 600, 600);
      // 	    TSpline3 *spline = new TSpline3("spline", graph_observed);
      // 	    //spline->SaveAs("spline.root");
      // 	    graph_expected->Draw("AP*");
      // 	    spline->Draw("SAME");
      // 	    c5->Print("c2.png");
      // 	  }
      //  if(mass==140) {
      // 	    TCanvas *c5 = new TCanvas("c5", "c5", 600, 600);
      // 	    TSpline3 *spline = new TSpline3("spline", graph_observed);
      // 	    //spline->SaveAs("spline.root");
      // 	    graph_expected->Draw("AP*");
      // 	    spline->Draw("SAME");
      // 	    c5->Print("c3.png");
      // 	  }

      //control plot plotting
      CLsControlPlots(graph_minus2sigma, graph_minus1sigma, graph_expected, graph_plus1sigma, graph_plus2sigma, graph_observed, directory, mass, xmax, ymax, model);
      //push back graphs and save mass for tex/txt output printing
      v_graph_minus2sigma.push_back(graph_minus2sigma);
      v_graph_minus1sigma.push_back(graph_minus1sigma);
      v_graph_expected.push_back(graph_expected);
      v_graph_plus1sigma.push_back(graph_plus1sigma);
      v_graph_plus2sigma.push_back(graph_plus2sigma);
      v_graph_observed.push_back(graph_observed);
      masses[imass]=mass;
     
      // Interpolation along the y-axis for filling everything in between
      if(FitMethod_==0 || FitMethod_==1 || FitMethod_==3 || FitMethod_==4){ //linear fit=0; spline=1; spline+linear=3; linear+spline=4
	limit->GetEntry(index[0]);
	float tbmin=tanb; 
	limit->GetEntry(index[nevent-1]);
	float tbmax=tanb; 
	for(int idy=1; idy<plane_minus2sigma->GetNbinsY()+1; idy++){
	  if (plane_minus2sigma->GetYaxis()->GetBinCenter(idy) > tbmin && plane_minus2sigma->GetYaxis()->GetBinCenter(idy) < tbmax ){
	    if(FitMethod_==0 || FitMethod_==4 ){
	      plane_minus2sigma->SetBinContent(plane_minus2sigma->GetXaxis()->FindBin(mass), idy, graph_minus2sigma_log->Eval(plane_minus2sigma->GetYaxis()->GetBinLowEdge(idy)));
	      plane_minus1sigma->SetBinContent(plane_minus1sigma->GetXaxis()->FindBin(mass), idy, graph_minus1sigma_log->Eval(plane_minus1sigma->GetYaxis()->GetBinLowEdge(idy)));
	      plane_expected   ->SetBinContent(plane_expected   ->GetXaxis()->FindBin(mass), idy, graph_expected_log   ->Eval(plane_expected   ->GetYaxis()->GetBinLowEdge(idy)));
	      plane_plus1sigma ->SetBinContent(plane_plus1sigma ->GetXaxis()->FindBin(mass), idy, graph_plus1sigma_log ->Eval(plane_plus1sigma ->GetYaxis()->GetBinLowEdge(idy)));
	      plane_plus2sigma ->SetBinContent(plane_plus2sigma ->GetXaxis()->FindBin(mass), idy, graph_plus2sigma_log ->Eval(plane_plus2sigma ->GetYaxis()->GetBinLowEdge(idy)));
	      plane_observed   ->SetBinContent(plane_observed   ->GetXaxis()->FindBin(mass), idy, graph_observed_log   ->Eval(plane_observed   ->GetYaxis()->GetBinLowEdge(idy)));
	    }
	    else if(FitMethod_==1 || FitMethod_==3){
	      plane_minus2sigma->SetBinContent(plane_minus2sigma->GetXaxis()->FindBin(mass), idy, graph_minus2sigma_log->Eval(plane_minus2sigma->GetYaxis()->GetBinLowEdge(idy), 0, "S"));
	      plane_minus1sigma->SetBinContent(plane_minus1sigma->GetXaxis()->FindBin(mass), idy, graph_minus1sigma_log->Eval(plane_minus1sigma->GetYaxis()->GetBinLowEdge(idy), 0, "S"));
	      plane_expected   ->SetBinContent(plane_expected   ->GetXaxis()->FindBin(mass), idy, graph_expected_log   ->Eval(plane_expected   ->GetYaxis()->GetBinLowEdge(idy), 0, "S"));
	      plane_plus1sigma ->SetBinContent(plane_plus1sigma ->GetXaxis()->FindBin(mass), idy, graph_plus1sigma_log ->Eval(plane_plus1sigma ->GetYaxis()->GetBinLowEdge(idy), 0, "S"));
	      plane_plus2sigma ->SetBinContent(plane_plus2sigma ->GetXaxis()->FindBin(mass), idy, graph_plus2sigma_log ->Eval(plane_plus2sigma ->GetYaxis()->GetBinLowEdge(idy), 0, "S"));
	      plane_observed   ->SetBinContent(plane_observed   ->GetXaxis()->FindBin(mass), idy, graph_observed_log   ->Eval(plane_observed   ->GetYaxis()->GetBinLowEdge(idy), 0, "S"));
	    }
	  }
	  else if(plane_minus2sigma->GetYaxis()->GetBinCenter(idy) < tbmin){
	    plane_minus2sigma->SetBinContent(plane_minus2sigma->GetXaxis()->FindBin(mass), idy, graph_minus2sigma_log->GetY()[0]);
	    plane_minus1sigma->SetBinContent(plane_minus1sigma->GetXaxis()->FindBin(mass), idy, graph_minus1sigma_log->GetY()[0]);
	    plane_expected   ->SetBinContent(plane_expected   ->GetXaxis()->FindBin(mass), idy, graph_expected_log   ->GetY()[0]);
	    plane_plus1sigma ->SetBinContent(plane_plus1sigma ->GetXaxis()->FindBin(mass), idy, graph_plus1sigma_log ->GetY()[0]);
	    plane_plus2sigma ->SetBinContent(plane_plus2sigma ->GetXaxis()->FindBin(mass), idy, graph_plus2sigma_log ->GetY()[0]);
	    plane_observed   ->SetBinContent(plane_observed   ->GetXaxis()->FindBin(mass), idy, graph_observed_log   ->GetY()[0]);
	  }
	  else if(plane_minus2sigma->GetYaxis()->GetBinCenter(idy) > tbmax){
	    plane_minus2sigma->SetBinContent(plane_minus2sigma->GetXaxis()->FindBin(mass), idy, graph_minus2sigma_log->GetY()[graph_minus2sigma_log->GetN()-1]);
	    plane_minus1sigma->SetBinContent(plane_minus1sigma->GetXaxis()->FindBin(mass), idy, graph_minus1sigma_log->GetY()[graph_minus1sigma_log->GetN()-1]);
	    plane_expected   ->SetBinContent(plane_expected   ->GetXaxis()->FindBin(mass), idy, graph_expected_log   ->GetY()[graph_expected_log   ->GetN()-1]);
	    plane_plus1sigma ->SetBinContent(plane_plus1sigma ->GetXaxis()->FindBin(mass), idy, graph_plus1sigma_log ->GetY()[graph_plus1sigma_log ->GetN()-1]);
	    plane_plus2sigma ->SetBinContent(plane_plus2sigma ->GetXaxis()->FindBin(mass), idy, graph_plus2sigma_log ->GetY()[graph_plus2sigma_log ->GetN()-1]);
	    plane_observed   ->SetBinContent(plane_observed   ->GetXaxis()->FindBin(mass), idy, graph_observed_log   ->GetY()[graph_observed_log   ->GetN()-1]);
	  }
	}
      }
    }
  }	

  // Interpolation along the x-axis for filling everything in between
  if(FitMethod_==0 || FitMethod_==1 || FitMethod_==3){ //linear fit=0; spline=1; spline+linear=3; linear+spline=4
    for(int idy=0; idy<plane_minus2sigma->GetNbinsY()+1; idy++){
      TGraph* graph_minus2sigma_tanb = new TGraph();
      TGraph* graph_minus1sigma_tanb = new TGraph();
      TGraph* graph_expected_tanb = new TGraph();
      TGraph* graph_plus1sigma_tanb = new TGraph();
      TGraph* graph_plus2sigma_tanb = new TGraph();
      TGraph* graph_observed_tanb = new TGraph();
      for(unsigned int imass=0; imass<bins_.size(); ++imass){
	// buffer mass value
	float mass = bins_[imass];
	graph_minus2sigma_tanb->SetPoint(imass, mass, plane_minus2sigma->GetBinContent(plane_minus2sigma->GetXaxis()->FindBin(mass), idy));
	graph_minus1sigma_tanb->SetPoint(imass, mass, plane_minus1sigma->GetBinContent(plane_minus1sigma->GetXaxis()->FindBin(mass), idy));
	graph_expected_tanb   ->SetPoint(imass, mass, plane_expected   ->GetBinContent(plane_expected   ->GetXaxis()->FindBin(mass), idy));
	graph_plus1sigma_tanb ->SetPoint(imass, mass, plane_plus1sigma ->GetBinContent(plane_plus1sigma ->GetXaxis()->FindBin(mass), idy));
	graph_plus2sigma_tanb ->SetPoint(imass, mass, plane_plus2sigma ->GetBinContent(plane_plus2sigma ->GetXaxis()->FindBin(mass), idy));
	graph_observed_tanb   ->SetPoint(imass, mass, plane_observed   ->GetBinContent(plane_observed   ->GetXaxis()->FindBin(mass), idy));
      }
      //graph_observed_tanb->SaveAs("graph.root");
      for(int idx=0; idx<plane_minus2sigma->GetNbinsX()+1; idx++){
	if(FitMethod_==0 || FitMethod_==3){
	  plane_minus2sigma->SetBinContent(idx, idy, graph_minus2sigma_tanb->Eval(plane_minus2sigma->GetXaxis()->GetBinLowEdge(idx)));
	  plane_minus1sigma->SetBinContent(idx, idy, graph_minus1sigma_tanb->Eval(plane_minus1sigma->GetXaxis()->GetBinLowEdge(idx)));
	  plane_expected   ->SetBinContent(idx, idy, graph_expected_tanb   ->Eval(plane_expected   ->GetXaxis()->GetBinLowEdge(idx)));
	  plane_plus1sigma ->SetBinContent(idx, idy, graph_plus1sigma_tanb ->Eval(plane_plus1sigma ->GetXaxis()->GetBinLowEdge(idx)));
	  plane_plus2sigma ->SetBinContent(idx, idy, graph_plus2sigma_tanb ->Eval(plane_plus2sigma ->GetXaxis()->GetBinLowEdge(idx)));
	  plane_observed   ->SetBinContent(idx, idy, graph_observed_tanb   ->Eval(plane_observed   ->GetXaxis()->GetBinLowEdge(idx)));
	}
	else if(FitMethod_==1 || FitMethod_==4){
	  plane_minus2sigma->SetBinContent(idx, idy, graph_minus2sigma_tanb->Eval(plane_minus2sigma->GetXaxis()->GetBinLowEdge(idx), 0, "S"));
	  plane_minus1sigma->SetBinContent(idx, idy, graph_minus1sigma_tanb->Eval(plane_minus1sigma->GetXaxis()->GetBinLowEdge(idx), 0, "S"));
	  plane_expected   ->SetBinContent(idx, idy, graph_expected_tanb   ->Eval(plane_expected   ->GetXaxis()->GetBinLowEdge(idx), 0, "S"));
	  plane_plus1sigma ->SetBinContent(idx, idy, graph_plus1sigma_tanb ->Eval(plane_plus1sigma ->GetXaxis()->GetBinLowEdge(idx), 0, "S"));
	  plane_plus2sigma ->SetBinContent(idx, idy, graph_plus2sigma_tanb ->Eval(plane_plus2sigma ->GetXaxis()->GetBinLowEdge(idx), 0, "S"));
	  plane_observed   ->SetBinContent(idx, idy, graph_observed_tanb   ->Eval(plane_observed   ->GetXaxis()->GetBinLowEdge(idx), 0, "S"));
	}
      }
    }
  }

  //change log back to normal in order to let contour plotting work
  for(int idy=0; idy<plane_minus2sigma->GetNbinsY()+1; idy++){
    for(int idx=0; idx<plane_minus2sigma->GetNbinsX()+1; idx++){
      plane_minus2sigma->SetBinContent(idx, idy, TMath::Exp(plane_minus2sigma->GetBinContent(idx, idy)));
      plane_minus1sigma->SetBinContent(idx, idy, TMath::Exp(plane_minus1sigma->GetBinContent(idx, idy)));
      plane_expected   ->SetBinContent(idx, idy, TMath::Exp(plane_expected   ->GetBinContent(idx, idy)));
      plane_plus1sigma ->SetBinContent(idx, idy, TMath::Exp(plane_plus1sigma ->GetBinContent(idx, idy)));
      plane_plus2sigma ->SetBinContent(idx, idy, TMath::Exp(plane_plus2sigma ->GetBinContent(idx, idy)));
      plane_observed   ->SetBinContent(idx, idy, TMath::Exp(plane_observed   ->GetBinContent(idx, idy)));
    }
  }
  
  if(FitMethod_==2){ //TGrah2D interpolation
    for(int i=0; i<=expected_th2d->GetXaxis()->GetNbins();i++){
      for(int j=0; j<=expected_th2d->GetYaxis()->GetNbins();j++){
	minus2sigma_th2d->SetBinContent(i,j,graph_minus2sigma_2d->Interpolate(minus2sigma_th2d->GetXaxis()->GetBinCenter(i),minus2sigma_th2d->GetYaxis()->GetBinCenter(j)));
	minus1sigma_th2d->SetBinContent(i,j,graph_minus1sigma_2d->Interpolate(minus1sigma_th2d->GetXaxis()->GetBinCenter(i),minus1sigma_th2d->GetYaxis()->GetBinCenter(j)));
	expected_th2d->SetBinContent(i,j,graph_expected_2d->Interpolate(expected_th2d->GetXaxis()->GetBinCenter(i),expected_th2d->GetYaxis()->GetBinCenter(j)));
	plus1sigma_th2d->SetBinContent(i,j,graph_plus1sigma_2d->Interpolate(plus1sigma_th2d->GetXaxis()->GetBinCenter(i),plus1sigma_th2d->GetYaxis()->GetBinCenter(j)));
	plus2sigma_th2d->SetBinContent(i,j,graph_plus2sigma_2d->Interpolate(plus2sigma_th2d->GetXaxis()->GetBinCenter(i),plus2sigma_th2d->GetYaxis()->GetBinCenter(j)));
	observed_th2d->SetBinContent(i,j,graph_observed_2d->Interpolate(observed_th2d->GetXaxis()->GetBinCenter(i),observed_th2d->GetYaxis()->GetBinCenter(j)));
      }
    }
  }
  // Grabbing contours
  std::vector<TGraph*> gr_minus2sigma;
  std::vector<TGraph*> gr_minus1sigma;
  std::vector<TGraph*> gr_expected;
  std::vector<TGraph*> gr_plus1sigma;
  std::vector<TGraph*> gr_plus2sigma;
  std::vector<TGraph*> gr_observed;
  std::vector<TGraph*> gr_injected;
  gr_injected.push_back(0);
    
  int n_m2s, n_m1s, n_exp, n_p1s, n_p2s, n_obs;
  if(FitMethod_==0 || FitMethod_==1 || FitMethod_==3 || FitMethod_==4){ //linear fit=0; spline=1; spline+linear=3; linear+spline=4
    TIter iterm2s((TList *)contourFromTH2(plane_minus2sigma, 1.0, 20, false));
    STestFunctor m2s = std::for_each( iterm2s.Begin(), TIter::End(), STestFunctor() );
    n_m2s=m2s.sum; 
    TIter iterm1s((TList *)contourFromTH2(plane_minus1sigma, 1.0, 20, false));
    STestFunctor m1s = std::for_each( iterm1s.Begin(), TIter::End(), STestFunctor() );
    n_m1s=m1s.sum; 
    TIter iterexp((TList *)contourFromTH2(plane_expected, 1.0, 20, false));
    STestFunctor exp = std::for_each( iterexp.Begin(), TIter::End(), STestFunctor() );
    n_exp=exp.sum; 
    TIter iterp1s((TList *)contourFromTH2(plane_plus1sigma, 1.0, 20, false));
    STestFunctor p1s = std::for_each( iterp1s.Begin(), TIter::End(), STestFunctor() );
    n_p1s=p1s.sum; 
    TIter iterp2s((TList *)contourFromTH2(plane_plus2sigma, 1.0, 20, false));
    STestFunctor p2s = std::for_each( iterp2s.Begin(), TIter::End(), STestFunctor() );
    n_p2s=p2s.sum; 
    TIter iterobs((TList *)contourFromTH2(plane_observed, 1.0, 20, false));
    STestFunctor obs = std::for_each( iterobs.Begin(), TIter::End(), STestFunctor() );
    n_obs=obs.sum; 
    for(int i=0; i<n_m2s; i++) {gr_minus2sigma.push_back((TGraph *)((TList *)contourFromTH2(plane_minus2sigma, 1.0, 20, false))->At(i));}
    for(int i=0; i<n_m1s; i++) {gr_minus1sigma.push_back((TGraph *)((TList *)contourFromTH2(plane_minus1sigma, 1.0, 20, false))->At(i));}
    for(int i=0; i<n_exp; i++) {gr_expected.push_back(   (TGraph *)((TList *)contourFromTH2(plane_expected,    1.0, 20, false))->At(i));}
    for(int i=0; i<n_p1s; i++) {gr_plus1sigma.push_back( (TGraph *)((TList *)contourFromTH2(plane_plus1sigma,  1.0, 20, false))->At(i));}
    for(int i=0; i<n_p2s; i++) {gr_plus2sigma.push_back( (TGraph *)((TList *)contourFromTH2(plane_plus2sigma,  1.0, 20, false))->At(i));}
    for(int i=0; i<n_obs; i++) {gr_observed.push_back(   (TGraph *)((TList *)contourFromTH2(plane_observed,    1.0, 20, false))->At(i));}
  }
  else if(FitMethod_==2){ //TGrah2D interpolation
    TIter iterm2s((TList *)contourFromTH2(minus2sigma_th2d, 1.0, 20, false,5));
    STestFunctor m2s = std::for_each( iterm2s.Begin(), TIter::End(), STestFunctor() );
    n_m2s=m2s.sum;
    TIter iterm1s((TList *)contourFromTH2(minus1sigma_th2d, 1.0, 20, false,5));
    STestFunctor m1s = std::for_each( iterm1s.Begin(), TIter::End(), STestFunctor() );
    n_m1s=m1s.sum;
    TIter iterexp((TList *)contourFromTH2(expected_th2d, 1.0, 20, false,5));
    STestFunctor exp = std::for_each( iterexp.Begin(), TIter::End(), STestFunctor() );
    n_exp=exp.sum;
    TIter iterp1s((TList *)contourFromTH2(plus1sigma_th2d, 1.0, 20, false,5));
    STestFunctor p1s = std::for_each( iterp1s.Begin(), TIter::End(), STestFunctor() );
    n_p1s=p1s.sum;
    TIter iterp2s((TList *)contourFromTH2(plus2sigma_th2d, 1.0, 20, false,5));
    STestFunctor p2s = std::for_each( iterp2s.Begin(), TIter::End(), STestFunctor() );
    n_p2s=p2s.sum;
    TIter iterobs((TList *)contourFromTH2(observed_th2d, 1.0, 20, false,5));
    STestFunctor obs = std::for_each( iterobs.Begin(), TIter::End(), STestFunctor() );
    n_obs=obs.sum;
    for(int i=0; i<n_m2s; i++) {gr_minus2sigma.push_back((TGraph *)((TList *)contourFromTH2(minus2sigma_th2d, 1.0, 20, false, 5))->At(i));}
    for(int i=0; i<n_m1s; i++) {gr_minus1sigma.push_back((TGraph *)((TList *)contourFromTH2(minus1sigma_th2d, 1.0, 20, false, 5))->At(i));}
    for(int i=0; i<n_exp; i++) {gr_expected.push_back((TGraph *)((TList *)contourFromTH2(expected_th2d, 1.0, 20, false, 5))->At(i));}
    for(int i=0; i<n_p1s; i++) {gr_plus1sigma.push_back((TGraph *)((TList *)contourFromTH2(plus1sigma_th2d, 1.0, 20, false, 5))->At(i));}
    for(int i=0; i<n_p2s; i++) {gr_plus2sigma.push_back((TGraph *)((TList *)contourFromTH2(plus2sigma_th2d, 1.0, 20, false, 5))->At(i));}
    for(int i=0; i<n_obs; i++) {gr_observed.push_back((TGraph *)((TList *)contourFromTH2(observed_th2d, 1.0, 20, false, 5))->At(i));}
  }
  
  // create plots for additional comparisons
  std::map<std::string, TGraph*> comparisons; TGraph* comp=0;
  if(arXiv_1211_6956_){ comp = new TGraph(), arXiv_1211_6956 (comp); comp->SetName("arXiv_1211_6956" ); comparisons[std::string("ATLAS H#rightarrow#tau#tau (4.8/fb)")] = comp;}
  if(arXiv_1204_2760_){ comp = new TGraph(); arXiv_1204_2760 (comp); comp->SetName("arXiv_1204_2760" ); comparisons[std::string("ATLAS H^{+} (4.6/fb)")               ] = comp;}
  if(arXiv_1302_2892_){ comp = new TGraph(); arXiv_1302_2892 (comp); comp->SetName("arXiv_1302_2892" ); comparisons[std::string("CMS #phi#rightarrowb#bar{b}")        ] = comp;}
  if(arXiv_1205_5736_){ comp = new TGraph(); arXiv_1205_5736 (comp); comp->SetName("arXiv_1205_5736" ); comparisons[std::string("CMS H^{+} (2/fb)")                   ] = comp;}
  if(HIG_12_052_     ){ comp = new TGraph(); HIG_12_052_lower(comp); comp->SetName("HIG_12_052_lower"); comparisons[std::string("CMS H^{+} (2-4.9/fb)")               ] = comp;}
  if(HIG_12_052_     ){ comp = new TGraph(); HIG_12_052_upper(comp); comp->SetName("HIG_12_052_upper"); comparisons[std::string("EMPTY")                              ] = comp;}

  // setup contratins from Higgs mass
  std::vector<TGraph*> gr_higgslow;
  std::vector<TGraph*> gr_higgshigh;
  std::vector<TGraph*> gr_higgsHlow;
  gr_higgsHlow.push_back(0);
  std::vector<TGraph*> gr_higgsHhigh;
  gr_higgsHhigh.push_back(0);
  std::vector<std::vector<TGraph*>> gr_higgsBands; 
  std::vector<TH2D*> plane_higgsBands;
  if(higgs125_){
    TH2D* plane_higgsBand = higgsConstraint(model, "h");
    plane_higgsBands.push_back(plane_higgsBand);
    //lower edge entry 0
    TIter iter_higgslow((TList *)contourFromTH2(plane_higgsBands[0], 122, 20, false));
    STestFunctor higgsband0 = std::for_each( iter_higgslow.Begin(), TIter::End(), STestFunctor() );
    for(int i=0; i<higgsband0.sum; i++) {gr_higgslow.push_back((TGraph *)((TList *)contourFromTH2(plane_higgsBands[0], 122, 20, false, 200))->At(i));}
    gr_higgsBands.push_back(gr_higgslow);
    //upper edge entry 1
    TIter iter_higgshigh((TList *)contourFromTH2(plane_higgsBands[0], 128, 20, false));
    STestFunctor higgsband1 = std::for_each( iter_higgshigh.Begin(), TIter::End(), STestFunctor() );
    for(int i=0; i<higgsband1.sum; i++) {gr_higgshigh.push_back((TGraph *)((TList *)contourFromTH2(plane_higgsBands[0], 128, 20, false, 200))->At(i));} 
    gr_higgsBands.push_back(gr_higgshigh);
    // possible to push back more curves to gr_higgsBands for Hhh need to call different higgsConstraint with model "H" 
    gr_higgsBands.push_back(gr_higgsHhigh);
    gr_higgsBands.push_back(gr_higgsHhigh);
    if(TString::Format(model)=="low-tb-high"){
      gr_higgsHlow.pop_back();  gr_higgsHlow.pop_back(); gr_higgsBands.pop_back(); gr_higgsBands.pop_back(); 
      TH2D* plane_higgsHBand = higgsConstraint(model, "H");
      plane_higgsBands.push_back(plane_higgsHBand);
      //lower edge entry 2
      TIter iter_higgsHlow((TList *)contourFromTH2(plane_higgsBands[1], 260, 20, false));
      STestFunctor higgsHband0 = std::for_each( iter_higgsHlow.Begin(), TIter::End(), STestFunctor() );
      for(int i=0; i<higgsHband0.sum; i++) {gr_higgsHlow.push_back((TGraph *)((TList *)contourFromTH2(plane_higgsBands[1], 260, 20, false, 200))->At(i));}
      gr_higgsBands.push_back(gr_higgsHlow);
      //upper edge entry 3
      TIter iter_higgsHhigh((TList *)contourFromTH2(plane_higgsBands[1], 350, 20, false));
      STestFunctor higgsHband1 = std::for_each( iter_higgsHhigh.Begin(), TIter::End(), STestFunctor() );
      for(int i=0; i<higgsHband1.sum; i++) {gr_higgsHhigh.push_back((TGraph *)((TList *)contourFromTH2(plane_higgsBands[1], 350, 20, false, 200))->At(i));} 
      gr_higgsBands.push_back(gr_higgsHhigh);
    }
  }  

  // do the plotting
  plottingTanb(canv, plane_expected, gr_minus2sigma, gr_minus1sigma, gr_expected, gr_plus1sigma, gr_plus2sigma, gr_observed, gr_injected, gr_higgsBands, comparisons, xaxis_, yaxis_, theory_, min_, max_, log_, transparent_, expectedOnly_, MSSMvsSM_, HIG, Brazilian_, azh_); 
  /// setup the CMS Preliminary
  //TPaveText* cmsprel = new TPaveText(0.145, 0.835+0.06, 0.145+0.30, 0.835+0.16, "NDC");
  TPaveText* cmsprel = new TPaveText(0.135, 0.735, 0.145+0.30, 0.785, "NDC"); // for "unpublished" in header
  //TPaveText* cmsprel = new TPaveText(0.0, 0.94, 0.86, 0.995, "NDC");
  cmsprel->SetBorderSize(   0 );
  cmsprel->SetFillStyle(    0 );
  cmsprel->SetTextAlign(   11 );
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
  // write txt and tex files
  if(txt_){
    print(std::string(output_).append("_").append(extralabel_).append(label_).c_str(), v_graph_minus2sigma, v_graph_minus1sigma, v_graph_expected, v_graph_plus1sigma, v_graph_plus2sigma, v_graph_observed, tanbLow, tanbHigh, masses, "txt");
    print(std::string(output_).append("_").append(extralabel_).append(label_).c_str(), v_graph_minus2sigma, v_graph_minus1sigma, v_graph_expected, v_graph_plus1sigma, v_graph_plus2sigma, v_graph_observed, tanbLow, tanbHigh, masses, "tex");
  }
  if(root_){
    TFile* output = new TFile(std::string(output_).append("_").append(extralabel_).append(label_).append(".root").c_str(), "update");
    if(!output->cd(output_.c_str())){
      output->mkdir(output_.c_str());
      output->cd(output_.c_str());
    }
    plane_expected->Write("plane_expected");  
    for(unsigned int i=0; i<gr_higgslow.size(); i++){
      gr_higgslow[i]   ->Write(TString::Format("gr_higgslow_%d", i)  ); 
    }
    for(unsigned int i=0; i<gr_higgshigh.size(); i++){
      gr_higgshigh[i]   ->Write(TString::Format("gr_higgshigh_%d", i)  ); 
    }   
    for(unsigned int i=0; i<gr_observed.size(); i++){
      gr_observed[i]   ->Write(TString::Format("gr_observed_%d", i)  ); 
    }
    for(unsigned int i=0; i<gr_expected.size(); i++){
      gr_expected[i]   ->Write(TString::Format("gr_expected_%d", i)    );
    }
    for(unsigned int i=0; i<gr_minus2sigma.size(); i++){
      gr_minus2sigma[i]->Write(TString::Format("gr_minus2sigma_%d", i)    );
    }
    for(unsigned int i=0; i<gr_minus1sigma.size(); i++){
      gr_minus1sigma[i]->Write(TString::Format("gr_minus1sigma_%d", i)    ); 
    }
    for(unsigned int i=0; i<gr_plus1sigma.size(); i++){
      gr_plus1sigma[i] ->Write(TString::Format("gr_plus1sigma_%d", i)     );
    }
    for(unsigned int i=0; i<gr_plus2sigma.size(); i++){
      gr_plus2sigma[i] ->Write(TString::Format("gr_plus2sigma_%d", i)     );
    }
    output->Close();
  }
  // save exclusion in each mass directory - needed for smart scan!
  for(unsigned int imass=0; imass<bins_.size(); ++imass){
    print(TString::Format("%s/%d/exclusion", directory, (int)bins_[imass]), v_graph_minus2sigma, v_graph_minus1sigma, v_graph_expected, v_graph_plus1sigma, v_graph_plus2sigma, v_graph_observed, tanbLow, tanbHigh, masses, "dat");
  }
  return;
}





void CLsControlPlots(TGraph* graph_minus2sigma, TGraph* graph_minus1sigma, TGraph* graph_expected, TGraph* graph_plus1sigma, TGraph* graph_plus2sigma, TGraph* graph_observed, const char* directory, float mass, int xmax, int ymax, const char* model){
//control plots showing the CLs value over tanb for each mass
    //minus2sigma
    TCanvas* canv_minus2sigma = new TCanvas();
    if((model==TString::Format("2HDMtyp1") || model==TString::Format("2HDMtyp2"))&&(int)mass!=mass) canv_minus2sigma = new TCanvas(TString::Format("tanb-CLs_025_%0.1f", mass), "", 600, 600);
    else canv_minus2sigma = new TCanvas(TString::Format("tanb-CLs_025_%d", (int)mass), "", 600, 600);
    canv_minus2sigma->cd();
    canv_minus2sigma->SetGridx(1);
    canv_minus2sigma->SetGridy(1);
    graph_minus2sigma->GetXaxis()->SetTitle("tan#beta");
    graph_minus2sigma->GetXaxis()->SetLabelFont(62);
    graph_minus2sigma->GetXaxis()->SetTitleFont(62);
    graph_minus2sigma->GetXaxis()->SetTitleColor(1);
    graph_minus2sigma->GetXaxis()->SetTitleOffset(1.05);
    graph_minus2sigma->GetYaxis()->SetTitle("CL_{s}");
    graph_minus2sigma->GetYaxis()->SetLabelFont(62);
    graph_minus2sigma->GetYaxis()->SetTitleFont(62);
    graph_minus2sigma->GetYaxis()->SetTitleOffset(1.05);
    graph_minus2sigma->GetYaxis()->SetLabelSize(0.03);
    //graph_minus2sigma->GetYaxis()->SetRangeUser(0,2);
    graph_minus2sigma->SetMarkerStyle(20);
    graph_minus2sigma->SetMarkerSize(1.3);
    ymax=0; ymax=0;
    for(int j=0; j<graph_minus2sigma->GetN(); j++){ 
      if(graph_minus2sigma->GetY()[j]>ymax) {ymax=graph_minus2sigma->GetY()[j]; xmax=graph_minus2sigma->GetX()[j];}
    }
    graph_minus2sigma->Draw("AP");
    if((model==TString::Format("2HDMtyp1") || model==TString::Format("2HDMtyp2"))&&(int)mass!=mass) canv_minus2sigma->Print(TString::Format("%s/%0.1f/tanb-CLs_025_%0.1f.png", directory, mass, mass));
    else canv_minus2sigma->Print(TString::Format("%s/%d/tanb-CLs_025_%d.png", directory, (int)mass, (int)mass));
    //minus1sigma
    TCanvas* canv_minus1sigma = new TCanvas();
    if((model==TString::Format("2HDMtyp1") || model==TString::Format("2HDMtyp2"))&&(int)mass!=mass) canv_minus1sigma = new TCanvas(TString::Format("tanb-CLs_160_%0.1f", mass), "", 600, 600);
    else canv_minus1sigma = new TCanvas(TString::Format("tanb-CLs_160_%d", (int)mass), "", 600, 600);
    canv_minus1sigma->cd();
    canv_minus1sigma->SetGridx(1);
    canv_minus1sigma->SetGridy(1);
    graph_minus1sigma->GetXaxis()->SetTitle("tan#beta");
    graph_minus1sigma->GetXaxis()->SetLabelFont(62);
    graph_minus1sigma->GetXaxis()->SetTitleFont(62);
    graph_minus1sigma->GetXaxis()->SetTitleColor(1);
    graph_minus1sigma->GetXaxis()->SetTitleOffset(1.05);
    graph_minus1sigma->GetYaxis()->SetTitle("CL_{s}");
    graph_minus1sigma->GetYaxis()->SetLabelFont(62);
    graph_minus1sigma->GetYaxis()->SetTitleFont(62);
    graph_minus1sigma->GetYaxis()->SetTitleOffset(1.05);
    graph_minus1sigma->GetYaxis()->SetLabelSize(0.03);
    //graph_minus1sigma->GetYaxis()->SetRangeUser(0,2);
    graph_minus1sigma->SetMarkerStyle(20);
    graph_minus1sigma->SetMarkerSize(1.3);
    ymax=0; ymax=0;
    for(int j=0; j<graph_minus1sigma->GetN(); j++){ 
      if(graph_minus1sigma->GetY()[j]>ymax) {ymax=graph_minus1sigma->GetY()[j]; xmax=graph_minus1sigma->GetX()[j];}
    }
    graph_minus1sigma->Draw("AP");
    if((model==TString::Format("2HDMtyp1") || model==TString::Format("2HDMtyp2"))&&(int)mass!=mass) canv_minus1sigma->Print(TString::Format("%s/%0.1f/tanb-CLs_160_%0.1f.png", directory, mass, mass));
    else canv_minus1sigma->Print(TString::Format("%s/%d/tanb-CLs_160_%d.png", directory, (int)mass, (int)mass));
    //expected
    TCanvas* canv_expected = new TCanvas();
    if((model==TString::Format("2HDMtyp1") || model==TString::Format("2HDMtyp2"))&&(int)mass!=mass) canv_expected = new TCanvas(TString::Format("tanb-CLs_EXP_%0.1f", mass), "", 600, 600);
    else canv_expected = new TCanvas(TString::Format("tanb-CLs_EXP_%d", (int)mass), "", 600, 600);
    canv_expected->cd();
    canv_expected->SetGridx(1);
    canv_expected->SetGridy(1);
    graph_expected->GetXaxis()->SetTitle("tan#beta");
    graph_expected->GetXaxis()->SetLabelFont(62);
    graph_expected->GetXaxis()->SetTitleFont(62);
    graph_expected->GetXaxis()->SetTitleColor(1);
    graph_expected->GetXaxis()->SetTitleOffset(1.05);
    graph_expected->GetYaxis()->SetTitle("CL_{s}");
    graph_expected->GetYaxis()->SetLabelFont(62);
    graph_expected->GetYaxis()->SetTitleFont(62);
    graph_expected->GetYaxis()->SetTitleOffset(1.05);
    graph_expected->GetYaxis()->SetLabelSize(0.03);
    //graph_expected->GetYaxis()->SetRangeUser(0,2);
    graph_expected->SetMarkerStyle(20);
    graph_expected->SetMarkerSize(1.3);
    ymax=0; ymax=0;
    for(int j=0; j<graph_expected->GetN(); j++){ 
      if(graph_expected->GetY()[j]>ymax) {ymax=graph_expected->GetY()[j]; xmax=graph_expected->GetX()[j];}
    }
    graph_expected->Draw("AP");
    if((model==TString::Format("2HDMtyp1") || model==TString::Format("2HDMtyp2"))&&(int)mass!=mass) canv_expected->Print(TString::Format("%s/%0.1f/tanb-CLs_EXP_%0.1f.png", directory, mass, mass));
    else canv_expected->Print(TString::Format("%s/%d/tanb-CLs_EXP_%d.png", directory, (int)mass, (int)mass));
    //plus1sigma
    TCanvas* canv_plus1sigma = new TCanvas();
    if((model==TString::Format("2HDMtyp1") || model==TString::Format("2HDMtyp2"))&&(int)mass!=mass) canv_plus1sigma = new TCanvas(TString::Format("tanb-CLs_860_%0.1f", mass), "", 600, 600);
    else canv_plus1sigma = new TCanvas(TString::Format("tanb-CLs_860_%d", (int)mass), "", 600, 600);
    canv_plus1sigma->cd();
    canv_plus1sigma->SetGridx(1);
    canv_plus1sigma->SetGridy(1);
    graph_plus1sigma->GetXaxis()->SetTitle("tan#beta");
    graph_plus1sigma->GetXaxis()->SetLabelFont(62);
    graph_plus1sigma->GetXaxis()->SetTitleFont(62);
    graph_plus1sigma->GetXaxis()->SetTitleColor(1);
    graph_plus1sigma->GetXaxis()->SetTitleOffset(1.05);
    graph_plus1sigma->GetYaxis()->SetTitle("CL_{s}");
    graph_plus1sigma->GetYaxis()->SetLabelFont(62);
    graph_plus1sigma->GetYaxis()->SetTitleFont(62);
    graph_plus1sigma->GetYaxis()->SetTitleOffset(1.05);
    graph_plus1sigma->GetYaxis()->SetLabelSize(0.03);
    //graph_plus1sigma->GetYaxis()->SetRangeUser(0,2);
    graph_plus1sigma->SetMarkerStyle(20);
    graph_plus1sigma->SetMarkerSize(1.3);
    ymax=0; ymax=0;
    for(int j=0; j<graph_plus1sigma->GetN(); j++){ 
      if(graph_plus1sigma->GetY()[j]>ymax) {ymax=graph_plus1sigma->GetY()[j]; xmax=graph_plus1sigma->GetX()[j];}
    }
    graph_plus1sigma->Draw("AP");
    if((model==TString::Format("2HDMtyp1") || model==TString::Format("2HDMtyp2"))&&(int)mass!=mass) canv_plus1sigma->Print(TString::Format("%s/%0.1f/tanb-CLs_860_%0.1f.png", directory, mass, mass));
    else canv_plus1sigma->Print(TString::Format("%s/%d/tanb-CLs_860_%d.png", directory, (int)mass, (int)mass));
    //plus2sigma
    TCanvas* canv_plus2sigma = new TCanvas();
    if((model==TString::Format("2HDMtyp1") || model==TString::Format("2HDMtyp2"))&&(int)mass!=mass) canv_plus2sigma = new TCanvas(TString::Format("tanb-CLs_975_%0.1f", mass), "", 600, 600);
    else canv_plus2sigma = new TCanvas(TString::Format("tanb-CLs_975_%d", (int)mass), "", 600, 600);
    canv_plus2sigma->cd();
    canv_plus2sigma->SetGridx(1);
    canv_plus2sigma->SetGridy(1);
    graph_plus2sigma->GetXaxis()->SetTitle("tan#beta");
    graph_plus2sigma->GetXaxis()->SetLabelFont(62);
    graph_plus2sigma->GetXaxis()->SetTitleFont(62);
    graph_plus2sigma->GetXaxis()->SetTitleColor(1);
    graph_plus2sigma->GetXaxis()->SetTitleOffset(1.05);
    graph_plus2sigma->GetYaxis()->SetTitle("CL_{s}");
    graph_plus2sigma->GetYaxis()->SetLabelFont(62);
    graph_plus2sigma->GetYaxis()->SetTitleFont(62);
    graph_plus2sigma->GetYaxis()->SetTitleOffset(1.05);
    graph_plus2sigma->GetYaxis()->SetLabelSize(0.03);
    //graph_plus2sigma->GetYaxis()->SetRangeUser(0,2);
    graph_plus2sigma->SetMarkerStyle(20);
    graph_plus2sigma->SetMarkerSize(1.3);
    ymax=0; ymax=0;
    for(int j=0; j<graph_plus2sigma->GetN(); j++){ 
      if(graph_plus2sigma->GetY()[j]>ymax) {ymax=graph_plus2sigma->GetY()[j]; xmax=graph_plus2sigma->GetX()[j];}
    }
    graph_plus2sigma->Draw("AP");
    if((model==TString::Format("2HDMtyp1") || model==TString::Format("2HDMtyp2"))&&(int)mass!=mass) canv_plus2sigma->Print(TString::Format("%s/%0.1f/tanb-CLs_975_%0.1f.png", directory, mass, mass));
    else canv_plus2sigma->Print(TString::Format("%s/%d/tanb-CLs_975_%d.png", directory, (int)mass, (int)mass));
    //observed
    TCanvas* canv_observed = new TCanvas();
    if((model==TString::Format("2HDMtyp1") || model==TString::Format("2HDMtyp2"))&&(int)mass!=mass) canv_observed = new TCanvas(TString::Format("tanb-CLs_OBS_%0.1f", mass), "", 600, 600);
    else canv_observed = new TCanvas(TString::Format("tanb-CLs_OBS_%d", (int)mass), "", 600, 600);
    canv_observed->cd();
    canv_observed->SetGridx(1);
    canv_observed->SetGridy(1);
    graph_observed->GetXaxis()->SetTitle("tan#beta");
    graph_observed->GetXaxis()->SetLabelFont(62);
    graph_observed->GetXaxis()->SetTitleFont(62);
    graph_observed->GetXaxis()->SetTitleColor(1);
    graph_observed->GetXaxis()->SetTitleOffset(1.05);
    graph_observed->GetYaxis()->SetTitle("CL_{s}");
    graph_observed->GetYaxis()->SetLabelFont(62);
    graph_observed->GetYaxis()->SetTitleFont(62);
    graph_observed->GetYaxis()->SetTitleOffset(1.05);
    graph_observed->GetYaxis()->SetLabelSize(0.03);
    //graph_observed->GetYaxis()->SetRangeUser(0,2);
    graph_observed->SetMarkerStyle(20);
    graph_observed->SetMarkerSize(1.3);
    ymax=0; ymax=0;
    for(int j=0; j<graph_observed->GetN(); j++){ 
      if(graph_observed->GetY()[j]>ymax) {ymax=graph_observed->GetY()[j]; xmax=graph_observed->GetX()[j];}
    }
    graph_observed->Draw("AP");
    if((model==TString::Format("2HDMtyp1") || model==TString::Format("2HDMtyp2"))&&(int)mass!=mass) canv_observed->Print(TString::Format("%s/%0.1f/tanb-CLs_OBS_%0.1f.png", directory, mass, mass));
    else canv_observed->Print(TString::Format("%s/%d/tanb-CLs_OBS_%d.png", directory, (int)mass, (int)mass));
    return;
}

