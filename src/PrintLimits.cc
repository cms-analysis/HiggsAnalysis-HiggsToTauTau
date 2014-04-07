 #include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

void 
PlotLimits::print(const char* filename, std::string& xval, std::string& yval, std::vector<TGraph*> contour, const char* type)
{
  if(std::string(type) == std::string("tex")){
    ofstream file;
    file.open (std::string(filename).append(".tex").c_str());
    file
      << "   " << std::setw(15) << std::right << xval << " (pb) " 
      << " & " << std::setw(15) << std::right << yval << " (pb) "
      << std::right << "  \\\\"
      << std::endl << "\\hline" << std::endl;
    for(std::vector<TGraph*>::const_iterator g=contour.begin(); g!=contour.end(); ++g){
      unsigned int precision = 5;
      for(int idx=0; idx<(*g)->GetN(); ++idx){
	file
	  << "   " << std::setw(15) << std::fixed << std::scientific << std::setprecision(precision) << std::right << (*g)->GetX()[idx]
	  << " & " << std::setw(15) << std::fixed << std::scientific << std::setprecision(precision) << std::right << (*g)->GetY()[idx]
	  << std::right << "  \\\\"
	  << std::endl << "\\hline" << std::endl;
      }
    }
  }
  if(std::string(type) == std::string("txt")){
    ofstream file;
    file.open (std::string(filename).append(".txt").c_str());
    file
      << "   " << std::setw(15) << std::right << xval 
      << "   " << std::setw(15) << std::right << yval
      << std::endl;
    for(std::vector<TGraph*>::const_iterator g=contour.begin(); g!=contour.end(); ++g){
      unsigned int precision = 5;
      for(int idx=0; idx<(*g)->GetN(); ++idx){
	file
	  << "   " << std::setw(15) << std::fixed << std::scientific << std::setprecision(precision) << std::right << (*g)->GetX()[idx]
	  << "   " << std::setw(15) << std::fixed << std::scientific << std::setprecision(precision) << std::right << (*g)->GetY()[idx]
	  << std::endl;
      }
    }
  }
}

