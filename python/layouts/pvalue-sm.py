import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string("Preliminary, #sqrt{s}=7-8 TeV, L = 24.3 fb^{-1}, H #rightarrow #tau #tau"),
    ## x-axis title
    xaxis = cms.string("m_{H} [GeV]"),
    ## x-axis title
    yaxis = cms.string("Local p-value"),
    ## indicate that this is bestfit
    bestfit = cms.bool(True),
    ## print to png
    png  = cms.bool(True),
    ## print to pdf
    pdf  = cms.bool(True),
    ## print to txt
    txt  = cms.bool(True),
    ## print to root
    root = cms.bool(True),
    ## min for plotting
    min = cms.double(1e-8),
    ## max for plotting
    max = cms.double(1.),
    ## min for plotting
    log = cms.int32(1),
    ## define verbosity level
    verbosity   = cms.uint32(0),
    ## define output label
    outputLabel = cms.string("p-value"),
    ## define masspoints for limit plot
    masspoints = cms.vdouble(range(110, 146, 5))
)
