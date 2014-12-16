import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string("CMS, H#rightarrow#tau#tau, 19.7 fb^{-1} at 8 TeV"),	
    #dataset = cms.string("CMS Preliminary, H #rightarrow #tau #tau, 18.3 fb^{-1} at 8 TeV"),
    ## extra labels (below legend)
    #extra = cms.string("A#rightarrowZh profiled"),	
    #extra = cms.string("gg#rightarrow#phi bb set to zero"),
    ## x-axis title
    xaxis = cms.string("m_{H} [GeV]"),
    ## x-axis title
    yaxis = cms.string("95% CL limit on #sigma(bbA#rightarrowbb#tau#tau)#timesBR [pb]"),
    ## min for plotting
    min = cms.double(0.01),
    ## max for plotting
    max = cms.double(5.), ## 200. 100000.
    ## min for plotting
    log = cms.int32(0),
    ## print to png
    png = cms.bool(True),
    ## print to pdf
    pdf = cms.bool(True),
    ## print to txt
    txt = cms.bool(True),
    ## print to root
    root = cms.bool(True),
    ## define verbosity level
    verbosity = cms.uint32(0),
    ## define output label
    outputLabel = cms.string(""), 
    ## define masspoints for limit plot
    masspoints = cms.vdouble(
   25.
   ,30.
   ,35.
   ,40.
   ,45.
   ,50.
   ,55.
   ,60.
   ,65.
   ,70.
   ,75.
   ,80.
    ),
    ## SM like limit without the line at sigma=1
    mssm_nolog = cms.bool(True),
    ## plot expected only
    expectedOnly = cms.bool(True),
    ## mass label for the injected signal print band in different layout for signal injected
    injectedMass=cms.string("125"),    
    ## print band in different layout for signal injected
    injected=cms.bool(False),
)