void
PlotLimits::print(const char* filename, TGraphAsymmErrors* outerBand, TGraphAsymmErrors* innerBand, TGraph* expected, TGraph* observed, const char* type)
{
  if(std::string(type) == std::string("tex")){
    ofstream file;
    file.open (std::string(filename).append(".tex").c_str());
    file
      << "   " << std::setw(15) << std::right << "    $m_{\\mathrm H}$";
    if(outerBand){
      file
	<< " & " << std::setw(15) << std::right << "$-2\\sigma$";
    }
    file
      << " & " << std::setw(15) << std::right << "$-1\\sigma$"
      << " & " << std::setw(15) << std::right << "     Median"
      << " & " << std::setw(15) << std::right << "$+1\\sigma$";
    if(outerBand){
      file
	<< " & " << std::setw(15) << std::right << "$+2\\sigma$";
    }
    file
      << " & " << std::setw(15) << std::right << "Obs. Limit"
      << std::right << "  \\\\"
      << std::endl << "\\hline" << std::endl;
    unsigned int precision = 2;
    for(int imass=0; imass<expected->GetN(); ++imass){
      file
	<< "   " << std::setw(15) << std::setprecision(4) << std::resetiosflags(std::ios_base::fixed) << std::right << expected->GetX()[imass] << "~\\GeV";
      if(outerBand){
	double value = expected->GetY()[imass] - outerBand->GetEYlow()[imass];
	int exponent = TMath::Nint(TMath::Floor(TMath::Log10(value)));
        double coeff = value/TMath::Power(10., exponent);
	if(exponent>=0){
	  file
	    << " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << "$" << value<< "$" ;
	}
	else{
	  file
	    << " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << "$" << coeff << " \\cdot 10^{" << exponent << "}$";
	}
      }
      double value = expected->GetY()[imass] - innerBand->GetEYlow()[imass];
      int exponent = TMath::Nint(TMath::Floor(TMath::Log10(value)));
      double coeff = value/TMath::Power(10., exponent);
      if(exponent>=0){
	file
	  << " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << "$" << value << "$" ;
      }
      else{
	file
	  << " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << "$" << coeff << " \\cdot 10^{" << exponent << "}$";
      }
      value =  expected->GetY()[imass];
      exponent = TMath::Nint(TMath::Floor(TMath::Log10(value)));
      coeff = value/TMath::Power(10., exponent);
      if(exponent>=0){
	file
	  << " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << "$" << value << "$" ;
      }
      else{
	file
	  << " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << "$" << coeff << " \\cdot 10^{" << exponent << "}$";
      }
      value = expected->GetY()[imass] + innerBand->GetEYhigh()[imass];;
      exponent = TMath::Nint(TMath::Floor(TMath::Log10(value)));
      coeff = value/TMath::Power(10., exponent);
      if(exponent>=0){
	file
	  << " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << "$" << value << "$";
      }
      else{
	file
	  << " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << "$" << coeff << " \\cdot 10^{" << exponent << "}$";
      }
      if(outerBand){	
	double value = expected->GetY()[imass] + outerBand->GetEYhigh()[imass];
	int exponent = TMath::Nint(TMath::Floor(TMath::Log10(value)));
        double coeff = value/TMath::Power(10., exponent);
	if(exponent>=0){
	  file
	    << " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << "$" << value << "$" ;
	}
	else{
	  file
	    << " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << "$" << coeff << " \\cdot 10^{" << exponent << "}$";
	}
      }
      if(observed){
	double value = observed->GetY()[imass];
	int exponent = TMath::Nint(TMath::Floor(TMath::Log10(value)));
        double coeff = value/TMath::Power(10., exponent);
	if(exponent>=0){
	  file
	    << " & " << std::setw(15) << std::right << "$" << value << "$" ;
	}
	else{
	  file
	    << " & " << std::setw(15) << std::right << "$" << coeff << " \\cdot 10^{" << exponent << "}$";
	}
      }
      file
	<< std::right << "  \\\\"
	<< std::endl << "\\hline" << std::endl;
    }
    file.close();
  }
  if(std::string(type) == std::string("txt")){
    ofstream file;
    file.open (std::string(filename).append(".txt").c_str());
    file
      << "#"
      << "   " << std::setw(15) << std::right << "         mX";
    if(outerBand){
      file
	<< "   " << std::setw(15) << std::right << "   -2 sigma";
    }
    file
      << "   " << std::setw(15) << std::right << "   -1 sigma"
      << "   " << std::setw(15) << std::right << "     Median"
      << "   " << std::setw(15) << std::right << "   +1 sigma";
    if(outerBand){
      file
	<< "   " << std::setw(15) << std::right << "   +2 sigma";
    }
    file
      << "   " << std::setw(15) << std::right << "Obs. Limit [pb]"
      << std::endl;
    for(int imass=0; imass<expected->GetN(); ++imass){
      file
	<< "   " << std::setw(15) << std::setprecision(3) << std::right << expected->GetX()[imass];
      if(outerBand){
	file
	  << "   " << std::setw(15) << std::setprecision(3) << std::right << expected->GetY()[imass] - outerBand->GetEYlow()[imass];
      }
      file
	<< "   " << std::setw(15) << std::setprecision(3) << std::right << expected->GetY()[imass] - innerBand->GetEYlow()[imass]
	<< "   " << std::setw(15) << std::setprecision(3) << std::right << expected->GetY()[imass]
	<< "   " << std::setw(15) << std::setprecision(3) << std::right << expected->GetY()[imass] + innerBand->GetEYhigh()[imass];
      if(outerBand){
	file
	  << "   " << std::setw(15) << std::setprecision(3) << std::right << expected->GetY()[imass] + outerBand->GetEYhigh()[imass];
      }
      if(observed){
	file
	  << "   " << std::setw(15) << std::right << observed->GetY()[imass];
      }
      file
	<< std::endl;
    }
    file.close();
  }
}

