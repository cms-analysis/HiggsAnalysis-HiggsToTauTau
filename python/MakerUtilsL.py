import re
import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import TFile,TH1F,TH1D

def main():
    db = DBuilder("unc.vals","inputs.txt","root/limit-inputs-mvis.root","unc.config","cgs.config")
    db.run()

class DBuilder:
    DividerStr = "------------------------------------------------------------------------------- \n"
    def __init__(self,uncertainty_file,out_file,root_file,unc_defs,cgs_defs,mass_point,categories=None):
        ## name of the input file to contain the uncertainties and where
        ## they apply (unc.vals)
        self.uncertainty_file = uncertainty_file
        ## name of the datacard output file (w/o .txt extension)
        self.out_file = out_file
        ## name of the root input file
        self.rootfile = root_file
        ## name of the input file to contain the uncertainty definitions
        ## (cgs.config)
        self.unc_defs = unc_defs
        ## name of the input file to contain the definitions of groups,
        ## categories, signal, backgrund and data (cgs.config)
        self.cgs_defs = cgs_defs
        ## masspoint for the signal samples
        self.mass_point = mass_point
        ## dictionary of samples mapping to predefined groups (like back-
        ## ground and signal)
        self.groups={}
        ## list of category names
        self.categories = []
        ## list of desired categories
        self.desired_categories = categories
        ## list of signal samples (mass point will be extended internally)
        self.signals = []
        ## list of the background samples
        self.backgrounds = []
        ## list of all simulated sample names (signal+background)
        self.samples = []
        ## name of the data sample; per default this should be data_obs,
        ## but it can also differ
        self.data_sample = ""
        ## dictionary of uncertainty names mapping to Uncertainty objects
        self.uncertainties = {}
        ## list of uncertainties
        self.unc_list = []
        ## the ultimate column width
        self.cw = 0
        ## width of the very first column
        self.column_zero_width = 0
        ## default name of RooWorkspace
        self.wsName = 'ws'

    def run(self):
        self.read_cgs()
        self.read_uncertainties()
        self.read()
        self.write()

    def read_cgs(self):
        width = 10
        f = open(self.cgs_defs)
        for line in f:
            line = line.strip().split("\n")[0].strip()
            ## remove all ',\s+' from line, so the group can be a comma
            ## seperated list separated by an arbitrary number of spaces
            pattern = re.compile(r",\s+")
            line = re.sub(pattern, ",", line)
            if line == "" or line.startswith("#") or line.startswith("%"):
                continue
            if line.startswith("$ GROUP"):
                wordarr = line.lstrip("$ GROUP").strip().split()
                name = wordarr[0]
                samples = wordarr[1].split(",")
                self.groups[name]=Group(name,samples)
                #print name,self.groups[name].samples
            if line.lower().startswith("categories:"):
                wordarr = line.lstrip("categories:").strip().split(",")
                # Only take desired categories
                self.categories=[
                    word for word in wordarr
                    if self.desired_categories is None or word in self.desired_categories]
                #print "categories are: ",self.categories
                for category in self.categories:
                    if len(category)+4 > width:
                        width = len(category)+4
            if line.lower().startswith("signals:"):
                self.signals = self.groups[line.lstrip("signals:").strip()].samples
                ## append the mass point in question to the signal samples in case of positive
                ## masses. In case of negative masses this part is skipped (usecase is the Ztt)
                ## cross section measeurement, which has Ztt as signal sample

                #for n in range(0, len(self.signals)):
                #    if int(self.mass_point)>0:
                #        self.signals[n]+=self.mass_point
                #        #print  self.signals[n]

                #print "signals are: ",self.signals
                for signal in self.signals:
                    if len(signal)+4> width:
                        width = len(signal)+4
            if line.lower().startswith("backgrounds:"):
                self.backgrounds = self.groups[line.lstrip("backgrounds:").strip()].samples
                #print "backgrounds are: ",self.backgrounds
                for background in self.backgrounds:
                    if len(background)+4>width:
                        width = len(background)+4
            if line.lower().startswith("data:"):
                self.data_sample = line.lstrip("data:").strip()
                #print "data is: ",self.data_sample
                if len(self.data_sample)+4>width:
                        width = len(self.data_sample)+4
        #print self.signals
        #print self.backgrounds
        self.samples = self.signals + self.backgrounds
        self.cw = width

    def read_uncertainties(self):
        f = open(self.unc_defs)
        width = 15
        for line in f:
            line = line.strip().rstrip("\n")
            if line == "" or line.startswith("#") or line.startswith("%"):
                continue
            else:
                wordarr = line.split()
                name = wordarr[0].strip()
                type = wordarr[1].strip()
		sideband_events = 0
                if len(wordarr)>2 and type == "gmN":
                    try:
                        sideband_events=int(wordarr[2])
                        #print "SIDEBAND EVENTS ARE: %d" % sideband_events
                    except ValueError as e:
                        print "gmN is expecting a numerical value for the number of events in the sideband"
                        raise
                self.uncertainties[name]=Uncertainty(name,type,sideband_events)
                self.unc_list.append(name)
                #print self.uncertainties[name].name,self.uncertainties[name].type
                if len(line)+4>width:
                    width = len(line)+4
        self.column_zero_width = width

    def read(self):
       file = open(self.uncertainty_file)
       for line in file:
           line = line.strip().split("\n")[0].strip()
           ## remove all ',\s+' from line, so the group can be a comma
           ## seperated list separated by an arbitrary number of spaces
           pattern = re.compile(r",\s+")
           line = re.sub(pattern, ",", line)
           #print line
           if line.startswith("#") or line.startswith("%") or line.strip()=="":
               continue
           wordarr = line.strip().rstrip("\n").strip().split()
           category_names = wordarr[0]
           sg_name = wordarr[1]
           uncert_name = wordarr[2]
           if not self.uncertainties.has_key(uncert_name):
               print "uncertainty not found."
           uncert = self.uncertainties[uncert_name]
           uncert_val=0
           if uncert.type != "gmN":
               uncert_val = float(wordarr[3])
           rel_categories = category_names.split(",")
           #print rel_categories
           samples_groups = sg_name.split(",")
           #print "samples_groups for this unc.:",samples_groups
           rel_samples = []
           for item in samples_groups:
               for comp in self.signals :
                   if comp.find(item)>-1:
                       item = comp
               if item in self.groups.keys():
                   #print item
                   for sample in self.groups[item].samples:
                       rel_samples.append(sample)
               if item in self.samples:
                   #print item
                   rel_samples.append(item)
           #print "rel samples for this unc.:",rel_samples
           for category in rel_categories:
               for sample in rel_samples:
                   #print "Adding the following category,sample,uncname,value pair...",category,sample,uncert_name,uncert_val
                   if not uncert.vals.has_key(category):
                       uncert.vals[category]={}
                   uncert.vals[category][sample]=uncert_val

    def get_rate(self,category,sample,mass=0):
        rate = 0
        f = TFile(self.rootfile)
        #print "fileName = %s" % self.rootfile
        #print f
        histName = category + "/" + sample
        if mass>0 :
            histName += mass
        #print "histogram name =", histName
        hist = f.Get(histName)
        #print hist
        if hist:
            rate = hist.Integral()
            if rate < 0:
                rate = 0
        else:
            wsPath = category + '/' + self.wsName
            ws = f.Get(wsPath)
            if not ws:
                raise Exception("Failed to find histogram %s or RooWorkspace %s in file %s" % (histName, wsPath, self.rootfile))
            # First check if the sample is data
            data = ws.data(sample)
            if data:
                rate = data.sumEntries()
            else:
                # Otherwise, check if the sample is a PDF
                pdf = ws.pdf(sample)
                if pdf:
                    rate = ws.pdf(sample).expectedEvents(None) # May need to provide variables in the future
                else:
                    raise Exception('Failed to find sample %s in RooWorkspace %s in file %s' % (sample, wsPath, self.rootfile))
        #print "type of hist is:",type(hist)
        #print "rate of %s in category %s is " % (sample,category),hist.Integral()
        #print "histogram normalization = ", rate
        return rate

    def write(self):
        outfile = open(self.out_file,'w')
        self.write_lands(outfile)
        self.write_paths(outfile)
        self.write_bins(outfile)
        self.write_vals(outfile)
        outfile.close()

    def write_lands(self,outfile):
        imax_str = "imax    %d     number of categories \n" % (len(self.categories))
        jmax_str = "jmax    %d     number of samples minus one \n" % (len(self.samples)-1)
        #kmax_str = "kmax    %d     number of nuisance parameters \n" % len(self.uncertainties.keys())
        kmax_str = "kmax    *     number of nuisance parameters \n"
        outfile.write(imax_str+jmax_str+kmax_str+DBuilder.DividerStr)

    def write_paths(self,outfile):
        kShapeUnc = False
        for unc in self.uncertainties.values():
            if unc.type == "shape":
                kShapeUnc = True
        wsPrefix = self.wsName + ':' if self.checkRooWorkspace() else ''
        #for category in self.categories:
        cat_str=""
        if kShapeUnc:
            cat_str="shapes * * %(file)s $CHANNEL/%(ws)s$PROCESS $CHANNEL/%(ws)s$PROCESS_$SYSTEMATIC \n" % {'file': self.rootfile, 'ws': wsPrefix}
            for signal in self.signals :
                ## add extra lines, which contain the corresponding mass, for all signal processes
                cat_str+="shapes %(signal)s * %(file)s $CHANNEL/%(ws)s$PROCESS$MASS $CHANNEL/%(ws)s$PROCESS$MASS_$SYSTEMATIC \n" % {'signal': signal, 'file': self.rootfile, 'ws': wsPrefix}
        else:
            cat_str = "shapes * * %(file)s $CHANNEL/%(ws)s$PROCESS \n" % {'file': self.rootfile, 'ws': wsPrefix}
            for signal in self.signals :
                ## add extra lines, which contain the corresponding mass, for all signal processes
                cat_str+= "shapes %(signal)s * %(file)s $CHANNEL/%(ws)s$PROCESS$MASS \n" % {'signal': signal, 'file': self.rootfile, 'ws': wsPrefix}
        outfile.write(cat_str)
        outfile.write(DBuilder.DividerStr)

    def write_bins(self,outfile):
        bin_str = "bin".ljust(self.column_zero_width)
        for category in self.categories:
            bin_str += category.ljust(self.cw)
        bin_str += " \n"
        outfile.write(bin_str)
        obs_str = "observation".ljust(self.column_zero_width)
        for category in self.categories:
            obs_str += ("%.0f"  % self.get_rate(category,self.data_sample)).ljust(self.cw)
        obs_str += " \n"
        outfile.write(obs_str)
        outfile.write(DBuilder.DividerStr)
        bins_str = "bin".ljust(self.column_zero_width)
        for category in self.categories:
            for index in range(len(self.signals)+len(self.backgrounds)):
                bins_str += category.ljust(self.cw)
        bins_str += " \n"
        outfile.write(bins_str)
        process_str_n = "process".ljust(self.column_zero_width)
        for category in self.categories:
            for signal_index in range(len(self.signals)):
                process_str_n += ("%d" % (signal_index-len(self.signals)+1)).ljust(self.cw)
            for background_index in range(1,len(self.backgrounds)+1):
                process_str_n += ("%d" % (background_index)).ljust(self.cw)
        process_str_n += " \n"
        outfile.write(process_str_n)
        process_str_l = "process".ljust(self.column_zero_width)
        for category in self.categories:
            for signal in self.signals:
                process_str_l += signal.ljust(self.cw)
            for background in self.backgrounds:
                process_str_l += background[0:self.cw-2].ljust(self.cw)
        process_str_l += " \n"
        process_str_l += "rate".ljust(self.column_zero_width)
        for category in self.categories:
            for signal in self.signals:
                process_str_l += ("%6g"  % (self.get_rate(category,signal,self.mass_point))).ljust(self.cw)
            for background in self.backgrounds:
                process_str_l += ("%6g" % (self.get_rate(category,background))).ljust(self.cw)
            for sample in self.samples:
                for unc_name,unc in self.uncertainties.iteritems():
                    if unc.vals.has_key(category):
                        if unc.vals[category].has_key(sample) and unc.type == "gmN":
                            # It's possible that we would want to use a gmN
                            # uncertainty to describe the stat uncertainty on a
                            # signal yield (for example in ZH).  We need to pass
                            # the mass in this case.
                            mass_for_gmN_query = 0
                            if sample in self.signals:
                                mass_for_gmN_query = self.mass_point
                            #print unc_name,"with %d sideband events" % unc.sideband_events
                            unc.vals[category][sample]=self.get_rate(category,sample,mass_for_gmN_query)/unc.sideband_events
        process_str_l += " \n"
        outfile.write(process_str_l)
        outfile.write(DBuilder.DividerStr)

    def write_vals(self,outfile):
        for uncertainty_name in self.unc_list:
            uncert = self.uncertainties[uncertainty_name]
            uncert_str = ""
            if uncert.type=="gmN":
                uncert_str = ("%s %s %d" % (uncert.name,uncert.type,uncert.sideband_events)).ljust(self.column_zero_width)
            else:
                uncert_str = ("%s %s" % (uncert.name,uncert.type)).ljust(self.column_zero_width)
            # If this systematic never appears in a category which is used, omit
            uncertainty_is_used = False
            for category_name in self.categories:
                for signal in self.signals:
                    sample_name = signal
                    try:
                        uncert_val = uncert.vals[category_name][sample_name]
                        #print category_name,sample_name,uncert.name,uncert_val
                        uncert_str += ("%4g" % uncert_val).ljust(self.cw)
                        uncertainty_is_used = True
                    except KeyError as e:
                        uncert_str += "-".ljust(self.cw)
                for background in self.backgrounds:
                    sample_name = background
                    try:
                        uncert_val = uncert.vals[category_name][sample_name]
                        #print category_name,sample_name,uncert.name,uncert_val
                        if uncert.type=="gmN":
                            uncert_str += ("%f" % uncert_val).ljust(self.cw)
                        else:
                            uncert_str += ("%4.3f" % uncert_val).ljust(self.cw)
                        uncertainty_is_used = True
                    except KeyError as e:
                        uncert_str += "-".ljust(self.cw)
            uncert_str += " \n"
            if uncertainty_is_used:
                outfile.write(uncert_str)

    def checkRooWorkspace(self):
        f = TFile(self.rootfile)
        ws = f.FindObjectAny(self.wsName)
        f.Close()
        return bool(ws)

class Group:
    def __init__(self,name,samples):
        self.name = name
        self.samples = samples

class Uncertainty:
    def __init__(self,name,type,sb_events=0):
        self.name = name
        self.type = type
        self.sideband_events = sb_events
        self.vals = {}

if __name__=='__main__': main()
