def htt_AZh(TYPE='ULB') :
    dict = {}
    dict['7TeV'] = 'None'
    dict['8TeV'] = 'ULB'
    dict['14TeV'] = 'None'
    return dict

def htt_ee(TYPE='KIT') :
    dict = {}
    dict['7TeV'] = 'DESY-KIT'
    dict['8TeV'] = 'DESY-KIT'
    dict['14TeV'] = 'DESY-KIT'
    return dict

def htt_mm(TYPE='KIT') :
    dict = {}
    dict['7TeV'] = 'DESY-KIT'
    dict['8TeV'] = 'DESY-KIT'
    dict['14TeV'] = 'DESY-KIT'
    return dict

def htt_em(TYPE='MIT') :
    dict = {}
    dict['7TeV'] = TYPE
    dict['8TeV'] = TYPE
    dict['14TeV'] = TYPE
    return dict    

def htt_et(TYPE='Imperial') :
    dict = {}
    dict['7TeV'] = TYPE
    dict['8TeV'] = TYPE
    dict['14TeV'] = TYPE
    return dict

def htt_mt(TYPE='Imperial') :
    dict = {}
    dict['7TeV'] = TYPE
    dict['8TeV'] = TYPE
    dict['14TeV'] = TYPE
    return dict

def htt_tt(TYPE='MIT') :
    dict = {}
    dict['7TeV'] = 'None'
    dict['8TeV'] = TYPE
    dict['14TeV'] = TYPE
    return dict

def vhtt(TYPE='VHTT') :
    dict = {}
    dict['7TeV'] = 'VHTT'
    dict['8TeV'] = 'VHTT'
    dict['14TeV'] = 'VHTT'
    return dict
