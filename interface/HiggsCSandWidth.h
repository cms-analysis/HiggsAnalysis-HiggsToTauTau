#ifndef HIGGSCSANDWIDTH_H
#define HIGGSCSANDWIDTH_H

#define PI 3.14159

#define  ID_ggToH  1
#define  ID_VBF    2
#define  ID_WH     3
#define  ID_ZH     4
#define  ID_ttH    5
#define  ID_Total  0 


#include <iostream>
#include <cstdlib>
#include <cmath>
#include <fstream>
#include <string>

#include "TROOT.h"
#include "TF1.h"
#include "TGraph.h"
#include "TCanvas.h"
#include "TSpline.h"


/**********************************************************/
/*            Class for Higgs Width and CS                */
/*                                                        */
/*  All numbers for CS and width are taken from official  */
/*  numbers on Higgs CS Twiki (Spring 2011)               */
/*                                                        */
/*  Cross Sections are given in pb                        */
/*  Widths are given in GeV                               */
/*                                                        */
/*  These numbers are taken into memory and a simple      */
/*  linear interpolation is done.                         */
/*                                                        */
/*  For any invalid process or mH out of range, -1 will   */
/*  be returned.                                          */
/*                                                        */
/*    Written by:                                         */
/*         Matt Snowball                                  */
/*         University of Florida                          */
/*         snowball@phys.ufl.edu                          */
/*                                                        */
/*       Last Update: April 5, 2012                       */
/*                                                        */
/**********************************************************/



class HiggsCSandWidth
{

 public:

  HiggsCSandWidth();
  ~HiggsCSandWidth();

  double HiggsCS(int ID, double mH, double sqrts, bool spline);
  double HiggsCSErrPlus(int ID, double mH, double sqrts);
  double HiggsCSErrMinus(int ID, double mH, double sqrts);
  double HiggsCSscaleErrPlus(int ID, double mH, double sqrts);
  double HiggsCSscaleErrMinus(int ID, double mH, double sqrts);
  double HiggsCSpdfErrPlus(int ID, double mH, double sqrts);
  double HiggsCSpdfErrMinus(int ID, double mH, double sqrts);
  double HiggsWidth(int ID,double mH, bool spline);
  double HiggsBR(int ID,double mH, bool spline);

 private:

  double scratchMass;
  double mass_BR[217];
  double mass_XS[197];
  double BR[26][217];
  double CS[6][197];
  double CSerrPlus[6][197];
  double CSerrMinus[6][197];
  double CSscaleErrPlus[6][197];
  double CSscaleErrMinus[6][197];
  double CSpdfErrPlus[6][197];
  double CSpdfErrMinus[6][197];

  int N_BR;
  int N_CS;
  std::string FileLoc;


};


using namespace std;

