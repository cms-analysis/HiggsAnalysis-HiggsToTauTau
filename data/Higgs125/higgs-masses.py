import os
from HiggsAnalysis.HiggsToTauTau.tools.mssm_xsec_tools import mssm_xsec_tools

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3 ...", description="This is a script to print out txt files containing tanb and the masses of the neutral higgs bosons of a given MSSM Higgs model.")
cgroup = OptionGroup(parser, "")
cgroup.add_option("--model", dest="model", default="mhmax-mu+200", type="string",
                  help="The model for which you will look up the values. [Default: \"mhmax-mu+200\"]")
cgroup.add_option("--verbosity", dest="verbosity", default=False, action="store_true",
                  help="Run in verbosity mode. [Default: False]")
parser.add_option_group(cgroup)
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

path = "auxiliaries/models/out.{MODEL}-8TeV-tanbHigh-nnlo.root".format(MODEL=options.model)
#path = "auxiliaries/models/out.{MODEL}-8TeV-tanbAll-nnlo.root".format(MODEL=options.model)
if options.model=="lowmH" :
    for MUE in range(300, 3101, 20) :
        file_name = "{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/data/Higgs125/{MODEL}/higgs_{MASS}.dat".format(CMSSW_BASE=os.environ['CMSSW_BASE'],MODEL=options.model,MASS=MUE)
        print "writing file:", file_name
        file = open(file_name,'w')
        for tanb in range(15, 96) :
            mssm_scan = mssm_xsec_tools("{CMSSW_BASE}/src/{PATH}".format(CMSSW_BASE=os.environ['CMSSW_BASE'], PATH=path))
            htt_query = mssm_scan.query(MUE, tanb/10., "NeutralMSSM") ; mh = htt_query['higgses']['h']['mass'] ; mH = htt_query['higgses']['H']['mass'] ; mA = htt_query['higgses']['A']['mass']
            if options.verbosity :
               print "%f \t%f \t%f \t%f \n" % (tanb/10., mh, mA, mH) ;
            file.write("%f \t%f \t%f \t%f \n" % (tanb/10., mh, mA, mH))	
        file.close()
elif options.model=="low-tb-high" :
    for mA in range(150, 501, 10) :
        file_name = "{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/data/Higgs125/{MODEL}/higgs_{MASS}.dat".format(CMSSW_BASE=os.environ['CMSSW_BASE'],MODEL=options.model,MASS=mA)
        print "writing file:", file_name
        file = open(file_name,'w')
        for tanb in range(5, 96) :
            mssm_scan = mssm_xsec_tools("{CMSSW_BASE}/src/{PATH}".format(CMSSW_BASE=os.environ['CMSSW_BASE'], PATH=path))
            htt_query = mssm_scan.query(mA, tanb/10., "NeutralMSSM") ; mh = htt_query['higgses']['h']['mass'] ; mH = htt_query['higgses']['H']['mass'] ; mA = htt_query['higgses']['A']['mass']
            if options.verbosity :
               print "%f \t%f \t%f \t%f \n" % (tanb/10., mh, mA, mH) ;
            file.write("%f \t%f \t%f \t%f \n" % (tanb/10., mh, mA, mH))	
        file.close()
else:
    for mA in [90, 100, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000] :
        file_name = "{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/data/Higgs125/{MODEL}/higgs_{MASS}.dat".format(CMSSW_BASE=os.environ['CMSSW_BASE'],MODEL=options.model,MASS=mA)
        print "writing file:", file_name
        file = open(file_name,'w')
        for tanb in range(5, 601) :
            mssm_scan = mssm_xsec_tools("{CMSSW_BASE}/src/{PATH}".format(CMSSW_BASE=os.environ['CMSSW_BASE'], PATH=path))
            htt_query = mssm_scan.query(mA, tanb/10., "NeutralMSSM") ; mh = htt_query['higgses']['h']['mass'] ; mH = htt_query['higgses']['H']['mass'] 
            if options.verbosity :
                print "%f \t%f \t%f \t%f \n" % (tanb/10., mh, mA, mH) ;
            file.write("%f \t%f \t%f \t%f \n" % (tanb/10., mh, mA, mH))	
        file.close()
