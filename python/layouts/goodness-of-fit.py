import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string(" Preliminary, H #rightarrow #tau #tau, L=24.3 fb^{-1}"),
    ## x-axis title
    xaxis = cms.string("Goodness of Fit"),
    ## x-axis title
    yaxis = cms.string("Number of Toys"),
    ## min for plotting (for fine tuning)
    min = cms.double(0.),
    ## max for plotting (for fine tuning)
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
    verbosity = cms.uint32(1),
    ## define output label
    outputLabel = cms.string("goodness-of-fit"),
    ## define masspoints for limit plot
    masspoints = cms.vdouble(125),
)
