import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    #dataset = cms.string("12.2 fb^{-1}  #sqrt{s}=8 TeV"),
    dataset = cms.string("4.9 fb^{-1}  #sqrt{s}=7 TeV"),
    ## x-axis title
    xaxis = cms.string("m_{A} [GeV]"),
    ## x-axis title
    yaxis = cms.string("#sigma(ggH/bbH#rightarrow#phi#rightarrow#tau#tau)_{95% CL} [pb]"),
    ## is this mssm?
    mssm = cms.bool(True),
    ## center of mass energy (7, 8, 78 for combined)
    ecms = cms.int32(7),
    ## print to png
    png  = cms.bool(True),
    ## print to pdf
    pdf  = cms.bool(True),
    ## print to txt
    txt  = cms.bool(True),
    ## print to root
    root = cms.bool(True),
    ## min for plotting
    min = cms.double(0.0005),
    ## max for plotting
    max = cms.double(200.),
    ## min for plotting
    log = cms.int32(1),
    ## define verbosity level
    verbosity   = cms.uint32(2),
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
