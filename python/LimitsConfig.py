import ConfigParser
import os

class configuration:
    def __init__(self, mode, config):
        self.config=ConfigParser.SafeConfigParser(allow_no_value=True)
        self.config.read(["{CMSSW}/src/HiggsAnalysis/HiggsToTauTau/limits.config".format(CMSSW=os.getenv('CMSSW_BASE')), config])
        #read values from config
        self.periods=self.config.get(mode, 'periods').split()
        self.channels=self.config.get(mode, 'channel').split()
        self.categories={}
        self.categoryname={}
        self.inputs={}
        for channel in self.channels:
            self.categories[channel]={}
            for period in self.periods:
                self.categories[channel][period]=self.get_categories(channel, period, mode)
            self.categoryname[channel]=self.get_category_names(channel, mode)
            self.inputs[channel]=self.config.get('inputs', channel)
        if mode == 'sm':
            self.bbbcat={}
            self.bbbproc={}
            self.bbbthreshold=self.config.get('bbb-'+mode,'threshold')
            for channel in self.channels:
                self.bbbcat[channel]={}
                for period in self.periods:
                    self.bbbcat[channel][period]=self.get_bbb_categories(channel, period, mode)
                self.bbbproc[channel]=self.get_bbb_processes(channel, mode)

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
