def get_mass(directory) :
    '''
    Returns the mass from a directory string. directories
    are expected to end with a floating point number of
    with an integer number. Trailing slashes are removed.
    The mass is returned as a string.
    '''
    idx = directory.rfind("/")
    if idx == (len(directory) - 1):
        idx = directory[:idx - 1].rfind("/")
    mass  = directory[idx + 1:]
    return mass.rstrip('/')

def is_number(s):
    '''
    check if the string is a number or not (works for int and float)
    '''
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_integer(elem):
    '''
    check if the element is an integer number or close to an integer number within
    a precision of 1e-6
    '''
    try:
        int(elem)
    except ValueError:
        return False
    if abs(int(elem) - float(elem)) < 1e-6:
        return True
    return False

def contained(elem, list) :
    """
    return true if the element is contained in the list
    """
    if elem in "\n".join(list) :
        return True
    return False


def mass_category(mass, category, channel) :
    """
    return the mass category depending on the value of mass. Currently we
    will have only one mass category for the pt sub-categorization.
    """
    value = float(mass)
    mass_category = 0
    if "hbb" in channel :
        if category in "0 1 2 3 4 5" :
            if value>=180 :
                mass_category = 1
            elif value<180 :
                mass_category = 0
        if category in "6" :
            if value>=200 :
                mass_category = 1
            elif value<200 :
                mass_category = 0
    return mass_category

def parseArgs(args) :
    """
    parse a list of arguments which can be floats, intergers or of type
    intA-intB:step where intA<=intB and both intA and intB have to be
    integers or floats 
    and fill this list of arguments into a list
    """
    list = []
    for elem in args :
        if elem.find("-") > -1 :
            if elem.find(":") > -1 :
                step = float(elem[elem.find(":")+1:])
                min = float(elem[:elem.find("-")  ])
                max = float(elem[elem.find("-")+1:elem.find(":")])
            else :
                step = 1
                min = float(elem[:elem.find("-")  ])
                max = float(elem[elem.find("-")+1:])
            while min <= max :
                if is_integer(min):
                    if not int(min) in list :
                        list.append(int(min))
                else:
                    if not min in list :
                        list.append(min)
                min=min+step
        else :
            if is_integer(elem):
                if not int(elem) in list :
                    list.append(int(elem))
            else:
                if not elem in list :
                    list.append(elem)
    return list

