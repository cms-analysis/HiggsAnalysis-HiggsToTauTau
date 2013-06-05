import os
import ROOT
from HiggsAnalysis.CombinedLimit.DatacardParser import *

class AsimovDatacard() :
    """
    Description:

    This class should take all datacards in a given directory and replace all data_obs histograms / entries by the asimov
    dataset. All data_obs histograms are kept in a file next to the original input files but indicated by an additional
    postfix _asimov. All datacardss in the given directory are modified accordingly to read the shapes for data from these
    new input files. The class works for shape analyses and counting experiments. Depending on the configuration all signal
    processes as given by the datacards can be added to the asimov dataset, multiplied by a scale factor, which is commonly
    applied to all signal processes. If configured such a parameter can be given to indicate the mass of the signal that
    should be added to the background processes. If a random seed>=0 is given the asimov dataset is randomized according
    to a poinsson dirstribution.
    """
    def __init__(self, parser_options, seed='-1', add_signal=True, mass='125', signal_scale='1.') :
        ## random seed in case the asimov dataset should be randomized (-1 will indicate that no randomization should be applied) 
        self.seed = seed
        ## should be true if signal should be considered for the asimov dataset
        self.add_signal = add_signal
        ## in case signal should be considered for the asimov datseet mass for the signal template
        self.mass = mass
        ## in case signal should be considered for the asimov dataset scale factor that should be used for the signal template
        self.signal_scale = signal_scale
        ## options for the datacard parser
        self.options = parser_options
    
    def list2string(self, card, bin, procs) :
        """
        Translate a list of processes to a string that contains the names of the actual histograms and can actually be used
        for blindData.C. The name of the histograms is obtained from the Daracard::path_of_shape for given bin and process,
        there potential directories are snipped off the path. This automatically contains any prefixes or postfixes (including
        the keyword $MASS, that will be replaced during later steps of the processing in the class) that might be needed to
        find the shape histogram. 
        """
        s = ''
        for proc in procs :
            buffer = card.path_to_shape(bin, proc)
            if '/' in buffer :
                buffer = buffer[buffer.rfind('/')+1:]
            s += buffer+','
        return s.strip(',')

    def adapt_shapes_lines(self, path) :
        """
        Find the lines starting with keyword 'shapes' in the datacard located at path. If there exists a shapes line
        for process data_obs modify it to point to the same input file with ending _asimov. If there exists no shapes
        line add a new shapes line with the shapes line for process '*' as template. 
        """
        old_file = open(path, 'r')
        card = parseCard(old_file, self.options)
        old_file.close()
        ## modify the input paths for the new datacards
        new_paths = []
        new_data_obs = []
        for bin in card.shapeMap.keys() :
            for proc in card.shapeMap[bin].keys() :
                ## define new_shapes line for process data_obs that points to asimov dataset. If there is a shapes line for process
                ## data_obs it is modified accordingly. If not '*' serves as template for a the new shapes for data_obs that and a
                ## new is added.
                if 'data_obs' in proc :
                    new_data_obs_shapes = list(card.shapeMap[bin][proc])
                    if not '.root_asimov' in new_data_obs_shapes[0] :
                        new_data_obs_shapes[0] = new_data_obs_shapes[0].replace('.root','.root_asimov')
                elif '*' in proc :
                    new_data_obs_shapes = list(card.shapeMap[bin][proc])
                    if not '.root_asimov' in new_data_obs_shapes[0] :
                        new_data_obs_shapes[0] = new_data_obs_shapes[0].replace('.root','.root_asimov')
                ## for all but data_obs everything remains as is.
                if not 'data_obs' in proc :
                    new_paths.append('shapes\t'+proc+'\t'+bin+'\t'+'\t'.join(card.shapeMap[bin][proc]))
            ## add the new path to data_obs to the end of all shapes; shape uncertainties are not needed for data_obs. This should be
            ## done for each bin.
            new_paths.append('shapes\tdata_obs'+'\t'+bin+'\t'+'\t'.join(new_data_obs_shapes))
        ## write new shapes lines to file
        first_pass = True
        old_file = open(path, 'r')
        new_file = open(path+'_tmp', 'w')
        for line in old_file :
            new_line = line
            words = line.lstrip().split()
            if words[0] == 'shapes' :
                if first_pass :
                    first_pass = False
                    new_line = '\n'.join(new_paths)+'\n'
                else :
                    continue
            new_file.write(new_line)
        new_file.close()
        old_file.close()
        os.system("mv {TMP} {FINAL}".format(TMP=path+'_tmp', FINAL=path))
                  
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
                    observations.append('%.d' % round(value))
                new_line = 'observation '+' '.join(observations)+'\n'
            new_file.write(new_line)
        old_file.close()
        new_file.close()
        os.system("mv {TMP} {FINAL}".format(TMP=path+'_tmp', FINAL=path))

    def asimov_shapes(self, dir) :
        """
        Parse all datacards in dir, collect signal and background processes and the paths to the input files and create
        the asimov dataset including background processes and signal processes if configured such. Write new rootfiles 
        which contain only the new data_obs histograms. This is done for each bin and each process independently. In a
        final step the individual rootfiles containing the asimov datasets are hadd'ed into one additional file for each
        inputfile with the extension _asimov. 
        """
        ## counter for files with blinded data_obs 
        index = 0
        ## processed files
        processed_files = []
        ## processed files and bins
        processed_files_bins = []
        ## parse all datacards, determine signal, background and  
        for name in os.listdir(dir) :
            if not name.endswith('.txt') :
                continue
            file = open(dir+'/'+name, 'r')
            card = parseCard(file, self.options)
            for bin in card.list_of_bins() :
                for proc in card.list_of_procs() :
                    path = card.path_to_file(bin, proc)
                    ## determine background list
                    bkg_list = self.list2string(card, bin, card.list_of_procs('b'))
                    ## determine signal list
                    sig_list = self.list2string(card, bin, card.list_of_procs('s')) if self.add_signal else ''
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
                                SEED = self.seed,
                                SCALE = self.signal_scale,
                                IDX = index,
                                DATA_OBS = self.list2string(card, bin, ['data_obs']) 
                                ))
                            index += 1
            file.close()
        ## combine all individual files into a single file for each used input rootfile
        for file in processed_files :
            os.system('hadd {TARGET} {SOURCE}'.format(
                TARGET=dir+'/'+file.replace('.root', '.root_asimov'),
                SOURCE=dir+'/'+file.replace('.root', '_*.root')
                ))
            os.system('rm {SOURCE}'.format(
                SOURCE=dir+'/'+file.replace('.root', '_*.root')
                ))

    def make_asimov_datacards(self, dir) :
        """
        For all datacards given in directory dir determine the paths to all root input files. Run the root macro
        blindData.C for all bins/channels and processes for which the datacards do require shapes. According to
        configuration add all background processes (and signal processes, if configured such) to the Asimov dataset.
        The data_obs histograms to contain the asimov datasets are written to separate files next to the original
        input files, indicatd by the postfix _asimov. All datacards are then adapted accordingly. If configured such
        the data_obs histograms / entries are randomized according to a Poisson distribution.
        """
        print "...creating asimov datasets."
        self.asimov_shapes(dir)
        print "...redirect input files in datacards."
        for card in os.listdir(dir) :
            if not card.endswith('.txt') :
                continue
            self.adapt_shapes_lines(dir+'/'+card)
        print "... adjust observation to modified shapes."
        for card in os.listdir(dir) :
            if not card.endswith('.txt') :
                continue
            self.adapt_observation_lines(dir+'/'+card)


