import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string(" HPA #sqrt{s} = 7 TeV, L = 10 fb^{-1} (proj.)"),
    #dataset = cms.string(", #sqrt{s} = 7 TeV, H #rightarrow #tau #tau, L = 4.6 fb^{-1}"),
    ## x-axis title
    xaxis = cms.string("m_{H} [GeV]"),
    ## x-axis title
    yaxis = cms.string("Significance"),
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
    max = cms.double(20.), ## 10
    ## min for plotting
    log = cms.int32(0),
    ## define verbosity level
    verbosity   = cms.uint32(2),
    ## define output label
    outputLabel = cms.string("sm"), 
    ## define masspoints for limit plot
    masspoints = cms.vdouble(
    110.
   ,115.
   ,118.
   ,120.
   ,122.
   ,124.
   ,126.
   ,128.
   ,130.
   ,135.
   ,140.
   ,150.
   ,160.
   ,170.
   ,180.
   ,190.
   ,200.
  ),
)
