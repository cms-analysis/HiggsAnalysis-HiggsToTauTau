/*void hist2Dbaseplot(TH2D* hist, const char* titlename, double zmin, double zmax, bool log=false, const char* ztitle="", double textsize=0.12, Color_t latexcolor=1){

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

	}*/

void hist2Dbaseplot(TCanvas* c, TH2D* hist, const char* titlename, double zmin, double zmax, bool log=false, const char* ztitle="", double textsize=0.12, Color_t latexcolor=1){  
  //TCanvas* c = new TCanvas("c", "c", 600,600);
	//SetStyle();

	// c->SetRightMargin(0.23);
// 	c->SetLeftMargin(0.1);
// 	c->SetTopMargin(0.05);
	
	c->SetFillColor      (0);
	c->SetBorderMode     (0);
	c->SetBorderSize     (10);
	// Set margins to reasonable defaults
	c->SetLeftMargin     (0.14);
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

	//return c
	  //c->Print(std::string(name).append("_").append(reference).append(".png").c_str());
	  //c->Print(std::string(name).append("_").append(reference).append(".pdf").c_str());
} 


void clusterplot(TH2D* clusterhist, const char* titlename, double textsize=0.12, Color_t latexcolor=1){
	gPad->SetRightMargin(0.20);
	gPad->SetTopMargin(0.05);
	clusterhist->Draw("Colz");
	clusterhist->SetStats(false);
	clusterhist->GetXaxis()->SetTitleSize(0.05);
	clusterhist->GetYaxis()->SetTitleSize(0.05);
	clusterhist->GetZaxis()->SetTitleSize(0.05);
	clusterhist->GetZaxis()->SetLabelSize(0.05);
	clusterhist->GetZaxis()->SetTitleOffset(1.1);
	clusterhist->GetZaxis()->SetRangeUser(0.,7.);

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

	TLatex* histtitle = new TLatex(120, 63, titlename);
	histtitle->SetTextColor(latexcolor);
	histtitle->SetTextSize(textsize);
	histtitle->Draw("Same");
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
	std::cout << filename << " " << xsfilename << std::endl;
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

	TH2D* mdiffAh = (TH2D*) XsFile->Get("massDiffAh");
	TH2D* mdiffAH = (TH2D*) XsFile->Get("massDiffAH");
	TH2D* mdiffHh = (TH2D*) XsFile->Get("massDiffHh");

	TH2D* mdiffhrefA = (TH2D*) XsFile->Get("massDiffhrefA");
	TH2D* mdiffHrefA = (TH2D*) XsFile->Get("massDiffHrefA");
	TH2D* mdiffhrefH = (TH2D*) XsFile->Get("massDiffhrefH");
	TH2D* mdiffArefH = (TH2D*) XsFile->Get("massDiffArefH");
	TH2D* mdiffArefh = (TH2D*) XsFile->Get("massDiffArefh");
	TH2D* mdiffHrefh = (TH2D*) XsFile->Get("massDiffHrefh");

	TH2D* ggcmb = (TH2D*) XsFile->Get("ggcmb");
	TH2D* bbcmb = (TH2D*) XsFile->Get("bbcmb");

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



	///_______

	TCanvas* c1 = new TCanvas("c1", "c1", 600, 600);
	TMultiGraph* gc1 =  exclusionObserved(hist1);
	hist2Dbaseplot(c1, hist1, "", 0,1, false, "CL_{s}");
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
	c1->Print("mia_CLs_obs.png");
	c1->Print("mia_CLs_obs.pdf");

	TCanvas* c2 = new TCanvas("c2", "c2", 600, 600);
	TMultiGraph* gc2 = new TMultiGraph();
	gc2 = exclusionObserved(hist5, 2, forbiddenRegionLevel);
	gc2->SetName("forbiddenRegion");
	TList* gc2list = gc2->GetListOfGraphs();
	for(int i=0;i<gc2list->GetSize();i++)
	{
	  std::cout << i << " " << ((TGraph*)gc2list->At(i))->GetX()[((TGraph*)gc2list->At(i))->GetN()-1] << " " << ((TGraph*)gc2list->At(i))->GetX()[0] << " " << ((TGraph*)gc2list->At(i))->GetY()[((TGraph*)gc2list->At(i))->GetN()-1] << " " << ((TGraph*)gc2list->At(i))->GetY()[0] << std::endl; 

	  //0 95 746.664 19.729 60.5

	  //  ende 95/19.729
	  //  anfang 746.664/60.5
	   
	  int zahl = ((TGraph*)gc2list->At(i))->GetN()-1;
	  ((TGraph*)gc2list->At(i))->SetFillColor(kGray);
	  ((TGraph*)gc2list->At(i))->SetLineColor(kGray);
	  ((TGraph*)gc2list->At(i))->SetLineWidth(-16003);
	  ((TGraph*)gc2list->At(i))->SetFillStyle(3005);
	  //((TGraph*)gc2list->At(i))->SetPoint( ((TGraph*)gc2list->At(i))->GetN(), 89, ((TGraph*)gc2list->At(i))->GetX()[((TGraph*)gc2list->At(i))->GetN()-1] );
	  //((TGraph*)gc2list->At(i))->SetPoint( ((TGraph*)gc2list->At(i))->GetN()+1, 89, 65);
	  //((TGraph*)gc2list->At(i))->SetPoint( ((TGraph*)gc2list->At(i))->GetN()+2, ((TGraph*)gc2list->At(i))->GetX()[0], 65);
	  //((TGraph*)gc2list->At(i))->SetPoint( ((TGraph*)gc2list->At(i))->GetN()+3, ((TGraph*)gc2list->At(i))->GetX()[0], ((TGraph*)gc2list->At(i))->GetY()[0]);
	  //((TGraph*)gc2list->At(i))->SaveAs("graph.root");
	}
	hist2Dbaseplot(c2, hist2, "",0.01,10000,true,"q_{#mu}",0.12,kGray);
	gc2->Draw("C");
	gPad->Update();
	c2->Print("mia_qMu.png");
	c2->Print("mia_qMu.pdf");

	TCanvas* c3 = new TCanvas("c3", "c3", 600, 600);
	hist2Dbaseplot(c3, hist3, "",0.01,10000,true,"q_{A}",0.12,kGray);
	gc2->Draw("C");
	gPad->Update();
	c3->Print("mia_qA.png");
	c3->Print("mia_qA.pdf");

	TCanvas* c4 = new TCanvas("c4", "c4", 600, 600);
	TMultiGraph* gc4 =  exclusionObserved(hist4);
	hist2Dbaseplot(c4, hist4, "", 0,1, false, "CL_{s}");
	gc4->Draw("C");
	L->Draw("Same");
	gPad->Update();
	c4->Print("mda_CLs_obs.png");
	c4->Print("mda_CLs_obs.pdf");

	TCanvas* c5 = new TCanvas("c5", "c5", 600, 600);
	hist2Dbaseplot(c5, hist5, "", 0.01,10000,true, "q_{#mu}");
	gc2->Draw("C");
	gPad->Update();
	c5->Print("mda_qMu.png");
	c5->Print("mda_qMu.pdf");

	TCanvas* c6 = new TCanvas("c6", "c6", 600, 600);
	hist2Dbaseplot(c6, hist6, "", 0.01,10000,true,"q_{A}");
	gc2->Draw("C");
	gPad->Update();
	c6->Print("mda_qA.png");
	c6->Print("mda_qA.pdf");


	///-----------------------------
	TCanvas* a1 = new TCanvas("a1", "a1", 600, 600);
	hist2Dbaseplot(a1, Xshist1, "",0.000001,300,true,"#sigma#font[42]{(ggA)}#upoint#font[52]{B}#font[42]{(A#rightarrow#tau#tau)} [pb]");
	a1->Print("ggA.png");
	a1->Print("ggA.pdf");

	TCanvas* a2 = new TCanvas("a2", "a2", 600, 600);
	hist2Dbaseplot(a2, Xshist2, "",0.000001,300,true,"#sigma#font[42]{(ggH)}#upoint#font[52]{B}#font[42]{(H#rightarrow#tau#tau)} [pb]");
	a2->Print("ggH.png");
	a2->Print("ggH.pdf");

	TCanvas* a3 = new TCanvas("a3", "a3", 600, 600);
	hist2Dbaseplot(a3, Xshist3, "",0.000001,300,true,"#sigma#font[42]{(ggh)}#upoint#font[52]{B}#font[42]{(h#rightarrow#tau#tau)} [pb]");
	a3->Print("ggh.png");
	a3->Print("ggh.pdf");

	TCanvas* a4 = new TCanvas("a4", "a4", 600, 600);
	hist2Dbaseplot(a4, Xshist4, "",0.000001,300,true,"#sigma#font[42]{(bbA)}#upoint#font[52]{B}#font[42]{(A#rightarrow#tau#tau)} [pb]");
	a4->Print("bbH.png");
	a4->Print("bbH.pdf");

	TCanvas* a5 = new TCanvas("a5", "a5", 600, 600);
	hist2Dbaseplot(a5, Xshist5, "",0.000001,300,true,"#sigma#font[42]{(bbH)}#upoint#font[52]{B}#font[42]{(H#rightarrow#tau#tau)} [pb]");
	a5->Print("bbH.png");
	a5->Print("bbH.pdf");

	TCanvas* a6 = new TCanvas("a6", "a6", 600, 600);
	hist2Dbaseplot(a6, Xshist6, "",0.000001,300,true,"#sigma#font[42]{(bbh)}#upoint#font[52]{B}#font[42]{(h#rightarrow#tau#tau)} [pb]");
	a6->Print("bbh.png");
	a6->Print("bbh.pdf");

	///-----------------------------

	TCanvas* d1 = new TCanvas("d1","d1", 600, 600);
	hist2Dbaseplot(d1, ggcmb, "",0.000001,450,true,"#sigma#font[42]{(gg#phi)}#upoint#font[52]{B}#font[42]{(#phi#rightarrow#tau#tau)} [pb]");
	d1->Print("ggPhi.png");
	d1->Print("ggPhi.pdf");

	TCanvas* d2 = new TCanvas("d2","d2", 600, 600);
	hist2Dbaseplot(d2, bbcmb, "",0.000001,450,true,"#sigma#font[42]{(bb#phi)}#upoint#font[52]{B}#font[42]{(#phi#rightarrow#tau#tau)} [pb]");
	d2->Print("bbPhi.png");
	d2->Print("bbPhi.pdf");

	///-----------------------------

	TCanvas* b1 = new TCanvas("b1", "b1", 600, 600);
	hist2Dbaseplot(b1, mdiffAh, "",0,1,false,"|m_{A}-m_{h}|/max(m_{A},m_{h})",0.08,kGray+2);
	b1->Print("m_diffmaxAh.png");
	b1->Print("m_diffmaxAh.pdf");

	TCanvas* b2 = new TCanvas("b2", "b2", 600, 600);
	hist2Dbaseplot(b2, mdiffAH, "",0,1,false,"|m_{A}-m_{H}|/max(m_{A},m_{H})",0.08,kGray);
	b2->Print("m_diffmaxAH.png");
	b2->Print("m_diffmaxAH.pdf");

        TCanvas* b3 = new TCanvas("b3", "b3", 600, 600);
	hist2Dbaseplot(b3, mdiffHh, "",0,1,false,"|m_{H}-m_{h}|/max(m_{H},m_{h})",0.08,kGray+2);
	b3->Print("m_diffmaxHh.png");
	b3->Print("m_diffmaxHh.pdf");

	///-----------------------------

	TCanvas* e1 = new TCanvas("e1", "e1", 600,600);
	hist2Dbaseplot(e1, mdiffhrefA, "",0,1,false,"|m_{A}-m_{h}|/(m_{A}",0.12,kGray+2);
	b3->Print("m_diffhrefA.png");
	b3->Print("m_diffhrefA.pdf");

	TCanvas* e2 = new TCanvas("e2", "e2", 600,600);
	hist2Dbaseplot(e2, mdiffHrefA, "",0,1,false,"|m_{A}-m_{H}|/m_{A}",0.12,kGray);
	b3->Print("m_diffHrefA.png");
	b3->Print("m_diffHrefA.pdf");

	TCanvas* e3 = new TCanvas("e3", "e3", 600,600);
	hist2Dbaseplot(e3, mdiffhrefH, "",0,1,false,"|m_{H}-m_{h}|/m_{H}",0.12,kGray+2);
	b3->Print("m_diffhrefH.png");
	b3->Print("m_diffhrefH.pdf");

	TCanvas* e4 = new TCanvas("e4", "e4", 600,600);
	hist2Dbaseplot(e4, mdiffArefH, "",0,1,false,"|m_{H}-m_{A}|/m_{H}",0.12,kGray);
	b3->Print("m_diffArefH.png");
	b3->Print("m_diffArefH.pdf");

	TCanvas* e5 = new TCanvas("e5", "e5", 600,600);
	hist2Dbaseplot(e5, mdiffArefh, "",0,1,false,"|m_{h}-m_{A}|/m_{h}",0.12,kGray+1);
	b3->Print("m_diffArefh.png");
	b3->Print("m_diffArefh.pdf");

	TCanvas* e6 = new TCanvas("e6", "e6", 600,600);
	hist2Dbaseplot(e6, mdiffHrefh, "",0,1,false,"|m_{h}-m_{H}|/m_{h}",0.12,kGray+1);
	b3->Print("m_diffHrefh.png");
	b3->Print("m_diffHrefh.pdf");

	///-----------------------------

	int massBins = hist1->GetNbinsX();
	int tanbBins = hist1->GetNbinsY();

	for(int i=0;i<=massBins; i++)
	{
		for(int j=0;j<=tanbBins;j++)
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

	TCanvas* f1 = new TCanvas("f1","f1", 600, 600);
	gPad->SetLeftMargin(0.15);
	gPad->SetTopMargin(0.01);
	gPad->SetRightMargin(0.05);
	CLsdiff->Draw();
	CLsdiff->SetStats(false);
	CLsdiff->GetXaxis()->SetTitleSize(0.045);
	CLsdiff->GetYaxis()->SetTitleOffset(2);
	gPad->Update();
	f1->Print("CLsDiff.pdf");
	f1->Print("CLsDiff.png");

	TCanvas* f2 = new TCanvas("f2","f2", 600, 600);
	gPad->SetLeftMargin(0.15);
	gPad->SetTopMargin(0.01);
	gPad->SetRightMargin(0.05);
	qmudiff->Draw();
	qmudiff->SetStats(false);
	qmudiff->GetXaxis()->SetTitleSize(0.045);
	qmudiff->GetYaxis()->SetTitleOffset(2);
	gPad->Update();
	f2->Print("qMuDiff.pdf");
	f2->Print("qMuDiff.png");

	TCanvas* f3 = new TCanvas("f3","f3", 600, 600);
	gPad->SetLeftMargin(0.15);
	gPad->SetTopMargin(0.01);
	gPad->SetRightMargin(0.05);
	qAdiff->Draw();
	qAdiff->SetStats(false);
	qAdiff->GetXaxis()->SetTitleSize(0.045);
	qAdiff->GetYaxis()->SetTitleOffset(2);
	gPad->Update();
	f3->Print("qADiff.pdf");
	f3->Print("qADiff.png");

	///-----------------------------

	TCanvas* g1 = new TCanvas("g1", "g1", 600, 600);
	double min = globalNLLhist->GetMinimum();
	double max = globalNLLhist->GetMaximum();
	double delta = max - min;
	//globalNLLhist->GetZaxis()->SetLabelSize(0.035);
	hist2Dbaseplot(g1, globalNLLhist, "NLL^{glob}",min, min + delta*1.01,false,"",0.06);//,kGray+1);
	g1->Print("mia_NLLglob.pdf");
	g1->Print("mia_NLLglob.png");
	
	TCanvas* g2 = new TCanvas("g2", "g2", 600, 600);
	//deltaNLLhist->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(g2, deltaNLLhist, "#DeltaNLL",0.001,10000,true,"",0.06);//,kGray+2);
	g2->Print("mia_DeltaNLL.pdf");
	g2->Print("mia_DeltaNLL.png");

	TCanvas* g3 = new TCanvas("g3", "g3", 600, 600);
	//fullNLLhist->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(g3, fullNLLhist, "full NLL",0.01,10000,true,"",0.06);//,kGray+2);
	g3->Print("mia_fullNLL.pdf");
	g3->Print("mia_fullNLL.png");

	TCanvas* g4 = new TCanvas("g4", "g4", 600, 600);
	//NLLmuGlobalforqmu->GetZaxis()->SetLabelSize(0.035);
	hist2Dbaseplot(g4, NLLmuGlobalforqmu, "NLL^{glob}",min, min + delta*1.01,false,"",0.06);//, kGray+1);
	g4->Print("mda_NLLglob.pdf");
	g4->Print("mda_NLLglob.png");

	TCanvas* g5 = new TCanvas("g5", "g5", 600, 600);
	//deltaNLLforqmu->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(g5, deltaNLLforqmu, "#DeltaNLL",0.001,10000,true,"",0.06);// ,kGray+2);
	g5->Print("mda_DeltaNLL.pdf");
	g5->Print("mda_DeltaNLL.png");

	TCanvas* g6 = new TCanvas("g6", "g6", 600, 600);
	//NLLmuFixedforqmu->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(g6, NLLmuFixedforqmu, "full NLL",0.01,10000,true,"",0.06);//kGray+2);
	g6->Print("mda_fullNLL.pdf");
	g6->Print("mda_fullNLL.png");

	///-----------------------------

	int mAbins = fullNLLhist->GetNbinsX();
	int tanbbins = fullNLLhist->GetNbinsY();
	for(int i=0;i<=mAbins;i++)
	{
		for(int j=0;j<=tanbbins;j++)
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

	TCanvas* h1 = new TCanvas("h1", "h1", 600, 600);
	gPad->SetRightMargin(0.20);
	gPad->SetTopMargin(0.05);
	NLLdiff->Draw();
	NLLdiff->SetStats(false);
	NLLdiff->GetXaxis()->SetTitleSize(0.05);
	gPad->Update();
	h1->Print("NLLdiff.pdf");
	h1->Print("NLLdiff.png");

	TCanvas* h2 = new TCanvas("h2", "h2", 600, 600);
	gPad->SetRightMargin(0.20);
	gPad->SetTopMargin(0.05);
	rNLLdiff->Draw();
	rNLLdiff->SetStats(false);
	rNLLdiff->GetXaxis()->SetTitleSize(0.05);
	gPad->Update();
	h2->Print("rNLLdiff.pdf");
	h2->Print("rNLLdiff.png");

	TCanvas* h3 = new TCanvas("h3", "h3", 600, 600);
	NLLdiff2D->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(h3, NLLdiff2D,"NLL_{mia}-NLL_{mda}",-6,6,false,"",0.06);
	h2->Print("NLLdiff_mia-mda.pdf");
	h2->Print("NLLdiff_mia-mda.png");

	TCanvas* h4 = new TCanvas("h4", "h4", 600, 600);
	rNLLdiff2D->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(h4, rNLLdiff2D,"NLL_{mia}-NLL_{mda}/NLL_{mda}",-0.3,0.3,false,"",0.06);
	h2->Print("NLLdiff_mia-mda_ref_mda.pdf");
	h2->Print("NLLdiff_mia-mda_ref_mda.png");

	///-----------------------------
	

	TH2D* CLsbHist2D = (TH2D*) File->Get("CLsbHist2D_as");
	TH2D* CLsbhistNLL = (TH2D*) File->Get("CLsbhistNLL");

	TCanvas* i1 = new TCanvas("i1", "i1", 600, 600);
	TMultiGraph* excl2D = new TMultiGraph();
	excl2D = exclusionObserved(CLsbHist2D);
	hist2Dbaseplot(i1, CLsbHist2D, "",0,1,false,"CL_{s+b}",0.06);
	excl2D->Draw("C");
	gPad->Update();
	i1->Print("CLsbHist2D_mia.pdf");
	i1->Print("CLsbHist2D_mia.png");

	TCanvas* i2 = new TCanvas("i2", "i2", 600, 600);
	CLsbhistNLL->Draw("Colz");
	TMultiGraph* exclNLL = new TMultiGraph();
	exclNLL = exclusionObserved(CLsbhistNLL);
	hist2Dbaseplot(i2, CLsbhistNLL, "",0,1,false,"CL_{s+b}",0.06);
	exclNLL->Draw("C");
	gPad->Update();
	i2->Print("CLsbhistNLL_mda.pdf");
	i2->Print("CLsbhistNLL_mda.png");
	
	TCanvas* i3 = new TCanvas("i3", "i3", 600, 600);
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
	i1->Print("CLsbComparison.pdf");
	i1->Print("CLsbComparison.png");

	if(!higgsBounds)
	{
		TCanvas* j1 = new TCanvas("j1","j1", 600, 600);
		deltaNLLhist_heavy->GetZaxis()->SetLabelSize(0.05);
		hist2Dbaseplot(j1, deltaNLLhist_heavy, "#DeltaNLL_{heavy}",0.001,10000,true,"",0.06,kBlack);
		j1->Print("DeltaNLL_heavy.pdf");
		j1->Print("DeltaNLL_heavy.pdf");

		TCanvas* j2 = new TCanvas("j2","j2", 600, 600);
		deltaNLLhist_light->GetZaxis()->SetLabelSize(0.05);
		hist2Dbaseplot(j2, deltaNLLhist_light, "#DeltaNLL_{light}",0.001,10000,true,"",0.06,kBlack);
		j2->Print("DeltaNLL_light.pdf");
		j2->Print("DeltaNLL_light.pdf");
	}
	else
	{
		TH2D* combinedCluster = (TH2D*) File->Get("combinedCluster");
		TH2D* combinedClusterMass = (TH2D*) File->Get("combinedClusterMass");
		TH2D* deltaNLLhistA = (TH2D*) File->Get("deltaNLLhistA");
		TH2D* deltaNLLhistH = (TH2D*) File->Get("deltaNLLhistH");
		TH2D* deltaNLLhisth = (TH2D*) File->Get("deltaNLLhisth");

		TCanvas* k1 = new TCanvas("k1","k1", 600, 600);
		hist2Dbaseplot(k1, combinedClusterMass, "m_{cluster}^{combined}",50,1000,true,"[GeV]",0.06,kBlack);
		k1->Print("HB_combinedCluster_mass.pdf");
		k1->Print("HB_combinedCluster_mass.png");

		TCanvas* k2 = new TCanvas("k2","k2", 600, 600);
		clusterplot(k2, combinedCluster, "cluster(comb)",0.06);
		k2->Print("HB_combinedCluster_higgs.pdf");
		k2->Print("HB_combinedCluster_higgs.png");

		TCanvas* k3 = new TCanvas("k3","k3", 600, 600);
		deltaNLLhistA->GetZaxis()->SetLabelSize(0.05);
		hist2Dbaseplot(k3, deltaNLLhistA, "#DeltaNLL_{cluster(A)}",0.001,10000,true,"",0.06,kBlack);
		k3->Print("HB_DeltaNLL_A.pdf");
		k3->Print("HB_DeltaNLL_A.png");

		TCanvas* k4 = new TCanvas("k4","k4", 600, 600);
		deltaNLLhistH->GetZaxis()->SetLabelSize(0.05);
		hist2Dbaseplot(k4, deltaNLLhistH, "#DeltaNLL_{cluster(H)}",0.001,10000,true,"",0.06,kBlack);
		k4->Print("HB_DeltaNLL_H.pdf");
		k4->Print("HB_DeltaNLL_H.png");

		TCanvas* k5 = new TCanvas("k5","k5", 600, 600);
		deltaNLLhisth->GetZaxis()->SetLabelSize(0.05);
		hist2Dbaseplot(k5, deltaNLLhisth, "#DeltaNLL_{cluster(h)}",0.001,10000,true,"",0.06,kBlack);
		k5->Print("HB_DeltaNLL_h.pdf");
		k5->Print("HB_DeltaNLL_h.png");
	}

	File->WriteTObject(CLsdiff,"");
	File->WriteTObject(qAdiff,"");
	File->WriteTObject(qmudiff,"");
	File->WriteTObject(rNLLdiff,"");
	File->WriteTObject(NLLdiff,"");
	File->Close();
	XsFile->Close();
}
