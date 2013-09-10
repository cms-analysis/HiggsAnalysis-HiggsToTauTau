import os
from HiggsAnalysis.HiggsToTauTau.tools.mssm_xsec_tools import mssm_xsec_tools

path = "auxiliaries/models/out.mhmax-mu+200-8TeV-tanbHigh-nnlo.root"
for mA in [90, 100, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000] :
    file_name = "{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/data/Higgs125/higgs_{MASS}.dat".format(CMSSW_BASE=os.environ['CMSSW_BASE'],MASS=mA)
    print "writing file:", file_name
    file = open(file_name,'w')
    for tanb in range(600) :
        mssm_scan = mssm_xsec_tools("{CMSSW_BASE}/src/{PATH}".format(CMSSW_BASE=os.environ['CMSSW_BASE'], PATH=path))
        htt_query = mssm_scan.query(mA, tanb/10.) ; mh = htt_query['higgses']['h']['mass'] ; mH = htt_query['higgses']['H']['mass']
        print "%f \t%f \t%f \t%f \n" % (tanb/10., mh, mA, mH) ; file.write("%f \t%f \t%f \t%f \n" % (tanb/10., mh, mA, mH))	
    file.close()
