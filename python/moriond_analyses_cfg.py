def htt_mm(TYPE='KIT') :
    dict = {}
    dict['7TeV'] = 'Htt_MuMu_Unblinded'
    dict['8TeV'] = 'Htt_MuMu_Unblinded'
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
