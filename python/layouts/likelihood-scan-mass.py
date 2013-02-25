import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string(" Preliminary, H #rightarrow #tau #tau, L = 24.3 fb^{-1}"),
    ## x-axis title
    xaxis = cms.string("m_{H} [GeV]"),
    ## x-axis title
    yaxis = cms.string("#Delta NLL"),
    ## print to png
    png  = cms.bool(True),
    ## print to pdf
    pdf  = cms.bool(True),
    ## print to txt
    txt  = cms.bool(True),
    ## print to root
    root = cms.bool(True),
    ## min for plotting
    min = cms.double(0.),
    ## max for plotting
    max = cms.double(4),
    ## min for plotting
    log = cms.int32(0),
    ## define verbosity level
    verbosity   = cms.uint32(0),
    ## define output label
    outputLabel = cms.string("mass_scan"),
    ## define masspoints for limit plot
    #masspoints = cms.vdouble(range(110, 146, 5))
    masspoints = cms.vdouble(range(110, 146, 1))
)
