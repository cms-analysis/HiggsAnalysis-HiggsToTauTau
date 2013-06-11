import os
import ROOT

from HiggsAnalysis.CombinedLimit.DatacardParser import *
from HiggsAnalysis.HiggsToTauTau.MODEL_PARAMS import MODEL_PARAMS
from HiggsAnalysis.HiggsToTauTau.ModelTemplate import ModelTemplate
from HiggsAnalysis.HiggsToTauTau.DatacardAdaptor import DatacardAdaptor


class ModelDatacard(DatacardAdaptor) :
    """
    Description:

    This class is derived from the base class DatacardAdaptor. The base class is extended by the possibility to modify the
    rates lines for signal processes for shape analyses with binned likelihoods.NB:  At the moment counting experiments are
    not yet supported, though they can in principle. This functionality will be added later. 
    """
    def __init__(self, parser_options, mass, model, model_label) :
        ## postfix label for the root input file where to find the rates modified according to the given model
        self.model_label = model_label
        ## model that should be applied to the raw input datacards: model is expected to be of type {proc, MODEL_PARAMS}
        self.model = model
        ## mass for which to evaluate the model
        self.mass = mass
        ## initialize base class
        super(ModelDatacard, self).__init__(parser_options)

    def adapt_rate_lines(self, path, procs) :
        """
        Adapt the rate for a given proc in the rates line of a given datacard located at path. The new rate is determined
        from the histogram integral of the corresponding shape template. The difficultie is to have the replacement at the
        proer position in the datcard. This is achieved by mapping the column index to a combination of bin and proc.
        """
        ## parse datacards
        old_file = open(path, 'r')
        card = parseCard(old_file, self.options)
        old_file.close()
        ## get proper oder of entries in lists of bins an procs: pick proper line for bin and proc from the datacard. The
        ## proper bin line is the line with proper length. The proper proc line is the line that has matches with the proc
        ## names determined from the datacards parsing. Both lines should have the same number of elements. These elements
        ## are concatenated and added to a list index_order that will later von be used to determine the column idx for
        ## given bin and proc.
        bin_list = []; proc_list= []
        old_file = open(path, 'r')        
        for line in old_file :
            words = line.lstrip().split()
            if words[0].lower() == 'bin' :
                if len(words[1:]) == len(card.list_of_bins())*len(card.list_of_procs()) :
                    bin_list = words[1:]
            if words[0].lower() == 'process' :
                if len(list(set(words[1:]).intersection(card.list_of_procs()))) > 0 :
                    proc_list = words[1:]
        old_file.close()
        index_order = []
        if not len(bin_list) == len(proc_list) :
            print "WARNING: line bin and line process do notcorrespond to the same number of elements."
        for idx in range(len(proc_list)) :
            index_order.append(bin_list[idx]+'_'+proc_list[idx])
        ## adapt the datacard. A list new_rates is determined from the old rates in the datacard. The signal rate for proc is
        ## determined from the shape template in the shape file given in the datacard. The list idx corresponding to bin and
        ## proc is determined and replaced by the new value. The list new_rates is combined to a string and writen to the new
        ## file.
        old_file = open(path, 'r')        
        new_file = open(path+'_tmp', 'w')
        for line in old_file :
            new_line = line
            words = line.lstrip().split()
            if words[0].lower() == 'rate' :
                new_rates = words[1:]
                for bin in card.list_of_bins() :
                    for proc in procs :
                        ## get signal rate from file
                        hist_file = ROOT.TFile(path[:path.rfind('/')+1]+card.path_to_file(bin, proc), 'READ')
                        hist = hist_file.Get(card.path_to_shape(bin, proc).replace('$MASS', self.mass))
                        new_rates[index_order.index(bin+'_'+proc)] = str(hist.Integral())
                new_line = 'rate\t'+'\t'.join(new_rates)+'\n'
            new_file.write(new_line)
        old_file.close()
        new_file.close()
        os.system("mv {TMP} {FINAL}".format(TMP=path+'_tmp', FINAL=path))

    def make_model_datacards(self, dir) :
        """
        For all datacards in dir, determine the root input files that correspond to the procs indicated by self.model.
        Create new signal templates from the raw templates located in the original root input file using the class
        ModelTemplate. The new templates will be located in a new root input file at the same location as the old one with
        label self.model_label. Adapt the shapes and the rate lines in the datacards accordingly.
        """
        self.cleanup(dir, self.model_label)
        ## determine root input files from datacards in dir
        shape_files = []
        for name in os.listdir(dir) :
            if not name.endswith('.txt') :
                continue
            file = open(dir+'/'+name)
            card = parseCard(file, self.options)
            file.close()
            for bin in card.list_of_bins() :
                for proc in self.model.keys() :
                    shape_file = card.path_to_file(bin, proc)
                    if not shape_file in shape_files :
                        shape_files.append(shape_file)
        ## create the new templates with modified signal model
        for shape_file in shape_files :
            print 'creating templates for', dir+'/'+shape_file  
            template = ModelTemplate(dir+'/'+shape_file)
            template.create_templates(self.model, self.model_label)
        ## adapt datacards to pick up proper signal rates
        for name in os.listdir(dir) :
            if not name.endswith('.txt') :
                continue
            print 'adapt inputs for', dir+'/'+name
            for proc in self.model.keys() :
                self.adapt_shapes_lines(dir+'/'+name, proc, self.model_label)
            self.adapt_rate_lines(dir+'/'+name, self.model.keys())

#def test(path=args[0]) :
#    ## prepare dummy model
#    param = MODEL_PARAMS()
#    model = {'ggH': param}
#    ## adapt datacards
#    adaptor = ModelDatacard(options, '120', model, '_new_model')
#    adaptor.make_model_datacards(full_path)
    
#test()
