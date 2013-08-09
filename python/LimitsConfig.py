import ConfigParser

class configuration:
    def __init__(self, mode, config):
        self.config=ConfigParser.SafeConfigParser(allow_no_value=True)
        self.config.read(config)
        #read values from config
        self.periods=self.config.get(mode, 'periods').split()
        self.channels=self.config.get(mode, 'channel').split()
        self.categories={}
        self.categoryname={}
        self.input={}
        for channel in self.channels:
            self.categories[channel]={}
            for period in self.periods:
                self.categories[channel][period]=self.get_categories(channel, period, mode)
            try:
                self.categoryname[channel]=self.get_category_names(channel, mode)
            except ConfigParser.NoOptionError:
                pass
            self.input[channel]=self.config.get('input', channel)
    def get_categories(self, channel, period, mode):
        categories=self.config.get(mode, channel+'_categories_'+period)
        return categories.split()
    def get_category_names(self, channel, mode):
        names=self.config.get(mode, channel+'_names')
        return names.split()
