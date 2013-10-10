import os
import re
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

ROOT.gSystem.Load('$CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit.so')
from ROOT import th1fmorph

class Morph:
    def __init__(self,input,directories,samples,uncerts,masses,step_size,verbose,extrapolate,trivial):
        ## verbose
        self.verbose = verbose
        ## trivial
        self.trivial = trivial
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
        ## list of mass points outside the range
        self.extrapolations = [x for x in re.sub(r'\s', '', extrapolate).split(',') if x != '']

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
        if self.trivial :
            if abs(float(value)-float(lower)) < abs(float(upper)-float(value)) :
                hist_morph = hist_lower.Clone(name.format(MASS=value)); hist_morph.SetTitle(name.format(MASS=value)); hist_morph.Scale(norm/hist_morph.Integral())
            else :
                hist_morph = hist_upper.Clone(name.format(MASS=value)); hist_morph.SetTitle(name.format(MASS=value)); hist_morph.Scale(norm/hist_morph.Integral())
        else :
            hist_morph = th1fmorph(name.format(MASS=value),name.format(MASS=value),hist_lower, hist_upper, float(lower), float(upper), float(value), norm, 0)
        # th1fmorph() will set a value null if you are right on top of it
        if not hist_lower and lower == value:
            hist_lower = hist_morph
        if not hist_upper and upper == value:
            hist_upper = hist_morph
        if self.verbose :
            print "writing morphed histogram to file: name =", hist_morph.GetName(), "integral =[ %.5f | %.5f | %.5f ]" % (hist_lower.Integral(), hist_morph.Integral(), hist_upper.Integral())
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
            if self.verbose:
                print "Morphing directory: %s" % dir
            for sample in self.samples :
                # Keep track of morphings that need to be done.  This list
                # holds tuples with (low, high, target) masses.
                masses_to_morph = []
                if self.verbose:
                    print "Morphing sample: %s" % sample
                for idx in range(len(self.masses)-1) :
                    nbin = int((float(self.masses[idx+1])-float(self.masses[idx]))/self.step_size)
                    if nbin > 1 :
                        for x in range(nbin-1) :
                            # This formatting is valid for 0.5 GeV bins up to TeV
                            # Returns 111 for 111.0, 111.5 for 111.5
                            value = "%.4g" % (float(self.masses[idx])+(x+1)*float(self.step_size))
                            masses_to_morph.append((self.masses[idx], self.masses[idx+1], value))
                            if self.verbose:
                                print "Morphing %0.1f between (%0.1f, %0.1f)" % tuple(float(x) for x in (value, self.masses[idx], self.masses[idx+1]))
                    else :
                        if self.verbose :
                            print "nothing needs to be done here: nbin =", nbin
                # Extrapolate outside the pivot range, if desired.
                for mass in self.extrapolations:
                    if float(mass) < float(self.masses[-1]) and float(mass) > float(self.masses[0]):
                        raise ValueError("The point %f does not need to be extrapolated, it is within the pivot range" % mass)
                    # Check if we are extrapolating on the high end or low end.
                    if float(mass) > float(self.masses[-1]):
                        # High end
                        masses_to_morph.append(
                            (self.masses[-2], self.masses[-1], mass)
                        )
                    else:
                        # Low end
                        masses_to_morph.append(
                            (self.masses[0], self.masses[1], mass)
                        )
                    #import pdb; pdb.set_trace()
                    print "Extrapolating [%0s, %0s] -> %0s" % masses_to_morph[-1]

                for mass_low, mass_high, value in masses_to_morph:
                    self.morph_hist(file, dir, sample, mass_low, mass_high, value)
                    for uncert in self.uncerts :
                        try:
                            if not uncert == '' :
                                self.morph_hist(file, dir, sample+'_'+uncert+'Up', mass_low, mass_high, value)
                                self.morph_hist(file, dir, sample+'_'+uncert+'Down', mass_low, mass_high, value)
                        except AttributeError:
                            print "Warning: could not find shape systematic %s, skipping"  % uncert
