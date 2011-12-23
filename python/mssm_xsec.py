#!/usr/bin/env python

import math
import os
 
from HiggsAnalysis.HiggsToTauTau.tools.mssm_xsec_tools import mssm_xsec_tools

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.gROOT.SetStyle("Plain")

_FILE_NAME = os.path.join(os.environ['CMSSW_BASE'], 'src/HiggsAnalysis/HiggsToTauTau/data', 'out.mhmax_7_nnlo.root')

helper = mssm_xsec_tools(_FILE_NAME)

def square(x):
    return x*x

inclusion_ranges = {
    'A' : lambda massA: True,
    'H' : lambda massA: massA >= 130,
    'h' : lambda massA: massA <= 130,
}

def effective_cross_section(mA, tanB, scheme='5flavor',
                            uncertainties = 0,
                            verbose=False):
    output = 0.0
    bb_prod_type_mapping = {
        '4flavor' : 'bbH4f',
        '5flavor' : 'bbH',
        'santander' : 'santander'
    }

    if scheme not in bb_prod_type_mapping:
        raise ValueError("Unknown scheme %s!" % scheme)

    bb_prod_type = bb_prod_type_mapping[scheme]

    mssm_info = helper.query(mA, tanB)
    total_correction = 0

    if verbose:
        print " Querying cross section - mA = %0.0f tanbeta = %0.0f" % (
            mA, tanB)
        print " Using xsec scheme: %s" % scheme

    for higgs_type in ['H', 'A', 'h']:
        linear_uncertainties = 0
        quadratic_uncertainties = 0
        for production_mechanism in ['ggF', bb_prod_type]:
            # Check if it's relevant
            if inclusion_ranges[higgs_type](mA):
                higgs_info = mssm_info['higgses'][higgs_type]
                br = higgs_info['BR']

                if uncertainties:
                    linear_uncertainties += \
                            higgs_info['mu'][
                                production_mechanism][uncertainties]*br
                    quadratic_uncertainties += square(
                        higgs_info['pdf']
                        [production_mechanism][uncertainties]*br
                    )

                xsec = (higgs_info['xsec'][production_mechanism]/helper.unit_pb)
                output += br*xsec
                if verbose:
                    print "--- %s-%s contributes %0.2f * %0.2fpb = %0.2f" % (
                        higgs_type, production_mechanism, br, xsec, br*xsec)
        correction = linear_uncertainties + uncertainties*math.sqrt(
            quadratic_uncertainties)
        total_correction += correction
    if verbose:
        print "Total cross section: %0.2f" % output
    return output + total_correction

def get_tanb_for_xsec(xsec, xsec_from_tanb_func):
    graph = ROOT.TGraph(55)
    for i, tanb in enumerate(range(5, 60+1)):
        eff_xsec = xsec_from_tanb_func(tanb)
        graph.SetPoint(i, eff_xsec, tanb)
    return graph.Eval(xsec)

def get_tanb_limit(mass, xsec_limit, type='5flavor', unc=0):
    # Make closure function that looks up for a given tanb
    def query(tanb):
        return effective_cross_section(mass, tanb, type, unc)
    # Get the tan beta limit for this mass
    tanb_limit = get_tanb_for_xsec(xsec_limit, query)
    return tanb_limit

def make_tanb_tgraph(masses, xsec_limits, type='5flavor'):
    output = ROOT.TGraph(len(masses))
    assert(len(masses) == len(xsec_limits))
    for i, (mass, xsec_limit) in enumerate(zip(masses, xsec_limits)):
        output.SetPoint(i, mass, get_tanb_limit(mass, xsec_limit, type))
    return output

