#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

/// This is the core plotting routine that can also be used within
/// root macros. It is therefore not element of the PlotLimits class.
void plotting2DScan(TCanvas& canv, TH2F* plot2D, TGraph* graph95, TGraph* graph68, TGraph* bestfit, std::string& xaxis, std::string& yaxis, std::string& masslabel, int mass, double xmin, double xmax, double ymin, double ymax, bool temp, bool log);

TGraph* 
PlotLimits::convexGraph(TGraph* graph)
{
  int n=graph->GetN();
  double bx[n]; double by[n];
  for(int idx=0; idx<n; ++idx){ graph->GetPoint(idx, bx[idx],by[idx]); }
  TGraph* convex = new TGraph();
  convex->SetPoint(0,0,0);
  for(int idx=0; idx<n; idx++){
    convex->SetPoint(idx+1, bx[idx], by[idx]);
  }
  return convex;
}

void 
PlotLimits::band1D(ostream& out, std::string& xval, std::string& yval, TGraph* bestFit, TGraph* band, float xoffset, float yoffset, std::string CL)
{
  float xmin = -1, xmax = -1.;
  float ymin = -1, ymax = -1.; 
  for(int i=0; i<band->GetN(); ++i){
    if(xmin<0 || band->GetX()[i]<xmin){
      xmin = band->GetX()[i];
    }
    if(xmax<0 || band->GetX()[i]>xmax){
      xmax = band->GetX()[i];
    }
    if(ymin<0 || band->GetY()[i]<ymin){
      ymin = band->GetY()[i];
    }
    if(ymax<0 || band->GetY()[i]>ymax){
      ymax = band->GetY()[i];
    }
  }
  xmin-=xoffset, xmax-=xoffset; ymin-=yoffset, ymax-=yoffset;
  out << std::setw(3) << " " << xval << " :"
      << std::setw(5) << " " << std::fixed << std::setprecision(3) << bestFit->GetX()[0]
      << std::setw(4) << "-" << std::fixed << std::setprecision(3) << TMath::Abs(xmin-bestFit->GetX()[0])
      << "/+" << std::fixed  << std::setprecision(3) << xmax-bestFit->GetX()[0]
      << " " << CL << std::endl;

  out << std::setw(3) << " " << yval << " :"
      << std::setw(5) << " " << std::fixed << std::setprecision(3) << bestFit->GetY()[0]
      << std::setw(4) << "-" << std::fixed << std::setprecision(3) << TMath::Abs(ymin-bestFit->GetY()[0]>0 ? bestFit->GetY()[0] : ymin-bestFit->GetY()[0])
      << "/+" << std::fixed  << std::setprecision(3) << ymax-bestFit->GetY()[0]
      << " " << CL << std::endl;
}

