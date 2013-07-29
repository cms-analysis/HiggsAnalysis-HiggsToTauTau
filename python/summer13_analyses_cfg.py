def htt_ee(TYPE='KIT') :
    dict = {}
    dict['7TeV'] = 'DESY-KIT'
    dict['8TeV'] = 'DESY-KIT'
    return dict

def htt_mm(TYPE='KIT') :
    dict = {}
    dict['7TeV'] = 'DESY-KIT'
    dict['8TeV'] = 'DESY-KIT'
    return dict

def htt_em(TYPE='MIT') :
    dict = {}
    dict['7TeV'] = TYPE
    dict['8TeV'] = TYPE
    return dict    

def htt_et(TYPE='Imperial') :
    dict = {}
    dict['7TeV'] = TYPE
    dict['8TeV'] = TYPE
    return dict

def htt_mt(TYPE='Imperial') :
    dict = {}
    dict['7TeV'] = TYPE
    dict['8TeV'] = TYPE
    return dict

def htt_tt(TYPE='MIT') :
    dict = {}
    dict['7TeV'] = 'None'
    dict['8TeV'] = TYPE
    return dict

def vhtt(TYPE='VHTT') :
    dict = {}
    dict['7TeV'] = 'VHTT'
    dict['8TeV'] = 'VHTT'
    return dict
