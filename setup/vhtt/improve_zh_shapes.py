#!/usr/bin/env python

# Add 145 GeV bin to LLT cards
import ROOT
ROOT.gROOT.SetBatch(True)

import os
import sys

input_filename = sys.argv[1]
output_filename = sys.argv[2]
input_file = ROOT.TFile(input_filename, "READ")
os.system("cp %s %s" % (input_filename, output_filename))
output_file = ROOT.TFile(output_filename, "UPDATE")

map_partner = {
    'eemt': 'mmmt',
    'mmmt': 'eemt',
    'eeet': 'mmet',
    'mmet': 'eeet',
    'mmme': 'eeem',
    'eeem': 'mmme',
    'eett': 'mmtt',
    'mmtt': 'eett',
}


def get_merged_shape(folder, histogram):
    initial = input_file.Get(folder + "_zh/" + histogram).Clone()
    if not initial.Integral():
        print folder, histogram, " is empty"
        return initial
    original_norm = initial.Integral()
    other = input_file.Get(map_partner[folder] + "_zh/" + histogram)
    initial.Add(other)
    initial.Scale(original_norm / initial.Integral())
    return initial


for fs in ['eemt', 'mmmt', 'eeem', 'mmme', 'eeet', 'mmet', 'mmtt', 'eett']:
    for mass in [110, 115, 120, 125, 130, 135, 140, 145]:
        hww = 'ZH_hww%i' % mass
        htt = 'ZH_htt%i' % mass
        merged_htt = get_merged_shape(fs, htt)
        output_file.cd(fs + "_zh")
        merged_htt.Write(htt, ROOT.TObject.kOverwrite)
        merged_hww = get_merged_shape(fs, hww)
        output_file.cd(fs + "_zh")
        merged_hww.Write(hww, ROOT.TObject.kOverwrite)
