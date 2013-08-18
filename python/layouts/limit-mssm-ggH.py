import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string("CMS Preliminary, H #rightarrow #tau #tau, 19.8 fb^{-1} at 8 TeV"),	
    #dataset = cms.string("CMS Preliminary, H #rightarrow #tau #tau, 4.9 fb^{-1} at 7 TeV, 19.4 fb^{-1} at 8 TeV"),
    ## extra labels (below legend)
    extra = cms.string("gg#rightarrow#phi bb profiled"),	
    ## x-axis title
    xaxis = cms.string("m_{#phi} [GeV]"),
    ## x-axis title
    yaxis = cms.string("95% CL limit on #sigma(gg#rightarrow#phi)#timesBR [pb]"),
    ## min for plotting
    min = cms.double(0.01),
    ## max for plotting
    max = cms.double(200.),
    ## min for plotting
    log = cms.int32(1),
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
    outputLabel = cms.string("ggH"), 
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
    ## is this mssm?
    mssm = cms.bool(True),
    ## plot expected only
    expectedOnly = cms.bool(False),
)
