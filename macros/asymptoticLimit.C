#include "map"
#include "vector" 
#include "string"
#include "utility" 
#include "cstdlib"
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

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"


/// enumerator of limits types
enum LimitType {observed=0, minus_2sigma=1, minus_1sigma=2, expected=3, plus_1sigma=4, plus_2sigma=5, all_types=6};
/// typedef CrossPoint to a bin plus flag on falling or rising edge
typedef std::pair<int, bool> CrossPoint;

double singlePointLimit(std::string filename, float tanb, unsigned int selected_type, unsigned int verbosity=0)
{
  TString fullpath;
  fullpath = TString::Format(filename.c_str(), tanb);
  TFile* file = new TFile(fullpath); 
  if(file->IsZombie()){ if( verbosity>0 ){ std::cout << "file not found: " << fullpath  << std::endl; } return -999.; }
  TTree* tree = (TTree*) file->Get("limit");
  if(!tree){ if( verbosity>0 ){ std::cout << "tree not found: limit" << std::endl; } return -999.; }

  float type; 
  double value;
  tree->SetBranchAddress("quantileExpected", &type);
  tree->SetBranchAddress("limit"           , &value);

  float target_type = -999.;
  if( selected_type == observed     ){ target_type =   -1.; }
  if( selected_type == minus_2sigma ){ target_type = 0.025; }
  if( selected_type == minus_1sigma ){ target_type = 0.160; }
  if( selected_type == expected     ){ target_type = 0.500; }
  if( selected_type == plus_1sigma  ){ target_type = 0.840; }
  if( selected_type == plus_2sigma  ){ target_type = 0.975; }

  double limit = -999;
  int nevent = tree->GetEntries();
  if( nevent<=0 ){ if( verbosity>0 ){ std::cout << "tree is empty" << std::endl; } return -999.; }
  for(int idx=0; idx<nevent; ++idx){
    tree->GetEvent(idx);
    if( fabs(type-target_type)<0.001 ){
      if( verbosity>0 ){ 
	if( type>0 ){	
	  std::cout << "tanb: " << tanb << " limit (exp" << type << ") = " << value/tanb << std::endl; 
	}
	else
	  std::cout << "tanb: " << tanb << " limit (observed ) = " << value/tanb << std::endl;
      }
      limit = value/tanb; 
    }
  }
  file->Close();
  return limit;
}

double edges(std::map<double, std::string>& tanb_values, bool min)
{
  double edge_value = min ? 999. : -999.;
  for(std::map<double, std::string>::const_iterator itanb=tanb_values.begin(); itanb!=tanb_values.end(); ++itanb){
    if( min ){
      if( edge_value>itanb->first ){ edge_value= itanb->first; }
    }
    else{
      if( edge_value<itanb->first ){ edge_value= itanb->first; }
    }
  }
  return edge_value;
}

double min(std::map<double, std::string> tanb_values){ return edges(tanb_values, true ); }

double max(std::map<double, std::string> tanb_values){ return edges(tanb_values, false); }

std::string enum2string(unsigned int type)
{
  switch(type){
  case observed :
    return std::string("observed"    );
  case minus_2sigma :
    return std::string("minus_2sigma");
  case minus_1sigma :
    return std::string("minus_1sigma");
  case expected     :
    return std::string("expected"    );
  case plus_1sigma  :
    return std::string("plus_1sigma" );
  case plus_2sigma  :
    return std::string("plus_2sigma" );
  };
  return std::string("unknown");
}

std::vector<CrossPoint> crossPoints(TGraph*& graph)
{
  std::vector<CrossPoint> points;
  for(int ibin=0; ibin<graph->GetN()-1; ++ibin){
    if((graph->GetY()[ibin]-1.)*(graph->GetY()[ibin+1]-1.)<=0){
      points.push_back(std::make_pair(ibin, (graph->GetY()[ibin]>graph->GetY()[ibin+1])));
    }
  }
  return points;
}

