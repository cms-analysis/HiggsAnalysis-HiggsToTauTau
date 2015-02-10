#include <iostream>
#include <vector>
#include <map>
#include <fstream>

#include "TCanvas.h"
#include "TGraphErrors.h"
#include "TLatex.h"
#include "TH2F.h"
#include "TStyle.h"
#include "TROOT.h"

#include "boost/regex.hpp"
#include "boost/format.hpp"
#include "boost/algorithm/string.hpp"
#include "boost/program_options.hpp"

namespace po = boost::program_options;
using namespace std;

// A struct and some functions extracted from framework and reproduced here
struct Pull {
  std::string name;
  double      prefit;
  double      prefit_err;
  double      bonly;
  double      bonly_err;
  double      splusb;
  double      splusb_err;
  double      rho;
  void Print() const;
};
void SetTdrStyle();
void PullsFromFile(std::string const& filename, std::vector<Pull> & pullvec, bool verbose);
std::vector<std::string> ParseFileLines(std::string const& file_name);
bool BvsSBComparator(Pull const& pull1, Pull const& pull2);

int main(int argc, char* argv[]){
  // Define and parse arguments 
  string input1, name1;
  bool splusb_1;
  string input2, name2;
  bool splusb_2;
  bool draw_difference;
  bool draw_first;
  string output;
  vector<string> filter_regex_str;

  po::options_description help_config("Help");
  help_config.add_options()
    ("help,h", "produce help message");
  po::options_description config("Configuration");
  config.add_options()
    ("input1",                po::value<string>(&input1)->required(), "The first file containing pulls [REQUIRED]")
    ("input2",                po::value<string>(&input2)->required(), "The second file containing pulls [REQUIRED]")
    ("label1",                po::value<string>(&name1)->default_value("input1"), "A label for the first input")
    ("label2",                po::value<string>(&name2)->default_value("input2"), "A label for the second input")
    ("output",                po::value<string>(&output)->default_value(""), "output filename")
    ("sb1",                   po::value<bool>(&splusb_1)->required(), "Use s+b pulls from the first file? [REQUIRED]")
    ("sb2",                   po::value<bool>(&splusb_2)->required(), "Use s+b pulls from the second file? [REQUIRED]")
    ("draw_difference",       po::value<bool>(&draw_difference)->default_value(true), "Draw the difference between inputs")
    ("draw_first",            po::value<bool>(&draw_first)->default_value(false), "Draw only first")
    ("filter_regex",          po::value<vector<string>>(&filter_regex_str), "A regular expression to filter pulls");
  po::variables_map vm;
  po::store(po::command_line_parser(argc, argv).options(help_config).allow_unregistered().run(), vm);
  po::notify(vm);
  if (vm.count("help")) {
    cout << config << "\n";
    cout << "Example usage: " << endl;
    cout << "print-pulls --input1=mlfit_a.txt --input2=mlfit_b.txt --label1=\"PullsA\" --label2=\"PullsB\" --sb1=true --sb2=false --filter_regex=\".*_bin_.*\"" << endl;
    return 1;
  }
  po::store(po::command_line_parser(argc, argv).options(config).allow_unregistered().run(), vm);
  po::notify(vm);

  // Build a list of regular expressions to filter nuisances
  std::vector<boost::regex> filter_regex;
  for (unsigned i = 0; i < filter_regex_str.size(); ++i) {
    filter_regex.push_back(boost::regex(filter_regex_str[i]));
    std::cout << "Filter nuisances with regex: " << filter_regex_str[i] << std::endl;
  }

  // Set a nice drawing style  
  SetTdrStyle();

  // Extract pulls from the two input files
  std::vector<Pull> pulls1;
  std::vector<Pull> pulls2;
  PullsFromFile(input1, pulls1, false);
  PullsFromFile(input2, pulls2, false);

  // Build new lists of the pulls common to both inputs, and in the same order
  std::vector<Pull> pulls1sorted;
  std::vector<Pull> pulls2sorted;
  for (unsigned i = 0; i < pulls1.size(); ++i) {
    bool found = false;
    for (unsigned j = 0; j < pulls2.size(); ++j) {
      if (pulls1[i].name == pulls2[j].name) {
        found = true;
        pulls2sorted.push_back(pulls2[j]);
        continue;
      }
    }
    if (found == true) pulls1sorted.push_back(pulls1[i]);
  }

  // Build a final vector of pulls taking b-only or s+b for each input respectively
  // Skip pulls that match one of the filter regex
  std::vector<Pull> final;
  for (unsigned i = 0; i < pulls1sorted.size(); ++i) {
    bool skip = false;
    for (unsigned j = 0; j < filter_regex.size(); ++j) {
      if (boost::regex_match(pulls1sorted[i].name, filter_regex[j])) skip = true;
    }
    if (skip) continue;
    Pull pull;
    pull.name = pulls1sorted[i].name;
    pull.bonly = splusb_1 ? pulls1sorted[i].splusb : pulls1sorted[i].bonly ;
    pull.bonly_err = splusb_1 ? pulls1sorted[i].splusb_err : pulls1sorted[i].bonly_err ;
    pull.splusb = splusb_2 ? pulls2sorted[i].splusb : pulls2sorted[i].bonly ;
    pull.splusb_err = splusb_2 ? pulls2sorted[i].splusb_err : pulls2sorted[i].bonly_err ;
    final.push_back(pull);
  }
  std::sort(final.begin(), final.end(), BvsSBComparator);
  unsigned npulls = final.size();


  // Prepare the canvas
  TCanvas canv("canvas", "canvas", draw_difference ? 1200 : 800 , 1200);
  canv.cd();
  canv.Update();
  TPad* pad1 = NULL;
  TPad* pad2 = NULL;
  if (draw_difference) {
    pad1 = new TPad("pad1","pad1",0, 0, 0.85, 1);
    pad2 = new TPad("pad2","pad2",0.85, 0, 1, 1);
    pad1->Draw();
    pad2->Draw();
  } else {
    pad1 = new TPad("pad1","pad1",0, 0, 1, 1);
  }
  pad1->SetBottomMargin(0.07);
  pad1->SetLeftMargin(0.45);
  pad1->SetRightMargin(0.03);
  pad1->SetTopMargin(0.05);
  pad1->SetGrid(1,0);
  pad1->Draw();
  pad1->cd();

  // Create a dummy TH2F to attach the nuisance labels
  // and TGraphErrors for each set of pulls
  TH2F *hpulls = new TH2F("pulls","pulls", 6, -3, 3, npulls, 0, npulls);
  TGraphErrors vals(npulls);
  TGraphErrors vals2(npulls);
  float ts1 = 30./(pad1->GetWw()*pad1->GetAbsWNDC());
  for (unsigned i = 0; i < final.size(); ++i) {
    vals.SetPoint(i, final[i].bonly, double(i) + 0.5);
    vals.SetPointError(i, final[i].bonly_err, 0);
    vals2.SetPoint(i, final[i].splusb, double(i) + 0.5);
    vals2.SetPointError(i, final[i].splusb_err, 0);
    hpulls->GetYaxis()->SetBinLabel(i+1, final[i].name.c_str());
  }
  hpulls->GetYaxis()->LabelsOption("v");
  hpulls->SetStats(false);
  hpulls->GetYaxis()->SetLabelSize(0.03);
  gStyle->SetEndErrorSize(5);
  hpulls->GetXaxis()->SetTitle("Pull (#sigma)");
  hpulls->GetXaxis()->CenterTitle();
  hpulls->GetXaxis()->SetTitleSize(0.04);
  hpulls->Draw("");
  hpulls->GetXaxis()->SetLabelSize(ts1);
  vals.Draw("pSAME");
  vals.SetLineWidth(2);
  vals2.SetLineWidth(2);
  vals.SetMarkerStyle(20);
  vals2.SetMarkerStyle(24);
  vals2.SetLineColor(4);
  vals2.SetMarkerColor(4);
  if(!draw_first) vals2.Draw("pSAME");
  canv.Update();

  TGraphErrors valsd;
  if (pad2) {
    pad2->cd();
    pad2->SetBottomMargin(0.07);
    pad2->SetLeftMargin(0.1);
    pad2->SetRightMargin(0.2);
    pad2->SetTopMargin(0.05);
    pad2->SetGrid(1,0);
    TH2F *hpulldiff = new TH2F("pulldiff","pulldiff", 2, -0.5, 0.5, npulls, 0, npulls);
    hpulldiff->GetYaxis()->SetLabelSize(0.0);
    hpulldiff->GetYaxis()->SetTitleSize(0.0);
    valsd = TGraphErrors(npulls);
    for (unsigned i = 0; i < final.size(); ++i) {
      valsd.SetPoint(i, final[i].splusb-final[i].bonly, double(i) + 0.5);
      valsd.SetPointError(i, 0, 0);
    }
    hpulldiff->SetStats(false);
    if (name1 == "") name1 = input1;
    if (name2 == "") name2 = input2;
    float ts2 = 30./(pad2->GetWw()*pad2->GetAbsWNDC());
    hpulldiff->GetXaxis()->SetLabelSize(ts2);
    hpulldiff->GetXaxis()->SetLabelOffset(-0.105);
    hpulldiff->GetXaxis()->SetNdivisions(502);
    hpulldiff->Draw("");
    valsd.Draw("pSAME");
    valsd.SetMarkerStyle(20);
    valsd.SetMarkerColor(4);
    canv.Update();
  }
  canv.cd();
  TLatex *title_latex = new TLatex();
  title_latex->SetNDC();
  title_latex->SetTextSize(0.03);
  title_latex->SetTextAlign(31);
  if(!draw_first) title_latex->DrawLatex(0.95,0.965, (std::string(name1) + (splusb_1?"(s+b)":"(b-only)") + " vs. #color[4]{" + name2 + "}" + (splusb_2?"(s+b)":"(b-only)")).c_str());
  else title_latex->DrawLatex(0.95,0.965, (std::string(name1) + (splusb_1?"(s+b)":"(b-only)")).c_str());
  canv.Update();
  if (output == "") output = ("compare_pulls_"+name1+(splusb_1?"_sb_":"_b_")+name2+(splusb_2?"_sb":"_b"));
  canv.SaveAs((output+".pdf").c_str());
  canv.SaveAs((output+".png").c_str());
  return 0;
}


