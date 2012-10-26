import os, re, sys

name = sys.argv[1]

file = open("test.C", "w")
file.write("void test() {\n")
file.write("   TFile* file = TFile::Open(\"" + name + "\");\n")
file.write("   file->ls();\n")
file.write("   gROOT->ProcessLine(\".q\");\n")
file.write("}\n")
file.close()

dir = os.popen("root -l test.C")
lines = dir.readlines()
os.system("rm test.C")

dirNames = []
for line in lines:
    if len(re.split("TDirectoryFile", line)) > 1:
        dirNames += [re.split(";1", line[:-1])[1][1:],]

for name in dirNames:
    print name


