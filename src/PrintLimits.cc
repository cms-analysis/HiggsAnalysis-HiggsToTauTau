#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

/*void 
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
}*/

void 
PlotLimits::print(const char* filename, std::string& xval, std::string& yval, TGraph* contour, const char* type)
{
  if(std::string(type) == std::string("tex")){
    ofstream file;
    file.open (std::string(filename).append(".tex").c_str());
    file
      << "   " << std::setw(15) << std::right << xval << " (pb) " 
      << " & " << std::setw(15) << std::right << yval << " (pb) "
      << std::right << "  \\\\"
      << std::endl << "\\hline" << std::endl;
      unsigned int precision = 5;
      for(int idx=0; idx<contour->GetN(); ++idx){
	file
	  << "   " << std::setw(15) << std::fixed << std::scientific << std::setprecision(precision) << std::right << contour->GetX()[idx]
	  << " & " << std::setw(15) << std::fixed << std::scientific << std::setprecision(precision) << std::right << contour->GetY()[idx]
	  << std::right << "  \\\\"
	  << std::endl << "\\hline" << std::endl;
      }
  }
  if(std::string(type) == std::string("txt")){
    ofstream file;
    file.open (std::string(filename).append(".txt").c_str());
    file
      << "   " << std::setw(15) << std::right << xval 
      << "   " << std::setw(15) << std::right << yval
      << std::endl;
    unsigned int precision = 5;
    for(int idx=0; idx<contour->GetN(); ++idx){
      file
	<< "   " << std::setw(15) << std::fixed << std::scientific << std::setprecision(precision) << std::right << contour->GetX()[idx]
	<< "   " << std::setw(15) << std::fixed << std::scientific << std::setprecision(precision) << std::right << contour->GetY()[idx]
	<< std::endl;
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
PlotLimits::print(const char* filename, std::vector<TGraph*> minus2sigma, std::vector<TGraph*> minus1sigma, std::vector<TGraph*> expected, std::vector<TGraph*> plus1sigma, std::vector<TGraph*> plus2sigma, std::vector<TGraph*> observed, double tanbLow, double tanbHigh, float *mass, const char* type)
{
  ofstream file;
  if(std::string(type) == std::string("tex")){
    file.open (std::string(filename).append(".tex").c_str());
    file
      << "   " << std::setw(10) << std::right << "    $m_{\\mathrm H}$";
    if(minus2sigma[0]){
      file
	<< " & " << std::setw(25) << std::right << "$-2\\sigma$";
    }
    file
      << " & " << std::setw(25) << std::right << "$-1\\sigma$"
      << " & " << std::setw(25) << std::right << "     Median"
      << " & " << std::setw(25) << std::right << "$+1\\sigma$";
    if(plus2sigma[0]){
      file
	<< " & " << std::setw(25) << std::right << "$+2\\sigma$";
    }
    file
      << " & " << std::setw(25) << std::right << "Obs. Limit"
      << std::right << "  \\\\"
      << std::endl << "\\hline" << std::endl;
  }

  if(std::string(type) == std::string("txt")){
    file.open (std::string(filename).append(".txt").c_str());
    file
      << "#"
      << "   " << std::setw(10) << std::right << "         mX";
    if(minus2sigma[0]){
      file
	<< "   " << std::setw(25) << std::right << "   -2 sigma";
    }
    file
      << "   " << std::setw(25) << std::right << "   -1 sigma"
      << "   " << std::setw(25) << std::right << "     Median"
      << "   " << std::setw(25) << std::right << "   +1 sigma";
    if(plus2sigma[0]){
      file
	<< "   " << std::setw(25) << std::right << "   +2 sigma";
    }
    file
      << "   " << std::setw(25) << std::right << "Obs. Limit [pb]"
      << std::endl;
  }

  for(unsigned int k=0; k<expected.size(); k++)
    {
      std::string char_observed, char_expected, char_minus2sigma, char_minus1sigma, char_plus1sigma, char_plus2sigma;
      
      //minus 2 sigma
      double max=-1, min=999;
      for(int j=0; j<minus2sigma[k]->GetN(); j++){
	if(minus2sigma[k]->GetY()[j] < min) min=minus2sigma[k]->GetY()[j];
	if(minus2sigma[k]->GetY()[j] > max) max=minus2sigma[k]->GetY()[j];	  
      }
      if(max < 1)  char_minus2sigma=TString::Format("%0.2f-%0.2f; ", tanbHigh, tanbLow); //all excluded
      else if(min > 1) char_minus2sigma=TString::Format("- "); //nothing excluded
      else{ //everything else
	double save;
	if(minus2sigma[k]->GetY()[minus2sigma[k]->GetN()-1]>1) save=minus2sigma[k]->GetY()[minus2sigma[k]->GetN()-1];
	else{
	  char_minus2sigma=TString::Format("%0.2f-", tanbHigh);
	  save=minus2sigma[k]->GetY()[minus2sigma[k]->GetN()-1];
	}
	for(int i=minus2sigma[k]->GetN()-2; i>=1; i--){
	  if(minus2sigma[k]->GetY()[i]>1 && save<1){ //out of excluded
	    double slope=(minus2sigma[k]->GetY()[i]-minus2sigma[k]->GetY()[i+1])/(minus2sigma[k]->GetX()[i]-minus2sigma[k]->GetX()[i+1]);
	    double constant=minus2sigma[k]->GetY()[i]-minus2sigma[k]->GetX()[i]*slope; 
	    char_minus2sigma+=TString::Format("%0.2f; ", (1-constant)/slope);
	    save=minus2sigma[k]->GetY()[i];
	  }
	  else if(minus2sigma[k]->GetY()[i]>1 && save>1) { //stay out of excluded
	    save=minus2sigma[k]->GetY()[i];
	  }
	  else if(minus2sigma[k]->GetY()[i]<1 && save<1) { //stay in excluded
	    save=minus2sigma[k]->GetY()[i];
	  }
	  else if(minus2sigma[k]->GetY()[i]<1 && save>1) {  //get in excluded
	    double slope=(minus2sigma[k]->GetY()[i]-minus2sigma[k]->GetY()[i+1])/(minus2sigma[k]->GetX()[i]-minus2sigma[k]->GetX()[i+1]);
	    double constant=minus2sigma[k]->GetY()[i]-minus2sigma[k]->GetX()[i]*slope; 
	    char_minus2sigma+=TString::Format("%0.2f-", (1-constant)/slope);
	    save=minus2sigma[k]->GetY()[i];
	  }
	}
	if(minus2sigma[k]->GetY()[0]>1 && save<1){
	  double slope=(minus2sigma[k]->GetY()[1]-minus2sigma[k]->GetY()[0])/(minus2sigma[k]->GetX()[1]-minus2sigma[k]->GetX()[0]);
	  double constant=minus2sigma[k]->GetY()[1]-minus2sigma[k]->GetX()[1]*slope; 
	  char_minus2sigma+=TString::Format("%0.2f; ", (1-constant)/slope);
	  save=minus2sigma[k]->GetY()[0];
	}
	else if(minus2sigma[k]->GetY()[0]>1 && save>1){
	  save=minus2sigma[k]->GetY()[0];
	}
	else if(minus2sigma[k]->GetY()[0]<1 && save<1){ 
	  char_minus2sigma+=TString::Format("%0.2f; ", tanbLow);
	  save=minus2sigma[k]->GetY()[0];
	}
	else if(minus2sigma[k]->GetY()[0]<1 && save>1){
	  double slope=(minus2sigma[k]->GetY()[1]-minus2sigma[k]->GetY()[0])/(minus2sigma[k]->GetX()[1]-minus2sigma[k]->GetX()[0]);
	  double constant=minus2sigma[k]->GetY()[1]-minus2sigma[k]->GetX()[1]*slope; 
	  char_minus2sigma+=TString::Format("%0.2f-%0.2f; ", (1-constant)/slope, tanbLow);
	  save=minus2sigma[k]->GetY()[0];
	}
      }
      
      //minus 1 sigma
      max=-1, min=999;
      for(int j=0; j<minus1sigma[k]->GetN(); j++){
	if(minus1sigma[k]->GetY()[j] < min) min=minus1sigma[k]->GetY()[j];
	if(minus1sigma[k]->GetY()[j] > max) max=minus1sigma[k]->GetY()[j];	  
      }
      if(max < 1)  char_minus1sigma=TString::Format("%0.2f-%0.2f; ", tanbHigh, tanbLow); //all excluded
      else if(min > 1) char_minus1sigma=TString::Format("- "); //nothing excluded
      else{ //everything else
	double save;
	if(minus1sigma[k]->GetY()[minus1sigma[k]->GetN()-1]>1) save=minus1sigma[k]->GetY()[minus1sigma[k]->GetN()-1];
	else{
	  char_minus1sigma=TString::Format("%0.2f-", tanbHigh);
	  save=minus1sigma[k]->GetY()[minus1sigma[k]->GetN()-1];
	}
	for(int i=minus1sigma[k]->GetN()-2; i>=1; i--){
	  if(minus1sigma[k]->GetY()[i]>1 && save<1){ //out of excluded
	    double slope=(minus1sigma[k]->GetY()[i]-minus1sigma[k]->GetY()[i+1])/(minus1sigma[k]->GetX()[i]-minus1sigma[k]->GetX()[i+1]);
	    double constant=minus1sigma[k]->GetY()[i]-minus1sigma[k]->GetX()[i]*slope; 
	    char_minus1sigma+=TString::Format("%0.2f; ", (1-constant)/slope);
	    save=minus1sigma[k]->GetY()[i];
	  }
	  else if(minus1sigma[k]->GetY()[i]>1 && save>1) { //stay out of excluded
	    save=minus1sigma[k]->GetY()[i];
	  }
	  else if(minus1sigma[k]->GetY()[i]<1 && save<1) { //stay in excluded
	    save=minus1sigma[k]->GetY()[i];
	  }
	  else if(minus1sigma[k]->GetY()[i]<1 && save>1) {  //get in excluded
	    double slope=(minus1sigma[k]->GetY()[i]-minus1sigma[k]->GetY()[i+1])/(minus1sigma[k]->GetX()[i]-minus1sigma[k]->GetX()[i+1]);
	    double constant=minus1sigma[k]->GetY()[i]-minus1sigma[k]->GetX()[i]*slope; 
	    char_minus1sigma+=TString::Format("%0.2f-", (1-constant)/slope);
	    save=minus1sigma[k]->GetY()[i];
	  }
	}
	if(minus1sigma[k]->GetY()[0]>1 && save<1){
	  double slope=(minus1sigma[k]->GetY()[1]-minus1sigma[k]->GetY()[0])/(minus1sigma[k]->GetX()[1]-minus1sigma[k]->GetX()[0]);
	  double constant=minus1sigma[k]->GetY()[1]-minus1sigma[k]->GetX()[1]*slope; 
	  char_minus1sigma+=TString::Format("%0.2f; ", (1-constant)/slope);
	  save=minus1sigma[k]->GetY()[0];
	}
	else if(minus1sigma[k]->GetY()[0]>1 && save>1){
	  save=minus1sigma[k]->GetY()[0];
	}
	else if(minus1sigma[k]->GetY()[0]<1 && save<1){ 
	  char_minus1sigma+=TString::Format("%0.2f; ", tanbLow);
	  save=minus1sigma[k]->GetY()[0];
	}
	else if(minus1sigma[k]->GetY()[0]<1 && save>1){
	  double slope=(minus1sigma[k]->GetY()[1]-minus1sigma[k]->GetY()[0])/(minus1sigma[k]->GetX()[1]-minus1sigma[k]->GetX()[0]);
	  double constant=minus1sigma[k]->GetY()[1]-minus1sigma[k]->GetX()[1]*slope; 
	  char_minus1sigma+=TString::Format("%0.2f-%0.2f; ", (1-constant)/slope, tanbLow);
	  save=minus1sigma[k]->GetY()[0];
	}
      }
      
      //expected
      max=-1, min=999;
      for(int j=0; j<expected[k]->GetN(); j++){
	if(expected[k]->GetY()[j] < min) min=expected[k]->GetY()[j];
	if(expected[k]->GetY()[j] > max) max=expected[k]->GetY()[j];	  
      }
      if(max < 1)  char_expected=TString::Format("%0.2f-%0.2f; ", tanbHigh, tanbLow); //all excluded
      else if(min > 1) char_expected=TString::Format("- "); //nothing excluded
      else{ //everything else
	double save;
	if(expected[k]->GetY()[expected[k]->GetN()-1]>1) save=expected[k]->GetY()[expected[k]->GetN()-1];
	else{
	  char_expected=TString::Format("%0.2f-", tanbHigh);
	  save=expected[k]->GetY()[expected[k]->GetN()-1];
	}
	for(int i=expected[k]->GetN()-2; i>=1; i--){
	  if(expected[k]->GetY()[i]>1 && save<1){ //out of excluded
	    double slope=(expected[k]->GetY()[i]-expected[k]->GetY()[i+1])/(expected[k]->GetX()[i]-expected[k]->GetX()[i+1]);
	    double constant=expected[k]->GetY()[i]-expected[k]->GetX()[i]*slope; 
	    char_expected+=TString::Format("%0.2f; ", (1-constant)/slope);
	    save=expected[k]->GetY()[i];
	  }
	  else if(expected[k]->GetY()[i]>1 && save>1) { //stay out of excluded
	    save=expected[k]->GetY()[i];
	  }
	  else if(expected[k]->GetY()[i]<1 && save<1) { //stay in excluded
	    save=expected[k]->GetY()[i];
	  }
	  else if(expected[k]->GetY()[i]<1 && save>1) {  //get in excluded
	    double slope=(expected[k]->GetY()[i]-expected[k]->GetY()[i+1])/(expected[k]->GetX()[i]-expected[k]->GetX()[i+1]);
	    double constant=expected[k]->GetY()[i]-expected[k]->GetX()[i]*slope; 
	    char_expected+=TString::Format("%0.2f-", (1-constant)/slope);
	    save=expected[k]->GetY()[i];
	  }
	}
	if(expected[k]->GetY()[0]>1 && save<1){
	  double slope=(expected[k]->GetY()[1]-expected[k]->GetY()[0])/(expected[k]->GetX()[1]-expected[k]->GetX()[0]);
	  double constant=expected[k]->GetY()[1]-expected[k]->GetX()[1]*slope; 
	  char_expected+=TString::Format("%0.2f; ", (1-constant)/slope);
	  save=expected[k]->GetY()[0];
	}
	else if(expected[k]->GetY()[0]>1 && save>1){
	  save=expected[k]->GetY()[0];
	}
	else if(expected[k]->GetY()[0]<1 && save<1){ 
	  char_expected+=TString::Format("%0.2f; ", tanbLow);
	  save=expected[k]->GetY()[0];
	}
	else if(expected[k]->GetY()[0]<1 && save>1){
	  double slope=(expected[k]->GetY()[1]-expected[k]->GetY()[0])/(expected[k]->GetX()[1]-expected[k]->GetX()[0]);
	  double constant=expected[k]->GetY()[1]-expected[k]->GetX()[1]*slope; 
	  char_expected+=TString::Format("%0.2f-%0.2f; ", (1-constant)/slope, tanbLow);
	  save=expected[k]->GetY()[0];
	}
      }
      
      //plus 1 sigma
      max=-1, min=999;
      for(int j=0; j<plus1sigma[k]->GetN(); j++){
	if(plus1sigma[k]->GetY()[j] < min) min=plus1sigma[k]->GetY()[j];
	if(plus1sigma[k]->GetY()[j] > max) max=plus1sigma[k]->GetY()[j];	  
      }
      if(max < 1)  char_plus1sigma=TString::Format("%0.2f-%0.2f; ", tanbHigh, tanbLow); //all excluded
      else if(min > 1) char_plus1sigma=TString::Format("- "); //nothing excluded
      else{ //everything else
	double save;
	if(plus1sigma[k]->GetY()[plus1sigma[k]->GetN()-1]>1) save=plus1sigma[k]->GetY()[plus1sigma[k]->GetN()-1];
	else{
	  char_plus1sigma=TString::Format("%0.2f-", tanbHigh);
	  save=plus1sigma[k]->GetY()[plus1sigma[k]->GetN()-1];
	}
	for(int i=plus1sigma[k]->GetN()-2; i>=1; i--){
	  if(plus1sigma[k]->GetY()[i]>1 && save<1){ //out of excluded
	    double slope=(plus1sigma[k]->GetY()[i]-plus1sigma[k]->GetY()[i+1])/(plus1sigma[k]->GetX()[i]-plus1sigma[k]->GetX()[i+1]);
	    double constant=plus1sigma[k]->GetY()[i]-plus1sigma[k]->GetX()[i]*slope; 
	    char_plus1sigma+=TString::Format("%0.2f; ", (1-constant)/slope);
	    save=plus1sigma[k]->GetY()[i];
	  }
	  else if(plus1sigma[k]->GetY()[i]>1 && save>1) { //stay out of excluded
	    save=plus1sigma[k]->GetY()[i];
	  }
	  else if(plus1sigma[k]->GetY()[i]<1 && save<1) { //stay in excluded
	    save=plus1sigma[k]->GetY()[i];
	  }
	  else if(plus1sigma[k]->GetY()[i]<1 && save>1) {  //get in excluded
	    double slope=(plus1sigma[k]->GetY()[i]-plus1sigma[k]->GetY()[i+1])/(plus1sigma[k]->GetX()[i]-plus1sigma[k]->GetX()[i+1]);
	    double constant=plus1sigma[k]->GetY()[i]-plus1sigma[k]->GetX()[i]*slope; 
	    char_plus1sigma+=TString::Format("%0.2f-", (1-constant)/slope);
	    save=plus1sigma[k]->GetY()[i];
	  }
	}
	if(plus1sigma[k]->GetY()[0]>1 && save<1){
	  double slope=(plus1sigma[k]->GetY()[1]-plus1sigma[k]->GetY()[0])/(plus1sigma[k]->GetX()[1]-plus1sigma[k]->GetX()[0]);
	  double constant=plus1sigma[k]->GetY()[1]-plus1sigma[k]->GetX()[1]*slope; 
	  char_plus1sigma+=TString::Format("%0.2f; ", (1-constant)/slope);
	  save=plus1sigma[k]->GetY()[0];
	}
	else if(plus1sigma[k]->GetY()[0]>1 && save>1){
	  save=plus1sigma[k]->GetY()[0];
	}
	else if(plus1sigma[k]->GetY()[0]<1 && save<1){ 
	  char_plus1sigma+=TString::Format("%0.2f; ", tanbLow);
	  save=plus1sigma[k]->GetY()[0];
	}
	else if(plus1sigma[k]->GetY()[0]<1 && save>1){
	  double slope=(plus1sigma[k]->GetY()[1]-plus1sigma[k]->GetY()[0])/(plus1sigma[k]->GetX()[1]-plus1sigma[k]->GetX()[0]);
	  double constant=plus1sigma[k]->GetY()[1]-plus1sigma[k]->GetX()[1]*slope; 
	  char_plus1sigma+=TString::Format("%0.2f-%0.2f; ", (1-constant)/slope, tanbLow);
	  save=plus1sigma[k]->GetY()[0];
	}
      }
      
      //plus 2 sigma
      max=-1, min=999;
      for(int j=0; j<plus2sigma[k]->GetN(); j++){
	if(plus2sigma[k]->GetY()[j] < min) min=plus2sigma[k]->GetY()[j];
	if(plus2sigma[k]->GetY()[j] > max) max=plus2sigma[k]->GetY()[j];	  
      }
      if(max < 1)  char_plus2sigma=TString::Format("%0.2f-%0.2f; ", tanbHigh, tanbLow); //all excluded
      else if(min > 1) char_plus2sigma=TString::Format("- "); //nothing excluded
      else{ //everything else
	double save;
	if(plus2sigma[k]->GetY()[plus2sigma[k]->GetN()-1]>1) save=plus2sigma[k]->GetY()[plus2sigma[k]->GetN()-1];
	else{
	  char_plus2sigma=TString::Format("%0.2f-", tanbHigh);
	  save=plus2sigma[k]->GetY()[plus2sigma[k]->GetN()-1];
	}
	for(int i=plus2sigma[k]->GetN()-2; i>=1; i--){
	  if(plus2sigma[k]->GetY()[i]>1 && save<1){ //out of excluded
	    double slope=(plus2sigma[k]->GetY()[i]-plus2sigma[k]->GetY()[i+1])/(plus2sigma[k]->GetX()[i]-plus2sigma[k]->GetX()[i+1]);
	    double constant=plus2sigma[k]->GetY()[i]-plus2sigma[k]->GetX()[i]*slope; 
	    char_plus2sigma+=TString::Format("%0.2f; ", (1-constant)/slope);
	    save=plus2sigma[k]->GetY()[i];
	  }
	  else if(plus2sigma[k]->GetY()[i]>1 && save>1) { //stay out of excluded
	    save=plus2sigma[k]->GetY()[i];
	  }
	  else if(plus2sigma[k]->GetY()[i]<1 && save<1) { //stay in excluded
	    save=plus2sigma[k]->GetY()[i];
	  }
	  else if(plus2sigma[k]->GetY()[i]<1 && save>1) {  //get in excluded
	    double slope=(plus2sigma[k]->GetY()[i]-plus2sigma[k]->GetY()[i+1])/(plus2sigma[k]->GetX()[i]-plus2sigma[k]->GetX()[i+1]);
	    double constant=plus2sigma[k]->GetY()[i]-plus2sigma[k]->GetX()[i]*slope; 
	    char_plus2sigma+=TString::Format("%0.2f-", (1-constant)/slope);
	    save=plus2sigma[k]->GetY()[i];
	  }
	}
	if(plus2sigma[k]->GetY()[0]>1 && save<1){
	  double slope=(plus2sigma[k]->GetY()[1]-plus2sigma[k]->GetY()[0])/(plus2sigma[k]->GetX()[1]-plus2sigma[k]->GetX()[0]);
	  double constant=plus2sigma[k]->GetY()[1]-plus2sigma[k]->GetX()[1]*slope; 
	  char_plus2sigma+=TString::Format("%0.2f; ", (1-constant)/slope);
	  save=plus2sigma[k]->GetY()[0];
	}
	else if(plus2sigma[k]->GetY()[0]>1 && save>1){
	  save=plus2sigma[k]->GetY()[0];
	}
	else if(plus2sigma[k]->GetY()[0]<1 && save<1){ 
	  char_plus2sigma+=TString::Format("%0.2f;", tanbLow);
	  save=plus2sigma[k]->GetY()[0];
	}
	else if(plus2sigma[k]->GetY()[0]<1 && save>1){
	  double slope=(plus2sigma[k]->GetY()[1]-plus2sigma[k]->GetY()[0])/(plus2sigma[k]->GetX()[1]-plus2sigma[k]->GetX()[0]);
	  double constant=plus2sigma[k]->GetY()[1]-plus2sigma[k]->GetX()[1]*slope; 
	  char_plus2sigma+=TString::Format("%0.2f-%0.2f; ", (1-constant)/slope, tanbLow);
	  save=plus2sigma[k]->GetY()[0];
	}
      }
      
      //observed
      max=-1, min=999;
      for(int j=0; j<observed[k]->GetN(); j++){
	if(observed[k]->GetY()[j] < min) min=observed[k]->GetY()[j];
	if(observed[k]->GetY()[j] > max) max=observed[k]->GetY()[j];	  
      }
      if(max < 1)  char_observed=TString::Format("%0.2f-%0.2f; ", tanbHigh, tanbLow); //all excluded
      else if(min > 1) char_observed=TString::Format("- "); //nothing excluded
      else{ //everything else
	double save;
	if(observed[k]->GetY()[observed[k]->GetN()-1]>1) save=observed[k]->GetY()[observed[k]->GetN()-1];
	else{
	  char_observed=TString::Format("%0.2f-", tanbHigh);
	  save=observed[k]->GetY()[observed[k]->GetN()-1];
	}
	for(int i=observed[k]->GetN()-2; i>=1; i--){
	  if(observed[k]->GetY()[i]>1 && save<1){ //out of excluded
	    double slope=(observed[k]->GetY()[i]-observed[k]->GetY()[i+1])/(observed[k]->GetX()[i]-observed[k]->GetX()[i+1]);
	    double constant=observed[k]->GetY()[i]-observed[k]->GetX()[i]*slope; 
	    char_observed+=TString::Format("%0.2f; ", (1-constant)/slope);
	    save=observed[k]->GetY()[i];
	  }
	  else if(observed[k]->GetY()[i]>1 && save>1) { //stay out of excluded
	    save=observed[k]->GetY()[i];
	  }
	  else if(observed[k]->GetY()[i]<1 && save<1) { //stay in excluded
	    save=observed[k]->GetY()[i];
	  }
	  else if(observed[k]->GetY()[i]<1 && save>1) {  //get in excluded
	    double slope=(observed[k]->GetY()[i]-observed[k]->GetY()[i+1])/(observed[k]->GetX()[i]-observed[k]->GetX()[i+1]);
	    double constant=observed[k]->GetY()[i]-observed[k]->GetX()[i]*slope; 
	    char_observed+=TString::Format("%0.2f-", (1-constant)/slope);
	    save=observed[k]->GetY()[i];
	  }
	}
	if(observed[k]->GetY()[0]>1 && save<1){
	  double slope=(observed[k]->GetY()[1]-observed[k]->GetY()[0])/(observed[k]->GetX()[1]-observed[k]->GetX()[0]);
	  double constant=observed[k]->GetY()[1]-observed[k]->GetX()[1]*slope; 
	  char_observed+=TString::Format("%0.2f; ", (1-constant)/slope);
	  save=observed[k]->GetY()[0];
	}
	else if(observed[k]->GetY()[0]>1 && save>1){
	  save=observed[k]->GetY()[0];
	}
	else if(observed[k]->GetY()[0]<1 && save<1){ 
	  char_observed+=TString::Format("%0.2f; ", tanbLow);
	  save=observed[k]->GetY()[0];
	}
	else if(observed[k]->GetY()[0]<1 && save>1){
	  double slope=(observed[k]->GetY()[1]-observed[k]->GetY()[0])/(observed[k]->GetX()[1]-observed[k]->GetX()[0]);
	  double constant=observed[k]->GetY()[1]-observed[k]->GetX()[1]*slope; 
	  char_observed+=TString::Format("%0.2f-%0.2f; ", (1-constant)/slope, tanbLow);
	  save=observed[k]->GetY()[0];
	}
      }
      
      // writing
      if(std::string(type) == std::string("tex")){
	file
	  << "   " << std::setw(25) << std::setprecision(4) << std::resetiosflags(std::ios_base::fixed) << std::right << mass[k] << "~\\GeV";    
	if(minus2sigma[k]){
	  file
	    << " & " << std::setw(25) << std::fixed << std::right << "$" << char_minus2sigma << "$" ;
	}
	file
	  << " & " << std::setw(25) << std::fixed << std::right << "$" << char_minus1sigma << "$" 
	  << " & " << std::setw(25) << std::fixed << std::right << "$" << char_expected << "$" 
	  << " & " << std::setw(25) << std::fixed << std::right << "$" << char_plus1sigma << "$" ;
	if(plus2sigma[k]){
	  file
	    << " & " << std::setw(25) << std::fixed << std::right << "$" << char_plus2sigma << "$" ; 
	}
	if(observed[k]){
	  file
	    << " & " << std::setw(25) << std::fixed << std::right << "$" << char_observed << "$" ;
	}
	file
	  << std::right << "  \\\\"
	  << std::endl << "\\hline" << std::endl;
      }
      
      if(std::string(type) == std::string("txt")){
	file
	  << "   " << std::setw(10) << std::setprecision(3) << std::right << mass[k];
	if(minus2sigma[k]){
	  file
	    << "   " << std::setw(25) << std::right << char_minus2sigma;
	}
	file
	  << "   " << std::setw(25) << std::right << char_minus1sigma
	  << "   " << std::setw(25) << std::right << char_expected
	  << "   " << std::setw(25) << std::right << char_plus1sigma;
	if(plus2sigma[k]){
	  file
	    << "   " << std::setw(25) << std::right << char_plus2sigma;
	}
	if(observed[k]){
	  file
	    << "   " << std::setw(25) << std::right << char_observed;
	}
	file
	  << std::endl;
      }
    }
  file.close();
}

void
PlotLimits::print(const char* filename, TGraphAsymmErrors* outerBand_1, TGraphAsymmErrors* innerBand_1, TGraph* expected_1, TGraph* observed_1, TGraphAsymmErrors* outerBand_2, TGraphAsymmErrors* innerBand_2, TGraph* expected_2, TGraph* observed_2, double tanbLow, double tanbHigh, double tanbLowHigh, const char* type)
{
  if(std::string(type) == std::string("tex")){
    //new tex format (v1)
    ofstream file;
    file.open (std::string(filename).append("-v1.tex").c_str());
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
	<< " & " << std::setw(25) << std::fixed << std::right << "$" << minus1sigma << "$" 
	<< " & " << std::setw(25) << std::fixed << std::right << "$" << expected << "$" 
        << " & " << std::setw(25) << std::fixed << std::right << "$" << plus1sigma << "$" ;
      if(outerBand_1){
	file
	  << " & " << std::setw(25) << std::fixed << std::right << "$" << plus2sigma << "$" ; 
      }
      if(observed_1){
	file
	  << " & " << std::setw(25) << std::fixed << std::right << "$" << observed << "$" ;
      }
      file
	<< std::right << "  \\\\"
	<< std::endl << "\\hline" << std::endl;
    }
    file.close();
  //new tex format (v2)
    ofstream file_v2;
    file_v2.open (std::string(filename).append("-v2.tex").c_str());
    file_v2
      << "   " << std::setw(10) << std::right << "    $m_{\\mathrm H}$";
    if(outerBand_1){
      file_v2
	<< " & " << std::setw(25) << std::right << "$-2\\sigma$";
    }
    file_v2
      << " & " << std::setw(25) << std::right << "$-1\\sigma$"
      << " & " << std::setw(25) << std::right << "     Median"
      << " & " << std::setw(25) << std::right << "$+1\\sigma$";
    if(outerBand_1){
      file_v2
	<< " & " << std::setw(25) << std::right << "$+2\\sigma$";
    }
    file_v2
      << " & " << std::setw(25) << std::right << "Obs. Limit"
      << std::right << "  \\\\"
      << std::endl << "\\hline" << std::endl;
    //unsigned int precision = 2;
    for(int imass=0; imass<expected_1->GetN(); ++imass){
      char observed[50], expected[50], minus2sigma[50], minus1sigma[50], plus1sigma[50], plus2sigma[50];
      //-2sigma
      if(expected_1->GetY()[imass]-outerBand_1->GetEYlow()[imass]==tanbLowHigh && expected_2->GetY()[imass]-outerBand_2->GetEYlow()[imass]==tanbLowHigh){ //all exluded
	sprintf(minus2sigma, ">%0.1f", tanbLow);
      }
      else if(expected_1->GetY()[imass]-outerBand_1->GetEYlow()[imass]!=expected_2->GetY()[imass]-outerBand_2->GetEYlow()[imass] && expected_2->GetY()[imass]-outerBand_2->GetEYlow()[imass]!=tanbLow){ //high and low limits
	sprintf(minus2sigma, ">%0.1f, <%0.1f", expected_1->GetY()[imass] - outerBand_1->GetEYlow()[imass], expected_2->GetY()[imass] - outerBand_2->GetEYlow()[imass]);
      }
      else if(expected_2->GetY()[imass]-outerBand_2->GetEYlow()[imass]==tanbLow && expected_1->GetY()[imass]-outerBand_1->GetEYlow()[imass]<=tanbHigh){ //only high limits
	sprintf(minus2sigma, ">%0.1f", expected_1->GetY()[imass] - outerBand_1->GetEYlow()[imass]);
      }
      else if(expected_1->GetY()[imass]-outerBand_1->GetEYlow()[imass]>tanbHigh){ //nothing excluded
	sprintf(minus2sigma, "-");
      }
      //-1sigma
      if(expected_1->GetY()[imass]-innerBand_1->GetEYlow()[imass]==tanbLowHigh && expected_2->GetY()[imass]-innerBand_2->GetEYlow()[imass]==tanbLowHigh){ //all exluded
	sprintf(minus1sigma, ">%0.1f", tanbLow);
      }
      else if(expected_1->GetY()[imass]-innerBand_1->GetEYlow()[imass]!=expected_2->GetY()[imass]-innerBand_2->GetEYlow()[imass] && expected_2->GetY()[imass]-innerBand_2->GetEYlow()[imass]!=tanbLow){ //high and low limits
	sprintf(minus1sigma, ">%0.1f, <%0.1f", expected_1->GetY()[imass] - innerBand_1->GetEYlow()[imass], expected_2->GetY()[imass] - innerBand_2->GetEYlow()[imass]);
      }
      else if(expected_2->GetY()[imass]-innerBand_2->GetEYlow()[imass]==tanbLow && expected_1->GetY()[imass]-innerBand_1->GetEYlow()[imass]<=tanbHigh){ //only high limits
	sprintf(minus1sigma, ">%0.1f", expected_1->GetY()[imass] - innerBand_1->GetEYlow()[imass]);
      }
      else if(expected_1->GetY()[imass]-innerBand_1->GetEYlow()[imass]>tanbHigh){ //nothing excluded
	sprintf(minus1sigma, "-");
      }
      //expected
      if(expected_1->GetY()[imass]==expected_2->GetY()[imass]){ //all exluded
	sprintf(expected, ">%0.1f", tanbLow);
      }
      else if(expected_1->GetY()[imass]!=expected_2->GetY()[imass] && expected_2->GetY()[imass]!=tanbLow){ //high and low limits
	sprintf(expected, ">%0.1f, <%0.1f", expected_1->GetY()[imass], expected_2->GetY()[imass]);
      }
      else if(expected_2->GetY()[imass]==tanbLow && expected_1->GetY()[imass]<=tanbHigh){ //only high limits
	sprintf(expected, ">%0.1f", expected_1->GetY()[imass]);
      }
      else if(expected_1->GetY()[imass]>tanbHigh){ //nothing excluded
	sprintf(expected, "-");
      }
      //+1sigma
      if(expected_1->GetY()[imass]+innerBand_1->GetEYhigh()[imass]==tanbLowHigh && expected_2->GetY()[imass]+innerBand_2->GetEYhigh()[imass]==tanbLowHigh){ //all exluded
	sprintf(plus1sigma, ">%0.1f", tanbLow);
      }
      else if(expected_1->GetY()[imass]+innerBand_1->GetEYhigh()[imass]!=expected_2->GetY()[imass]+innerBand_2->GetEYhigh()[imass] && expected_2->GetY()[imass]+innerBand_2->GetEYhigh()[imass]!=tanbLow){ //high and low limits
	sprintf(plus1sigma, ">%0.1f, <%0.1f", expected_1->GetY()[imass] + innerBand_1->GetEYhigh()[imass], expected_2->GetY()[imass] + innerBand_2->GetEYhigh()[imass]);
      }
      else if(expected_2->GetY()[imass]+innerBand_2->GetEYhigh()[imass]==tanbLow && expected_1->GetY()[imass]+innerBand_1->GetEYhigh()[imass]<=tanbHigh){ //only high limits
	sprintf(plus1sigma, ">%0.1f", expected_1->GetY()[imass] + innerBand_1->GetEYhigh()[imass]);
      }
      else if(expected_1->GetY()[imass]+innerBand_1->GetEYhigh()[imass]>tanbHigh){ //nothing excluded
	sprintf(plus1sigma, "-");
      }
      //+2sigma
      if(expected_1->GetY()[imass]+outerBand_1->GetEYhigh()[imass]==tanbLowHigh && expected_2->GetY()[imass]+outerBand_2->GetEYhigh()[imass]==tanbLowHigh){ //all exluded
	sprintf(plus2sigma, ">%0.1f", tanbLow);
      }
      else if(expected_1->GetY()[imass]+outerBand_1->GetEYhigh()[imass]!=expected_2->GetY()[imass]+outerBand_2->GetEYhigh()[imass] && expected_2->GetY()[imass]+outerBand_2->GetEYhigh()[imass]!=tanbLow){ //high and low limits
	sprintf(plus2sigma, ">%0.1f, <%0.1f", expected_1->GetY()[imass] + outerBand_1->GetEYhigh()[imass], expected_2->GetY()[imass] + outerBand_2->GetEYhigh()[imass]);
      }
      else if(expected_2->GetY()[imass]+outerBand_2->GetEYhigh()[imass]==tanbLow && expected_1->GetY()[imass]+outerBand_1->GetEYhigh()[imass]<=tanbHigh){ //only high limits
	sprintf(plus2sigma, ">%0.1f", expected_1->GetY()[imass] + outerBand_1->GetEYlow()[imass]);
      }
      else if(expected_1->GetY()[imass]+outerBand_1->GetEYhigh()[imass]>tanbHigh){ //nothing excluded
	sprintf(plus2sigma, "-");
      }
      //observed
      if(observed_1->GetY()[imass]==observed_2->GetY()[imass]){ //all exluded
	sprintf(observed, ">%0.1f", tanbLow);
      }
      else if(observed_1->GetY()[imass]!=observed_2->GetY()[imass] && observed_2->GetY()[imass]!=tanbLow){ //high and low limits
	sprintf(observed, ">%0.1f, <%0.1f", observed_1->GetY()[imass], observed_2->GetY()[imass]);
      }
      else if(observed_2->GetY()[imass]==tanbLow && observed_1->GetY()[imass]<=tanbHigh){ //only high limits
	sprintf(observed, ">%0.1f", observed_1->GetY()[imass]);
      }
      else if(observed_1->GetY()[imass]>tanbHigh){ //nothing excluded
	sprintf(observed, "-");
      }
      // writing
      file_v2
	<< "   " << std::setw(25) << std::setprecision(4) << std::resetiosflags(std::ios_base::fixed) << std::right << expected_1->GetX()[imass] << "~\\GeV";    
      if(outerBand_1){
	file_v2
	  << " & " << std::setw(25) << std::fixed << std::right << "$" << minus2sigma << "$" ;
      }
      file_v2
	<< " & " << std::setw(25) << std::fixed << std::right << "$" << minus1sigma << "$" 
	<< " & " << std::setw(25) << std::fixed << std::right << "$" << expected << "$" 
        << " & " << std::setw(25) << std::fixed << std::right << "$" << plus1sigma << "$" ;
      if(outerBand_1){
	file_v2
	  << " & " << std::setw(25) << std::fixed << std::right << "$" << plus2sigma << "$" ; 
      }
      if(observed_1){
	file_v2
	  << " & " << std::setw(25) << std::fixed << std::right << "$" << observed << "$" ;
      }
      file_v2
	<< std::right << "  \\\\"
	<< std::endl << "\\hline" << std::endl;
    }
    file_v2.close();
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