void SetTdrStyle() {
  gStyle->SetCanvasBorderMode(0);
  gStyle->SetCanvasColor(kWhite);
  gStyle->SetCanvasDefH(700); //Height of canvas
  gStyle->SetCanvasDefW(700); //Width of canvas

  gStyle->SetCanvasDefX(0);   //POsition on screen
  gStyle->SetCanvasDefY(0);

  // For the Pad:
  gStyle->SetPadBorderMode(0);
  // gStyle->SetPadBorderSize(Width_t size = 1);
  gStyle->SetPadColor(kWhite);
  gStyle->SetPadGridX(false);
  gStyle->SetPadGridY(false);
  gStyle->SetGridColor(0);
  gStyle->SetGridStyle(3);
  gStyle->SetGridWidth(1);

  // For the frame:
  gStyle->SetFrameBorderMode(0);
  gStyle->SetFrameBorderSize(10);
  gStyle->SetFrameFillColor(0);
  gStyle->SetFrameFillStyle(0);
  gStyle->SetFrameLineColor(1);
  gStyle->SetFrameLineStyle(0);
  gStyle->SetFrameLineWidth(2);

  // For the histo:
  // gStyle->SetHistFillColor(1);
  // gStyle->SetHistFillStyle(0);
  gStyle->SetHistLineColor(1);
  gStyle->SetHistLineStyle(0);
  gStyle->SetHistLineWidth(short(0.1));
  // gStyle->SetLegoInnerR(Float_t rad = 0.5);
  // gStyle->SetNumberContours(Int_t number = 20);

  gStyle->SetEndErrorSize(0);
  //gStyle->SetErrorMarker(20);
  gStyle->SetErrorX(0.5);

  gStyle->SetMarkerStyle(20);

  //For the fit/function:
  gStyle->SetOptFit(1);
  gStyle->SetFitFormat("5.4g");
  gStyle->SetFuncColor(2);
  gStyle->SetFuncStyle(1);
  gStyle->SetFuncWidth(1);

  //For the date:
  gStyle->SetOptDate(0);
  // gStyle->SetDateX(Float_t x = 0.01);
  // gStyle->SetDateY(Float_t y = 0.01);

  // For the statistics box:
  //  gStyle->SetOptFile(0);
  gStyle->SetOptStat(1);
  gStyle->SetOptStat("MRn");
  gStyle->SetStatColor(kWhite);
  gStyle->SetStatFont(42);
  gStyle->SetStatFontSize(0.04);///---> gStyle->SetStatFontSize(0.025);
  gStyle->SetStatTextColor(1);
  gStyle->SetStatFormat("6.4g");
  gStyle->SetStatBorderSize(1);
  gStyle->SetStatH(0.1);
  gStyle->SetStatW(0.2);///---> gStyle->SetStatW(0.15);

  // gStyle->SetStatStyle(Style_t style = 1001);
  // gStyle->SetStatX(Float_t x = 0);
  // gStyle->SetStatY(Float_t y = 0);

  // Margins:
  gStyle->SetPadTopMargin(0.05);
  gStyle->SetPadBottomMargin(0.10);
  gStyle->SetPadLeftMargin(0.16);
  gStyle->SetPadRightMargin(0.05);

  // For the Global title:

  gStyle->SetOptTitle(0);
  gStyle->SetTitleFont(42);
  gStyle->SetTitleColor(1);
  gStyle->SetTitleTextColor(1);
  gStyle->SetTitleFillColor(10);
  gStyle->SetTitleFontSize(0.05);
  // gStyle->SetTitleH(0); // Set the height of the title box
  // gStyle->SetTitleW(0); // Set the width of the title box
  // gStyle->SetTitleX(0); // Set the position of the title box
  // gStyle->SetTitleY(0.985); // Set the position of the title box
  // gStyle->SetTitleStyle(Style_t style = 1001);
  // gStyle->SetTitleBorderSize(2);

  // For the axis titles:

  gStyle->SetTitleColor(1, "XYZ");
  gStyle->SetTitleFont(42, "XYZ");
  gStyle->SetTitleSize(0.05, "XYZ");
  // gStyle->SetTitleXSize(Float_t size = 0.02); // Another way to set the size?
  // gStyle->SetTitleYSize(Float_t size = 0.02);
  gStyle->SetTitleXOffset(0.9);
  gStyle->SetTitleYOffset(1.55);
  // gStyle->SetTitleOffset(1.1, "Y"); // Another way to set the Offset

  // For the axis labels:

  gStyle->SetLabelColor(1, "XYZ");
  gStyle->SetLabelFont(42, "XYZ");
  gStyle->SetLabelOffset(0.007, "XYZ");
  gStyle->SetLabelSize(0.04, "XYZ");

  // For the axis:

  gStyle->SetAxisColor(1, "XYZ");
  gStyle->SetStripDecimals(kTRUE);
  gStyle->SetTickLength(0.02, "XYZ");
  gStyle->SetNdivisions(510, "XYZ");
  gStyle->SetPadTickX(1);  // To get tick marks on the opposite side of the frame
  gStyle->SetPadTickY(1);

  // Change for log plots:
  gStyle->SetOptLogx(0);
  gStyle->SetOptLogy(0);
  gStyle->SetOptLogz(0);
  gStyle->SetLineStyleString(11,"20 10");

  // Postscript options:
  //  gStyle->SetPaperSize(20.,20.);
  // gStyle->SetLineScalePS(Float_t scale = 3);
  // gStyle->SetLineStyleString(Int_t i, const char* text);
  // gStyle->SetHeaderPS(const char* header);
  // gStyle->SetTitlePS(const char* pstitle);

  // gStyle->SetBarOffset(Float_t baroff = 0.5);
  // gStyle->SetBarWidth(Float_t barwidth = 0.5);
  // gStyle->SetPaintTextFormat(const char* format = "g");
  // gStyle->SetPalette(Int_t ncolors = 0, Int_t* colors = 0);
  // gStyle->SetTimeOffset(Double_t toffset);
  // gStyle->SetHistMinimumZero(kTRUE);

  //   gStyle->cd();

  gROOT->ForceStyle();
}

