#include "TString.h"
#include "HiggsAnalysis/HiggsToTauTau/interface/HttStyles.h"

void hist2Dbaseplot(TH2D* hist, const char* titlename, double zmin, double zmax, bool log=false, const char* ztitle="", std::string name, std::string reference, double textsize=0.12, Color_t latexcolor=1){  
	TCanvas* c = new TCanvas("c", "c", 600,600);
	//SetStyle();

	// c->SetRightMargin(0.23);
// 	c->SetLeftMargin(0.1);
// 	c->SetTopMargin(0.05);
	
	c->SetFillColor      (0);
	c->SetBorderMode     (0);
	c->SetBorderSize     (10);
	// Set margins to reasonable defaults
	c->SetLeftMargin     (0.13);
	c->SetRightMargin    (0.18);
	//c->SetTopMargin      (0.08);
	c->SetBottomMargin   (0.13);
	// Setup a frame which makes sense
	c->SetFrameFillStyle (0);
	c->SetFrameLineStyle (0);
	c->SetFrameBorderMode(0);
	c->SetFrameBorderSize(10);
	c->SetFrameFillStyle (0);
	c->SetFrameLineStyle (0);
	c->SetFrameBorderMode(0);
	c->SetFrameBorderSize(10);
  
	hist->Draw("Colz");
	hist->SetStats(false);
	hist->GetXaxis()->SetLabelFont(62);
	hist->GetXaxis()->SetLabelOffset(0.018);
	hist->GetXaxis()->SetTitleColor(1);
	hist->GetXaxis()->SetTitleOffset(1.05);
	hist->GetXaxis()->SetTitleFont(62);
	hist->GetXaxis()->SetTitleSize(0.055);

	hist->GetYaxis()->SetLabelFont(62);
	hist->GetYaxis()->SetLabelOffset(0.023);
	hist->GetYaxis()->SetTitleSize(0.055);
	hist->GetYaxis()->SetTitleOffset(1.15);
	hist->GetYaxis()->SetTitleFont(62);
	hist->GetYaxis()->SetLabelSize(0.04);
	
	hist->GetZaxis()->SetTitle(ztitle);
	hist->GetZaxis()->SetLabelFont(62);
	hist->GetZaxis()->SetTitleSize(0.055);
	hist->GetZaxis()->SetTitleOffset(1.15);
	hist->GetZaxis()->SetLabelSize(0.04);
	



	TLatex* histtitle = new TLatex(120, 63, titlename);
	histtitle->SetTextColor(latexcolor);
	histtitle->SetTextSize(textsize);
	histtitle->Draw("Same");
	if(log) {
	  c->SetLogz();
	  hist->GetZaxis()->SetRangeUser(zmin, zmax);
	}
	else {
	  hist->GetZaxis()->SetRangeUser(zmin, zmax);
	}
	c->Update();

 	c->Print(std::string(name).append("_").append(reference).append(".png").c_str());
        c->Print(std::string(name).append("_").append(reference).append(".pdf").c_str());
} 

void set_plot_style()
{
    const Int_t NRGBs = 5;
    const Int_t NCont = 255;

    Double_t stops[NRGBs] = { 0.00, 0.34, 0.61, 0.84, 1.00 };
    Double_t red[NRGBs]   = { 0.00, 0.00, 0.87, 1.00, 0.51 };
    Double_t green[NRGBs] = { 0.00, 0.81, 1.00, 0.20, 0.00 };
    Double_t blue[NRGBs]  = { 0.51, 1.00, 0.12, 0.00, 0.00 };
    TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);
    gStyle->SetNumberContours(NCont);
}