void
PlotLimits::print(const char* filename, TGraph* expected, TGraph* observed, const char* type)
{
  if(std::string(type) == std::string("tex")){
    ofstream file;
    file.open (std::string(filename).append(".tex").c_str());
    file
      << "   " << std::setw(15) << std::right << "    $m_{\\mathrm H}$"
      << " & " << std::setw(15) << std::right << "$-2\\sigma$"
      << " & " << std::setw(15) << std::right << "$-1\\sigma$"
      << " & " << std::setw(15) << std::right << "     Median"
      << " & " << std::setw(15) << std::right << "$+1\\sigma$"
      << " & " << std::setw(15) << std::right << "$+2\\sigma$"
      << " & " << std::setw(15) << std::right << "Obs. Limit"
      << std::right << "  \\\\"
      << std::endl << "\\hline" << std::endl;
    unsigned int precision = 2;
    for(int imass=0; imass<expected->GetN(); ++imass){
      file
	<< "   " << std::setw(15) << std::setprecision(3) << std::resetiosflags(std::ios_base::fixed) << std::right << expected->GetX()[imass] << "~\\GeV"
	<< " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << " - "
	<< " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << " - "
	<< " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << expected->GetY()[imass]
	<< " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << " - "
	<< " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << " - ";
      if(observed){
	file
	  << " & " << std::setw(15) << std::right << observed->GetY()[imass];
      }
      file
	<< std::right << "  \\\\"
	<< std::endl << "\\hline" << std::endl;
    }
    file.close();
  }
  if(std::string(type) == std::string("txt")){
    ofstream file;
    file.open (std::string(filename).append(".txt").c_str());
    file
      << "#"
      << "   " << std::setw(15) << std::right << "         mX"
      << "   " << std::setw(15) << std::right << "   -2 sigma"
      << "   " << std::setw(15) << std::right << "   -1 sigma"
      << "   " << std::setw(15) << std::right << "     Median"
      << "   " << std::setw(15) << std::right << "   +1 sigma"
      << "   " << std::setw(15) << std::right << "   +2 sigma"
      << "   " << std::setw(15) << std::right << "Obs. Limit [pb]"
      << std::endl;
    for(int imass=0; imass<expected->GetN(); ++imass){
      file
	<< "   " << std::setw(15) << std::setprecision(3) << std::right << expected->GetX()[imass]
	<< "   " << std::setw(15) << std::setprecision(3) << std::right << " - "
	<< "   " << std::setw(15) << std::setprecision(3) << std::right << " - "
	<< "   " << std::setw(15) << std::setprecision(3) << std::right << expected->GetY()[imass]
	<< "   " << std::setw(15) << std::setprecision(3) << std::right << " - "
	<< "   " << std::setw(15) << std::setprecision(3) << std::right << " - ";
      if(observed){
	file
	  << "   " << std::setw(15) << std::right << observed->GetY()[imass];
      }
      file
	<< std::endl;
    }
    file.close();
  }
}

