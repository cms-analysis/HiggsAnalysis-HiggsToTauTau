#!/usr/bin/env python
import re
import pprint
import copy
import sqlite3

categories = {
    '00':'0jet_low',
    '01':'0jet_high',
    '02':'boost_low',
    '03':'boost_high',
    '04':'2jet',
    '05':'vbf',
    '06':'btag_low',
    '07':'btag_high'
    }

class Conf(object):
    def __init__(self, str, cfgFile):
        self.cfgFile = cfgFile
        self.str = str
        spl = str.split()
        self.stat = None
        if len(spl)==2:
            self.name, self.type = spl[:2]
        elif len(spl)==3:
            self.name, self.type = spl[:2]
            self.stat = spl[2]
        else:
            raise ValueError('Conf: bad line:' + str)

    def __str__(self):
        thestr =  '{name:50} {type:20}'.format(name=self.name,
                                               type=self.type)
        if self.stat:
            thestr = '\t'.join([thestr, str(self.stat)])
        return thestr


class Val(object):
    def __init__(self, str, cfgFile):
        self.cfgFile = cfgFile
        self.str = str
        spl = str.split()
        if len(spl) == 4:
            self.category = spl[0]
            self.processes = spl[1].split(',')
            self.uncertainty = spl[2]
            self.value = float( spl[3] )
        else:
            raise ValueError('Val: bad line:'+str)

    def __str__(self):
        thestr =  '{category:50} {processes:30} {uncertainty:50} {value:5.2f}'.format(
            category=self.category,
            processes=','.join(self.processes),
            uncertainty=self.uncertainty,
            value=self.value)
        return thestr
        
     
class ConfigFile(list):

    pattern = re.compile('.*(\d+)TeV-(\d+).*')
    
    def readLines(self, fnam):
        self.name = fnam
        file = open(fnam)
        self.channel = fnam.split('/')[-2]
        m = ConfigFile.pattern.match(fnam)
        if m:
            self.sqrts = m.group(1)
            self.category = categories[m.group(2)]
        else:
            raise ValueError('ConfigFile: cannot parse filename to find the sqrts:', fnam)
        return [line.rstrip() for line in file if not line.startswith('#') and not line.find('#'*10)>-1 \
                and not line.rstrip()=='']

    def __eq__(self, other):
        return self.channel == other.channel and \
               self.sqrts == other.sqrts and \
               self.category == other.category
    
    def __str__(self):
        thestrs = [ '{name}, sqrt(s)={sqrts} TeV, channel={channel}, category={category}'.format(
            name=self.name,
            sqrts=self.sqrts,
            channel=self.channel,
            category=self.category
            ) ]
        thestrs.extend( str(item) for item in self )
        return '\n'.join(thestrs)
    

class ValsFile(ConfigFile):
    def __init__(self, fnam):
        super(ValsFile, self).__init__( Val(line, self) for line in self.readLines(fnam) )        
        
        
class ConfFile(ConfigFile):
    def __init__(self, fnam):
        super(ConfFile, self).__init__( Conf(line, self) for line in self.readLines(fnam) )


class Info(object):
    def __init__(self, dictlike=None):
        if dictlike:
            self.__dict__.update(dictlike)
    def __str__(self):
        return str(self.__dict__)