void PullsFromFile(std::string const& filename, std::vector<Pull> & pullvec, bool verbose) {
  std::vector<std::string> lines = ParseFileLines(filename);
  for (unsigned i = 0; i < lines.size(); ++i) {
    boost::erase_all(lines[i],"*");
    boost::erase_all(lines[i],"!");
    std::vector<std::string> blocks;
    boost::split(blocks, lines[i], boost::is_any_of(" "), boost::token_compress_on);
    if (blocks.size() > 0) {
      if (blocks[0] == "name") continue;
    }
    if (blocks.size() == 15) {
      pullvec.push_back(Pull());
      Pull & new_pull = pullvec.back();
      new_pull.name = blocks[0];
      new_pull.prefit = boost::lexical_cast<double>(blocks[1]);
      new_pull.prefit_err = boost::lexical_cast<double>(blocks[3]);
      new_pull.bonly = boost::lexical_cast<double>(blocks[4]);
      new_pull.bonly_err = boost::lexical_cast<double>(blocks[6]);
      new_pull.splusb = boost::lexical_cast<double>(blocks[9]);
      new_pull.splusb_err = boost::lexical_cast<double>(blocks[11]);
      new_pull.rho = boost::lexical_cast<double>(blocks[14]);
      if (verbose) new_pull.Print();
    }
    for (unsigned j = 0; j < blocks.size(); ++j) {
    }
  }
}

bool BvsSBComparator(Pull const& pull1, Pull const& pull2) {
  return ( fabs(pull1.bonly - pull1.splusb) > fabs(pull2.bonly - pull2.splusb) );
}

std::vector<std::string> ParseFileLines(std::string const& file_name) {
  // Build a vector of input files
  std::vector<std::string> files;
  std::ifstream file;
  file.open(file_name.c_str());
  if (!file.is_open()) {
    std::cerr << "Warning: File " << file_name << " cannot be opened." << std::endl;
    return files;
  }
  std::string line = "";
  while(std::getline(file, line)) {//while loop through lines
    files.push_back(line);
  }
  file.close();
  return files;
}

void Pull::Print() const {
  std::cout << boost::format("%-60s %-4.2f +/- %-4.2f   %+-4.2f +/- %-4.2f   %+-4.2f +/- %-4.2f   %+-4.2f \n")
    % name % prefit %prefit_err % bonly % bonly_err % splusb % splusb_err % rho;
}




