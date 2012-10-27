#To run you need to do:
#python modify.py
#NEWFILES will be created where modified card files will be stored

import os, sys, re

os.system("mkdir NEWFILES")

modes = ["mu", "ele"]
energies = ["7TeV", "8TeV"]
specialHistos = ["W", "QCD", "TT"]

#create a simple macro that does compilation
for mode in modes:
    for energy in energies:
        file = open("test.C", "w")
        file.write("void test() {\n")
        file.write("  gROOT->ProcessLine(\".L FitTails.C+\");\n")
        file.write("  gROOT->ProcessLine(\"FitTails(\\\"" + mode + "\\\",\\\"" + energy + "\\\")\");\n")
        file.write("  gROOT->ProcessLine(\".q\");\n")
        file.write("}\n")
        file.close()
        os.system("root -l -b test.C")
os.system("rm test.C")

#all input histograms are ready to be inserted in root files

for mode in modes:
    for energy in energies:
        counter = 0

        # for debuggin, consider just first file
        #if mode <> modes[0]:
        #    continue
        #if energy <> energies[0]:
        #    continue

        file = open("produce.C", "w")
        file.write("void produce(){\n")
        
        fileName = "htt_mt.inputs-mssm-"+energy+".root"
        specialDirs = ["muTau_btag_high","muTau_btag_low","muTau_boost_high"]
        if mode == "ele":
            fileName = "htt_et.inputs-mssm-"+energy+".root"
            specialDirs = ["eleTau_btag_high","eleTau_btag_low","eleTau_boost_high"]
        file.write("  TH1F* tmp;\n")
        file.write("  TFile* in   = TFile::Open(\"" + fileName + "\");\n")
        file.write("  TFile* W0   = TFile::Open(\"" + specialDirs[0] + "_W.root\");\n")
        file.write("  TFile* W1   = TFile::Open(\"" + specialDirs[1] + "_W.root\");\n")
        file.write("  TFile* W2   = TFile::Open(\"" + specialDirs[2] + "_W.root\");\n") 
        file.write("  TFile* QCD0 = TFile::Open(\"" + specialDirs[0] + "_QCD.root\");\n")
        file.write("  TFile* QCD1 = TFile::Open(\"" + specialDirs[1] + "_QCD.root\");\n")
        file.write("  TFile* QCD2 = TFile::Open(\"" + specialDirs[2] + "_QCD.root\");\n") 
        file.write("  TFile* TT0  = TFile::Open(\"" + specialDirs[0] + "_TT.root\");\n")
        file.write("  TFile* TT1  = TFile::Open(\"" + specialDirs[1] + "_TT.root\");\n")
        file.write("  TFile* TT2  = TFile::Open(\"" + specialDirs[2] + "_TT.root\");\n") 

        file.write("  TFile* out = TFile::Open(\"NEWFILES\/" + fileName + "\",\"RECREATE\");\n") 
        
        directories = os.popen("python getDirNames.py " + fileName)
        for dir in directories:
            file.write("  out->mkdir(\"" + dir[:-1] + "\");\n")
            file.write("  out->cd(\"" + dir[:-1] + "\");\n")
            setHistos = os.popen("python getHistoNames.py " + fileName + " " + dir[:-1])
            for histo in setHistos:
                if dir[:-1] in specialDirs and histo[:-1] in specialHistos:
                    newHistoRootFile = dir[:-1] + "_" + histo[:-1] + ".root"
                    newHistos = os.popen("python getHistoNames.py " + newHistoRootFile + " ..")
                    if dir[:-1] == specialDirs[0]:
                        counter = 0
                    if dir[:-1] == specialDirs[1]:
                        counter = 1
                    if dir[:-1] == specialDirs[2]:
                        counter = 2
                    for inHisto in newHistos:
                        file.write("  tmp = (TH1F*)" + histo[:-1] + str(counter) + "->Get(\"" + inHisto[:-1] + "\");\n")
                        file.write("  tmp->Write();\n")
                        file.write("  delete tmp;\n")
                    counter += 1
                else:
                    file.write("  tmp = (TH1F*)in->Get(\"" + dir[:-1] + "/" + histo[:-1] + "\");\n")
                    file.write("  tmp->Write();\n")
                    file.write("  delete tmp;\n")
            file.write("  out->cd(\"../\");\n")
        file.write("   gROOT->ProcessLine(\".q\");\n")
        file.write("}\n")
        file.close()
        os.system("root -l produce.C")
        os.system("rm produce.C")
            
                
        
