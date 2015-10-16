

void hist1Dbaseplot(TCanvas* c, TH1D* hist){  
  	c->SetBottomMargin(0.15);
        c->SetRightMargin(0.20);
	c->SetTopMargin(0.05);
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
	hist->SetLineWidth(3);
	hist->Draw();
} 


void hist2Dbaseplot(TCanvas* c, TH2D* hist, const char* titlename, double zmin, double zmax, bool log=false, const char* ztitle="", double textsize=0.12, Color_t latexcolor=1){  

	c->SetFillColor      (0);
	c->SetBorderMode     (0);
	c->SetBorderSize     (10);
	// Set margins to reasonable defaults
	c->SetLeftMargin     (0.14);
	c->SetRightMargin    (0.20);
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

	hist->GetXaxis()->SetTitle("m_{A} [GeV]");
	hist->GetXaxis()->SetLabelFont(62);
	hist->GetXaxis()->SetLabelOffset(0.018);
	hist->GetXaxis()->SetTitleColor(1);
	hist->GetXaxis()->SetTitleOffset(1.05);
	hist->GetXaxis()->SetTitleFont(62);
	hist->GetXaxis()->SetTitleSize(0.055);

	hist->GetYaxis()->SetTitle("tan#beta");
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
} 


void clusterplot(TH2D* clusterhist, const char* titlename, double textsize=0.12, Color_t latexcolor=1){
  	gPad->SetFillColor      (0);
	gPad->SetBorderMode     (0);
	gPad->SetBorderSize     (10);
	// Set margins to reasonable defaults
	gPad->SetLeftMargin     (0.14);
	//gPad->SetRightMargin    (0.20);
	//gPad->SetTopMargin      (0.08);
	gPad->SetBottomMargin   (0.13);

	clusterhist->Draw("Col");
	clusterhist->SetStats(false);
	clusterhist->GetXaxis()->SetTitle("m_{A} [GeV]");
	clusterhist->GetXaxis()->SetLabelFont(62);
	clusterhist->GetXaxis()->SetLabelOffset(0.018);
	clusterhist->GetXaxis()->SetTitleColor(1);
	clusterhist->GetXaxis()->SetTitleOffset(1.05);
	clusterhist->GetXaxis()->SetTitleFont(62);
	clusterhist->GetXaxis()->SetTitleSize(0.055);

	clusterhist->GetYaxis()->SetTitle("tan#beta");
	clusterhist->GetYaxis()->SetLabelFont(62);
	clusterhist->GetYaxis()->SetLabelOffset(0.023);
	clusterhist->GetYaxis()->SetTitleSize(0.055);
	clusterhist->GetYaxis()->SetTitleOffset(1.15);
	clusterhist->GetYaxis()->SetTitleFont(62);
	clusterhist->GetYaxis()->SetLabelSize(0.04);

	clusterhist->GetZaxis()->SetTitleSize(0.05);
	clusterhist->GetZaxis()->SetLabelSize(0.05);
	clusterhist->GetZaxis()->SetTitleOffset(1.1);
	clusterhist->GetZaxis()->SetRangeUser(0.,7.);

	//Int_t colors[] = {0, 1, 2, 3, 4, 5, 6, 7}; // #colors >= #levels - 1
	Int_t colors[] = {0, kRed+3, 2, 3, 4, kOrange+1, 8, 7};
	gStyle->SetPalette((sizeof(colors)/sizeof(Int_t)), colors);

	TH2D* h = new TH2D();
	h->SetFillColor(kRed+3);
	TH2D* H = new TH2D();
	H->SetFillColor(2);
	// TH2D* h_H = new TH2D();
// 	h_H->SetFillColor(kBlue);
	TH2D* A = new TH2D();
	A->SetFillColor(4);
	TH2D* h_A = new TH2D();
	h_A->SetFillColor(kOrange+1);
	TH2D* H_A = new TH2D();
	H_A->SetFillColor(8);
	TH2D* h_H_A = new TH2D();
	h_H_A->SetFillColor(7);
	
	TLegend* leg2 = new TLegend(0.15, 0.57, 0.35, 0.88);
	leg2->SetBorderSize( 0  );
	leg2->SetFillStyle (1001);
	leg2->SetTextSize  (0.03);
	leg2->SetTextFont  ( 62 ); 
	leg2->SetFillColor (kWhite);
	leg2->SetLineWidth (2);
	leg2->SetLineColor (kBlack);
	leg2->SetHeader("Contributions:");
	leg2->AddEntry(h,"h","F");
	leg2->AddEntry(H,"H","F");
	leg2->AddEntry(A,"A","F");
	leg2->AddEntry(h_A,"h+A","F");
	leg2->AddEntry(H_A,"A+H","F");
	leg2->AddEntry(h_H_A,"h+A+H","F");
	leg2->Draw("same");
	 
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
	hist_copy->SetLineWidth(3);
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

	//mia
	TH2D* globalNLLhist = (TH2D*) File->Get("globalNLLhist");
	TH2D* fullNLLhist = (TH2D*) File->Get("fullNLLhist");
	TH2D* deltaNLLhist = (TH2D*) File->Get("deltaNLLhist");

	///mda
	TH2D* qmuHist2D = (TH2D*) File->Get("qmuHist2D");
	TH2D* NLLmuFixedforqmu = (TH2D*) File->Get("NLLmuFixedforqmu");
	TH2D* NLLmuGlobalforqmu = (TH2D*) File->Get("NLLmuGlobalforqmu");
	TH2D* deltaNLLforqmu = (TH2D*) File->Get("deltaNLLforqmu");

	//TH2D* NLLdiff2D = (TH2D*) File->Get("NLLdiff2D");
	//TH2D* rNLLdiff2D = (TH2D*) File->Get("rNLLdiff2D");

	//mda
	TH2D* fullNLLdiff2D = (TH2D*) File->Get("deltaNLLhist")->Clone();
	TH2D* rfullNLLdiff2D = (TH2D*) File->Get("fullNLLhist")->Clone();
	TH2D* deltaNLLdiff2D = (TH2D*) File->Get("globalNLLhist")->Clone();
	TH2D* rdeltaNLLdiff2D = (TH2D*) File->Get("deltaNLLforqmu")->Clone();

	TH2D* deltaNLLhist_heavy = (TH2D*) File->Get("deltaNLLhist_heavy");
	TH2D* deltaNLLhist_light = (TH2D*) File->Get("deltaNLLhist_light");

	//mia
	TH1D* fullNLLdiff = new TH1D("fullNLLdiff", ";NLL_{re} - NLL_{di}",100, -10,10);
	TH1D* rfullNLLdiff = new TH1D("rfullNLLdiff", ";(NLL_{re} - NLL_{di})/NLL_{di}",100, -1.0,1.0);
	TH1D* deltaNLLdiff = new TH1D("deltaNLLdiff", ";NLL_{re} - NLL_{di}",100, -10,10);
	TH1D* rdeltaNLLdiff = new TH1D("rdeltaNLLdiff", ";(NLL_{re} - NLL_{di})/NLL_{di}",100, -1.0,1.0);

	TH1D* CLsdiff = new TH1D("CLsdiff", ";CL_{s}^{own fit} - CL_{s}^{combine};Entries", 100, -0.1, 0.1);
	TH1D* qmudiff = new TH1D("qmudiff", ";q_{#mu}^{own fit} - q_{#mu}^{combine};Entries", 100, -10, 10);
	TH1D* qAdiff = new TH1D("qAdiff", ";q_{A}^{own fit} - q_{A}^{combine};Entries", 100, -10, 10);



	///_______

	TCanvas* c1 = new TCanvas("c1", "c1", 600, 600);
	TMultiGraph* gc1 =  exclusionObserved(hist1);
	hist2Dbaseplot(c1, hist1, "", 0,1, false, "CL_{s}",0.06);
	for(int i=0;i<=hist1->GetNbinsX();i++){
	  for(int j=0;j<=hist1->GetNbinsY();j++){
	    if(hist1->GetBinContent(i,j)<=0) hist1->SetBinContent(i,j,0.001);
	  }
	}
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
	c1->Print("mda_combine_CLs_obs.png");
	c1->Print("mda_combine_CLs_obs.pdf");

	TCanvas* c2 = new TCanvas("c2", "c2", 600, 600);
	TMultiGraph* gc2 = new TMultiGraph();
	gc2 = exclusionObserved(hist5, 2, forbiddenRegionLevel);
	gc2->SetName("forbiddenRegion");
	TList* gc2list = gc2->GetListOfGraphs();
	for(int i=0;i<gc2list->GetSize();i++)
	{
	  for(int j=0;j<((TGraph*)gc2list->At(i))->GetN();j++){
	    ((TGraph*)gc2list->At(i))->SetPoint( j, ((TGraph*)gc2list->At(i))->GetX()[j], ((TGraph*)gc2list->At(i))->GetY()[j]-0.5 );
	  }

	  ((TGraph*)gc2list->At(i))->SetFillColor(kGray);
	  ((TGraph*)gc2list->At(i))->SetLineColor(kGray);
	  ((TGraph*)gc2list->At(i))->SetLineWidth(3);
	  ((TGraph*)gc2list->At(i))->SetFillStyle(1001);
	  ((TGraph*)gc2list->At(i))->SetPoint( ((TGraph*)gc2list->At(i))->GetN(), 89, ((TGraph*)gc2list->At(i))->GetY()[((TGraph*)gc2list->At(i))->GetN()-1] );
	  ((TGraph*)gc2list->At(i))->SetPoint( ((TGraph*)gc2list->At(i))->GetN(), 89, 80);
	  ((TGraph*)gc2list->At(i))->SetPoint( ((TGraph*)gc2list->At(i))->GetN(), ((TGraph*)gc2list->At(i))->GetX()[0], 80);
	  ((TGraph*)gc2list->At(i))->SetPoint( ((TGraph*)gc2list->At(i))->GetN(), ((TGraph*)gc2list->At(i))->GetX()[0], ((TGraph*)gc2list->At(i))->GetY()[0]);
	  //((TGraph*)gc2list->At(i))->SaveAs("graph.root");
	}
	TGraph * outer2= (TGraph*)gc2list->At(0)->Clone();
	outer2->SetLineWidth(3);
	outer2->SetLineColor(kGray+2);
	TGraph * outer= (TGraph*)gc2list->At(0)->Clone();
	outer->SetFillStyle(3005);
	outer->SetFillColor(kGray+2);
	hist2Dbaseplot(c2, hist2, "",0.001,10000,true,"q_{#mu}",0.06);
	gc2->Draw("CF");
	outer->Draw("CFsame");
	outer2->Draw("Csame");
	gPad->RedrawAxis();
	gPad->Update();
	c2->Print("mda_combine_qMu.png");
	c2->Print("mda_combine_qMu.pdf");

	TCanvas* c3 = new TCanvas("c3", "c3", 600, 600);
	hist2Dbaseplot(c3, hist3, "",0.001,10000,true,"q_{A}",0.06);
	gc2->Draw("CF");
	outer->Draw("CFsame");
	outer2->Draw("Csame");
	gPad->RedrawAxis();
	gPad->Update();
	c3->Print("mda_combine_qA.png");
	c3->Print("mda_combine_qA.pdf");

	TCanvas* c4 = new TCanvas("c4", "c4", 600, 600);
	TMultiGraph* gc4 =  exclusionObserved(hist4);
	hist2Dbaseplot(c4, hist4, "", 0,1, false, "CL_{s}",0.06);
	for(int i=0;i<=hist4->GetNbinsX();i++){
	  for(int j=0;j<=hist4->GetNbinsY();j++){
	    if(hist4->GetBinContent(i,j)<=0) hist4->SetBinContent(i,j,0.001);
	  }
	}
	gc4->Draw("C");
	gc2->Draw("CF");
	outer->Draw("CFsame");
	outer2->Draw("Csame");
	L->Draw("Same");
	gPad->Update();
	c4->Print("mda_self_CLs_obs.png");
	c4->Print("mda_self_CLs_obs.pdf");

	TCanvas* c5 = new TCanvas("c5", "c5", 600, 600);
	hist2Dbaseplot(c5, hist5, "", 0.001,10000,true, "q_{#mu}",0.06);
	gc2->Draw("CF");
	outer->Draw("CFsame");
	outer2->Draw("Csame");
	gPad->RedrawAxis();
	gPad->Update();
	c5->Print("mda_self_qMu.png");
	c5->Print("mda_self_qMu.pdf");

	TCanvas* c6 = new TCanvas("c6", "c6", 600, 600);
	hist2Dbaseplot(c6, hist6, "", 0.001,10000,true,"q_{A}",0.06);
	gc2->Draw("CF");
	outer->Draw("CFsame");
	outer2->Draw("Csame");
	gPad->RedrawAxis();
	gPad->Update();
	c6->Print("mda_self_qA.png");
	c6->Print("mda_self_qA.pdf");


	///-----------------------------
	TCanvas* a1 = new TCanvas("a1", "a1", 600, 600);
	hist2Dbaseplot(a1, Xshist1, "",0.000001,300,true,"#sigma#font[42]{(ggA)}#upoint#font[52]{B}#font[42]{(A#rightarrow#tau#tau)} [pb]",0.06);
	a1->Print("ggA.png");
	a1->Print("ggA.pdf");

	TCanvas* a2 = new TCanvas("a2", "a2", 600, 600);
	hist2Dbaseplot(a2, Xshist2, "",0.000001,300,true,"#sigma#font[42]{(ggH)}#upoint#font[52]{B}#font[42]{(H#rightarrow#tau#tau)} [pb]",0.06);
	a2->Print("ggHH.png");
	a2->Print("ggHH.pdf");

	TCanvas* a3 = new TCanvas("a3", "a3", 600, 600);
	hist2Dbaseplot(a3, Xshist3, "",0.000001,300,true,"#sigma#font[42]{(ggh)}#upoint#font[52]{B}#font[42]{(h#rightarrow#tau#tau)} [pb]",0.06);
	a3->Print("ggh.png");
	a3->Print("ggh.pdf");

	TCanvas* a4 = new TCanvas("a4", "a4", 600, 600);
	hist2Dbaseplot(a4, Xshist4, "",0.000001,300,true,"#sigma#font[42]{(bbA)}#upoint#font[52]{B}#font[42]{(A#rightarrow#tau#tau)} [pb]",0.06);
	a4->Print("bbA.png");
	a4->Print("bbA.pdf");

	TCanvas* a5 = new TCanvas("a5", "a5", 600, 600);
	hist2Dbaseplot(a5, Xshist5, "",0.000001,300,true,"#sigma#font[42]{(bbH)}#upoint#font[52]{B}#font[42]{(H#rightarrow#tau#tau)} [pb]",0.06);
	a5->Print("bbHH.png");
	a5->Print("bbHH.pdf");

	TCanvas* a6 = new TCanvas("a6", "a6", 600, 600);
	hist2Dbaseplot(a6, Xshist6, "",0.000001,300,true,"#sigma#font[42]{(bbh)}#upoint#font[52]{B}#font[42]{(h#rightarrow#tau#tau)} [pb]",0.06);
	a6->Print("bbh.png");
	a6->Print("bbh.pdf");

	///-----------------------------

	TCanvas* d1 = new TCanvas("d1","d1", 600, 600);
	hist2Dbaseplot(d1, ggcmb, "",0.000001,450,true,"#sigma#font[42]{(gg#phi)}#upoint#font[52]{B}#font[42]{(#phi#rightarrow#tau#tau)} [pb]",0.06);
	d1->Print("ggPhi.png");
	d1->Print("ggPhi.pdf");

	TCanvas* d2 = new TCanvas("d2","d2", 600, 600);
	hist2Dbaseplot(d2, bbcmb, "",0.000001,450,true,"#sigma#font[42]{(bb#phi)}#upoint#font[52]{B}#font[42]{(#phi#rightarrow#tau#tau)} [pb]",0.06);
	d2->Print("bbPhi.png");
	d2->Print("bbPhi.pdf");

	///-----------------------------

	TCanvas* b1 = new TCanvas("b1", "b1", 600, 600);
	hist2Dbaseplot(b1, mdiffAh, "",0,1,false,"|m_{A}-m_{h}|/max(m_{A},m_{h})",0.06);
	b1->Print("m_diffmaxAh.png");
	b1->Print("m_diffmaxAh.pdf");

	TCanvas* b2 = new TCanvas("b2", "b2", 600, 600);
	hist2Dbaseplot(b2, mdiffAH, "",0,1,false,"|m_{A}-m_{H}|/max(m_{A},m_{H})",0.06);
	b2->Print("m_diffmaxAH.png");
	b2->Print("m_diffmaxAH.pdf");

        TCanvas* b3 = new TCanvas("b3", "b3", 600, 600);
	hist2Dbaseplot(b3, mdiffHh, "",0,1,false,"|m_{H}-m_{h}|/max(m_{H},m_{h})",0.06);
	b3->Print("m_diffmaxHh.png");
	b3->Print("m_diffmaxHh.pdf");

	///-----------------------------

	TCanvas* e1 = new TCanvas("e1", "e1", 600,600);
	hist2Dbaseplot(e1, mdiffhrefA, "",0,1,false,"|m_{A}-m_{h}|/(m_{A}",0.06);
	b3->Print("m_diffhrefA.png");
	b3->Print("m_diffhrefA.pdf");

	TCanvas* e2 = new TCanvas("e2", "e2", 600,600);
	hist2Dbaseplot(e2, mdiffHrefA, "",0,1,false,"|m_{A}-m_{H}|/m_{A}",0.06);
	b3->Print("m_diffHrefA.png");
	b3->Print("m_diffHrefA.pdf");

	TCanvas* e3 = new TCanvas("e3", "e3", 600,600);
	hist2Dbaseplot(e3, mdiffhrefH, "",0,1,false,"|m_{H}-m_{h}|/m_{H}",0.06);
	b3->Print("m_diffhrefH.png");
	b3->Print("m_diffhrefH.pdf");

	TCanvas* e4 = new TCanvas("e4", "e4", 600,600);
	hist2Dbaseplot(e4, mdiffArefH, "",0,1,false,"|m_{H}-m_{A}|/m_{H}",0.06);
	b3->Print("m_diffArefH.png");
	b3->Print("m_diffArefH.pdf");

	TCanvas* e5 = new TCanvas("e5", "e5", 600,600);
	hist2Dbaseplot(e5, mdiffArefh, "",0,1,false,"|m_{h}-m_{A}|/m_{h}",0.06);
	b3->Print("m_diffArefh.png");
	b3->Print("m_diffArefh.pdf");

	TCanvas* e6 = new TCanvas("e6", "e6", 600,600);
	hist2Dbaseplot(e6, mdiffHrefh, "",0,1,false,"|m_{h}-m_{H}|/m_{h}",0.06);
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
	hist2Dbaseplot(g1, globalNLLhist, "", -0.001, delta*1.01,false,"#DeltaNLL_{mA}^{*, tan#beta}",0.06);//,kGray+1);
	gc2->Draw("CF");
	outer->Draw("CFsame");
	outer2->Draw("Csame");
	gPad->RedrawAxis();
	g1->Print("mia_NLLglob.pdf");
	g1->Print("mia_NLLglob.png");
	
	TCanvas* g1_log = new TCanvas("g1_log", "g1_log", 600, 600);
	hist2Dbaseplot(g1_log, globalNLLhist, "", 0.001, 100,true,"#DeltaNLL_{mA}^{*, tan#beta}",0.06);//,kGray+1);
	gc2->Draw("CF");
	outer->Draw("CFsame");
	gPad->RedrawAxis();
	g1_log->Print("mia_NLLglob_log.pdf");
	g1_log->Print("mia_NLLglob_log.png");

	TCanvas* g2 = new TCanvas("g2", "g2", 600, 600);
	//deltaNLLhist->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(g2, deltaNLLhist, "",0.001,1000,true,"#DeltaNLL",0.06);//,kGray+2);
	gc2->Draw("CF");
	outer->Draw("CFsame");
	outer2->Draw("Csame");
	gPad->RedrawAxis();
	g2->Print("mia_DeltaNLL.pdf");
	g2->Print("mia_DeltaNLL.png");

	TCanvas* g3 = new TCanvas("g3", "g3", 600, 600);
	//fullNLLhist->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(g3, fullNLLhist, "",0.001,1000,true,"#DeltaNLL_{mA}^{tanb}",0.06);//,kGray+2);
	gc2->Draw("CF");
	outer->Draw("CFsame");
	outer2->Draw("Csame");
	gPad->RedrawAxis();
	g3->Print("mia_fullNLL.pdf");
	g3->Print("mia_fullNLL.png");

	TCanvas* g35 = new TCanvas("g35", "g35", 600, 600);
	//fullNLLhist->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(g35, fullNLLhist, "",0,7,false,"#DeltaNLL_{mA}^{tanb}",0.06);//,kGray+2);
	gc2->Draw("CF");
	outer->Draw("CFsame");
	outer2->Draw("Csame");
	gPad->RedrawAxis();
	g35->Print("mia_fullNLL_lin.pdf");
	g35->Print("mia_fullNLL_lin.png");


	
	min = NLLmuGlobalforqmu->GetMinimum();
	max = NLLmuGlobalforqmu->GetMaximum();
	delta = max - min;
	TCanvas* g4 = new TCanvas("g4", "g4", 600, 600);
	hist2Dbaseplot(g4, NLLmuGlobalforqmu, "", 0, delta*1.01,false,"#DeltaNLL_{mA}^{*, tan#beta}",0.06);//, kGray+1);
	gc2->Draw("CF");
	outer->Draw("CFsame");
	outer2->Draw("Csame");
	gPad->RedrawAxis();
	g4->Print("mda_NLLglob.pdf");
	g4->Print("mda_NLLglob.png");

	TCanvas* g4_log = new TCanvas("g4_log", "g4_log", 600, 600);
	hist2Dbaseplot(g4_log, NLLmuGlobalforqmu, "", 0.001, 100, true,"#DeltaNLL_{mA}^{*, tan#beta}",0.06);//, kGray+1);
	gc2->Draw("CF");
	outer->Draw("CFsame");
	outer2->Draw("Csame");
	gPad->RedrawAxis();
	g4_log->Print("mda_NLLglob_log.pdf");
	g4_log->Print("mda_NLLglob_log.png");

	TCanvas* g5 = new TCanvas("g5", "g5", 600, 600);
	//deltaNLLforqmu->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(g5, deltaNLLforqmu, "",0.001,1000,true,"#DeltaNLL",0.06);// ,kGray+2);
	gc2->Draw("CF");
	outer->Draw("CFsame");
	outer2->Draw("Csame");
	gPad->RedrawAxis();
	g5->Print("mda_DeltaNLL.pdf");
	g5->Print("mda_DeltaNLL.png");

	TCanvas* g6 = new TCanvas("g6", "g6", 600, 600);
	//NLLmuFixedforqmu->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(g6, NLLmuFixedforqmu, "",0.001,1000,true,"#DeltaNLL_{mA}^{tanb}",0.06);//kGray+2);
	gc2->Draw("CF");
	outer->Draw("CFsame");
	outer2->Draw("Csame");
	gPad->RedrawAxis();
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
	      double deltadiff = deltaNLLhist->GetBinContent(i,j) - deltaNLLforqmu->GetBinContent(i,j);
	      double rdeltadiff = (deltaNLLhist->GetBinContent(i,j) - deltaNLLforqmu->GetBinContent(i,j))/deltaNLLforqmu->GetBinContent(i,j);
	      if(diff < 10 && diff >-10){
		  fullNLLdiff->Fill(diff);
		  fullNLLdiff2D->SetBinContent(i,j,diff);
		  deltaNLLdiff->Fill(deltadiff);
		  deltaNLLdiff2D->SetBinContent(i,j,deltadiff);
		}
	      else if(diff >= 10){
		  fullNLLdiff->Fill(10);
		  fullNLLdiff2D->SetBinContent(i,j,10);
		  deltaNLLdiff->Fill(10);
		  deltaNLLdiff2D->SetBinContent(i,j,10);
		}
	      else if(diff <= -10){
		  fullNLLdiff->Fill(-10);
		  fullNLLdiff2D->SetBinContent(i,j,-10);
		  deltaNLLdiff->Fill(-10);
		  deltaNLLdiff2D->SetBinContent(i,j,-10);
		}
	      if(rdiff < 1.0 && rdiff > -1.0){
		  rfullNLLdiff->Fill(rdiff);
		  rfullNLLdiff2D->SetBinContent(i,j,rdiff);
		  rdeltaNLLdiff->Fill(rdeltadiff);
		  rdeltaNLLdiff2D->SetBinContent(i,j,rdeltadiff);
		}
	      else if(diff >= 1.0){
		  fullNLLdiff->Fill(1.0);
		  fullNLLdiff2D->SetBinContent(i,j,1.0);
		  deltaNLLdiff->Fill(1.0);
		  deltaNLLdiff2D->SetBinContent(i,j,1.0);
		}
	      else if(diff <= -1.0){
		  fullNLLdiff->Fill(-1.0);
		  fullNLLdiff2D->SetBinContent(i,j,-1.0);
		  deltaNLLdiff->Fill(-1.0);
		  deltaNLLdiff2D->SetBinContent(i,j,-1.0);
		}
	    }
	}
	
	TCanvas* h1 = new TCanvas("h1", "h1", 600, 600);
	hist1Dbaseplot(h1, fullNLLdiff);
	gPad->Update();
	h1->Print("fullNLLdiff_1D.pdf");
	h1->Print("fullNLLdiff_1D.png");

	TCanvas* h2 = new TCanvas("h2", "h2", 600, 600);
	hist1Dbaseplot(h2, rfullNLLdiff);
	gPad->Update();
	h2->Print("rfullNLLdiff_1D.pdf");
	h2->Print("rfullNLLdiff_1D.png");

	TCanvas* h3 = new TCanvas("h3", "h3", 600, 600);
	fullNLLdiff2D->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(h3, fullNLLdiff2D,"",-10,10,false,"NLL_{re}-NLL_{di}",0.06);	
	gc2->Draw("CF");
	outer->Draw("CFsame");
	outer2->Draw("Csame");
	gPad->RedrawAxis();
	h3->Print("fullNLLdiff_2D.pdf");
	h3->Print("fullNLLdiff_2D.png");

	TCanvas* h4 = new TCanvas("h4", "h4", 600, 600);
	rfullNLLdiff2D->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(h4, rfullNLLdiff2D,"",-1.0,1.0,false,"(NLL_{re}-NLL_{di})/NLL_{di}",0.06);
	gc2->Draw("CF");
	outer->Draw("CFsame");
	outer2->Draw("Csame");
	gPad->RedrawAxis();
	h4->Print("rfullNLLdiff_2D.pdf");
	h4->Print("rfullNLLdiff_2D.png");

	TCanvas* h5 = new TCanvas("h5", "h5", 600, 600);
	hist1Dbaseplot(h5, deltaNLLdiff);
	gPad->Update();
	h5->Print("deltaNLLdiff_1D.pdf");
	h5->Print("deltaNLLdiff_1D.png");

	TCanvas* h6 = new TCanvas("h6", "h6", 600, 600);
	hist1Dbaseplot(h6, rdeltaNLLdiff);
	gPad->Update();
	h6->Print("rdeltaNLLdiff_1D.pdf");
	h6->Print("rdeltaNLLdiff_1D.png");

	TCanvas* h7 = new TCanvas("h7", "h7", 600, 600);
	deltaNLLdiff2D->GetZaxis()->SetLabelSize(0.05);
	hist2Dbaseplot(h7, deltaNLLdiff2D,"",-10,10,false,"NLL_{re}-NLL_{di}",0.06);	
	gc2->Draw("CF");
	outer->Draw("CFsame");
	outer2->Draw("Csame");
	gPad->RedrawAxis();
	h7->Print("deltaNLLdiff_2D.pdf");
	h7->Print("deltaNLLdiff_2D.png");

