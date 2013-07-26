#include "string" 
#include "vector" 
#include "fstream"
#include "iomanip"
#include "iostream"
#include "algorithm"

#include "TTree.h"
#include "TFile.h"
#include "TAxis.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TPaveLabel.h"
#include "TGraphAsymmErrors.h"

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"
#include "HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"

static const double MARKER_SIZE = 0.9;  // 1.3

bool
channel(std::string& label){
  return (label==std::string("HIG-12-043") ||
	  label==std::string("HIG-12-050")
	  );
}

std::string legendEntry(const std::string& channel){
  std::string title;
  if(channel==std::string("HIG-12-043")) title = std::string("HIG-12-043 (17 fb^{-1})");
  if(channel==std::string("HIG-12-050")) title = std::string("HIG-12-050 (17 fb^{-1})");
  return title;
}

void compareSignalShapesMSSM(std::string path, std::string category, std::string channel, std::string period, const char* shapestr1, const char* shapestr2, double minimum=0., double maximum=20., bool log=false, const char* label=" Preliminary, H#rightarrow#tau#tau, L=19.8 fb^{-1} at 8TeV")
{
  SetStyle();

  std::map<std::string, unsigned int> colors;
  colors["HIG-12-043" ] = kBlack;
  colors["HIG-12-050" ] = kBlack;


  std::cout << " *******************************************************************************************************\n"
	    << " * Usage     : root -l                                                                                  \n"
	    << " *             .x compareSignalShapesMSSM.C+(file, category, shape1, shape2, max, min)                  \n"
	    << " *                                                                                                      \n"
	    << " * Arguments :  + path     string           path to directory where files are stored                    \n"
	    << " *                                          must be 'common' directory                                  \n"
	    << " *              + category string           choose which category should be compared,                   \n"
	    << " *              + channel  string           choose which channel  should be compared,                   \n"
	    << " *              + period   string           choose which period   should be compared,                   \n"
	    << " *                                          e.g. btag, nobtag                                           \n"
	    << " *              + shape1   const char*      list of shapes to be compared to shape2                     \n"
	    << " *                                          The list should be comma separated and may contain          \n"
	    << " *                                          whitespaces                                                 \n"
	    << " *              + shape2   const char*      list of shapes to be compared to shape1                     \n"
	    << " *                                          The list should be comma separated and may contain          \n"
	    << " *                                          whitespaces                                                 \n"
	    << " *              + max       double          maximum of the plot (default is 20.)                        \n"
	    << " *                                                                                                      \n"
	    << " *              + min       double          minimum of the plot (default is  0.)                        \n"
	    << " *                                                                                                      \n"
	    << " *              + log       bool            set log scale yes or no (default is false)                  \n"
	    << " *                                                                                                      \n"
	    << " *******************************************************************************************************\n";


  /// prepare input parameters
  std::vector<std::string> shape1;
  string2Vector(cleanupWhitespaces(shapestr1), shape1);
  std::vector<std::string> shape2;
  string2Vector(cleanupWhitespaces(shapestr2), shape2); 
  std::vector<std::string> shape3;
  string2Vector(cleanupWhitespaces(shapestr1), shape3);
  std::vector<std::string> shape4;
  string2Vector(cleanupWhitespaces(shapestr2), shape4);
  std::vector<std::string> shape5;
  string2Vector(cleanupWhitespaces(shapestr1), shape5);
  std::vector<std::string> shape6;
  string2Vector(cleanupWhitespaces(shapestr2), shape6);
  /// test input files 
  std::vector<std::string> filenames;
  filenames.push_back(std::string(path+"/"+"htt_"+channel+".inputs-mssm-"+period+"-0.root_130_1.0"));
  filenames.push_back(std::string(path+"/"+"htt_"+channel+".inputs-mssm-"+period+"-0.root_130_2.0"));	
  filenames.push_back(std::string(path+"/"+"htt_"+channel+".inputs-mssm-"+period+"-0.root_130_6.0"));
  filenames.push_back(std::string(path+"/"+"htt_"+channel+".inputs-mssm-"+period+"-0.root_130_12.0"));	
  filenames.push_back(std::string(path+"/"+"htt_"+channel+".inputs-mssm-"+period+"-0.root_130_20.0"));
  filenames.push_back(std::string(path+"/"+"htt_"+channel+".inputs-mssm-"+period+"-0.root_130_30.0"));	
  
  TFile* inputFile0 = new TFile(filenames[0].c_str()); 
  if(inputFile0->IsZombie()){ 
    std::cout << "ERROR:: file: " << filenames[0] << " does not exist -> Will be removed from list of files." << std::endl; 
    filenames.erase(filenames.begin());
  } 
  TFile* inputFile1 = new TFile(filenames[1].c_str()); 
  if(inputFile1->IsZombie()){ 
    std::cout << "ERROR:: file: " << filenames[1] << " does not exist -> Will be removed from list of files." << std::endl; 
    filenames.erase(filenames.begin()+1);
  }  
  TFile* inputFile2 = new TFile(filenames[2].c_str()); 
  if(inputFile2->IsZombie()){ 
    std::cout << "ERROR:: file: " << filenames[2] << " does not exist -> Will be removed from list of files." << std::endl; 
    filenames.erase(filenames.begin());
  } 
  TFile* inputFile3 = new TFile(filenames[3].c_str()); 
  if(inputFile3->IsZombie()){ 
    std::cout << "ERROR:: file: " << filenames[3] << " does not exist -> Will be removed from list of files." << std::endl; 
    filenames.erase(filenames.begin()+1);
  }
  TFile* inputFile4 = new TFile(filenames[4].c_str()); 
  if(inputFile4->IsZombie()){ 
    std::cout << "ERROR:: file: " << filenames[4] << " does not exist -> Will be removed from list of files." << std::endl; 
    filenames.erase(filenames.begin());
  }  
  TFile* inputFile5 = new TFile(filenames[5].c_str()); 
  if(inputFile5->IsZombie()){ 
    std::cout << "ERROR:: file: " << filenames[5] << " does not exist -> Will be removed from list of files." << std::endl; 
    filenames.erase(filenames.begin()+1);
  }
  
  std::vector<TH1F*> hshape1;
  std::vector<TH1F*> hshape2;
  std::vector<TH1F*> hshape3;
  std::vector<TH1F*> hshape4;
  std::vector<TH1F*> hshape5;
  std::vector<TH1F*> hshape6;
  /// prepare histograms
  for(unsigned i=0; i<shape1.size(); ++i){
    //if(filenames[0].find("_em")!=std::string::npos) hshape1.push_back(get<TH1F>(inputFile0, std::string("emu_"+category+"/").append(shape1[i]).c_str()));
    // if(filenames[0].find("_et")!=std::string::npos) hshape1.push_back(get<TH1F>(inputFile0, std::string("eleTau_"+category+"/").append(shape1[i]).c_str()));
    //if(filenames[0].find("_mm")!=std::string::npos) hshape1.push_back(get<TH1F>(inputFile0, std::string("mumu_"+category+"/").append(shape1[i]).c_str()));
    if(filenames[0].find("_mt")!=std::string::npos) hshape1.push_back(get<TH1F>(inputFile0, std::string("muTau_"+category+"/").append(shape1[i]).c_str()));
    //if(filenames[0].find("_tt")!=std::string::npos) hshape1.push_back(get<TH1F>(inputFile0, std::string("tauTau"+category+"/").append(shape1[i]).c_str()));		   	       
  }
  for(unsigned i=0; i<shape2.size(); ++i){
    //if(filenames[1].find("_em")!=std::string::npos) hshape2.push_back(get<TH1F>(inputFile1, std::string("emu_"+category+"/").append(shape2[i]).c_str()));
    //if(filenames[1].find("_et")!=std::string::npos) hshape2.push_back(get<TH1F>(inputFile1, std::string("eleTau_"+category+"/").append(shape2[i]).c_str()));
    //if(filenames[1].find("_mm")!=std::string::npos) hshape2.push_back(get<TH1F>(inputFile1, std::string("mumu_"+category+"/").append(shape2[i]).c_str()));
    if(filenames[1].find("_mt")!=std::string::npos) hshape2.push_back(get<TH1F>(inputFile1, std::string("muTau_"+category+"/").append(shape2[i]).c_str()));
    //if(filenames[1].find("_tt")!=std::string::npos) hshape2.push_back(get<TH1F>(inputFile1, std::string("tauTau"+category+"/").append(shape2[i]).c_str()));
  }
  for(unsigned i=0; i<shape3.size(); ++i){
    //if(filenames[0].find("_em")!=std::string::npos) hshape1.push_back(get<TH1F>(inputFile0, std::string("emu_"+category+"/").append(shape1[i]).c_str()));
    // if(filenames[0].find("_et")!=std::string::npos) hshape1.push_back(get<TH1F>(inputFile0, std::string("eleTau_"+category+"/").append(shape1[i]).c_str()));
    //if(filenames[0].find("_mm")!=std::string::npos) hshape1.push_back(get<TH1F>(inputFile0, std::string("mumu_"+category+"/").append(shape1[i]).c_str()));
    if(filenames[2].find("_mt")!=std::string::npos) hshape3.push_back(get<TH1F>(inputFile2, std::string("muTau_"+category+"/").append(shape3[i]).c_str()));
    //if(filenames[0].find("_tt")!=std::string::npos) hshape1.push_back(get<TH1F>(inputFile0, std::string("tauTau"+category+"/").append(shape1[i]).c_str()));		   	       
  }
  for(unsigned i=0; i<shape4.size(); ++i){
    //if(filenames[1].find("_em")!=std::string::npos) hshape2.push_back(get<TH1F>(inputFile1, std::string("emu_"+category+"/").append(shape2[i]).c_str()));
    //if(filenames[1].find("_et")!=std::string::npos) hshape2.push_back(get<TH1F>(inputFile1, std::string("eleTau_"+category+"/").append(shape2[i]).c_str()));
    //if(filenames[1].find("_mm")!=std::string::npos) hshape2.push_back(get<TH1F>(inputFile1, std::string("mumu_"+category+"/").append(shape2[i]).c_str()));
    if(filenames[3].find("_mt")!=std::string::npos) hshape4.push_back(get<TH1F>(inputFile3, std::string("muTau_"+category+"/").append(shape4[i]).c_str()));
    //if(filenames[1].find("_tt")!=std::string::npos) hshape2.push_back(get<TH1F>(inputFile1, std::string("tauTau"+category+"/").append(shape2[i]).c_str()));
  }
   for(unsigned i=0; i<shape5.size(); ++i){
    //if(filenames[0].find("_em")!=std::string::npos) hshape1.push_back(get<TH1F>(inputFile0, std::string("emu_"+category+"/").append(shape1[i]).c_str()));
    // if(filenames[0].find("_et")!=std::string::npos) hshape1.push_back(get<TH1F>(inputFile0, std::string("eleTau_"+category+"/").append(shape1[i]).c_str()));
    //if(filenames[0].find("_mm")!=std::string::npos) hshape1.push_back(get<TH1F>(inputFile0, std::string("mumu_"+category+"/").append(shape1[i]).c_str()));
    if(filenames[4].find("_mt")!=std::string::npos) hshape5.push_back(get<TH1F>(inputFile4, std::string("muTau_"+category+"/").append(shape5[i]).c_str()));
    //if(filenames[0].find("_tt")!=std::string::npos) hshape1.push_back(get<TH1F>(inputFile0, std::string("tauTau"+category+"/").append(shape1[i]).c_str()));		   	       
   }
  for(unsigned i=0; i<shape6.size(); ++i){
    //if(filenames[1].find("_em")!=std::string::npos) hshape2.push_back(get<TH1F>(inputFile1, std::string("emu_"+category+"/").append(shape2[i]).c_str()));
    //if(filenames[1].find("_et")!=std::string::npos) hshape2.push_back(get<TH1F>(inputFile1, std::string("eleTau_"+category+"/").append(shape2[i]).c_str()));
    //if(filenames[1].find("_mm")!=std::string::npos) hshape2.push_back(get<TH1F>(inputFile1, std::string("mumu_"+category+"/").append(shape2[i]).c_str()));
    if(filenames[5].find("_mt")!=std::string::npos) hshape6.push_back(get<TH1F>(inputFile5, std::string("muTau_"+category+"/").append(shape6[i]).c_str()));
    //if(filenames[1].find("_tt")!=std::string::npos) hshape2.push_back(get<TH1F>(inputFile1, std::string("tauTau"+category+"/").append(shape2[i]).c_str()));
  }
  


  /// do the drawing
  TCanvas* canv1 = new TCanvas("canv1", "Absolute Comparison", 600, 600);
  canv1->cd();
  canv1->SetGridx(1);
  canv1->SetGridy(1);
 
  bool firstPlot=true;
  for(unsigned int i=0; i<hshape1.size(); ++i){
    if(firstPlot){
      if(log){ canv1->SetLogy(1); }
      // format x-axis
      std::string x_title;
      //x_title = std::string("#sigma#timesBR/#sigma#timesBR_{SM}");
      x_title = std::string("m_{#tau#tau}");
      hshape1[i]->SetXTitle(x_title.c_str());
      hshape1[i]->GetXaxis()->SetTitleFont(62);
      hshape1[i]->GetXaxis()->SetLabelFont(62);
      hshape1[i]->GetXaxis()->SetTitleColor(1);
      hshape1[i]->GetXaxis()->SetTitleOffset(1.05);

      // format y-axis
      std::string y_title;
      y_title = std::string("#Events"); 
      hshape1[i]->SetYTitle(y_title.c_str());
      hshape1[i]->GetXaxis()->SetTitleFont(62);
      hshape1[i]->GetYaxis()->SetLabelFont(62);
      //hshape1[i]->GetYaxis()->SetTitleSize(0.05);
      hshape1[i]->GetYaxis()->SetTitleOffset(1.2);
      hshape1[i]->GetYaxis()->SetLabelSize(0.03);
      hshape1[i]->GetXaxis()->SetRangeUser(0,1000);
      hshape1[i]->SetMaximum(maximum);
      hshape1[i]->SetMinimum(minimum);
      hshape1[i]->GetYaxis()->SetRangeUser(minimum, maximum);

      for(int k=0; k<hshape1[i]->GetNbinsX()+1; k++){
	hshape1[i]->SetBinError(k, 0);
      }
    }  
    hshape1[i]->SetLineStyle(1.);
    hshape1[i]->SetLineWidth(2.); 
    hshape1[i]->SetLineColor(kBlue);
    hshape1[i]->SetMarkerStyle(20);
    hshape1[i]->SetMarkerSize(MARKER_SIZE);
    hshape1[i]->SetMarkerColor(kBlue);
    firstPlot=false;  
    if(i>0) hshape1[0]->Add(hshape1[i]);
  }
  hshape1[0]->Scale(9);
  hshape1[0]->SetMaximum(maximum);
  hshape1[0]->SetMinimum(minimum);
  hshape1[0]->GetYaxis()->SetRangeUser(minimum, maximum);
  hshape1[0]->SetTitle("");
  hshape1[0]->Draw("PL");

  firstPlot=true;
  for(unsigned int i=0; i<hshape2.size(); ++i){
    if(firstPlot){
      if(log){ canv1->SetLogy(1); }
      // format x-axis
      std::string x_title;
      //x_title = std::string("#sigma#timesBR/#sigma#timesBR_{SM}");
      x_title = std::string("m_{#tau#tau}");
      hshape2[i]->SetXTitle(x_title.c_str());
      hshape2[i]->GetXaxis()->SetTitleFont(62);
      hshape2[i]->GetXaxis()->SetLabelFont(62);
      hshape2[i]->GetXaxis()->SetTitleColor(1);
      hshape2[i]->GetXaxis()->SetTitleOffset(1.05);

      // format y-axis
      std::string y_title;
      y_title = std::string("#Events"); 
      hshape2[i]->SetYTitle(y_title.c_str());
      hshape2[i]->GetXaxis()->SetTitleFont(62);
      hshape2[i]->GetYaxis()->SetLabelFont(62);
      //hshape2[i]->GetYaxis()->SetTitleSize(0.05);
      hshape2[i]->GetYaxis()->SetTitleOffset(1.2);
      hshape2[i]->GetYaxis()->SetLabelSize(0.03);
      hshape2[i]->GetXaxis()->SetRangeUser(0,1000);
      hshape2[i]->SetMaximum(maximum);
      hshape2[i]->SetMinimum(minimum);
      hshape2[i]->GetYaxis()->SetRangeUser(minimum, maximum);

      for(int k=0; k<hshape2[i]->GetNbinsX()+1; k++){
	hshape2[i]->SetBinError(k, 0);
      }
    }  
    hshape2[i]->SetLineStyle(11.);
    hshape2[i]->SetLineWidth(2.); 
    hshape2[i]->SetLineColor(kRed); 
    hshape2[i]->SetMarkerStyle(21);
    hshape2[i]->SetMarkerSize(MARKER_SIZE);
    hshape2[i]->SetMarkerColor(kRed);
    if(i>0) hshape2[0]->Add(hshape2[i]);
    firstPlot=false;  
  }
  hshape2[0]->Scale(12);
  hshape2[0]->SetMaximum(maximum);
  hshape2[0]->SetMinimum(minimum);
  hshape2[0]->GetYaxis()->SetRangeUser(minimum, maximum);
  hshape2[0]->Draw("PLsame");
  canv1->RedrawAxis();

  firstPlot=true;
  for(unsigned int i=0; i<hshape3.size(); ++i){
    if(firstPlot){
      if(log){ canv1->SetLogy(1); }
      // format x-axis
      std::string x_title;
      //x_title = std::string("#sigma#timesBR/#sigma#timesBR_{SM}");
      x_title = std::string("m_{#tau#tau}");
      hshape3[i]->SetXTitle(x_title.c_str());
      hshape3[i]->GetXaxis()->SetTitleFont(62);
      hshape3[i]->GetXaxis()->SetLabelFont(62);
      hshape3[i]->GetXaxis()->SetTitleColor(1);
      hshape3[i]->GetXaxis()->SetTitleOffset(1.05);

      // format y-axis
      std::string y_title;
      y_title = std::string("#Events"); 
      hshape3[i]->SetYTitle(y_title.c_str());
      hshape3[i]->GetXaxis()->SetTitleFont(62);
      hshape3[i]->GetYaxis()->SetLabelFont(62);
      //hshape3[i]->GetYaxis()->SetTitleSize(0.05);
      hshape3[i]->GetYaxis()->SetTitleOffset(1.2);
      hshape3[i]->GetYaxis()->SetLabelSize(0.03);
      hshape3[i]->GetXaxis()->SetRangeUser(0,1000);
      hshape3[i]->SetMaximum(maximum);
      hshape3[i]->SetMinimum(minimum);
      hshape3[i]->GetYaxis()->SetRangeUser(minimum, maximum);

      for(int k=0; k<hshape3[i]->GetNbinsX()+1; k++){
	hshape3[i]->SetBinError(k, 0);
      }
    }  
    //std::string test = hshape3[i]->GetName();
    //if(test.find("bbH")!=std::string::npos) hshape3[i]->Scale(15);  
    //if(test.find("ggH")!=std::string::npos) hshape3[i]->Scale(15); 
    hshape3[i]->SetLineStyle(1.);
    hshape3[i]->SetLineWidth(2.); 
    hshape3[i]->SetLineColor(kGreen); 
    hshape3[i]->SetMarkerStyle(20);
    hshape3[i]->SetMarkerSize(MARKER_SIZE);
    hshape3[i]->SetMarkerColor(kGreen);
    if(i>0) hshape3[0]->Add(hshape3[i]);
    firstPlot=false;  
  }
  hshape3[0]->Scale(15);
  hshape3[0]->SetMaximum(maximum);
  hshape3[0]->SetMinimum(minimum);
  hshape3[0]->GetYaxis()->SetRangeUser(minimum, maximum);
  hshape3[0]->Draw("PLsame");
  canv1->RedrawAxis();

  firstPlot=true;
  for(unsigned int i=0; i<hshape4.size(); ++i){
    if(firstPlot){
      if(log){ canv1->SetLogy(1); }
      // format x-axis
      std::string x_title;
      //x_title = std::string("#sigma#timesBR/#sigma#timesBR_{SM}");
      x_title = std::string("m_{#tau#tau}");
      hshape4[i]->SetXTitle(x_title.c_str());
      hshape4[i]->GetXaxis()->SetTitleFont(62);
      hshape4[i]->GetXaxis()->SetLabelFont(62);
      hshape4[i]->GetXaxis()->SetTitleColor(1);
      hshape4[i]->GetXaxis()->SetTitleOffset(1.05);

      // format y-axis
      std::string y_title;
      y_title = std::string("#Events"); 
      hshape4[i]->SetYTitle(y_title.c_str());
      hshape4[i]->GetXaxis()->SetTitleFont(62);
      hshape4[i]->GetYaxis()->SetLabelFont(62);
      //hshape4[i]->GetYaxis()->SetTitleSize(0.05);
      hshape4[i]->GetYaxis()->SetTitleOffset(1.2);
      hshape4[i]->GetYaxis()->SetLabelSize(0.03);
      hshape4[i]->GetXaxis()->SetRangeUser(0,1000);
      hshape4[i]->SetMaximum(maximum);
      hshape4[i]->SetMinimum(minimum);
      hshape4[i]->GetYaxis()->SetRangeUser(minimum, maximum);

      for(int k=0; k<hshape4[i]->GetNbinsX()+1; k++){
	hshape4[i]->SetBinError(k, 0);
      }
    }  
    //std::string test = hshape4[i]->GetName();
    //if(test.find("bbH")!=std::string::npos) hshape4[i]->Scale(15);  
    //if(test.find("ggH")!=std::string::npos) hshape4[i]->Scale(15); 
    hshape4[i]->SetLineStyle(11.);
    hshape4[i]->SetLineWidth(2.); 
    hshape4[i]->SetLineColor(kOrange); 
    hshape4[i]->SetMarkerStyle(21);
    hshape4[i]->SetMarkerSize(MARKER_SIZE);
    hshape4[i]->SetMarkerColor(kOrange);
    if(i>0) hshape4[0]->Add(hshape4[i]);
    firstPlot=false;  
  }
  hshape4[0]->Scale(20);
  hshape4[0]->SetMaximum(maximum);
  hshape4[0]->SetMinimum(minimum);
  hshape4[0]->GetYaxis()->SetRangeUser(minimum, maximum);
  hshape4[0]->Draw("PLsame");
  canv1->RedrawAxis();

  firstPlot=true;
  for(unsigned int i=0; i<hshape5.size(); ++i){
    if(firstPlot){
      if(log){ canv1->SetLogy(1); }
      // format x-axis
      std::string x_title;
      //x_title = std::string("#sigma#timesBR/#sigma#timesBR_{SM}");
      x_title = std::string("m_{#tau#tau}");
      hshape5[i]->SetXTitle(x_title.c_str());
      hshape5[i]->GetXaxis()->SetTitleFont(62);
      hshape5[i]->GetXaxis()->SetLabelFont(62);
      hshape5[i]->GetXaxis()->SetTitleColor(1);
      hshape5[i]->GetXaxis()->SetTitleOffset(1.05);

      // format y-axis
      std::string y_title;
      y_title = std::string("#Events"); 
      hshape5[i]->SetYTitle(y_title.c_str());
      hshape5[i]->GetXaxis()->SetTitleFont(62);
      hshape5[i]->GetYaxis()->SetLabelFont(62);
      //hshape5[i]->GetYaxis()->SetTitleSize(0.05);
      hshape5[i]->GetYaxis()->SetTitleOffset(1.2);
      hshape5[i]->GetYaxis()->SetLabelSize(0.03);
      hshape5[i]->GetXaxis()->SetRangeUser(0,1000);
      hshape5[i]->SetMaximum(maximum);
      hshape5[i]->SetMinimum(minimum);
      hshape5[i]->GetYaxis()->SetRangeUser(minimum, maximum);

      for(int k=0; k<hshape5[i]->GetNbinsX()+1; k++){
	hshape5[i]->SetBinError(k, 0);
      }
    }  
    //std::string test = hshape5[i]->GetName();
    //if(test.find("bbH")!=std::string::npos) hshape5[i]->Scale(15);  
    //if(test.find("ggH")!=std::string::npos) hshape5[i]->Scale(15); 
    hshape5[i]->SetLineStyle(11.);
    hshape5[i]->SetLineWidth(3.); 
    hshape5[i]->SetLineColor(kViolet); 
    hshape5[i]->SetMarkerStyle(20);
    hshape5[i]->SetMarkerSize(MARKER_SIZE);
    hshape5[i]->SetMarkerColor(kViolet);
    if(i>0) hshape5[0]->Add(hshape5[i]);
    firstPlot=false;  
  }
  hshape5[0]->Scale(25);
  hshape5[0]->SetMaximum(maximum);
  hshape5[0]->SetMinimum(minimum);
  hshape5[0]->SetLineStyle(11.);
  hshape5[0]->SetLineWidth(3.); 
  hshape5[0]->SetLineColor(kViolet); 
  hshape5[0]->SetMarkerStyle(20);
  hshape5[0]->SetMarkerSize(MARKER_SIZE);
  hshape5[0]->SetMarkerColor(kViolet);
  hshape5[0]->GetYaxis()->SetRangeUser(minimum, maximum);
  hshape5[0]->Draw("PLsame");
  canv1->RedrawAxis();

  firstPlot=true;
  for(unsigned int i=0; i<hshape6.size(); ++i){
    if(firstPlot){
      if(log){ canv1->SetLogy(1); }
      // format x-axis
      std::string x_title;
      //x_title = std::string("#sigma#timesBR/#sigma#timesBR_{SM}");
      x_title = std::string("m_{#tau#tau}");
      hshape6[i]->SetXTitle(x_title.c_str());
      hshape6[i]->GetXaxis()->SetTitleFont(62);
      hshape6[i]->GetXaxis()->SetLabelFont(62);
      hshape6[i]->GetXaxis()->SetTitleColor(1);
      hshape6[i]->GetXaxis()->SetTitleOffset(1.05);

      // format y-axis
      std::string y_title;
      y_title = std::string("#Events"); 
      hshape6[i]->SetYTitle(y_title.c_str());
      hshape6[i]->GetXaxis()->SetTitleFont(62);
      hshape6[i]->GetYaxis()->SetLabelFont(62);
      //hshape6[i]->GetYaxis()->SetTitleSize(0.05);
      hshape6[i]->GetYaxis()->SetTitleOffset(1.2);
      hshape6[i]->GetYaxis()->SetLabelSize(0.03);
      hshape6[i]->GetXaxis()->SetRangeUser(0,1000);
      hshape6[i]->SetMaximum(maximum);
      hshape6[i]->SetMinimum(minimum);
      hshape6[i]->GetYaxis()->SetRangeUser(minimum, maximum);

      for(int k=0; k<hshape6[i]->GetNbinsX()+1; k++){
	hshape6[i]->SetBinError(k, 0);
      }
    }  
    //std::string test = hshape6[i]->GetName();
    //if(test.find("bbH")!=std::string::npos) hshape6[i]->Scale(15);  
    //if(test.find("ggH")!=std::string::npos) hshape6[i]->Scale(15); 
    hshape6[i]->SetLineStyle(11.);
    hshape6[i]->SetLineWidth(3.); 
    hshape6[i]->SetLineColor(kBlack); 
    hshape6[i]->SetMarkerStyle(20);
    hshape6[i]->SetMarkerSize(MARKER_SIZE);
    hshape6[i]->SetMarkerColor(kBlack);
    if(i>0) hshape6[0]->Add(hshape6[i]);
    firstPlot=false;  
  }
  hshape6[0]->Scale(30);
  hshape6[0]->SetMaximum(maximum);
  hshape6[0]->SetMinimum(minimum);
  hshape6[0]->SetLineStyle(11.);
  hshape6[0]->SetLineWidth(3.); 
  hshape6[0]->SetLineColor(kBlack); 
  hshape6[0]->SetMarkerStyle(20);
  hshape6[0]->SetMarkerSize(MARKER_SIZE);
  hshape6[0]->SetMarkerColor(kBlack);
  hshape6[0]->GetYaxis()->SetRangeUser(minimum, maximum);
  hshape6[0]->Draw("PLsame");
  canv1->RedrawAxis();


  TLegend* leg0;
  /// setup the CMS Preliminary
  CMSPrelim(label, "", 0.15, 0.835);
  leg0 = new TLegend(0.45, 0.70, 0.90, 0.90); 
  leg0->SetBorderSize( 0 );
  leg0->SetFillStyle ( 1001 );
  leg0->SetFillColor (kWhite);
  leg0->SetHeader( std::string(category+" Shapes").c_str() );
  std::string shape1cmb;
  for(unsigned int i=0; i<shape1.size(); ++i){
    if (i==0) shape1cmb=shape1[i];
    else shape1cmb=shape1cmb+"+"+shape1[i];
  }
  std::string shape2cmb;
  for(unsigned int i=0; i<shape2.size(); ++i){    
    if (i==0) shape2cmb=shape2[i];
    else shape2cmb=shape2cmb+"+"+shape2[i];
  }
  leg0->AddEntry( hshape1[0] , std::string(shape1cmb+ " - tanb  1.0").c_str(),  "PL" );
  leg0->AddEntry( hshape3[0] , std::string(shape1cmb+ " - tanb  2.0").c_str(),  "PL" );
  leg0->AddEntry( hshape2[0] , std::string(shape2cmb+ " - tanb  6.0").c_str(),  "PL" );
  leg0->AddEntry( hshape4[0] , std::string(shape2cmb+ " - tanb 12.0").c_str(),  "PL" );
  leg0->AddEntry( hshape5[0] , std::string(shape1cmb+ " - tanb 20.0").c_str(),  "PL" );
  leg0->AddEntry( hshape6[0] , std::string(shape2cmb+ " - tanb 30.0").c_str(),  "PL" );
  leg0->Draw("same");
  
  canv1->Print(std::string("CompareShapes-Absolute_"+category).append(".png").c_str());
  canv1->Print(std::string("CompareShapes-Absolute_"+category).append(".pdf").c_str());
  canv1->Print(std::string("CompareShapes-Absolute_"+category).append(".eps").c_str());


  /* not really working atm
  /// do the drawing
  TCanvas* canv2 = new TCanvas("canv2", "Relative Comparison", 600, 600);
  canv2->cd();
  canv2->SetGridx(1);
  canv2->SetGridy(1);

  TH1F* relative = (TH1F*)hshape1[0]->Clone();
  //TH1F* relative = new TH1F();
  //relative->Add(hshape1[0]);
  for(unsigned i=0; i<hshape1[0]->GetXaxis()->GetNbins(); i++){
    double content1=hshape1[0]->GetBinContent(i+1);
    double content2=hshape2[0]->GetBinContent(i+1);
    double content=0;
    if(content1!=0){
      content=(content1-content2)/content1;
    }
    std::cout<<i<<" "<<content1<<" "<<content2<<" "<<content<<std::endl;
    relative->SetBinContent(i+1, content);
  }

  std::string x_title;
  //x_title = std::string("#sigma#timesBR/#sigma#timesBR_{SM}");
  x_title = std::string("m_{#tau#tau}");
  relative->SetXTitle(x_title.c_str());
  relative->GetXaxis()->SetTitleFont(62);
  relative->GetXaxis()->SetLabelFont(62);
  relative->GetXaxis()->SetTitleColor(1);
  relative->GetXaxis()->SetTitleOffset(1.05);

  // format y-axis
  std::string y_title;
  y_title = std::string("arbitary numbers"); 
  relative->SetYTitle(y_title.c_str());
  relative->GetXaxis()->SetTitleFont(62);
  relative->GetYaxis()->SetLabelFont(62);
  //relative->GetYaxis()->SetTitleSize(0.05);
  relative->GetYaxis()->SetTitleOffset(1.05);
  relative->GetYaxis()->SetLabelSize(0.03);
  relative->GetXaxis()->SetRangeUser(0,500);
  relative->SetMaximum(1);
  relative->SetMinimum(-1);
  
  relative->SetLineStyle(11.);
  relative->SetLineWidth(3.); 
  relative->SetLineColor(kBlack); 
  relative->SetMarkerStyle(20);
  relative->SetMarkerSize(MARKER_SIZE);
  relative->SetMarkerColor(kBlack);
  relative->Draw("PL");
  canv2->RedrawAxis();

  TLegend* leg1;
  /// setup the CMS Preliminary
  CMSPrelim(label, "", 0.15, 0.835);
  leg1 = new TLegend(0.45, 0.60, 0.90, 0.90); 
  leg1->SetBorderSize( 0 );
  leg1->SetFillStyle ( 1001 );
  leg1->SetFillColor (kWhite);
  leg1->SetHeader( std::string(category+" Shapes").c_str() );
  leg1->AddEntry( relative , std::string("Relative to shape1").c_str(),  "PL" );
  leg1->Draw("same");


  canv2->Print(std::string("CompareShapes-Relative").append(".png").c_str());
  canv2->Print(std::string("CompareShapes-Relative").append(".pdf").c_str());
  canv2->Print(std::string("CompareShapes-Relative").append(".eps").c_str());
*/
  return;
}


