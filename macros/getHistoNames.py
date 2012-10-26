import os, re, sys

name = sys.argv[1]
dir = sys.argv[2]

file = open("test.C", "w")
file.write("void test() {\n")
file.write("   TFile* file = TFile::Open(\"" + name + "\");\n")
file.write("   file->cd(\"" + dir + "\");\n")
file.write("   file->ls();\n")
file.write("   gROOT->ProcessLine(\".q\");\n")
file.write("}\n")
file.close()

dir = os.popen("root -l test.C")
lines = dir.readlines()
os.system("rm test.C")

histoNames = []
for line in lines:
    if len(re.split("TDirectoryFile", line)) == 1 and len(re.split("TFile", line)) == 1:
        elements = re.split("TH1F\t", line)
        if len(re.split("KEY", elements[0])) > 1:
            print re.split(";", elements[1])[0]
