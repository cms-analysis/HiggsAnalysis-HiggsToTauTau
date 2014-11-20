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
    counting experiments. For counting experiments no differences in acceptance due to differing masses of the contributing
    Higgses are taken into account, as these can not be a priori known from a single datacard. 
    """
    def __init__(self, parser_options, model_label, parameter1, update_file=False, ana_type='') :
        ## postfix label for the root input file where to find the rates modified according to the given model
        self.model_label = model_label
        ## write the the new template histogram with new histogram name into the same file (i.e. update the existing file)
        ## or write the new template histogram with the usual process name in a new root file?
        self.update_file = update_file
        ## options for the datacard parser
        self.options = parser_options
        ## memory of the root input files that have been processed by ModelTemplates during the lifetime of the instantiated
        ## class object
        self.already_processed_template_files = []
        ## analyses type (for Htt its empty, only for Hplus its 'Hplus'
        self.ana_type=ana_type
        ## mass of A or in the case of the lowmH scenario its mu
        self.parameter1 = parameter1
        ## initialize base class
        super(ModelDatacard, self).__init__()

    def columns(self, path, card) :
        """
        Return a list with elements of form bin+'_'+proc to allow to determine the proper position of rates or uncertainty
        entries in the datacard column. Get proper oder of entries in lists of bins an procs: pick proper line for bin and
        proc from the datacard. The proper bin line is the line with proper length. The proper proc line is the line that
        has matches with the proc names determined from the datacard parsing. Both lines should have the same number of
        elements. These elements are concatenated and added to a list index_order that will later von be used to determine
        the column idx for given bin and proc, which are determined from the datacard.
        """
        bin_list = []; proc_list= []
        ## update datacard
        file = open(path, 'r')
        card = parseCard(file, self.options)
        file.close()
        ## modify datacard
        old_file = open(path, 'r')        
        for line in old_file :
            words = line.lstrip().split()
            if words[0].lower() == 'bin':
                if len(words[1:]) > len(card.list_of_bins()) :
                    bin_list = words[1:]
            if words[0].lower() == 'process' :
                if len(list(set(words[1:]).intersection(card.list_of_procs()))) > 0 :
                    proc_list = words[1:]
        old_file.close()
        index_order = []
        if not len(bin_list) == len(proc_list) :
            print "Warning: line bin and line process do not correspond to the same number of elements."
        for idx in range(len(proc_list)) :
            index_order.append(bin_list[idx]+'_'+proc_list[idx])
        return index_order

    def adapt_rate_lines(self, path, procs, mass) :
        """
        Adapt the rate for a given set of procs in the rates line of a given datacard located at path. The new rate is
        determined from the histogram integral of the corresponding shape template. The difficulty is to have the replacement
        at the proper position in the datcard. This is achieved by mapping the column index to a combination of bin and proc.
        The parameter card corresponds to the parsed datacard using the method parseCard of the HCG datacard parser.
        """
        ## update datacard
        file = open(path, 'r')
        card = parseCard(file, self.options)
        file.close()
        ## list of columns in datacards ordered by bin+'_'+proc
        index_order = self.columns(path, card)
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
                        if not '_SM125' in proc :
                            if card.path_to_file(bin, proc) == '' :
                                ## this channel is counting only; NOTE: this does not allow to take acceptance differences due
                                ## to the different masses of the different higgses into account. THIS IS NOT WORKING CURRENTLY
                                print "counting only is currently NOT WORKING"; continue
                                new_rate=0
                                for higgs in self.model[proc].list_of_higgses :
                                    new_rate+=float(self.model[proc].xsec[higgs])*float(self.model[proc].brs[higgs])
                                new_rates[index_order.index(bin+'_'+proc)] = str(new_rate)
                            else :
                                ## get signal rate from file
                                hist_file = ROOT.TFile(path[:path.rfind('/')+1]+card.path_to_file(bin, proc), 'READ')
                                hist = hist_file.Get(card.path_to_shape(bin, proc).replace('$MASS', mass))
                                new_rates[index_order.index(bin+'_'+proc)] = str(hist.Integral())
                    if self.ana_type=="Hplus" : ##felix for tt scale background, but only once!
                        for bkg in card.list_of_backgrounds() :
                            if "tt_" in bkg and bkg!="EWKnontt_faketau" :
                                if card.path_to_file(bin, bkg) == '' :
                                    ## this channel is counting only; NOTE: this does not allow to take acceptance differences due
                                    ## to the different masses of the different higgses into account. THIS IS NOT WORKING CURRENTLY
                                    print "counting only is NOT SUPPORTED"
                                else :
                                    ## get tt rate from file
                                    hist_file = ROOT.TFile(path[:path.rfind('/')+1]+card.path_to_file(bin, bkg), 'READ')
                                    hist = hist_file.Get(card.path_to_shape(bin, bkg))
                                    new_rates[index_order.index(bin+'_'+bkg)] = str(hist.Integral())
                new_line = 'rate\t'+'\t'.join(new_rates)+'\n'
            new_file.write(new_line)
        old_file.close()
        new_file.close()
        os.system("mv {TMP} {FINAL}".format(TMP=path+'_tmp', FINAL=path))

    def wildcard_uncerts(self, path) :
        """
        Parse a datacards located at path. Search for the kmax line and replace potential explicit numbers of uncerts by a
        wild card.
        """
        old_file = open(path, 'r')
        new_file = open(path+'_tmp', 'w')
        for line in old_file :
            words = line.lstrip().split()
            if words[0] == 'kmax' :
                words[1] = '*'
                line = ' '.join(words)+'\n'
            new_file.write(line)
        old_file.close()
        new_file.close()
        os.system("mv {TMP} {FINAL}".format(TMP=path+'_tmp', FINAL=path))
        
    def add_uncert_lines(self, path, model) :
        """
        Add a set of uncertainties lines to the datacards located at path for the model uncertainties given in model, as
        defined in the class MODEL in tanb_grid_new.py.
        """
        self.wildcard_uncerts(path)
        ## update datacard
        file = open(path, 'r')
        card = parseCard(file, self.options)
        file.close()
        ## list of columns ordered by bin+'_'+proc
        index_order = self.columns(path, card)
        ## create uncertainty lines corresponding to all components that are present in model. For this purpose iterate over
        ## all items in uncerts. Note that for each key in uncerts there must exist a corresponding key in central, which is
        ## called here as well. This is fullfilled in the class MODEL by construction.
        uncert_appendix = {}
        for type in model.uncerts.keys() :
            for (key,params) in model.uncerts[type].iteritems() :
                ## expected key elements are (period,decay,proc)
                period = key[0]; decay = key[1]; proc = key[2]
                label = proc+'_'+decay+'_'+type+'_'+period
                ## central value and up/down shifts for uncertainties. NOTE: the effectives of params[0/1] correspond to abs.
                ## shifts. For mu these shifts are added linearly for each higgs (MOMENT=1). For pdf they are added in quad-
                ## rature (MOMENT=2). In the datacards the absolute shifts are divided by the central value (added linearly)
                ## to transform them into relative shifts. The difference in adding the uncertainties leads to a slightly
                ## different treatment, in the transformation of abs->rel difference, esp for the -shift.
                value = model.central[key].effective()
                lower = params[0].effective(1 if type == 'mu' else 2)
                upper = params[1].effective(1 if type == 'mu' else 2)
                uncerts = []
                for bin in card.list_of_bins() :
                    if not (decay in bin or '*' in bin) :
                        continue
                    if not (period in bin or '*' in bin) :
                        continue
                    if self.ana_type=="Hplus" :
                        label = 'signal_'+decay+'_'+type+'_'+period
                        if len(uncerts)==0 :
                            for idx in range(len(index_order)) :
                                uncerts.append('-')
                            for idx in range(len(index_order)) :
                                for proc_in_card in card.list_of_signals() :
                                    if idx == index_order.index(bin+'_'+proc_in_card) :
                                        uncerts[idx]=" \t\t %.3f " % (1.21 if params[0].masses['Hp'] < 165 else 1.32)
                    else :
                        for proc_in_card in card.list_of_signals() :
                            if proc_in_card == proc :
                                ## first fill whole list with placeholders then replace with uncertainty numbers at right places
                                if len(uncerts)==0 :
                                    for idx in range(len(index_order)) :
                                        uncerts.append('-')
                                for idx in range(len(index_order)) :
                                    if idx == index_order.index(bin+'_'+proc) :
                                        if type == 'mu' :
                                            if  value>0 and lower/value!=1 :
                                                uncerts[idx]=" \t\t %.3f/%.3f " % (1./(1.-lower/value), 1.+upper/value)
                                            else :
                                                uncerts[idx]=" \t\t 0.1 "
                                        if type == 'pdf' :
                                            if value>0 :
                                                uncerts[idx]=" \t\t %.3f/%.3f " % (1./(1.+lower/value), 1.+upper/value)
                                            else :
                                                uncerts[idx]=" \t\t 0.1 "
                ## in case label is not yet in dict, add uncerts as they are. Otherwise update '-' entries in existing list
                ## of uncerts
                if self.ana_type=="Hplus" :
                    uncert_appendix[label] = uncerts
                    break
                if not label in uncert_appendix :
                    uncert_appendix[label] = uncerts
                else :
                    for idx in range(len(uncert_appendix[label])) :
                        if uncert_appendix[idx] == '-' :
                            uncert_appendix[idx] = uncer[idx]
        ## replace lines that might already exist with updated values. Otherwise just append the new uncertainy lines
        for label,uncerts in uncert_appendix.iteritems() :
            found_label = False
            old_file = open(path, 'r')
            new_file = open(path+'_tmp', 'w')
            for line in old_file :
                words = line.lstrip().split()
                if words[0] == label :
                    found_label = True
                    line = label+'\t lnN \t'+'\t'.join(uncerts)+'\n'
                ## handle mhplus dependent lnN errors in Hplus (using nearest neightbour)
                if self.ana_type=="Hplus" : 
                    if len(line.lstrip().split()) > 2 :
                        if words[1]=="lnN" :
                            nuisance_file = open("../common/HplusNuisanceFile.dat", 'r')
                            delta=100
                            for n_line in nuisance_file:
                                n_words = n_line.lstrip().split()
                                if words[0]==n_words[1] and abs(float(n_words[0])-float(params[0].masses['Hp'])) < delta :
                                    delta = abs(float(n_words[0])-float(params[0].masses['Hp']))
                                    line = n_line.lstrip(n_words[0]+" ")
                            nuisance_file.close()
                new_file.write(line)
            old_file.close()
            new_file.close()
            os.system("mv {TMP} {FINAL}".format(TMP=path+'_tmp', FINAL=path))
            if not found_label :
                ## append new uncertainty line to the end of the file in case it has not yet been found
                file = open(path, 'a')
                file.write(label+'\t lnN \t'+'\t'.join(uncerts)+'\n')
                file.close()

    def make_model_datacard(self, path, model, morph) :
        """
        For a datacard located at path, determine the root input files that correspond to bins and procs indicated by the
        model, as defined in the class MODEL in tanb_grid_new.py. The dict morph indicates the morphing mode, that should be
        used for each corresponding bin. The function creates new signal templates from the raw templates located in the
        original root input file using the class ModelTemplate. Depending on the configuration of the class the new templates
        will be located in a new root input file at the same location as the old one but with label self.model_label or in
        the same root input file, while the histgorams will have modified names (option self.update_file==True). The function
        does adapt the shapes and the rate lines in the datacards accordingly after the new templates have been created. The
        function parameter card corresponds to the parsed datacard using the method parseCard of the HCG datacard parser.
        """
        ## create the new templates with modified signal model. For this purpose the dict of central values is iterated first.
        ## In case of self.update_file hadd the newly created model file. Make sure that no file that has been processed
        ## during the lifetime of any instance of this class will be processed second time. This is for performance reasons,
        ## as the old files would just be replaced, by the same file.
        dir = path[:path.rfind('/')+1]
        ## update datacard
        file = open(path, 'r')
        card = parseCard(file, self.options)
        file.close()
        ## determine schedule for the files and procs that need to be processed. Schedule is of type {'file_name':['proc']}
        schedule = {}
        morph_per_file = {}
        for (key,params) in model.central.iteritems() :
            ## expected key elements are (period,decay,proc)
            period = key[0]; decay = key[1]; proc = key[2]
            for bin in card.list_of_bins() :
                if not decay in bin :
                    continue
                if not period in bin :
                    continue
                for proc_in_card in card.list_of_signals() :
                    if proc_in_card == proc :
                        shape_file = card.path_to_file(bin, proc)
                        if not shape_file in schedule.keys() :
                            ## define schedule
                            schedule[shape_file] = [(proc,params)]
                            ## define morphing mode (per file)
                            for subchn in morph.keys() :
                                if subchn in bin :
                                    if not shape_file in morph_per_file.keys() :
                                        morph_per_file[shape_file] = morph[subchn]
                        else :
                            if not (proc,params) in schedule[shape_file] :
                                schedule[shape_file].append((proc,params))
        ## process each file exactly once. Treat all processes in one iteration
        for (shape_file,reduced_model) in schedule.iteritems() :
            print 'creating template(s) :', dir+shape_file, '(morphing mode is', morph_per_file[shape_file]+')'
            if self.update_file :
                template = ModelTemplate(dir+shape_file, self.parameter1, self.ana_type, self.model_label)
                template.create_templates(reduced_model, self.model_label, 1./float(model.tanb), morph_per_file[shape_file])
                tmp = '/tmp/'+''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
                os.system("hadd {TMP} {SOURCE} {SOURCE}{MODEL}".format(TMP=tmp, SOURCE=dir+shape_file, MODEL=self.model_label))
                os.system("mv {TMP} {SOURCE}".format(TMP=tmp, SOURCE=dir+shape_file))
                os.system("rm {SOURCE}{MODEL}".format(SOURCE=dir+shape_file,MODEL=self.model_label))
            else :
                template = ModelTemplate(dir+shape_file, self.parameter1, self.ana_type)
                template.create_templates(reduced_model, self.model_label, 1./float(model.tanb), morph_per_file[shape_file])
        ## adapt datacards to pick up proper signal rates
        print 'adapting datacard(s) :', path
        if self.ana_type=="Hplus" :            
            ## filename gets label self.model_label, histogram name remains as is
            self.adapt_shapes_lines(path, card, 'tt_EWK_faketau', '', self.model_label) #background ugly hardcoded ...
        for key in model.central.keys() :
            ## expected key elements are (period,decay,proc)
            period = key[0]; decay = key[1]; proc = key[2]
            ## update datacard
            file = open(path, 'r')
            card = parseCard(file, self.options)
            file.close()
            if self.update_file :
                ## histogram name gets label self.model_label, filename remains as is
                self.adapt_shapes_lines(path, card, proc, self.model_label, '')
            else :
                ## filename gets label self.model_label, histogram name remains as is
                self.adapt_shapes_lines(path, card, proc, '', self.model_label)
        self.adapt_rate_lines(path, card.list_of_signals(), model.save_float_conversion(self.parameter1))
        self.add_uncert_lines(path, model)
