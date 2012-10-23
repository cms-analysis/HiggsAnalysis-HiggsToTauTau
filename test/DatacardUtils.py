import re

def get_svar(factor,fname):
    '''Obtains the sigma variation of fit parameter (factor) from the fit result file ffile'''
    ffile = open(fname,'r')
    for line in ffile.readlines():
        if line.strip().lower().startswith(factor.lower()):
            res = re.search("[+-]\d+\.\d+(?=sig)",line)
            svar = float(res.group(0))
            #svar = float(line.strip().split()[1].split(",")[0])
            return svar
            #return float(res.group(0))
            
def get_sigma(factor,fname):
    '''Obtains the sigma of fit parameter (factor) from the fit result file ffile'''
    ffile = open(fname,'r')
    for line in ffile.readlines():
        if line.strip().lower().startswith(factor.lower()):
	    sigma = float(line.split("(")[1].split(")")[0].split(" ")[1])
            return sigma
            
def parse_dcard(datacard,fitres,bin_name="ANYBIN"):
    '''Parses a datacard and returns a dictionary with sample names as keys and fit weights as the values.'''

    # Relies upon a certain datacard layout: "sections" are divided by lines of dashes ("---------")
    # The second to last section should include a row that starts with "process" and has columns for each
    # sample name, separated by whitespace. The last section consists of rows in the following format:
    # parameter_name fit_type uncert_1 uncert_2 uncert_3 ...., where uncert_1 is the value of a +1 sigma
    # variation in the parameter. Only parameters of type "lnN" are considered. The number of sigma
    # variations of a given parameter in the ml fit is given in the fit result file, fitres; this value is
    # obtained by calling DatacardUtils.get_svar (see above). The size of the sigma variation is multiplied
    # by the number of sigma variations and added to 1 in order to get the fit weight. The resulting
    # dictionary is the list of fit weights for the category specified by bin_name (or else the only
    # category represented in the sample if bin_name="ANYBIN" is specified

    weights_dict = {}
    #files are opened
    dcard = open(datacard,'r')
    #section and process_line are bookkeepers
    section = 0
    bins = []
    rel_indices = []
    processes = []
    process_weights = {}
    process_uncertainties = {}
    process_shape_weights = {}
    process_shape_uncertainties = {}
    factor_weights = {}
    rates = []
    nsplits = 0
    process_section = 0
    for sline in dcard:
       #print 'hello'
       sline = sline.strip()
       if sline.startswith('--'):
           nsplits +=1 
       if sline.startswith('process'):
           process_section = nsplits
           continue
    
    mycard = open(datacard,'r')
    for line in mycard:
       #print line
       if line.startswith("#") or line.strip() == "":
           continue
       if line.startswith("--"):
           section+= 1
           continue
       if section == process_section:
           if line.strip().startswith("bin"):
               bins = line.strip().split()[1:]
               for index in range(len(bins)):
                   if bins[index] == bin_name or bin_name == "ANYBIN":
                       rel_indices.append(index)
           if line.strip().startswith("process"):
               tprocesses = line.strip().split()[1:]
               try:
                   intval = int(tprocesses[0])
                   continue
               except ValueError:
               # initialize the weights in the weights dictionary
                   processes = tprocesses
                   for process in processes:
                       process_weights[process]=1
                       process_uncertainties[process]=0
                       process_shape_weights[process]={}
                       process_shape_uncertainties[process]={}
               # we don't gain any valuable information from the second line beginning with "process", which numbers the bins
               
           # need to figure out what this is useful for.
           if line.strip().startswith("rate"):
               rates = line.strip().split()
               for index in range(len(rates)):
                   if index is not 0:
                       rates[index] = float(rates[index])
           else:
               continue
       
       # here is we parse the actual uncertainty values
       if section==process_section+1:
           #print line
           info = line.strip().split("\n")[0].split()
           factor_name = info[0].strip() # the factor name will need to match 
           # log normal or gaussian are the usual fit types
           fit_type = info[1].strip()
           aligned_list = info[2:]
           #print "aligned list length is %d" % len(processes)
           for index in range(0,len(bins)):
               if not (index in rel_indices):
                   continue
               val = aligned_list[index].strip()
               # the datacard has a dash if the uncertainty does not apply to that sample
               if val == "-":
                   continue
               else:
                   # the uncertainty is a float
                   uncert = float(val)
                   # subtract 1 to get a decimal representation of the "percent" uncertainty
                   uncert -= 1
                   svar = get_svar(factor_name,fitres) #obtain the sigma variation
                   if type(svar).__name__=="NoneType" :
                       svar = 0.0
                   sigma = get_sigma(factor_name,fitres) #obtain the sigma variation
                   if type(sigma).__name__=="NoneType" :
                       sigma = 0.0
                   #print processes[index],factor_name,"Uncertainty: ",uncert,"Sigma variations: ",svar,"Total: ",1+uncert*svar
                   new_weight = 1 + uncert*svar
                   if fit_type.strip() == "gmN":
                       new_weight = 1 + svar
                   if new_weight<0:
                       new_weight = 0
                       print "SETTING WEIGHT TO 0... NEGATIVE WEIGHT FOUND", processes[index], factor_name, uncert, svar
		   if fit_type.strip() == "lnN":
                       process_weights[processes[index]]*= new_weight #multiply the existing weight by the new weight.
                       process_uncertainties[processes[index]]+= pow(uncert*sigma,2)
		   elif fit_type.strip() == "shape":
                       process_shape_weights[processes[index]][factor_name] = float(val)*svar #multiply the existing weight by the new weight.
                       process_shape_uncertainties[processes[index]][factor_name] = sigma
   # return the dictionary of weights
                   factor_weights[factor_name]= "%f ; // 1+%f*%f " % (1+uncert*svar,uncert,svar)
    #print "the list of indices for bin %s is:" % bin_name,rel_indices
    return process_weights, process_shape_weights, process_uncertainties, process_shape_uncertainties
