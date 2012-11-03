#include "map"
#include "vector" 
#include "string"
#include "utility" 
#include "cstdlib"
#include "fstream"
#include "iostream"
#include "algorithm"

#include "TF1.h"
#include "TH1F.h"
#include "TMath.h"
#include "TFile.h"
#include "TTree.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TSpline.h"

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"


/// typedef CrossPoint to a bin plus flag on falling or rising intercept, true for falling
typedef std::pair<int, bool> CrossPoint;
/// enumerator of limit types
enum LimitType        {observed=0, minus_2sigma=1, minus_1sigma=2, expected=3, plus_1sigma=4, plus_2sigma=5, all_types=6};
/// limit types as saved in combine
float LimitTypes[7] = {       -1.,          0.025,          0.160,      0.500,         0.840,         0.975             };


std::string limitType(unsigned int type)
{
  switch(type){
  case observed :
    return std::string("OBS");
  case minus_2sigma :
    return std::string("025");
  case minus_1sigma :
    return std::string("160");
  case expected     :
    return std::string("EXP");
  case plus_1sigma  :
    return std::string("840");
  case plus_2sigma  :
    return std::string("975");
  };
  return std::string("UNKNOWN");
}

double singlePointLimit(std::string filename, float tanb, unsigned int LIMIT_TYPE, unsigned int verbosity=0)
{
  /*
    Get the observed, expected and +/-1 ans +/-2 sigma band from limit trees, which are the 
    output of combine
  */
  TString fullpath; fullpath = TString::Format(filename.c_str(), tanb); TFile* file = new TFile(fullpath); 
  if(file->IsZombie()){ if( verbosity>0 ){ std::cout << "> File not found: " << fullpath << std::endl; } return -999.; }
  TTree* tree = (TTree*) file->Get("limit");
  if(!tree){ if( verbosity>0 ){ std::cout << "> Tree not found in file: " << fullpath << std::endl; } return -999.; }
  int nevent = tree->GetEntries();
  if( nevent<=0 ){ if( verbosity>0 ){ std::cout << "> Tree is empty" << std::endl; } return -999.; }

  float type; double value;
  tree->SetBranchAddress("quantileExpected", &type );
  tree->SetBranchAddress("limit"           , &value);
  float target = LimitTypes[LIMIT_TYPE]; double limit = -999;
  for(int idx=0; idx<nevent; ++idx){
    tree->GetEvent(idx);
    if( fabs(type-target)<0.001 ){
      // allow for some tolerance for determination of type
      if( verbosity>1 ){ std::cout << "tanb: " << tanb << " limit (" << limitType(LIMIT_TYPE) << ") = " << value/tanb << std::endl; }
      limit = value/tanb; 
    }
  }
  file->Close();
  return limit;
}

std::vector<CrossPoint> crossPoints(TGraph*& graph)
{
  /*
    Determine all cross points of graph with y==1 
  */
  std::vector<CrossPoint> points;
  for(int ibin=0; ibin<graph->GetN()-1; ++ibin){
    if((graph->GetY()[ibin]-1.)*(graph->GetY()[ibin+1]-1.)<=0){
      points.push_back(std::make_pair(ibin, (graph->GetY()[ibin]>graph->GetY()[ibin+1])));
    }
  }
  return points;
}

