import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string("Preliminary, #sqrt{s}=7-8 TeV, L = 24.3 fb^{-1}, H #rightarrow #tau #tau"),
    ## x-axis title
    xaxis = cms.string("r_{V}"),
    ## x-axis title
    yaxis = cms.string("r_{F}"),
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
    verbosity = cms.uint32(0),
    ## define output label
    outputLabel = cms.string("scan"),
    ## define masspoints for limit plot
    masspoints = cms.vdouble(125),
    ## make a temperature plot?
    temp = cms.bool(False),
    ## define physics-model
    model = cms.string("RV-RF"),
    ## max for plotting (for fine tuning)
    xmaxs = cms.VPSet(
    cms.PSet(mass = cms.double( 125.), max = cms.double(-1.)),
    ),    
)
