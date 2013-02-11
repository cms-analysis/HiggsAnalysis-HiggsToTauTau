import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    #dataset = cms.string(", Preliminary 2012, H #rightarrow #tau #tau, L = 19.4 fb^{-1}"),
    dataset = cms.string(", Preliminary, H #rightarrow #tau #tau, L = 24.3 fb^{-1}"),
    #dataset = cms.string(", Preliminary 2011, H #rightarrow #tau #tau, L = 4.9 fb^{-1}"),
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
    outputLabel = cms.string("limit"),
    ## define masspoints for limit plot
    masspoints = cms.vdouble(range(110, 146, 5)),
    ## plot expected only
    expectedOnly = cms.bool(False),
    ## print band in different layout for signal injected
    injected=cms.bool(False),
    ## print band in different layout if SM 125GeV Higgs has been added to Background
    higgsBG=cms.bool(False),
)
