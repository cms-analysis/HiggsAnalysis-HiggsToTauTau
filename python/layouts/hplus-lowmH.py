import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    #dataset = cms.string("#scale[1.5]{CMS}   h,H,A#rightarrow#tau#tau                     19.7 fb^{-1} (8 TeV) + 4.9 fb^{-1} (7 TeV)"),
    dataset = cms.string("#scale[1.5]{CMS} (unpublished), H^{+}#rightarrow#tau#nu,                         19.7 fb^{-1} (8 TeV)"),
    #dataset = cms.string("#scale[1.5]{CMS}   h,H,A#rightarrow#tau#tau                                           18.3 fb^{-1} (8 TeV)"),
    ## x-axis title
    xaxis = cms.string("m_{A} [GeV]"),
    ## x-axis title
    yaxis = cms.string("#bf{tan#beta}"),
    ## theory label 
    theory = cms.string("MSSM low-m_{H} scenario"),
    ## min for plotting
    min = cms.double(1.5),
    ## max for plotting
    max = cms.double(9.5),
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
    outputLabel = cms.string("mA-tanb") ,
    ## define masspoints for limit plot
    masspoints = cms.vdouble(
     300.
     #,320.
     #,340.
     #,360.
     #,380.
     ,400.
     #,420.
     #,440.
     #,460.
     #,480.
     ,500.
     #,520.
     #,540.
     #,560.
     #,580.
     ,600.
     #,620.
     #,640.
     #,660.
     #,680.
     ,700.
     #,720.
     #,740.
     #,760.
     #,780.
     ,800.
     #,820.
     #,840.
     #,860.
     #,880.
     #,900.
     #,920.
     #,940.
     #,960.
     #,980.
     #,1000.
     #,1020.
     #,1040.
     #,1060.
     #,1080.
     ,1100.
     #,1120.
     #,1140.
     #,1160.
     #,1180.
     #,1200.
     #,1220.
     #,1240.
     #,1260.
     #,1280.
     ,1300.
     #,1320.
     #,1340.
     #,1360.
     #,1380.
     ,1400.
     #,1420.
     #,1440.
     #,1460.
     #,1480.
     ,1500.
     #,1520.
     #,1540.
     #,1560.
     #,1580.
     ,1600.
     #,1620.
     #,1640.
     #,1660.
     #,1680.
     ,1700.
     #,1720.
     #,1740.
     #,1760.
     #,1780.
     ,1800.
     #,1820.
     #,1840.
     #,1860.
     #,1880.
     ,1900.
     #,1920.
     #,1940.
     #,1960.
     #,1980.
     ,2000.
     #,2020.
     #,2040.
     #,2060.
     #,2080.
     ,2100.
     #,2120.
     #,2140.
     #,2160.
     #,2180.
     ,2200.
     #,2220.
     #,2240.
     #,2260.
     #,2280.
     ,2300.
     #,2320.
     #,2340.
     #,2360.
     #,2380.
     ,2400.
     #,2420.
     #,2440.
     #,2460.
     #,2480.
     ,2500.
     #,2520.
     #,2540.
     #,2560.
     #,2580.
     ,2600.
     #,2620.
     #,2640.
     #,2660.
     #,2680.
     ,2700.
     #,2720.
     #,2740.
     #,2760.
     #,2780.
     ,2800.
     #,2820.
     #,2840.
     #,2860.
     #,2880.
     ,2900.
     #,2920.
     #,2940.
     #,2960.
     #,2980.
     ,3000.
     #,3020.
     #,3040.
     #,3060.
     #,3080.
     ,3100.
     ),
    ## is this mssm?
    mssm = cms.bool(True),
    ## is this MSSMvsSM?
    MSSMvsSM = cms.bool(False),
    ## plot black and white friendly?
    BlackWhite = cms.bool(False),
    ## plot transparent?
    transparent = cms.bool(True),
    ## print the 2-sigma band
    outerband = cms.bool(True),
    ## plot expected only
    expectedOnly = cms.bool(False),
    ## print constraints from mH=125GeV
    higgs125 = cms.bool(True),
    ## add arXiv-1211-6956 (ATLAS) to plot
    arXiv_1211_6956 = cms.bool(False),
    ## add arXiv-1204-2760 (ATLAS) to plot
    arXiv_1204_2760 = cms.bool(False),
    ## add arXiv-1302-2892
    arXiv_1302_2892 = cms.bool(False),
    ## add arXiv-1205-5736
    arXiv_1205_5736 = cms.bool(False),
    ## add HIG-12-052
    HIG_12_052 = cms.bool(False),
)
