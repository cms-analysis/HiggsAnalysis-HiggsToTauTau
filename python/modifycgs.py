import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--channel", "-c", nargs="*", dest="channel", help="channels to be considered")
parser.add_argument("--periods", "-p", nargs="*", dest="period", help="periods to be considered")
parser.add_argument("--category", "-cat", nargs="*", dest="category", help="categories to be edited")
parser.add_argument("--add-to-signal", "-as", nargs="*", dest="addsignal", help="processes to be added to the signal")
parser.add_argument("--add-to-background", "-ab", nargs="*", default='', dest="addbackground", help="processes to be added to the background")
opt=parser.parse_args()

setuppath="%s/src/HiggsAnalysis/HiggsToTauTau/setup"%os.getenv("CMSSW_BASE")

for channel in opt.channel:
    for period in opt.period:
        for category in opt.category:
            filename="{SETUP}/{CHANNEL}/cgs-sm-{PERIOD}-{CATEGORY}.conf".format(SETUP=setuppath, CHANNEL=channel, PERIOD=period, CATEGORY=category)
            infile=open(filename, 'r')
            outfile=open(filename+"_tmp", 'w')
            for line in infile:
                if "GROUP signal" in line and line[0]=='#':
                    line=line[1:]
                    for signal in opt.addsignal:
                        line=line.rstrip("\n")
                        line+=", "+signal+"\n"
                    for signal in opt.addbackground:
                        if signal+", " in line:
                            line=line.replace(signal+", ", "") #change to re.sub()
                        if ", "+signal in line:
                            line=line.replace(", "+signal, "")
                if "GROUP background" in line:
                    for signal in opt.addsignal:
                        if signal+", " in line:
                            line=line.replace(signal+", ", "")
                        if ", "+signal in line:
                            line=line.replace(", "+signal, "")
                    for signal in opt.addbackground:
                        line+=", "+signal
                outfile.write(line)
            os.system("mv -v %s_tmp %s"%(filename, filename))
