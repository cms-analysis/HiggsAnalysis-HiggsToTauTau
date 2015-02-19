
import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    #dataset = cms.string("#scale[1.5]{CMS}   Projection       #phi#rightarrow#tau#tau                 300 fb^{-1} (14 TeV)"),    
    #dataset = cms.string("#scale[1.5]{CMS}   #phi#rightarrow#tau#tau                                          19.7 fb^{-1} (8 TeV)"),
    #dataset = cms.string("#scale[1.5]{CMS} (unpublished)   #phi#rightarrow#tau#tau                 19.7 fb^{-1} (8 TeV)"),
    dataset = cms.string("#phi#rightarrow#tau#tau                                          19.7 fb^{-1} (8 TeV)"),
    ## x-axis title
    xaxis = cms.string("#sigma#font[42]{(gg#phi)}#upoint#font[52]{B}#font[42]{(#phi#rightarrow#tau#tau)} [pb]"),
    ## x-axis title
    yaxis = cms.string("#sigma#font[42]{(bb#phi)}#upoint#font[52]{B}#font[42]{(#phi#rightarrow#tau#tau)} [pb]"),
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
    masspoints = cms.vdouble(
    90
   ,100
   #,110
   ,120
   ,125
   ,130
   ,140
   #,150
   ,160
   #,170
   ,180
   #,190
   ,200
   #,210
   #,220
   #,230
   #,240
   ,250
   #,275
   ,300
   #,325
   ,350
   #,375
   ,400
   #,425
   ,450
   #,475
   ,500
   #,550
   ,600
   #,650
   ,700
   #,750
   ,800
   #,850
   ,900
   #,950
   ,1000
    ),
    #masspoints = cms.vdouble(140),
    ## is this mssm?
    mssm = cms.bool(True),
    ## make a temperature plot?
    temp = cms.bool(False),
    ## draw the SM expectation
    drawSM = cms.bool(False),
    ## apply smoothing before plotting?
    smooth = cms.bool(True),
    ## define physics-model
    model = cms.string("ggH-bbH"),
    ## max for plotting (for fine tuning)
    xmaxs = cms.VPSet(
    cms.PSet(mass = cms.double(  90.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 100.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 120.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 130.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 140.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 160.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 180.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 200.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 250.), max = cms.double(-1)),
    cms.PSet(mass = cms.double( 300.), max = cms.double(-1)),
    cms.PSet(mass = cms.double( 350.), max = cms.double(-1)),
    cms.PSet(mass = cms.double( 400.), max = cms.double(-1)),
    cms.PSet(mass = cms.double( 450.), max = cms.double(-1)),
    cms.PSet(mass = cms.double( 500.), max = cms.double(-1)),
    cms.PSet(mass = cms.double( 600.), max = cms.double(-1)),
    cms.PSet(mass = cms.double( 700.), max = cms.double(-1)),
    cms.PSet(mass = cms.double( 800.), max = cms.double(-1)),
    cms.PSet(mass = cms.double( 900.), max = cms.double(-1)),
    cms.PSet(mass = cms.double(1000.), max = cms.double(-1)),
    ),
    ## max for plotting (for fine tuning)
    ymaxs = cms.VPSet(
    cms.PSet(mass = cms.double(  90.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 100.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 120.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 130.), max = cms.double( 3.)),
    cms.PSet(mass = cms.double( 140.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 160.), max = cms.double(1.5)),
    cms.PSet(mass = cms.double( 180.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 200.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 250.), max = cms.double(0.4)),
    cms.PSet(mass = cms.double( 300.), max = cms.double(.25)),
    cms.PSet(mass = cms.double( 350.), max = cms.double(0.2)),
    cms.PSet(mass = cms.double( 400.), max = cms.double(.15)),
    cms.PSet(mass = cms.double( 450.), max = cms.double(0.1)),
    cms.PSet(mass = cms.double( 500.), max = cms.double(0.1)),
    cms.PSet(mass = cms.double( 600.), max = cms.double(0.1)),
    cms.PSet(mass = cms.double( 700.), max = cms.double(.05)),
    cms.PSet(mass = cms.double( 800.), max = cms.double(.05)),
    cms.PSet(mass = cms.double( 900.), max = cms.double(.03)),
    cms.PSet(mass = cms.double(1000.), max = cms.double(.03)),
    ),        
)
