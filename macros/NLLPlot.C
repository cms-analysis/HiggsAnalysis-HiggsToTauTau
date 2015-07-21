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

TMultiGraph* exclusionObserved(TH2D* hist, int color=1, double level=0.05)
{
	TH2D* hist_copy = new TH2D();
	hist->Copy(*hist_copy);
	Double_t contours[1];
	contours[0]=level;
	hist_copy->SetContour(1,contours);
	hist_copy->Draw("CONT LIST");
	hist_copy->SetLineWidth(2);
	gPad->Update();
   TObjArray *conts = (TObjArray*)gROOT->GetListOfSpecials()->FindObject("contours");
	TList* contLevel = (TList*) conts->At(0);
	TMultiGraph* contoursGraph = new TMultiGraph();
	for (int i=0; i<contLevel->GetSize(); i++)
	{
		TGraph* curve = (TGraph*)contLevel->At(i);
		curve->SetLineColor(color);
		contoursGraph->Add((TGraph*)curve->Clone());
	}
	return contoursGraph;
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

void NLLPlot(const char* filename="output.root", const char* xsfilename="$CMSSW_BASE/src/higgsContributions/higgsContribution.modelmhmodp.tolerance0.15.referenceA.contrhHA.root", double forbiddenRegionLevel = 100.0, bool higgsBounds)
{
	set_plot_style();

	TFile* File = new TFile(filename, "UPDATE");
	TFile* XsFile = new TFile(xsfilename, "UPDATE");

	// Extracting 2D histograms from root file
	TH2D* hist1 = (TH2D*) File->Get("CLsHist2D");
	TH2D* hist2 = (TH2D*) File->Get("qmuHist2D");
	TH2D* hist3 = (TH2D*) File->Get("qAHist2D");

	TH2D* hist4 = (TH2D*) File->Get("CLsHist2D_as");
	TH2D* hist5 = (TH2D*) File->Get("qmuHist2D_as");
	TH2D* hist6 = (TH2D*) File->Get("qAHist2D_as");

	TH2D* hist7 = (TH2D*) File->Get("CLsbHist2D");
	TH2D* hist8 = (TH2D*) File->Get("CLbHist2D");

	TH2D* hist9 = (TH2D*) File->Get("CLsbHist2D_as");
	TH2D* hist10 = (TH2D*) File->Get("CLbHist2D_as");

	TH2D* Xshist1 = (TH2D*) XsFile->Get("ggAXsBR");
	TH2D* Xshist2 = (TH2D*) XsFile->Get("ggHXsBR");
	TH2D* Xshist3 = (TH2D*) XsFile->Get("gghXsBR");

	TH2D* Xshist4 = (TH2D*) XsFile->Get("bbAXsBR");
	TH2D* Xshist5 = (TH2D*) XsFile->Get("bbHXsBR");
	TH2D* Xshist6 = (TH2D*) XsFile->Get("bbhXsBR");

	TH2D* mhist1 = (TH2D*) XsFile->Get("massDiff1");
	TH2D* mhist2 = (TH2D*) XsFile->Get("massDiff2");

	TH2D* ggcmb = (TH2D*) XsFile->Get("ggcmb");
	TH2D* bbcmb = (TH2D*) XsFile->Get("bbcmb");
	TH2D* cluster = (TH2D*) XsFile->Get("cluster");

	TH2D* globalNLLhist = (TH2D*) File->Get("globalNLLhist");
	TH2D* fullNLLhist = (TH2D*) File->Get("fullNLLhist");
	TH2D* deltaNLLhist = (TH2D*) File->Get("deltaNLLhist");
	TH2D* qmuHist2D = (TH2D*) File->Get("qmuHist2D");
	TH2D* NLLmuFixedforqmu = (TH2D*) File->Get("NLLmuFixedforqmu");
	TH2D* NLLmuGlobalforqmu = (TH2D*) File->Get("NLLmuGlobalforqmu");
	TH2D* deltaNLLforqmu = (TH2D*) File->Get("deltaNLLforqmu");
	TH2D* NLLdiff2D = (TH2D*) File->Get("NLLdiff2D");
	TH2D* rNLLdiff2D = (TH2D*) File->Get("rNLLdiff2D");

	TH2D* deltaNLLhist_heavy = (TH2D*) File->Get("deltaNLLhist_heavy");
	TH2D* deltaNLLhist_light = (TH2D*) File->Get("deltaNLLhist_light");

	TH1D* NLLdiff = new TH1D("NLLdiff", ";NLL_{mia} - NLL_{mda}",100, -6,6);
	TH1D* rNLLdiff = new TH1D("rNLLdiff", ";NLL_{mia} - NLL_{mda}/NLL_{mda}",100, -1.5,1.5);

	TH1D* CLsdiff = new TH1D("CLsdiff", ";CL_{s}^{own fit} - CL_{s}^{combine};Entries", 100, -0.1, 0.1);
	TH1D* qmudiff = new TH1D("qmudiff", ";q_{#mu}^{own fit} - q_{#mu}^{combine};Entries", 100, -10, 10);
	TH1D* qAdiff = new TH1D("qAdiff", ";q_{A}^{own fit} - q_{A}^{combine};Entries", 100, -10, 10);

	TCanvas* c1 = new TCanvas("c1", "c1", 1300, 700);
	c1->Divide(3,2);
	c1->cd(1);
	TMultiGraph* gc1 =  exclusionObserved(hist1);
	hist2Dbaseplot(hist1, "CL_{s}",0,1);
	gc1->Draw("C");
	TLegend* L = new TLegend(0.55,0.15,0.8,0.4);
	TLine* CLsObs = new TLine();
	CLsObs->SetLineColor(1);
	CLsObs->SetLineWidth(2);
	L->AddEntry(CLsObs,"CL_{s}^{obs}=0.05 ","l");
	L->SetFillStyle(0);
	L->SetBorderSize(0);
	L->Draw("Same");
	gPad->Update();

	c1->cd(2);
	TMultiGraph* gc2 = new TMultiGraph();
	gc2 = exclusionObserved(hist5, 2, forbiddenRegionLevel);
	gc2->SetName("forbiddenRegion");
	TList* gc2list = gc2->GetListOfGraphs();
	for(int i=0;i<gc2list->GetSize();i++)
	{
		((TGraph*)gc2list->At(i))->SetLineWidth(-603);
		((TGraph*)gc2list->At(i))->SetFillStyle(3005);
	}
	hist2Dbaseplot(hist2, "q_{#mu}",0.01,10000,true,"",0.12,kGray);
	gc2->Draw("C");
	gPad->Update();

	c1->cd(3);
	hist2Dbaseplot(hist3, "q_{A}",0.01,10000,true,"",0.12,kGray);
	gc2->Draw("C");
	gPad->Update();

	c1->cd(4);
	TMultiGraph* gc4 =  exclusionObserved(hist4);
	hist2Dbaseplot(hist4, "CL_{s}",0,1);
	gc4->Draw("C");
	L->Draw("Same");
	gPad->Update();

	c1->cd(5);
	hist2Dbaseplot(hist5, "q_{#mu}",0.01,10000,true);
	gc2->Draw("C");
	gPad->Update();

	c1->cd(6);
	hist2Dbaseplot(hist6, "q_{A}",0.01,10000,true);
	gc2->Draw("C");
	gPad->Update();

	c1->SaveAs("plotted2Dhistos.pdf");

	TCanvas* c2 = new TCanvas("c2", "c2", 1300, 700);
	c2->Divide(3,2);

	c2->cd(1);
	hist2Dbaseplot(Xshist1, "#sigma_{ggA}#upointBR_{A#rightarrow#tau#tau}",0.000001,300,true,"[pb]");

	c2->cd(2);
	hist2Dbaseplot(Xshist2, "#sigma_{ggH}#upointBR_{H#rightarrow#tau#tau}",0.000001,300,true,"[pb]");

	c2->cd(3);
	hist2Dbaseplot(Xshist3, "#sigma_{ggh}#upointBR_{h#rightarrow#tau#tau}",0.000001,300,true,"[pb]");

	c2->cd(4);
	hist2Dbaseplot(Xshist4, "#sigma_{bbA}#upointBR_{A#rightarrow#tau#tau}",0.000001,300,true,"[pb]");

	c2->cd(5);
	hist2Dbaseplot(Xshist5, "#sigma_{bbH}#upointBR_{H#rightarrow#tau#tau}",0.000001,300,true,"[pb]");

	c2->cd(6);
	hist2Dbaseplot(Xshist6, "#sigma_{bbh}#upointBR_{h#rightarrow#tau#tau}",0.000001,300,true,"[pb]");

	c2->SaveAs("plottedXsBr.pdf");

	TCanvas* d2 = new TCanvas("d2","d2", 866, 350);
	d2->Divide(2,1);

	d2->cd(1);
	hist2Dbaseplot(ggcmb, "#sigma_{gg#phi}#upointBR_{#phi#rightarrow#tau#tau}",0.000001,450,true,"[pb]");

	d2->cd(2);
	hist2Dbaseplot(bbcmb, "#sigma_{bb#phi}#upointBR_{#phi#rightarrow#tau#tau}",0.000001,450,true,"[pb]");

	d2->SaveAs("combinedXs.pdf");

	TCanvas* c3 = new TCanvas("c3", "c3", 1300,350);
	c3->Divide(3,1);

	c3->cd(1);
	hist2Dbaseplot(mhist1, "|m_{A}-m_{h}|/m_{A}",0,1,false,"",0.12,kGray+2);

	c3->cd(2);
	hist2Dbaseplot(mhist2, "|m_{A}-m_{H}|/m_{A}",0,1,false,"",0.12,kGray);

	c3->cd(3);
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

	c3->SaveAs("massDifferences.pdf");

	int massBins = hist1->GetNbinsX();
	int tanbBins = hist1->GetNbinsY();

	for(int i=1;i<=massBins; i++)
	{
		for(int j=1;j<=tanbBins;j++)
		{
			double CLsDifference = hist1->GetBinContent(i,j) - hist4->GetBinContent(i,j);
			double qmuDifference = hist2->GetBinContent(i,j) - hist5->GetBinContent(i,j);
			double qADifference = hist3->GetBinContent(i,j) - hist6->GetBinContent(i,j);
			
			CLsdiff->Fill(CLsDifference);
			
			if(qmuDifference>10) qmudiff->Fill(9);
			else if(qmuDifference<-10) qmudiff->Fill(-10);
			else qmudiff->Fill(qmuDifference);
			
			if(qADifference>10) qAdiff->Fill(9);
			else if(qADifference<-10) qAdiff->Fill(-10);
			else qAdiff->Fill(qADifference);
		}
	}
	TCanvas* d1 = new TCanvas("d1","d1", 1300, 500);
	d1->Divide(3,1);

	d1->cd(1);
	gPad->SetLeftMargin(0.15);
	gPad->SetTopMargin(0.01);
	gPad->SetRightMargin(0.05);
	CLsdiff->Draw();
	CLsdiff->SetStats(false);
	CLsdiff->GetXaxis()->SetTitleSize(0.045);
	CLsdiff->GetYaxis()->SetTitleOffset(2);
	gPad->Update();

	d1->cd(2);
	gPad->SetLeftMargin(0.15);
	gPad->SetTopMargin(0.01);
	gPad->SetRightMargin(0.05);
	qmudiff->Draw();
	qmudiff->SetStats(false);
	qmudiff->GetXaxis()->SetTitleSize(0.045);
	qmudiff->GetYaxis()->SetTitleOffset(2);
	gPad->Update();

	d1->cd(3);
	gPad->SetLeftMargin(0.15);
	gPad->SetTopMargin(0.01);
	gPad->SetRightMargin(0.05);
	qAdiff->Draw();
	qAdiff->SetStats(false);
	qAdiff->GetXaxis()->SetTitleSize(0.045);
	qAdiff->GetYaxis()->SetTitleOffset(2);
	gPad->Update();

	d1->SaveAs("quantitiesDifference.pdf");

	int mAbins = fullNLLhist->GetNbinsX();
	int tanbbins = fullNLLhist->GetNbinsY();
	for(int i=1;i<=mAbins;i++)
	{
		for(int j=1;j<=tanbbins;j++)
		{
			double diff = fullNLLhist->GetBinContent(i,j) - NLLmuFixedforqmu->GetBinContent(i,j);
			double rdiff = (fullNLLhist->GetBinContent(i,j) - NLLmuFixedforqmu->GetBinContent(i,j))/NLLmuFixedforqmu->GetBinContent(i,j);
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
		}
	}
	TCanvas* c = new TCanvas("c", "c", 1300, 700);
	c->Divide(3,2);

	c->cd(1);
	double min = globalNLLhist->GetMinimum();
	double max = globalNLLhist->GetMaximum();
	double delta = max - min;
	globalNLLhist->GetZaxis()->SetLabelSize(0.035);
	hist2Dbaseplot(globalNLLhist, "NLL^{glob}",min, min + delta*1.01,false,"",0.12,kGray+1);
	

	c->cd(2);
	deltaNLLhist->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(deltaNLLhist, "#DeltaNLL",0.001,10000,true,"",0.12,kGray+2);

	c->cd(3);
	fullNLLhist->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(fullNLLhist, "full NLL",0.01,10000,true,"",0.12,kGray+2);

	c->cd(4);
	NLLmuGlobalforqmu->GetZaxis()->SetLabelSize(0.035);
	hist2Dbaseplot(NLLmuGlobalforqmu, "NLL^{glob}",min, min + delta*1.01,false,"",0.12,kGray+1);


	c->cd(5);
	deltaNLLforqmu->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(deltaNLLforqmu, "#DeltaNLL",0.001,10000,true,"",0.12,kGray+2);

	c->cd(6);
	NLLmuFixedforqmu->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(NLLmuFixedforqmu, "full NLL",0.01,10000,true,"",0.12,kGray+2);
	
	c->SaveAs("deltaNLL.pdf");
	
	
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
	
	d->SaveAs("NLLdiff.pdf");


	
	TH2D* CLsbHist2D = (TH2D*) File->Get("CLsbHist2D_as");
	TH2D* CLsbhistNLL = (TH2D*) File->Get("CLsbhistNLL");
	TCanvas* e = new TCanvas("e", "e", 1300, 350);
	e->Divide(3,1);

	e->cd(1);
	TMultiGraph* excl2D = new TMultiGraph();
	excl2D = exclusionObserved(CLsbHist2D);
	hist2Dbaseplot(CLsbHist2D, "CL_{s+b}",0,1);;
	excl2D->Draw("C");
	gPad->Update();

	e->cd(2);
	CLsbhistNLL->Draw("Colz");
	TMultiGraph* exclNLL = new TMultiGraph();
	exclNLL = exclusionObserved(CLsbhistNLL);
	hist2Dbaseplot(CLsbhistNLL, "CL_{s+b}",0,1);
	exclNLL->Draw("C");
	gPad->Update();
	
	e->cd(3);
	gPad->SetRightMargin(0.20);
	gPad->SetTopMargin(0.05);
	TMultiGraph* excl2Dcompare = new TMultiGraph();
	TMultiGraph* exclNLLcompare = new TMultiGraph();
	TMultiGraph* CLscompare = new TMultiGraph();

	excl2Dcompare = exclusionObserved(CLsbHist2D,1);
	exclNLLcompare = exclusionObserved(CLsbhistNLL,2);
	CLscompare = exclusionObserved(hist4,3);

	excl2Dcompare->Draw("C");
	exclNLLcompare->Draw("C");
	CLscompare->Draw("C");

	TLegend* l = new TLegend(0.15,0.6,0.35,0.9);
	TLine* md = new TLine();
	md->SetLineColor(1);
	md->SetLineWidth(2);
	TLine* mi = new TLine();
	mi->SetLineColor(2);
	mi->SetLineWidth(2);
	TLine* cl = new TLine();
	cl->SetLineColor(3);
	cl->SetLineWidth(2);
	l->AddEntry(md, "CL_{s+b} mda","l");
	l->AddEntry(mi, "CL_{s+b} mia","l");
	l->AddEntry(cl, "CL_{s} mda","l");
	l->SetFillStyle(0);
	l->SetBorderSize(0);
	l->Draw("Same");
	gPad->Update();
	e->SaveAs("CLsbComparison.pdf");

	if(!higgsBounds)
	{
		TCanvas* f = new TCanvas("f","f", 866, 350);
		f->Divide(2,1);
		f->cd(1);
		deltaNLLhist_heavy->GetZaxis()->SetLabelSize(0.05);
		hist2Dbaseplot(deltaNLLhist_heavy, "#DeltaNLL_{heavy}",0.001,10000,true,"",0.12,kGray+2);
		f->cd(2);
		deltaNLLhist_light->GetZaxis()->SetLabelSize(0.05);
		hist2Dbaseplot(deltaNLLhist_light, "#DeltaNLL_{light}",0.001,10000,true,"",0.12,kGray+2);
		f->SaveAs("lightvsheavy.pdf");
	}
	else
	{
		TH2D* combinedCluster = (TH2D*) File->Get("combinedCluster");
		TH2D* combinedClusterMass = (TH2D*) File->Get("combinedClusterMass");
		TH2D* deltaNLLhistA = (TH2D*) File->Get("deltaNLLhistA");
		TH2D* deltaNLLhistH = (TH2D*) File->Get("deltaNLLhistH");
		TH2D* deltaNLLhisth = (TH2D*) File->Get("deltaNLLhisth");

		TCanvas* f = new TCanvas("f","f", 866, 350);
		f->Divide(2,1);
		f->cd(1);
		hist2Dbaseplot(combinedClusterMass, "m_{cluster}^{combined}",50,1000,true,"[GeV]");
		f->cd(2);
		gPad->SetRightMargin(0.20);
		gPad->SetTopMargin(0.05);
		combinedCluster->Draw("Colz");
		combinedCluster->SetStats(false);
		combinedCluster->GetXaxis()->SetTitleSize(0.05);
		combinedCluster->GetYaxis()->SetTitleSize(0.05);
		combinedCluster->GetZaxis()->SetTitleSize(0.05);
		combinedCluster->GetZaxis()->SetLabelSize(0.05);
		combinedCluster->GetZaxis()->SetTitleOffset(1.1);
		combinedCluster->GetZaxis()->SetRangeUser(0.,7.);

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
		f->SaveAs("combinedCluster.pdf");

		TCanvas* f1 = new TCanvas("f1","f1",1300,350);
		f1->Divide(3,1);
		f1->cd(1);
		deltaNLLhistA->GetZaxis()->SetLabelSize(0.05);
		hist2Dbaseplot(deltaNLLhistA, "#DeltaNLL_{cluster(A)}",0.001,10000,true,"",0.12,kGray+2);
		f1->cd(2);
		deltaNLLhistH->GetZaxis()->SetLabelSize(0.05);
		hist2Dbaseplot(deltaNLLhistH, "#DeltaNLL_{cluster(H)}",0.001,10000,true,"",0.12,kGray+2);
		f1->cd(3);
		deltaNLLhisth->GetZaxis()->SetLabelSize(0.05);
		hist2Dbaseplot(deltaNLLhisth, "#DeltaNLL_{cluster(h)}",0.001,10000,true,"",0.12,kGray+2);
		f1->SaveAs("higgsBoundsDeltaNLL.pdf");
	}

	File->WriteTObject(CLsdiff,"");
	File->WriteTObject(qAdiff,"");
	File->WriteTObject(qmudiff,"");
	File->WriteTObject(rNLLdiff,"");
	File->WriteTObject(NLLdiff,"");
	File->Close();
	XsFile->Close();
}
