void NLLAnalysis(const char* filename="output.root"){

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

// Defining range for the z axis
hist2->GetZaxis()->SetRangeUser(0.001, 10000);
hist3->GetZaxis()->SetRangeUser(0.001, 10000);
hist5->GetZaxis()->SetRangeUser(0.001, 10000);
hist6->GetZaxis()->SetRangeUser(0.001, 10000);

// Plotting 2D histograms
c->Divide(3,2);
c->cd(1);
hist1->Draw("Colz");
gPad->Update();
TPaveStats* statbox = (TPaveStats*) hist1->FindObject("stats");
statbox->SetX1NDC(0.13);
statbox->SetX2NDC(0.33);
statbox->SetY1NDC(0.65);
statbox->SetY2NDC(0.89);
hist1->Draw("Colz");

c->cd(2);
hist2->Draw("Colz");
gPad->SetLogz();
gPad->Update();
statbox = (TPaveStats*) hist2->FindObject("stats");
statbox->SetX1NDC(0.69);
statbox->SetX2NDC(0.89);
statbox->SetY1NDC(0.65);
statbox->SetY2NDC(0.89);
hist2->GetZaxis()->SetLabelSize(0.03);
hist2->GetZaxis()->SetLabelOffset(0.003);
hist2->Draw("Colz");

c->cd(3);
hist3->Draw("Colz");
gPad->SetLogz();
gPad->Update();
statbox = (TPaveStats*) hist3->FindObject("stats");
statbox->SetX1NDC(0.69);
statbox->SetX2NDC(0.89);
statbox->SetY1NDC(0.65);
statbox->SetY2NDC(0.89);
hist3->GetZaxis()->SetLabelSize(0.03);
hist3->GetZaxis()->SetLabelOffset(0.003);
hist3->Draw("Colz");

c->cd(4);
hist4->Draw("Colz");
gPad->Update();
statbox = (TPaveStats*) hist4->FindObject("stats");
statbox->SetX1NDC(0.13);
statbox->SetX2NDC(0.33);
statbox->SetY1NDC(0.65);
statbox->SetY2NDC(0.89);
hist4->Draw("Colz");

c->cd(5);
hist5->Draw("Colz");
gPad->SetLogz();
gPad->Update();
statbox = (TPaveStats*) hist5->FindObject("stats");
statbox->SetX1NDC(0.69);
statbox->SetX2NDC(0.89);
statbox->SetY1NDC(0.65);
statbox->SetY2NDC(0.89);
hist5->GetZaxis()->SetLabelSize(0.03);
hist5->GetZaxis()->SetLabelOffset(0.003);
hist5->Draw("Colz");

c->cd(6);
hist6->Draw("Colz");
gPad->SetLogz();
gPad->Update();
statbox = (TPaveStats*) hist6->FindObject("stats");
statbox->SetX1NDC(0.69);
statbox->SetX2NDC(0.89);
statbox->SetY1NDC(0.65);
statbox->SetY2NDC(0.89);
hist6->GetZaxis()->SetLabelSize(0.03);
hist6->GetZaxis()->SetLabelOffset(0.003);
hist6->Draw("Colz");

c->SaveAs("plotted2Dhistos.pdf");

TCanvas* c1 = new TCanvas("c1", "c1", 1300, 700);
c1->Divide(3,2);

c1->cd(1);
Xshist1->Draw("Colz");
gPad->SetLogz();
gPad->Update();
statbox = (TPaveStats*) Xshist1->FindObject("stats");
statbox->SetX1NDC(0.69);
statbox->SetX2NDC(0.89);
statbox->SetY1NDC(0.65);
statbox->SetY2NDC(0.89);
Xshist1->GetZaxis()->SetLabelSize(0.03);
Xshist1->GetZaxis()->SetLabelOffset(0.003);
Xshist1->Draw("Colz");

c1->cd(2);
Xshist2->Draw("Colz");
gPad->SetLogz();
gPad->Update();
statbox = (TPaveStats*) Xshist2->FindObject("stats");
statbox->SetX1NDC(0.69);
statbox->SetX2NDC(0.89);
statbox->SetY1NDC(0.65);
statbox->SetY2NDC(0.89);
Xshist2->GetZaxis()->SetLabelSize(0.03);
Xshist2->GetZaxis()->SetLabelOffset(0.003);
Xshist2->Draw("Colz");

c1->cd(3);
Xshist3->Draw("Colz");
gPad->SetLogz();
gPad->Update();
statbox = (TPaveStats*) Xshist3->FindObject("stats");
statbox->SetX1NDC(0.69);
statbox->SetX2NDC(0.89);
statbox->SetY1NDC(0.65);
statbox->SetY2NDC(0.89);
Xshist3->GetZaxis()->SetLabelSize(0.03);
Xshist3->GetZaxis()->SetLabelOffset(0.003);
Xshist3->Draw("Colz");

c1->cd(4);
Xshist4->Draw("Colz");
gPad->SetLogz();
gPad->Update();
statbox = (TPaveStats*) Xshist4->FindObject("stats");
statbox->SetX1NDC(0.69);
statbox->SetX2NDC(0.89);
statbox->SetY1NDC(0.65);
statbox->SetY2NDC(0.89);
Xshist4->GetZaxis()->SetLabelSize(0.03);
Xshist4->GetZaxis()->SetLabelOffset(0.003);
Xshist4->Draw("Colz");

c1->cd(5);
Xshist5->Draw("Colz");
gPad->SetLogz();
gPad->Update();
statbox = (TPaveStats*) Xshist5->FindObject("stats");
statbox->SetX1NDC(0.69);
statbox->SetX2NDC(0.89);
statbox->SetY1NDC(0.65);
statbox->SetY2NDC(0.89);
Xshist5->GetZaxis()->SetLabelSize(0.03);
Xshist5->GetZaxis()->SetLabelOffset(0.003);
Xshist5->Draw("Colz");

c1->cd(6);
Xshist6->Draw("Colz");
gPad->SetLogz();
gPad->Update();
statbox = (TPaveStats*) Xshist6->FindObject("stats");
statbox->SetX1NDC(0.69);
statbox->SetX2NDC(0.89);
statbox->SetY1NDC(0.65);
statbox->SetY2NDC(0.89);
Xshist6->GetZaxis()->SetLabelSize(0.03);
Xshist6->GetZaxis()->SetLabelOffset(0.003);
Xshist6->Draw("Colz");

c1->SaveAs("plottedXsBr.pdf");

TCanvas* c2 = new TCanvas("c2", "c2", 1300,700);
c2->Divide(2,1);

c2->cd(1);
mhist1->GetZaxis()->SetRangeUser(-0.000001,1);
mhist1->Draw("Colz");
gPad->Update();
statbox = (TPaveStats*) mhist1->FindObject("stats");
statbox->SetX1NDC(0.69);
statbox->SetX2NDC(0.89);
statbox->SetY1NDC(0.65);
statbox->SetY2NDC(0.89);
mhist1->Draw("Colz");

c2->cd(2);
mhist2->Draw("Colz");
gPad->Update();
statbox = (TPaveStats*) mhist2->FindObject("stats");
statbox->SetX1NDC(0.69);
statbox->SetX2NDC(0.89);
statbox->SetY1NDC(0.65);
statbox->SetY2NDC(0.89);
mhist2->GetZaxis()->SetRangeUser(-0.000001,1);
mhist2->Draw("Colz");

c2->SaveAs("massDifferences.pdf");

// Creating new 1D histograms with differences between the quantities computed by hand vs asymptotic
TH1D* CLsdiff = new TH1D("CLsdiff", "Difference of CL_{s}: by hand vs. asymptotic; CL_{s}^{by hand} - CL_{s}^{asymptotic}; Entries", 100, -0.2, 0.2);
TH1D* qmudiff = new TH1D("qmudiff", "Difference of q_{#mu}: by hand vs. asymptotic; q_{#mu}^{by hand} - q_{#mu}^{asymptotic}; Entries", 100, -10, 10);
TH1D* qAdiff = new TH1D("qAdiff", "Difference of q_{A}: by hand vs. asymptotic; q_{A}^{by hand} - q_{A}^{asymptotic}; Entries", 100, -10, 10);

CLsdiff->GetYaxis()->SetTitleOffset(1.5);
CLsdiff->GetYaxis()->SetLabelSize(0.03);
qmudiff->GetYaxis()->SetTitleOffset(1.5);
qmudiff->GetYaxis()->SetLabelSize(0.03);
qAdiff->GetYaxis()->SetTitleOffset(1.5);
qAdiff->GetYaxis()->SetLabelSize(0.03);

//Creating new 2D histograms for combined Crosssection for the (mA, tanb) plane

TH2D* ggcmb = new TH2D();
TH2D* bbcmb = new TH2D();

hist1->Copy(*ggcmb);
hist1->Copy(*bbcmb);

ggcmb->Reset();
bbcmb->Reset();

ggcmb->SetTitle("Combined #sigma(gg#phi)#upointBR(#phi#rightarrow#tau#tau) [pb] for (m_{A}, tan#beta) plane; m_{A}; tan#beta");
ggcmb->SetName("ggcmb");
bbcmb->SetTitle("Combined #sigma(bb#phi)#upointBR(#phi#rightarrow#tau#tau) [pb] for (m_{A}, tan#beta) plane; m_{A}; tan#beta");
bbcmb->SetName("bbcmb");

TCanvas* d = new TCanvas("d","d", 1300, 700);
TCanvas* d1 = new TCanvas("d1","d1", 1300, 700);
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
		
		double ggcmbXs = Xshist1->GetBinContent(i,j);
		double bbcmbXs = Xshist4->GetBinContent(i,j);
		//if (mhist1->GetBinContent(i,j)==0.0) std::cout << "Point with no difference between mA ans mH: (" << mhist1->GetXaxis()->GetBinLowEdge(i) << "," << mhist1->GetYaxis()->GetBinLowEdge(j) <<  ")" << std::endl;
		if (mhist1->GetBinContent(i,j) <= 0.15)
		{
			ggcmbXs += Xshist2->GetBinContent(i,j);
			bbcmbXs += Xshist5->GetBinContent(i,j);
		}
		if (mhist2->GetBinContent(i,j) <= 0.15)
		{
			ggcmbXs += Xshist3->GetBinContent(i,j);
			bbcmbXs += Xshist6->GetBinContent(i,j);
		}
		ggcmb->SetBinContent(i,j,ggcmbXs);
		bbcmb->SetBinContent(i,j,bbcmbXs);
		
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
// Plotting the new 1D

d->Divide(3,1);

d->cd(1);
CLsdiff->Draw();
gPad->Update();

d->cd(2);
qmudiff->Draw();
gPad->Update();

d->cd(3);
qAdiff->Draw();
gPad->Update();

d->SaveAs("quantitiesDifference.pdf");

// Plotting the new 2D

d1->Divide(2,1);

d1->cd(1);
ggcmb->Draw("Colz");
gPad->SetLogz();
gPad->Update();
statbox = (TPaveStats*) ggcmb->FindObject("stats");
statbox->SetX1NDC(0.69);
statbox->SetX2NDC(0.89);
statbox->SetY1NDC(0.65);
statbox->SetY2NDC(0.89);
ggcmb->GetZaxis()->SetLabelSize(0.024);
ggcmb->GetZaxis()->SetLabelOffset(0.001);
ggcmb->Draw("Colz");

d1->cd(2);
bbcmb->Draw("Colz");
gPad->SetLogz();
gPad->Update();
statbox = (TPaveStats*) bbcmb->FindObject("stats");
statbox->SetX1NDC(0.69);
statbox->SetX2NDC(0.89);
statbox->SetY1NDC(0.65);
statbox->SetY2NDC(0.89);
bbcmb->GetZaxis()->SetLabelSize(0.024);
bbcmb->GetZaxis()->SetLabelOffset(0.001);
bbcmb->Draw("Colz");

d1->SaveAs("combinedXs.pdf");

ggcmb->Write();
bbcmb->Write();
CLsdiff->Write();
qAdiff->Write();
qmudiff->Write();
File->Close();
}