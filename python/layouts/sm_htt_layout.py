import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string(" ICHEP 2012, H #rightarrow #tau #tau, L = 10.0 fb^{-1}"),
    #dataset = cms.string(" Preliminary 2012, H #rightarrow #tau #tau, L = 12.0 fb^{-1}"),
    #dataset = cms.string(" Preliminary 2011, H #rightarrow #tau #tau, L = 4.9 fb^{-1}"),
    #dataset = cms.string(", Preliminary, H #rightarrow #tau #tau, L = 17 fb^{-1}"),
    ## x-axis title
    xaxis = cms.string("m_{H} [GeV]"),
    ## x-axis title
    yaxis = cms.string("95% CL limit on #sigma/#sigma_{SM}"),
    ## plot expected only
    #expectedOnly = cms.bool(True),
    ## print band for signal injected
    #injected=cms.bool(True),
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
    min = cms.double(0.),
    ## max for plotting
    max = cms.double(5.), ##5.
    ## min for plotting
    log = cms.int32(0),
    ## define verbosity level
    verbosity   = cms.uint32(2),
    ## define output label
    outputLabel = cms.string("limit"),
    ## define masspoints for limit plot
    masspoints = cms.vdouble(range(110, 146, 5))
    #masspoints = cms.vdouble([125])
)