def get_channel_dirs(finalstate, category, period):
    ''' Turn 'mt' + 00 -> muTau_0jet_low '''
    fs_map = {
        'mt'  : 'muTau',
        'et'  : 'eleTau',
        'em'  : 'emu',
        'mm'  : 'mumu',
        'ee'  : 'ee',
        'tt'  : 'tauTau',
        'vhtt': '',
    }
    cat_map = {'7TeV':
        {
        'ee' : {
        '00' : ['0jet_low' ],
        '01' : ['0jet_high'],
        '02' : ['1jet_low' ],
        '03' : ['1jet_high'],
        '04' : ['vbf'      ],
        '08' : ['nobtag'   ],
        '09' : ['btag'     ],
        },
        'mm' : {
        '00' : ['0jet_low' ],
        '01' : ['0jet_high'],
        '02' : ['1jet_low' ],
        '03' : ['1jet_high'],
        '04' : ['vbf'      ],
        '08' : ['nobtag'   ],
        '09' : ['btag'     ],
        },
        'em' : {
        '00' : ['0jet_low' ],
        '01' : ['0jet_high'],
        '02' : ['1jet_low' ],
        '03' : ['1jet_high'],
        '04' : ['vbf_loose'],
        '08' : ['nobtag'   ],
        '09' : ['btag'     ],
        },
        'et' : {
        '00' : ['0jet_low'   ],
        '01' : ['0jet_medium'],
        '02' : ['0jet_high'  ],
        '03' : ['1jet_medium'],
        '04' : ['1jet_high_lowhiggs'],
        '05' : ['1jet_high_mediumhiggs'],
        '06' : ['vbf'  ],
        '08' : ['nobtag'     ],
        '09' : ['btag'       ],
        },
        'mt' : {
        '00' : ['0jet_low'   ],
        '01' : ['0jet_medium'],
        '02' : ['0jet_high'  ],
        '03' : ['1jet_medium'],
        '04' : ['1jet_high_lowhiggs'],
        '05' : ['1jet_high_mediumhiggs'],
        '06' : ['vbf'  ],
        '08' : ['nobtag'     ],
        '09' : ['btag'       ],
        },
        'tt' : {
        },
        'vhtt' : {
        '00' : ['mmt'],
        '01' : ['emt'],
        '02' : ['eetCatHigh', 'eetCatLow'],
        '03' : ['mmme_zh', 'eeem_zh' ],
        '04' : ['mmmt_zh', 'eemt_zh' ],
        '05' : ['mmet_zh', 'eeet_zh' ],
        '06' : ['mmtt_zh', 'eett_zh' ],
        '07' : ['mtt'],
        '08' : ['ett'],
        },        
        },
        '8TeV':
        {
        'ee' : {
        '00' : ['0jet_low' ],
        '01' : ['0jet_high'],
        '02' : ['1jet_low' ],
        '03' : ['1jet_high'],
        '04' : ['vbf'      ],
        '08' : ['nobtag'   ],
        '09' : ['btag'     ],
        },
        'mm' : {
        '00' : ['0jet_low' ],
        '01' : ['0jet_high'],
        '02' : ['1jet_low' ],
        '03' : ['1jet_high'],
        '04' : ['vbf'      ],
        '08' : ['nobtag'   ],
        '09' : ['btag'     ],
        },
        'em' : {
        '00' : ['0jet_low' ],
        '01' : ['0jet_high'],
        '02' : ['1jet_low' ],
        '03' : ['1jet_high'],
        '04' : ['vbf_loose'],
        '05' : ['vbf_tight'],
        '08' : ['nobtag'   ],
        '09' : ['btag'     ],
        },
        'et' : {
        '00' : ['0jet_low'   ],
        '01' : ['0jet_medium'],
        '02' : ['0jet_high'  ],
        '03' : ['1jet_medium'],
        '04' : ['1jet_high_lowhiggs'],
        '05' : ['1jet_high_mediumhiggs'],
        '06' : ['vbf_loose'  ],
        '07' : ['vbf_tight'  ],
        '08' : ['nobtag'     ],
        '09' : ['btag'       ],
        },
        'mt' : {
        '00' : ['0jet_low'   ],
        '01' : ['0jet_medium'],
        '02' : ['0jet_high'  ],
        '03' : ['1jet_medium'],
        '04' : ['1jet_high_lowhiggs'],
        '05' : ['1jet_high_mediumhiggs'],
        '06' : ['vbf_loose'  ],
        '07' : ['vbf_tight'  ],
        '08' : ['nobtag'     ],
        '09' : ['btag'       ],
        '10' : ['soft_0jet_low'   ],
        '11' : ['soft_0jet_medium'],
        '12' : ['soft_0jet_high'  ],
        '13' : ['soft_1jet_medium'],
        '15' : ['soft_1jet_high'  ],
        '16' : ['soft_vbf'   ],
        },
        'tt' : {
        '00' : ['1jet_high_mediumhiggs'],
        '01' : ['1jet_high_highhiggs'],
        '02' : ['vbf'   ],
        '08' : ['nobtag'],
        '09' : ['btag'  ],              
        },
        'vhtt' : {
        '00' : ['mmtCatHigh', 'mmtCatLow'],
        '01' : ['emtCatHigh', 'emtCatLow'],
        '02' : ['eetCatHigh', 'eetCatLow'],
        '03' : ['mmme_zh', 'eeem_zh' ],
        '04' : ['mmmt_zh', 'eemt_zh' ],
        '05' : ['mmet_zh', 'eeet_zh' ],
        '06' : ['mmtt_zh', 'eett_zh' ],
        '07' : ['mtt'],
        '08' : ['ett'],
        },        
    }
    }
    if fs_map[finalstate] == '' :
        return cat_map[period][finalstate][category]
    else :
        combined_names = []
        for dir in cat_map[period][finalstate][category] :
            combined_names.append(fs_map[finalstate]+'_'+dir)
        return combined_names

def get_shape_systematics(setup, period, channel, category, proc, catname = None):
    """
    take a set of inputs corresponding to an uncertainty configuration
    and return a list of all shape uncertainties corresponding to the given process
    """
    card = "-sm-{PER}-{CAT}".format(PER=period, CAT=category)
    shape_systematics = []
    proc_qualifier = [proc]
    ## determine the names used for the process in the uncertainty file
    cgs = open(setup+"/"+channel+"/cgs"+card+".conf")
    for line in cgs:
        line = line.strip().split()
        if line and line[0] == '$':
            new_line = []
            for l in line:
                new_line.extend(l.split(','))
            line = [l.strip().strip(',') for l in new_line]
            if proc in line:
                   proc_qualifier.append(line[2])
    cgs.close()
    ## extract all uncertainties which are associated with the process from the unc*.vals file
    vals = open(setup+"/"+channel+"/unc"+card+".vals")
    for line in vals:
        line = line.strip().split()
        if line and '#' not in line[0]:
            if not catname or line[0] == catname:
                if any(procs in [i.strip() for i in line[1].split(',')] for procs in proc_qualifier):
                    shape_systematics.append(line[2])
    vals.close()
    ## remove all non-shape uncertainties from the list of uncertainties
    config = open(setup+"/"+channel+"/unc"+card+".conf")
    for line in config:
        line = line.strip().split()
        if line and '#' not in line[0]:
            if line[0] in shape_systematics and line[1] != 'shape':
                shape_systematics.remove(line[0])
    config.close()
    return shape_systematics
