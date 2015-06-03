void hist2Dbaseplot(TH2D* hist, const char* titlename, double zmin, double zmax, bool log=false, const char* ztitle=""){

	gPad->SetRightMargin(0.20);
	gPad->SetTopMargin(0.05);
	hist->Draw("Colz");
	hist->SetStats(false);
	hist->GetXaxis()->SetTitleSize(0.05);
	hist->GetYaxis()->SetTitleSize(0.05);
	hist->GetZaxis()->SetTitleSize(0.05);
	hist->GetZaxis()->SetLabelSize(0.05);
	hist->GetZaxis()->SetTitle(ztitle);
	hist->GetZaxis()->SetTitleOffset(1.1);

	TLatex* histtitle = new TLatex(120, 50, titlename);
	histtitle->SetTextSize(0.12);
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


void NLLAnalysis(const char* filename="output.root", std::string higgses="hHA", double tolerance=0.15){

set_plot_style();
// Creating output textfile for xs*BR
std::ofstream xsfile;
xsfile.open("xs_boundaries.txt");
// Reading root file
TFile* File = new TFile(filename, "UPDATE");
TCanvas* c = new TCanvas("c", "c", 1300, 700);

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

TH2D* Xshist1 = (TH2D*) File->Get("ggAXsBR");
TH2D* Xshist2 = (TH2D*) File->Get("ggHXsBR");
TH2D* Xshist3 = (TH2D*) File->Get("gghXsBR");

TH2D* Xshist4 = (TH2D*) File->Get("bbAXsBR");
TH2D* Xshist5 = (TH2D*) File->Get("bbHXsBR");
TH2D* Xshist6 = (TH2D*) File->Get("bbhXsBR");

TH2D* mhist1 = (TH2D*) File->Get("massDiffH");
TH2D* mhist2 = (TH2D*) File->Get("massDiffh");


// Plotting 2D histograms
c->Divide(3,2);
c->cd(1);
TGraph* gc1 =  exclusionObserved(hist1);
hist2Dbaseplot(hist1, "CL_{s}",0,1);
gc1->Draw("C");
gPad->Update();

c->cd(2);
hist2Dbaseplot(hist2, "q_{#mu}",0.01,10000,true);

c->cd(3);
hist2Dbaseplot(hist3, "q_{A}",0.01,10000,true);

c->cd(4);
TGraph* gc4 =  exclusionObserved(hist4);
hist2Dbaseplot(hist4, "CL_{s}",0,1);
gc4->Draw("C");
gPad->Update();

c->cd(5);
hist2Dbaseplot(hist5, "q_{#mu}",0.01,10000,true);

c->cd(6);
hist2Dbaseplot(hist6, "q_{A}",0.01,10000,true);

c->SaveAs("plotted2Dhistos.pdf");

TCanvas* c1 = new TCanvas("c1", "c1", 1300, 700);
c1->Divide(3,2);

c1->cd(1);
hist2Dbaseplot(Xshist1, "#sigma_{ggA}#upointBR_{A#rightarrow#tau#tau}",0.000001,300,true,"[pb]");

c1->cd(2);
hist2Dbaseplot(Xshist2, "#sigma_{ggH}#upointBR_{H#rightarrow#tau#tau}",0.000001,300,true,"[pb]");

c1->cd(3);
hist2Dbaseplot(Xshist3, "#sigma_{ggh}#upointBR_{h#rightarrow#tau#tau}",0.000001,300,true,"[pb]");

c1->cd(4);
hist2Dbaseplot(Xshist4, "#sigma_{bbA}#upointBR_{A#rightarrow#tau#tau}",0.000001,300,true,"[pb]");

c1->cd(5);
hist2Dbaseplot(Xshist5, "#sigma_{bbH}#upointBR_{H#rightarrow#tau#tau}",0.000001,300,true,"[pb]");

c1->cd(6);
hist2Dbaseplot(Xshist6, "#sigma_{bbh}#upointBR_{h#rightarrow#tau#tau}",0.000001,300,true,"[pb]");

c1->SaveAs("plottedXsBr.pdf");

// Creating new 1D histograms with differences between the quantities computed own fit vs combine
TH1D* CLsdiff = new TH1D("CLsdiff", ";CL_{s}^{own fit} - CL_{s}^{combine};Entries", 100, -0.1, 0.1);
TH1D* qmudiff = new TH1D("qmudiff", ";q_{#mu}^{own fit} - q_{#mu}^{combine};Entries", 100, -10, 10);
TH1D* qAdiff = new TH1D("qAdiff", ";q_{A}^{own fit} - q_{A}^{combine};Entries", 100, -10, 10);

// Filling the new 1D and 2D histograms 

int massBins = hist1->GetNbinsX();
int tanbBins = hist1->GetNbinsY();

// Bin numering convention: From 1 to Nbins !!!

for(int i=1;i<=massBins; i++)
{
	//std::cout << "Outer loop" << std::endl;
	for(int j=1;j<=tanbBins;j++)
	{
		//std::cout << "Inner loop" << std::endl;
		double CLsDifference = hist1->GetBinContent(i,j) - hist4->GetBinContent(i,j);
		double qmuDifference = hist2->GetBinContent(i,j) - hist5->GetBinContent(i,j);
		double qADifference = hist3->GetBinContent(i,j) - hist6->GetBinContent(i,j);
		//if(qmuDifference>10 || qmuDifference<-10 || qADifference>10 || qADifference<-10) std::cout << "Differences: " << CLsDifference << ", " << qmuDifference << ", " << qADifference << std::endl;
		/*if (CLsDifference != CLsDifference)
		{
			std::cout << "Point with NaN value for CLs: (" << hist1->GetXaxis()->GetBinLowEdge(i) << "," << hist1->GetYaxis()->GetBinLowEdge(j) << ")" << std::endl;
			std::cout << "Respective q_mu value: " << hist2->GetBinContent(i,j) << std::endl;
			std::cout << "Respective q_A value: " << hist3->GetBinContent(i,j) << std::endl;
		}*/
		CLsdiff->Fill(CLsDifference);
		
		if(qmuDifference>10) qmudiff->Fill(9);
		else if(qmuDifference<-10) qmudiff->Fill(-10);
		else qmudiff->Fill(qmuDifference);
		
		if(qADifference>10) qAdiff->Fill(9);
		else if(qADifference<-10) qAdiff->Fill(-10);
		else qAdiff->Fill(qADifference);

		if (j==tanbBins)
		{
			int current_mass = hist1->GetXaxis()->GetBinLowEdge(i);
			if (current_mass>=400)
			{
				xsfile << std::setprecision(4) << "    (\"ggH-bbH\", \""  << current_mass  << "\")  : (" <<  std::setprecision(3) << ggcmbXs << ", " << bbcmbXs << ")," << std::endl;
			}
			else if (current_mass<400 && current_mass >= 300)
			{
				xsfile << std::setprecision(4) << "    (\"ggH-bbH\", \""  << current_mass  << "\")  : (" <<  std::setprecision(3) << ggcmbXs << ", " << bbcmbXs/3.0 << ")," << std::endl;
			}
			else if (current_mass<300 && current_mass >= 250)
			{
				xsfile << std::setprecision(4) << "    (\"ggH-bbH\", \""  << current_mass  << "\")  : (" <<  std::setprecision(3) << ggcmbXs/2.0 << ", " << bbcmbXs/6.0 << ")," << std::endl;
			}
			else if (current_mass<250 && current_mass >= 200)
			{
				xsfile << std::setprecision(4) << "    (\"ggH-bbH\", \""  << current_mass  << "\")  : (" <<  std::setprecision(3) << ggcmbXs/3.0 << ", " << bbcmbXs/10.0 << ")," << std::endl;
			}
			else if (current_mass<200)
			{
				xsfile << std::setprecision(4) << "    (\"ggH-bbH\", \""  << current_mass  << "\")  : (" <<  std::setprecision(3) << ggcmbXs/3.0 << ", " << bbcmbXs/5.0 << ")," << std::endl;
			}
		}
	}
}
xsfile << std::endl;
xsfile.close();

TCanvas* c2 = new TCanvas("c2", "c2", 1300,350);
c2->Divide(3,1);

c2->cd(1);
hist2Dbaseplot(mhist1, "|m_{A}-m_{H}|/m_{A}",0,1);

c2->cd(2);
hist2Dbaseplot(mhist2, "|m_{A}-m_{h}|/m_{A}",0,1);

c2->cd(3);
gPad->SetRightMargin(0.20);
gPad->SetTopMargin(0.05);
cluster->Draw("Colz");
cluster->SetStats(false);
cluster->GetXaxis()->SetTitleSize(0.05);
cluster->GetYaxis()->SetTitleSize(0.05);
cluster->GetZaxis()->SetTitleSize(0.05);
cluster->GetZaxis()->SetLabelSize(0.05);
cluster->GetZaxis()->SetTitleOffset(1.1);
cluster->GetZaxis()->SetRangeUser(0.,4.);

TMarker* A = new TMarker();
A->SetMarkerStyle(21);
A->SetMarkerColor(kCyan+2);

TMarker* hA = new TMarker();
hA->SetMarkerStyle(21);
hA->SetMarkerColor(kGreen-9);

TMarker* HA = new TMarker();
HA->SetMarkerStyle(21);
HA->SetMarkerColor(kOrange+1);

TMarker* hHA = new TMarker();
hHA->SetMarkerStyle(21);
hHA->SetMarkerColor(kRed+3);

TLegend* l = new TLegend(0.38,0.52,0.78,0.92);
l->SetHeader("Higgs contribution");
l->AddEntry(A,"A","p");
l->AddEntry(hA,"h+A","p");
l->AddEntry(HA,"H+A","p");
l->AddEntry(hHA,"h+H+A","p");
l->Draw("Same");
gPad->Update();
//hist2Dbaseplot(cluster, "",0,4);
c2->SaveAs("massDifferences.pdf");





// Plotting the new 1D
TCanvas* d = new TCanvas("d","d", 1300, 500);
d->Divide(3,1);

d->cd(1);
gPad->SetLeftMargin(0.15);
gPad->SetTopMargin(0.01);
gPad->SetRightMargin(0.05);
CLsdiff->Draw();
CLsdiff->SetStats(false);
CLsdiff->GetXaxis()->SetTitleSize(0.045);
CLsdiff->GetYaxis()->SetTitleOffset(2);
gPad->Update();

d->cd(2);
gPad->SetLeftMargin(0.15);
gPad->SetTopMargin(0.01);
gPad->SetRightMargin(0.05);
qmudiff->Draw();
qmudiff->SetStats(false);
qmudiff->GetXaxis()->SetTitleSize(0.045);
qmudiff->GetYaxis()->SetTitleOffset(2);
gPad->Update();

d->cd(3);
gPad->SetLeftMargin(0.15);
gPad->SetTopMargin(0.01);
gPad->SetRightMargin(0.05);
qAdiff->Draw();
qAdiff->SetStats(false);
qAdiff->GetXaxis()->SetTitleSize(0.045);
qAdiff->GetYaxis()->SetTitleOffset(2);
gPad->Update();

d->SaveAs("quantitiesDifference.pdf");

// Plotting the new 2D
TCanvas* d1 = new TCanvas("d1","d1", 866, 350);
d1->Divide(2,1);

d1->cd(1);
hist2Dbaseplot(ggcmb, "#sigma_{gg#phi}#upointBR_{#phi#rightarrow#tau#tau}",0.000001,450,true,"[pb]");

d1->cd(2);
hist2Dbaseplot(bbcmb, "#sigma_{bb#phi}#upointBR_{#phi#rightarrow#tau#tau}",0.000001,450,true,"[pb]");

d1->SaveAs("combinedXs.pdf");

ggcmb->Write();
bbcmb->Write();
CLsdiff->Write();
qAdiff->Write();
qmudiff->Write();
File->Close();
}