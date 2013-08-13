import os
import re

class UncertAdaptor(object) :
    """
    Description:

    This is a class for basic manipulations of uncertainty files in a given setup directory. This should work on a single set
    of uncertainty files of type cgs.conf, unc.conf, unc.vals that are passed on to the member functions as arguments.
    """
    def __init__(self, cgs_signal_group='GROUP signal', cgs_background_group='GROUP background') :
        ## key string for signal grouping in the cgs.conf file
        self.cgs_signal_group = cgs_signal_group
        ## key string for background grouping in the cgs.conf file
        self.cgs_background_group = cgs_background_group
        ## regex pattern to remove whitespaces if needed
        self.whitespace = re.compile(r',\s*,')

    def cgs_processes(self, cgs_path, signal_procs=None, background_procs=None) :
        """
        Add processes to signal and/or background in the cgs file located at cgs_path. In case there is no definition of
        signal add or uncomment it. In case any element in processes is part of the backgrounds remomve it from the
        backgrounds and vice versa.
        """
        file_old = open(cgs_path, 'r')
        file_new = open(cgs_path+"_tmp", 'w')
        for line in file_old :
            if "signals" in line :
                if signal_procs :
                    if line[0] == '#' :
                        line = line.strip('#')
            if self.cgs_signal_group in line :
                signalstr = ''
                if signal_procs :
                    if line[0] == '#':
                        ## uncomment and remove remnants of what had been commented, in case
                        ## they exist; furthermore we need to get rid of the leading ',' for
                        ## the first element.
                        line = line[1:line.rfind(self.cgs_signal_group)+len(self.cgs_signal_group)+1]
                    ## setup string of signal processes
                    for signal in signal_procs :
                        if not signal in line :
                            signalstr+= ","+signal
                if line.split()[-1] == 'signal' :
                    signalstr = signalstr.strip(',')
                line=line.rstrip('\n')+signalstr+'\n'
                ## remove elements that might be part of signal, in case they should be moved
                ## to background.
                if background_procs :
                    for signal in background_procs :
                        line=line.replace(signal, '')
                        line = re.sub(self.whitespace, '', line)
            if self.cgs_background_group in line:
                ## remove procs that might have been moved to signal from the background group
                if signal_procs :
                    for signal in signal_procs :
                        line=line.replace(signal, '')
                        line = re.sub(self.whitespace, '', line)
                backgroundstr=''
                if background_procs :
                    for background in background_procs :
                        if not background in line :
                            backgroundstr+=","+background
                line=line.rstrip('\n')+backgroundstr+'\n'                        
            file_new.write(line)
        os.system("mv -v %s_tmp %s"%(cgs_path, cgs_path))
