#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

/// This is the core plotting routine that can also be used within
/// root macros. It is therefore not element of the PlotLimits class.
void contour2D(TString xvar, int xbins, float xmin, float xmax, TString yvar, int ybins, float ymin, float ymax, float smx=1.0, float smy=1.0, TFile *fOut=0, TString name="contour2D");
TList* contourFromTH2(TH2 *h2in, double threshold, int minPoints=20, bool require_minPoints=true, double multip=1);
void plottingScan2D(TCanvas& canv, TH2D* plot2D, TGraph* bestfit, TGraph* c68, TGraph* c95, TString file, TMarker* SMexpected, TMarker* SMexpectedLayer, std::string& xaxis, std::string& yaxis, std::string& masslabel, int mass, double xmin, double xmax, double ymin, double ymax, bool temp, bool log);

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
PlotLimits::plot2DScan(TCanvas& canv, const char* directory, std::string typ)
{
  // set up styles
  SetStyle();
  // determine x-value from model
  std::string xval = model_.substr(0, model_.find('-'));
  // determine y-value from model
  std::string yval = model_.substr(model_.find('-')+1);
  // catch CV-CF, where there is no prefix 'r_' for the branch names when filling the
  // histogram from the TTree
  bool CVCF = (xval.find("CV")!=std::string::npos && yval.find("CF")!=std::string::npos);
  // catch RV-RF, where there is no prefix 'r_' for the branch names when filling the
  // histogram from the TTree
  bool RVRF = (xval.find("R")!=std::string::npos && yval.find("R")!=std::string::npos);
  // catch CB-CTAU, where there is no prefix 'r_' for the branch names when filling the
  // histogram from the TTree
  bool CBCTAU = (xval.find("Cb")!=std::string::npos && yval.find("Ctau")!=std::string::npos);
  // catch CL-CQ, where there is no prefix 'r_' for the branch names when filling the
  // histogram from the TTree
  bool CLCQ = (xval.find("Cl")!=std::string::npos && yval.find("Cq")!=std::string::npos);
  std::cout << model_ << std::endl;
  // output root file which is needed for plotting, depends if FC or Multidim
  TFile* Fout = 0; std::string plot_rootname="";

  // pick up boundaries of the scan from .scan file in masses directory. This
  // requires that you have run imits.py beforehand with option --multidim-fit
  char type[20]; 
  float first=0, second=0;
  float points=2, xmin=0, xmax=0, ymin=0, ymax=0;
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
      std::cout << "mass: " << mass << ";" << " points: " << points << ";"
		<< " " << xval << " : " << xmin << " -- " << xmax << ";" 
		<< " " << yval << " : " << ymin << " -- " << ymax << ";"
		<< std::endl;
    }
    float nbins = TMath::Sqrt(points);
    if(typ=="multidim-fit"){
      // tree scan
      char* label = (char*)model_.c_str(); int i=0;
      while(label[i]){ label[i]=putchar(toupper(label[i])); ++i; } std::cout << " : ";
      TString fullpath = TString::Format("%s/%d/higgsCombine%s.MultiDimFit.mH%d.root", directory, (int)mass, label, (int)mass);
      std::cout << "open file: " << fullpath << std::endl;
      TFile* file_ = TFile::Open(fullpath); if(!file_){ std::cout << "--> TFile is corrupt: skipping masspoint." << std::endl; continue; }
      TTree* limit = (TTree*) file_->Get("limit"); if(!limit){ std::cout << "--> TTree is corrupt: skipping masspoint." << std::endl; continue; }
      float nll, x, y;
      TH2F* scan2D = new TH2F("scan2D", "", nbins, xmin, xmax, nbins, ymin, ymax);
      limit->SetBranchAddress("deltaNLL", &nll );  
      std::string xbranch = (CVCF || RVRF || CBCTAU || CLCQ) ? xval.c_str() : (std::string("r_")+xval).c_str();
      std::string ybranch = (CVCF || RVRF || CBCTAU || CLCQ) ? yval.c_str() : (std::string("r_")+yval).c_str();
      limit->SetBranchAddress(xbranch.c_str() , &x);  
      limit->SetBranchAddress(ybranch.c_str() , &y);
      int nevent = limit->GetEntries();
      ofstream database;  
      database.open(TString::Format("%s/%d/database_%d.out", directory, (int)mass, (int)mass)); 
      for(int i=0; i<nevent; ++i){
	limit->GetEvent(i);
	if(scan2D->GetBinContent(scan2D->FindBin(x,y))==0){
	  // catch small negative values that might occure due to rounding
	  scan2D->Fill(x, y, fabs(nll));
	  database << x << " " << y << " " << fabs(nll) << std::endl; 
	}
      }
      plot_rootname =TString::Format("%s/%d/%s-%s-%s-%d.root", directory, (int)mass, output_.c_str(), label_.c_str(), model_.c_str(), (int)mass);
      Fout = new TFile(plot_rootname.c_str(), "RECREATE");
      gFile = file_;
      contour2D(xbranch.c_str(), nbins, xmin, xmax, ybranch.c_str(), nbins, ymin, ymax, 1.0, 1.0, Fout);  
      file_->Close();
    }
    else if(typ=="feldman-cousins"){
      plot_rootname = TString::Format("%s/%d/plots2DFC.root", directory, (int)mass);
      Fout = TFile::Open(plot_rootname.c_str()); 
    }
    gFile = Fout;
    // do the plotting 
    TH2D *plot2D = 0;
    TGraph *bestfit = 0;
    TGraph *c68 = 0;
    TGraph *c95 = 0;
    if(typ=="multidim-fit"){
      plot2D = (TH2D *)gDirectory->Get("contour2D_h2d")->Clone();
      bestfit = (TGraph *)gDirectory->Get("contour2D_best")->Clone();
      c68 = (TGraph *)((TList *)gDirectory->Get("contour2D_c68"))->At(0)->Clone();
      c95 = (TGraph *)((TList *)gDirectory->Get("contour2D_c95"))->At(0)->Clone();
    }
    else if(typ=="feldman-cousins"){
      plot2D = (TH2D *)gDirectory->Get("h2_cl")->Clone();
      int binx, biny, binz;
      plot2D->GetBinXYZ(plot2D->GetMinimumBin(),binx,biny,binz);
      bestfit = new TGraph();
      bestfit->SetPoint(0, plot2D->GetXaxis()->GetBinCenter(binx), plot2D->GetYaxis()->GetBinCenter(biny));
      c68 = (TGraph *)((TList *)contourFromTH2(plot2D, 0.68))->At(0)->Clone();    
      c95 = (TGraph *)((TList *)contourFromTH2(plot2D, 0.95))->At(0)->Clone();
      //      bestfit = (TGraph *)gDirectory->Get("h2_confcontour_0")->Clone(); //can not used for plotting since TGraph2D and not contour list
      //       c68 = (TGraph *)gDirectory->Get("h2_confcontour_68")->Clone(); //can not used for plotting since TGraph2D and not contour list
      //       c95 = (TGraph *)gDirectory->Get("h2_confcontour_95")->Clone(); //can not used for plotting since TGraph2D and not contour list
    }
    //Draw SM expectation?
    //To make official style diamond, it is necessary to use the deadful hack of overlaying one marker on top of another slightly larger marker
    TMarker* SMexpected = 0;
    TMarker* SMexpectedLayer = 0;
    if(drawsm_){
      SMexpected = new TMarker();
      SMexpectedLayer = new TMarker();
      //Size and colour are set here. For TMarker the position must be set when drawing, so this can be found in src/plottingScan2D.cxx. 
      //Currently positions hardcoded 
      //SMexpected->SetMarkerSize(3.0); SMexpected->SetMarkerColor(97); SMexpected->SetMarkerStyle(33);
      SMexpected->SetMarkerSize(3.0); SMexpected->SetMarkerColor(1); SMexpected->SetMarkerStyle(33);
      SMexpectedLayer->SetMarkerSize(1.8); SMexpectedLayer->SetMarkerColor(89); SMexpectedLayer->SetMarkerStyle(33);
    }
    std::string masslabel = mssm_ ? std::string("m_{#phi}") : std::string("m_{H}");    
    plottingScan2D(canv, plot2D, bestfit, c68, c95, plot_rootname, SMexpected, SMexpectedLayer, xaxis_, yaxis_, masslabel, (int)mass, xmin, xmax, ymin, ymax, temp_, log_);
    // add the CMS Preliminary stamp
    CMSPrelim(dataset_.c_str(), "", 0.135, 0.835);
    //CMSPrelim(dataset_.c_str(), "", 0.145, 0.835);
      
    // print 1d band
    ofstream scanOut;  
    scanOut.open(TString::Format("%s/%d/signal-strength.output", directory, (int)mass));
    scanOut << " --- MultiDimFit ---" << std::endl;
    scanOut << "best fit parameter values and uncertainties from NLL scan:" << std::endl;
    band1D(scanOut, xval, yval, bestfit, c68, (xmax-xmin)/nbins/2, (ymax-ymin)/nbins/2, "(68%)");
    
    if(png_){
      canv.Print(TString::Format("%s-%s-%s-%d.png", output_.c_str(), label_.c_str(), model_.c_str(), (int)mass));
    }
    if(pdf_){
      canv.Print(TString::Format("%s-%s-%s-%d.pdf", output_.c_str(), label_.c_str(), model_.c_str(), (int)mass));
      canv.Print(TString::Format("%s-%s-%s-%d.eps", output_.c_str(), label_.c_str(), model_.c_str(), (int)mass));
      canv.Print(TString::Format("%s-%s-%s-%d.C"  , output_.c_str(), label_.c_str(), model_.c_str(), (int)mass));
    }
    if(txt_){
      TString path;
      path = TString::Format("%s_%s_%s-%d-CL68", output_.c_str(), label_.c_str(), model_.c_str(), (int)mass);
      print(path, xval, yval, c68, "txt"); print(path, xval, yval, c68, "tex");
      path = TString::Format("%s_%s_%s-%d-CL95", output_.c_str(), label_.c_str(), model_.c_str(), (int)mass);
      print(path, xval, yval, c95, "txt"); print(path, xval, yval, c95, "tex");
    }
    if(root_){
      TFile* output = new TFile(TString::Format("scan-%s-versus-%s.root", xval.c_str(), yval.c_str()), "update");
      if(!output->cd(output_.c_str())){
	output->mkdir(output_.c_str());
	output->cd(output_.c_str());
      }
      c68    ->Write(TString::Format("graph68_%d"  , (int)mass)); 
      c95    ->Write(TString::Format("graph95_%d"  , (int)mass)); 
      bestfit->Write(TString::Format("bestfit_%d"  , (int)mass));
      plot2D ->Write(TString::Format("plot2D_%d"   , (int)mass));

      output->Close();
    }
  }
  return;
}