void clusterPlot(TFile* file, std::string reference)
{
	TH2D* masscluster = (TH2D*) file->Get("masscluster");
	TH2D* ggcmb = (TH2D*) file->Get("ggcmb");
	TH2D* bbcmb = (TH2D*) file->Get("bbcmb");
	TH2D* cluster = (TH2D*) file->Get("cluster");
   
	//hist2Dbaseplot(ggcmb, "#sigma_{gg#phi}#upoint#font[52]{B}_{#phi#rightarrow#tau#tau}",0.000001,450,true,"[pb]", "xs_gg", reference);
	hist2Dbaseplot(ggcmb, "",0.000001,450,true,"#sigma#font[42]{(gg#phi)}#upoint#font[52]{B}#font[42]{(#phi#rightarrow#tau#tau)} [pb]", "xs_gg", reference, 0.06);
	//hist2Dbaseplot(bbcmb, "#sigma_{bb#phi}#upoint#font[52]{B}_{#phi#rightarrow#tau#tau}",0.000001,450,true,"[pb]", "xs_bb", reference);
	hist2Dbaseplot(bbcmb, "",0.000001,450,true,"#sigma#font[42]{(gg#phi)}#upoint#font[52]{B}#font[42]{(#phi#rightarrow#tau#tau)} [pb]", "xs_bb", reference, 0.06);
	hist2Dbaseplot(masscluster, "cluster mass",50,1000,true,"[GeV]", "clusterMass", reference,0 .06);

	TCanvas* c1 = new TCanvas("c1", "c1", 600,600);	
	c1->SetFillColor      (0);
	c1->SetBorderMode     (0);
	c1->SetBorderSize     (10);
	// Set margins to reasonable defaults
	c1->SetLeftMargin     (0.13);
	c1->SetRightMargin    (0.18);
	//c->SetTopMargin      (0.08);
	c1->SetBottomMargin   (0.13);
	// Setup a frame which makes sense
	c1->SetFrameFillStyle (0);
	c1->SetFrameLineStyle (0);
	c1->SetFrameBorderMode(0);
	c1->SetFrameBorderSize(10);
	c1->SetFrameFillStyle (0);
	c1->SetFrameLineStyle (0);
	c1->SetFrameBorderMode(0);
	c1->SetFrameBorderSize(10);
  
	cluster->Draw("Colz");
	cluster->SetStats(false);
	cluster->GetXaxis()->SetLabelFont(62);
	cluster->GetXaxis()->SetLabelOffset(0.018);
	cluster->GetXaxis()->SetTitleColor(1);
	cluster->GetXaxis()->SetTitleOffset(1.05);
	cluster->GetXaxis()->SetTitleFont(62);
	cluster->GetXaxis()->SetTitleSize(0.055);

	cluster->GetYaxis()->SetLabelFont(62);
	cluster->GetYaxis()->SetLabelOffset(0.023);
	cluster->GetYaxis()->SetTitleSize(0.055);
	cluster->GetYaxis()->SetTitleOffset(1.15);
	cluster->GetYaxis()->SetTitleFont(62);
	cluster->GetYaxis()->SetLabelSize(0.04);
	
	//cluster->GetZaxis()->SetTitle(ztitle);
	cluster->GetZaxis()->SetLabelFont(62);
	cluster->GetZaxis()->SetTitleSize(0.055);
	cluster->GetZaxis()->SetTitleOffset(1.15);
	cluster->GetZaxis()->SetLabelSize(0.04);
	cluster->GetZaxis()->SetRangeUser(0.,7.);


	TPaveText* pt = new TPaveText(630,28,980,58);
	pt->AddText("Contributions");
	pt->AddText("1: h");
	pt->AddText("2: H");
	pt->AddText("3: h+H");
	pt->AddText("4: A");
	pt->AddText("5: h+A");
	pt->AddText("6: H+A");
	pt->AddText("7: h+H+A");
	pt->SetFillStyle(0);
	pt->SetBorderSize(0);
	pt->Draw("Same");
	c1->Update();

	c1->SaveAs("cluster.pdf");
	c1->SaveAs("cluster.png");

}

void higgsContributionsPlot(const char* xsfilenameA, const char* xsfilenameH, const char* xsfilenameh)
{
	set_plot_style();

	TFile* xsfileA = new TFile(xsfilenameA, "READ");
	TFile* xsfileH = new TFile(xsfilenameH, "READ");
	TFile* xsfileh = new TFile(xsfilenameh, "READ");

	clusterPlot(xsfileA,"A");
	clusterPlot(xsfileH,"H");
	clusterPlot(xsfileh,"h");
}

