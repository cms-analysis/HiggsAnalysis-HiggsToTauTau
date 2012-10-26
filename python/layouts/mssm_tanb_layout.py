import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    #dataset = cms.string("Preliminary #sqrt{s} = 7 TeV, L = 1.6 fb^{-1}"),
    dataset = cms.string("Preliminary, #sqrt{s} = 7+8 TeV, L = 17 fb^{-1}"),
    ## x-axis title
    xaxis = cms.string("m_{A} [GeV]"),
    ## x-axis title
    yaxis = cms.string("#bf{tan#beta}"),
    ## is this mssm?
    mssm = cms.bool(True),
    ## print to png
    png  = cms.bool(True),
    ## print to pdf
    pdf  = cms.bool(True),
    ## print to txt
    txt  = cms.bool(True),
    ## print to root
    root = cms.bool(True),
    ## print the +/- 2 sigma band?
    outerband = cms.bool(True),
    ## min for plotting
    min = cms.double(0.),
    ## max for plotting
    max = cms.double(50.),
    ## min for plotting
    log = cms.int32(0),
    ## define verbosity level
    verbosity   = cms.uint32(2),
    ## define output label
    outputLabel = cms.string("mA-tanb"),
    ## Set true if we want to skip observed limits
    expectedOnly = cms.bool(True),
    ## print mh=125GeV bands?
    higgs125_bands = cms.bool(False),
    ## define masspoints for limit plot
    masspoints = cms.vdouble(
    #90.
    100.
   ,120.
   ,130.
   ,140.
   ,160.
   ,180.
   ,200.
   ,250.  
   ,300.
   ,350.
   ,400.
   ,450.
   ,500.
   ,600.
   ,700.
   ,800.
   ,900.
   ,1000.
  ),
)
