import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string("CMS,  H#rightarrow#tau#tau,  4.9 fb^{-1} at 7 TeV, 19.7 fb^{-1} at 8 TeV"),
    ## x-axis title
    xaxis = cms.string("Signal Strength"),
    ## x-axis title
    yaxis = cms.string("#Delta NLL"),
    ## min for plotting (for fine tuning)
    min = cms.double(0.),
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
    ## input model - if no model specified it should be "Test" - upper and lower case sensitive
    model = cms.string("Test"),
    ## define output label
    outputLabel = cms.string("likelihood-scan"),
    ## define masspoints for limit plot
    masspoints = cms.vdouble(125),
)
