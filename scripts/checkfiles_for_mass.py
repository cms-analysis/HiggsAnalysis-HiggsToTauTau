#!/usr/bin/env python
import os

for mass in [90 + 10*m for m in range(92)]:
	#print "Anzahl der Dateien fuer Mass {mass}: ".format(mass=mass)
	os.system("find {mass}/batch*.root | wc -l".format(mass=mass))
