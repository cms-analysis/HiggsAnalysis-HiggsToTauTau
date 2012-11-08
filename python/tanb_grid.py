#!/usr/bin/env python

from optparse import OptionParser

parser = OptionParser(usage="usage: %prog [options] datacatd.txt",
                      description="Main script to create individual a modified datacard for given mass and tanb value.")
parser.add_option("-m", "--mA",    dest="mA",       default=120.,  type="float",   help="Value of mA. [Default: 120.]")
parser.add_option("-t", "--tanb",  dest="tanb",     default='20.',   type="string",   help="Values of tanb. [Default: 20.]")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="Run in verbose mode")
parser.add_option("--sm-like", dest="sm_like", default=False, action="store_true", help="Do not divide by the value of tanb, but only scale to MSSM xsec according to tanb value. (Will result in typical SM limit on signal strength for given value of tanb). Used for debugging. [Default: False]")
parser.add_option("--no-acc-corr", dest="no_acc_corr", default=False, action="store_true", help="Do not apply acceptance corrections for masswindow that has been applied for cross section calculation. Kept for legacy. [Default: False]")
parser.add_option("--model", dest="model", default='HiggsAnalysis/HiggsToTauTau/data/out.mhmax-mu+200-{PERIOD}-{tanbRegion}-nnlo.root', type="string", help="Model to be applied for the limit calculation. [Default: 'HiggsAnalysis/HiggsToTauTau/data/out.mhmax-mu+200-{PERIOD}-{tanbRegion}-nnlo.root']")
parser.add_option("--interpolation", dest="interpolation_mode", default='mode-1', type="choice", help="Mode for mass interpolation for direct tanb limits. Choices are: mode-0 -- non-degenerate-masses for all htt channels, mode-1 -- non-degenerate-masses for classic htt channels non-degenerate-masses-light for htt_mm, mode-2 -- non-degenerate-masses for classic htt channels degenerate-masses for htt_mm, mode-3 -- non-degenerate-masses-light for all htt channels, mode-4 -- non-degenerate-masses-light for classic htt channels degenerate-masses for htt_mm, mode-5 -- degenerate-masses for all htt channels [Default: mode-1]", choices=["mode-0", "mode-1", "mode-2", "mode-3", "mode-4", "mode-5"])
(options, args) = parser.parse_args()

import re
import os
import math
import sys
import shutil
import ROOT

higgs_file = open("higgs_mass.dat", 'a')

ROOT.gSystem.Load('$CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit.so') #can be removed after including interplolate2D to package
#ROOT.gSystem.Load('$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/interpolate2D/th1fmorph_cc.so') ##- don't has to be included i guess
#ROOT.gSystem.Load('$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/interpolate2D/th2fmorph_cc.so') ##- th2 morphing not armed yet
from ROOT import th1fmorph
# from ROOT import th1fmorph, th2fmorph - th2 morphing not armed yet
from HiggsAnalysis.HiggsToTauTau.tools.mssm_xsec_tools import mssm_xsec_tools
from HiggsAnalysis.HiggsToTauTau.acceptance_correction import interval 
from HiggsAnalysis.HiggsToTauTau.acceptance_correction import acceptance_correction 

