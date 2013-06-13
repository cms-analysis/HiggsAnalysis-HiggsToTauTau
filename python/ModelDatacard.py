import os
import ROOT
import string
import random

from HiggsAnalysis.CombinedLimit.DatacardParser import *
from HiggsAnalysis.HiggsToTauTau.MODEL_PARAMS import MODEL_PARAMS
from HiggsAnalysis.HiggsToTauTau.ModelTemplate import ModelTemplate
from HiggsAnalysis.HiggsToTauTau.DatacardAdaptor import DatacardAdaptor


class ModelDatacard(DatacardAdaptor) :
    """
    Description:

    This class is derived from the base class DatacardAdaptor. The base class is extended by the possibility to modify the
    rates lines for signal processes for shape analyses with binned likelihoods. This class operates on shape analysis or
    counting experiments
    """
    def __init__(self, parser_options, mass, model_label, update_file=False) :
        ## postfix label for the root input file where to find the rates modified according to the given model
        self.model_label = model_label
        ## mass for which to evaluate the model
        self.mass = mass
        ## write the the new template histogram with new histogram name into the same file (i.e. update the existing file)
        ## or write the new template histogram with the usual process name in a new root file?
        self.update_file = update_file
        ## memory of the root input files that have been processed by ModelTemplates during the lifetime of the instantiated
        ## class object
        self.processed_template_files = []
        ## initialize base class
        super(ModelDatacard, self).__init__(parser_options)

    def adapt_rate_lines(self, path, procs) :
        """
        Adapt the rate for a given set of procs in the rates line of a given datacard located at path. The new rate is
        determined from the histogram integral of the corresponding shape template. The difficulty is to have the replacement
        at the proper position in the datcard. This is achieved by mapping the column index to a combination of bin and proc.
        """
        ## parse datacards
        old_file = open(path, 'r')
        card = parseCard(old_file, self.options)
        old_file.close()
        ## get proper oder of entries in lists of bins an procs: pick proper line for bin and proc from the datacard. The
        ## proper bin line is the line with proper length. The proper proc line is the line that has matches with the proc
        ## names determined from the datacards parsing. Both lines should have the same number of elements. These elements
        ## are concatenated and added to a list index_order that will later von be used to determine the column idx for
        ## given bin and proc, which are determined from the datacard.
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
            print "WARNING: line bin and line process do not correspond to the same number of elements."
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
                        if card.path_to_file(bin, proc) == '' :
                            ## this channel is counting only; NOTE: this does not allow to take acceptance differences due
                            ## to the different masses of the different higgses into account.
                            new_rate=0
                            for higgs in self.model[proc].list_of_higgses :
                                new_rate+=float(self.model[proc].xsec[higgs])*float(self.model[proc].brs[higgs])
                            new_rates[index_order.index(bin+'_'+proc)] = str(new_rate)
                        else :
                            ## get signal rate from file
                            hist_file = ROOT.TFile(path[:path.rfind('/')+1]+card.path_to_file(bin, proc), 'READ')
                            hist = hist_file.Get(card.path_to_shape(bin, proc).replace('$MASS', self.mass))
                            new_rates[index_order.index(bin+'_'+proc)] = str(hist.Integral())
                new_line = 'rate\t'+'\t'.join(new_rates)+'\n'
            new_file.write(new_line)
        old_file.close()
        new_file.close()
        os.system("mv {TMP} {FINAL}".format(TMP=path+'_tmp', FINAL=path))

    def add_uncert_line(self, card, path, proc, label, model, uncerts, MOMENT) :
        """
        Add an uncertainties line for the model uncertainties given by uncerts for a given proc in a datacards located at
        path. Uncerts is of type {'type':(MODEL_PARAMS,MODEL_PARAMS)}, where the first element in the tuple corresponds to
        the down shift and the second element in the tuple corresponds to the up shift. MOMENT=1 means that uncerts for all
        higgses are added linearly, MOMENT=2 means that the uncerts for all higgses are added in quadrature. By convention
        for 'pdf' like uncertainties uncerts are added in quadrature, for 'mu' like uncerts they are added linearly. I'm not
        sure whether this makes sense?!? Please check.
        """
        value = model[proc].effective()
        lower = uncerts[proc][0].effective(MOMENT)
        upper = uncerts[proc][1].effective(MOMENT)
        ## pick process line from file to be able to determine the index position corresponding to proc
        proc_list = []
        file = open(path, 'r')        
        for line in file :
            words = line.lstrip().split()
            if words[0].lower() == 'process' :
                if len(list(set(words[1:]).intersection(card.list_of_procs()))) > 0 :
                    proc_list = words[1:]
        file.close()
        ## create uncertainty line
        uncerts = []
        for idx in range(len(proc_list)) :
            if idx == proc_list.index(proc) :
                if  value>0 and lower/value!=1 :
                    uncerts.append(" \t\t %.3f/%.3f " % (1./(1.-lower/value), 1.+upper/value))
                else :
                    uncerts.append(" \t\t 0.1 ")
            else :
                uncerts.append('-')
        ## append new uncertainty line to the end of the file
        file = open(path, 'a')
        file.write(label+'\t lnN \t'+'\t'.join(uncerts)+'\n')
        file.close()

    def make_model_datacard(self, path, model) :
        """
        For a datacard located at path, determine the root input files that correspond to the procs indicated by model.
        Create new signal templates from the raw templates located in the original root input file using the class
        ModelTemplate. Depending on the configuration of the class the new templates will be located in a new root input
        file at the same location as the old one but with label self.model_label or in the same root input file, while
        the histgorams will have modified names (option self.update_file==True). Adapt the shapes and the rate lines in
        the datacards accordingly.
        """
        ## determine root input files from datacard located at path
        shape_files = []
        file = open(path)
        card = parseCard(file, self.options)
        file.close()
        for bin in card.list_of_bins() :
            for proc in model.keys() :
                shape_file = card.path_to_file(bin, proc)
                if not shape_file in shape_files :
                    shape_files.append(shape_file)
        ## create the new templates with modified signal model. In case of self.update_file hadd the newly created model file.
        ## Make sure that no file that has been processed during the lifetime of any instance of this class will be processed
        ## another time. This is for performance reasons, as the old files would just be replaced, by the same file.
        for shape_file in shape_files :
            dir = path[:path.rfind('/')+1]
            if not shape_file in self.processed_template_files :
                print 'creating templates for', dir+shape_file  
                if self.update_file :
                    template = ModelTemplate(dir+shape_file, self.model_label)
                    template.create_templates(model, self.model_label)
                    tmp = '/tmp/'+''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
                    os.system("hadd {TMP} {SOURCE} {SOURCE}{MODEL}".format(TMP=tmp, SOURCE=dir+shape_file, MODEL=self.model_label))
                    os.system("mv {TMP} {SOURCE}".format(TMP=tmp, SOURCE=dir+shape_file))
                    os.system("rm {SOURCE}{MODEL}".format(SOURCE=dir+shape_file,MODEL=self.model_label))
                else :
                    template = ModelTemplate(dir+shape_file)
                    template.create_templates(model, self.model_label)
                ## keep in mind that this file has been processed already
                self.processed_template_files.append(shape_file)
        ## adapt datacards to pick up proper signal rates
        print 'adapt inputs for', path
        for proc in model.keys() :
            if self.update_file :
                ## histogram name gets label self.model_label, filename remains as is
                self.adapt_shapes_lines(path, proc, self.model_label, '')
            else :
                ## filename gets label self.model_label, histogram name remains as is
                self.adapt_shapes_lines(path, proc, '', self.model_label)
        self.adapt_rate_lines(path, model.keys())
