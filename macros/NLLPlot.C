void NLLPlot(const char* filename="output.root", bool asimov=false)
{
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
	TCanvas* c = new TCanvas("c", "c", 1300, 700);
	TCanvas* d = new TCanvas("d", "d", 1300, 700);
	
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

	TH1D* NLLdiff = new TH1D("NLLdiff", "Difference between the full NLL of the two approaches; NLL_{mia} - NLL_{mda}",100, -6,6);
	TH1D* rNLLdiff = new TH1D("rNLLdiff", "rel. Difference between the full NLL of the two approaches; (NLL_{mia} - NLL_{mda})/NLL_{mda}",100, -1.5,1.5);

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
	c->Divide(3,2);

	c->cd(1);
	globalNLLhist->Draw("Colz");
	double min = globalNLLhist->GetMinimum();
	globalNLLhist->GetZaxis()->SetRangeUser(min-0.1,min+3);
	globalNLLhist->SetStats(false);
	gPad->Update();
	globalNLLhist->Draw("Colz");

	c->cd(2);
	fullNLLhist->Draw("Colz");
	fullNLLhist->GetZaxis()->SetRangeUser(0.01,10000);
	fullNLLhist->SetStats(false);
	gPad->SetLogz();
	gPad->Update();
	fullNLLhist->Draw("Colz");

	c->cd(3);
	deltaNLLhist->Draw("Colz");
	deltaNLLhist->GetZaxis()->SetRangeUser(0.001,10000);
	deltaNLLhist->SetStats(false);
	gPad->SetLogz();
	gPad->Update();
	deltaNLLhist->Draw("Colz");

	c->cd(4);
	NLLmuGlobalforqmu->Draw("Colz");
	min = NLLmuGlobalforqmu->GetMinimum();
	NLLmuGlobalforqmu->GetZaxis()->SetRangeUser(min-0.1, min+3);
	NLLmuGlobalforqmu->SetStats(false);
	NLLmuGlobalforqmu->GetZaxis()->SetLabelSize(0.024);
	NLLmuGlobalforqmu->GetZaxis()->SetLabelOffset(0.001);
	gPad->Update();
	NLLmuGlobalforqmu->Draw("Colz");

	c->cd(5);
	NLLmuFixedforqmu->Draw("Colz");
	NLLmuFixedforqmu->GetZaxis()->SetRangeUser(0.01,10000);
	NLLmuFixedforqmu->SetStats(false);
	NLLmuFixedforqmu->GetZaxis()->SetLabelSize(0.024);
	NLLmuFixedforqmu->GetZaxis()->SetLabelOffset(0.001);
	gPad->SetLogz();
	gPad->Update();
	NLLmuFixedforqmu->Draw("Colz");

	c->cd(6);
	deltaNLLforqmu->Draw("Colz");
	deltaNLLforqmu->GetZaxis()->SetRangeUser(0.001,10000);
	deltaNLLforqmu->SetStats(false);
	gPad->SetLogz();
	gPad->Update();
	deltaNLLforqmu->Draw("Colz");
	
	const char* plotnamec = (char*) ("deltaNLL"+as+".pdf").c_str();
	c->SaveAs(plotnamec);
	
	d->Divide(2,2);

	d->cd(1);
	NLLdiff->Draw();
	d->cd(2);
	rNLLdiff->Draw();
	d->cd(3);
	NLLdiff2D->SetStats(false);
	NLLdiff2D->Draw("Colz");
	d->cd(4);
	rNLLdiff2D->SetStats(false);
	rNLLdiff2D->GetZaxis()->SetRangeUser(-0.2, 1);
	rNLLdiff2D->Draw("Colz");
	
	const char* plotnamed = (char*) ("NLLdiff"+as+".pdf").c_str();
	d->SaveAs(plotnamed);

	if(asimov)
	{
		TH2D* CLsHist2D = (TH2D*) File->Get("CLsHist2D");
		TH2D* CLshistNLL = (TH2D*) File->Get("CLshistNLL");
		TCanvas* e = new TCanvas("e", "e", 1300, 700);
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
