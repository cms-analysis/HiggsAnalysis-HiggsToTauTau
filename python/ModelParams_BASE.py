from HiggsAnalysis.HiggsToTauTau.tools.mssm_xsec_tools import mssm_xsec_tools
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
    The main function to be used for creation of the MODEL_PARAMS is 'create_model_params'
    """
    def __init__(self, mA, tanb):
        self.mA = mA
        self.tanb = tanb
    
    def create_model_params(self, period, channel, decay, mu, pdf, modelpath, modeltype='mssm_xsec'):
        """
        Main function to be used for creating a object of type MODEL_PARAMS for a given period,
        production channel, decay channel and model.
        periode is one of '7TeV', '8TeV'
        channel is of type gg[h,H,A]
        decay is of type [h,H,A]tt
        mu and pdf specify the uncertainties (scale and pdf) to be taken into account. Allowed values are +1,-1,0
        +1 and -1 stand for an plus/minus variation of the uncertainty. 0 specifies that the uncertainty is not taken into account.
        modelpath corresponds to the file to be used for the model specified in modeltype
          - feyn_higgs_mssm : modelpath is the name of the model to be used (e.g. mhmax)
          - mssm_xsec_tools : modelpath is the name of the model to be used including uncerts (e.g mhmax-mu+200)
        modeltype can be 'mssm_xsec' or 'feyn_higgs'
        """
        self.mu = float(mu)
        self.pdf = float(pdf)
        model_params = MODEL_PARAMS()
        if modeltype == 'feyn_higgs':
            self.use_feyn_higgs(modelpath, period, channel, decay, model_params)
        elif modeltype == 'mssm_xsec':
            if float(self.tanb) <= 1:
                tanbregion = 'tanbLow'
            else:
                tanbregion = 'tanbHigh'
            if modelpath == '':
                mssm_xsec_tools_path = getenv('CMSSW_BASE')+'/src/HiggsAnalysis/HiggsToTauTau/data/out.mhmax-mu+200-'+period+'-'+tanbregion+'-nnlo.root'
            else:
                mssm_xsec_tools_path = getenv('CMSSW_BASE')+'/src/HiggsAnalysis/HiggsToTauTau/data/out.'+modelpath+'-'+period+'-'+tanbregion+'-nnlo.root'
            self.use_mssm_xsec(mssm_xsec_tools_path, channel, decay, model_params)
        else:
            exit('ERROR: modeltype \'%s\' not supported'%modeltype)
        return model_params

    def use_feyn_higgs(self, path, period, channel, decay, model_params):
        """
        This functions takes the input from create_model_params and uses feyn_higgs_mssm to determine the masses, cross-sections
        and branchingratios for the given production and decay channels
        """
        scan = feyn_higgs_mssm(self.mA, self.tanb, 'sm', path, period) #consider using variable for 'sm', 'mssm'
        for higgs in model_params.list_of_higgses:
            if higgs == 'A': model_params.masses[higgs] = self.mA
            if higgs == 'h': model_params.masses[higgs] = scan.get_mh()
            if higgs == 'H': model_params.masses[higgs] = scan.get_mH()
            xsecs = scan.get_xs(channel[:-1]+higgs)
            model_params.xsecs[higgs] = xsecs
            brs = scan.get_br(higgs+decay[1:])
            model_params.brs[higgs] = brs

    def use_mssm_xsec(self, path, channel, decay, model_params):
        """
        This function takes the imput from create_model_params and uses mssm_xsec_tools to determine the masses,
        cross-sections and branchingratios for the given production and decay channels
        """
        for higgs in model_params.list_of_higgses:
            model_params.masses[higgs] = self.query_masses(higgs, path)
            model_params.xsecs[higgs] = self.query_xsec(higgs, channel, path)
            model_params.brs[higgs] = self.query_br(higgs, decay, path)
        
    def query_masses(self, higgs, path):
        """
        Determine the mass of the higgs given as input. This function uses the
        mssm_xsec_tools.
        """
        if higgs == 'A': return self.mA
        scan = mssm_xsec_tools(path)
        htt_query = scan.query(self.mA, self.tanb)
        return htt_query['higgses'][higgs]['mass']

    def query_xsec(self, higgs, channel, path):
        """
        Determine the cross-section of the specified production channel for a given higgs.
        This function uses the mssm_xsec_tools.
        Currently only 'ggh', 'santander' and 'bbh' are supported
        """
        channels = {'ggh':'ggF', 'santander':'santander', 'bbh':'bbh'}
        if channel not in channels:
            exit('ERROR: Production channel \'%s\' not supported'%channel)
        scan = mssm_xsec_tools(path)
        htt_query = scan.query(self.mA, self.tanb)
        if self.mu == 0 and self.pdf == 0:
            return htt_query['higgses'][higgs]['xsec'][channels[channel]]
        elif abs(self.pdf) == 1 and self.mu == 0:
            return htt_query['higgses'][higgs]['pdf'][channels[channel]][self.pdf]
        elif abs(self.mu) == 1 and self.pdf == 0:
            return htt_query['higgses'][higgs]['mu'][channels[channel]][self.mu]
        else:
            exit("ERROR: mu = %i and pdf = %i is not supported"%(self.mu, self.pdf))

    def query_br(self, higgs, decay, path):
        """
        Determine the branching ratio of the specified decay channel for a given higgs.
        This function uses the mssm_xsec_tools.
        Currently only htt, hbb and hmm are supported.
        """
        brname = {'tt':'BR','bb':'BR-bb', 'mm' : 'BR-mumu'}
        if decay[1:] not in brname:
            exit('ERROR: Decay channel \'%s\' not supported'%decay)
        scan = mssm_xsec_tools(path)
        htt_query = scan.query(self.mA, self.tanb)
        return htt_query['higgses'][higgs][brname[decay[1:]]]
