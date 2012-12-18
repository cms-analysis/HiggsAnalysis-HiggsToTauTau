import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string(", Preliminary, H #rightarrow #tau #tau, L = 17 fb^{-1}"),
    ## x-axis title
    xaxis = cms.string("m_{H} [GeV]"),
    ## x-axis title
    yaxis = cms.string("95% CL limit on #sigma/#sigma_{SM}"),
    ## min for plotting
    min = cms.double(0.),
    ## max for plotting
    max = cms.double(-1.),
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
    ## define output label for root file
    outputLabel = cms.string("limits"),
    ## define masspoints for limit plot
    masspoints = cms.vdouble(range(110, 146, 5))
    #masspoints = cms.vdouble([125])
    ## plot expected only
    #expectedOnly = cms.bool(True),
    ## print band for signal injected
    #injected=cms.bool(True),

)