bool convex(TGraph*& graph, const CrossPoint& point){
  if ( 0 == point.first ){
    float deltaY = graph->GetY()[point.first+2]-graph->GetY()[point.first  ];
    float deltaX = graph->GetX()[point.first+2]-graph->GetX()[point.first  ];
    return deltaY/deltaX*(graph->GetX()[point.first+1]-graph->GetX()[point.first])>graph->GetY()[point.first+1];
  }
  if( 0<point.first && point.first<graph->GetN() ){
    float deltaY = graph->GetY()[point.first+1]-graph->GetY()[point.first-1];
    float deltaX = graph->GetX()[point.first+1]-graph->GetX()[point.first-1];
    return deltaY/deltaX*(graph->GetX()[point.first]-graph->GetX()[point.first-1])>graph->GetY()[point.first  ];
  }
  else{
    float deltaY = graph->GetY()[point.first  ]-graph->GetY()[point.first-2];
    float deltaX = graph->GetX()[point.first  ]-graph->GetX()[point.first-2];
    return deltaY/deltaX*(graph->GetX()[point.first]-graph->GetX()[point.first-1])>graph->GetY()[point.first-1];
  }
}

void fillTree(TTree*& tree, TGraph*& graph, double& limit, unsigned int itype, std::map<double, std::string>& tanb_values, bool upper_exclusion, unsigned int verbosity)
{
  unsigned int ibin=0;
  for(std::map<double, std::string>::const_iterator tanb = tanb_values.begin(); tanb!=tanb_values.end(); ++tanb){
    double value = singlePointLimit(tanb->second, tanb->first, itype, verbosity);
    if( value>0 ){
      graph->SetPoint(ibin++, tanb->first, value); 
    }
  }
  TF1* interpol;
  bool filled = false;
  std::vector<CrossPoint> points = crossPoints(graph);
  for(std::vector<CrossPoint>::const_iterator point = points.begin(); point!=points.end(); ++point){
    TString fnc("fnc_"); fnc+=point->first;
    int dist = 2;
    double min = (point->first-dist)>0 ? graph->GetX()[point->first-dist] : graph->GetX()[0]; 
    double max = (point->first+dist)<graph->GetN() ? graph->GetX()[point->first+dist] : graph->GetX()[graph->GetN()-1];
    if(point->second){
      if( !convex(graph, *point) ){
	std::cout << "falling convex - applied model: [0]*1/([1]+x)^[2]" << std::endl;
	//interpol = new TF1(fnc, "[0]*exp([1]*(x-[2]))", 1., 70.);
	//graph->Fit(fnc, "EM+", "", min, max);
	//float p0 = graph->GetFunction(fnc)->GetParameter(0);
	//float p1 = graph->GetFunction(fnc)->GetParameter(1);
	//float p2 = graph->GetFunction(fnc)->GetParameter(2);
	//limit = (p0<=0 || p1==0) ? -999 : -TMath::Log(p0)/p1+p2;
	interpol = new TF1(fnc, "[0]*1/([1]+x)^[2]", 3., 70.);
	graph->Fit(fnc, "EM+", "", min, max);
	float p0 = graph->GetFunction(fnc)->GetParameter(0);
	float p1 = graph->GetFunction(fnc)->GetParameter(1);
	float p2 = graph->GetFunction(fnc)->GetParameter(2);
	limit = (p2==0) ? -999. : TMath::Power(p0,1./p2)-p1;
      }
      else{
	std::cout << "falling concav - applied model: [2]+[1]*x+[0]*x*x" << std::endl;
	interpol = new TF1(fnc, "[2]+[1]*x+[0]*x*x", 1., 70.);
	graph->Fit(fnc, "EM+", "", min, max);
	float p0 = graph->GetFunction(fnc)->GetParameter(0);
	float p1 = graph->GetFunction(fnc)->GetParameter(1);
	float p2 = graph->GetFunction(fnc)->GetParameter(2)-1.;
	float p3 = TMath::Sqrt(p1*p1-4*p0*p2);
	limit = fabs((-p1-p3)/(2*p0)-point->first)<fabs((-p1+p3)/(2*p0)-point->first) ? (-p1-p3)/(2*p0) : (-p1+p3)/(2*p0); 
      }
      std::cout << "*************************************************"   << std::endl;
      std::cout << "* asymptotic limit(type " << itype << ") :" << limit;
      if( upper_exclusion && !filled ){
	std::cout << " [to file]"; filled=true; tree->Fill();
      }
      std::cout << std::endl;
      std::cout << "*************************************************"   << std::endl;
    }
    else{
      if( !convex(graph, *point) ){
	std::cout << "rising convex - applied model: [0]+[1]*1/([2]+x)^[3]" << std::endl;
	//interpol = new TF1(fnc, "[0]*exp([1]*(x-[2]))", 1., 70.);
	//graph->Fit(fnc, "EM+", "", min, max);
	//float p0 = graph->GetFunction(fnc)->GetParameter(0);
	//float p1 = graph->GetFunction(fnc)->GetParameter(1);
	//float p2 = graph->GetFunction(fnc)->GetParameter(2);
	//limit = (p0<=0 || p1==0) ? -999 : -TMath::Log(p0)/p1+p2;
	interpol = new TF1(fnc, "[0]+[1]*1/([2]+x)^[3]", 3., 70.);
	graph->Fit(fnc, "EM+", "", min, max);
	float p0 = graph->GetFunction(fnc)->GetParameter(0);
	float p1 = graph->GetFunction(fnc)->GetParameter(1);
	float p2 = graph->GetFunction(fnc)->GetParameter(2);
	float p3 = graph->GetFunction(fnc)->GetParameter(3);
	limit = (p0 == 1 || p3 == 0) ? -999. : TMath::Power(p1/(1.-p0),1./p3)-p2;
      }
      else{
	std::cout << "rising concav - applied model: [0]+[1]*exp([2]+[3]*x)" << std::endl;
	//interpol = new TF1(fnc, "[2]+[1]*x+[0]*x*x", 1., 70.);
	//graph->Fit(fnc, "EM+", "", min, max);
	//float p0 = graph->GetFunction(fnc)->GetParameter(0);
	//float p1 = graph->GetFunction(fnc)->GetParameter(1);
	//float p2 = graph->GetFunction(fnc)->GetParameter(2)-1.;
	//float p3 = TMath::Sqrt(p1*p1-4*p0*p2);
	interpol = new TF1(fnc, "[0]+[1]*exp([2]+[3]*x)", 1., 70.);
	graph->Fit(fnc, "EM+", "", min, max);
	float p0 = graph->GetFunction(fnc)->GetParameter(0);
	float p1 = graph->GetFunction(fnc)->GetParameter(1);
	float p2 = graph->GetFunction(fnc)->GetParameter(2);
	float p3 = graph->GetFunction(fnc)->GetParameter(3);
	limit = (p0 == 1 || p2 == 0 || p3 == 0) ? -999. : (TMath::Log(1.-p0) - TMath::Log(p1) - p2)/p3; 
      }
      std::cout << "*************************************************"   << std::endl;
      std::cout << "* asymptotic limit(type " << itype << ") :" << limit;
      if( !upper_exclusion && !filled ){
	std::cout << " [to file]"; filled=true; tree->Fill();
      }
      std::cout << std::endl;
      std::cout << "*************************************************"   << std::endl;
    }
    delete interpol;
  }
  if( verbosity>1 ){
    std::string monitor = enum2string(itype);
    TCanvas* canv = new TCanvas(monitor.c_str(), monitor.c_str(), 600, 600);
    TH1F* frame = canv->DrawFrame(min(tanb_values), 0., max(tanb_values), 2.);
    canv->SetGridx(1); canv->SetGridy(1); canv->cd(); graph->SetMarkerStyle(20.); graph->SetMarkerColor(kBlack); graph->SetMarkerSize(1.3); graph->Draw("P");
    canv->Print(monitor.append(".png").c_str(), "png");
    delete frame;
    delete canv;
  }
  return;
}

void asymptoticLimit(const char* outputfile, const char* inputfiles, unsigned int verbosity=0, bool upper_exclusion=true)
{
  /// prepare input names from inputfiles
  std::vector<std::string> tanb_files;
  string2Vector(cleanupWhitespaces(inputfiles), tanb_files);
  /// prepare tanb values from inputfiles
  std::map<double, std::string> tanb_values;  
  for(std::vector<std::string>::const_iterator tanb_file = tanb_files.begin(); tanb_file!=tanb_files.end(); ++tanb_file){
    tanb_values[atof(tanb_file->substr(tanb_file->rfind("_")+1, tanb_file->find(".root")-tanb_file->rfind("_")-1).c_str())] = *tanb_file;
  }
  
  double limit;
  TFile* file = TFile::Open(outputfile, "update");
  TTree* tree = new TTree("limit", "limit");
  tree->Branch("limit", &limit, "limit/D");

  TGraph* graph = new TGraph();
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
