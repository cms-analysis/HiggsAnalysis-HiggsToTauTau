from HiggsAnalysis.HiggsToTauTau.tools.mssm_xsec_tools import mssm_xsec_tools
from HiggsAnalysis.HiggsToTauTau.tools.hplus_xsec_tools import hplus_xsec_tools
from HiggsAnalysis.HiggsToTauTau.tools.feyn_higgs_mssm import feyn_higgs_mssm
from HiggsAnalysis.HiggsToTauTau.MODEL_PARAMS import MODEL_PARAMS
from os import getenv
from sys import exit

class ModelParams_BASE:
    """
    Description:

    Basic class for determination of model parameters.
    This class takes as input mA and tanb and and additional parameter for the model.
    It then determines the parameter of the model and stores them in a variable of type
    MODEL_PARAMS.
    The main functions to be used for creation of the MODEL_PARAMS are 'setup_model' and  'create_model_params'
    """
    def __init__(self, parameter1, tanb, ana_type):
        self.parameter1 = parameter1 #mass of pseudoscalar A or for lowmH scenario the higgsino mass mu
        self.tanb = tanb
        self.ana_type = ana_type
   
    def setup_model(self, period, modelpath='mhmax-mu+200', modeltype='mssm_xsec'):
        """
        Function to setup the model for the determination of crossection and brnachingratios
        arguments as period, modelpath and modeltype
        periode is one of '7TeV', '8TeV'
        modelpath corresponds to the file to be used for the model specified in modeltype
          - feyn_higgs_mssm : modelpath is the name of the model to be used (e.g. mhmax)
          - mssm_xsec_tools : modelpath is the name of the model to be used including uncerts (e.g mhmax-mu+200)
        modeltype can be 'mssm_xsec' or 'feyn_higgs'
        """
        self.model = modeltype
        if modeltype == 'mssm_xsec':
            if float(self.tanb) < 1:
                tanbregion = 'tanbLow'
            else:
                tanbregion = 'tanbHigh'
            mssm_xsec_tools_path = getenv('CMSSW_BASE')+'/src/auxiliaries/models/out.'+modelpath+'-'+period+'-'+tanbregion+'-nnlo.root'
            scan = mssm_xsec_tools(mssm_xsec_tools_path)
            self.htt_query = scan.query(self.parameter1, self.tanb, self.ana_type)
        elif modeltype == 'hplus_xsec' :
            hplus_xsec_tools_path = getenv('CMSSW_BASE')+'/src/auxiliaries/models/hplus.'+modelpath+'-'+period+'-LHCHXSWG.root'
            scan = hplus_xsec_tools(hplus_xsec_tools_path)
            self.htt_query = scan.query(self.parameter1, self.tanb)

    def create_model_params(self, period, channel, decay, uncert=''):
        """
        Main function to be used for creating a object of type MODEL_PARAMS for a given period,
        production channel, decay channel and model.
        periode is one of '7TeV', '8TeV'
        channel is of type ggH
        decay is of type [h,H,A]tt
        uncert specifies the uncertainty to be used. It can be 'mu+', 'mu-', 'pdf+', 'pdf-' or ''
        The trailing +/- corresponds to an up/down fluctuation of the uncertainty.
        '' specifies no uncertainty to be used.
        """
        self.uncert = uncert
        model_params = MODEL_PARAMS(self.ana_type)
        if self.model == 'feyn_higgs':
            self.use_feyn_higgs(modelpath, period, channel, decay, model_params)
        elif self.model == 'mssm_xsec':
            self.use_mssm_xsec(self.htt_query, channel, decay, model_params)
        elif self.model == 'hplus_xsec':
            self.use_hplus_xsec(self.htt_query, channel, decay, model_params)           
        else:
            exit('ERROR: modeltype \'%s\' not supported'%modeltype)
        return model_params

    def use_feyn_higgs(self, path, period, channel, decay, model_params):
        """
        This functions takes the input from create_model_params and uses feyn_higgs_mssm to determine the masses, cross-sections
        and branchingratios for the given production and decay channels
        """
        scan = feyn_higgs_mssm(self.parameter1, self.tanb, 'sm', path, period) #consider using variable for 'sm', 'mssm'
        for higgs in model_params.list_of_higgses:
            if higgs == 'A': model_params.masses[higgs] = self.parameter1
            if higgs == 'h': model_params.masses[higgs] = scan.get_mh()
            if higgs == 'H': model_params.masses[higgs] = scan.get_mH()
            xsecs = scan.get_xs(channel[:-1]+higgs)
            model_params.xsecs[higgs] = xsecs
            brs = scan.get_br(higgs+decay[1:])
            model_params.brs[higgs] = brs

    def use_mssm_xsec(self, query, channel, decay, model_params):
        """
        This function takes the input from create_model_params and uses mssm_xsec_tools to determine the masses,
        cross-sections and branchingratios for the given production and decay channels
        """
        for higgs in model_params.list_of_higgses:
            model_params.masses[higgs] = self.query_masses(higgs, query)
            model_params.xsecs[higgs] = self.query_xsec(higgs, channel, query)
            model_params.brs[higgs] = self.query_br(higgs, decay, channel, query)

    def use_hplus_xsec(self, query, channel, decay, model_params):
        """
        This function takes the input from create_model_params and uses mssm_xsec_tools to determine the masses,
        cross-sections and branchingratios for the given production and decay channels
        """
        for higgs in model_params.list_of_higgses:
            model_params.masses[higgs] = self.query_masses(higgs, query)
            model_params.xsecs[higgs] = self.query_xsec(higgs, channel, query)
            model_params.brs[higgs] = self.query_br(higgs, decay, channel, query)
        model_params.ttscale = self.query_ttscale('Hp', decay, channel, query)
        model_params.mA = self.query_mA(query)
        
    def query_masses(self, higgs, query):
        """
        Determine the mass of the higgs given as input. This function uses the
        mssm_xsec_tools.
        """     
        return query['higgses'][higgs]['mass']

    def query_xsec(self, higgs, channel, query):
        """
        Determine the cross-section of the specified production channel for a given higgs.
        This function uses the mssm_xsec_tools.
        For NeutralMSSM currently only 'ggH' and 'bbH' are supported.
        For Hhh currently only 'ggAToZhToLLTauTau', 'ggHTohhTo2Tau2B' and 'ggAToZhToLLBB' are supported.
        For Hplus currently only 'HH' and 'HW' are supported.
        """
        channels = {'ggH':'ggF', 'bbH':'santander', 'ggAToZhToLLBB':'ggF','ggAToZhToLLTauTau':'ggF', 'ggHTohhTo2Tau2B':'ggF', 'HH':'HH', 'HW':'HW'} 
        if channel not in channels:
            exit('ERROR: Production channel \'%s\' not supported'%channel)
        if self.uncert == '':
            return query['higgses'][higgs]['xsec'][channels[channel]]
        elif self.uncert[-1] == '+':
            return query['higgses'][higgs][self.uncert[:-1]][channels[channel]][1]
        elif self.uncert[-1] == '-':
            return query['higgses'][higgs][self.uncert[:-1]][channels[channel]][-1]
        else:
            exit("ERROR: uncertainty %s is not supported"%(self.uncert))

    def query_br(self, higgs, decay, channel, query):
        """
        Determine the branching ratio of the specified decay channel for a given higgs.
        This function uses the mssm_xsec_tools.
        For NeutralMSSM currently only htt, hbb and hmm are supported.
        For Hhh currently only Hhh*hbb*(hbb/htt/hmm) and AZh*hbb*ZLL and AZh*htt*Zbb are supported.
        For Hplus currently only BR(t->Hp+b) and BR(Hp->tau+nu) are supported.
        """
        brname = {'tt':'BR', 'bb':'BR-bb', 'mm':'BR-mumu', 'HTohhTo2Tau2B':'BR-hh', 'AToZhToLLTauTau':'BR-Zh', 'AToZhToLLBB':'BR-Zh', 'tHpb':'BR-tHpb', 'taunu':'BR-taunu'}
        if decay[1:] not in brname:
            exit('ERROR: Decay channel \'%s\' not supported'%decay)
        if self.ana_type=='Hhh' :
            if channel=='ggHTohhTo2Tau2B' :
                return str(query['higgses'][higgs][brname[channel[2:]]]*query['higgses']['h'][brname['bb']]*query['higgses']['h'][brname[decay[1:]]]*2) #factor 2: bbtautau or tautaubb
            elif channel=='ggAToZhToLLBB' :
                return str(query['higgses'][higgs][brname[channel[2:]]]*query['higgses']['h'][brname['bb']]*0.10099) #BR(Z->LL)=0.003363(ee)+0.003366(mumu)+0.003370(tautau)
            elif channel=='ggAToZhToLLTauTau' :
                return str(query['higgses'][higgs][brname[channel[2:]]]*query['higgses']['h'][brname['tt']]*0.10099) #BR(Z->LL)=0.003363(ee)+0.003366(mumu)+0.003370(tautau)
            elif channel=='bbH' :
                return query['higgses'][higgs][brname[decay[1:]]]
        elif self.ana_type=='Hplus':
            if 'HH' in channel :
                return str(query['higgses'][higgs][brname['tHpb']]*query['higgses'][higgs][brname['tHpb']]*query['higgses'][higgs][brname['taunu']]*query['higgses'][higgs][brname['taunu']])
            elif 'HW' in channel : 
               return str(2*(1-query['higgses'][higgs][brname['tHpb']]*query['higgses'][higgs][brname['taunu']])*query['higgses'][higgs][brname['tHpb']]*query['higgses'][higgs][brname['taunu']]) 
        else : 
            return query['higgses'][higgs][brname[decay[1:]]]

    def query_ttscale(self, higgs, decay, channel, query):
        """
        Determine the tt MC rescale factor.
        This function uses the hplus_xsec_tools.
        Its only used for Hplus.
        """
        brname = {'tHpb':'BR-tHpb', 'taunu':'BR-taunu'}
        if decay[1:] not in brname:
            exit('ERROR: Decay channel \'%s\' not supported'%decay)
        if self.ana_type=='Hplus':
            return str((1-query['higgses'][higgs][brname['tHpb']]*query['higgses'][higgs][brname['taunu']])*(1-query['higgses'][higgs][brname['tHpb']]*query['higgses'][higgs][brname['taunu']]))
        else : 
            return str(1.0)

    def query_mA(self, query):
        """
        Save the mass of the pseudoscalar A.
        Its only used for Hplus.
        """
        if self.ana_type=='Hplus':
            return str(query['massA'])
        else : 
            return str(-999)
