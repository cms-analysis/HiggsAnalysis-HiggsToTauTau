import re
import ROOT

## needed to make th1morph known to class
ROOT.gSystem.Load('$CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit.so')
from ROOT import th1fmorph

class ModelTemplate():
    """
    Description:

    This class is meant to provide template histograms for arbitary (BSM) Higgs signal processes based on raw templates for
    these processes for a given set of pivotal masses. It requires the masses of the Higgs bosons contributing to the given
    process and a normalization factor corresponding to the cross section times BR of the Higgs boson in the corresponding
    model. the latter are passed in for of MODEL_PARAMS.
    """
    def __init__(self, path) :
        ## path to root input file
        self.path = path
        ## root input file where to find the raw templates
        self.input_file = ROOT.TFile(path)
        ## dict of type {dir : [pivotal masses]} for each dir in the root file
        self.pivotals = {}

    def __del__(self) :
        ## close input root file
        self.input_file.Close()
        
    def fill_pivotals(self, proc, dir) :
        """
        Loop all objects for given proc in dir. When another directory is found decend. When an object of type TH1 is found
        check for an exact match to proc+integer/float. Each exact match corresponds to a raw mass template in dir. The
        integer/float to the mass value, which is added to the list of pivotal masses for the given directory. The complete
        list of pivotal masses is added with the name dir as key to the dictionary self.pivotals. The file self is also added
        to the dictionary with key '.'.
        """
        ## list of pivotals in dir
        pivotals = []
        ## match for raw templates for different masses and process proc
        proc_match = re.compile("{PROC}(\d*.?\d*)$".format(PROC=proc))
        ## iterate each object in dir
        for key in dir.GetListOfKeys() :
            name=key.GetName()
            if key.GetClassName().startswith('TDirectory') :
                self.fill_pivotals(proc, dir.Get(name))
            else :
                if isinstance(dir.Get(name), ROOT.TH1) :
                    for pivotal in proc_match.findall(name) :
                        if not pivotal in pivotals :
                            pivotals.append(pivotal)
        if not dir.GetName() in self.pivotals.keys() :
            self.pivotals['.' if dir.GetName() == self.input_file.GetName() else dir.GetName()] = pivotals
        return

    def load_hist(self, name) :
        """
        Load a histogram with name from file. Issue a warning in case the histogram is not available. In this case the class
        will most probably crash, but at least one know which histogram was searched for and not found.
        """
        hist = self.input_file.Get(name)
        if type(hist) == ROOT.TObject :
            print "hist not found: ", self.input_file.GetName(), ":", name
        return hist

    def pivotal_mass_window(self, mass, pivotals) :
        """
        Determine closest pivotal above and below mass. The return value is a tuple of type (lower_pivotal,upper_pivotal). If
        mass is available as pivotal lower_pivotal==upper_pivotal will be returned. If mass is smaller than the lowest pivotal
        lower_pivotal will be larger than mass. If mass is larger than the highest pivotal upper_pivotal will be smaller than
        mass. The corresponding values for upper_pivotal/lower_pivotal will loose their meaning in these cases. In case that
        the list of pivotals is empty None will be returned. The pivotal mass window is used for linear scale interpolation.
        """
        pmw = None
        if len(pivotals)>0 :
            ## get index and value of closest element to mass in list of pivotals
            (idx, value) = min(enumerate(pivotals), key=lambda x: abs(float(x[1])-mass))
            if float(value) > mass :
                pmw = (pivotals[max(idx-1,0)],value)
            elif float(value) == mass :
                pmw = (value,value)
            else :
                pmw = (value,pivotals[min(idx+1,len(pivotals)-1)])
        return pmw

    def interpolation_scale(self, start, stop, x) :
        """
        Determine the residual scale due to differences in acceptance and reconstruction efficiency when interpolating from
        embracing pivotal masses to mass. Start and stop are passed tuples of type (x-value,y-value). x is the value to
        interpolate to.
        """
        return 1+(stop[1]-start[1])/(stop[0]-start[0])/start[1]*(x-start[0])

    def single_template(self, dir, proc, mass, scale, MODE='MORPHED') :
        """
        Return a single template histogram for a given dir, proc and mass. The histogram will be scaled by scale (corres-
        ponding to the cross section times BR of the corresponding Higgs boson). Scale will be modified by a linea inter-
        polation scale taking into account difference in acceptance and reconstruction efficiency as a function of mass.
        Two modes exist to determine the template: MORPHED - will use horizontal template morphing (the morphing will
        always be applied from the pivotal, which is closest to mass to minimize uncertainties from the interplation);
        CLOSEST_NEIGHBOUR - will use the closest mass point in the list of pivotals w/o any additional horizontal inter-
        polation. 
        """
        ## window of closest pivotal masses below/above mass. Window can be None, if no pivotals exist for a given dir. In
        ## this case retiurn None
        window = self.pivotal_mass_window(float(mass), self.pivotals[dir])
        if not window :
            return None
        if float(window[0]) == float(mass) and float(mass) == float(window[1]) :
            ## exact match with pivotal: clone exact pivotal
            single_template = self.load_hist(dir+'/'+proc+mass).Clone(proc+'_template')
        elif float(window[0]) > float(mass) :
            ## mass out of bounds of pivotals (too small)
            single_template = self.load_hist(dir+'/'+proc+window[0]).Clone(proc+'_template')
        elif float(window[1]) < float(mass) :
            ## mass out of bounds of pivotals (too large)
            single_template = self.load_hist(dir+'/'+proc+window[1]).Clone(proc+'_template')
        else :
            ## mass somewhere between pivotals: masses is the tuple of the embracing pivotals, histos is the tuple of
            ## corresponding template histograms. The closest pivotal to mass is the first element in each of the tuples,
            ## the further away pivotal is second.
            if (float(mass) - float(window[0])) < (float(window[1]) - float(mass)) :
                ## lower bound pivotal closer to mass
                masses = (float(window[0]),float(window[1]))
                histos = (self.load_hist(dir+'/'+proc+window[0]),self.load_hist(dir+'/'+proc+window[1]))
            else :
                ## upper bound pivotal closer to mass
                masses = (float(window[1]),float(window[0]))
                histos = (self.load_hist(dir+'/'+proc+window[1]),self.load_hist(dir+'/'+proc+window[0]))
            scale*= self.interpolation_scale((float(masses[0]),histos[0].Integral()), (float(masses[1]),histos[1].Integral()), float(mass))
            if MODE == 'MORPHED' :
                single_template = th1fmorph(proc+'_template', proc+mass, histos[0], histos[1], masses[0], masses[1], float(mass), scale*histos[0].Integral(), 0)
            if MODE == 'CLOSEST_NEIGHBOUR' :
                single_template = histos[0].Clone(proc+'_template'); single_template.Scale(scale)
        return single_template

    def create_templates(self, model, label, MODE='MORPHED') :
        """
        Determine a combined template build up from single templates for Higgs bosons with different masses and cross sections.
        Model is expected to be a dictionary of type {proc : MODEL_PARAMS}, where all information about available Higgses,
        their masses, BRs and cross sections are encoded in the class MODEL_PARAMS. Proc indicated the process to which
        MODEL_PARAMS applies. Proc should be present as a raw template for at least one mass in the root input file. The
        pivotal masses that do exist for each corresponding proc in each directory of the root input files are determined. The
        single templates are detrived and added. The directory structure relevant for each proc is set up in a root output
        file to which these new combined templates are written to. The output file will be located in the same directory as
        the root input file. It will be distinguished by the postfit label from the input file. It will only contain the
        combined signal templates for the proc given as keys in model.
        """
        output_file = ROOT.TFile(self.path+label, 'UPDATE')
        for (proc,param) in model.iteritems() :
            self.fill_pivotals(proc, self.input_file)
            for dir in self.pivotals.keys() :
                ## skip directories that did not contain templates for proc in the input file
                if len(self.pivotals[dir]) == 0 :
                    continue
                ## build up directory structure in output file
                if not output_file.GetDirectory(dir) :
                    if not dir == '.' :
                        output_file.mkdir(dir)
                ## build up combined template histogram
                combined_template = None
                for higgs in param.list_of_higgses :
                    scale = float(param.xsecs[higgs])*float(param.brs[higgs])
                    histo = self.single_template(dir, proc, param.masses[higgs], scale, MODE)
                if combined_template :
                    combined_template.Add(histo)
                else:
                    combined_template = histo
                ## write combined template to output file
                output_file.cd('' if dir == '.' else dir)
                if combined_template :
                    print 'write histogram to file: ', proc+param.masses['A']  
                    combined_template.Write(proc+param.masses['A'], ROOT.TObject.kOverwrite)
        output_file.Close()
        return 
                    
def main() :
    ## toy model 
    class MODEL_PARAMS():
        def __init__(self) :
            self.list_of_higgses = ['A', 'H', 'h']
            self.masses = {'A' : '120', 'H' : '130', 'h' : '118'}
            self.xsecs  = {'A' : '3'  , 'H' : '2'  , 'h' : '1'  }
            self.brs    = {'A' : '0.1', 'H' : '0.1', 'h' : '0.1'}
            self.tanb   = 15
    param = MODEL_PARAMS()
    model = {'ggH': param,
             'qqH': param
             }

    ## and do the testing
    template = ModelTemplate("htt_mt.input_8TeV.root")
    template.create_templates(model, '_test')

main()
