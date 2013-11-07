import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string("CMS,  H#rightarrow#tau#tau,  4.9 fb^{-1} at 7 TeV, 19.7 fb^{-1} at 8 TeV"),
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
    ## log for plotting
    log = cms.int32(0),
    ## define verbosity level
    verbosity   = cms.uint32(0),
    ## define output label
    outputLabel = cms.string("mass_scan"),
    ## define masspoints for limit plot
    masspoints = cms.vdouble(range(110, 146, 5))
#    masspoints = cms.vdouble(range(110, 146, 1))
)
