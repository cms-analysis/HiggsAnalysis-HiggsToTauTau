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

void compareShapesMSSM(std::string path, std::string category, std::string channel, std::string period, const char* shapestr1, const char* shapestr2, double minimum=0., double maximum=20., bool log=false, double mA=140, double tanb=1.0, const char* label="CMS Privat, H#rightarrow#tau#tau, L=19.7 fb^{-1} at 8TeV")
{
  SetStyle();

  std::map<std::string, unsigned int> colors;
  colors["HIG-12-043" ] = kBlack;
  colors["HIG-12-050" ] = kBlack;


  std::cout << " *******************************************************************************************************\n"
	    << " * Usage     : root -l                                                                                  \n"
	    << " *             .x compareShapesMSSM.C+(file, category, shape1, shape2, max, min)                        \n"
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
	    << " *              + mA        double          mass of pseudoscalar A                                      \n"
	    << " *                                                                                                      \n"
	    << " *              + tanb      double          tanb (always give with first decimal place)                 \n"
	    << " *                                                                                                      \n"
	    << " *******************************************************************************************************\n";


  /// prepare input parameters
  std::vector<std::string> shape1;
  string2Vector(cleanupWhitespaces(shapestr1), shape1);
  std::vector<std::string> shape2;
  string2Vector(cleanupWhitespaces(shapestr2), shape2); 
  std::vector<std::string> shape3;
  shape3.push_back("ggH_SM125");
  shape3.push_back("qqH_SM125");
  shape3.push_back("VH_SM125");
  /// test input files 
  char tanb_help[50], mA_help[50];
  sprintf (mA_help,   "%0.0f", mA); 
  sprintf (tanb_help, "%0.1f", tanb); 
  std::vector<std::string> filenames;
  filenames.push_back(std::string(path+"/"+"htt_"+channel+".inputs-mssm-"+period+"-0.root_"+mA_help+"_"+tanb_help));
  filenames.push_back(std::string(path+"/"+"htt_"+channel+".inputs-mssm-"+period+"-0.root"));
  filenames.push_back(std::string(path+"/"+"htt_"+channel+".inputs-mssm-"+period+"-0.root"));
  
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
  
  std::vector<TH1F*> hshape1;
  std::vector<TH1F*> hshape2;
  std::vector<TH1F*> hshape3;
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
    //if(filenames[1].find("_em")!=std::string::npos) hshape2.push_back(get<TH1F>(inputFile1, std::string("emu_"+category+"/").append(shape2[i]).c_str()));
    //if(filenames[1].find("_et")!=std::string::npos) hshape2.push_back(get<TH1F>(inputFile1, std::string("eleTau_"+category+"/").append(shape2[i]).c_str()));
    //if(filenames[1].find("_mm")!=std::string::npos) hshape2.push_back(get<TH1F>(inputFile1, std::string("mumu_"+category+"/").append(shape2[i]).c_str()));
    if(filenames[1].find("_mt")!=std::string::npos) hshape3.push_back(get<TH1F>(inputFile1, std::string("muTau_"+category+"/").append(shape3[i]).c_str()));
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
    }  
    hshape1[i]->SetLineStyle(1.);
    hshape1[i]->SetLineWidth(3.); 
    hshape1[i]->SetLineColor(kBlue);
    hshape1[i]->SetMarkerStyle(20);
    hshape1[i]->SetMarkerSize(MARKER_SIZE);
    hshape1[i]->SetMarkerColor(kBlue);
    for(int k=0; k<hshape1[i]->GetNbinsX()+1; k++){
	hshape1[i]->SetBinError(k, 0);
    }
    if(i>0) hshape1[0]->Add(hshape1[i]);
    firstPlot=false;  
  }
  hshape1[0]->Scale(tanb); 
  hshape1[0]->SetMaximum(maximum);
  hshape1[0]->SetMinimum(minimum);
  hshape1[0]->GetYaxis()->SetRangeUser(minimum, maximum);
  hshape1[0]->SetTitle("");
  hshape1[0]->Draw("H");

  firstPlot=true;
  for(unsigned int i=0; i<hshape2.size(); ++i){
    if(firstPlot){
      if(log){ canv1->SetLogy(1); }
      // format x-axis
      std::string x_title;
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
    }  
    hshape2[i]->SetLineStyle(1.);
    hshape2[i]->SetLineWidth(3.); 
    hshape2[i]->SetLineColor(kRed); 
    hshape2[i]->SetMarkerStyle(20);
    hshape2[i]->SetMarkerSize(MARKER_SIZE);
    hshape2[i]->SetMarkerColor(kRed);   
    for(int k=0; k<hshape2[i]->GetNbinsX()+1; k++){
      hshape2[i]->SetBinError(k, 0);
    }
    if(i>0) hshape2[0]->Add(hshape2[i]);
    firstPlot=false;  
  }
  // hshape2[0]->Scale(20);
  hshape2[0]->SetMaximum(maximum);
  hshape2[0]->SetMinimum(minimum);
  hshape2[0]->GetYaxis()->SetRangeUser(minimum, maximum);
  hshape2[0]->SetTitle("");
  hshape2[0]->Draw("Hsame");
  canv1->RedrawAxis();

  firstPlot=true;
  for(unsigned int i=0; i<hshape3.size(); ++i){
    if(firstPlot){
      if(log){ canv1->SetLogy(1); }
      // format x-axis
      std::string x_title;
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
    }  
    hshape3[i]->SetLineStyle(1.);
    hshape3[i]->SetLineWidth(3.); 
    hshape3[i]->SetLineColor(kGreen); 
    hshape3[i]->SetMarkerStyle(20);
    hshape3[i]->SetMarkerSize(MARKER_SIZE);
    hshape3[i]->SetMarkerColor(kGreen);
    for(int k=0; k<hshape3[i]->GetNbinsX()+1; k++){
      hshape3[i]->SetBinError(k, 0);
    }
    if(i>0) hshape3[0]->Add(hshape3[i]);
    firstPlot=false;  
  }
  // hshape3[0]->Scale(20);
  hshape3[0]->SetMaximum(maximum);
  hshape3[0]->SetMinimum(minimum);
  hshape3[0]->GetYaxis()->SetRangeUser(minimum, maximum);
  hshape3[0]->SetTitle("");
  hshape3[0]->Draw("Hsame");
  canv1->RedrawAxis();


  TLegend* leg0;
  /// setup the CMS Preliminary
  CMSPrelim(label, "", 0.15, 0.835);
  leg0 = new TLegend(0.50, 0.67, 0.95, 0.90); 
  leg0->SetBorderSize( 0 );
  leg0->SetFillStyle ( 1001 );
  leg0->SetFillColor (kWhite);
  leg0->SetHeader( std::string(channel+"-"+category+" Shapes").c_str() );
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
  leg0->AddEntry( hshape1[0], std::string(shape1cmb+ " - tanb="+tanb_help).c_str(),  "L" ); 
  //leg0->AddEntry((TObject*)0, "tanb=0.8 mA=200GeV", "");
  leg0->AddEntry( hshape2[0], std::string(shape2cmb).c_str(),  "L" );
  //leg0->AddEntry((TObject*)0, "background"  "" );
  leg0->AddEntry( hshape3[0], "ggH+VH+qqH - SM Higgs",  "L" );
  //leg0->AddEntry((TObject*)0, "SM Higgs",  "" );
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


