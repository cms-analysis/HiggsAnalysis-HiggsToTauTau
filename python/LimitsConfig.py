import ConfigParser
import os
import sys

class configuration:
    def __init__(self, mode, config, mtsoft=False):
        self.config=ConfigParser.SafeConfigParser(allow_no_value=True)
        config_read=self.config.read(["{CMSSW}/src/HiggsAnalysis/HiggsToTauTau/limits.config".format(CMSSW=os.getenv('CMSSW_BASE')), config])
        if len(config_read) == 1 and config:
            sys.stderr.write("ERROR in LimitsConfig: Specified configuration file does not exist or is not readable.\n")
            exit(1) 
        #read values from config
        self.periods=self.config.get(mode, 'periods').split()
        self.channels=self.config.get(mode, 'channels').split()
        self.categories={}
        self.categoryname={}
        self.inputs={}
        self.unblind=self.config.has_option(mode,'unblind')
        if self.config.has_option(mode, 'blind'):
            self.unblind = False
        self.comb_periods=self.config.get('combination', 'periods').split()
        self.comb_channels=self.config.get('combination', 'channels_'+mode).split()
        self.comb_categories=self.config.get('combination', 'categories_'+mode).split()
        for channel in self.channels:
            self.categories[channel]={}
            for period in self.periods:
                self.categories[channel][period]=self.get_categories(channel, period, mode)
            self.categoryname[channel]=self.get_category_names(channel, mode)
            self.inputs[channel]=self.config.get('inputs', channel)
        if mtsoft and 'mt' in self.channels and mode == 'sm':
            self.categoryname['mt'] = self.categoryname['mt']+self.get_category_names('mt_soft', 'sm')
            for period in self.periods:
                self.categories['mt'][period] = self.categories['mt'][period]+self.get_categories('mt_soft', period, 'sm')
            self.inputs['mt_soft']=self.config.get('inputs', 'mt_soft')
        self.bbbcat={}
        self.bbbproc={}
        self.bbbthreshold={}
        for channel in self.channels:
            self.bbbthreshold[channel]=self.config.get('bbb-'+mode,channel+'_threshold')
            self.bbbcat[channel]={}
            for period in self.periods:
                self.bbbcat[channel][period]=self.get_bbb_categories(channel, period, mode)
            self.bbbproc[channel]=self.get_bbb_processes(channel, mode)
        if mtsoft and 'mt' in self.channels and mode == 'sm':
            self.bbbproc['mt'] = self.bbbproc['mt']+self.get_bbb_processes('mt_soft', mode)
            for period in self.periods:
                self.bbbcat['mt'][period] = self.bbbcat['mt'][period]+self.get_bbb_categories('mt_soft', period, mode)


    def get_categories(self, channel, period, mode):
        categories=self.config.get(mode, channel+'_categories_'+period)
        return categories.split()
    def get_category_names(self, channel, mode):
        names=self.config.get(mode, channel+'_names')
        return names.split()
    def get_bbb_categories(self, channel, period, mode):
        categories=self.config.get('bbb-'+mode, channel+'_categories_'+period)
        return categories.split()
    def get_bbb_processes(self, channel, mode):
        process=self.config.get('bbb-'+mode, channel+'_processes')
        return process.split()
