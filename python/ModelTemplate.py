import re
import ROOT

## structure for parameters of given models
from HiggsAnalysis.HiggsToTauTau.MODEL_PARAMS import MODEL_PARAMS
## needed to make th1morph known to class
ROOT.gSystem.Load('$CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit.so')
from ROOT import th1fmorph

class ModelTemplate():
    """
    Description:

    This class is meant to provide template histograms for arbitary (BSM) Higgs signal processes based on raw templates for
    these processes for a given set of pivotal masses. It requires the masses of the Higgs bosons contributing to the given
    process and a normalization factor corresponding to the cross section times BR of the Higgs boson in the corresponding
    model. The latter are passed in form of MODEL_PARAMS. The class will automatically determine all shapes for central value
    and all available shape uncertainties for each bin (=directory in the root input file) and each available pivotal for
    each bin.
    """
    def __init__(self, path, parameter1, ana_type='', hist_label='', verbosity=0) :
        ## path to root input file
        self.path = path
        ## root input file where to find the raw templates
        self.input_file = ROOT.TFile(path)
        ## a label that can optionally be added to the new model template, when writing it to file
        self.hist_label = hist_label
        ## dict of type {dir : [pivotal masses]} for each dir in the root file
        self.pivotals = {}
        ## dict of type {dir : [shape_labels]} for each dir in the root file. The central shape has an empty label. The shapes
        ## for uncertainties are saved from the last digit of the mass value till the end of the name string.
        self.shape_labels = {}
        ## determine verbosity level
        self.verbosity = verbosity
        ## ana-type
        self.ana_type = ana_type
        ## mass of A or in the case of the lowmH scenario its mu
        self.parameter1 = parameter1

    def __del__(self) :
        ## close input root file
        self.input_file.Close()

    def fill_shape_labels(self, proc, dir) :
        """
        Loop all objects for a given proc in dir. When another directory is found decend. When an object of type TH1 is found
        check for a match to proc+integer/float. Add any remainder beyond the last digit of the float to self.shape_labels.
        This is needed to pick up all shapes corresponding to central value or to shape uncertainties.
        """
        ## list of pivotals in dir
        shape_labels = []
        ## match for raw templates for different masses and process proc
        proc_match = re.compile("{PROC}(?P<MASS>[0-9]*\.?[0-9]*)(?P<LABEL>_?\w*)?".format(PROC=proc))
        ## iterate each object in dir
        for key in dir.GetListOfKeys() :
            name=key.GetName()
            if key.GetClassName().startswith('TDirectory') :
                self.fill_shape_labels(proc, dir.Get(name))
            else :
                if isinstance(dir.Get(name), ROOT.TH1) :
                    if proc_match.match(name) :
                        shape_label = proc_match.match(name).group('LABEL')
                        mass_label  = proc_match.match(name).group('MASS' )
                        if not shape_label in shape_labels :
                            shape_labels.append(shape_label)
        if not dir.GetName() in self.shape_labels.keys() :
            self.shape_labels['.' if dir.GetName() == self.input_file.GetName() else dir.GetName()] = shape_labels
        return

    def fill_pivotals(self, proc, label, dir) :
        """
        Loop all objects for a given proc and label in dir. When another directory is found decend. When an object of type
        TH1 is found check for an exact match to proc+integer/float+label. Each exact match corresponds to a raw mass template
        in dir. The integer/float to the mass value, which is added to the list of pivotal masses for the given directory. The
        complete list of pivotal masses is added with the name dir as key to the dictionary self.pivotals. The file itself is
        also added to the dictionary with key '.'.
        """
        ## list of pivotals in dir
        pivotals = []
        ## match for raw templates for different masses and process proc
        proc_match = re.compile("^{PROC}([0-9]+\.?[0-9]*){LABEL}$".format(PROC=proc, LABEL=label))
        ## iterate each object in dir
        for key in dir.GetListOfKeys() :
            name=key.GetName()
            if key.GetClassName().startswith('TDirectory') :
                self.fill_pivotals(proc, label, dir.Get(name))
            else :
                if isinstance(dir.Get(name), ROOT.TH1) :
                    for pivotal in proc_match.findall(name) :
                        if dir.Get(name).Integral()>0 :
                            if not pivotal in pivotals:
                                pivotals.append(pivotal)
        if not dir.GetName() in self.pivotals.keys() :
            self.pivotals['.' if dir.GetName() == self.input_file.GetName() else dir.GetName()] = pivotals
        return

    def save_float_conversion(self, float_value) :
        """
        Convert a float into a string. Remove trailing .0's, which are not present for integer masses and would spoil the
        histogram search in the root input file.
        """
        value_str = str(float_value)
        if re.match('^\d*\.0$', value_str) :
            value_str = value_str[:value_str.rfind('.0')]
        return value_str
                            
    def load_hist(self, name) :
        """
        Load a histogram with name from self.input_file. Issue a warning in case the histogram is not available. In this case
        the class will most probably crash, but at least one knows which histogram was searched for and not found.
        """
        if name.startswith('./') :
            name=name.replace('./','')
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
        pivotals.sort(key=float)
        if len(pivotals)>0 :
            ## get index and value of closest element to mass in list of pivotals
            (idx, value) = min(enumerate(pivotals), key=lambda x: abs(float(x[1])-mass))
            if mass < float(pivotals[0]) :
                ## mass value beyond lower bound
                pmw = (value,value)
            elif mass > float(pivotals[-1]) : 
                ## mass value beyond upper bound
                pmw = (value,value)
            elif float(value) > mass :
                ## mass closer to lower bound
                pmw = (pivotals[max(idx-1,0)],value)
            elif float(value) == mass :
                ## mass sits directly on one of the bounds
                pmw = (value,value)
            else :
                ## mass closer to upper bound 
                pmw = (value,pivotals[min(idx+1,len(pivotals)-1)])
        return pmw

    def interpolation_scale(self, start, stop, x, debug=False) :
        """
        Determine the residual scale due to differences in acceptance and reconstruction efficiency when interpolating from
        embracing pivotal masses to mass. Start and stop are passed tuples of type (x-value,y-value). x is the value to
        interpolate to.
        """
        return 1+(stop[1]-start[1])/(stop[0]-start[0])/start[1]*(x-start[0])

    def single_template(self, dir, proc, mass, label, scale, MODE='MORPHED', debug=False) :
        """
        Return a single template histogram for a given dir, proc, mass and label. The histogram will be scaled by scale
        (corresponding to the cross section times BR of the corresponding Higgs boson). Scale will be modified by a linear
        interpolation scale taking into account differences in acceptance and reconstruction efficiency as a function of
        mass. Two modes exist to determine the template: MORPHED - will use horizontal template morphing (the morphing will
        always be applied from the pivotal, which is closest to mass to minimize uncertainties from the interplation);
        NEAREST_NEIGHBOUR - will use the closest mass point in the list of pivotals w/o any additional horizontal inter-
        polation. 
        """
        ## window of closest pivotal masses below/above mass. Window can be None, if no pivotals exist for a given dir. In
        ## this case return None       
        if self.ana_type=="Hplus" and mass=="" : 
            single_template = self.load_hist(dir+'/'+proc+label).Clone(proc+label+'_template'); single_template.Scale(scale)
            return single_template
        window = self.pivotal_mass_window(float(mass), self.pivotals[dir])
        if not window :
            return None
        if float(window[0]) == float(mass) and float(mass) == float(window[1]) :
            ## exact match with pivotal: clone exact pivotal
            single_template = self.load_hist(dir+'/'+proc+mass+label).Clone(proc+mass+label+'_template'); single_template.Scale(scale)
        elif float(window[0]) > float(mass) :
            ## mass out of bounds of pivotals (too small)
            single_template = self.load_hist(dir+'/'+proc+window[0]+label).Clone(proc+window[0]+label+'_template'); single_template.Scale(scale) 
        elif float(window[1]) < float(mass) :           
            ## mass out of bounds of pivotals (too large)
            single_template = self.load_hist(dir+'/'+proc+window[1]+label).Clone(proc+window[1]+label+'_template'); single_template.Scale(scale)
        else :
            ## mass somewhere between pivotals: masses is the tuple of the embracing pivotals, histos is the tuple of
            ## corresponding template histograms. The closest pivotal to mass is the first element in each of the tuples,
            ## the further away pivotal is second.
            if (float(mass) - float(window[0])) < (float(window[1]) - float(mass)) :
                ## lower bound pivotal closer to mass
                masses = (float(window[0]),float(window[1]))
                histos = (self.load_hist(dir+'/'+proc+window[0]+label),self.load_hist(dir+'/'+proc+window[1]+label))
            else :
                ## upper bound pivotal closer to mass
                masses = (float(window[1]),float(window[0]))
                histos = (self.load_hist(dir+'/'+proc+window[1]+label),self.load_hist(dir+'/'+proc+window[0]+label))
            scale*= self.interpolation_scale((float(masses[0]),histos[0].Integral()), (float(masses[1]),histos[1].Integral()), float(mass), debug)
            if MODE == 'MORPHED' :
                single_template = th1fmorph(proc+str(mass)+label+'_template', proc+mass+label, histos[0], histos[1], masses[0], masses[1], float(mass), scale*histos[0].Integral(), 0)
            if MODE == 'NEAREST_NEIGHBOUR' :
                single_template = histos[0].Clone(proc+str(mass)+label+'_template'); single_template.Scale(scale)
        return single_template

    def create_templates(self, reduced_model, file_label, hist_scale=1., MODE='MORPHED', debug=False) :
        """
        Determine a combined template, built up from single templates for Higgs bosons with different masses and cross
        sections. Reduced_model is expected to be a dictionary of type {(period,decay,proc) : MODEL_PARAMS}, where all
        information about available Higgses, their masses, BRs and cross sections are encoded in the class MODEL_PARAMS. In
        the key, period, indicates the run period in terms of center of mass energy, decay indicates the decay channel and
        proc indicates the process, to which MODEL_PARAMS applies. Proc should be present as a raw template for at least one
        mass in the root input file. The pivotal masses that do exist for each corresponding proc in each directory of the
        root input files are determined. The single templates are derived and summed. The directory structure relevant for
        each proc is set up in a root output file, to which these new combined templates are written to. The output file will
        be located in the same directory as the root input file. It will be distinguished by the postfix rootfile_label from
        the input file. It will only contain the combined signal templates for the procs given as keys in model. The
        templates can optionally be scaled by an additional parameter (like 1./float(model.tanb)).
        """
        output_file = ROOT.TFile(self.path+file_label, 'UPDATE')
        print "output file", self.path+file_label
        for (proc, params) in reduced_model :
            ## determine all available shapes (central value and uncerts) for given proc
            self.shape_labels = {}; self.fill_shape_labels(proc, self.input_file)
            for dir in self.shape_labels.keys() :
                ## skip directories that did not contain any templates for proc in the input file
                if len(self.shape_labels[dir]) == 0 :
                    continue
                ## build up directory structure in output file
                if not output_file.GetDirectory(dir) :
                    if not dir == '.' :
                        output_file.mkdir(dir)
                ## build up combined template histogram for each central value and each shape uncertainty for bin and proc
                for label in self.shape_labels[dir] :
                    combined_template = None
                    self.pivotals = {}; self.fill_pivotals(proc, label, self.input_file)
                    for higgs in params.list_of_higgses :
                        if self.ana_type=="Hplus" :
                            scale = float(params.brs[higgs])*hist_scale
                        else :
                            scale = float(params.xsecs[higgs])*float(params.brs[higgs])*hist_scale
                        histo = self.single_template(dir, proc, self.save_float_conversion(params.masses[higgs]), label, scale, MODE)
                        if combined_template :
                            if not 'fine_binning' in histo.GetName() :
                                combined_template.Add(histo)
                        else:
                            combined_template = histo
                    ## write combined template to output file
                    output_file.cd('' if dir == '.' else dir)
                    if combined_template :
                        if self.verbosity>0 :
                            print 'write histogram to file: ', dir+'/'+proc+self.save_float_conversion(self.parameter1)+self.hist_label+label
                        combined_template.Write(proc+self.save_float_conversion(self.parameter1)+self.hist_label+label, ROOT.TObject.kOverwrite)
        ## for Hplus the MC tt background has to be rescaled by params.ttscale (1-BR(t->Hp+b)*BR(Hp->tau+nu))^2
        if self.ana_type=="Hplus" :
            self.shape_labels = {}; self.fill_shape_labels("tt_EWK_faketau", self.input_file) #bkg name ugly hardcoded..
            params=reduced_model[0][1] #get ttscale (same for all signals)..
            for dir in self.shape_labels.keys() :
                ## skip directories that did not contain any templates for proc in the input file
                if len(self.shape_labels[dir]) == 0 :
                    continue
                ## build up directory structure in output file
                if not output_file.GetDirectory(dir) :
                    if not dir == '.' :
                        output_file.mkdir(dir)
                ## build up combined template histogram for each central value and each shape uncertainty for bin and proc
                for label in self.shape_labels[dir] :
                    combined_template = None
                    scale = float(params.ttscale)
                    histo = self.single_template(dir, "tt_EWK_faketau", "", label, scale, MODE) #bkg name ugly hardcoded..
                    if combined_template :
                        if not 'fine_binning' in histo.GetName() :
                            combined_template.Add(histo)
                    else:
                        combined_template = histo
                    ## write combined template to output file
                    output_file.cd('' if dir == '.' else dir)
                    if combined_template :
                        if self.verbosity>0 :
                            print 'write histogram to file: ', dir+'/'+"tt_EWK_faketau"+self.hist_label+label
                        combined_template.Write("tt_EWK_faketau"+self.hist_label+label, ROOT.TObject.kOverwrite)
        output_file.Close()
        return 