class MakeDatacard :
       def __init__(self, tanb, mA, model="HiggsAnalysis/HiggsToTauTau/data/out.mhmax-mu+200-{PERIOD}-{tanbRegion}-nnlo.root", feyn_higgs_model="", sm_like=False, acc_corr=True) :
              ## full path for the input file for the htt xsec tools, expected in the data directory of the package
              ## This file is used to determine the cross sections and uncertainties for calculations for htt, as
              ## as for determining the masses for htt and hww
              self.mssm_xsec_tools_input_path = model
              ## model to be used exploiting the feyn-higgs calculations also for htt. This is the case for model,
              ## which have not been provided by the MSSM cross section group. In this cases the cross sections
              ## are calculated from feyn-higgs, while the uncertainties are stil taken from the MSSM cross section
              ## group on the basis of the default mhmax scenario
              self.feyn_higgs_model = feyn_higgs_model
              ## do not divide yields by value of tanb but only rescale by xsec for given value of tanb
              self.sm_like = sm_like
              ## apply acceptance corrections for restricted mass window in cross section calculation or not
              self.acc_corr = acc_corr
              ## tanb as float
              self.tanb = tanb
              ## mA as float
              self.mA = mA
              ## mH as float (filled from htt tools)
              self.mH = 0.
              ## mh as float (filled from htt tools)
              self.mh = 0.
              ## cross point in mA from where on for hww the contribution from h dominates over the contribution from H
              self.hww_cross_point = 250
              ## mapping of unique (standardized) production process names to all possible kinds of production processes (=histograms)
              self.standardized_production_processes = {
                      "ggH":["SM", "GGH", "ggH", "VH"
                             "GGHNoJet", "GGHJet", "Higgs_gg_mssm_"] ## patch for tests with old HIG-11-029 cards only 
                     ,"bbH":["BBH", "bbH",
                             "BBHNoJet", "BBHJet", "Higgs_bb_mssm_"] ## patch for tests with old HIG-11-029 cards only 
                     ,"qqH":["VBF", "qqH", "vbf"]
                     ,"ZH" :["ZH"]
                     ,"WH" :["WH"]
                     }
              ## mapping of unique (standardized) decay channel names to all possible decay channels
              self.standardized_decay_channels = {
                     "hmm"    : ["hmm_0", "hmm_1",
                                 ],
                     "htt"    : ["htt_em_0_7TeV", "htt_em_1_7TeV", "htt_em_2_7TeV", "htt_em_3_7TeV", "htt_em_4_7TeV", "htt_em_5_7TeV", "htt_em_6_7TeV", "htt_em_7_7TeV", "htt_em_8_7TeV", "htt_em_9_7TeV",
                                 "htt_et_0_7TeV", "htt_et_1_7TeV", "htt_et_2_7TeV", "htt_et_3_7TeV", "htt_et_4_7TeV", "htt_et_5_7TeV", "htt_et_6_7TeV", "htt_et_7_7TeV", "htt_et_8_7TeV", "htt_et_9_7TeV",
                                 "htt_mt_0_7TeV", "htt_mt_1_7TeV", "htt_mt_2_7TeV", "htt_mt_3_7TeV", "htt_mt_4_7TeV", "htt_mt_5_7TeV", "htt_mt_6_7TeV", "htt_mt_7_7TeV", "htt_mt_8_7TeV", "htt_mt_9_7TeV",
                                 "htt_mm_0_7TeV", "htt_mm_1_7TeV", "htt_mm_2_7TeV", "htt_mm_3_7TeV", "htt_mm_4_7TeV", "htt_mm_5_7TeV", "htt_mm_6_7TeV", "htt_mm_7_7TeV", "htt_mm_8_7TeV", "htt_mm_9_7TeV",
                                 "htt_em_0_8TeV", "htt_em_1_8TeV", "htt_em_2_8TeV", "htt_em_3_8TeV", "htt_em_4_8TeV", "htt_em_5_8TeV", "htt_em_6_8TeV", "htt_em_7_8TeV", "htt_em_8_8TeV", "htt_em_9_8TeV",
                                 "htt_et_0_8TeV", "htt_et_1_8TeV", "htt_et_2_8TeV", "htt_et_3_8TeV", "htt_et_4_8TeV", "htt_et_5_8TeV", "htt_et_6_8TeV", "htt_et_7_8TeV", "htt_et_8_8TeV", "htt_et_9_8TeV",
                                 "htt_mt_0_8TeV", "htt_mt_1_8TeV", "htt_mt_2_8TeV", "htt_mt_3_8TeV", "htt_mt_4_8TeV", "htt_mt_5_8TeV", "htt_mt_6_8TeV", "htt_mt_7_8TeV", "htt_mt_8_8TeV", "htt_mt_9_8TeV",
                                 "htt_mm_0_8TeV", "htt_mm_1_8TeV", "htt_mm_2_8TeV", "htt_mm_3_8TeV", "htt_mm_4_8TeV", "htt_mm_5_8TeV", "htt_mm_6_8TeV", "htt_mm_7_8TeV", "htt_mm_8_8TeV", "htt_mm_9_8TeV",
                                 ],
                     "hww"    : ["hwwof_0j_shape", "hwwof_1j_shape",
                                 "hwwsf_0j_shape", "hwwsf_1j_shape",
                                 "hww_2j_cut"
                                 ],
                     "vhtt"   : ["vhtt_mmt_mumu_final_MuTauMass",
                                 "vhtt_emt_emu_final_SubleadingMass"
                                 ]
                     }
              ## list of signal indexes in input datacard
              self.signal_indexes = []
              ## list of all(!) available decay channels in the input datacard
              self.decay_channels_ = []
              ## list of initial datacards that went into combineCards.py from first line of input datacard
              self.initial_datacards = []
              ## list of all(!) available production processes (=histograms) in the input datacard
              self.production_processes = []
              ## mapping of shape uncertainties to signal_indexes in the production_processes list (=histograms)
              self.uncertainty_to_signal_indexes = {}
              ## names of output histfiles
              self.output_histfiles = []
              ## list of decay channels that have separated
              self.hists_in_separate_files = [
                     "hwwof_0j_shape", "hwwof_1j_shape",
                     "hwwsf_0j_shape", "hwwsf_1j_shape"
                     ]
              ## histogram extensions for value histograms
              self.value_hist_extensions = {}
              ## histogram extentions for shift histograms
              self.shift_hist_extensions = {}
              ## mapping of decay channel to interpolation method. Available methods are
              ## - non-degenerate-masses        : w/  template morphing
              ## - non-degenerate-masses-light  : w/o template morphing
              ## - degenerate-masses            : degenerate masses assumption
              ## - single-mass                  : depending on hww_cross_point only mh or
              ##                                  only mH is considered (for hww limits)
              ## the mapping is initialized in self.interpolation_mode(self, mode)
              self.decay_channel_to_interpolation_method = {}
              ## mapping of output histfiles to output directories in that histfiles
              self.histfile_to_directories = {}
              ## mapping of output histfiles to decay the channels that these histfiles are used for
              self.histfile_to_decay_channels = {}
              ## mapping of the production channel times the decay channel to the effective cross section
              self.signal_channel_to_cross_section = {}
              ## mapping of the production channel times the decay channel to the cross section uncertainties
              self.signal_channel_to_uncertainties = {}
              ## list of all possible line-heads to start the uncertainty lines with (per signal channel)
              self.standardized_signal_process_to_uncertainty_heads = {
                     "ggH":["ggHScale", "ggHPDF"],
                     "bbH":["bbHScale", "bbHPDF"],
                     "qqH":["qqHScale", "qqHPDF"],
                     "VH" :["VHScale" , "VHPDF" ]
                     }
              ## mapping of production channels to uncertainty lines in the output datacard
              self.signal_channel_to_uncertainty_lines = {}

       def interpolation_mode(self, mode="mode-1") :
              """
              Configure interpolation mode for htt limits. Considered modes are:

              classic htt channels (htt_em, htt_et, htt_mt)             htt_mm / hmm
              mode-0 :            non-degenerate-masses                 non-degenerate-masses
              mode-1 :            non-degenerate-masses                 non-degenerate-masses-light
              mode-2 :            non-degenerate-masses                 degenerate-masses
              mode-3 :            non-degenerate-masses-light           non-degenerate-masses-light
              mode-4 :            non-degenerate-masses-light           non-degenerate-masses
              mode-5 :            degenerate-masses                     degenerate-masses
              """
              if mode == "mode-0" :
                     for chn in ["mm", "em", "et", "mt"] :
                            for cat in ["8", "9"] : #"0", "1", "2", "3", "4", "5", "6", "7"] :
                                   for period in ["7TeV", "8TeV"] :
                                          decay_channel = "htt_{CHN}_{CAT}_{PERIOD}".format(CHN=chn, CAT=cat, PERIOD=period)
                                          self.decay_channel_to_interpolation_method[decay_channel] = "non-degenerate-masses"
                     self.decay_channel_to_interpolation_method["hmm_0"         ] = "non-degenerate-masses"
                     self.decay_channel_to_interpolation_method["hmm_1"         ] = "non-degenerate-masses"
                     self.decay_channel_to_interpolation_method["hwwof_0j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hwwof_1j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hwwsf_0j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hwwsf_1j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hww_2j_cut"    ] = "single-mass"
              if mode == "mode-1" :
                     for chn in ["mm", "em", "et", "mt"] :
                            for cat in ["8", "9"] : #"0", "1", "2", "3", "4", "5", "6", "7"] :
                                   for period in ["7TeV", "8TeV"] :
                                          decay_channel = "htt_{CHN}_{CAT}_{PERIOD}".format(CHN=chn, CAT=cat, PERIOD=period)
                                          if chn == "mm" :
                                                 self.decay_channel_to_interpolation_method[decay_channel] = "non-degenerate-masses-light"
                                          else :
                                                 self.decay_channel_to_interpolation_method[decay_channel] = "non-degenerate-masses"
                     self.decay_channel_to_interpolation_method["hmm_0"         ] = "non-degenerate-masses-light"
                     self.decay_channel_to_interpolation_method["hmm_1"         ] = "non-degenerate-masses-light"
                     self.decay_channel_to_interpolation_method["hwwof_0j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hwwof_1j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hwwsf_0j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hwwsf_1j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hww_2j_cut"    ] = "single-mass"
              if mode == "mode-2" :
                     for chn in ["mm", "em", "et", "mt"] :
                            for cat in ["8", "9"] : #"0", "1", "2", "3", "4", "5", "6", "7"] :
                                   for period in ["7TeV", "8TeV"] :
                                          decay_channel = "htt_{CHN}_{CAT}_{PERIOD}".format(CHN=chn, CAT=cat, PERIOD=period)
                                          if chn == "mm" :
                                                 self.decay_channel_to_interpolation_method[decay_channel] = "degenerate-masses"
                                          else :
                                                 self.decay_channel_to_interpolation_method[decay_channel] = "non-degenerate-masses"
                     self.decay_channel_to_interpolation_method["hmm_0"         ] = "degenerate-masses"
                     self.decay_channel_to_interpolation_method["hmm_1"         ] = "degenerate-masses"
                     self.decay_channel_to_interpolation_method["hwwof_0j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hwwof_1j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hwwsf_0j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hwwsf_1j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hww_2j_cut"    ] = "single-mass"
              if mode == "mode-3" :
                     for chn in ["mm", "em", "et", "mt"] :
                            for cat in ["8", "9"] : #"0", "1", "2", "3", "4", "5", "6", "7"] :
                                   for period in ["7TeV", "8TeV"] :
                                          decay_channel = "htt_{CHN}_{CAT}_{PERIOD}".format(CHN=chn, CAT=cat, PERIOD=period)
                                          self.decay_channel_to_interpolation_method[decay_channel] = "non-degenerate-masses-light"
                     self.decay_channel_to_interpolation_method["hmm_0"         ] = "non-degenerate-masses-light"
                     self.decay_channel_to_interpolation_method["hmm_1"         ] = "non-degenerate-masses-light"
                     self.decay_channel_to_interpolation_method["hwwof_0j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hwwof_1j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hwwsf_0j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hwwsf_1j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hww_2j_cut"    ] = "single-mass"
              if mode == "mode-4" :
                     for chn in ["mm", "em", "et", "mt"] :
                            for cat in ["8", "9"] : #"0", "1", "2", "3", "4", "5", "6", "7"] :
                                   for period in ["7TeV", "8TeV"] :
                                          decay_channel = "htt_{CHN}_{CAT}_{PERIOD}".format(CHN=chn, CAT=cat, PERIOD=period)
                                          if chn == "mm" :
                                                 self.decay_channel_to_interpolation_method[decay_channel] = "degenerate-masses"
                                          else :
                                                 self.decay_channel_to_interpolation_method[decay_channel] = "non-degenerate-masses-light"
                     self.decay_channel_to_interpolation_method["hmm_0"         ] = "degenerate-masses"
                     self.decay_channel_to_interpolation_method["hmm_1"         ] = "degenerate-masses"
                     self.decay_channel_to_interpolation_method["hwwof_0j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hwwof_1j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hwwsf_0j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hwwsf_1j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hww_2j_cut"    ] = "single-mass"
              if mode == "mode-5" :
                     for chn in ["mm", "em", "et", "mt"] :
                            for cat in ["8", "9"] : #"0", "1", "2", "3", "4", "5", "6", "7"] :
                                   for period in ["7TeV", "8TeV"] :
                                          decay_channel = "htt_{CHN}_{CAT}_{PERIOD}".format(CHN=chn, CAT=cat, PERIOD=period)
                                          self.decay_channel_to_interpolation_method[decay_channel] = "degenerate-masses"
                     self.decay_channel_to_interpolation_method["hmm_0"         ] = "degenerate-masses"
                     self.decay_channel_to_interpolation_method["hmm_1"         ] = "degenerate-masses"
                     self.decay_channel_to_interpolation_method["hwwof_0j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hwwof_1j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hwwsf_0j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hwwsf_1j_shape"] = "single-mass"
                     self.decay_channel_to_interpolation_method["hww_2j_cut"    ] = "single-mass"
              print "using mass interpolation", mode, "for htt limits"

       def init(self, interpolation_mode="mode-1") :
              ## load masses
              self.load_masses()
              ## setup interpolation mode for htt
              self.interpolation_mode(interpolation_mode)
              ## announce model
              if self.feyn_higgs_model != "0" :
                     print "preparing limit calculation for model input: feyn-higgs model="+self.feyn_higgs_model
              else :
                     print "preparing limit calculation for model input:", self.mssm_xsec_tools_input_path
	      higgs_file.write("%f  %f  %f  %f \n" % (self.tanb, self.mh, self.mA, self.mH))	

       def decay_channels(self, words) :
              """
              Determine the number and names of decay channels involved in this combination, as determined
              by the individual datacards that went into the combination when using combineCards.py. Input
              is the first line of the input datacard.
              """
              decay_channels = []
              for word in words :
                     if word.find("=")>-1 :
                            decay_channels.append(word[:word.find("=")])
              return decay_channels

       def find_decay_channel(self, word) :
              """
              Determine the channel that a directory in a given file belongs to. This is determined from
              the third word of the 'shape' line, which is expected to be composed of the channel and a
              potential directory in the input histfile, if there is more than one directory in the file
              Expected input is any line of the input datacard that starts with the key word 'shapes'.
              The return value corresponds to the words in the 'bin' line of the input datacard.
              """
              decay_channel = "NONE"
              for channel in self.initial_datacards :
                     if word.find(channel)>-1 :
                            decay_channel = channel
              return decay_channel

       def find_directories_in_histfile(self, words) :
              """
              Determine the list of all directories in a given input histfile, determined from any line
              of the input datacard that starts with the key word 'shape'. In principle the directories
              for shape uncertainties can be different from directories for the central values. Apart
              from the fact that this function will be able to cope with this matter this is not taken
              into account any further until a first use case occures.
              """
              histfile_directories = []
              for word in words :
                     directory = ""
                     if not word.find(".root")>-1 :
                            if word.find("/")>-1 :
                                   directory = word[:word.find("/")]
                            histfile_directories.append(directory)
              return histfile_directories

       def append_unique_value(self, dict, key, value) :
              """
              Append a value to a list belonging to a given key in a dictionary. Take care that each
              value in the list appears only once. If value is "" it will not be added to the list.
              This function is used to fill the mappings from histfiles to decay channels and to
              directories.
              """
              if not key in dict :
                     if value == "" :
                            dict[key] = []
                     else :
                            dict[key] = [value]
              else :
                     if value!="" and not dict[key].count(value)>0 :
                            dict[key].append(value)

       def standardized_signal_process(self, word) :
              """
              Determine a standardized signal process for a given word as it has been introduced
              in the datacards of each individual channel. The word corresponds to the actual
              histogram name in each corresponding input histfile, which is important for internal
              looping. The standardized signal process name is of importance, when determining
              the scale and pdf uncertainties for the effective production (production process x
              BR for the corresponding decay channel), which are the same for each sub-channel
              that corresponds to the same decay channel like htt_em_0, htt_em_1, htt_em_2, aso.
              Standardized signal processes are defined in self.standardized_production_processes.
              """
              signal_process = "NONE"
              for key, value in self.standardized_production_processes.iteritems() :
                     for type in value :
                            if word.find(type)>-1 :
                                   signal_process = key
              return signal_process

       def standardized_decay_channel(self, word) :
              """
              Determine a standardized decay channel for a given decay channel word as it appears
              in self.decay_channels_. The word corresponds to the actual decay (sub-)channel as
              it has been introduced by the combination of the individual datacards for each (sub-)
              channel. It is important for internal looping. The standardized decay channel is of
              importance when determining the scale and pdf uncertainties for the effective
              production (production process x BR for the corresponding decay channel), which are
              the same for each sub-channel that corresponds to the same decay channel like
              htt_em_0, htt_em_1, htt_em_2, aso. Standardized decay channels are defined in
              self.standardized_decay_channels.
              """
              decay_channel = "NONE"
              for key, value in self.standardized_decay_channels.iteritems() :
                     for type in value :
                            if word.find(type)>-1 :
                                   decay_channel = key
              if decay_channel == "NONE" :
                     print "ERROR in standardized_decay_channel: did not find channel : ", word, " in list of objects"
              return decay_channel

       def load_masses(self) :
              """
              Fill mh and mH depending on mA. These values are calculated from the htt tools.
              """
              if self.feyn_higgs_model != "":
                     ## read masses from feyn-higgs for models that are not available from the
                     ## htt mssm cross section tools. Here the cross section is not of interest,
                     ## instead just mh and mH are grep'ed
                     self.mh = float(os.popen("feyn-higgs-mssm xs mssm ggA {mA} {tanb} model={model} | grep mh".format(
                            mA=self.mA, tanb=self.tanb, model=self.feyn_higgs_model)).read().split()[2])
                     self.mH = float(os.popen("feyn-higgs-mssm xs mssm ggA {mA} {tanb} model={model} | grep mH".format(
                            mA=self.mA, tanb=self.tanb, model=self.feyn_higgs_model)).read().split()[2])
              else :
                     ## read masses from htt mssm cross section tools (default behavior); the
                     ## masses are taken from the 7TeV input files
                     path = ""
                     if(float(self.tanb)>=1) :
                            path = self.mssm_xsec_tools_input_path.format(PERIOD="7TeV", tanbRegion="tanbHigh")
                     else :
                            path = self.mssm_xsec_tools_input_path.format(PERIOD="7TeV", tanbRegion="tanbLow")
                     scan = mssm_xsec_tools("{CMSSW_BASE}/src/{PATH}".format(CMSSW_BASE=os.environ['CMSSW_BASE'], PATH=path))
                     htt_query = scan.query(self.mA, self.tanb)
                     self.mh = htt_query['higgses']['h']['mass']
                     self.mH = htt_query['higgses']['H']['mass']

       def cross_sections_hww(self, production_channel) :
              """
              Fill cross section results for different production channels for hww depending on mass
              and tanb vaoue. The variable 'production_channel' can have the values:

              - 'gg[A,H,h]'  for gluon gluon fusion,
              - 'qq[A,H,h]'  for VBF and
              - 'W/Z[A,H,h]' for assicoated higgs production.

              The values in '[]' will be completed automatically. The function returns the dictionary
              of production cross sections mapped to the individual Higgs bosons 'A', 'H' and 'h'.
              """
              cross_sections = {"A" : 0., "H" : 0., "h" : 0.}
              ## read cross section results for hww, the cross section is returned in fb
              for key in cross_sections :
                     xs = float(os.popen("feyn-higgs-mssm xs mssm {channel}{higgs} {mA} {tanb} | grep value".format(
                            channel=production_channel, higgs=key, mA=self.mA, tanb=self.tanb)).read().split()[2])/1000.
                     br = float(os.popen("feyn-higgs-mssm br mssm {higgs}WW {mA} {tanb} | grep value".format(
                            higgs=key, mA=self.mA, tanb=self.tanb)).read().split()[2])
                     cross_sections[key] = xs*br
                     if cross_sections[key] < 0 :
                            ## non-existing cross sections * branching ratios are set to 0.
                            cross_sections[key] = 0
              return cross_sections

       def cross_sections_htt(self, production_channel, decay_channel, period) :
              """
              Fill cross section results for different production channels for htt and hmm, which uses
              the same infrastructure as htt depending on mass and tanb. The variable 'production_channel'
              can have the values:

              - 'ggF' for gluon gluon fusion and
              - 'santander' for higgs production in association with b quarks.

              The variable 'decay_channel' can have the values:

              - 'htt' for htt
              - 'hmm' for hmm

              The function returns the dictionary of production cross sections mapped to the individual
              run periods (7TeV or 8TeV) and higgses in form 'period' : {'A', 'H' and 'h'}.
              """
              cross_sections = {"A" : 0., "H" : 0., "h" : 0.}
              if self.feyn_higgs_model != "":
                     ## map production channel channel back to feyn-higgs compatible inputs
                     if production_channel == "ggF" :
                            channel = "gg"
                     if production_channel == "santander" :
                            channel = "bb"
                     if decay_channel == "htt" :
                            feyn_decay = "tt"
                     if decay_channel == "hmm" :
                            feyn_decay = "mm"
                     for key in cross_sections :
                            xs = float(os.popen("feyn-higgs-mssm xs mssm {channel}{higgs} {mA} {tanb} model={model} | grep value".format(
                                   channel=channel, higgs=key, mA=self.mA, tanb=self.tanb, model=self.feyn_higgs_model)).read().split()[2])/1000.
                            br = float(os.popen("feyn-higgs-mssm br mssm {higgs}{decay} {mA} {tanb} model={model}| grep value".format(
                                   higgs=key, decay=feyn_decay, mA=self.mA, tanb=self.tanb, model=self.feyn_higgs_model)).read().split()[2])
                            cross_sections[key] = xs*br
                            if cross_sections[key] < 0 :
                                   ## non-existing cross sections * branching ratios are set to 0.
                                   cross_sections[key] = 0
              else:
                     ## read cross section results for htt
                     path = ""
                     if(float(self.tanb)>=1) :
                            path = self.mssm_xsec_tools_input_path.format(PERIOD=period, tanbRegion="tanbHigh")
                     else :
                            path = self.mssm_xsec_tools_input_path.format(PERIOD=period, tanbRegion="tanbLow") 
                     scan = mssm_xsec_tools("{CMSSW_BASE}/src/{PATH}".format(CMSSW_BASE=os.environ['CMSSW_BASE'], PATH=path))
                     htt_query = scan.query(self.mA, self.tanb)
                     ## fill cross section (central values)
                     for key in cross_sections :
                            if decay_channel == "htt" :
                                   cross_sections[key] = htt_query["higgses"][key]["xsec"][production_channel]*htt_query["higgses"][key]["BR"]
                            if decay_channel == "hmm" :
                                   cross_sections[key] = htt_query["higgses"][key]["xsec"][production_channel]*htt_query["higgses"][key]["BR-mumu"]
              return cross_sections

       def load_cross_sections_map(self) :
              """
              Fill signal process to cross section dictionary for all involved production processes and
              decay channels. At the moment this function calls htt and hww cross sections only. To
              extend it add a function self.cross_sections_XYZ(self, production_channel) and modify this
              function accordingly.
              """
              filled_htt  = False
              filled_hmm  = False
              filled_vhtt = False
              filled_hww  = False
              for decay_channel in self.decay_channels_ :
                     if not filled_htt :
                            if self.standardized_decay_channel(decay_channel) == "htt" :
                                   filled_htt = True
                                   for period in ["7TeV", "8TeV"] :
                                          self.signal_channel_to_cross_section[("ggH_htt", period)] = self.cross_sections_htt("ggF", "htt", period)
                                          self.signal_channel_to_cross_section[("bbH_htt", period)] = self.cross_sections_htt("santander", "htt", period)
                                          self.signal_channel_to_cross_section[("qqH_htt", period)] = {"A" : 1., "H" : 1., "h" : 1.}
                                          self.signal_channel_to_cross_section[("VH_htt" , period)] = {"A" : 1., "H" : 1., "h" : 1.}
                     if not filled_hmm :
                            if self.standardized_decay_channel(decay_channel) == "hmm" :
                                   filled_hmm = True
                                   for period in ["7TeV", "8TeV"] :
                                          self.signal_channel_to_cross_section[("ggH_hmm", period)] = self.cross_sections_htt("ggF", "hmm", period)
                                          self.signal_channel_to_cross_section[("bbH_hmm", period)] = self.cross_sections_htt("santander", "hmm", period)
                                          self.signal_channel_to_cross_section[("qqH_hmm", period)] = {"A" : 1., "H" : 1., "h" : 1.}
                                          self.signal_channel_to_cross_section[("VH_hmm" , period)] = {"A" : 1., "H" : 1., "h" : 1.}
                     if not filled_vhtt :
                            if self.standardized_decay_channel(decay_channel) == "vhtt" :
                                   filled_htt = True
                                   for period in ["7TeV", "8TeV"] :
                                          self.signal_channel_to_cross_section[("ggH_vhtt", period)] = {"A" : 1., "H" : 1., "h" : 1.}
                                          self.signal_channel_to_cross_section[("bbH_vhtt", period)] = {"A" : 1., "H" : 1., "h" : 1.}
                                          self.signal_channel_to_cross_section[("qqH_vhtt", period)] = {"A" : 1., "H" : 1., "h" : 1.}
                                          self.signal_channel_to_cross_section[("VH_vhtt" , period)] = {"A" : 1., "H" : 1., "h" : 1.}
                     if not filled_hww :
                            if self.standardized_decay_channel(decay_channel) == "hww" :
                                   filled_hww = True
                                   for period in ["7TeV", "8TeV"] :
                                          self.signal_channel_to_cross_section[("ggH_hww", period)] = self.cross_sections_hww("gg")
                                          self.signal_channel_to_cross_section[("qqH_hww", period)] = self.cross_sections_hww("qq")
                                          self.signal_channel_to_cross_section[("WH_hww" , period)] = self.cross_sections_hww("W" )
                                          self.signal_channel_to_cross_section[("ZH_hww" , period)] = self.cross_sections_hww("Z" )

       def contracted_cross_section(self, standardized_production_process, standardized_decay_channel, period, mode=0) :
              """
              Conracted cross section for A, H, h for a given production process and decay channel. The
              contracted cross section is provided in three modes:
              mode 0 : cross sections for all Higgses added
              mode 1 : cross sections added for degenerate mass mode (depending on mA only two or all
                       higgses contribute)
              mode 2 : cross section for single mass mode (depending on mA only one Higgs contributes)
              The argument 'period' indicates the 7TeV or 8TeV running period.
              """
              contracted_cross_section = 0.
              channel = standardized_production_process+"_"+standardized_decay_channel
              if mode == 2 :
                     ## determine cross section for single-mass mode
                     if self.mA<self.hww_cross_point :
                            contracted_cross_section = self.signal_channel_to_cross_section[(channel, period)]["H"]
                     else :
                            contracted_cross_section = self.signal_channel_to_cross_section[(channel, period)]["h"]
              elif mode == 1 :
                     ## determine cross section for degenerate-masses mode
                     if abs(self.mA-self.mh) < abs(self.mA-self.mH) :
                            contracted_cross_section = self.signal_channel_to_cross_section[(channel, period)]["A"]
                            contracted_cross_section+= self.signal_channel_to_cross_section[(channel, period)]["h"]
                     else:
                            contracted_cross_section = self.signal_channel_to_cross_section[(channel, period)]["A"]
                            contracted_cross_section+= self.signal_channel_to_cross_section[(channel, period)]["H"]
                     if self.mA == 130. :
                            contracted_cross_section = self.signal_channel_to_cross_section[(channel, period)]["A"]
                            contracted_cross_section+= self.signal_channel_to_cross_section[(channel, period)]["H"]
                            contracted_cross_section+= self.signal_channel_to_cross_section[(channel, period)]["h"]
              else :
                     ## determine cross section for non-degenerate-masses mode
                     for higgs in self.signal_channel_to_cross_section[(channel, period)] :
                            contracted_cross_section += self.signal_channel_to_cross_section[(channel, period)][higgs]
              return contracted_cross_section

       def uncertainties_htt(self, production_channel, decay_channel, period, uncertainty_type, uncertainty_direction):
              """
              Fill cross section uncertainties for different production channels for htt and hmm, which uses
              the same infrastructure as htt, depending on mass and tanb. The variable 'production_channel'
              can have the values:

              - 'ggF' for gluon gluon fusion and
              - 'santander' for higgs production in association with b quarks.

              The variable 'decay_channel' can have the values:

              - 'htt' for htt
              - 'hmm' for hmm

              The variables 'period' can have the values:

              - '7TeV' for the 7TeV data taking period
              - '8TeV' for the 8TeV data taking period

              The variable 'uncertainty_type' can have the values 'mu' and 'pdf' for the different
              uncertainty types (scale or pdf). The variable 'uncertainty_direction' can be -1 or
              +1 for the minus or plus variation of the uncertainty. The function returns the
              dictionary of production cross sections mapped to the individual higgses, 'A', 'H'
              and 'h'. NOTE: The uncertainties are returned as absolute shifts to the central value.
              """
              cross_sections = {"A" : 0., "H" : 0., "h" : 0.}
              ## read cross section results for htt
              path = ""
              if(float(self.tanb)>=1) :
                     path = self.mssm_xsec_tools_input_path.format(PERIOD=period, tanbRegion="tanbHigh")
              else :
                     path = self.mssm_xsec_tools_input_path.format(PERIOD=period, tanbRegion="tanbLow") 
              inputFileName="{CMSSW_BASE}/src/{PATH}".format(CMSSW_BASE=os.environ['CMSSW_BASE'], PATH=path)
              scan = mssm_xsec_tools(inputFileName)
              htt_query = scan.query(self.mA, self.tanb)
              ## fill uncertainties of Up/Down type
              for key in cross_sections :
                     if decay_channel == "htt" :
                            cross_sections[key] = htt_query["higgses"][key][uncertainty_type][production_channel][uncertainty_direction]*htt_query["higgses"][key]["BR"]
                     if decay_channel == "hmm" :
                            cross_sections[key] = htt_query["higgses"][key][uncertainty_type][production_channel][uncertainty_direction]*htt_query["higgses"][key]["BR-mumu"]
              return cross_sections

       def contracted_uncertainty(self, standardized_production_process, standardized_decay_channel, period, uncertainty_type, uncertainty_direction) :
              """
              Contract the uncertainties for A, H, h into a single uncertainty for a given production process
              times decay channel. Scale uncertainties are added linearly, PDF uncertainties are added in
              quadrature. The argument 'period' indicates the 7TeV or 8TeV running period.
              """
              contracted_uncertainty = 0.
              channel = standardized_production_process+"_"+standardized_decay_channel+"_"+uncertainty_type+uncertainty_direction
              for higgs in self.signal_channel_to_uncertainties[(channel, period)] :
                     if uncertainty_type == "mu" :
                            contracted_uncertainty += self.signal_channel_to_uncertainties[(channel, period)][higgs]
                     if uncertainty_type == "pdf" :
                            contracted_uncertainty += self.signal_channel_to_uncertainties[(channel, period)][higgs]*self.signal_channel_to_uncertainties[(channel, period)][higgs]
              if uncertainty_type == "pdf" :
                     contracted_uncertainty = math.sqrt(contracted_uncertainty)
              return contracted_uncertainty

       def load_uncertainties_map(self) :
              """
              Fill signal process to uncertainties dictionary for scale and pdf uncertainties for all involved
              production cross sections and decay channels. At the moment thisis only implemented for htt.
              """
              filled_htt  = False
              filled_hmm  = False
              filled_vhtt = False
              filled_hww  = False
              for decay_channel in self.decay_channels_ :
                     if not filled_htt :
                            if self.standardized_decay_channel(decay_channel) == "htt" :
                                   filled_htt = True
                                   for period in ["7TeV", "8TeV"] :
                                          self.signal_channel_to_uncertainties[("ggH_htt_mu+" , period)] = self.uncertainties_htt("ggF"      , "htt", period, "mu" ,  1)
                                          self.signal_channel_to_uncertainties[("ggH_htt_mu-" , period)] = self.uncertainties_htt("ggF"      , "htt", period, "mu" , -1)
                                          self.signal_channel_to_uncertainties[("bbH_htt_mu+" , period)] = self.uncertainties_htt("santander", "htt", period, "mu" ,  1)
                                          self.signal_channel_to_uncertainties[("bbH_htt_mu-" , period)] = self.uncertainties_htt("santander", "htt", period, "mu" , -1)
                                          self.signal_channel_to_uncertainties[("qqH_htt_mu+" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("qqH_htt_mu-" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("VH_htt_mu+"  , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("VH_htt_mu-"  , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("ggH_htt_pdf+", period)] = self.uncertainties_htt("ggF"      , "htt", period, "pdf",  1)
                                          self.signal_channel_to_uncertainties[("ggH_htt_pdf-", period)] = self.uncertainties_htt("ggF"      , "htt", period, "pdf", -1)
                                          self.signal_channel_to_uncertainties[("bbH_htt_pdf+", period)] = self.uncertainties_htt("santander", "htt", period, "pdf",  1)
                                          self.signal_channel_to_uncertainties[("bbH_htt_pdf-", period)] = self.uncertainties_htt("santander", "htt", period, "pdf", -1)
                                          self.signal_channel_to_uncertainties[("qqH_htt_pdf+", period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("qqH_htt_pdf-", period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("VH_htt_pdf+" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("VH_htt_pdf-" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                     if not filled_hmm :
                            if self.standardized_decay_channel(decay_channel) == "hmm" :
                                   filled_hmm = True
                                   for period in ["7TeV", "8TeV"] :
                                          self.signal_channel_to_uncertainties[("ggH_hmm_mu+" , period)] = self.uncertainties_htt("ggF"      , "hmm", period, "mu" ,  1)
                                          self.signal_channel_to_uncertainties[("ggH_hmm_mu-" , period)] = self.uncertainties_htt("ggF"      , "hmm", period, "mu" , -1)
                                          self.signal_channel_to_uncertainties[("bbH_hmm_mu+" , period)] = self.uncertainties_htt("santander", "hmm", period, "mu" ,  1)
                                          self.signal_channel_to_uncertainties[("bbH_hmm_mu-" , period)] = self.uncertainties_htt("santander", "hmm", period, "mu" , -1)
                                          self.signal_channel_to_uncertainties[("qqH_hmm_mu+" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("qqH_hmm_mu-" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("VH_hmm_mu+"  , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("VH_hmm_mu-"  , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("ggH_hmm_pdf+", period)] = self.uncertainties_htt("ggF"      , "hmm", period, "pdf",  1)
                                          self.signal_channel_to_uncertainties[("ggH_hmm_pdf-", period)] = self.uncertainties_htt("ggF"      , "hmm", period, "pdf", -1)
                                          self.signal_channel_to_uncertainties[("bbH_hmm_pdf+", period)] = self.uncertainties_htt("santander", "hmm", period, "pdf",  1)
                                          self.signal_channel_to_uncertainties[("bbH_hmm_pdf-", period)] = self.uncertainties_htt("santander", "hmm", period, "pdf", -1)
                                          self.signal_channel_to_uncertainties[("qqH_hmm_pdf+", period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("qqH_hmm_pdf-", period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("VH_hmm_pdf+" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("VH_hmm_pdf-" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                     if not filled_vhtt :
                            if self.standardized_decay_channel(decay_channel) == "vhtt" :
                                   filled_vhtt = True
                                   for period in ["7TeV", "8TeV"] :
                                          self.signal_channel_to_uncertainties[("ggH_vhtt_mu+" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("ggH_vhtt_mu-" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("bbH_vhtt_mu+" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("bbH_vhtt_mu-" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("qqH_vhtt_mu+" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("qqH_vhtt_mu-" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("VH_vhtt_mu+"  , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("VH_vhtt_mu-"  , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("ggH_vhtt_pdf+", period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("ggH_vhtt_pdf-", period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("bbH_vhtt_pdf+", period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("bbH_vhtt_pdf-", period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("qqH_vhtt_pdf+", period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("qqH_vhtt_pdf-", period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("VH_vhtt_pdf+" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("VH_vhtt_pdf-" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                     if not filled_hww :
                            if self.standardized_decay_channel(decay_channel) == "hww" :
                                   filled_hww = True
                                   for period in ["7TeV", "8TeV"] :
                                          self.signal_channel_to_uncertainties[("ggH_hww_mu+" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("ggH_hww_mu-" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("bbH_hww_mu+" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("bbH_hww_mu-" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("qqH_hww_mu+" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("qqH_hww_mu-" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("VH_hww_mu+"  , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("VH_hww_mu-"  , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("ggH_hww_pdf+", period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("ggH_hww_pdf-", period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("bbH_hww_pdf+", period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("bbH_hww_pdf-", period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("qqH_hww_pdf+", period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("qqH_hww_pdf-", period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("VH_hww_pdf+" , period)] = {"A" : .1, "H" : .1, "h" : .1}
                                          self.signal_channel_to_uncertainties[("VH_hww_pdf-" , period)] = {"A" : .1, "H" : .1, "h" : .1}

       def load_available_masses(self, decay_channel) :
              """
              Read all available masses for a given decay channel. The values are read from a file masses.vals,
              which is expected to be located in the same directory, in which the script is executed. If the
              file is not found it is looked for in a directory with name 'common' next to the current directory.
              The variable 'decay_channel' is expected to be of type of self.decay_channel (='htt_em_0',
              'htt_em_1', 'htt_em_2', ...).
              """
              masses = []
              if os.path.exists("masses.vals") :
                     file = open("masses.vals", 'r')
              else :
                     file = open("%s/../common/masses.vals" % os.getcwd(), 'r')
              for line in file :
                     words = line.split()
                     if words[0] == decay_channel :
                            for word in words :
                                   if re.search(r"^\d+\.?\d+?$", word.strip()) :
                                          masses.append(float(word))
              file.close()
              return masses

       def embracing_masses(self, mass, masses) :
              """
              Determine the closest lower and upper mass value to 'mass' in the list of 'masses'. The return
              value of this function is a tuple of a boolean to indicate whether 'mass' was out of range or
              not and of the closest lower and upper mass value. In case that the mass was out of range the
              closest lower and upper mass values are -1. At the moment a warning is issued in this case.
              """
              lower  = -1.
              upper  = -1.
              failed = False
              ## drop out here if there's not more than one mass available
              if not len(masses)>1 :
                     return (True, lower, upper)
              for idx in range(len(masses)-1) :
                     if masses[idx]<mass and mass<=masses[idx+1] :
                            lower = masses[idx  ]
                            upper = masses[idx+1]
                     if idx == (len(masses)-2) and lower<0:
                            print 'mass out of range: m=%.3f'% mass
                            failed = True
              #print "embracing masses: ", lower, " -- ", mass, " -- ", upper
              return (failed, lower, upper)

       def scale(self, hist_lower, hist_upper, m_lower, m_upper, mass) :
              """
              Determine the residual scale due to potential differences in reconstruction and
              selection efficiencies for the interpolated mass histogram from the embacing
              mass histograms.
              """
              scale = 1.
              if m_upper>m_lower:
                     scale = hist_lower.Integral()+abs(hist_upper.Integral()-hist_lower.Integral())/abs(m_upper-m_lower)*(mass-m_lower)
              return scale

       def expand_filename(self, filename, mass=-1) :
              """
              Determine the proper filename for the loading of histograms for the rescaling of
              the histograms for the central value and for the embracing masses for h an H. If
              the histogram name contains the keyword $MASS (i.e. signal histograms for all mass
              points not all contained in the same file), this keyword will be replaced by the
              value of mass. In this case the embracing histograms will be looked up from the
              input histfiles in other directories of the setup. If mass is -1, the keyword will
              be ignored. This is the case for the central value, which has already the proper
              filename and is located in the current directory. In this case the keyword is erased
              from the filename.
              """
              expanded_filename = filename
              if filename.find("$MASS")>-1 :
                     if mass>0 :
                            expanded_filename = filename.replace("$MASS", "%.0f" % mass).replace("_%.0f_%.2f.root" % (self.mA, self.tanb), ".root")
                     else :
                            expanded_filename =  filename.replace("../$MASS", ".")
              #print "mass: ", mass, " -- opening file: ", expanded_filename
              return expanded_filename

       def expand_histname(self, channel, process, uncertainty="") :
              """
              Map signal or background process to histogram name in case of shape analyses.
              The modification string is taken from the lines starting with keyword 'shape'
              in the datacard.
              """
              expanded_histname = process
              if uncertainty == "" :
                     ## apply modifications which are common for all inputs
                     if channel+"/*" in self.value_hist_extensions :
                            expanded_histname = self.value_hist_extensions[channel+"/*"].replace("$PROCESS", process).replace("$MASS", "%.0f" % self.mA)
                     ## apply modifications which are common for special inputs
                     if channel+"/"+process in self.value_hist_extensions :
                            expanded_histname = self.value_hist_extensions[channel+"/"+process].replace("$PROCESS", process).replace("$MASS", "%.0f" % self.mA)
              else :
                     ## apply modifications which are common for all inputs
                     if channel+"/*" in self.shift_hist_extensions :
                            expanded_histname = self.shift_hist_extensions[channel+"/*"].replace("$PROCESS", process).replace("$MASS", "%.0f" % self.mA).replace("$SYSTEMATIC", uncertainty)
                     ## apply modifications which are common for special inputs
                     if channel+"/"+process in self.shift_hist_extensions :
                            expanded_histname = self.shift_hist_extensions[channel+"/"+process].replace("$PROCESS", process).replace("$MASS", "%.0f" % self.mA).replace("$SYSTEMATIC", uncertainty)
              return expanded_histname

       def rescale_histogram(self, filename, dir, process, masses, cross_sections, channel, uncertainty="", interpolation_method="") :
              """
              Rescale a histogram with name 'process' according to the non-degenerate-masses scheme.
              The histogram for mA is scaled as is. For mH and mh the closest available histograms
              to the corresponding value of mH/mh are searched in the list of all available masses
              for the given (sub-)decay channel, between these two histograms a histogram according
              to the actual value of mH/mh is derived by horizontal template morphing and the
              resulting histogram is scaled according to the corresponding cross section/tanb
              times a linearly interpolated scale factor for the efficiency of the event selection
              and mass reconstruction. In a light version the histograms for mH/mh are not determined
              by horizontal template morphing but the histogram closest to mH/mh is chosen. NOTE:
              this function has the results of self.load_cross_sections_map and self.load_available_masses
              as input.

              NOTE: (not yet armed)
              This rescaling includes an acceptance correction due to the smearing of mA/H/h on generator
              level. The NNLO cross section is determined in a mass window of 30% of the nominal boson mass.
              Currently analyses have not corrected for this, therefore this correction is applied here.    
              """
              ## cross check whether more then one histfile is needed or not
              single_file = not (filename.find("$MASS")>-1)
              ## open root file and get original histograms
              path_name = self.expand_histname(channel, process, uncertainty)
              hist_name = path_name[path_name.rfind("/")+1:]
              ## prepare mA hist
              new_filename  = self.expand_filename(filename)
              file_mA_value = ROOT.TFile(new_filename, "UPDATE")
              ## check whether the requested histogram does exist or not: in
              ## the case of shape uncertainties of type shape? this has to
              ## be determined from the existence of a shape uncertainty hist
              if not self.exists(file_mA_value, path_name) :
                     return
              buff_mA_value = self.load_hist(file_mA_value, path_name)
              hist_mA_value = buff_mA_value.Clone(hist_name)
              #print "RESCALING OF HIST STARTING: ", hist_mA_value.GetName(), " -- ", hist_mA_value.Integral()

              acc_mA = acceptance_correction(self.standardized_signal_process(process), self.mA) if self.acc_corr else 1.
              hist_mA_value.Scale(cross_sections["A"]/self.tanb*acc_mA) 
              ## determine upper and lower mass edges for mh
              (mh_failed, mh_lower, mh_upper) = self.embracing_masses(self.mh, masses)
              if not mh_failed :
                     if not single_file :
                            new_filename  = self.expand_filename(filename, mh_lower)
                            file_mh_lower = ROOT.TFile(new_filename, "READ")
                     buff_mh_lower = self.load_hist(
                            file_mA_value if single_file else file_mh_lower, path_name.replace("%.0f" % self.mA, "%.0f" % mh_lower) if self.mA!=mh_lower else path_name
                            )
                     hist_mh_lower = buff_mh_lower.Clone(hist_name.replace(str(self.mA), "%.0f" % mh_lower))
                     if not single_file :
                            new_filename  = self.expand_filename(filename, mh_upper)
                            file_mh_upper = ROOT.TFile(new_filename, "READ")
                     buff_mh_upper = self.load_hist(
                            file_mA_value if single_file else file_mh_upper, path_name.replace("%.0f" % self.mA, "%.0f" % mh_upper) if mh_upper!=self.mA else path_name
                            )
                     hist_mh_upper = buff_mh_upper.Clone(hist_name.replace(str(self.mA), "%.0f" % mh_upper))
                     if interpolation_method == "light" :
                            if (self.mh-mh_lower)<(mh_upper-self.mh) :
                                   hist_mh_value = hist_mh_lower
                            else :
                                   hist_mh_value = hist_mh_upper
                            if hist_mh_value.Integral()>0 :
                                   norm_mh_value = cross_sections["h"]/self.tanb*self.scale(hist_mh_lower, hist_mh_upper, mh_lower, mh_upper, self.mh)
                                   acc_mh = acceptance_correction(self.standardized_signal_process(process), self.mh) if self.acc_corr else 1.
                                   hist_mh_value.Scale(norm_mh_value/hist_mh_value.Integral()*acc_mh)
                     else:
                            norm_mh_value = cross_sections["h"]/self.tanb*self.scale(hist_mh_lower, hist_mh_upper, mh_lower, mh_upper, self.mh)
                            acc_mh = acceptance_correction(self.standardized_signal_process(process), self.mh) if self.acc_corr else 1.                            
                            if channel.find("htt_mm")>-1 :
                                   hist_mh_value = th1fmorph("I","mh_"+hist_name,hist_mh_lower, hist_mh_upper, mh_lower, mh_upper, self.mh, norm_mh_value, 0)
                                   ##hist_mH_value = th2fmorph("I","mH_"+hist_name,hist_mh_lower, hist_mh_upper, mh_lower, mh_upper, norm_mh_value, true) ## change to th2 morphing - not armed yet
                            else :
                                   hist_mh_value = th1fmorph("I","mh_"+hist_name,hist_mh_lower, hist_mh_upper, mh_lower, mh_upper, self.mh, norm_mh_value, 0)

                            hist_mh_value.Scale(acc_mh)
              else :
                     hist_mh_value = hist_mA_value.Clone(hist_name)
                     acc_mh = acceptance_correction(self.standardized_signal_process(process), self.mh) if self.acc_corr else 1.
                     hist_mh_value.Scale(cross_sections["h"]/self.tanb*acc_mh) 
              ## catch cases where the morphing failed. Fallback to mA
              ## in this case and scale according to cross section of mh
              if not hist_mA_value.GetNbinsX() == hist_mh_value.GetNbinsX() :
                     hist_mh_value = hist_mA_value.Clone(hist_name)
                     acc_mh = acceptance_correction(self.standardized_signal_process(process), self.mh) if self.acc_corr else 1.
                     hist_mh_value.Scale(cross_sections["h"]/self.tanb*acc_mh) 
              else :
                     hist_mA_value.Add(hist_mh_value)

              ## determine upper and lower mass edges for mH
              (mH_failed, mH_lower, mH_upper) = self.embracing_masses(self.mH, masses)
              if not mH_failed :
                     if not single_file :
                            new_filename  = self.expand_filename(filename, mH_lower)
                            file_mH_lower = ROOT.TFile(new_filename, "READ")
                     buff_mH_lower = self.load_hist(
                            file_mA_value if single_file else file_mH_lower, path_name.replace("%0.f" % self.mA, "%.0f" % mH_lower)  if self.mA!=mH_lower else path_name
                            )
                     hist_mH_lower = buff_mH_lower.Clone(hist_name.replace(str(self.mA), "%.0f" % mH_lower))
                     if not single_file :
                            new_filename  = self.expand_filename(filename, mH_upper)
                            file_mH_upper = ROOT.TFile(new_filename, "READ")
                     buff_mH_upper = self.load_hist(
                            file_mA_value if single_file else file_mH_upper, path_name.replace("%0.f" % self.mA, "%.0f" % mH_upper)  if mH_upper!=self.mA else path_name
                            )
                     hist_mH_upper = buff_mH_upper.Clone(hist_name.replace(str(self.mA), "%.0f" % mH_upper))
                     if interpolation_method == "light" :
                            if (self.mH-mH_lower)<(mH_upper-self.mH) :
                                   hist_mH_value = hist_mH_lower
                            else :
                                   hist_mH_value = hist_mH_upper
                            if hist_mH_value.Integral()>0 :
                                   norm_mH_value = cross_sections["H"]/self.tanb*self.scale(hist_mH_lower, hist_mH_upper, mH_lower, mH_upper, self.mH)
                                   acc_mH = acceptance_correction(self.standardized_signal_process(process), self.mH) if self.acc_corr else 1.
                                   hist_mH_value.Scale(norm_mH_value/hist_mH_value.Integral()*acc_mH)
                     else :
                            norm_mH_value = cross_sections["H"]/self.tanb*self.scale(hist_mH_lower, hist_mH_upper, mH_lower, mH_upper, self.mH)
                            acc_mH = acceptance_correction(self.standardized_signal_process(process), self.mH) if self.acc_corr else 1.
                            if channel.find("htt_mm")>-1 :
                                   hist_mH_value = th1fmorph("I","mH_"+hist_name,hist_mH_lower, hist_mH_upper, mH_lower, mH_upper, self.mH, norm_mH_value, 0) 
                                   ##hist_mH_value = th2fmorph("I","mH_"+hist_name,hist_mH_lower, hist_mH_upper, mH_lower, mH_upper, norm_mH_value, true) ## change to th2 morphing - not armed yet
                            else :
                                 hist_mH_value = th1fmorph("I","mH_"+hist_name, hist_mH_lower, hist_mH_upper, mH_lower, mH_upper, self.mH, norm_mH_value, 0)                              
                            hist_mH_value.Scale(acc_mH)
              else :
                     hist_mH_value = hist_mA_value.Clone(hist_name)
                     acc_mH = acceptance_correction(self.standardized_signal_process(process), self.mH) if self.acc_corr else 1.
                     hist_mH_value.Scale(cross_sections["H"]/self.tanb*acc_mH) 
              ## catch cases where the morphing failed. Fallback to mA
              ## in this case and scale according to cross section of mH
              if not hist_mA_value.GetNbinsX() == hist_mH_value.GetNbinsX() :
                     hist_mH_value = hist_mA_value.Clone(hist_name)
                     acc_mH = acceptance_correction(self.standardized_signal_process(process), self.mH) if self.acc_corr else 1.
                     hist_mH_value.Scale(cross_sections["H"]/self.tanb*acc_mH) 
              else :
                     hist_mA_value.Add(hist_mH_value)
              #print "RESCALING OF HIST FINISHED: ", hist_mA_value.GetName(), " -- ", hist_mA_value.Integral()

              ## write modified histogram to file
              if self.path(dir)=="" :
                     file_mA_value.cd()
              else :
                     file_mA_value.cd(dir)
              hist_mA_value.Write(hist_name, ROOT.TObject.kOverwrite)
              file_mA_value.Close()
              if not single_file :
                     if not mh_failed :
                            file_mh_upper.Close()
                            file_mh_lower.Close()
                     if not mH_failed :
                            file_mH_upper.Close()
                            file_mH_lower.Close()

       def rescale_histogram_degenerate(self, filename, dir, process, cross_sections, channel, uncertainty="") :
              """
              Rescale a histogram with name 'process' according to the degenerate-masses scheme.

              NOTE: (not yet armed)
              This rescaling includes an acceptance correction due to the smearing of mA/H/h on
              generator level. The NNLO cross section is determined in a mass window of 30% of
              the nominal boson mass. Currently analyses have not corrected for this, therefore
              this correction is applied here.    
              """
              ## open root file and get original histograms
              path_name = self.expand_histname(channel, process, uncertainty)
              hist_name = path_name[path_name.rfind("/")+1:]
              ## prepare mA hist
              new_filename  = self.expand_filename(filename)
              file_mA_value = ROOT.TFile(new_filename, "UPDATE")
              ## check whether the requested histogram does exist or not: in
              ## the case of shape uncertainties of type shape? this has to
              ## be determined from the existence of a shape uncertainty hist
              if not self.exists(file_mA_value, path_name) :
                     return
              hist_mA_value = self.load_hist(file_mA_value, path_name)
              ## determine cross section for degenerate mass assumption
              if abs(self.mA-self.mh) < abs(self.mA-self.mH) :
                     cross_section = cross_sections["A"]+cross_sections["h"]
              else:
                     cross_section = cross_sections["A"]+cross_sections["H"]
              if self.mA == 130. :
                     cross_section = cross_sections["A"]+cross_sections["H"]+cross_sections["h"]
              ## rescale histogram
              acc_mA = acceptance_correction(self.standardized_signal_process(process), self.mA) if self.acc_corr else 1.
              hist_mA_value.Scale(cross_section/self.tanb*acc_mA) 
              ## write modified histogram to file
              if self.path(dir)=="" :
                     file_mA_value.cd()
              else :
                     file_mA_value.cd(dir)
              ## this is not yet sharp whil it is stillin test mode
              hist_mA_value.Write(hist_name, ROOT.TObject.kOverwrite)
              file_mA_value.Close()

       def rescale_histogram_single_mass(self, filename, dir, process, masses, cross_sections, channel, uncertainty="") :
              """
              Rescale a histogram with name 'process' according to the single-mass scheme. This scheme
              is used for limits based on the limit on the SM Higgs boson search in the hww channel,
              where the limit comes either from the absence of mh or mH. It can be viewed as a special
              case of the degenerate-masses mode, where mA does actually not contribute due to the
              zero coupling. For mA<250 GeV H is the contributing part (with masses ~130 GeV) leading
              to a potential exclusion for low tanb values. For mA>250 GeV h is the contributing part
              (also with masses ~130 GeV) leading to a potential exclusion for large tanb values. The
              contribution by A is set to zero by construction. Of H/h only the corresponding leading
              contributions is taken into account. This is a conservative approach. The better solution
              would be to have the MVA discriminant for each mass value for the selection of each
              corresponding mass point. In this case both contribution from H and h could be taken
              into account. Still the choice would be to choose the selection optimized for the mass
              point of the dominating contribution.
              """
              ## cross check whether more then one histfile is needed or not
              single_file = not (filename.find("$MASS")>-1)
              ## open root file and get original histograms
              path_name = self.expand_histname(channel, process, uncertainty)
              hist_name = path_name[path_name.rfind("/")+1:]
              ## prepare mA hist
              new_filename  = self.expand_filename(filename)
              file_mA_value = ROOT.TFile(new_filename, "UPDATE")
              ## check whether the requested histogram does exist or not: in
              ## the case of shape uncertainties of type 'shape?' this has to
              ## be determined from the existence of a shape uncertainty hist
              if not self.exists(file_mA_value, path_name) :
                     return
              hist_mA_value = self.load_hist(file_mA_value, path_name)
              #print "RESCALING OF HIST STARTING: ", hist_mA_value.GetName(), " -- ", hist_mA_value.Integral()
              if self.mA<self.hww_cross_point :
                     ## rescale histogram
                     acc_mA = acceptance_correction(self.standardized_signal_process(process), self.mH) if self.acc_corr else 1.
                     hist_mA_value.Scale(cross_sections["H"]/(1. if self.sm_like else self.tanb)*acc_mA) 
              else :
                     ## rescale histogram
                     acc_mA = acceptance_correction(self.standardized_signal_process(process), self.mh) if self.acc_corr else 1.
                     hist_mA_value.Scale(cross_sections["h"]/(1. if self.sm_like else self.tanb)*acc_mA) 
              #print "RESCALING OF HIST FINISHED: ", hist_mA_value.GetName(), " -- ", hist_mA_value.Integral()

              ## write modified histogram to file
              if self.path(dir)=="" :
                     file_mA_value.cd()
              else :
                     file_mA_value.cd(dir)
              hist_mA_value.Write(hist_name, ROOT.TObject.kOverwrite)

       def rescale_value_histograms(self) :
              """
              Rescale all histograms for central values
              """
              ## extend empty lists by empty strings to allow looping
              for key, value in self.histfile_to_directories.iteritems() :
                     if len(value)==0 :
                            value.append("")
              ## loop files, directories and signal histograms and rescale all apropriate hists
              for histfile in self.output_histfiles :
                     for jdx in range(len(self.histfile_to_directories[histfile])) :
                            directory = self.histfile_to_directories[histfile][jdx]
                            decay_channel = self.histfile_to_decay_channels[histfile][jdx]
                            for idx in self.signal_indexes :
                                   if self.decay_channels_[idx] == decay_channel :
                                          ## standardized production key for cross section mapping
                                          std_prod  = self.standardized_signal_process(self.production_processes[idx])
                                          ## standardized decay key for cross section mapping
                                          std_decay = self.standardized_decay_channel(decay_channel)
                                          ## list of all available masses for this decay channel
                                          masses = self.load_available_masses(decay_channel)
                                          ## modify path to hist file for such decay channels that do not keep
                                          ## signal hists for all masses in one file
                                          for in_separate_files in self.hists_in_separate_files :
                                                 if self.decay_channels_[idx] == in_separate_files :
                                                        if not histfile.find("$MASS")>-1:
                                                               histfile = "../$MASS/"+histfile
                                          ## add prefix to histogram name where needed
                                          hist_name = self.production_processes[idx]
                                          ## define run period for proper histogram scaling according to 7TeV or 8TeV cross sections
                                          period = self.decay_channels_[idx][self.decay_channels_[idx].rfind("_")+1:]
                                          ## rescale central value histograms
                                          if self.decay_channel_to_interpolation_method.has_key(self.decay_channels_[idx]) :
                                                 if self.decay_channel_to_interpolation_method[self.decay_channels_[idx]] == "non-degenerate-masses-light" :
                                                        print "using non-degenerate-masses-light mode for value histograms for decay channel: ", self.decay_channels_[idx]
                                                        self.rescale_histogram(
                                                               histfile,
                                                               directory,
                                                               hist_name,
                                                               masses,
                                                               self.signal_channel_to_cross_section[(std_prod+"_"+std_decay, period)],
                                                               self.decay_channels_[idx],
                                                               "",
                                                               "light"
                                                               )
                                                 elif self.decay_channel_to_interpolation_method[self.decay_channels_[idx]] == "degenerate-masses" :
                                                        print "using degenerate-masses mode for value histograms for decay channel: ", self.decay_channels_[idx]
                                                        self.rescale_histogram_degenerate(
                                                               histfile,
                                                               directory,
                                                               hist_name,
                                                               self.signal_channel_to_cross_section[(std_prod+"_"+std_decay, period)],
                                                               self.decay_channels_[idx]
                                                               )
                                                 elif self.decay_channel_to_interpolation_method[self.decay_channels_[idx]] == "single-mass" :
                                                        print "using single-mass mode for value histograms for decay channel: ", self.decay_channels_[idx]
                                                        self.rescale_histogram_single_mass(
                                                               histfile,
                                                               directory,
                                                               hist_name,
                                                               masses,
                                                               self.signal_channel_to_cross_section[(std_prod+"_"+std_decay, period)],
                                                               self.decay_channels_[idx]
                                                               )
                                                 else :
                                                        ## fall back to the default
                                                        self.rescale_histogram(
                                                               histfile,
                                                               directory,
                                                               hist_name,
                                                               masses,
                                                               self.signal_channel_to_cross_section[(std_prod+"_"+std_decay, period)],
                                                               self.decay_channels_[idx]
                                                               )
                                          else :
                                                 self.rescale_histogram(
                                                        histfile,
                                                        directory,
                                                        hist_name,
                                                        masses,
                                                        self.signal_channel_to_cross_section[(std_prod+"_"+std_decay, period)],
                                                        self.decay_channels_[idx]
                                                        )

       def rescale_shift_histograms(self) :
              """
              Rescale all histograms for upper/lower boundaries of shift histograms
              """
              ## extend empty lists by empty strings to allow looping
              for key, value in self.histfile_to_directories.iteritems() :
                     if len(value)==0 :
                            value.append("")
              ## loop files, directories and signal histograms and rescale all apropriate hists
              for histfile in self.output_histfiles :
                     for jdx in range(len(self.histfile_to_directories[histfile])) :
                            directory = self.histfile_to_directories[histfile][jdx]
                            decay_channel = self.histfile_to_decay_channels[histfile][jdx]
                            for idx in self.signal_indexes :
                                   if self.decay_channels_[idx] == decay_channel :
                                          ## standardized production key for cross section mapping
                                          std_prod  = self.standardized_signal_process(self.production_processes[idx])
                                          ## standardized decay key for cross section mapping
                                          std_decay = self.standardized_decay_channel(decay_channel)
                                          ## list of all available masses for this decay channel
                                          masses = self.load_available_masses(decay_channel)
                                          ## modify path to hist file for such decay channels that do not keep
                                          ## signal hists for all masses in one file
                                          for in_separate_files in self.hists_in_separate_files :
                                                 if self.decay_channels_[idx] == in_separate_files :
                                                        if not histfile.find("$MASS")>-1:
                                                               histfile = "../$MASS/"+histfile
                                          ## add prefix to histogram name where needed
                                          hist_name = self.production_processes[idx]
                                          ## define run period for proper histogram scaling according to 7TeV or 8TeV cross sections
                                          period = self.decay_channels_[idx][self.decay_channels_[idx].rfind("_")+1:]
                                          ## rescal histograms for "Up"/"Down" shape uncertainties
                                          for uncertainty, indexes in self.uncertainty_to_signal_indexes.iteritems() :
                                                 for jdx in indexes :
                                                        if jdx == idx :
                                                               if self.decay_channel_to_interpolation_method.has_key(self.decay_channels_[idx]) :
                                                                      if self.decay_channel_to_interpolation_method[self.decay_channels_[idx]] == "non-degenerate-masses-light" :
                                                                             print "using non-degenerate-masses-light mode for shift histograms for decay channel: ", self.decay_channels_[idx]
                                                                             self.rescale_histogram(
                                                                                    histfile,
                                                                                    directory,
                                                                                    hist_name,
                                                                                    masses,
                                                                                    self.signal_channel_to_cross_section[(std_prod+"_"+std_decay, period)],
                                                                                    self.decay_channels_[idx],
                                                                                    uncertainty+"Up",
                                                                                    "light"
                                                                                    )
                                                                             self.rescale_histogram(
                                                                                    histfile,
                                                                                    directory,
                                                                                    hist_name,
                                                                                    masses,
                                                                                    self.signal_channel_to_cross_section[(std_prod+"_"+std_decay, period)],
                                                                                    self.decay_channels_[idx],
                                                                                    uncertainty+"Down",
                                                                                    "light"
                                                                                    )
                                                                      elif self.decay_channel_to_interpolation_method[self.decay_channels_[idx]] == "degenerate-masses" :
                                                                             print "using degenerate-masses mode for shift histograms for decay channel: ", self.decay_channels_[idx]
                                                                             self.rescale_histogram_degenerate(
                                                                                    histfile,
                                                                                    directory,
                                                                                    hist_name,
                                                                                    self.signal_channel_to_cross_section[(std_prod+"_"+std_decay, period)],
                                                                                    self.decay_channels_[idx],
                                                                                    uncertainty+"Up"
                                                                                    )
                                                                             self.rescale_histogram_degenerate(
                                                                                    histfile,
                                                                                    directory,
                                                                                    hist_name,
                                                                                    self.signal_channel_to_cross_section[(std_prod+"_"+std_decay, period)],
                                                                                    self.decay_channels_[idx],
                                                                                    uncertainty+"Down"
                                                                                    )
                                                                      elif self.decay_channel_to_interpolation_method[self.decay_channels_[idx]] == "single-mass" :
                                                                             print "using single-mass mode for shift histograms for decay channel: ", self.decay_channels_[idx]
                                                                             self.rescale_histogram_single_mass(
                                                                                    histfile,
                                                                                    directory,
                                                                                    hist_name,
                                                                                    masses,
                                                                                    self.signal_channel_to_cross_section[(std_prod+"_"+std_decay, period)],
                                                                                    self.decay_channels_[idx],
                                                                                    uncertainty+"Up"
                                                                                    )
                                                                             self.rescale_histogram_single_mass(
                                                                                    histfile,
                                                                                    directory,
                                                                                    hist_name,
                                                                                    masses,
                                                                                    self.signal_channel_to_cross_section[(std_prod+"_"+std_decay, period)],
                                                                                    self.decay_channels_[idx],
                                                                                    uncertainty+"Down"
                                                                                    )
                                                                      else :
                                                                             ## fall back to the default
                                                                             self.rescale_histogram(
                                                                                    histfile,
                                                                                    directory,
                                                                                    hist_name,
                                                                                    masses,
                                                                                    self.signal_channel_to_cross_section[(std_prod+"_"+std_decay, period)],
                                                                                    self.decay_channels_[idx],
                                                                                    uncertainty+"Up"
                                                                                    )
                                                                             self.rescale_histogram(
                                                                                    histfile,
                                                                                    directory,
                                                                                    hist_name,
                                                                                    masses,
                                                                                    self.signal_channel_to_cross_section[(std_prod+"_"+std_decay, period)],
                                                                                    self.decay_channels_[idx],
                                                                                    uncertainty+"Down"
                                                                                    )
                                                               else :
                                                                      self.rescale_histogram(
                                                                             histfile,
                                                                             directory,
                                                                             hist_name,
                                                                             masses,
                                                                             self.signal_channel_to_cross_section[(std_prod+"_"+std_decay, period)],
                                                                             self.decay_channels_[idx],
                                                                             uncertainty+"Up"
                                                                             )
                                                                      self.rescale_histogram(
                                                                             histfile,
                                                                             directory,
                                                                             hist_name+"_"+uncertainty+"Down",
                                                                             masses,
                                                                             self.signal_channel_to_cross_section[(std_prod+"_"+std_decay, period)],
                                                                             self.decay_channels_[idx],
                                                                             uncertainty+"Down"
                                                                             )

       def path(self, directory):
              """
              Add '/' to directory in case it is non-empty.
              """
              path=""
              if not directory=="" :
                     path=directory+"/"
              return path

       def exists(self, file, name) :
              """
              Check whether a given histogram exists in a given file. This is needed to test whether
              shape histograms do exist for shape uncertainties, which can be of type shape?, which
              means that the given uncertainty can be of type shape for some channels, while for
              others it is not.
              """
              hist = file.Get(name)
              return not (type(hist) == ROOT.TObject)

       def load_hist(self, file, name) :
              """
              Load a histogram with name from input histfile. Issue a warning in case the histogram
              is not available.
              """
              hist = file.Get(name)
              if type(hist) == ROOT.TObject :
                     print "hist not found: ", file.GetName(), ":", name
              return hist

       def rate_from_hist(self, file, directory, hist, channel, uncertainty="") :
              """
              Return rate from histogram in output histfile.
              """
              file = ROOT.TFile(file,"READ")
              rate=0.0
              hist=self.load_hist(file, self.expand_histname(channel, hist, uncertainty))
              rate=hist.Integral()
              return rate

       def map_shape_uncertainties(self, words) :
              """
              Add a list of signal indexes to a map of uncertainties
              """
              for idx in range(len(self.production_processes)) :
                     if not words[idx+2] == "-" :
                            if not words[0] in self.uncertainty_to_signal_indexes :
                                   self.uncertainty_to_signal_indexes[words[0]] = [idx]
                            else :
                                   self.uncertainty_to_signal_indexes[words[0]].append(idx)

       def modify_shapes_line(self, words, output_line) :
              """
              Find the output histfile for shape analyses from the list of words. Modify the output histfile name
              to include the values of mA and tanb accordingly. Copy the original output histfile to a new one
              with the new output name. Append the new name of the output file as a unique value to the list of
              self.output_histfiles.

              A single output histfile can serve more than one channel: Append the channel, which corresponds to
              this hist output file to the dictionary of self.histfile_to_decay_channels.

              An output histfile can contain one or more directories to indicate sub-channels or the histograms
              can be safed directly in the root file. Determine the number of directories in the corresponding
              input file and add it to the dictionary of self.histfile_to_directories. If no directories exist
              in the given file an empty list is stored for the given key.

              Histogram names can be different from sample names. Such differences are indicated in column 5
              and 6 of the datacards in the lines that start with keyword 'shape'. fetch potential extensions
              and safe them in the dictionaries self.value_hist_extensions and self.shift_hist_extensions.
              """
              for (idx, word) in enumerate(words):
                     if word.find(".root")>-1 :
                            output_histfile=word.replace(".root", "_%.0f_%.2f.root" % (self.mA, self.tanb))
                            output_line = output_line.replace(word, output_histfile)
                            if not self.output_histfiles.count(output_histfile)>0 :
                                   self.output_histfiles.append(output_histfile)
                                   shutil.copy(word, output_histfile)
                            ## one file can belong to more than one channel; map
                            ## each file to its corresponding channels
                            channel = self.find_decay_channel(words[2])
                            self.append_unique_value(self.histfile_to_decay_channels, output_histfile, channel)
                            ## figure out which directories exist in which files
                            directories = self.find_directories_in_histfile(words)
                            for directory in directories :
                                   self.append_unique_value(self.histfile_to_directories, output_histfile, directory)
                     ## determine histogram name modifications for all samples in consideration
                     unique_sample = self.find_decay_channel(words[2])+'/'+words[1]
                     if idx == 4 :
                            ## determines the full path for value histograms
                            if not unique_sample in self.value_hist_extensions :
                                   self.value_hist_extensions[unique_sample] = word
                                   #word[word.find('/')+1:]
                     if idx == 5 :
                            ## determines the full path for shift histograms
                            if not unique_sample in self.shift_hist_extensions :
                                   self.shift_hist_extensions[unique_sample] = word
                                   #word[word.find('/')+1:]
              return output_line

       def modify_rates_line(self, words, output_line) :
              """
              Modify the rates in the 'rates' output line in the output datacard. The new rate is
              read out from the rescaled histograms for the central values.
              """
              self.load_uncertainties_map()
              self.load_cross_sections_map()
              self.rescale_value_histograms()
              for idx in self.signal_indexes :
                     cut_and_count = True
                     ## first deal with signals with shapes
                     for histfile in self.output_histfiles :
                            for jdx in range(len(self.histfile_to_directories[histfile])) :
                                   directory = self.histfile_to_directories[histfile][jdx]
                                   decay_channel = self.histfile_to_decay_channels[histfile][jdx]
                                   if self.decay_channels_[idx] == decay_channel :
                                          cut_and_count = False
                                          hist_name = self.production_processes[idx]
                                          output_list = output_line.split()
                                          output_list[idx+1] = str(self.rate_from_hist(histfile, directory, hist_name, self.decay_channels_[idx]))
                                          output_line = '\t   '.join(output_list)+'\n'
                     ## cut and count channels
                     if cut_and_count :
                            contracted_cross_section_mode = 0
                            if self.decay_channel_to_interpolation_method[self.decay_channels_[idx]] == "degenerate-masses" :
                                   contracted_cross_section_mode = 1
                            if self.decay_channel_to_interpolation_method[self.decay_channels_[idx]] == "single-mass" :
                                   contracted_cross_section_mode = 2
                            ## define run period for proper histogram scaling according to 7TeV or 8TeV cross sections
                            period = self.decay_channels_[idx][self.decay_channels_[idx].rfind("_")+1:]
                            xsec = self.contracted_cross_section(
                                   self.standardized_signal_process(self.production_processes[idx]),
                                   self.standardized_decay_channel(self.decay_channels_[idx]),
                                   period,
                                   contracted_cross_section_mode
                                   )
                            output_list = output_line.split()
                            new_rate = float(output_list[idx+1])*xsec/(1. if self.sm_like else self.tanb)
                            output_list[idx+1] = str(new_rate)
                            output_line = '\t   '.join(output_list)+'\n'
              return output_line

       def add_uncertainty_lines(self) :
              """
              Determine additional lines that are needed for the uncertainties. For each signal
              process type (ggH, qqH, bbH, VH) two additional uncertainties are added for Scale
              and for PDF to the datacard. In this function all signal processes are looped and
              at first occurence of each process a line is prepared for the corresponding
              uncertainty. This line starts with the word $PROCESSScale or $PROCESSPDF and has
              the uncertainty at the position of the given process and a '-' for all all other
              processes.
              """
              for idx in self.signal_indexes :
                     signal = self.standardized_signal_process(self.production_processes[idx])
                     for key in self.standardized_signal_process_to_uncertainty_heads :
                            if key == signal :
                                   for uncertainty in self.standardized_signal_process_to_uncertainty_heads[key] :
                                          if not self.signal_channel_to_uncertainty_lines.has_key(uncertainty) :
                                                 ## add entry to dictionary if it does not yet exist
                                                 ## initialize line with line head for uncertainties
                                                 self.signal_channel_to_uncertainty_lines[uncertainty] = uncertainty+" \t\t lnN \t\t"
                                                 for jdx in range(len(self.production_processes)) :
                                                        if self.standardized_signal_process(self.production_processes[jdx]) == key :
                                                               prod = self.standardized_signal_process(self.production_processes[jdx])
                                                               decay = self.standardized_decay_channel(self.decay_channels_[jdx])
                                                               contracted_cross_section_mode = 0
                                                               if self.decay_channel_to_interpolation_method[self.decay_channels_[jdx]] == "degenerate-masses" :
                                                                      contracted_cross_section_mode = 1
                                                               if self.decay_channel_to_interpolation_method[self.decay_channels_[jdx]] == "single-mass" :
                                                                      contracted_cross_section_mode = 2
                                                               ## define run period for proper histogram scaling according to 7TeV or 8TeV cross sections
                                                               period = self.decay_channels_[idx][self.decay_channels_[idx].rfind("_")+1:]
                                                               ## add uncertainties for given process
                                                               if uncertainty.find("Scale")>-1 :
                                                                      cross_section = self.contracted_cross_section(prod, decay, period, contracted_cross_section_mode)
                                                                      uncert_upper  = self.contracted_uncertainty(prod, decay, period, "mu" , "+")
                                                                      uncert_lower  = self.contracted_uncertainty(prod, decay, period, "mu" , "-")
                                                                      if cross_section>0. and uncert_lower/cross_section!=1 :
                                                                             self.signal_channel_to_uncertainty_lines[uncertainty] += " \t\t %.3f/%.3f " % \
                                                                             (1./(1.-uncert_lower/cross_section), 1.+uncert_upper/cross_section)
                                                                      else :
                                                                             self.signal_channel_to_uncertainty_lines[uncertainty] += " \t\t  0.1 "
                                                               if uncertainty.find("PDF"  )>-1 :
                                                                      cross_section = self.contracted_cross_section(prod, decay, period, contracted_cross_section_mode)
                                                                      uncert_upper  = self.contracted_uncertainty(prod, decay, period, "pdf", "+")
                                                                      uncert_lower  = self.contracted_uncertainty(prod, decay, period, "pdf", "-")
                                                                      if cross_section>0. :
                                                                             uncert = (1./(1.+uncert_lower/cross_section))/(1.+uncert_upper/cross_section)
                                                                             self.signal_channel_to_uncertainty_lines[uncertainty] += " \t\t %.3f/%.3f " % \
                                                                             (1./(1.+uncert_lower/cross_section), 1.+uncert_upper/cross_section)
                                                                      else :
                                                                             self.signal_channel_to_uncertainty_lines[uncertainty] += " \t\t  0.1 "
                                                        else :
                                                               ## add dash for all other processes
                                                               self.signal_channel_to_uncertainty_lines[uncertainty] += " \t\t - "


if len(args) < 1 :
       parser.print_help()
       exit(1)

## decide whether to run with acceptions or not 
acc_corr = False if options.no_acc_corr else True
## skip first pass of 'bin'
first_pass_on_bin = True
## name of the input datacard
input_name = args[0]
## setup datacard creator
print "creating datacard for mA=%s, tanb=%s" % (options.mA, options.tanb)
if options.model.find("feyn-higgs")>-1:
       model = options.model[options.model.find("::")+2:]
       datacard_creator = MakeDatacard(tanb=float(options.tanb), mA=float(options.mA), feyn_higgs_model=options.model[options.model.find("::")+2:], sm_like=options.sm_like, acc_corr=acc_corr)
else:
       datacard_creator = MakeDatacard(tanb=float(options.tanb), mA=float(options.mA), model=options.model, sm_like=options.sm_like, acc_corr=acc_corr)
datacard_creator.init(options.interpolation_mode)

## first file parsing
input_file = open(input_name,'r')
output_file = open(input_name.replace(".txt", "_%.2f.txt" % float(options.tanb)), 'w')
for input_line in input_file :
       words = input_line.split()
       output_line = input_line
       if len(words) < 1: continue
       ## determine a list of unique decay channels
       if words[0] == "Combination" :
              datacard_creator.initial_datacards = datacard_creator.decay_channels(words)
       ## need to fix kmax in the head of the file here
       if words[0] == "kmax" :
              output_line = output_line.replace(words[1], " *")
       ## determine which file and directory structures to take care of for this combination
       if words[0] == "shapes":
              output_line = datacard_creator.modify_shapes_line(words, output_line)
       ## determine the list of all single channels (in standardized format, multiple occurences possible)
       if words[0] == "bin" :
              if not first_pass_on_bin :
                     for (idx, word) in enumerate(words) :
                            if idx==0 :
                                   continue
                            datacard_creator.decay_channels_.append(word)
              first_pass_on_bin = False
       ## determine which processes are actually signal (processes correspond to the shape histograms in case of shape analyses)
       ## the way to determine signal processes is by the process id smaller equal 0. The indexes of all signal processes are
       ## kept in signal_indexes. These can be used to look up the signals in signal_processes and the according channel these
       ## belong to in signal_channels
       if words[0] == "process" :
              for (idx, word) in enumerate(words) :
                     if idx==0 :
                            continue
                     if word.isdigit() or word.lstrip("-").isdigit() :
                            if int(word) <=0 :
                                   datacard_creator.signal_indexes.append(idx-1)
                     else :
                            datacard_creator.production_processes.append(word)
       ## modify rates for central values
       if words[0] == "rate" :
              ## manipulate histograms
              output_line = datacard_creator.modify_rates_line(words, output_line)
       ## map shape uncertainties to individual signal channels, for uncertainties,
       ## which are of type shape only for a subset of channels the keyword is
       ## shape?. In this case datacard_creator.rescale_histograms(...) has to find
       ## out on its own, whether really a histogram exists for a given uncertainty
       ## or not
       if len(words)>1 and words[1].find("shape")>-1 :
              ## map out the shape uncertainties for later rescaling of hists
              datacard_creator.map_shape_uncertainties(words)
       ## write output line to output file
       output_file.write(output_line)

## rescale the shape uncertainty histograms
datacard_creator.rescale_shift_histograms()
## map out the uncertainty lines for scale and pdf uncertainties
datacard_creator.add_uncertainty_lines()
## add new scale and pdf uncertainties for new datacard
for signal_channel, uncertainy_lines in datacard_creator.signal_channel_to_uncertainty_lines.iteritems() :
       output_file.write(datacard_creator.signal_channel_to_uncertainty_lines[signal_channel]+"\n")

##close files
higgs_file.close()
input_file.close()
output_file.close()
print "done"
