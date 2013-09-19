import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    #dataset = cms.string("CMS Preliminary,  H#rightarrow#tau#tau,  4.9 fb^{-1} at 7 TeV"),
    #dataset = cms.string("CMS Preliminary,  H#rightarrow#tau#tau,  19.4 fb^{-1} at 8 TeV"),
    dataset = cms.string("CMS Preliminary,  H#rightarrow#tau#tau,  4.9 fb^{-1} at 7 TeV, 19.7 fb^{-1} at 8 TeV"),
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
    max = cms.double(7.), ## 50
    ## min for plotting
    log = cms.int32(0), ## 1
    ## define verbosity level
    verbosity   = cms.uint32(0),
    ## define output label
    outputLabel = cms.string("significance"), 
    ## define masspoints for limit plot
    masspoints = cms.vdouble(range(110, 146, 5)),
    ## plot expected only
    expectedOnly = cms.bool(True),
)
