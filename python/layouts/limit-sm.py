import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    #dataset = cms.string("CMS Preliminary,  H#rightarrow#tau#tau,  4.9 fb^{-1} at 7 TeV"),
    #dataset = cms.string("CMS Preliminary,  H#rightarrow#tau#tau,  19.4 fb^{-1} at 8 TeV"),
    dataset = cms.string("CMS Preliminary,  H#rightarrow#tau#tau,  4.9 fb^{-1} at 7 TeV, 19.7 fb^{-1} at 8 TeV"),
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
    ## mass label for the injected signal print band in different layout for signal injected
    injectedMass=cms.string("125"),    
    ## print band in different layout for signal injected
    injected=cms.bool(False),
    ## print band in different layout if SM 125GeV Higgs has been added to Background
    higgsBG=cms.bool(False),
)
