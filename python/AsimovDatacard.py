import os
import ROOT
import random
import glob

from HiggsAnalysis.CombinedLimit.DatacardParser import *
from HiggsAnalysis.HiggsToTauTau.DatacardAdaptor import DatacardAdaptor

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch()

class AsimovDatacard(DatacardAdaptor) :
    """
    Description:

    This class should take all datacards in a given directory and replace all data_obs histograms / entries by the asimov
    dataset. There are two ways to introduce the new data_obs: either it is saved in the the same root input file with name
    data_obs_asimov, or it is saved with the same name in a different root input file, which is indicated by an additional
    postfix _asimov. All datacardss in the given directory are modified accordingly. The class works for shape analyses and
    counting experiments. Depending on the configuration all signal processes as given by the datacards can be added to the
    asimov dataset, multiplied by a scale factor, which is commonly applied to all signal processes. If configured such, a
    parameter can be given to indicate the mass of the signal that should be added to the background processes. In addition
    extra templates can be added into the data_obs, which are present in the root input file, but not part of the processes
    indicated in the datacard. If a random seed>=0 is given the asimov dataset is randomized according to a Poisson
    distribution.
    """
    def __init__(self, parser_options, update_file=False, seed='-1', add_signal=True, mass='125', signal_scale='1.', extra_templates='', blacklist=[]) :
        ## random seed in case the asimov dataset should be randomized (-1 will indicate that no randomization should be applied) 
        self.seed = seed
        ## should be true if signal should be considered for the asimov dataset
        self.add_signal = add_signal
        ## in case signal should be considered for the asimov datseet mass for the signal template
        self.mass = mass
        ## in case signal should be considered for the asimov dataset scale factor that should be used for the signal template
        self.signal_scale = signal_scale
        ## in case any other templates should be added to the asimov dataset (e.g. SM signal to MSSM datacards)
        self.extra_templates = extra_templates
        ## in case any signal/background template should be ignored when creating the asimov dataset (e.g. if a central
        ## template should be replaced by a shifted template, or if only ggH should be added into the asimov dataset and
        ## other signal processes should be ignored)
        self.blacklist = blacklist
        ## write the asomiv dataset with new histogram name into the same file (i.e. update the existing file) or write the
        ## asimov dataset with the same histogram name in a new root file?
        self.update_file = update_file
        ## options for the datacard parser
        self.options = parser_options
        ## initialize base class
        super(AsimovDatacard, self).__init__()
    
    def adapt_observation_lines(self, path) :
        """
        Find the lines starting with keyword 'observations' in the datacard located at path. For each bin in the datacards
        determine data_obs from the histograms given for process data_obs in that bin. If there is no path to a shape file
        for data_obs, the bin corresponds to a counting experiment. In this case add up the rates from all background
        processes and from all signal processes if configured such. Randomization can be applied ain analogy to the case
        with shapes. 
        """
        observations = []
        old_file = open(path, 'r')
        card = parseCard(old_file, self.options)
        old_file.close()
        ## adapt the datacard
        old_file = open(path, 'r')
        new_file = open(path+'_tmp', 'w')
        for line in old_file :
            new_line = line
            words = line.lstrip().split()
            if words[0].lower() == 'observation' :
                for bin in card.list_of_bins() :
                    value = 0
                    if card.path_to_file(bin, 'data_obs') == '' :
                        ## this channel is counting only
                        for proc in card.list_of_backgrounds() :
                            value+= float(card.rate(bin, proc))
                        if self.add_signal :
                            for proc in card.list_of_signals() :
                                value+= float(self.signal_scale)*float(card.rate(bin, proc))                            
                        if not self.seed == '-1' :
                            rnd = ROOT.TRandom3(int(self.seed))
                            rnd.SetSeed()
                            value = rnd.Poisson(value)
                    else :
                        hist_file = ROOT.TFile(path[:path.rfind('/')+1]+card.path_to_file(bin, 'data_obs'), 'READ')
                        hist = hist_file.Get(card.path_to_shape(bin, 'data_obs'))
                        value = hist.Integral()
                        hist_file.Close()
                    if value:
                        observations.append('%.d' % round(value))
                    else:
                        observations.append('0')
                new_line = 'observation '+' '.join(observations)+'\n'
            new_file.write(new_line)
        old_file.close()
        new_file.close()
        os.system("mv {TMP} {FINAL}".format(TMP=path+'_tmp', FINAL=path))

    def asimov_shapes(self, dir) :
        """
        Parse all datacards in dir, collect signal and background processes and the paths to the input files and create
        the asimov dataset including background processes (and signal processes if configured such). Write new rootfiles 
        which contain only the new data_obs histograms. This is done for each bin and each process independently. In a
        final step the individual rootfiles containing the asimov datasets are hadd'ed into one additional file for each
        inputfile with the extension _asimov. If the option self.update_file is chosen the new data_obs histogram(s) will
        be written as new histograms to the same file with an additional label _asimov.
        """
        ## counter for files with blinded data_obs 
        index = 0
        ## processed files
        processed_files = []
        ## processed files and bins
        processed_files_bins = []
        ## parse all datacards, determine signal and background
        ## create a list of datacards and sort them
        dirs = glob.glob(dir+"/*.txt")
        dirs.sort()
        ## create a list of random numbers with one number per category
        random.seed(self.seed)
        catseeds = [ random.randint(1, 999999) for i in dirs]
        ind = 0
        for name in dirs :
            file = open(name, 'r')
            card = parseCard(file, self.options)
            for bin in card.list_of_bins() :
                for proc in card.list_of_procs() :
                    path = card.path_to_file(bin, proc)
                    ## determine background list, add extra contributions to this list if configured such,
                    ## remove blacklisted background templates if configured such
                    bkg_procs_reduced = card.list_of_procs('b')
                    for ignore in self.blacklist :
                        if ignore in bkg_procs_reduced :
                            bkg_procs_reduced.remove(ignore)
                    bkg_list = self.list2string(card, bin, bkg_procs_reduced)
                    bkg_list = bkg_list+','+self.extra_templates.replace(' ','') if self.extra_templates!='' else bkg_list
                    ## determine signal list, remove blacklisted signal templates if configured such
                    sig_procs_reduced = card.list_of_procs('s')
                    for ignore in self.blacklist :
                        if ignore in sig_procs_reduced :
                            sig_procs_reduced.remove(ignore)
                    sig_list = self.list2string(card, bin, sig_procs_reduced) if self.add_signal else ''
                    if not path == '' :
                        if not (path, bin) in processed_files_bins :
                            processed_files_bins.append((path, bin))
                            if not path in processed_files :
                                processed_files.append(path)
                            os.system("root -l -b -q {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/blindData.C+\\(\\\"{INPUT}\\\",\\\"{BKG}\\\",\\\"{SIG}\\\",\\\"{DIR}\\\",true,{SEED},{SCALE},\\\"{IDX}\\\",\\\"{DATA_OBS}\\\",0\\)".format(
                                CMSSW_BASE = os.environ['CMSSW_BASE'],
                                INPUT = dir+'/'+path,
                                BKG = bkg_list,
                                SIG = sig_list.replace('$MASS',self.mass),
                                DIR = bin,
                                SEED = catseeds[ind] if not int(self.seed) == -1 else -1,
                                SCALE = self.signal_scale,
                                IDX = '' if self.update_file else index,
                                DATA_OBS = self.list2string(card, bin, ['data_obs']) 
                                ))
                            index += 1
            ind += 1
            file.close()
        ## combine all individual files into a single file for each used input rootfile. This is only necessary if the
        ## data_obs histograms have been written in separate files.
        if not self.update_file :
            for file in processed_files :
                os.system('hadd {TARGET} {SOURCE}'.format(
                    TARGET=dir+'/'+file.replace('.root', '.root_asimov'),
                    SOURCE=dir+'/'+file.replace('.root', '_*.root')
                    ))
                os.system('rm {SOURCE}'.format(
                    SOURCE=dir+'/'+file.replace('.root', '_*.root')
                    ))

    def make_asimov_datacards(self, dir, adapt_datacards_only=False) :
        """
        For all datacards given in directory dir determine the paths to all root input files. Run the root macro
        blindData.C for all bins/channels and processes for which the datacards do require shapes. According to
        configuration add all background processes (and signal processes, if configured such) to the Asimov dataset.
        The data_obs histograms to contain the asimov datasets are written to separate files next to the original
        input files, indicatd by the postfix _asimov. All datacards are then adapted accordingly. If configured such
        the data_obs histograms / entries are randomized according to a Poisson distribution.
        """
        if not adapt_datacards_only :
            print "...creating asimov datasets."
            self.asimov_shapes(dir)
        print "...redirecting input files in datacards."
        for name in os.listdir(dir) :
            if not name.endswith('.txt') :
                continue
            path = dir+'/'+name
            ## parse datacard
            old_file = open(path, 'r')
            card = parseCard(old_file, self.options)
            old_file.close()
            if self.update_file :
                ## histogram name gets label _asimov, filename remains as is
                self.adapt_shapes_lines(path, card, 'data_obs', '_asimov', '')
            else:
                ## filename gets label _asimov, histogram name remains as is
                self.adapt_shapes_lines(path, card, 'data_obs', '', '_asimov')
        print "...adjusting observation to modified shapes."
        for name in os.listdir(dir) :
            if not name.endswith('.txt') :
                continue
            self.adapt_observation_lines(dir+'/'+name)