void fillTree(TTree*& tree, TGraph*& graph, double& limit, unsigned int itype, std::map<double, std::string>& tanb_values, bool upper_exclusion, unsigned int verbosity)
{
  double value=-99;
  double tanb_help=-99;
  unsigned int ibin=0;
  // fill graph with scanned points
  for(std::map<double, std::string>::const_iterator tanb = tanb_values.begin(); tanb!=tanb_values.end(); ++tanb){
    value = singlePointLimit(tanb->second, tanb->first, itype, verbosity);
    if( value>0 ){
      graph->SetPoint(ibin++, tanb->first, value); 
    }
    tanb_help=tanb->first;
  }
  // determine smooth curve on graph for interpolation
  TSpline3* spline = new TSpline3("spline", graph, "r", 3., 10.);
  // determine all crossing points with y==1 
  std::vector<CrossPoint> points = crossPoints(graph);

  int dist = 1;
  bool filled = false;
  unsigned int np = 0;
  unsigned int steps = 10e6; 
  if(points.size()>0) limit = graph->GetX()[upper_exclusion ? points.begin()->first : points.end()->first];

  for(std::vector<CrossPoint>::const_reverse_iterator point = points.rbegin(); point!=points.rend(); ++point, ++np){
    double min = (point->first-dist)>0 ? graph->GetX()[point->first-dist] : graph->GetX()[0]; 
    double max = (point->first+dist)<graph->GetN() ? graph->GetX()[point->first+dist] : graph->GetX()[graph->GetN()-1];

    double y_min = (point->first-dist)>0 ? graph->GetY()[point->first-dist] : graph->GetY()[0]; 
    double y_max = (point->first+dist)<graph->GetN() ? graph->GetY()[point->first+dist] : graph->GetY()[graph->GetN()-1];
    double crossing  = (1.-y_min)/(y_max-y_min)*(max-min);
				  
    double deltaM = -999.;
    double offset = min; double step_size = (max-min)/steps;
    for(unsigned int scan=0; scan<=steps; ++scan){
      if(deltaM<0 || fabs(spline->Eval(offset+scan*step_size)-1.)<deltaM){
	limit=offset+scan*step_size;
	deltaM=fabs(spline->Eval(offset+scan*step_size)-1.);
      }
    }
    std::cout << "****************************************************************" << std::endl;
    std::cout << "* [" << np+1 << "|" << point->second << "] asymptotic limit(";
    std::cout << limitType(itype) << ") :" << crossing << " -- " << limit << " deltaM : " << deltaM;
    if(((upper_exclusion && point->second) || (!upper_exclusion && !(point->second))) && !filled){
      //std::cout << "limit is taken from linear interpolation at the moment" << std::endl;
      //limit = crossing;
      std::cout << "    [-->to file]"; filled=true; tree->Fill();
    }
    std::cout << endl;
    std::cout << "****************************************************************" << std::endl;
  }
  // catch cases where no crossing point was found
  if(!filled){
    if(value<1)
      {
	std::cout << "WARNING: no crossing found - all tanb values excluded: " << value << std::endl;
	if(itype == observed)     { limit=3.00; }
	if(itype == plus_2sigma)  { limit=5.00; }
	if(itype == plus_1sigma)  { limit=4.00; }
	if(itype == expected)     { limit=3.00; }
	if(itype == minus_1sigma) { limit=2.00; }
	if(itype == minus_2sigma) { limit=1.00; }
	tree->Fill();
      }
    else
      {
	std::cout << "WARNING: no crossing found - no tanb value excluded" << value << " -- " << tanb_help << std::endl;
	if(itype == observed)     { limit=tanb_help*value; }
	if(itype == plus_2sigma)  { limit=tanb_help*value; }
	if(itype == plus_1sigma)  { limit=tanb_help*value; }
	if(itype == expected)     { limit=tanb_help*value; }
	if(itype == minus_1sigma) { limit=tanb_help*value; }
	if(itype == minus_2sigma) { limit=tanb_help*value; }
	tree->Fill();
      }
  }
  if( verbosity>0 ){
    std::string monitor = std::string("SCAN-")+limitType(itype);
    TCanvas* canv = new TCanvas(monitor.c_str(), monitor.c_str(), 600, 600);
    TH1F* frame = canv->DrawFrame(graph->GetX()[0]-0.1, 0., graph->GetX()[graph->GetN()-1]+0.1, 3.);
    canv->SetGridx(1); canv->SetGridy(1); canv->cd(); 
    graph->SetMarkerStyle(20.); 
    graph->SetMarkerColor(kBlack); 
    graph->SetMarkerSize(1.3); 
    graph->Draw("P");
    spline->SetLineColor(kBlue); 
    spline->SetLineWidth(3.); 
    spline->Draw("same");
    canv->Print(monitor.append(".png").c_str(), "png");
    delete frame; delete canv; delete spline;
  }
  return;
}

void asymptoticLimit(const char* outputfile, const char* inputfiles, unsigned int verbosity=0, bool upper_exclusion=true)
{
  // prepare input names from inputfiles
  std::vector<std::string> tanb_files;
  string2Vector(cleanupWhitespaces(inputfiles), tanb_files);
  // prepare tanb values from inputfiles
  std::map<double, std::string> tanb_values;  
  for(std::vector<std::string>::const_iterator tanb_file = tanb_files.begin(); tanb_file!=tanb_files.end(); ++tanb_file){
    tanb_values[atof(tanb_file->substr(tanb_file->rfind("_")+1, tanb_file->find(".root")-tanb_file->rfind("_")-1).c_str())] = *tanb_file;
  }

  double limit;
  TGraph* graph = new TGraph();
  TFile* file = TFile::Open(outputfile, "update");
  TTree* tree = new TTree("limit", "limit");
  tree->Branch("limit", &limit, "limit/D");
  for(unsigned int itype=0; itype<all_types; ++itype){
    graph->Clear();
    if( std::string(outputfile).find("quant0.027")!=std::string::npos ){
      if( itype == minus_2sigma ){
	fillTree(tree, graph, limit, itype, tanb_values, upper_exclusion, verbosity);
	break;
      }
    }
    else if( std::string(outputfile).find("quant0.160")!=std::string::npos ){
      if( itype == minus_1sigma ){
	fillTree(tree, graph, limit, itype, tanb_values, upper_exclusion, verbosity);
	break;
      }
    }
    else if( std::string(outputfile).find("quant0.500")!=std::string::npos ){
      if( itype == expected ){
	fillTree(tree, graph, limit, itype, tanb_values, upper_exclusion, verbosity);
	break;
      }
    }
    else if( std::string(outputfile).find("quant0.840")!=std::string::npos ){
      if( itype == plus_1sigma ){
	fillTree(tree, graph, limit, itype, tanb_values, upper_exclusion, verbosity);
	break;
      }
    }
    else if( std::string(outputfile).find("quant0.975")!=std::string::npos ){
      if( itype == plus_2sigma ){
	fillTree(tree, graph, limit, itype, tanb_values, upper_exclusion, verbosity);
	break;
      }
    }
    else{
      if( itype == observed ){
	fillTree(tree, graph, limit, itype, tanb_values, upper_exclusion, verbosity);
      }
    }
  }
  file->cd();
  tree->Write();
  file->Close();
  delete graph;

  return;
}