if __name__ == "__main__":

    masses = [ 90, 90., 120., 130., 160., 200., 250., 300.]

    obs_limits = [ 1000, 394.7, 86.5, 59.9, 28.3, 16.4, 12.9, 9.4 ]
    exp_limits = [ 1000, 621.9, 59.8, 40.5, 19.0, 11.2, 7.6, 5.7 ]

    five_flavor_graph = {
        'exp' : ROOT.TGraph(len(masses)),
        'obs' : ROOT.TGraph(len(masses)),
    }

    four_flavor_graph = {
        'exp' : ROOT.TGraph(len(masses)),
        'obs' : ROOT.TGraph(len(masses)),
    }

    for key, graph in five_flavor_graph.iteritems():
        graph.SetLineColor(ROOT.EColor.kBlue)
        graph.SetLineWidth(2)
        if '1' in key:
            graph.SetLineStyle(2)

    for key, graph in four_flavor_graph.iteritems():
        graph.SetLineColor(ROOT.EColor.kRed)
        graph.SetLineWidth(2)
        if '1' in key:
            graph.SetLineStyle(2)

    five_flavor_graph['exp'].SetLineStyle(2)

    for type, limit_collection in [('exp', exp_limits), ('obs', obs_limits)]:
        for index, (mass, limit) in enumerate(zip(masses, limit_collection)):

            def five_flavor_query(tanb):
                return effective_cross_section(mass, tanb, '5flavor', 0)
            def four_flavor_query(tanb):
                return effective_cross_section(mass, tanb, '4flavor', 0)
            def five_flavor_query_up(tanb):
                return effective_cross_section(mass, tanb, '5flavor', -1)
            def five_flavor_query_down(tanb):
                return effective_cross_section(mass, tanb, '5flavor', +1)
            def four_flavor_query_up(tanb):
                return effective_cross_section(mass, tanb, '4flavor', -1)
            def four_flavor_query_down(tanb):
                return effective_cross_section(mass, tanb, '4flavor', +1)

            five_flavor = get_tanb_for_xsec(limit, five_flavor_query)
            five_flavor_graph[type].SetPoint(index, mass, five_flavor)

            four_flavor = get_tanb_for_xsec(limit, four_flavor_query)
            four_flavor_graph[type].SetPoint(index, mass, four_flavor)

            diff = (five_flavor - four_flavor)/five_flavor
            print "mass: %3.0f 5flavor: %3.2f 4flavor: %3.2f diff: %2.2f%%" % (
                mass,
                five_flavor,
                four_flavor,
                diff*100.0
            )

    tev_masses = [ 90,  100,  110,  120,  130,  140,  150,  160,  170,  180,  190, 200, 201, 210 ]
    tev_limits = [ 31,  46,   43,   34,   29,   30,   31,   33,   38,   42,   48,  55, 60., 65 ]

    tev_graph = ROOT.TGraph(len(tev_limits))
    for i, (mass, limit) in enumerate(zip(tev_masses, tev_limits)):
        tev_graph.SetPoint(i, mass, limit)

    canvas = ROOT.TCanvas("blah", "blah", 800, 600)
    canvas.SetBottomMargin(0.13)
    canvas.SetLeftMargin(0.1)
    canvas.SetRightMargin(0.1)

    legend = ROOT.TLegend(0.55, 0.15, 0.9, 0.42, "", "brNDC")
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)

    # make exclusion zone look good
    five_flavor_graph['obs'].SetPoint(0, 80, 43)
    five_flavor_graph['exp'].SetPoint(0, 80, 55)

    tev_graph.SetLineColor(ROOT.EColor.kAzure -1)
    tev_graph.SetFillColor(ROOT.EColor.kAzure -1)
    tev_graph.SetFillStyle(1001)

    five_flavor_graph['exp'].SetLineColor(ROOT.EColor.kRed)
    five_flavor_graph['obs'].SetLineColor(ROOT.EColor.kAzure -4)

    five_flavor_graph['obs'].SetLineWidth(9902)
    five_flavor_graph['obs'].SetFillStyle(1001)
    five_flavor_graph['obs'].SetFillColor(
        five_flavor_graph['obs'].GetLineColor())
    five_flavor_graph['obs'].SetLineColor(1)

    five_flavor_graph['obs'].Draw("al")
    five_flavor_graph['exp'].Draw("l,same")

    five_flavor_graph['exp'].SetLineWidth(3)

    tev_graph.SetLineWidth(4)
    tev_graph.SetFillStyle(3003)
    tev_graph.SetFillColor(tev_graph.GetLineColor())
    tev_graph.Draw("l,same")

    legend.AddEntry(five_flavor_graph['obs'], "Excluded", "f")
    legend.AddEntry(five_flavor_graph['exp'], "Expected limit", "l")
    legend.AddEntry(tev_graph, "Tevatron excluded", "l")

    label = ROOT.TPaveText(0.12, 0.17, 0.5, 0.28, "NDC")
    label.SetBorderSize(0)
    label.SetFillStyle(0)
    label.AddText("MSSM m_{h}^{max} scenario")
    label.AddText("95% C.L. excluded regions")
    label.Draw()

    histo = five_flavor_graph['obs'].GetHistogram()
    histo.GetXaxis().SetRangeUser(90, 300)
    histo.SetMinimum(0)
    histo.GetXaxis().SetTitle("m_{A} (GeV/c^{2})")
    histo.GetXaxis().SetTitleSize(0.05)
    histo.GetYaxis().SetTitleSize(0.05)
    histo.GetYaxis().SetNdivisions(110)

    histo.GetYaxis().SetTitle("tan #beta")
    histo.SetTitle("")
    histo.SetMaximum(60)
    histo.Draw("axissame")

    legend.Draw()

    canvas.SaveAs('tan_beta.pdf')

    effective_cross_section(120, 30, verbose=True)
    effective_cross_section(120, 30, True, verbose=True)
    effective_cross_section(250, 30, verbose=True)
    effective_cross_section(250, 30, True, verbose=True)

