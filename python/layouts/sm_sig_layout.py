import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string(" Test #sqrt{s} = 7 TeV, L = 17 fb^{-1}"),
    #dataset = cms.string(", #sqrt{s} = 7 TeV, H #rightarrow #tau #tau, L = 4.6 fb^{-1}"),
    ## x-axis title
    xaxis = cms.string("m_{H} [GeV]"),
    ## x-axis title
    yaxis = cms.string("Significance"),
    ## plot expected only
    expectedOnly = cms.bool(True),
    ## is this mssm?
    mssm = cms.bool(False),
    ## print to png
    png  = cms.bool(True),
    ## print to pdf
    pdf  = cms.bool(True),
    ## print to txt
    txt  = cms.bool(True),
    ## print to root
    root = cms.bool(True),
    ## min for plotting
    min = cms.double(0.1), ## 0.05
    ## max for plotting
    max = cms.double(50.), ## 50
    ## min for plotting
    log = cms.int32(1),
    ## define verbosity level
    verbosity   = cms.uint32(2),
    ## define output label
    outputLabel = cms.string("significance"), 
    ## define masspoints for limit plot
    masspoints = cms.vdouble(
    110.
   ,115.
   ,120.
   ,125.
   ,130.
   ,135.
   ,140.
   ,145.
  ),
)
