import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string("Preliminary #Phi #rightarrow #tau #tau, 17 fb^{-1}  #sqrt{s}=7+8 TeV"),
    #dataset = cms.string("Preliminary 1.6 fb^{-1}  #sqrt{s}=7 TeV"),
    ## x-axis title
    xaxis = cms.string("m_{A} [GeV]"),
    ## x-axis title
    yaxis = cms.string("#sigma(pp#rightarrow#phi#rightarrow#tau#tau) [pb]"),
    ## is this mssm?
    mssm = cms.bool(True),
    ## center of mass energy (7, 8, 78 for combination)
    ecms = cms.int32(78),
    ## print to png
    png  = cms.bool(True),
    ## print to pdf
    pdf  = cms.bool(True),
    ## print to txt
    txt  = cms.bool(True),
    ## print to root
    root = cms.bool(True),
    ## min for plotting
    min = cms.double(-0.2),
    ## max for plotting
    max = cms.double(4.),
    ## min for plotting
    log = cms.int32(0),
    ## process of interest - r_ggH or r_bbH
    POI = cms.string("r_bbH"),
    ## define verbosity level
    verbosity   = cms.uint32(2),
    ## Set true if we want to skip observed limits
    expectedOnly = cms.bool(True),
    ## define output label
    outputLabel = cms.string("mssm"), 
    ## define masspoints for limit plot
    masspoints = cms.vdouble(
    90.
   ,100.
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
