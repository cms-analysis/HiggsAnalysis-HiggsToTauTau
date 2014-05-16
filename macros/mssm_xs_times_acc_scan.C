#include <iostream>

#include "HiggsAnalysis/HiggsToTauTau/macros/mssm_xs_tools.h"
#include "HiggsAnalysis/HiggsToTauTau/macros/mssm_xs_tools.C"

#include "TTree.h"
#include "TFile.h"
#include "TAxis.h"
#include "TGraph.h"
#include "TString.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TPaveLabel.h"
#include "TGraphAsymmErrors.h"
#include <string> 
#include <map>  

#include "HiggsAnalysis/HiggsToTauTau/macros/Utils.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"
#include "HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc"

double closest_mass(double mass){
  if(fabs(mass-90)<fabs(mass-100)){
    return 90;
  }
  else{
    if(fabs(mass-100)<fabs(mass-120)){
      return 100;
    }
    else{
      if(fabs(mass-120)<fabs(mass-130)){
	return 120;
      }      
      else{
	if(fabs(mass-130)<fabs(mass-140)){
	  return 130;
	}
	else{
	  if(fabs(mass-140)<fabs(mass-160)){
	    return 140;
	  }	
	  else{
	    if(fabs(mass-160)<fabs(mass-180)){
	      return 160;
	    }
	    else{
	      if(fabs(mass-180)<fabs(mass-200)){
		return 180;
	      }
	      else{
		if(fabs(mass-200)<fabs(mass-250)){
		  return 200;
		}
		else{
		  if(fabs(mass-250)<fabs(mass-300)){
		    return 250;
		  }
		  else{
		    if(fabs(mass-300)<fabs(mass-350)){
		      return 300;
		    }
		    else{
		      if(fabs(mass-350)<fabs(mass-400)){
			return 350;
		      }
		      else{
			if(fabs(mass-400)<fabs(mass-450)){
			  return 400;
			}
			else{
			  if(fabs(mass-450)<fabs(mass-500)){
			    return 450;
			  }
			  else{
			    if(fabs(mass-500)<fabs(mass-600)){
			      return 500;
			    }
			    else{
			      if(fabs(mass-600)<fabs(mass-700)){
				return 600;
			      }
			      else{
				if(fabs(mass-700)<fabs(mass-800)){
				  return 700;
				}
				else{
				  if(fabs(mass-800)<fabs(mass-900)){
				    return 800;
				  }
				  else{
				    if(fabs(mass-900)<fabs(mass-1000)){
				      return 900;
				    }
				    else{
				      return 1000;
				    }
				  }
				}
			      }
			    }
			  }
			}
		      }
		    }
		  }
		}
	      }
	    }
	  }
	}
      }
    }
  }
}