void
PlotLimits::plot2DScan(TCanvas& canv, const char* directory)
{
  // set up styles
  SetStyle();
  // determine x-value from model
  std::string xval = model_.substr(0, model_.find('-'));
  // determine y-value from model
  std::string yval = model_.substr(model_.find('-')+1);
  
  // pick up boundaries of the scan from .scan file in masses directory. This
  // requires that you have run imits.py beforehand with option --multidim-fit
  char type[20]; 
  float first, second;
  float points, xmin, xmax, ymin, ymax;
  for(unsigned int imass=0; imass<bins_.size(); ++imass){
    // buffer mass value
    float mass = bins_[imass];
    if(verbosity_>2){ std::cout << mass << std::endl; }
    std::string line; 
    ifstream file(TString::Format("%s/%d/.scan", directory, (int)mass));
    if(file.is_open()){
      while( file.good() ){
	getline(file,line);
	sscanf(line.c_str(),"%s : %f %f", type, &first, &second);
	if(std::string(type)==std::string("points")){ points = int(first); }
	if(std::string(type)==xval){ xmin = first; xmax = second; }
	if(std::string(type)==yval){ ymin = first; ymax = second; }
      }
      file.close();
    }
    if(verbosity_>1){
      std::cout << " mass: " << mass << ";" << " points: " << points << ";"
		<< " " << xval << " : " << xmin << " -- " << xmax << ";" 
		<< " " << yval << " : " << ymin << " -- " << ymax << ";"
		<< std::endl;
    }

    // tree scan
    char* label = (char*)model_.c_str(); int i=0;
    while(label[i]){ label[i]=putchar(toupper(label[i])); ++i; } std::cout << " : ";
    TString fullpath = TString::Format("%s/%d/higgsCombine%s.MultiDimFit.mH%d.root", directory, (int)mass, label, (int)mass);
    std::cout << "open file: " << fullpath << std::endl;

    TFile* file_ = TFile::Open(fullpath);
    TTree* limit = (TTree*) file_->Get("limit");
    float nll, x, y;
    float nbins = TMath::Sqrt(points);
    TH2F* scan2D = new TH2F("scan2D", "", nbins, xmin, xmax, nbins, ymin, ymax);
    limit->SetBranchAddress("deltaNLL", &nll );  
    limit->SetBranchAddress((std::string("r_")+xval).c_str() , &x);  
    limit->SetBranchAddress((std::string("r_")+yval).c_str() , &y);
    int nevent = limit->GetEntries();
    for(int i=0; i<nevent; ++i){
      limit->GetEvent(i);
      if(scan2D->GetBinContent(scan2D->FindBin(x,y))==0){
	scan2D->Fill(x, y, nll);
      }
    }

    // determine bestfit graph
    float bestFit=-1.; 
    float buffer, bestX=-999., bestY=-999.;
    for(int i=0; i<nevent; ++i){
      limit->GetEvent(i);
      buffer=scan2D->GetBinContent(scan2D->FindBin(x,y));
      if (bestFit<0 || bestFit>buffer){
	// adjust best fit to granularity of scan; we do this to prevent artefacts 
	// when quoting the 1d uncertainties of the scan. For the plotting this 
	// does not play a role. 
	bestX=scan2D->GetXaxis()->GetBinCenter(scan2D->GetXaxis()->FindBin(x)); 
	bestY=scan2D->GetYaxis()->GetBinCenter(scan2D->GetYaxis()->FindBin(y));
	bestFit=buffer; 
      }
    }  
    TGraph* bestfit = new TGraph();
    bestfit->SetPoint(0, bestX, bestY);

    // determine newcontours for 68% CL and 95% CL limits
    double contours[2];
    contours[0] = 0.5;     //68% CL
    contours[1] = 1.92;    //95% CL
    scan2D->SetContour(2, contours);
    scan2D->Draw("CONT Z LIST");  // draw contours as filled regions, and save points
    canv.Update();                // needed to force the plotting and retrieve the contours in TGraph
    TObjArray* conts = (TObjArray*)gROOT->GetListOfSpecials()->FindObject("contours");

    TGraph* graph68=0; TGraph* filled68=0;;
    TGraph* graph95=0; TGraph* filled95=0;;
    // get 68% CL and 95% CL contours 
    for(int i=0; i<conts->GetEntries(); ++i){   
      TList* graphlist = (TList*)conts->At(i);  
      for(int g=0; g<graphlist->GetEntries(); ++g){
	if(i==0){
	  graph68 = (TGraph*)graphlist->At(g);
	  filled68 = convexGraph(graph68);
	}
	if(i==1){
	  graph95 = (TGraph*)graphlist->At(g); 
	  filled95 = convexGraph(graph95);
	}
      }
    }    
    
    // get the old contour plot back for plotting, for temperature plots it is filled 
    // as usual. Otherwise it's left empty and only used to set the boundaries for 
    // plotting.
    TH2F* plot2D = new TH2F("plot2D", "", nbins, xmin, xmax, nbins, ymin, ymax);
    if(temp_){
      for(int i=0; i<nevent; ++i){
	limit->GetEvent(i);
	if(plot2D->GetBinContent(plot2D->FindBin(x,y))==0){plot2D->Fill(x, y, nll);}
      }
    }
    // do the plotting
    std::string masslabel = mssm_ ? std::string("m_{#phi}") : std::string("m_{H}");
    if(temp_){
      plotting2DScan(canv, plot2D, graph95 , graph68 , bestfit, xaxis_, yaxis_, masslabel, mass, xmins_[mass], xmaxs_[mass], ymins_[mass], ymaxs_[mass], temp_, log_);    
    }
    else{
      plotting2DScan(canv, plot2D, filled95, filled68, bestfit, xaxis_, yaxis_, masslabel, mass, xmins_[mass], xmaxs_[mass], ymins_[mass], ymaxs_[mass], temp_, log_);    
    }
    // add the CMS Preliminary stamp
    CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);
    // print 1d band
    ofstream scanOut;  
    scanOut.open(TString::Format("%s/%d/multi-dim.fitresult", directory, (int)mass));
    scanOut << " --- MultiDimFit ---" << std::endl;
    scanOut << "best fit parameter values and uncertainties from NLL scan:" << std::endl;
    band1D(scanOut, xval, yval, bestfit, graph68, (xmax-xmin)/nbins/2, (ymax-ymin)/nbins/2, "(68%)");

    if(png_){
    canv.Print(TString::Format("scan-%s-versus-%s-%d.png", xval.c_str(), yval.c_str(), (int)mass));
    }
    if(pdf_){
      canv.Print(TString::Format("scan-%s-versus-%s-%d.pdf", xval.c_str(), yval.c_str(), (int)mass));
      canv.Print(TString::Format("scan-%s-versus-%s-%d.eps", xval.c_str(), yval.c_str(), (int)mass));
    }
    if(txt_){
      //print(std::string(output_).append("_").append(label_).c_str(), outerBand, innerBand, expected, observed, "txt");
      //print(std::string(output_).append("_").append(label_).c_str(), outerBand, innerBand, expected, observed, "tex");
    }
    if(root_){
      TFile* output = new TFile(TString::Format("scan-%s-versus-%s.root", xval.c_str(), yval.c_str()), "update");
      if(!output->cd(output_.c_str())){
	output->mkdir(output_.c_str());
	output->cd(output_.c_str());
      }
      graph68 ->Write(TString::Format("graph68_%d"  , (int)mass) );
      filled68->Write(TString::Format("filled68_%d" , (int)mass) );      
      graph95 ->Write(TString::Format("graph95_%d"  , (int)mass) );
      filled95->Write(TString::Format("filled95_%d" , (int)mass) );
      plot2D  ->Write(TString::Format("plot2D_%d"   , (int)mass) );
      output->Close();
    }
  }
  return;
}
