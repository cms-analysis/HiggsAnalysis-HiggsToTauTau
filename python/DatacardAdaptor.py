import os
import ROOT

from HiggsAnalysis.CombinedLimit.DatacardParser import *

class DatacardAdaptor(object) :
    """
    Description:

    This is a class for basic manipulations of datacards in a given directory. It provides the common functionliaty to trans-
    form lists od strings to comma separated strings that can be used for root macros like blindData.c and rescaleLumi.C and
    to replace paths to root input files to point to modified files (self.adapt_shape_lines). The latter assumes that the
    modified files exist in the same location as the original files but are distinguished by the original file only by a
    postfilx label. Only the templates corresponding to a given process will be picked up from the modified input file.
    """
    def __init__(self, parser_options) :
        ## options for the datacard parser
        self.options = parser_options
    
    def list2string(self, card, bin, procs) :
        """
        Translate a list of processes to a string that contains the names of the actual histograms and can actually be used
        for for further processing in root macros like blindData.C or rescaleSignal.C. The name of the histograms is obtained
        from the Daracard::path_of_shape for given bin and proc, the potential directories are snipped off from the path to
        make sure that just the histogram name is obtained. This treatment automatically guarantees that any prefixes or
        postfixes that might be part of the histogram name but not part of proc (including the keyword $MASS, that will be
        replaced during later steps of the processing in the class) that might be needed to find the shape histogram will be
        taken into account properly. 
        """
        s = ''
        for proc in procs :
            buffer = card.path_to_shape(bin, proc)
            if '/' in buffer :
                buffer = buffer[buffer.rfind('/')+1:]
            s += buffer+','
        return s.strip(',')

    def cleanup(self, dir, label) :
        """
        Cleanup all datacards and input files in dir before re-evaluation.
        """
        if label in os.listdir(dir+'/../common/') :
            os.system('rm {DIR}/../common/*{LABEL}'.format(DIR=dir, LABEL=label))
        for name in os.listdir(dir) :
            os.system("perl -pi -e 's/{LABEL}//g' {DIR}/{DATACARD}".format(LABEL=label, DIR=dir, DATACARD=name))

    def adapt_shapes_lines(self, path, target_proc, target_label) :
        """
        This is a function to modify 'shapes' lines in datacards to point to new root files with modified datasets or
        templates. It finds the lines starting with keyword 'shapes' in the datacard located at path. If there exists a
        shapes line for process target_proc it is modified to point to the same input file as before with the additional
        postfix label target_label. If there exists no shapes line a new line of type 'shapes' is added to the datacard
        with the 'shapes' line for process '*' as template and corresponding modification. 
        """
        old_file = open(path, 'r')
        card = parseCard(old_file, self.options)
        old_file.close()
        ## modify the input paths for the new datacards
        new_paths = []
        new_data_obs = []
        for bin in card.shapeMap.keys() :
            for proc in card.shapeMap[bin].keys() :
                ## define new_shapes line for process target_proc that points to a modified dataset or template. If there is
                ## a shapes line for target_proc it is modified accordingly. If not '*' serves as template for a the new 
                ## shapes line for target_proc and this new line is added to the datacard.
                if target_proc in proc :
                    new_target_proc_shapes = list(card.shapeMap[bin][proc])
                    if not '.root'+target_label in new_target_proc_shapes[0] :
                        new_target_proc_shapes[0] = new_target_proc_shapes[0].replace('.root','.root'+target_label)
                elif '*' in proc :
                    new_target_proc_shapes = list(card.shapeMap[bin][proc])
                    if not '.root'+target_label in new_target_proc_shapes[0] :
                        new_target_proc_shapes[0] = new_target_proc_shapes[0].replace('.root','.root'+target_label)
                ## for all but target_proc everything remains as is.
                if not target_proc in proc :
                    new_paths.append('shapes\t'+proc+'\t'+bin+'\t'+'\t'.join(card.shapeMap[bin][proc]))
            ## add the new path to target_proc to the end of all shapes. This should be done for each bin.
            new_paths.append('shapes\t'+target_proc+'\t'+bin+'\t'+'\t'.join(new_target_proc_shapes))
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
