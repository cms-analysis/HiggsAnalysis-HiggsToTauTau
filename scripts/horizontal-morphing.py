#!/usr/bin/env python

from optparse import OptionParser
       
parser = OptionParser(usage="usage: %prog [options] datacatd.txt",
                      description="script to apply horizontal template morphing for htt datacards to estimate masses, which have not been simulated.")
parser.add_option("--categories", dest="categories", default="emu_vbf,emu_boost, emu_novbf", type="string", help="List of event categories to be morphed; can be given as comma separated list of strings with an aritary number of whitespaces. [Default: 'vbf,boost,novbf']")
parser.add_option("--samples", dest="samples", default="ggH{MASS},qqH{MASS}", type="string", help="List of signal samples to be morphed; can be given as comma separated list of strings with an aritary number of whitespaces. The sample name is expected to include the key word {MASS}. [Default: 'ggH{MASS}, qqH{MASS}']")
parser.add_option("--uncerts", dest="uncerts", default="CMS_res_e", type="string", help="List of uncertainty/ies to be considered for morphing; can be given as comma separated list of strings with an aribtary number of whitespaces. The sample name will be completed in the form: {SAMPLE}_{UNCERT}Up/Down. [Default: 'CMS_res_e']")
parser.add_option("--masses", dest="masses", default="110,115,120,125,130,135,140,145", type="string", help="List pivotal mass points for morphing; can be given as comma separated list of strings with an aribtary number of whitespaces. [Default: '110,115,120,125,130,135,140,145']")
parser.add_option("--step-size", dest="step_size", default="1", type="string", help="Step-size for morphing in GeV of the mass. [Default: 1]")
parser.add_option("-i", "--input", dest="input", default='testFile.root', type="string", help="Input file for morphing. Note that the file will be updated [Default: 'testFile.root']")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="Run in verbose mode")
(options, args) = parser.parse_args()


import os
import re
import ROOT

ROOT.gSystem.Load('$CMSSW_BASE/lib/slc5_amd64_gcc434/libHiggsAnalysisCombinedLimit.so')
from ROOT import th1fmorph


class Morph:
    def __init__(self,input,directories,samples,uncerts,masses,step_size,verbose):
        ## verbose
        self.verbose = verbose
        ## input file
        self.input = input
        ## step size
        self.step_size = float(step_size)
        ## list of pivotal masses
        self.masses = re.sub(r'\s', '', masses ).split(',')
        ## list of samples
        self.samples = re.sub(r'\s', '', samples).split(',')
        ## list of uncertainties
        self.uncerts = re.sub(r'\s', '', uncerts).split(',')
        ## list of event categories
        self.directories = re.sub(r'\s', '', directories).split(',')
        
    def load_hist(self, file, directory, name) :
        """
        Load a histogram with name from input histfile. Issue a warning in case the histogram
        is not available.
        """
        hist = file.Get(directory+'/'+name)
        if type(hist) == ROOT.TObject :
            print "hist not found: ", file.GetName(), ":", directory+'/'+name
        return hist

    def zero_safe(self, hist) :
        """
        Make sure that no pivotal histograms are passed to the template morphing, which are
        completely empty. This will cause the template morphing to explode. Voice a warning
        as this is only a technical workaround. This situation should be fixed asap.
        """
        if hist.Integral() == 0 :
            print "Warning: histogram ", hist.GetName(), "is empty!" 
            hist.SetBinContent(1, 10e-6)
        return hist

    def norm_hist(self, hist_lower, hist_upper, lower, upper, value) :
        """
        Determine the normalization for the morphed histogram from the lower and
        upper boundary histograms.
        """
        norm = 1.
        if upper>lower :
            norm = hist_lower.Integral()+(hist_upper.Integral()-hist_lower.Integral())/abs(upper-lower)*(value-lower)
        return norm

    def morph_hist(self, file, directory, name, lower, upper, value) :
        """
        Load histograms with name NAME that correspond to upper and lower bound,
        determine morphed histogram corresponding to VALUE, and write the morphed
        histogram to file.
        """
        #print "loading fingerprint: ", file, directory, name
        hist_lower = self.zero_safe(self.load_hist(file, directory, name.format(MASS=lower)))
        hist_upper = self.zero_safe(self.load_hist(file, directory, name.format(MASS=upper)))
        norm = self.norm_hist(hist_lower, hist_upper, float(lower), float(upper), float(value))
        hist_morph = th1fmorph(name.format(MASS=value),name.format(MASS=value),hist_lower, hist_upper, float(lower), float(upper), float(value), norm, 0)
        if self.verbose :
            print "writing morphed histogram to file: name =", hist_morph.GetName(), "integral =", hist_morph.Integral()
        if directory == "" :
            file.cd()
        else :
            file.cd(directory)
        hist_morph.Write(hist_morph.GetName())

    def run(self) : 
        """
        Open input rootfile, loop all directories and samples. Pick pivotal masses
        and apply horizontal template morphing for all samples and systematic shifts.  
        """
        file = ROOT.TFile(self.input, "UPDATE")
        if not file :
            print "file not found: ", self.input 
        for dir in self.directories :
            for sample in self.samples :
                for idx in range(len(self.masses)-1) :
                    nbin = int(float(self.masses[idx+1])-float(self.masses[idx])/self.step_size)
                    for x in range(nbin-1) :
                        value = "%.0f" % (float(self.masses[idx])+(x+1)*float(self.step_size))
                        self.morph_hist(file, dir, sample, self.masses[idx], self.masses[idx+1], value)
                        for uncert in self.uncerts :
                            if not uncert == '' :
                                self.morph_hist(file, dir, sample+'_'+uncert+'Up', self.masses[idx], self.masses[idx+1], value)
                                self.morph_hist(file, dir, sample+'_'+uncert+'Down', self.masses[idx], self.masses[idx+1], value)
                    
template_morphing = Morph(options.input,options.categories,options.samples,options.uncerts,options.masses,options.step_size,options.verbose)
template_morphing.run()
