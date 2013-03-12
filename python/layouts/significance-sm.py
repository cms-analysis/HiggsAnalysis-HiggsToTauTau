import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string("Preliminary, #sqrt{s}=7-8 TeV, L = 24.3 fb^{-1}, H #rightarrow #tau #tau"),
    ## x-axis title
    xaxis = cms.string("m_{H} [GeV]"),
    ## x-axis title
    yaxis = cms.string("Significance"),
    ## plot expected only
    #expectedOnly = cms.bool(True),
    ## plot with dedicated significance layout for low significance, w/o bands
    significance = cms.bool(True),
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
    min = cms.double(0.), ## 0.05
    ## max for plotting
    max = cms.double(7..), ## 50
    ## min for plotting
    log = cms.int32(0), ## 1
    ## define verbosity level
    verbosity   = cms.uint32(0),
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