class FlatInfo(list):

    def load(self, conffiles, valfiles):
        for valfile in valfiles:
            conffilecandidates = [conffile for conffile in conffiles if valfile==conffile]
            if len(conffilecandidates) > 1:
                for c in conffilecandidates:
                    print c
                raise ValueError('several candidate configuration files found')
            elif len(conffilecandidates) == 0:
                print valfile
                for conffile in conffiles:
                    print conffile
                raise ValueError('no corresponding configuration file was found.')                
            conffile = conffilecandidates[0]
            # building row info
            info = Info()
            info.channel = valfile.channel
            info.sqrts = valfile.sqrts
            info.category = valfile.category
            for val in valfile:
                info.value = val.value
                info.uncertainty = val.uncertainty
                uncconfcandidates = [conf for conf in conffile if conf.name == info.uncertainty ]
                if len(uncconfcandidates) > 1:
                    for c in uncconfcandidates:
                        print c
                    raise ValueError('several uncertainty configuration found for '+info.uncertainty)
                elif len(uncconfcandidates) == 0:
                    print valfile
                    print 
                    print conffile
                    raise ValueError('no corresponding uncertainty configuration was found for ' + info.uncertainty)
                uncconf = uncconfcandidates[0]
                # print uncconf
                info.type = uncconf.type
                info.stat = uncconf.stat
                # print val.processes
                for process in val.processes:
                    pinfo = copy.copy(info)
                    pinfo.process = process
                    self.append(pinfo)

    def loadFromDB(self, db, selstr):
        del self[0:]
        res = db.execute(selstr).fetchall()
        for row in res:
            self.append( Info(row) )

    def select(self, var, sel):
        sellines = [ line for line in self if getattr(line, var)==sel]
        return FlatInfo(sellines)

    def __str__(self):
        theStrs = [str(i) for i in self]
        return '\n'.join(theStrs)
            
conn = sqlite3.connect(':memory:')
conn.row_factory = sqlite3.Row
conn.text_factory = str
cursor = conn.cursor()

def createDB(flatinfo):
    created = False
    for i in flatinfo:
        if not created:
            cursor.execute('''CREATE TABLE dc (category text, process text, stat text, channel text, sqrts text, uncertainty text, type text, value real)''')
            created = True
            
        insertStr = "INSERT INTO dc VALUES ('{category}', '{process}', '{stat}', '{channel}', '{sqrts}', '{uncertainty}', '{type}', {value:8.5})".format(
            category = i.category,
            process = i.process,
            stat = i.stat,
            channel = i.channel,
            sqrts = i.sqrts,
            uncertainty = i.uncertainty,
            type = i.type,
            value = i.value
            )
        # print insertStr
        cursor.execute(insertStr)
    conn.commit()
    return cursor


def correlations(db):
    
    uncs = FlatInfo()
    uncs.loadFromDB(db, "select distinct(uncertainty) from dc order by uncertainty")
    print uncs
    for res in uncs:
        unc = res.uncertainty
        print '-'*12, unc
        fi = FlatInfo()
        fi.loadFromDB(db, "select * from dc where uncertainty='{unc}' order by category".format(unc=unc))
        print fi
        
    
    
##     for i in uncs:
##         catchanyear = FlatInfo()
##         catchanyear.loadFromDB(db, "select distinct(uncertainty) from dc order by uncertainty")
    
        
    

if __name__ == '__main__':

    import sys
    from optparse import OptionParser

    usage = """
    %prog [options] list_of_files

    list_of_files should be a list of .conf and .vals files.
    You might have to make sure that they correspond to each other.

    Example:
    
    cd CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau
    %prog setup/mt/unc-sm-*


    By default, this script prints a basic summary table.
    You can also run the script in interactive mode, and browse the datacard
    information using SQL commands.
    """
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()

    files = args
    if len(files)<2:
        print 'you need to provide at least one .conf file and its corresponding .vals file'
        sys.exit(1)

    conffiles = [f for f in files if f.endswith('.conf')]
    valsfiles = [f for f in files if f.endswith('.vals')]

    confs = []
    for f in conffiles:
        confs.append( ConfFile(f) )
    valss = []
    for f in valsfiles:
        valss.append( ValsFile(f) )

    flatinfo = FlatInfo()
    flatinfo.load(confs, valss)
    db = createDB(flatinfo)
    selinfo = FlatInfo()
    selinfo.loadFromDB(db, "select * from dc")
    # print selinfo
    correlations(db)

    # selinfo.loadFromDB(db, "select category, uncertainty, value, sqrts from dc where sqrts==8 and category like '%0jet%' order by category"); print selinfo
