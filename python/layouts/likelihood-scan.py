import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string(", Preliminary, H #rightarrow #tau #tau, L = 17 fb^{-1}"),
    ## x-axis title
    xaxis = cms.string("Signal Strength (in multiples of #sigma(SM))"),
    ## x-axis title
    yaxis = cms.string("NLL"),
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
    masspoints = cms.vdouble(
    110
   ,115
   ,120
   ,125
   ,130
   ,135
   ,140
   ,145
    ),
)
