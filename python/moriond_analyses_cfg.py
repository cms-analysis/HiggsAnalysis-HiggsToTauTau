def htt_ee(TYPE='KIT') :
    dict = {}
    dict['7TeV'] = 'Htt_EE'
    dict['8TeV'] = 'Htt_EE'
    return dict

def htt_mm(TYPE='KIT') :
    dict = {}
    dict['7TeV'] = 'Htt_MuMu'
    dict['8TeV'] = 'Htt_MuMu'
    return dict

def htt_em(TYPE='MIT') :
    dict = {}
    dict['7TeV'] = 'MIT'
    dict['8TeV'] = TYPE
    return dict    

def htt_et(TYPE='Wisconsin') :
    dict = {}
    dict['7TeV'] = 'Imperial'
    dict['8TeV'] = TYPE
    return dict

def htt_mt(TYPE='Wisconsin') :
    dict = {}
    dict['7TeV'] = 'Imperial'
    dict['8TeV'] = TYPE
    return dict

def htt_tt(TYPE='MIT') :
    dict = {}
    directories = {'MIT' : 'MIT', 'CERN' : 'Htt_FullHad'}
    dict['7TeV'] = 'None'
    dict['8TeV'] = directories[TYPE]
    return dict
