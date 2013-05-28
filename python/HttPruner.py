import re
import ROOT

from HiggsAnalysis.CombinedLimit.DatacardPruner import DatacardPruner

class HttPruner(DatacardPruner) :
    """
    Description:

    This class is derived from the class DatacardPruner. The base class is extended by an option to prevent nuisance
    parameters, which are supposed to correspond to bin-by-bin uncertainties in pre-defined windows of the input histograms
    to be pruned. These windows are supposed to be given as a tuple of type (center, size), where center corresponds to the
    center of the window and size to its relative size. Nuisance parameters that correspond to bin-by-bin uncertainties are
    supposed to contain a regex of type '\s*\w+bin\_*(\d*)' in their name as it is automatically the case when using the htt
    tool to add bin-by-bin uncertainties.
    """
    def __init__(self, fit_results, metric='max', mass='125', threshold='0.05', blacklist=[], whitelist=[], comment_nuisances=False, windows=[], pattern='\s*\w+bin\_*(\d*)') :
        ## list of windows of type (center, size)
        self.windows = windows
        ## python like regex to indicate bin-by-bin uncertainties
        self.pattern = pattern
        ## initialize base class
        super(HttPruner, self).__init__(fit_results, metric, mass, threshold, blacklist, whitelist, comment_nuisances)
        
    def save_bbb(self, TDIR, SAVES=[]) :
        """
        uses: TDIR (root directory  that should be searched for histograms), SAVES (list of histograms that have been saved as
        they fall into the shielding windows) , self.windows
        Check TDIR for histograms that follow the pattern corresponding to bin-by-bin uncertainties. From these histograms the
        bins of the lower_bounds and upper_bounds are determined. If the bin of the uncertainty falls between these bins, the
        histgoram is added to the list of SAVES. If a directory is found in TDIR, the function will be called iteratively.
        """
        bbb_pattern = re.compile(self.pattern+'Up')
        for key in TDIR.GetListOfKeys() :
            name=key.GetName()
            if key.GetClassName().startswith('TDirectory') :
                self.save_bbb(TDIR.Get(name), SAVES)
            else :
                if isinstance(TDIR.Get(name), ROOT.TH1) :
                    ## look for the bin-by-bin pattern and determine the bin at the same time
                    bin = bbb_pattern.findall(name)
                    if bin :
                        hist = TDIR.Get(name)
                        for window in self.windows :
                            lower_bound = float(window[0])*(1-float(window[1]))
                            upper_bound = float(window[0])*(1+float(window[1]))
                            if hist.GetXaxis().FindBin(lower_bound)<=int(bin[0]) and int(bin[0])<=hist.GetXaxis().FindBin(upper_bound) :
                                SAVES.append(name[name.find('CMS'):name.find('Up')])
        return SAVES
    
    def saves_by_rootfiles(self, FILENAMES) :
        """
        uses: FILENAMES (list of relative paths to the root files to be checked for bin-by-bin uncertainties)
        Check the root files with paths FILENAMES for bin-by-bin uncertainty histograms and determine the bins of the lower
        and upper bounds corresponding to the central values and sizes of the defined windows. If the bin the histogram
        corresponds to falls between these bins the uncertainty name is added to the list of histograms to be saved, which
        is the return value.
        """
        saves = []
        for filename in FILENAMES :
            input = ROOT.TFile(filename, 'READ')
            if not input :
                raise IOError("Can't open input file: %s" % filename)
            saves.extend(self.save_bbb(input))
            input.Close()
        return saves

    def saves_by_datacard(self, DATACARD) :
        """
        uses: DATACARD (absolute path to datacard), PATH (absolute path to the location of the original datacards)
        Parse DATACARD and determine all root input files that DATACARD refers to. From the list of root input files
        determine the list of bin-by-bin uncertainty histograms. From this list determine the the bin-by-bin histograms to be
        saved by shielding.
        """
        rootfiles = []
        file = open(DATACARD, 'r')
        for line in file :
            words = line.lstrip().split()
            if words[0] == 'shapes' :
                rootfile = words[3]
                if not rootfile in rootfiles :
                    rootfiles.append(rootfile)
        file.close()
        return self.saves_by_rootfiles(rootfiles)

    def shield_bbb_uncertainties(self, DATACARD, DROPPED, KEPT) :
        """
        uses: DATACARD (absolute path to the datacard under investigation), PATH (absolute path to the location of the
        original datacards), DROPPED (list of dropped uncertainties), KEPT (list of kept uncertainties)
        Determine the bin-by-bin uncertainties, which should be shielded from DATACARD. Check DROP for shielded bin-by-bin
        uncertainties and sort those form DRPOPPED to KEPT.
        """
        rescued = 0
        reduced_dropped = []
        saves = self.saves_by_datacard(DATACARD)
        for unc in DROPPED :
            if unc in saves :
                rescued+=1
                KEPT.append(unc)
            else :
                reduced_dropped.append(unc)
        return (reduced_dropped, rescued)
