import argparse
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument("--setup", "-s", nargs="*", default='', dest="setuppath", help="absolute path to the setup directory, in which the operation should take place")
parser.add_argument("--channel", "-c", nargs="*", dest="channel", help="channels to be considered")
parser.add_argument("--periods", "-p", nargs="*", dest="period", help="periods to be considered")
parser.add_argument("--category", "-cat", nargs="*", dest="category", help="categories to be edited")
parser.add_argument("--add-to-signal", "-as", nargs="*", dest="addsignal", help="processes to be added to the signal")
parser.add_argument("--add-to-background", "-ab", nargs="*", default='', dest="addbackground", help="processes to be added to the background")
opt=parser.parse_args()

pattern = re.compile(r',\s*,')
## This should not only work on the cantral directory for setup in the package but on dedicated copies of that.
## I therefore made it configurable. But, Rene, how can I parse a simple string with argparse?!?
setuppath=opt.setuppath[0]
for channel in opt.channel:
    for period in opt.period:
        for category in opt.category:
            filename="{SETUP}/{CHANNEL}/cgs-sm-{PERIOD}-{CATEGORY}.conf".format(SETUP=setuppath, CHANNEL=channel, PERIOD=period, CATEGORY=category)
            infile=open(filename, 'r')
            outfile=open(filename+"_tmp", 'w')
            for line in infile:
                if "signals" in line :
                    if line[0] == '#' :
                        line=line.strip('#')
                if "GROUP signal" in line :
                    if line[0]=='#':
                        ## uncomment and remove remnants of what had been commented, in case
                        ## they exist; furthermore we need to get rid of the leading ',' for
                        ## the first element. 
                        line=line[1:line.rfind("GROUP signal")+13]
                    signalstr=''
                    for signal in opt.addsignal:
                        if not signal in line :
                            signalstr+=","+signal
                    line=line.rstrip('\n')+signalstr.strip(',')+'\n'
                    ## remove elements that might be part of signal, in case they should be moved
                    ## to background.
                    for signal in opt.addbackground:
                        line=line.replace(signal, '')
                        line = re.sub(pattern, '', line)
                if "GROUP background" in line:
                    for signal in opt.addsignal:
                        line=line.replace(signal, '')
                        line = re.sub(pattern, '', line)
                    backgroundstr=''
                    for background in opt.addbackground:
                        if not background in line :
                            backgroundstr+=","+background
                    line=line.rstrip('\n')+backgroundstr+'\n'                        
                outfile.write(line)
            os.system("mv -v %s_tmp %s"%(filename, filename))
