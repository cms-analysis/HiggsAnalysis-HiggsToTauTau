#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"
#include <vector>
#include <TF1.h>
#include <TFitResult.h>
#include <TGraph2D.h>
#include <TSpline.h>
#include <TMath.h>

/// This is the core plotting routine that can also be used within
/// root macros. It is therefore not element of the PlotLimits class.
void plottingTanbML(TCanvas& canv, TH2D* h2d, std::string& xaxis, std::string& yaxis, std::string& theory, double min=0., double max=50., bool log=false);


void 
PlotLimits::plotTanbML(TCanvas& canv, const char* directory)
{
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
  std::vector<TGraph*> v_graph_minus1sigma;
  std::vector<TGraph*> v_graph_expected;
  std::vector<TGraph*> v_graph_plus1sigma;
  std::vector<TGraph*> v_graph_observed;
  //float masses[50];

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

  TH2D *plane_minus1sigma = 0, *plane_expected = 0, *plane_plus1sigma = 0, *plane_observed = 0;

  if(model!=TString::Format("lowmH")) {
    plane_minus1sigma = new TH2D("minus1sigma","minus1sigma", nxbins, xbins, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
    plane_expected    = new TH2D("expected","expected",       nxbins, xbins, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
    plane_plus1sigma  = new TH2D("plus1sigma","plus1sigma",   nxbins, xbins, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
    plane_observed    = new TH2D("observed","observed",       nxbins, xbins, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
  }
  else { 
    plane_minus1sigma = new TH2D("minus1sigma","minus1sigma", 29, 300, 3100, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
    plane_expected    = new TH2D("expected",   "expected",    29, 300, 3100, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
    plane_plus1sigma  = new TH2D("plus1sigma","plus1sigma",   29, 300, 3100, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
    plane_observed    = new TH2D("observed","observed",       29, 300, 3100, (int)((tanbHigh-tanbLow)*10-1), tanbLow, tanbHigh);
  }


  for(int idx=1; idx<plane_minus1sigma->GetNbinsX()+1; idx++){
    for(int idy=1; idy<plane_minus1sigma->GetNbinsY()+1; idy++){
      plane_minus1sigma->SetBinContent(idx, idy, 1.1);
      plane_expected   ->SetBinContent(idx, idy, 1.1);
      plane_plus1sigma ->SetBinContent(idx, idy, 1.1);
      plane_observed   ->SetBinContent(idx, idy, 1.1);
    }
  }
  
  TGraph2D* graph_minus1sigma_2d = 0;
  TGraph2D* graph_expected_2d = 0;
  TGraph2D* graph_plus1sigma_2d = 0;
  TGraph2D* graph_observed_2d =0;
  TH2D *minus1sigma_th2d =new TH2D("minus1sigma_th2d","minus1sigma_th2d",4*nxbins,xbins[0],xbins[nxbins-1],(int)((tanbHigh-tanbLow)*10-1),tanbLow,tanbHigh);
  TH2D *expected_th2d =new TH2D("expected_th2d","expected_th2d",4*nxbins,xbins[0],xbins[nxbins-1],(int)((tanbHigh-tanbLow)*10-1),tanbLow,tanbHigh);
  TH2D *plus1sigma_th2d =new TH2D("plus1sigma_th2d","plus1sigma_th2d",4*nxbins,xbins[0],xbins[nxbins-1],(int)((tanbHigh-tanbLow)*10-1),tanbLow,tanbHigh);
  TH2D *observed_th2d =new TH2D("observed_th2d","observed_th2d",4*nxbins,xbins[0],xbins[nxbins-1],(int)((tanbHigh-tanbLow)*10-1),tanbLow,tanbHigh);
  
  //2D Graphs 
  int kTwod=0;
  graph_minus1sigma_2d = new TGraph2D();
  graph_expected_2d = new TGraph2D();
  graph_plus1sigma_2d = new TGraph2D();
  graph_observed_2d = new TGraph2D();
    
  for(unsigned int imass=0; imass<bins_.size(); ++imass){
    // buffer mass value
    float mass = bins_[imass];    
    TGraph* graph_minus1sigma = new TGraph();
    TGraph* graph_expected = new TGraph();
    TGraph* graph_plus1sigma = new TGraph();
    TGraph* graph_observed = new TGraph();
    
    
    TString fullpath = TString::Format("%s/%d/MLFit.root", directory, (int)mass);
    if (model==TString::Format("2HDMtyp1") || model==TString::Format("2HDMtyp2")){ 
      if(bins_[imass]!=(int)bins_[imass]) fullpath = TString::Format("%s/%0.1f/MLFit.root", directory, bins_[imass]);
      else fullpath = TString::Format("%s/%d/MlFit.root",directory,(int)mass);
    }
    std::cout << "open file: " << fullpath << std::endl;
    TFile* file_ = TFile::Open(fullpath); if(!file_){ std::cout << "--> TFile is corrupt: skipping masspoint." << std::endl; continue; }
    TTree* limit = (TTree*) file_->Get("tree"); if(!limit){ std::cout << "--> TTree is corrupt: skipping masspoint." << std::endl; continue; }
    double tanb, exp, obs, plus1sigma, minus1sigma;
    limit->SetBranchAddress("tanb", &tanb );  
    limit->SetBranchAddress("minus1sigma", &minus1sigma);
    limit->SetBranchAddress("expected", &exp);
    limit->SetBranchAddress("plus1sigma", &plus1sigma); 
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
      graph_minus1sigma->SetPoint(k, tanb, minus1sigma);
      graph_expected   ->SetPoint(k, tanb, exp);
      graph_plus1sigma ->SetPoint(k, tanb, plus1sigma);
      graph_observed   ->SetPoint(k, tanb, obs);
      k++;      
      for(int j=0; j<graph_minus1sigma->GetN(); j++){ 
	if(graph_minus1sigma->GetY()[j]>ymax && graph_minus1sigma->GetX()[j]>=1) {ymax=graph_minus1sigma->GetY()[j]; xmax=graph_minus1sigma->GetX()[j]; tanbLowHigh=xmax;} //tanb>=1 hardcoded to fix that point 	  
      }
      
      // Fill TH2D with calculated limit points
      if(FitMethod_==0 || FitMethod_==1 || FitMethod_==3 || FitMethod_==4){ //linear fit=0; spline=1; spline+linear=3; linear+spline=4
	plane_minus1sigma->SetBinContent(plane_minus1sigma->GetXaxis()->FindBin(mass), plane_minus1sigma->GetYaxis()->FindBin(tanb), minus1sigma);
	plane_expected   ->SetBinContent(plane_expected   ->GetXaxis()->FindBin(mass), plane_expected   ->GetYaxis()->FindBin(tanb), exp);
	plane_plus1sigma ->SetBinContent(plane_plus1sigma ->GetXaxis()->FindBin(mass), plane_plus1sigma ->GetYaxis()->FindBin(tanb), plus1sigma);
	plane_observed   ->SetBinContent(plane_observed   ->GetXaxis()->FindBin(mass), plane_observed   ->GetYaxis()->FindBin(tanb), obs);
      }
      else if(FitMethod_==2){ //TGraph2D interpolation
	graph_minus1sigma_2d->SetPoint(kTwod,mass,tanb,minus1sigma);
	graph_expected_2d->SetPoint(kTwod,mass,tanb,exp);
	graph_plus1sigma_2d->SetPoint(kTwod,mass,tanb,plus1sigma);
	graph_observed_2d->SetPoint(kTwod,mass,tanb,obs);
	kTwod++;
      }	
    }	  
    //push back graphs and save mass for tex/txt output printing
    v_graph_minus1sigma.push_back(graph_minus1sigma);
    v_graph_expected.push_back(graph_expected);
    v_graph_plus1sigma.push_back(graph_plus1sigma);
    v_graph_observed.push_back(graph_observed);
    //masses[imass]=mass;
    
    // Interpolation along the y-axis for filling everything in between
    if(FitMethod_==0 || FitMethod_==1 || FitMethod_==3 || FitMethod_==4){ //linear fit=0; spline=1; spline+linear=3; linear+spline=4
      limit->GetEntry(index[0]);
      float tbmin=tanb; 
      limit->GetEntry(index[nevent-1]);
      float tbmax=tanb; 
      for(int idy=1; idy<plane_minus1sigma->GetNbinsY()+1; idy++){
	if (plane_minus1sigma->GetYaxis()->GetBinCenter(idy) > tbmin && plane_minus1sigma->GetYaxis()->GetBinCenter(idy) < tbmax ){
	  if(FitMethod_==0 || FitMethod_==4 ){
	    plane_minus1sigma->SetBinContent(plane_minus1sigma->GetXaxis()->FindBin(mass), idy, graph_minus1sigma->Eval(plane_minus1sigma->GetYaxis()->GetBinLowEdge(idy)));
	    plane_expected   ->SetBinContent(plane_expected   ->GetXaxis()->FindBin(mass), idy, graph_expected   ->Eval(plane_expected   ->GetYaxis()->GetBinLowEdge(idy)));
	    plane_plus1sigma ->SetBinContent(plane_plus1sigma ->GetXaxis()->FindBin(mass), idy, graph_plus1sigma ->Eval(plane_plus1sigma ->GetYaxis()->GetBinLowEdge(idy)));
	    plane_observed   ->SetBinContent(plane_observed   ->GetXaxis()->FindBin(mass), idy, graph_observed   ->Eval(plane_observed   ->GetYaxis()->GetBinLowEdge(idy)));
	  }
	  else if(FitMethod_==1 || FitMethod_==3){
	    plane_minus1sigma->SetBinContent(plane_minus1sigma->GetXaxis()->FindBin(mass), idy, graph_minus1sigma->Eval(plane_minus1sigma->GetYaxis()->GetBinLowEdge(idy), 0, "S"));
	    plane_expected   ->SetBinContent(plane_expected   ->GetXaxis()->FindBin(mass), idy, graph_expected   ->Eval(plane_expected   ->GetYaxis()->GetBinLowEdge(idy), 0, "S"));
	    plane_plus1sigma ->SetBinContent(plane_plus1sigma ->GetXaxis()->FindBin(mass), idy, graph_plus1sigma ->Eval(plane_plus1sigma ->GetYaxis()->GetBinLowEdge(idy), 0, "S"));
	    plane_observed   ->SetBinContent(plane_observed   ->GetXaxis()->FindBin(mass), idy, graph_observed   ->Eval(plane_observed   ->GetYaxis()->GetBinLowEdge(idy), 0, "S"));
	  }
	}
	else if(plane_minus1sigma->GetYaxis()->GetBinCenter(idy) < tbmin){
	  plane_minus1sigma->SetBinContent(plane_minus1sigma->GetXaxis()->FindBin(mass), idy, graph_minus1sigma->GetY()[0]);
	  plane_expected   ->SetBinContent(plane_expected   ->GetXaxis()->FindBin(mass), idy, graph_expected   ->GetY()[0]);
	  plane_plus1sigma ->SetBinContent(plane_plus1sigma ->GetXaxis()->FindBin(mass), idy, graph_plus1sigma ->GetY()[0]);
	  plane_observed   ->SetBinContent(plane_observed   ->GetXaxis()->FindBin(mass), idy, graph_observed   ->GetY()[0]);
	}
	else if(plane_minus1sigma->GetYaxis()->GetBinCenter(idy) > tbmax){
	  plane_minus1sigma->SetBinContent(plane_minus1sigma->GetXaxis()->FindBin(mass), idy, graph_minus1sigma->GetY()[graph_minus1sigma->GetN()-1]);
	  plane_expected   ->SetBinContent(plane_expected   ->GetXaxis()->FindBin(mass), idy, graph_expected   ->GetY()[graph_expected   ->GetN()-1]);
	  plane_plus1sigma ->SetBinContent(plane_plus1sigma ->GetXaxis()->FindBin(mass), idy, graph_plus1sigma ->GetY()[graph_plus1sigma ->GetN()-1]);
	  plane_observed   ->SetBinContent(plane_observed   ->GetXaxis()->FindBin(mass), idy, graph_observed   ->GetY()[graph_observed   ->GetN()-1]);
	}
      }
    }
  }
	
  // Interpolation along the x-axis for filling everything in between
  if(FitMethod_==0 || FitMethod_==1 || FitMethod_==3){ //linear fit=0; spline=1; spline+linear=3; linear+spline=4
    for(int idy=0; idy<plane_minus1sigma->GetNbinsY()+1; idy++){
      TGraph* graph_minus1sigma_tanb = new TGraph();
      TGraph* graph_expected_tanb = new TGraph();
      TGraph* graph_plus1sigma_tanb = new TGraph();
      TGraph* graph_observed_tanb = new TGraph();
      for(unsigned int imass=0; imass<bins_.size(); ++imass){
	// buffer mass value
	float mass = bins_[imass];
	graph_minus1sigma_tanb->SetPoint(imass, mass, plane_minus1sigma->GetBinContent(plane_minus1sigma->GetXaxis()->FindBin(mass), idy));
	graph_expected_tanb   ->SetPoint(imass, mass, plane_expected   ->GetBinContent(plane_expected   ->GetXaxis()->FindBin(mass), idy));
	graph_plus1sigma_tanb ->SetPoint(imass, mass, plane_plus1sigma ->GetBinContent(plane_plus1sigma ->GetXaxis()->FindBin(mass), idy));
	graph_observed_tanb   ->SetPoint(imass, mass, plane_observed   ->GetBinContent(plane_observed   ->GetXaxis()->FindBin(mass), idy));
      }
      //graph_observed_tanb->SaveAs("graph.root");
      for(int idx=0; idx<plane_minus1sigma->GetNbinsX()+1; idx++){
	if(FitMethod_==0 || FitMethod_==3){
	  plane_minus1sigma->SetBinContent(idx, idy, graph_minus1sigma_tanb->Eval(plane_minus1sigma->GetXaxis()->GetBinLowEdge(idx)));
	  plane_expected   ->SetBinContent(idx, idy, graph_expected_tanb   ->Eval(plane_expected   ->GetXaxis()->GetBinLowEdge(idx)));
	  plane_plus1sigma ->SetBinContent(idx, idy, graph_plus1sigma_tanb ->Eval(plane_plus1sigma ->GetXaxis()->GetBinLowEdge(idx)));
	  plane_observed   ->SetBinContent(idx, idy, graph_observed_tanb   ->Eval(plane_observed   ->GetXaxis()->GetBinLowEdge(idx)));
	}
	else if(FitMethod_==1 || FitMethod_==4){
	  plane_minus1sigma->SetBinContent(idx, idy, graph_minus1sigma_tanb->Eval(plane_minus1sigma->GetXaxis()->GetBinLowEdge(idx), 0, "S"));
	  plane_expected   ->SetBinContent(idx, idy, graph_expected_tanb   ->Eval(plane_expected   ->GetXaxis()->GetBinLowEdge(idx), 0, "S"));
	  plane_plus1sigma ->SetBinContent(idx, idy, graph_plus1sigma_tanb ->Eval(plane_plus1sigma ->GetXaxis()->GetBinLowEdge(idx), 0, "S"));
	  plane_observed   ->SetBinContent(idx, idy, graph_observed_tanb   ->Eval(plane_observed   ->GetXaxis()->GetBinLowEdge(idx), 0, "S"));
	}
      }
    }
  }
  
  if(FitMethod_==2){ //TGrah2D interpolation
    for(int i=0; i<=expected_th2d->GetXaxis()->GetNbins();i++){
      for(int j=0; j<=expected_th2d->GetYaxis()->GetNbins();j++){
	minus1sigma_th2d->SetBinContent(i,j,graph_minus1sigma_2d->Interpolate(minus1sigma_th2d->GetXaxis()->GetBinCenter(i),minus1sigma_th2d->GetYaxis()->GetBinCenter(j)));
	expected_th2d->SetBinContent(i,j,graph_expected_2d->Interpolate(expected_th2d->GetXaxis()->GetBinCenter(i),expected_th2d->GetYaxis()->GetBinCenter(j)));
	plus1sigma_th2d->SetBinContent(i,j,graph_plus1sigma_2d->Interpolate(plus1sigma_th2d->GetXaxis()->GetBinCenter(i),plus1sigma_th2d->GetYaxis()->GetBinCenter(j)));
	observed_th2d->SetBinContent(i,j,graph_observed_2d->Interpolate(observed_th2d->GetXaxis()->GetBinCenter(i),observed_th2d->GetYaxis()->GetBinCenter(j)));
      }
    }
  }

   // do the plotting
  plottingTanbML(canv, plane_expected, xaxis_, yaxis_, theory_, min_, max_, log_); 
  /// setup the CMS Preliminary
  TPaveText* cmsprel = new TPaveText(0.145, 0.835+0.06, 0.145+0.30, 0.835+0.16, "NDC");
  //TPaveText* cmsprel = new TPaveText(0.135, 0.735, 0.145+0.30, 0.785, "NDC"); // for "unpublished" in header
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
//   if(txt_){
//     print(std::string(output_).append("_").append(extralabel_).append(label_).c_str(), v_graph_minus2sigma, v_graph_minus1sigma, v_graph_expected, v_graph_plus1sigma, v_graph_plus2sigma, v_graph_observed, tanbLow, tanbHigh, masses, "txt");
//     print(std::string(output_).append("_").append(extralabel_).append(label_).c_str(), v_graph_minus2sigma, v_graph_minus1sigma, v_graph_expected, v_graph_plus1sigma, v_graph_plus2sigma, v_graph_observed, tanbLow, tanbHigh, masses, "tex");
//   }
  if(root_){
    TFile* output = new TFile(std::string(output_).append("_").append(extralabel_).append(label_).append(".root").c_str(), "update");
    if(!output->cd(output_.c_str())){
      output->mkdir(output_.c_str());
      output->cd(output_.c_str());
    }
    plane_minus1sigma->Write("plane_minus1sigma");   
    plane_expected   ->Write("plane_expected");   
    plane_plus1sigma ->Write("plane_plus1sigma");  
    plane_observed   ->Write("plane_observed");    
  //   for(unsigned int i=0; i<gr_observed.size(); i++){
//       gr_observed[i]   ->Write(TString::Format("gr_observed_%d", i)  ); 
//     }
//     for(unsigned int i=0; i<gr_expected.size(); i++){
//       gr_expected[i]   ->Write(TString::Format("gr_expected_%d", i)    );
//     }
//     for(unsigned int i=0; i<gr_minus1sigma.size(); i++){
//       gr_minus1sigma[i]->Write(TString::Format("gr_minus1sigma_%d", i)    ); 
//     }
//     for(unsigned int i=0; i<gr_plus1sigma.size(); i++){
//       gr_plus1sigma[i] ->Write(TString::Format("gr_plus1sigma_%d", i)     );
//     }
    output->Close();
  }
  return;
}
