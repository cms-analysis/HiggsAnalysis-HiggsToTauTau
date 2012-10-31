import FWCore.ParameterSet.Config as cms

layout = cms.PSet(
    ## dataset
    dataset=cms.string(
        ", #sqrt{s}=7-8 TeV, VH #rightarrow #tau #tau, L=17 fb^{-1}"),
    ## x-axis title
    xaxis=cms.string("m_{H} [GeV]"),
    ## x-axis title
    yaxis=cms.string("95% CL limit on #sigma/#sigma_{SM}"),
    ## plot expected only
    expectedOnly=cms.bool(False),
    ## is this mssm?
    mssm=cms.bool(False),
    ## print to png
    png=cms.bool(True),
    ## print to pdf
    pdf=cms.bool(True),
    ## print to txt
    txt=cms.bool(True),
    ## print to root
    root=cms.bool(True),
    ## min for plotting
    min=cms.double(0.),
    ## max for plotting
    max=cms.double(15),  ##12
    ## min for plotting
    log=cms.int32(0),
    ## define verbosity level
    verbosity=cms.uint32(2),
    ## define output label
    outputLabel=cms.string("injected_limit"),
    ## define masspoints for limit plot
    masspoints=cms.vdouble(range(110, 146, 5)),
    injected=cms.bool(True),
)
