void hist2Dbaseplot(TH2D* hist, const char* titlename, double zmin, double zmax, bool log=false, const char* ztitle="", double textsize=0.12, Color_t latexcolor=1){

	gPad->SetRightMargin(0.20);
	gPad->SetTopMargin(0.05);
	hist->Draw("Colz");
	hist->SetStats(false);
	hist->GetXaxis()->SetTitleSize(0.05);
	hist->GetYaxis()->SetTitleSize(0.05);
	hist->GetZaxis()->SetTitleSize(0.05);
	hist->GetZaxis()->SetLabelSize(0.05);
	hist->GetZaxis()->SetLabelOffset(0.01);
	hist->GetZaxis()->SetTitle(ztitle);
	hist->GetZaxis()->SetTitleOffset(1.1);

	TLatex* histtitle = new TLatex(120, 50, titlename);
	histtitle->SetTextColor(latexcolor);
	histtitle->SetTextSize(textsize);
	histtitle->Draw("Same");
	if(log)
	{
		gPad->SetLogz();
		hist->GetZaxis()->SetRangeUser(zmin, zmax);
	}
	else
	{
		hist->GetZaxis()->SetRangeUser(zmin, zmax);
	}
	gPad->Update();

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

	TCanvas* c = new TCanvas("c", "c", 866,700);
	c->Divide(2,2);

	c->cd(1);
	hist2Dbaseplot(ggcmb, "#sigma_{gg#phi}#upointBR_{#phi#rightarrow#tau#tau}",0.000001,450,true,"[pb]");

	c->cd(2);
	hist2Dbaseplot(bbcmb, "#sigma_{bb#phi}#upointBR_{#phi#rightarrow#tau#tau}",0.000001,450,true,"[pb]");

	c->cd(3);
	gPad->SetRightMargin(0.20);
	gPad->SetTopMargin(0.05);
	cluster->Draw("Colz");
	cluster->SetStats(false);
	cluster->GetXaxis()->SetTitleSize(0.05);
	cluster->GetYaxis()->SetTitleSize(0.05);
	cluster->GetZaxis()->SetTitleSize(0.05);
	cluster->GetZaxis()->SetLabelSize(0.05);
	cluster->GetZaxis()->SetTitleOffset(1.1);
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
	gPad->Update();

	c->cd(4);
	hist2Dbaseplot(masscluster, "m_{cluster}",50,1000,true,"[GeV]");

	if(reference=="A") c->SaveAs("clusterA.pdf");
	if(reference=="H") c->SaveAs("clusterH.pdf");
	if(reference=="h") c->SaveAs("clusterh.pdf");
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

