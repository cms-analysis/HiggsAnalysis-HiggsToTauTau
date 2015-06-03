void hist2Dbaseplot(TH2D* hist, const char* titlename, double zmin, double zmax, bool log=false, const char* ztitle="", double textsize=0.12){

	gPad->SetRightMargin(0.20);
	gPad->SetTopMargin(0.05);
	hist->Draw("Colz");
	hist->SetStats(false);
	hist->GetXaxis()->SetTitleSize(0.05);
	hist->GetYaxis()->SetTitleSize(0.05);
	hist->GetZaxis()->SetTitleSize(0.05);
	hist->GetZaxis()->SetLabelOffset(0.01);
	hist->GetZaxis()->SetTitle(ztitle);
	hist->GetZaxis()->SetTitleOffset(1.1);

	TLatex* histtitle = new TLatex(120, 50, titlename);
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

TGraph* exclusionObserved(TH2D* hist)
{
	TH2D* hist_copy = new TH2D();
	hist->Copy(*hist_copy);
	Double_t contours[1];
	contours[0]=0.05;
	hist_copy->SetContour(1,contours);
	hist_copy->Draw("CONT LIST");
	hist_copy->SetLineWidth(2);
	gPad->Update();
   TObjArray *conts = (TObjArray*)gROOT->GetListOfSpecials()->FindObject("contours");
	TGraph* curve = (TGraph*)conts->First();
	gPad->Clear();
	return (TGraph*)curve->Clone();
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

void NLLPlot(const char* filename="output.root", bool asimov=false)
{
	set_plot_style();
	std::string qmu, as;
	if (asimov)
	{
		qmu = "qA";
		as = "_as";
	}
	else
	{
		qmu = "qmu";
		as = "";
	}
	TFile* File = new TFile(filename, "READ");

	const char* string1 = (char*) ("globalNLLhist"+as).c_str();
	const char* string2 = (char*) ("fullNLLhist"+as).c_str();
	const char* string3 = (char*) ("deltaNLLhist"+as).c_str();
	const char* string4 = (char*) (qmu+"Hist2D").c_str();
	const char* string5 = (char*) ("NLLmuFixedfor"+qmu).c_str();
	const char* string6 = (char*) ("NLLmuGlobalfor"+qmu).c_str();
	const char* string7 = (char*) ("deltaNLLfor"+qmu).c_str();
	const char* string8 = (char*) ("NLLdiff2D"+as).c_str();
	const char* string9 = (char*) ("rNLLdiff2D"+as).c_str();

	TH2D* globalNLLhist = (TH2D*) File->Get(string1);
	TH2D* fullNLLhist = (TH2D*) File->Get(string2);
	TH2D* deltaNLLhist = (TH2D*) File->Get(string3);
	TH2D* qmuHist2D = (TH2D*) File->Get(string4);
	TH2D* NLLmuFixedforqmu = (TH2D*) File->Get(string5);
	TH2D* NLLmuGlobalforqmu = (TH2D*) File->Get(string6);
	TH2D* deltaNLLforqmu = (TH2D*) File->Get(string7);
	TH2D* NLLdiff2D = (TH2D*) File->Get(string8);
	TH2D* rNLLdiff2D = (TH2D*) File->Get(string9);

	TH1D* NLLdiff = new TH1D("NLLdiff", ";NLL_{mia} - NLL_{mda}",100, -6,6);
	TH1D* rNLLdiff = new TH1D("rNLLdiff", ";NLL_{mia} - NLL_{mda}/NLL_{mda}",100, -1.5,1.5);

	int mAbins = fullNLLhist->GetNbinsX();
	int tanbbins = fullNLLhist->GetNbinsY();
	for(int i=1;i<=mAbins;i++)
	{
		for(int j=1;j<=tanbbins;j++)
		{
			double diff = fullNLLhist->GetBinContent(i,j) - NLLmuFixedforqmu->GetBinContent(i,j);
			double rdiff = (fullNLLhist->GetBinContent(i,j) - NLLmuFixedforqmu->GetBinContent(i,j))/NLLmuFixedforqmu->GetBinContent(i,j);
			deltaNLLforqmu->SetBinContent(i,j,qmuHist2D->GetBinContent(i,j)/2.0);
			if(diff < 10 && diff >-10)
			{
				NLLdiff->Fill(diff);
				NLLdiff2D->SetBinContent(i,j,diff);
			}
			if(rdiff < 1.5 && rdiff > -1.5)
			{
				rNLLdiff->Fill(rdiff);
				rNLLdiff2D->SetBinContent(i,j,rdiff);
			}
			//else std::cout << "relative: " << rdiff << " Bin: (" << fullNLLhist->GetXaxis()->GetBinLowEdge(i) << "," << fullNLLhist->GetYaxis()->GetBinLowEdge(j) << ")" << " Values: mia = " << fullNLLhist->GetBinContent(i,j) << " ,mda = " << NLLmuFixedforqmu->GetBinContent(i,j) << std::endl;
		}
	}
	TCanvas* c = new TCanvas("c", "c", 1300, 700);
	c->Divide(3,2);

	c->cd(1);
	double min = globalNLLhist->GetMinimum();
	//globalNLLhist->GetZaxis()->SetRangeUser(min-0.1,min+3);
	globalNLLhist->GetZaxis()->SetLabelSize(0.035);
	hist2Dbaseplot(globalNLLhist, "NLL^{glob}",-1039364.58, -1039364.56);
	

	c->cd(2);
	fullNLLhist->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(fullNLLhist, "full NLL",0.01,10000,true);

	c->cd(3);
	deltaNLLhist->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(deltaNLLhist, "#DeltaNLL",0.001,10000,true);

	c->cd(4);
	min = NLLmuGlobalforqmu->GetMinimum();
	NLLmuGlobalforqmu->GetZaxis()->SetLabelSize(0.035);
	hist2Dbaseplot(NLLmuGlobalforqmu, "NLL^{glob}",-1039364.58, -1039364.56);


	c->cd(5);
	NLLmuFixedforqmu->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(NLLmuFixedforqmu, "full NLL",0.01,10000,true);

	c->cd(6);
	deltaNLLforqmu->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(deltaNLLforqmu, "#DeltaNLL",0.001,10000,true);
	
	const char* plotnamec = (char*) ("deltaNLL"+as+".pdf").c_str();
	c->SaveAs(plotnamec);
	
	
	TCanvas* d = new TCanvas("d", "d", 1000, 700);
	d->Divide(2,2);

	d->cd(1);
	gPad->SetRightMargin(0.20);
	gPad->SetTopMargin(0.05);
	NLLdiff->Draw();
	NLLdiff->SetStats(false);
	NLLdiff->GetXaxis()->SetTitleSize(0.05);
	gPad->Update();
	d->cd(2);
	gPad->SetRightMargin(0.20);
	gPad->SetTopMargin(0.05);
	rNLLdiff->Draw();
	rNLLdiff->SetStats(false);
	rNLLdiff->GetXaxis()->SetTitleSize(0.05);
	gPad->Update();
	d->cd(3);
	NLLdiff2D->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(NLLdiff2D,"NLL_{mia}-NLL_{mda}",-6,6,false,"",0.08);
	d->cd(4);
	rNLLdiff2D->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(rNLLdiff2D,"NLL_{mia}-NLL_{mda}/NLL_{mda}",-0.3,0.3,false,"",0.08);
	
	const char* plotnamed = (char*) ("NLLdiff"+as+".pdf").c_str();
	d->SaveAs(plotnamed);

	if(asimov)
	{
		TH2D* CLsHist2D = (TH2D*) File->Get("CLsHist2D");
		TH2D* CLshistNLL = (TH2D*) File->Get("CLshistNLL");
		TCanvas* e = new TCanvas("e", "e", 866, 350);
		e->Divide(2,1);
		
		e->cd(1);
		CLsHist2D->Draw("Colz");
		gPad->Update();
		CLsHist2D->SetStats(false);
		CLsHist2D->GetZaxis()->SetRangeUser(0,1);
		CLsHist2D->Draw("Colz");

		e->cd(2);
		CLshistNLL->Draw("Colz");
		gPad->Update();
		CLshistNLL->SetStats(false);
		CLshistNLL->GetZaxis()->SetRangeUser(0,1);
		CLshistNLL->Draw("Colz");

		e->SaveAs("CLsComparison.pdf");
	}
	File->Close();
}
