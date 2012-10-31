#!/usr/bin/env python

# Add 145 GeV bin to LLT cards
import ROOT
ROOT.gROOT.SetBatch(True)


def add(filepath, tev):
    file = ROOT.TFile(filepath, "UPDATE")
    for dir in ["emt", "mmt"]:
        print "Adding 145 GeV point in", dir
        file.cd(dir)
        htt_145 = ROOT.gDirectory.Get("WH140").Clone("WH145")
        hww_145 = ROOT.gDirectory.Get("WH_hww140").Clone("WH_hww145")
        xsec_scale = 0.3406 / 0.3761 if tev == 7 else 0.4164 / 0.4713
        tt_br_scale = 2.61E-02 / 3.52E-02
        ww_br_scale = 6.00E-01 / 5.01E-01

        htt_145.Scale(xsec_scale * tt_br_scale)
        hww_145.Scale(xsec_scale * ww_br_scale)
        htt_145.Write()
        hww_145.Write()

add('vhtt.inputs-sm-7TeV.root', 7)
add('vhtt.inputs-sm-8TeV.root', 8)