HiggsCSandWidth::HiggsCSandWidth()
{

  N_BR = 217;
  N_CS = 197;

  ifstream file;
 
  // Read Widths into memory
  FileLoc = std::string(getenv("CMSSW_BASE"))+std::string("/src/HiggsAnalysis/HiggsToTauTau/data/SM4/HiggsBR_7TeV_Official.txt"); //directory of input file
  const char* BranchRatioFileLoc = FileLoc.c_str(); 
  file.open(BranchRatioFileLoc);
  for(int k = 0; k < N_BR; k++){

    file >> mass_BR[k] >> BR[0][k] >> BR[1][k] >> BR[2][k] >> BR[3][k] >> BR[4][k] >> BR[5][k] >> BR[6][k] >> BR[7][k] >> BR[8][k] >> BR[9][k]
	 >> BR[10][k] >> BR[11][k] >> BR[12][k] >> BR[13][k] >> BR[14][k] >> BR[15][k] >> BR[16][k] >> BR[17][k] >> BR[18][k] >> BR[19][k] >> BR[20][k]
	 >> BR[21][k] >> BR[22][k] >> BR[23][k] >> BR[24][k] >> BR[25][k];


  }
  file.close();

  // Read CS into memory                                                                                                                                                  
  file.open((std::string(getenv("CMSSW_BASE"))+std::string("/src/HiggsAnalysis/HiggsToTauTau/data/SM4/HiggsCS_Official.txt")).c_str());//directory of input file
  for(int k = 0; k < N_CS; k++){
    file >> mass_XS[k] >> CS[ID_ggToH][k] >> CS[ID_VBF][k] >> CS[ID_WH][k] >> CS[ID_ZH][k] >> CS[ID_ttH][k] >> CS[ID_Total][k];
  }
  file.close();

  file.open((std::string(getenv("CMSSW_BASE"))+std::string("/src/HiggsAnalysis/HiggsToTauTau/data/SM4/HiggsCS_ErrorPlus_Official.txt")).c_str());//directory of input file 
  for(int k = 0; k < N_CS; k++){
    file >> scratchMass >> CSerrPlus[ID_ggToH][k] >> CSerrPlus[ID_VBF][k] >> CSerrPlus[ID_WH][k] >> CSerrPlus[ID_ZH][k] >> CSerrPlus[ID_ttH][k];
  }
  file.close();

  file.open((std::string(getenv("CMSSW_BASE"))+std::string("/src/HiggsAnalysis/HiggsToTauTau/data/SM4/HiggsCS_ErrorMinus_Official.txt")).c_str());//directory of input file 
  for(int k = 0; k < N_CS; k++){
    file >> scratchMass >> CSerrMinus[ID_ggToH][k] >> CSerrMinus[ID_VBF][k] >> CSerrMinus[ID_WH][k] >> CSerrMinus[ID_ZH][k] >> CSerrMinus[ID_ttH][k];
  }
  file.close();

  file.open((std::string(getenv("CMSSW_BASE"))+std::string("/src/HiggsAnalysis/HiggsToTauTau/data/SM4/HiggsCS_ScaleErrorPlus_Official.txt")).c_str());//directory of input file
  for(int k = 0; k < N_CS; k++){
    file >> scratchMass >> CSscaleErrPlus[ID_ggToH][k] >> CSscaleErrPlus[ID_VBF][k] >> CSscaleErrPlus[ID_WH][k] >> CSscaleErrPlus[ID_ZH][k] >> CSscaleErrPlus[ID_ttH][k];
  }
  file.close();

  file.open((std::string(getenv("CMSSW_BASE"))+std::string("/src/HiggsAnalysis/HiggsToTauTau/data/SM4/HiggsCS_ScaleErrorMinus_Official.txt")).c_str());//directory of input file
  for(int k = 0; k < N_CS; k++){
    file >> scratchMass >> CSscaleErrMinus[ID_ggToH][k] >> CSscaleErrMinus[ID_VBF][k] >> CSscaleErrMinus[ID_WH][k] >> CSscaleErrMinus[ID_ZH][k] >> CSscaleErrMinus[ID_ttH][k];
  }
  file.close();

  file.open((std::string(getenv("CMSSW_BASE"))+std::string("/src/HiggsAnalysis/HiggsToTauTau/data/SM4/HiggsCS_PdfErrorPlus_Official.txt")).c_str());//directory of input file                  
  for(int k = 0; k < N_CS; k++){
    file >> scratchMass >> CSpdfErrPlus[ID_ggToH][k] >> CSpdfErrPlus[ID_VBF][k] >> CSpdfErrPlus[ID_WH][k] >> CSpdfErrPlus[ID_ZH][k] >> CSpdfErrPlus[ID_ttH][k];
  }
  file.close();

  file.open((std::string(getenv("CMSSW_BASE"))+std::string("/src/HiggsAnalysis/HiggsToTauTau/data/SM4/HiggsCS_PdfErrorMinus_Official.txt")).c_str());//directory of input file
  for(int k = 0; k < N_CS; k++){
    file >> scratchMass >> CSpdfErrMinus[ID_ggToH][k] >> CSpdfErrMinus[ID_VBF][k] >> CSpdfErrMinus[ID_WH][k] >> CSpdfErrMinus[ID_ZH][k] >> CSpdfErrMinus[ID_ttH][k];
  }
  file.close();

}


HiggsCSandWidth::~HiggsCSandWidth()
{
  //destructor

}