// 	TCanvas* h8 = new TCanvas("h8", "h8", 600, 600);
// 	rdeltaNLLdiff2D->GetZaxis()->SetLabelSize(0.05);
// 	hist2Dbaseplot(h8, rdeltaNLLdiff2D,"",-1.0,1.0,false,"(NLL_{re}-NLL_{di})/NLL_{di}",0.06);
// 	gc2->Draw("CF");
// 	outer->Draw("CFsame");
// 	outer2->Draw("Csame");
// 	gPad->RedrawAxis();
// 	h8->Print("rdeltaNLLdiff_2D.pdf");
// 	h8->Print("rdeltaNLLdiff_2D.png");

	///-----------------------------
	

	TH2D* CLsbHist2D = (TH2D*) File->Get("CLsbHist2D_as");
	TH2D* CLsbhistNLL = (TH2D*) File->Get("CLsbhistNLL");

	TCanvas* i1 = new TCanvas("i1", "i1", 600, 600);
	TMultiGraph* excl2D = new TMultiGraph();
	excl2D = exclusionObserved(CLsbHist2D);
	hist2Dbaseplot(i1, CLsbHist2D, "",0,1,false,"CL_{s+b}",0.06);
	for(int i=0;i<=CLsbHist2D->GetNbinsX();i++){
	  for(int j=0;j<=CLsbHist2D->GetNbinsY();j++){
	    if(CLsbHist2D->GetBinContent(i,j)<=0) CLsbHist2D->SetBinContent(i,j,0.001);
	  }
	}
	excl2D->Draw("C");
	gc2->Draw("CF");
	outer->Draw("CFsame");
	outer2->Draw("Csame");
	gPad->RedrawAxis();
	gPad->Update();
	i1->Print("mda_CLsb.pdf");
	i1->Print("mda_CLsb.png");

	TCanvas* i2 = new TCanvas("i2", "i2", 600, 600);
	CLsbhistNLL->Draw("Colz");
	TMultiGraph* exclNLL = new TMultiGraph();
	exclNLL = exclusionObserved(CLsbhistNLL);
	hist2Dbaseplot(i2, CLsbhistNLL, "",0,1,false,"CL_{s+b}",0.06);
	for(int i=0;i<=CLsbhistNLL->GetNbinsX();i++){
	  for(int j=0;j<=CLsbhistNLL->GetNbinsY();j++){
	    if(CLsbhistNLL->GetBinContent(i,j)<=0) CLsbhistNLL->SetBinContent(i,j,0.001);
	  }
	}
	exclNLL->Draw("C");
	gc2->Draw("CF");
	outer->Draw("CFsame");
	outer2->Draw("Csame");
	gPad->RedrawAxis();
	gPad->Update();
	i2->Print("mia_CLsb.pdf");
	i2->Print("mia_CLsb.png");
	
	TCanvas* i3 = new TCanvas("i3", "i3", 600, 600);
	i3->SetLeftMargin     (0.14);
	i3->SetBottomMargin   (0.13);
	TMultiGraph* excl2Dcompare = new TMultiGraph();
	TMultiGraph* exclNLLcompare = new TMultiGraph();
	TMultiGraph* CLscompare = new TMultiGraph();

	excl2Dcompare = exclusionObserved(CLsbHist2D,kGreen+3);
	exclNLLcompare = exclusionObserved(CLsbhistNLL,kRed);
	CLscompare = exclusionObserved(hist4,kBlue);
	excl2Dcompare->SaveAs("mda.root");
	exclNLLcompare->SaveAs("mia.root");
	CLscompare->SaveAs("CLs.root");

	excl2Dcompare->Draw("C");
	exclNLLcompare->Draw("C");
	CLscompare->Draw("C");
	gc2->Draw("CF");
	outer2->Draw("Csame");
	outer->Draw("CFsame");

	TLegend* l = new TLegend(0.15,0.6,0.45,0.9);
	l->SetBorderSize( 1  );
	l->SetFillStyle (1001);
	l->SetTextSize  (0.035);
	l->SetTextFont  ( 62 ); 
	l->SetFillColor (kWhite);
	l->SetLineWidth (2);
	TLine* mi = new TLine();
	mi->SetLineColor(kGreen+3);
	mi->SetLineWidth(2);
	TLine* md = new TLine();
	md->SetLineColor(kRed);
	md->SetLineWidth(2);
	TLine* cl = new TLine();
	cl->SetLineColor(kBlue);
	cl->SetLineWidth(2);
	//l->SetTextSize
	l->AddEntry(md, "CL_{s+b}^{re-interpretation}","l");
	l->AddEntry(mi, "CL_{s+b}^{direct}","l");
	l->AddEntry(cl, "CL_{s}^{direct}","l");
	//l->SetFillStyle(0);
	//l->SetBorderSize(0);
	l->Draw("Same");
	i3->Update();
	//gPad->RedrawAxis();
	i3->Print("CLsbComparison.pdf");
	i3->Print("CLsbComparison.png");

