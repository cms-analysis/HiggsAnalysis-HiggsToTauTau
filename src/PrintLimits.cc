#include "HiggsAnalysis/HiggsToTauTau/interface/PlotLimits.h"

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
	<< "   " << std::setw(15) << std::setprecision(3) << std::resetiosflags(std::ios_base::fixed) << std::right << expected->GetX()[imass] << "~\\GeV";
      if(outerBand){
	file
	  << " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << expected->GetY()[imass] - outerBand->GetEYlow()[imass];
      }
      file
	<< " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << expected->GetY()[imass] - innerBand->GetEYlow()[imass]
	<< " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << expected->GetY()[imass]
	<< " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << expected->GetY()[imass] + innerBand->GetEYhigh()[imass];
      if(outerBand){
	file
	  << " & " << std::setw(15) << std::fixed << std::setprecision(precision) << std::right << expected->GetY()[imass] + outerBand->GetEYhigh()[imass];
      }
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