void 
mssm_xs_times_acc_scan(char* path, std::string filepath, double tanb, std::string category)
{
  mssm_xs_tools xs;
  xs.SetInput(path);
  
  //TGraph *SM = new TGraph();
  TGraph *ggH = new TGraph();
  TGraph *bbH = new TGraph();
  TGraph *ggA = new TGraph();
  TGraph *gg = new TGraph();
  TGraph *bbA = new TGraph();
  TGraph *ggh = new TGraph();
  TGraph *bbh = new TGraph();
  TGraph *bb = new TGraph();
  TGraph *signi = new TGraph();

  TGraph *ggHacc = new TGraph();
  TGraph *bbHacc = new TGraph();
  TGraph *ggAacc = new TGraph();
  TGraph *ggacc = new TGraph();
  TGraph *bbAacc = new TGraph();
  TGraph *gghacc = new TGraph();
  TGraph *bbhacc = new TGraph();
  TGraph *bbacc = new TGraph();

  double xs_eff_ggH[4];
  double xs_eff_bbH[4];

  double masses[19];
  masses[0]=  90;
  masses[1]= 100;
  masses[2]= 120;
  masses[3]= 130;
  masses[4]= 140;
  masses[5]= 160;
  masses[6]= 180;
  masses[7]= 200;
  masses[8]= 250;
  masses[9]= 300;
  masses[10]= 350;
  masses[11]= 400;
  masses[12]= 450;
  masses[13]= 500;
  masses[14]= 600;
  masses[15]= 700;
  masses[16]= 800;
  masses[17]= 900;
  masses[18]=1000;

  TFile* inputFile = new TFile(std::string(filepath+"/"+"htt_mt.inputs-mssm-8TeV-0.root").c_str()); 
  TH1F* h_background = new TH1F();
  double ggH_value, bbH_value, ggA_value, bbA_value, ggh_value, bbh_value;;
  
  double mA;

  h_background=get<TH1F>(inputFile, std::string("muTau_"+category+"/ZTT").c_str());
  h_background->Add(get<TH1F>(inputFile, std::string("muTau_"+category+"/QCD").c_str()));
  h_background->Add(get<TH1F>(inputFile, std::string("muTau_"+category+"/W").c_str()));
  h_background->Add(get<TH1F>(inputFile, std::string("muTau_"+category+"/ZL").c_str()));
  h_background->Add(get<TH1F>(inputFile, std::string("muTau_"+category+"/ZJ").c_str()));
  h_background->Add(get<TH1F>(inputFile, std::string("muTau_"+category+"/TT").c_str()));
  h_background->Add(get<TH1F>(inputFile, std::string("muTau_"+category+"/VV").c_str()));
   
 TH1F* h_ggH = new TH1F();
 TH1F* h_bbH = new TH1F();
 TH1F* h_ggh = new TH1F();
 TH1F* h_bbh = new TH1F();
 TH1F* h_ggA = new TH1F();
 TH1F* h_bbA = new TH1F();

  for(unsigned int idx=0; idx<19; idx++){
  
    mA=masses[idx];
    std::cout << "mh = " << xs.Give_Mass_h(mA, tanb) << "   mA = " << mA << "   mH = " << xs.Give_Mass_H(mA, tanb) << std::endl;
    std::cout << "mh = " << closest_mass(xs.Give_Mass_h(mA, tanb)) << "   mA = " << mA << "   mH = " << closest_mass(xs.Give_Mass_H(mA, tanb)) << std::endl;

    //SM->SetPoint(tanb-1, tanb, 1.21*1000);

    std::cout << "MSSM Cross Section [ggH]:" << std::endl;
    xs_eff_ggH[0] = xs.Give_Xsec_ggFA(mA, tanb)*xs.Give_BR_A_tautau(mA, tanb);
    std::cout << " -> xsec(ggA):\t" << xs.Give_Xsec_ggFA(mA, tanb) << "\t --- \t" << xs.Give_BR_A_tautau(mA, tanb) << std::endl;
    xs_eff_ggH[1] = xs.Give_Xsec_ggFH(mA, tanb)*xs.Give_BR_H_tautau(mA, tanb);
    std::cout << " -> xsec(ggH):\t" << xs.Give_Xsec_ggFH(mA, tanb) << "\t --- \t" << xs.Give_BR_H_tautau(mA, tanb) << std::endl;
    xs_eff_ggH[2] = xs.Give_Xsec_ggFh(mA, tanb)*xs.Give_BR_h_tautau(mA, tanb);
    std::cout << " -> xsec(ggh):\t" << xs.Give_Xsec_ggFh(mA, tanb) << "\t --- \t" << xs.Give_BR_h_tautau(mA, tanb) << std::endl;
    xs_eff_ggH[3] = (xs_eff_ggH[0]+xs_eff_ggH[1]+xs_eff_ggH[2]);//*1.237; 
    std::cout << "mA: "<< mA << "  tanb: "<<tanb<<" -> ggH_xsec(cmb):\t" << xs_eff_ggH[3] << std::endl;
  
    char mass_help[50];
    sprintf (mass_help, "%0.0f", mA); 
    h_ggA = get<TH1F>(inputFile, std::string("muTau_"+category+"/ggH"+mass_help).c_str());
    ggA_value=h_ggA->Integral();
    std::cout << "acc of ggA " << h_ggA->Integral() << std::endl;
    ggA->SetPoint(idx, mA, xs_eff_ggH[0]);
    ggAacc->SetPoint(idx, mA, ggA_value);

    sprintf (mass_help, "%0.0f", closest_mass(xs.Give_Mass_H(mA, tanb))); 
    h_ggH = get<TH1F>(inputFile, std::string("muTau_"+category+"/ggH"+mass_help).c_str());
    ggH_value=h_ggH->Integral();
    std::cout << "acc of ggH " << h_ggH->Integral() << std::endl;
    ggH->SetPoint(idx, mA, xs_eff_ggH[1]);
    ggHacc->SetPoint(idx, mA, ggH_value);

    sprintf (mass_help, "%0.0f", closest_mass(xs.Give_Mass_h(mA, tanb))); 
    h_ggh = get<TH1F>(inputFile, std::string("muTau_"+category+"/ggH"+mass_help).c_str());
    ggh_value=h_ggh->Integral();
    std::cout << "acc of ggh " << h_ggh->Integral() << std::endl;
    ggh->SetPoint(idx, mA, xs_eff_ggH[2]);
    gghacc->SetPoint(idx, mA, ggh_value);

    //gg->SetPoint(idx, mA, xs_eff_ggH[2]+xs_eff_ggH[1]+xs_eff_ggH[0]);
    if(mA<130) gg->SetPoint(idx, mA, xs_eff_ggH[2]+xs_eff_ggH[0]);
    else if(mA==130) gg->SetPoint(idx, mA, xs_eff_ggH[2]+xs_eff_ggH[1]+xs_eff_ggH[0]);
    else gg->SetPoint(idx, mA, xs_eff_ggH[1]+xs_eff_ggH[0]);
    //ggacc->SetPoint(idx, mA, ggh_value+ggH_value+ggA_value);
    if(mA<130) ggacc->SetPoint(idx, mA, ggh_value+ggA_value);
    else if(mA==130) ggacc->SetPoint(idx, mA, ggh_value+ggH_value+ggA_value);
    else ggacc->SetPoint(idx, mA, ggH_value+ggA_value);
    std::cout << std::endl;



    std::cout << "MSSM Cross Section [bbH]:" << std::endl;
    xs_eff_bbH[0] = xs.GiveXsec_Santander_A(mA, tanb)*xs.Give_BR_A_tautau(mA, tanb);
    std::cout << " -> xsec(ggA):\t" << xs.GiveXsec_Santander_A(mA, tanb) << "\t --- \t" << xs.Give_BR_A_tautau(mA, tanb) << std::endl;
    xs_eff_bbH[1] = xs.GiveXsec_Santander_H(mA, tanb)*xs.Give_BR_H_tautau(mA, tanb);
    std::cout << " -> xsec(bbH):\t" << xs.GiveXsec_Santander_H(mA, tanb) << "\t --- \t" << xs.Give_BR_H_tautau(mA, tanb) << std::endl;
    xs_eff_bbH[2] = xs.GiveXsec_Santander_h(mA, tanb)*xs.Give_BR_h_tautau(mA, tanb);
    std::cout << " -> xsec(ggh):\t" << xs.GiveXsec_Santander_h(mA, tanb) << "\t --- \t" << xs.Give_BR_h_tautau(mA, tanb) << std::endl;
    xs_eff_bbH[3] = (xs_eff_bbH[0]+xs_eff_bbH[1]+xs_eff_bbH[2]);//*1.627;
    std::cout << "mA: "<< mA << "  tanb: "<<tanb<<"  -> bbH_xsec(cmb):\t" << xs_eff_bbH[3] << std::endl;

    sprintf (mass_help, "%0.0f", mA); 
    h_bbA = get<TH1F>(inputFile, std::string("muTau_"+category+"/bbH"+mass_help).c_str());
    bbA_value=h_bbA->Integral();
    std::cout << "acc of bbA " << h_bbA->Integral() << std::endl;
    bbA->SetPoint(idx, mA, xs_eff_bbH[0]);
    bbAacc->SetPoint(idx, mA, bbA_value);

    sprintf (mass_help, "%0.0f", closest_mass(xs.Give_Mass_H(mA, tanb))); 
    h_bbH = get<TH1F>(inputFile, std::string("muTau_"+category+"/bbH"+mass_help).c_str());
    bbH_value=h_bbH->Integral();
    std::cout << "acc of bbH " << h_bbH->Integral() << std::endl;
    bbH->SetPoint(idx, mA, xs_eff_bbH[1]);
    bbHacc->SetPoint(idx, mA, bbH_value);

    sprintf (mass_help, "%0.0f", closest_mass(xs.Give_Mass_h(mA, tanb))); 
    h_bbh = get<TH1F>(inputFile, std::string("muTau_"+category+"/bbH"+mass_help).c_str());
    bbh_value=h_bbh->Integral();
    std::cout << "acc of bbh " << h_bbh->Integral() << std::endl;
    bbh->SetPoint(idx, mA, xs_eff_bbH[2]);
    bbhacc->SetPoint(idx, mA, bbh_value);

    //bb->SetPoint(idx, mA, xs_eff_bbH[2]+xs_eff_bbH[1]+xs_eff_bbH[0]);
    if(mA<130) bb->SetPoint(idx, mA, xs_eff_bbH[2]+xs_eff_bbH[0]);
    else if(mA==130) bb->SetPoint(idx, mA, xs_eff_bbH[2]+xs_eff_bbH[1]+xs_eff_bbH[0]);
    else bb->SetPoint(idx, mA, xs_eff_bbH[1]+xs_eff_bbH[0]); 
    //bbacc->SetPoint(idx, mA, bbh_value+bbH_value+bbA_value);
    if(mA<130) bbacc->SetPoint(idx, mA, bbh_value+bbA_value);
    else if(mA==130) bbacc->SetPoint(idx, mA, bbh_value+bbH_value+bbA_value);
    else bbacc->SetPoint(idx, mA, bbH_value+bbA_value); 		  
    std::cout << std::endl;
    std::cout << std::endl;

    h_ggA->Scale(xs_eff_ggH[0]);
    h_ggH->Scale(xs_eff_ggH[1]); 
    h_ggh->Scale(xs_eff_ggH[2]);
    h_bbA->Scale(xs_eff_bbH[0]);
    h_bbH->Scale(xs_eff_bbH[1]); 
    h_bbh->Scale(xs_eff_bbH[2]);

    h_ggA->Add(h_ggH);
    h_ggA->Add(h_ggh);    
    h_bbA->Add(h_bbH);
    h_bbA->Add(h_bbh);   
    h_bbA->Add(h_ggA);

    double significance=0;
    double significance_help=0;
    for(int nbin=0; nbin<h_bbA->GetNbinsX()+1; nbin++){ 
      if(h_background->GetBinContent(nbin)+h_bbA->GetBinContent(nbin)!=0) significance=h_bbA->GetBinContent(nbin)/sqrt(h_background->GetBinContent(nbin)+h_bbA->GetBinContent(nbin));
      else significance=0;
      //if(significance>significance_help){
      significance_help+=significance;
      //}
    }
    std::cout << "significance " << significance_help << std::endl;
    signi->SetPoint(idx, mA, significance_help);

    //destruct TH1Fs
    h_ggA->~TH1F();
    h_ggH->~TH1F(); 
    h_ggh->~TH1F();
    h_bbA->~TH1F();
    h_bbH->~TH1F(); 
    h_bbh->~TH1F();

    std::cout << std::endl;
    std::cout << std::endl;
  }			    

  /// do the drawing
  TCanvas* canv1 = new TCanvas("canv1", "xs*BR", 600, 600);
  canv1->cd();
  //canv1->SetGridx(1);
  //canv1->SetGridy(1);
  canv1->SetLeftMargin(0.15);
  canv1->SetLogy(1);

  // draw a frame to define the range
  TH1F* hr=canv1->DrawFrame(ggA->GetX()[0]-.01, 0.0001, ggA->GetX()[ggA->GetN()-1]+.01, 10000);
  // format x axis
  hr->SetXTitle("m_{A}");
  hr->GetXaxis()->SetLabelSize(0.045);
  hr->GetXaxis()->SetTitleFont(62);
  hr->GetXaxis()->SetLabelFont(62);
  hr->GetXaxis()->SetTitleColor(1);
  hr->GetXaxis()->SetTitleOffset(1.08);
  // format y axis
  hr->SetYTitle("#sigma*BR and acc*signal_{eff}*lumi");
  hr->GetXaxis()->SetTitleFont(62);
  hr->GetYaxis()->SetLabelFont(62);
  hr->GetYaxis()->SetLabelSize(0.045);
  hr->GetYaxis()->SetTitleOffset(1.6);
  hr->GetXaxis()->SetTitleColor(1);
  hr->SetNdivisions(505, "X");

  //ggA->Draw("PLsame");
  ggA->SetLineStyle(3.);
  ggA->SetLineWidth(2.); 
  ggA->SetLineColor(kBlue);
  ggA->SetMarkerStyle(23);
  ggA->SetMarkerSize(0);
  ggA->SetMarkerColor(kBlue);

  //ggH->Draw("PLsame");
  ggH->SetLineStyle(2.);
  ggH->SetLineWidth(2.); 
  ggH->SetLineColor(kBlue);
  ggH->SetMarkerStyle(22);
  ggH->SetMarkerSize(0);
  ggH->SetMarkerColor(kBlue);

  //ggh->Draw("PLsame");
  ggh->SetLineStyle(1.);
  ggh->SetLineWidth(2.); 
  ggh->SetLineColor(kBlue);
  ggh->SetMarkerStyle(20);
  ggh->SetMarkerSize(0);
  ggh->SetMarkerColor(kBlue);

   //ggAacc->Draw("PLsame");
  ggAacc->SetLineStyle(3.);
  ggAacc->SetLineWidth(2.); 
  ggAacc->SetLineColor(kMagenta);
  ggAacc->SetMarkerStyle(23);
  ggAacc->SetMarkerSize(0);
  ggAacc->SetMarkerColor(kMagenta);

  //ggHacc->Draw("PLsame");
  ggHacc->SetLineStyle(2.);
  ggHacc->SetLineWidth(2.); 
  ggHacc->SetLineColor(kMagenta);
  ggHacc->SetMarkerStyle(22);
  ggHacc->SetMarkerSize(0);
  ggHacc->SetMarkerColor(kMagenta);

  //gghacc->Draw("PLsame");
  gghacc->SetLineStyle(1.);
  gghacc->SetLineWidth(2.); 
  gghacc->SetLineColor(kMagenta);
  gghacc->SetMarkerStyle(20);
  gghacc->SetMarkerSize(0);
  gghacc->SetMarkerColor(kMagenta);

  //bbA->Draw("PLsame");
  bbA->SetLineStyle(3.);
  bbA->SetLineWidth(2.); 
  bbA->SetLineColor(kRed);
  bbA->SetMarkerStyle(23);
  bbA->SetMarkerSize(0);
  bbA->SetMarkerColor(kRed);

  //bbH->Draw("PLsame");
  bbH->SetLineStyle(2.);
  bbH->SetLineWidth(2.); 
  bbH->SetLineColor(kRed);
  bbH->SetMarkerStyle(22);
  bbH->SetMarkerSize(0);
  bbH->SetMarkerColor(kRed);

  //bbh->Draw("PLsame");
  bbh->SetLineStyle(1.);
  bbh->SetLineWidth(2.); 
  bbh->SetLineColor(kRed);
  bbh->SetMarkerStyle(20);
  bbh->SetMarkerSize(0);
  bbh->SetMarkerColor(kRed);

   //bbAacc->Draw("PLsame");
  bbAacc->SetLineStyle(3.);
  bbAacc->SetLineWidth(2.); 
  bbAacc->SetLineColor(kOrange);
  bbAacc->SetMarkerStyle(23);
  bbAacc->SetMarkerSize(0);
  bbAacc->SetMarkerColor(kOrange);

  //bbHacc->Draw("PLsame");
  bbHacc->SetLineStyle(2.);
  bbHacc->SetLineWidth(2.); 
  bbHacc->SetLineColor(kOrange);
  bbHacc->SetMarkerStyle(22);
  bbHacc->SetMarkerSize(0);
  bbHacc->SetMarkerColor(kOrange);

  //bbhacc->Draw("PLsame");
  bbhacc->SetLineStyle(1.);
  bbhacc->SetLineWidth(2.); 
  bbhacc->SetLineColor(kOrange);
  bbhacc->SetMarkerStyle(20);
  bbhacc->SetMarkerSize(0);
  bbhacc->SetMarkerColor(kOrange);
  
  gg->Draw("PLsame");
  gg->SetLineStyle(1.);
  gg->SetLineWidth(3.); 
  gg->SetLineColor(kBlue+2);
  gg->SetMarkerStyle(20);
  gg->SetMarkerSize(0);
  gg->SetMarkerColor(kBlue+2);

  ggacc->Draw("PLsame");
  ggacc->SetLineStyle(1.);
  ggacc->SetLineWidth(3.); 
  ggacc->SetLineColor(kMagenta);
  ggacc->SetMarkerStyle(20);
  ggacc->SetMarkerSize(0);
  ggacc->SetMarkerColor(kMagenta);

  bb->Draw("PLsame");
  bb->SetLineStyle(1.);
  bb->SetLineWidth(3.); 
  bb->SetLineColor(kRed+2);
  bb->SetMarkerStyle(20);
  bb->SetMarkerSize(0);
  bb->SetMarkerColor(kRed+2);

  bbacc->Draw("PLsame");
  bbacc->SetLineStyle(1.);
  bbacc->SetLineWidth(3.); 
  bbacc->SetLineColor(kOrange);
  bbacc->SetMarkerStyle(20);
  bbacc->SetMarkerSize(0);
  bbacc->SetMarkerColor(kOrange);

  /*SM->Draw("PLsame");
  SM->SetLineStyle(8.);
  SM->SetLineWidth(3.); 
  SM->SetLineColor(kGreen+1);
  SM->SetMarkerStyle(20);
  SM->SetMarkerSize(0);
  SM->SetMarkerColor(kGreen+1);*/

  // signi->Draw("PLsame");
  signi->SetLineStyle(1.);
  signi->SetLineWidth(2.); 
  signi->SetLineColor(kBlack);
  signi->SetMarkerStyle(20);
  signi->SetMarkerSize(0);
  signi->SetMarkerColor(kBlack);

  TLegend* leg0;
  /// setup the CMS Preliminary
  //std::ostringstream ss;
  //ss << mA;
  //std::string s(ss.str());
  std::string tanb_string = std::to_string((int)tanb);
  CMSPrelim(std::string("#events,   m^{h}_{max} scenario,  tan#beta = " + tanb_string).c_str(), "", 0.15, 0.835);
  leg0 = new TLegend(0.58, 0.12, 0.90, 0.32); 
  leg0->SetBorderSize( 0 );
  leg0->SetFillStyle ( 1001 );
  leg0->SetFillColor (kWhite);
  //leg0->SetHeader( "#sigma * BR" );
  //leg0->AddEntry( SM,  "ggH_{SM} #rightarrow #tau#tau",  "PL" );

  //leg0->AddEntry( gghacc, "ggh #sigma*BR",  "PL" );
  //leg0->AddEntry( ggAacc, "ggA #sigma*BR",  "PL" );
  //leg0->AddEntry( ggHacc, "ggH #sigma*BR",  "PL" );
  leg0->AddEntry( gg,  "gg #sigma*BR",  "PL" );

  //leg0->AddEntry( ggh, "ggh acc*s_{eff}*lumi",  "PL" );
  //leg0->AddEntry( ggA, "ggA acc*s_{eff}*lumi",  "PL" );
  //leg0->AddEntry( ggH, "ggH acc*sl_{eff}*lumi",  "PL" );
  leg0->AddEntry( ggacc,  "gg acc*s_{eff}*lumi",  "PL" );

  //leg0->AddEntry( bbh, "bbh #sigma*BR",  "PL" );
  //leg0->AddEntry( bbA, "bbA #sigma*BR",  "PL" );
  //leg0->AddEntry( bbH, "bbH #sigma*BR",  "PL" );
  leg0->AddEntry( bb,  "bb #sigma*BR",  "PL" );

  //leg0->AddEntry( bbhacc, "bbh acc*s_{eff}*lumi",  "PL" );
  //leg0->AddEntry( bbAacc, "bbA acc*s_{eff}*lumi",  "PL" );
  //leg0->AddEntry( bbHacc, "bbH acc*s_{eff}*lumi",  "PL" );
  leg0->AddEntry( bbacc,  "bb acc*s_{eff}*lumi",  "PL" );

  //leg0->AddEntry( signi,  "sum of all bins: s/sqrt(s+b)",  "PL" );
  leg0->Draw("same");
  
  canv1->Print("xsBRtimesacc.png");
  canv1->Print("xsBRtimesacc.pdf");
return;
}