// 	if(!higgsBounds)
// 	{
// 		TCanvas* j1 = new TCanvas("j1","j1", 600, 600);
// 		deltaNLLhist_heavy->GetZaxis()->SetLabelSize(0.05);
// 		hist2Dbaseplot(j1, deltaNLLhist_heavy, "#DeltaNLL_{heavy}",0.001,10000,true,"a.u.",0.06,kBlack);
// 		gc2->Draw("CF");
// 		j1->Print("DeltaNLL_heavy.pdf");
// 		j1->Print("DeltaNLL_heavy.pdf");

// 		TCanvas* j2 = new TCanvas("j2","j2", 600, 600);
// 		deltaNLLhist_light->GetZaxis()->SetLabelSize(0.05);
// 		hist2Dbaseplot(j2, deltaNLLhist_light, "#DeltaNLL_{light}",0.001,10000,true,"a.u.",0.06,kBlack);
// 		gc2->Draw("CF");
// 		j2->Print("DeltaNLL_light.pdf");
// 		j2->Print("DeltaNLL_light.pdf");
// 	}
// 	else
	if(higgsBounds)
	{
		TH2D* combinedCluster = (TH2D*) File->Get("combinedCluster");
		TH2D* combinedClusterMass = (TH2D*) File->Get("combinedClusterMass");
		TH2D* deltaNLLhistA = (TH2D*) File->Get("deltaNLLhistA");
		TH2D* deltaNLLhistH = (TH2D*) File->Get("deltaNLLhistH");
		TH2D* deltaNLLhisth = (TH2D*) File->Get("deltaNLLhisth");

		TCanvas* k1 = new TCanvas("k1","k1", 600, 600);
		hist2Dbaseplot(k1, combinedClusterMass, "",50,1000,true,"m_{cluster}^{combined} [GeV]",0.06,kBlack);
		gc2->Draw("CF");
		outer2->Draw("Csame");
		outer->Draw("CFsame");
		k1->Print("HB_combinedCluster_mass.pdf");
		k1->Print("HB_combinedCluster_mass.png");

		TCanvas* k2 = new TCanvas("k2","k2", 600, 600);
		clusterplot(combinedCluster, "",0.06);
		gc2->Draw("CF");
		outer2->Draw("Csame");
		outer->Draw("CFsame");
		k2->Print("HB_combinedCluster_higgs.pdf");
		k2->Print("HB_combinedCluster_higgs.png");
		k2->Print("HB_combinedCluster_higgs.root");
		combinedCluster->SaveAs("HB_combinedCluster_higgs2.root");

		set_plot_style();
		TCanvas* k3 = new TCanvas("k3","k3", 600, 600);
		deltaNLLhistA->GetZaxis()->SetLabelSize(0.05);
		hist2Dbaseplot(k3, deltaNLLhistA, "",0.001,10000,true,"#DeltaNLL_{mA}^{*, tan#beta} cluster(A)",0.06,kBlack);
		gc2->Draw("CF");
		outer->Draw("CFsame");
		outer2->Draw("Csame");
		gPad->RedrawAxis();
		k3->Print("HB_DeltaNLL_A.pdf");
		k3->Print("HB_DeltaNLL_A.png");

		TCanvas* k4 = new TCanvas("k4","k4", 600, 600);
		deltaNLLhistH->GetZaxis()->SetLabelSize(0.05);
		hist2Dbaseplot(k4, deltaNLLhistH, "",0.001,10000,true,"#DeltaNLL_{mA}^{*, tan#beta} cluster(H)",0.06,kBlack);
		gc2->Draw("CF");
		outer->Draw("CFsame");
		outer2->Draw("Csame");
		gPad->RedrawAxis();
		k4->Print("HB_DeltaNLL_HH.pdf");
		k4->Print("HB_DeltaNLL_HH.png");

		TCanvas* k5 = new TCanvas("k5","k5", 600, 600);
		deltaNLLhisth->GetZaxis()->SetLabelSize(0.05);
		hist2Dbaseplot(k5, deltaNLLhisth, "",0.001,10000,true,"#DeltaNLL_{mA}^{*, tan#beta} cluster(h)",0.06,kBlack);
		gc2->Draw("CF");
		outer->Draw("CFsame");
		outer2->Draw("Csame");
		gPad->RedrawAxis();
		k5->Print("HB_DeltaNLL_h.pdf");
		k5->Print("HB_DeltaNLL_h.png");
	}

	File->WriteTObject(CLsdiff,"");
	File->WriteTObject(qAdiff,"");
	File->WriteTObject(qmudiff,"");
	File->WriteTObject(rdeltaNLLdiff,"");
	File->WriteTObject(deltaNLLdiff,"");
	File->WriteTObject(rdeltaNLLdiff2D,"");
	File->WriteTObject(deltaNLLdiff2D,"");
	File->WriteTObject(rfullNLLdiff,"");
	File->WriteTObject(fullNLLdiff,"");
	File->WriteTObject(rfullNLLdiff2D,"");
	File->WriteTObject(fullNLLdiff2D,"");
	File->Close();
	XsFile->Close();
}
