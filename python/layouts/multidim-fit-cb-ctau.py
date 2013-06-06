import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset = cms.string("Preliminary, #sqrt{s}=7-8 TeV, L = 24.3 fb^{-1}, H #rightarrow #tau #tau"),
    ## x-axis title
    xaxis = cms.string("c_{b}"),
    ## x-axis title
    yaxis = cms.string("c_{#tau}"),
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
    verbosity = cms.uint32(3),
    ## define output label
    outputLabel = cms.string("scan"),
    ## define masspoints for limit plot
    masspoints = cms.vdouble(
   # 90
   100
   #,120
   #,130
   #,140
   #,160
   #,180
   #,200
   #,250
   #,300
   #,350
   #,400
   #,450
   #,500
   #,600
   #,700
   #,800
   #,900
   #,1000
    ),
    ## make a temperature plot?
    temp = cms.bool(False),
    ## define physics-model
    model = cms.string("CB-CTAU"),
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
    cms.PSet(mass = cms.double( 250.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 300.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 350.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 400.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 450.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 500.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 600.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 700.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 800.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double( 900.), max = cms.double(-1.)),
    cms.PSet(mass = cms.double(1000.), max = cms.double(-1.)),
    ),        
)
