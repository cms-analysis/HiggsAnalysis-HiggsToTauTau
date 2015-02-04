#!/usr/bin/env python

import os
import glob
#import re

new_file = open("HplusNuisanceFile.dat", 'w')

for datacard in glob.glob("*.txt") :
    file = open(datacard, 'r')
    masses = datacard.rstrip(".txt").split("_m")
    print masses, masses[1]
    for line in file :
        words=line.split()
        if len(words) < 2 :
            #print line
            continue
        new_line=""
        idx=0
        if words[1]=="lnN" :
            new_line=masses[1]+" "
            for idx, word in enumerate(line.split(" ")) :
                #print word
                new_line=new_line+word
                new_line=new_line+" "
                idx=idx+1
        if new_line.endswith(" ") :
            new_file.write(new_line.rstrip(" "))
        else :
            new_file.write(new_line)
    file.close()
        


