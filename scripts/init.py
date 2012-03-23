#!/usr/bin/env python

import os

os.system("python {CMSSW_BASE}/src/data/init-data.py".format(CMSSW_BASE=os.environ.get("CMSSW_BASE")))
os.system("python {CMSSW_BASE}/src/data/init-setup.py".format(CMSSW_BASE=os.environ.get("CMSSW_BASE")))
