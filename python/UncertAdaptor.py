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

    def cgs_processes(self, cgs_path, signal_procs=None, background_procs=None, signal_drop=None, background_drop=None) :
        """
        Add processes to signal and/or background in the cgs file located at cgs_path. In case there is no definition of
        signal add or uncomment it. In case any element in processes is part of the backgrounds remomve it from the
        backgrounds and vice versa.
        """
        file_old = open(cgs_path, 'r')
        file_new = open(cgs_path+"_tmp", 'w')
        for line in file_old :
            if "signal" in line :
                if signal_procs :
                    if line[0] == '#' :
                        line = line.lstrip('#')
            if self.cgs_signal_group in line :
                signals = [''] if signal_procs else line[line.rfind(self.cgs_signal_group)+len(self.cgs_signal_group)+1:].split(',')
                signals = [sig.strip() for sig in signals]
                line = line[:line.rfind(self.cgs_signal_group)+len(self.cgs_signal_group)+1]
                signals = self.setup_processes(signals, signal_procs, background_procs)
                signals = self.setup_processes(signals, None, signal_drop)
                line=line+','.join(signals)+'\n'
            if self.cgs_background_group in line:
                backgrounds = line[line.rfind(self.cgs_background_group)+len(self.cgs_background_group)+1:].split(',')
                backgrounds = [bck.strip() for bck in backgrounds]
                line = line[:line.rfind(self.cgs_background_group)+len(self.cgs_background_group)+1]
                backgrounds = self.setup_processes(backgrounds, background_procs, signal_procs)
                backgrounds = self.setup_processes(backgrounds, None, background_drop)
                line=line+','.join(backgrounds)+'\n'
            file_new.write(line)
        os.system("mv -v %s_tmp %s"%(cgs_path, cgs_path))
    def setup_processes(self, processes, appends, removes):
        """
        Basic function to first remove strings given in removes from processes and afterwards append strings given in appends
        """
        if removes:
            for proc in removes:
                if proc in processes:
                    processes.remove(proc)
        if appends:
            for proc in appends:
                if not proc in processes:
                    processes.append(proc)
        processes = filter(bool, processes)
        return processes