void
PlotLimits::print(const char* filename, TGraphAsymmErrors* outerBand_1, TGraphAsymmErrors* innerBand_1, TGraph* expected_1, TGraph* observed_1, TGraphAsymmErrors* outerBand_2, TGraphAsymmErrors* innerBand_2, TGraph* expected_2, TGraph* observed_2, double tanbLow, double tanbHigh, double tanbLowHigh, const char* type)
{
  if(std::string(type) == std::string("tex")){
    ofstream file;
    file.open (std::string(filename).append(".tex").c_str());
    file
      << "   " << std::setw(10) << std::right << "    $m_{\\mathrm H}$";
    if(outerBand_1){
      file
	<< " & " << std::setw(25) << std::right << "$-2\\sigma$";
    }
    file
      << " & " << std::setw(25) << std::right << "$-1\\sigma$"
      << " & " << std::setw(25) << std::right << "     Median"
      << " & " << std::setw(25) << std::right << "$+1\\sigma$";
    if(outerBand_1){
      file
	<< " & " << std::setw(25) << std::right << "$+2\\sigma$";
    }
    file
      << " & " << std::setw(25) << std::right << "Obs. Limit"
      << std::right << "  \\\\"
      << std::endl << "\\hline" << std::endl;
    //unsigned int precision = 2;
    for(int imass=0; imass<expected_1->GetN(); ++imass){
      char observed[50], expected[50], minus2sigma[50], minus1sigma[50], plus1sigma[50], plus2sigma[50];
      //-2sigma
      if(expected_1->GetY()[imass]-outerBand_1->GetEYlow()[imass]==tanbLowHigh && expected_2->GetY()[imass]-outerBand_2->GetEYlow()[imass]==tanbLowHigh){ //all exluded
	sprintf(minus2sigma, "%0.2f-%0.2f", tanbHigh, tanbLow);
      }
      else if(expected_1->GetY()[imass]-outerBand_1->GetEYlow()[imass]!=expected_2->GetY()[imass]-outerBand_2->GetEYlow()[imass] && expected_2->GetY()[imass]-outerBand_2->GetEYlow()[imass]!=tanbLow){ //high and low limits
	sprintf(minus2sigma, "%0.2f-%0.2f, %0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass] - outerBand_1->GetEYlow()[imass], expected_2->GetY()[imass] - outerBand_2->GetEYlow()[imass], tanbLow);
      }
      else if(expected_2->GetY()[imass]-outerBand_2->GetEYlow()[imass]==tanbLow && expected_1->GetY()[imass]-outerBand_1->GetEYlow()[imass]<=tanbHigh){ //only high limits
	sprintf(minus2sigma, "%0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass] - outerBand_1->GetEYlow()[imass]);
      }
      else if(expected_1->GetY()[imass]-outerBand_1->GetEYlow()[imass]>tanbHigh){ //nothing excluded
	sprintf(minus2sigma, "-");
      }
      //-1sigma
      if(expected_1->GetY()[imass]-innerBand_1->GetEYlow()[imass]==tanbLowHigh && expected_2->GetY()[imass]-innerBand_2->GetEYlow()[imass]==tanbLowHigh){ //all exluded
	sprintf(minus1sigma, "%0.2f-%0.2f", tanbHigh, tanbLow);
      }
      else if(expected_1->GetY()[imass]-innerBand_1->GetEYlow()[imass]!=expected_2->GetY()[imass]-innerBand_2->GetEYlow()[imass] && expected_2->GetY()[imass]-innerBand_2->GetEYlow()[imass]!=tanbLow){ //high and low limits
	sprintf(minus1sigma, "%0.2f-%0.2f, %0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass] - innerBand_1->GetEYlow()[imass], expected_2->GetY()[imass] - innerBand_2->GetEYlow()[imass], tanbLow);
      }
      else if(expected_2->GetY()[imass]-innerBand_2->GetEYlow()[imass]==tanbLow && expected_1->GetY()[imass]-innerBand_1->GetEYlow()[imass]<=tanbHigh){ //only high limits
	sprintf(minus1sigma, "%0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass] - innerBand_1->GetEYlow()[imass]);
      }
      else if(expected_1->GetY()[imass]-innerBand_1->GetEYlow()[imass]>tanbHigh){ //nothing excluded
	sprintf(minus1sigma, "-");
      }
      //expected
      if(expected_1->GetY()[imass]==expected_2->GetY()[imass]){ //all exluded
	sprintf(expected, "%0.2f-%0.2f", tanbHigh, tanbLow);
      }
      else if(expected_1->GetY()[imass]!=expected_2->GetY()[imass] && expected_2->GetY()[imass]!=tanbLow){ //high and low limits
	sprintf(expected, "%0.2f-%0.2f, %0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass], expected_2->GetY()[imass], tanbLow);
      }
      else if(expected_2->GetY()[imass]==tanbLow && expected_1->GetY()[imass]<=tanbHigh){ //only high limits
	sprintf(expected, "%0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass]);
      }
      else if(expected_1->GetY()[imass]>tanbHigh){ //nothing excluded
	sprintf(expected, "-");
      }
      //+1sigma
      if(expected_1->GetY()[imass]+innerBand_1->GetEYhigh()[imass]==tanbLowHigh && expected_2->GetY()[imass]+innerBand_2->GetEYhigh()[imass]==tanbLowHigh){ //all exluded
	sprintf(plus1sigma, "%0.2f-%0.2f", tanbHigh, tanbLow);
      }
      else if(expected_1->GetY()[imass]+innerBand_1->GetEYhigh()[imass]!=expected_2->GetY()[imass]+innerBand_2->GetEYhigh()[imass] && expected_2->GetY()[imass]+innerBand_2->GetEYhigh()[imass]!=tanbLow){ //high and low limits
	sprintf(plus1sigma, "%0.2f-%0.2f, %0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass] + innerBand_1->GetEYhigh()[imass], expected_2->GetY()[imass] + innerBand_2->GetEYhigh()[imass], tanbLow);
      }
      else if(expected_2->GetY()[imass]+innerBand_2->GetEYhigh()[imass]==tanbLow && expected_1->GetY()[imass]+innerBand_1->GetEYhigh()[imass]<=tanbHigh){ //only high limits
	sprintf(plus1sigma, "%0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass] + innerBand_1->GetEYhigh()[imass]);
      }
      else if(expected_1->GetY()[imass]+innerBand_1->GetEYhigh()[imass]>tanbHigh){ //nothing excluded
	sprintf(plus1sigma, "-");
      }
      //+2sigma
      if(expected_1->GetY()[imass]+outerBand_1->GetEYhigh()[imass]==tanbLowHigh && expected_2->GetY()[imass]+outerBand_2->GetEYhigh()[imass]==tanbLowHigh){ //all exluded
	sprintf(plus2sigma, "%0.2f-%0.2f", tanbHigh, tanbLow);
      }
      else if(expected_1->GetY()[imass]+outerBand_1->GetEYhigh()[imass]!=expected_2->GetY()[imass]+outerBand_2->GetEYhigh()[imass] && expected_2->GetY()[imass]+outerBand_2->GetEYhigh()[imass]!=tanbLow){ //high and low limits
	sprintf(plus2sigma, "%0.2f-%0.2f, %0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass] + outerBand_1->GetEYhigh()[imass], expected_2->GetY()[imass] + outerBand_2->GetEYhigh()[imass], tanbLow);
      }
      else if(expected_2->GetY()[imass]+outerBand_2->GetEYhigh()[imass]==tanbLow && expected_1->GetY()[imass]+outerBand_1->GetEYhigh()[imass]<=tanbHigh){ //only high limits
	sprintf(plus2sigma, "%0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass] + outerBand_1->GetEYlow()[imass]);
      }
      else if(expected_1->GetY()[imass]+outerBand_1->GetEYhigh()[imass]>tanbHigh){ //nothing excluded
	sprintf(plus2sigma, "-");
      }
      //observed
      if(observed_1->GetY()[imass]==observed_2->GetY()[imass]){ //all exluded
	sprintf(observed, "%0.2f-%0.2f", tanbHigh, tanbLow);
      }
      else if(observed_1->GetY()[imass]!=observed_2->GetY()[imass] && observed_2->GetY()[imass]!=tanbLow){ //high and low limits
	sprintf(observed, "%0.2f-%0.2f, %0.2f-%0.2f", tanbHigh, observed_1->GetY()[imass], observed_2->GetY()[imass], tanbLow);
      }
      else if(observed_2->GetY()[imass]==tanbLow && observed_1->GetY()[imass]<=tanbHigh){ //only high limits
	sprintf(observed, "%0.2f-%0.2f", tanbHigh, observed_1->GetY()[imass]);
      }
      else if(observed_1->GetY()[imass]>tanbHigh){ //nothing excluded
	sprintf(observed, "-");
      }
      // writing
      file
	<< "   " << std::setw(25) << std::setprecision(4) << std::resetiosflags(std::ios_base::fixed) << std::right << expected_1->GetX()[imass] << "~\\GeV";    
      if(outerBand_1){
	file
	  << " & " << std::setw(25) << std::fixed << std::right << "$" << minus2sigma << "$" ;
      }
      file
	<< " & " << std::setw(25) << std::fixed << std::right << "$" << minus2sigma << "$" 
	<< " & " << std::setw(25) << std::fixed << std::right << "$" << minus1sigma << "$" 
        << " & " << std::setw(25) << std::fixed << std::right << "$" << plus1sigma << "$" ;
      if(outerBand_1){
	file
	  << " & " << std::setw(25) << std::fixed << std::right << "$" << plus2sigma << "$" ; 
      }
      if(observed_1){
	file
	  << " & " << std::setw(25) << std::fixed << std::right << "$" << observed << "$" ;
      }
      /*if(outerBand_1){
	double value = expected_1->GetY()[imass] - outerBand_1->GetEYlow()[imass];
	int exponent = TMath::Nint(TMath::Floor(TMath::Log10(value)));
        double coeff = value/TMath::Power(10., exponent);
	if(exponent>=0){
	  file
	    << " & " << std::setw(25) << std::fixed << std::setprecision(precision) << std::right << "$" << value<< "$" ;
	}
	else{
	  file
	    << " & " << std::setw(25) << std::fixed << std::setprecision(precision) << std::right << "$" << coeff << " \\cdot 10^{" << exponent << "}$";
	}
      }
      double value = expected_1->GetY()[imass] - innerBand_1->GetEYlow()[imass];
      int exponent = TMath::Nint(TMath::Floor(TMath::Log10(value)));
      double coeff = value/TMath::Power(10., exponent);
      if(exponent>=0){
	file
	  << " & " << std::setw(25) << std::fixed << std::setprecision(precision) << std::right << "$" << value << "$" ;
      }
      else{
	file
	  << " & " << std::setw(25) << std::fixed << std::setprecision(precision) << std::right << "$" << coeff << " \\cdot 10^{" << exponent << "}$";
      }
      value =  expected_1->GetY()[imass];
      exponent = TMath::Nint(TMath::Floor(TMath::Log10(value)));
      coeff = value/TMath::Power(10., exponent);
      if(exponent>=0){
	file
	  << " & " << std::setw(25) << std::fixed << std::setprecision(precision) << std::right << "$" << value << "$" ;
      }
      else{
	file
	  << " & " << std::setw(25) << std::fixed << std::setprecision(precision) << std::right << "$" << coeff << " \\cdot 10^{" << exponent << "}$";
      }
      value = expected_1->GetY()[imass] + innerBand_1->GetEYhigh()[imass];;
      exponent = TMath::Nint(TMath::Floor(TMath::Log10(value)));
      coeff = value/TMath::Power(10., exponent);
      if(exponent>=0){
	file
	  << " & " << std::setw(25) << std::fixed << std::setprecision(precision) << std::right << "$" << value << "$";
      }
      else{
	file
	  << " & " << std::setw(25) << std::fixed << std::setprecision(precision) << std::right << "$" << coeff << " \\cdot 10^{" << exponent << "}$";
      }
      if(outerBand_1){	
	double value = expected_1->GetY()[imass] + outerBand_1->GetEYhigh()[imass];
	int exponent = TMath::Nint(TMath::Floor(TMath::Log10(value)));
        double coeff = value/TMath::Power(10., exponent);
	if(exponent>=0){
	  file
	    << " & " << std::setw(25) << std::fixed << std::setprecision(precision) << std::right << "$" << value << "$" ;
	}
	else{
	  file
	    << " & " << std::setw(25) << std::fixed << std::setprecision(precision) << std::right << "$" << coeff << " \\cdot 10^{" << exponent << "}$";
	}
      }
      if(observed_1){
	double value = observed_1->GetY()[imass];
	int exponent = TMath::Nint(TMath::Floor(TMath::Log10(value)));
        double coeff = value/TMath::Power(10., exponent);
	if(exponent>=0){
	  file
	    << " & " << std::setw(25) << std::right << "$" << value << "$" ;
	}
	else{
	  file
	    << " & " << std::setw(25) << std::right << "$" << coeff << " \\cdot 10^{" << exponent << "}$";
	}
      }*/
      file
	<< std::right << "  \\\\"
	<< std::endl << "\\hline" << std::endl;
    }
    file.close();
  }
  if(std::string(type) == std::string("txt")){
    ofstream file;
    file.open (std::string(filename).append(".txt").c_str());
    file
      << "#"
      << "   " << std::setw(10) << std::right << "         mX";
    if(outerBand_1){
      file
	<< "   " << std::setw(25) << std::right << "   -2 sigma";
    }
    file
      << "   " << std::setw(25) << std::right << "   -1 sigma"
      << "   " << std::setw(25) << std::right << "     Median"
      << "   " << std::setw(25) << std::right << "   +1 sigma";
    if(outerBand_1){
      file
	<< "   " << std::setw(25) << std::right << "   +2 sigma";
    }
    file
      << "   " << std::setw(25) << std::right << "Obs. Limit [pb]"
      << std::endl;
    for(int imass=0; imass<expected_1->GetN(); ++imass){
      char observed[50], expected[50], minus2sigma[50], minus1sigma[50], plus1sigma[50], plus2sigma[50];
      //-2sigma
      if(expected_1->GetY()[imass]-outerBand_1->GetEYlow()[imass]==tanbLowHigh && expected_2->GetY()[imass]-outerBand_2->GetEYlow()[imass]==tanbLowHigh){ //all exluded
	sprintf(minus2sigma, "%0.2f-%0.2f", tanbHigh, tanbLow);
      }
      else if(expected_1->GetY()[imass]-outerBand_1->GetEYlow()[imass]!=expected_2->GetY()[imass]-outerBand_2->GetEYlow()[imass] && expected_2->GetY()[imass]-outerBand_2->GetEYlow()[imass]!=tanbLow){ //high and low limits
	sprintf(minus2sigma, "%0.2f-%0.2f, %0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass] - outerBand_1->GetEYlow()[imass], expected_2->GetY()[imass] - outerBand_2->GetEYlow()[imass], tanbLow);
      }
      else if(expected_2->GetY()[imass]-outerBand_2->GetEYlow()[imass]==tanbLow && expected_1->GetY()[imass]-outerBand_1->GetEYlow()[imass]<=tanbHigh){ //only high limits
	sprintf(minus2sigma, "%0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass] - outerBand_1->GetEYlow()[imass]);
      }
      else if(expected_1->GetY()[imass]-outerBand_1->GetEYlow()[imass]>tanbHigh){ //nothing excluded
	sprintf(minus2sigma, "-");
      }
      //-1sigma
      if(expected_1->GetY()[imass]-innerBand_1->GetEYlow()[imass]==tanbLowHigh && expected_2->GetY()[imass]-innerBand_2->GetEYlow()[imass]==tanbLowHigh){ //all exluded
	sprintf(minus1sigma, "%0.2f-%0.2f", tanbHigh, tanbLow);
      }
      else if(expected_1->GetY()[imass]-innerBand_1->GetEYlow()[imass]!=expected_2->GetY()[imass]-innerBand_2->GetEYlow()[imass] && expected_2->GetY()[imass]-innerBand_2->GetEYlow()[imass]!=tanbLow){ //high and low limits
	sprintf(minus1sigma, "%0.2f-%0.2f, %0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass] - innerBand_1->GetEYlow()[imass], expected_2->GetY()[imass] - innerBand_2->GetEYlow()[imass], tanbLow);
      }
      else if(expected_2->GetY()[imass]-innerBand_2->GetEYlow()[imass]==tanbLow && expected_1->GetY()[imass]-innerBand_1->GetEYlow()[imass]<=tanbHigh){ //only high limits
	sprintf(minus1sigma, "%0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass] - innerBand_1->GetEYlow()[imass]);
      }
      else if(expected_1->GetY()[imass]-innerBand_1->GetEYlow()[imass]>tanbHigh){ //nothing excluded
	sprintf(minus1sigma, "-");
      }
      //expected
      if(expected_1->GetY()[imass]==expected_2->GetY()[imass]){ //all exluded
	sprintf(expected, "%0.2f-%0.2f", tanbHigh, tanbLow);
      }
      else if(expected_1->GetY()[imass]!=expected_2->GetY()[imass] && expected_2->GetY()[imass]!=tanbLow){ //high and low limits
	sprintf(expected, "%0.2f-%0.2f, %0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass], expected_2->GetY()[imass], tanbLow);
      }
      else if(expected_2->GetY()[imass]==tanbLow && expected_1->GetY()[imass]<=tanbHigh){ //only high limits
	sprintf(expected, "%0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass]);
      }
      else if(expected_1->GetY()[imass]>tanbHigh){ //nothing excluded
	sprintf(expected, "-");
      }
      //+1sigma
      if(expected_1->GetY()[imass]+innerBand_1->GetEYhigh()[imass]==tanbLowHigh && expected_2->GetY()[imass]+innerBand_2->GetEYhigh()[imass]==tanbLowHigh){ //all exluded
	sprintf(plus1sigma, "%0.2f-%0.2f", tanbHigh, tanbLow);
      }
      else if(expected_1->GetY()[imass]+innerBand_1->GetEYhigh()[imass]!=expected_2->GetY()[imass]+innerBand_2->GetEYhigh()[imass] && expected_2->GetY()[imass]+innerBand_2->GetEYhigh()[imass]!=tanbLow){ //high and low limits
	sprintf(plus1sigma, "%0.2f-%0.2f, %0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass] + innerBand_1->GetEYhigh()[imass], expected_2->GetY()[imass] + innerBand_2->GetEYhigh()[imass], tanbLow);
      }
      else if(expected_2->GetY()[imass]+innerBand_2->GetEYhigh()[imass]==tanbLow && expected_1->GetY()[imass]+innerBand_1->GetEYhigh()[imass]<=tanbHigh){ //only high limits
	sprintf(plus1sigma, "%0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass] + innerBand_1->GetEYhigh()[imass]);
      }
      else if(expected_1->GetY()[imass]+innerBand_1->GetEYhigh()[imass]>tanbHigh){ //nothing excluded
	sprintf(plus1sigma, "-");
      }
      //+2sigma
      if(expected_1->GetY()[imass]+outerBand_1->GetEYhigh()[imass]==tanbLowHigh && expected_2->GetY()[imass]+outerBand_2->GetEYhigh()[imass]==tanbLowHigh){ //all exluded
	sprintf(plus2sigma, "%0.2f-%0.2f", tanbHigh, tanbLow);
      }
      else if(expected_1->GetY()[imass]+outerBand_1->GetEYhigh()[imass]!=expected_2->GetY()[imass]+outerBand_2->GetEYhigh()[imass] && expected_2->GetY()[imass]+outerBand_2->GetEYhigh()[imass]!=tanbLow){ //high and low limits
	sprintf(plus2sigma, "%0.2f-%0.2f, %0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass] + outerBand_1->GetEYhigh()[imass], expected_2->GetY()[imass] + outerBand_2->GetEYhigh()[imass], tanbLow);
      }
      else if(expected_2->GetY()[imass]+outerBand_2->GetEYhigh()[imass]==tanbLow && expected_1->GetY()[imass]+outerBand_1->GetEYhigh()[imass]<=tanbHigh){ //only high limits
	sprintf(plus2sigma, "%0.2f-%0.2f", tanbHigh, expected_1->GetY()[imass] + outerBand_1->GetEYlow()[imass]);
      }
      else if(expected_1->GetY()[imass]+outerBand_1->GetEYhigh()[imass]>tanbHigh){ //nothing excluded
	sprintf(plus2sigma, "-");
      }
      //observed
      if(observed_1->GetY()[imass]==observed_2->GetY()[imass]){ //all exluded
	sprintf(observed, "%0.2f-%0.2f", tanbHigh, tanbLow);
      }
      else if(observed_1->GetY()[imass]!=observed_2->GetY()[imass] && observed_2->GetY()[imass]!=tanbLow){ //high and low limits
	sprintf(observed, "%0.2f-%0.2f, %0.2f-%0.2f", tanbHigh, observed_1->GetY()[imass], observed_2->GetY()[imass], tanbLow);
      }
      else if(observed_2->GetY()[imass]==tanbLow && observed_1->GetY()[imass]<=tanbHigh){ //only high limits
	sprintf(observed, "%0.2f-%0.2f", tanbHigh, observed_1->GetY()[imass]);
      }
      else if(observed_1->GetY()[imass]>tanbHigh){ //nothing excluded
	sprintf(observed, "-");
      }
      // writing 
      file
	<< "   " << std::setw(10) << std::setprecision(3) << std::right << expected_1->GetX()[imass];
      if(outerBand_1){
	file
	  << "   " << std::setw(25) << std::right << minus2sigma;
      }
      file
	<< "   " << std::setw(25) << std::right << minus1sigma
	<< "   " << std::setw(25) << std::right << expected
	<< "   " << std::setw(25) << std::right << plus1sigma;
      if(outerBand_1){
	file
	  << "   " << std::setw(25) << std::right << plus2sigma;
      }
      if(observed_1){
	file
	  << "   " << std::setw(25) << std::right << observed;
      }
      file
	<< std::endl;
    }
    file.close();
  }
}