//Higgs CS takes process ID, higgs mass mH, and COM energy sqrts in TeV (numbers are for 7 TeV only in this version)
double HiggsCSandWidth::HiggsCS(int ID, double mH, double sqrts, bool spline){

  /**********IDs*************/ 
  /*     ggToH = 1          */
  /*       VBF = 2          */ 
  /*        WH = 3          */ 
  /*        ZH = 4          */
  /*       ttH = 5          */
  /*     Total = 0          */
  /**************************/
 
  int i = 0;
  double closestMass = 0;
  double reqCS = 0;
  double tmpLow = 0, tmpHigh = 0;
  double deltaX = 0, deltaY = 0;
  double slope = 0;
  double step = 0;


  // If ID is unavailable return -1                                                                                                
  if(ID > ID_ttH || ID < ID_Total){return -1;}
  // If Ecm is not 7 TeV return -1
  if(sqrts != 7){return -1;}
  //Don't interpolate btw 0 and numbers for mH300
  if(ID > ID_VBF && mH > 300){return 0;}


  // If mH is out of range return -1                                           
  // else find what array number to read         
  if( mH < 90 || mH > 1000){return -1;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 90)/step); closestMass = (int)(step*i + 90);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(4 + (mH - 110)/step); closestMass = (step*(i-4) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(64 + (mH - 140)/step); closestMass = (int)(step*(i-64) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(84 + (mH - 160)/step); closestMass = (int)(step*(i-84) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(149 + (mH - 290)/step); closestMass = (int)(step*(i-149) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(161 + (mH-350)/step); closestMass = (int)(step*(i-161) + 350);}
    if(mH > 400){step = 20; i = (int)(166 + (mH-400)/step); closestMass = (int)(step*(i-166) + 400);}

      tmpLow = CS[ID][i];
      tmpHigh = CS[ID][i+1];

      deltaX = mH - closestMass;

      deltaY = tmpHigh - tmpLow;
      slope = deltaY/step;

      if(!spline)
	{
	  if(deltaX == 0){ reqCS = tmpLow;}
	  else{ reqCS = slope*deltaX + tmpLow;}
	}
      else if(spline)
	{
	  if(i < 1){i = 1;}
	  if(i+2 >= N_CS){i = N_CS - 3;}
	  static const int index = 4;
	  double xmh[index], sig[index];
	  xmh[0]=mass_XS[i-1];xmh[1]=mass_XS[i];xmh[2]=mass_XS[i+1];xmh[3]=mass_XS[i+2];
	  sig[0]=CS[ID][i-1]; sig[1]=CS[ID][i]; sig[2]=CS[ID][i+1]; sig[3]=CS[ID][i+2];
	  
	  TGraph *graph = new TGraph(index, xmh, sig);
	  TSpline3 *gs = new TSpline3("gs",graph);
	  gs->Draw();
	  reqCS = gs->Eval(mH);
	  delete gs;
	  delete graph;
	}
      
  }
  
  return reqCS;
  
}


//Higgs CS takes process ID, higgs mass mH, and COM energy sqrts in TeV (numbers are for 7 TeV only in this version)                   
double HiggsCSandWidth::HiggsCSErrPlus(int ID, double mH, double sqrts){

  /**********IDs*************/
  /*     ggToH = 1          */
  /*       VBF = 2          */
  /*        WH = 3          */
  /*        ZH = 4          */
  /*       ttH = 5          */
  /**************************/

  int i = 0;
  double closestMass = 0;
  double reqCSerr = 0;
  double tmpLow = 0, tmpHigh = 0;
  double deltaX = 0, deltaY = 0;
  double slope = 0;
  double step = 0;


  // If ID is unavailable return -1                                                                                    
  if(ID > ID_ttH || ID < ID_Total){return -1;}
  if(ID == ID_Total){return 0;}
  // If Ecm is not 7 TeV return -1                                                                                                
  if(sqrts != 7){return -1;}
  //Don't interpolate btw 0 and numbers for mH300                        
  if(ID > ID_VBF && mH > 300){return 0;}

  // If mH is out of range return -1                                                                        
  // else find what array number to read                                          
  if( mH < 90 || mH > 1000){return -1;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 90)/step); closestMass = (int)(step*i + 90);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(4 + (mH - 110)/step); closestMass = (step*(i-4) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(64 + (mH - 140)/step); closestMass = (int)(step*(i-64) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(84 + (mH - 160)/step); closestMass = (int)(step*(i-84) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(149 + (mH - 290)/step); closestMass = (int)(step*(i-149) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(161 + (mH-350)/step); closestMass = (int)(step*(i-161) + 350);}
    if(mH > 400){step = 20; i = (int)(166 + (mH-400)/step); closestMass = (int)(step*(i-166) + 400);}



    tmpLow = CSerrPlus[ID][i];
    tmpHigh = CSerrPlus[ID][i+1];

    deltaX = mH - closestMass;

    deltaY = tmpHigh - tmpLow;
    slope = deltaY/step;

    // For partial widths                                                                                                      
    if(deltaX == 0){ reqCSerr = tmpLow;}
    else{ reqCSerr = slope*deltaX + tmpLow;}
    reqCSerr *= .01; //Account for percentage
  }

  return reqCSerr;

}


//Higgs CS takes process ID, higgs mass mH, and COM energy sqrts in TeV (numbers are for 7 TeV only in this version)      
double HiggsCSandWidth::HiggsCSErrMinus(int ID, double mH, double sqrts){

  /**********IDs*************/
  /*     ggToH = 1          */
  /*       VBF = 2          */
  /*        WH = 3          */
  /*        ZH = 4          */
  /*       ttH = 5          */
  /**************************/

  int i = 0;
  double closestMass = 0;
  double reqCSerr = 0;
  double tmpLow = 0, tmpHigh = 0;
  double deltaX = 0, deltaY = 0;
  double slope = 0;
  double step = 0;


  // If ID is unavailable return -1                                                                                       
  if(ID > ID_ttH || ID < ID_Total){return -1;}
  if(ID == ID_Total){return 0;}
  // If Ecm is not 7 TeV return -1                                                                                           
  if(sqrts != 7){return -1;}
  //Don't interpolate btw 0 and numbers for mH300                                                        
  if(ID > ID_VBF && mH > 300){return 0;}


  // If mH is out of range return -1                                                                           
  // else find what array number to read                                                                 
  if( mH < 90 || mH > 1000){return -1;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 90)/step); closestMass = (int)(step*i + 90);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(4 + (mH - 110)/step); closestMass = (step*(i-4) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(64 + (mH - 140)/step); closestMass = (int)(step*(i-64) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(84 + (mH - 160)/step); closestMass = (int)(step*(i-84) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(149 + (mH - 290)/step); closestMass = (int)(step*(i-149) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(161 + (mH-350)/step); closestMass = (int)(step*(i-161) + 350);}
    if(mH > 400){step = 20; i = (int)(166 + (mH-400)/step); closestMass = (int)(step*(i-166) + 400);}



    tmpLow = CSerrMinus[ID][i];
    tmpHigh = CSerrMinus[ID][i+1];

    deltaX = mH - closestMass;

    deltaY = tmpHigh - tmpLow;
    slope = deltaY/step;

    // For partial widths                                               
    if(deltaX == 0){ reqCSerr = tmpLow;}
    else{ reqCSerr = slope*deltaX + tmpLow;}
    reqCSerr *= .01; //Account for percentage                                                                                                   
  }

  return reqCSerr;

}

//Higgs CS takes process ID, higgs mass mH, and COM energy sqrts in TeV (numbers are for 7 TeV only in this version)          
double HiggsCSandWidth::HiggsCSscaleErrPlus(int ID, double mH, double sqrts){

  /**********IDs*************/
  /*     ggToH = 1          */
  /*       VBF = 2          */
  /*        WH = 3          */
  /*        ZH = 4          */
  /*       ttH = 5          */
  /**************************/

  int i = 0;
  double closestMass = 0;
  double reqCSerr = 0;
  double tmpLow = 0, tmpHigh = 0;
  double deltaX = 0, deltaY = 0;
  double slope = 0;
  double step = 0;


  // If ID is unavailable return -1                                                         
  if(ID > ID_ttH || ID < ID_Total){return -1;}
  if(ID == ID_Total){return 0;}
  // If Ecm is not 7 TeV return -1                                                
  if(sqrts != 7){return -1;}
  //Don't interpolate btw 0 and numbers for mH300                                           
  if(ID > ID_VBF && mH > 300){return 0;}

  // If mH is out of range return -1                                                         
  // else find what array number to read                                                      
  if( mH < 90 || mH > 1000){return -1;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 90)/step); closestMass = (int)(step*i + 90);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(4 + (mH - 110)/step); closestMass = (step*(i-4) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(64 + (mH - 140)/step); closestMass = (int)(step*(i-64) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(84 + (mH - 160)/step); closestMass = (int)(step*(i-84) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(149 + (mH - 290)/step); closestMass = (int)(step*(i-149) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(161 + (mH-350)/step); closestMass = (int)(step*(i-161) + 350);}
    if(mH > 400){step = 20; i = (int)(166 + (mH-400)/step); closestMass = (int)(step*(i-166) + 400);}



    tmpLow = CSscaleErrPlus[ID][i];
    tmpHigh = CSscaleErrPlus[ID][i+1];

    deltaX = mH - closestMass;

    deltaY = tmpHigh - tmpLow;
    slope = deltaY/step;

    // For partial widths                                              
    if(deltaX == 0){ reqCSerr = tmpLow;}
    else{ reqCSerr = slope*deltaX + tmpLow;}
    reqCSerr *= .01; //Account for percentage                 
  }

  return reqCSerr;

}

//Higgs CS takes process ID, higgs mass mH, and COM energy sqrts in TeV (numbers are for 7 TeV only in this version)    
double HiggsCSandWidth::HiggsCSscaleErrMinus(int ID, double mH, double sqrts){

  /**********IDs*************/
  /*     ggToH = 1          */
  /*       VBF = 2          */
  /*        WH = 3          */
  /*        ZH = 4          */
  /*       ttH = 5          */
  /**************************/

  int i = 0;
  double closestMass = 0;
  double reqCSerr = 0;
  double tmpLow = 0, tmpHigh = 0;
  double deltaX = 0, deltaY = 0;
  double slope = 0;
  double step = 0;


  // If ID is unavailable return -1                     
  if(ID > ID_ttH || ID < ID_Total){return -1;}
  if(ID == ID_Total){return 0;}
  // If Ecm is not 7 TeV return -1                                                               
  if(sqrts != 7){return -1;}
  //Don't interpolate btw 0 and numbers for mH300                                   
  if(ID > ID_VBF && mH > 300){return 0;}


  // If mH is out of range return -1                        
  // else find what array number to read                              
  if( mH < 90 || mH > 1000){return -1;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 90)/step); closestMass = (int)(step*i + 90);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(4 + (mH - 110)/step); closestMass = (step*(i-4) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(64 + (mH - 140)/step); closestMass = (int)(step*(i-64) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(84 + (mH - 160)/step); closestMass = (int)(step*(i-84) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(149 + (mH - 290)/step); closestMass = (int)(step*(i-149) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(161 + (mH-350)/step); closestMass = (int)(step*(i-161) + 350);}
    if(mH > 400){step = 20; i = (int)(166 + (mH-400)/step); closestMass = (int)(step*(i-166) + 400);}



    tmpLow = CSscaleErrMinus[ID][i];
    tmpHigh = CSscaleErrMinus[ID][i+1];

    deltaX = mH - closestMass;

    deltaY = tmpHigh - tmpLow;
    slope = deltaY/step;

    // For partial widths                                             
    if(deltaX == 0){ reqCSerr = tmpLow;}
    else{ reqCSerr = slope*deltaX + tmpLow;}
    reqCSerr *= .01; //Account for percentage                                                                                          
  }

  return reqCSerr;

}


//Higgs CS takes process ID, higgs mass mH, and COM energy sqrts in TeV (numbers are for 7 TeV only in this version)                  
double HiggsCSandWidth::HiggsCSpdfErrPlus(int ID, double mH, double sqrts){

  /**********IDs*************/
  /*     ggToH = 1          */
  /*       VBF = 2          */
  /*        WH = 3          */
  /*        ZH = 4          */
  /*       ttH = 5          */
  /**************************/

  int i = 0;
  double closestMass = 0;
  double reqCSerr = 0;
  double tmpLow = 0, tmpHigh = 0;
  double deltaX = 0, deltaY = 0;
  double slope = 0;
  double step = 0;


  // If ID is unavailable return -1                                                                           
  if(ID > ID_ttH || ID < ID_Total){return -1;}
  if(ID == ID_Total){return 0;}
  // If Ecm is not 7 TeV return -1                                                                                         
  if(sqrts != 7){return -1;}
  //Don't interpolate btw 0 and numbers for mH300                                                  
  if(ID > ID_VBF && mH > 300){return 0;}


  // If mH is out of range return -1                                                                                  
  // else find what array number to read                                                              
  if( mH < 90 || mH > 1000){return -1;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 90)/step); closestMass = (int)(step*i + 90);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(4 + (mH - 110)/step); closestMass = (step*(i-4) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(64 + (mH - 140)/step); closestMass = (int)(step*(i-64) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(84 + (mH - 160)/step); closestMass = (int)(step*(i-84) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(149 + (mH - 290)/step); closestMass = (int)(step*(i-149) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(161 + (mH-350)/step); closestMass = (int)(step*(i-161) + 350);}
    if(mH > 400){step = 20; i = (int)(166 + (mH-400)/step); closestMass = (int)(step*(i-166) + 400);}



    tmpLow = CSpdfErrPlus[ID][i];
    tmpHigh = CSpdfErrPlus[ID][i+1];

    deltaX = mH - closestMass;

    deltaY = tmpHigh - tmpLow;
    slope = deltaY/step;

    // For partial widths                    
    if(deltaX == 0){ reqCSerr = tmpLow;}
    else{ reqCSerr = slope*deltaX + tmpLow;}
    reqCSerr *= .01; //Account for percentage                                                                                             
  }

  return reqCSerr;

}


//Higgs CS takes process ID, higgs mass mH, and COM energy sqrts in TeV (numbers are for 7 TeV only in this version)         
double HiggsCSandWidth::HiggsCSpdfErrMinus(int ID, double mH, double sqrts){

  /**********IDs*************/
  /*     ggToH = 1          */
  /*       VBF = 2          */
  /*        WH = 3          */
  /*        ZH = 4          */
  /*       ttH = 5          */
  /**************************/

  int i = 0;
  double closestMass = 0;
  double reqCSerr = 0;
  double tmpLow = 0, tmpHigh = 0;
  double deltaX = 0, deltaY = 0;
  double slope = 0;
  double step = 0;


  // If ID is unavailable return -1                           
  if(ID > ID_ttH || ID < ID_Total){return -1;}
  if(ID == ID_Total){return 0;}
  // If Ecm is not 7 TeV return -1                                                                 
  if(sqrts != 7){return -1;}
  //Don't interpolate btw 0 and numbers for mH300             
  if(ID > ID_VBF && mH > 300){return 0;}


  // If mH is out of range return -1                                                              
  // else find what array number to read                            
  if( mH < 90 || mH > 1000){return -1;}
  else{

    if(mH <= 110 ){step = 5; i = (int)((mH - 90)/step); closestMass = (int)(step*i + 90);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(4 + (mH - 110)/step); closestMass = (step*(i-4) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(64 + (mH - 140)/step); closestMass = (int)(step*(i-64) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(84 + (mH - 160)/step); closestMass = (int)(step*(i-84) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(149 + (mH - 290)/step); closestMass = (int)(step*(i-149) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(161 + (mH-350)/step); closestMass = (int)(step*(i-161) + 350);}
    if(mH > 400){step = 20; i = (int)(166 + (mH-400)/step); closestMass = (int)(step*(i-166) + 400);}



    tmpLow = CSpdfErrMinus[ID][i];
    tmpHigh = CSpdfErrMinus[ID][i+1];

    deltaX = mH - closestMass;


    deltaY = tmpHigh - tmpLow;
    slope = deltaY/step;

    // For partial widths                                                          
    if(deltaX == 0){ reqCSerr = tmpLow;}
    else{ reqCSerr = slope*deltaX + tmpLow;}
    reqCSerr *= .01; //Account for percentage                                                                                    
  }

  return reqCSerr;

}



// HiggsWidth takes process ID and higgs mass mH
double HiggsCSandWidth::HiggsWidth(int ID, double mH, bool spline){


  /***********************IDs************************/
  /*                       Total = 0                */
  /*                       H->bb = 1                */
  /*                   H->tautau = 2                */
  /*                     H->mumu = 3                */
  /*                       H->ss = 4                */
  /*                       H->cc = 5                */
  /*                       H->tt = 6                */
  /*                       H->gg = 7                */
  /*                   H->gamgam = 8                */
  /*                     H->gamZ = 9                */
  /*                       H->WW = 10               */
  /*                       H->ZZ = 11               */
  /*                       H->4e = 12               */
  /*                    H->2e2mu = 13               */
  /*              H->4lep (e,mu) = 14               */
  /*          H->4lep (e,mu,tau) = 15               */
  /*                H->e+nu e-nu = 16               */
  /*               H->e+nu mu-nu = 17               */
  /*    H->2l2nu(l=e,mu)(nu=any) = 18               */
  /* H->2l2nu(l=e,mu,tau)(nu=any) = 19              */  
  /*    H->2l2q (l=e,mu)(q=udcsb) = 20              */
  /* H->2l2q(l=e,mu,tau)(q=udcsb) = 21              */
  /* H->l+nu qq(*) (l=e,mu)(q=udcsb) = 22           */
  /*  H->2nu2q (nu=any)(q=udcsb) = 23               */
  /*            H->4q (q=udcsb) = 24                */
  /*      H->4f (f=any fermion) = 25                */
  /**************************************************/



  double TotalWidth = 0;
  double PartialWidth = 0;
  double Width = 0;
  int i = 0;
  double closestMass = 0;
  double tmpLow1, tmpHigh1, deltaX, deltaY1, slope1;
  double deltaY2, tmpLow2, tmpHigh2, slope2, step;


  // If ID is unavailable return -1                                           
  if(ID > 25 || ID < 0){return -1;}


  // If mH is out of range return -1                                            
  // else find what array number to read                                        
  if( mH < 90 || mH > 1000){return -1;}
  else{

    //Find index and closest higgs mass for which we have numbers
    if(mH <=110 ){step = 5; i = (int)((mH - 90)/step); closestMass = (int)(step*i + 90);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(4 + (mH-110)/step); closestMass = (step*(i-4) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(64 + (mH-140)/step); closestMass = (int)(step*(i-64) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(84 + (mH-160)/step); closestMass = (int)(step*(i-84) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(149 + (mH-290)/step); closestMass = (int)(step*(i-149) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(161 + (mH-350)/step); closestMass = (int)(step*(i-161) + 350);}
    if(mH > 400 && mH <= 600 ){step = 20; i = (int)(166 + (mH-400)/step); closestMass = (int)(step*(i-166) + 400);}
    if(mH > 600){step = 10; i = (int)(176 + (mH-600)/step); closestMass = (int)(step*(i-176) + 600);}


      tmpLow1 = BR[ID][i]*BR[0][i];                                                                                                                        
      tmpHigh1 = BR[ID][i+1]*BR[0][i+1];                                                                                                                   


      tmpLow2 = BR[0][i];
      tmpHigh2 = BR[0][i+1];
      deltaX = mH - closestMass;

      deltaY1 = tmpHigh1 - tmpLow1;
      slope1 = deltaY1/step;


      deltaY2 = tmpHigh2 - tmpLow2;
      slope2 = deltaY2/step;

      if(!spline)
	{
	  // For partial widths                                                                                                                 
	  if(deltaX == 0){ PartialWidth = tmpLow1;
	    TotalWidth = tmpLow2;}
	  else{ PartialWidth = slope1*deltaX + tmpLow1;
	    TotalWidth = slope2*deltaX + tmpLow2;}
	  // For total width  
	  if( ID == 0 ){ Width = TotalWidth; }
	  else{ Width = PartialWidth;}
	}
      else if(spline)
	{
	  if( ID == 0 )
	    {
	      if(i < 1){i = 1;}
	      if(i+2 >= N_BR){i = N_BR - 3;}
	      static const int indexW = 4;
	      double xmhW[indexW], sigW[indexW];
	      xmhW[0]=mass_BR[i-1];xmhW[1]=mass_BR[i];xmhW[2]=mass_BR[i+1];xmhW[3]=mass_BR[i+2];
	      sigW[0]=BR[ID][i-1]; sigW[1]=BR[ID][i]; sigW[2]=BR[ID][i+1]; sigW[3]=BR[ID][i+2];
	      
	      TGraph *graphW = new TGraph(indexW, xmhW, sigW);
	      TSpline3 *gsW = new TSpline3("gsW",graphW);
	      gsW->Draw();
	      Width = gsW->Eval(mH);
	      delete gsW;
	      delete graphW;
	    }
	  else{
	      if(i < 1){i = 1;}
	      if(i+2 >= N_BR){i = N_BR - 3;}

	      static const int indexW = 4;
	      double xmhW[indexW], sigW[indexW];
	      xmhW[0]=mass_BR[i-1];xmhW[1]=mass_BR[i];xmhW[2]=mass_BR[i+1];xmhW[3]=mass_BR[i+2];
	      sigW[0]=BR[0][i-1]; sigW[1]=BR[0][i]; sigW[2]=BR[0][i+1]; sigW[3]=BR[0][i+2];
	      
	      TGraph *graphW = new TGraph(indexW, xmhW, sigW);
	      TSpline3 *gsW = new TSpline3("gsW",graphW);
	      gsW->Draw();
	      PartialWidth = gsW->Eval(mH);
	      delete gsW;
	      delete graphW;
   
	      static const int indexPW = 4;
	      double xmhPW[indexPW], sigPW[indexPW];
	      xmhPW[0]=mass_BR[i-1];xmhPW[1]=mass_BR[i];xmhPW[2]=mass_BR[i+1];xmhPW[3]=mass_BR[i+2];
	      sigPW[0]=BR[ID][i-1]; sigPW[1]=BR[ID][i]; sigPW[2]=BR[ID][i+1]; sigPW[3]=BR[ID][i+2];
	      
	      TGraph *graphPW = new TGraph(indexPW, xmhPW, sigPW);
	      TSpline3 *gsPW = new TSpline3("gsPW",graphPW);
	      gsPW->Draw();
	      PartialWidth *= gsPW->Eval(mH);
	      delete gsPW;
	      delete graphPW;

	      Width = PartialWidth;
	  
	  }
		  
	}
            
  }
  
  return Width;
  
} 


// HiggsWidth takes process ID and higgs mass mH
double HiggsCSandWidth::HiggsBR(int ID, double mH, bool spline){


  /***********************IDs************************/
  /*                       Total = 0                */
  /*                       H->bb = 1                */
  /*                   H->tautau = 2                */
  /*                     H->mumu = 3                */
  /*                       H->ss = 4                */
  /*                       H->cc = 5                */
  /*                       H->tt = 6                */
  /*                       H->gg = 7                */
  /*                   H->gamgam = 8                */
  /*                     H->gamZ = 9                */
  /*                       H->WW = 10               */
  /*                       H->ZZ = 11               */
  /*                       H->4e = 12               */
  /*                    H->2e2mu = 13               */
  /*              H->4lep (e,mu) = 14               */
  /*          H->4lep (e,mu,tau) = 15               */
  /*                H->e+nu e-nu = 16               */
  /*               H->e+nu mu-nu = 17               */
  /*    H->2l2nu(l=e,mu)(nu=any) = 18               */
  /* H->2l2nu(l=e,mu,tau)(nu=any) = 19              */  
  /*    H->2l2q (l=e,mu)(q=udcsb) = 20              */
  /* H->2l2q(l=e,mu,tau)(q=udcsb) = 21              */
  /* H->l+nu qq(*) (l=e,mu)(q=udcsb) = 22           */
  /*  H->2nu2q (nu=any)(q=udcsb) = 23               */
  /*            H->4q (q=udcsb) = 24                */
  /*      H->4f (f=any fermion) = 25                */
  /**************************************************/



  double PartialBR = 0;
  double BranchRatio = 0;
  int i = 0;
  double closestMass = 0;
  double tmpLow1, tmpHigh1, deltaX, deltaY1, slope1;
  double step;


  // If ID is unavailable return -1                                           
  if(ID > 25 || ID < 1){return -1;}


  // If mH is out of range return -1                                            
  // else find what array number to read                                        
  if( mH < 90 || mH > 1000){return -1;}
  else{

    //Find index and closest higgs mass for which we have numbers
    if(mH <=110 ){step = 5; i = (int)((mH - 90)/step); closestMass = (int)(step*i + 90);}
    if(mH > 110 && mH <= 140 ){step = 0.5; i = (int)(4 + (mH-110)/step); closestMass = (step*(i-4) + 110);}
    if(mH > 140 && mH <= 160 ){step = 1; i = (int)(64 + (mH-140)/step); closestMass = (int)(step*(i-64) + 140);}
    if(mH > 160 && mH <= 290 ){step = 2; i = (int)(84 + (mH-160)/step); closestMass = (int)(step*(i-84) + 160);}
    if(mH > 290 && mH <= 350 ){step = 5; i = (int)(149 + (mH-290)/step); closestMass = (int)(step*(i-149) + 290);}
    if(mH > 350 && mH <= 400 ){step = 10; i = (int)(161 + (mH-350)/step); closestMass = (int)(step*(i-161) + 350);}
    if(mH > 400 && mH <= 600 ){step = 20; i = (int)(166 + (mH-400)/step); closestMass = (int)(step*(i-166) + 400);}
    if(mH > 600){step = 10; i = (int)(176 + (mH-600)/step); closestMass = (int)(step*(i-176) + 600);}


      tmpLow1 = BR[ID][i];                                                                                                                        
      tmpHigh1 = BR[ID][i+1];                                                                                                                   

      deltaX = mH - closestMass;

      deltaY1 = tmpHigh1 - tmpLow1;
      slope1 = deltaY1/step;

      if(!spline)
	{
	  if(deltaX == 0){ PartialBR = tmpLow1;}
	  else{ PartialBR = slope1*deltaX + tmpLow1;}
	}
      else if(spline)
	{
	  if(i < 1){i = 1;}
	  if(i+2 >= N_BR){i = N_BR - 3;}
	  static const int indexBR = 4;
	  double xmhBR[indexBR], sigBR[indexBR];
	  xmhBR[0]=mass_BR[i-1];xmhBR[1]=mass_BR[i];xmhBR[2]=mass_BR[i+1];xmhBR[3]=mass_BR[i+2];
	  sigBR[0]=BR[ID][i-1]; sigBR[1]=BR[ID][i]; sigBR[2]=BR[ID][i+1]; sigBR[3]=BR[ID][i+2];
	  
	  TGraph *graphBR = new TGraph(indexBR, xmhBR, sigBR);
	  TSpline3 *gsBR = new TSpline3("gsBR",graphBR);
	  gsBR->Draw();
	  PartialBR = gsBR->Eval(mH);
	  delete gsBR;
	  delete graphBR;
	}

      BranchRatio = PartialBR;

  }

  return BranchRatio;

} 


#endif
