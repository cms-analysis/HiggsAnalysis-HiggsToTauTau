#!/usr/bin/env python
#import re
import ROOT
import compute_limits
import sys

ROOT.gROOT.SetBatch(True)
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetFrameLineWidth(2)
ROOT.gStyle.SetLineWidth(2)

def make_tgraph(xs, ys):
    assert(len(xs) == len(ys))
    output = ROOT.TGraph(len(xs))
    for i, (x, y) in enumerate(zip(xs, ys)):
        output.SetPoint(i, x, y)
    return output

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s xsec_br_limits.txt [opt]" % sys.argv[0]
        print "[opt] is a comma separated list of options."
        print "Available options: hplus,moriond,lp,exponly"
        sys.exit(1)

    observed_col = 6
    expected_col = 3

    # Limits of plot
    min = 90
    max = 500
    ymax = 50

    print "NOTA BENE: I expect the following table format:"
    print "First column: mass_A, as integer"
    print "Column %i: expected limit" % expected_col
    print "Column %i: observed limit" % observed_col
    print "(These parameters are configurable) -- see line 26"

    add_hplus = False if len(sys.argv) < 3 else ('hplus' in sys.argv[2])
    add_moriond = False if len(sys.argv) < 3 else ('moriond' in sys.argv[2])
    add_lp = False if len(sys.argv) < 3 else ('lp' in sys.argv[2])
    exponly = False if len(sys.argv) < 3 else ('exponly' in sys.argv[2])
    if add_hplus:
        print "Adding H+ limit!"
    if add_moriond:
        print "Adding Moriond limits"
    if add_lp:
        print "Adding LP limits"
    if exponly:
        print "Only showing expected limits"

    limit_lines = compute_limits.get_columns(sys.argv[1])

    limit_data = list(compute_limits.translate_to_tan_beta(
        limit_lines, 'santander', 0))

    limit_data_up = list(compute_limits.translate_to_tan_beta(
        limit_lines, 'santander', 1))

    limit_data_down = list(compute_limits.translate_to_tan_beta(
        limit_lines, 'santander', -1))

    mass_points = [ row[0] for row in limit_data ]
    observed = [ row[observed_col] for row in limit_data ]
    observed_up = [ row[observed_col] for row in limit_data_up ]
    observed_down = [ row[observed_col] for row in limit_data_down ]
    expected = [ row[expected_col] for row in limit_data ]

    for row in limit_data:
        print "mass: {mass} | -2sigma: {outerLow} | -1sigma: {innerLow} | expected: {exp} | +1sigma: {innerHigh} | +2sigma: {outerHigh} | observed: {obs}".format(mass=row[0], outerLow=row[1], innerLow=row[2], exp=row[expected_col], innerHigh=row[4], outerHigh=row[5], obs=row[observed_col])

    d0 = [
        (90, 28.8),
        (100, 32.0),
        (110, 33.6),
        (120, 25.0),
        (130, 26.3),
        (140, 28.1),
        (150, 25.3),
        (160, 27.3),
        (170, 29.8),
        (180, 38.4),
        (190, 41.6),
        (200, 45.8),
        (210, 51.8),
        (220, 56.7),
        (230, 60.9),
        (240, 68.6),
        (250, 75.5),
        (260, 81.0),
        (270, 93.5),
        (280, 99.2),
    ]

    # LEP from H+ macro
    hp_lep = [
        (50,100),
        (91,100),
        (91.8,30.02624),
        (91.845,22.07032),
        (91.845,17.12491),
        (91.84523,13.64727),
        (92.61388,11.94143),
        (93.38253,10.03852),
        (94.91982,9.021481),
        (95.68846,8.107481),
        (97.22578,7.141608),
        (99.5317,6.680381),
        (103.375,7.189448),
        (104.1436,7.841313),
        (106.4496,8.326916),
        (109.5242,8.609568),
        (112.5988,8.438845),
        (115.6733,8.107481),
        (118.748,7.384029),
        (122.5912,6.547911),
        (126.4344,5.963618),
        (131.815,5.359424),
        (138.7328,4.752558),
        (144.1134,4.445624),
        (149.4939,4.186368),
        (156.4118,3.968637),
        (164.8669,3.687628),
        (177.1653,3.472575),
        (187.9264,3.29197),
        (203.2994,3.141663),
        (221.7469,2.978266),
        (241.7318,2.861322),
        (261.7167,2.767383),
        (283.2388,2.676528),
        (304.761,2.641027),
        (334.7383,2.554322),
        (357.0292,2.50367),
        (383.9319,2.48701),
        (420.8271,2.454023),
        (452.3417,2.421473),
        (487.6996,2.405361),
    ]

    # extend - EK
    hp_lep.append((550,2.405361))
    #hp_lep.append((487.6996,0))
    hp_lep.append((550,0))
    #hp_lep.append((0,0))

    lep = hp_lep

    # Observed limit from H+
    hp_obs = [
        (89.08514,25.22366),
        (114.6131,41.91862),
        (126.634,63.53459),
        (132.5185,88.55868),
    ]
    hp_exp = [
        (89.08514,25.08533),
        (114.6131,39.99895),
        (126.634,58.14883),
        (132.5185,77.68212),
    ]

    #Observed H+ from tevatron
    hp_tev = [
        (59.46563,33),
        (89.08514,50),
        (114.6131,103),
        (114.6131,110),
        (59.46563,110),
    ]

    # Combined TeV limits
    tev_masses = [ 90,  100,  110,  120,  130,  140,  150,  160,  170,  180,  190, 200, 201, 210 ]
    tev_limits = [ 31,  46,   43,   34,   29,   30,   31,   33,   38,   42,   48,  55, 60., 65 ]

    moriond_exp = [
        (90  , 27.90 ),
        (100 , 31.15),
        (120 , 31.58),
        (130 , 30.92),
        (140 , 31.70),
        (160 , 31.77),
        (180 , 34.34 ),
        (200 , 38.39 ),
        (250 , 50.65),
        (300 , 66.69),
    ]

    moriond_obs = [
        (90 , 27.39),
        (100 ,29.31),
        (120 ,25.42),
        (130 ,22.81),
        (140 ,23.83),
        (160 ,24.21),
        (180 ,28.59),
        (200 ,33.67),
        (250 ,44.43),
        (300 ,58.18),
        (350 ,78.48),
    ]

    lp_exp = [(90, 9.5999999999999996),
              (100, 10.0),
              (120, 10.1),
              (130, 8.8000000000000007),
              (140, 10.699999999999999),
              (160, 11.699999999999999),
              (180, 12.699999999999999),
              (200, 14.4),
              (250, 18.600000000000001),
              (300, 23.800000000000001),
              (400, 36.299999999999997),
              (450, 43.399999999999999),
              (500, 52.700000000000003)]

    lp_obs = [(90, 8.5),
              (100, 7.9000000000000004),
              (120, 8.6999999999999993),
              (130, 7.7999999999999998),
              (140, 11.0),
              (160, 12.699999999999999),
              (180, 14.0),
              (200, 17.699999999999999),
              (250, 24.5),
              (300, 31.699999999999999),
              (400, 44.799999999999997),
              (450, 50.600000000000001),
              (500, 59.5)]

    observed_graph = make_tgraph(
        [mass_points[-1]+10, 60, 70, 80.0] + mass_points + [mass_points[-1]+0.01, mass_points[-1] + 10],
        [175, 175, observed[0] + 5, observed[0]] + observed + [100, 175]
    )

    observed_up_graph = make_tgraph(mass_points, observed_up)
    observed_down_graph = make_tgraph(mass_points, observed_down)
    expected_graph = make_tgraph(mass_points, expected)

    d0_graph = make_tgraph([x[0] for x in d0], [x[1] for x in d0])
    tev_graph = make_tgraph(tev_masses, tev_limits)
    lep_graph = make_tgraph([x[0] for x in lep], [x[1] for x in lep])
    hp_graph = make_tgraph([x[0] for x in hp_obs], [x[1] for x in hp_obs])
    moriond_graph = make_tgraph([x[0] for x in moriond_exp], [x[1] for x in moriond_exp])
    moriond_obs_graph = make_tgraph([x[0] for x in moriond_obs], [x[1] for x in moriond_obs])
    lp_graph = make_tgraph([x[0] for x in lp_exp], [x[1] for x in lp_exp])
    lp_obs_graph = make_tgraph([x[0] for x in lp_obs], [x[1] for x in lp_obs])

    # Setup colors
    d0_color = ROOT.TColor(1500, 0.373, 0.533, 1.0)
    cms_color = ROOT.TColor(1501, 0.463, 0.867, 0.957)
    cms_hp_color = ROOT.TColor(1505, 76.0/255, 75./255, 232./255)
    lep_color = ROOT.TColor(1502, 0.494, 0.694, 0.298)
    red_color = ROOT.TColor(1503, 1.0, 0.071, 0.0)
    tev_color = ROOT.TColor(1504, 1., 0.533, 1.0)
    moriond_color = ROOT.TColor(1506, 97/255., 56/255., 204/255.)

    line_width = 2

    observed_graph.SetLineWidth(9902)
    observed_graph.SetFillColor(1501)
    observed_graph.SetFillStyle(1001)

    observed_up_graph.SetLineWidth(line_width)
    observed_up_graph.SetLineStyle(2)

    observed_down_graph.SetLineWidth(line_width)
    observed_down_graph.SetLineStyle(2)

    if exponly :
        expected_graph.SetLineWidth(804)
        expected_graph.SetFillColor(1503)
        expected_graph.SetFillStyle(3001)
    else :
        expected_graph.SetLineWidth(line_width)
    expected_graph.SetLineStyle(3)
    expected_graph.SetLineColor(1503)

    moriond_graph.SetLineStyle(2)
    moriond_graph.SetLineWidth(3)
    moriond_graph.SetLineColor(1506)

    moriond_obs_graph.SetLineStyle(1)
    moriond_obs_graph.SetLineWidth(3)
    moriond_obs_graph.SetLineColor(1506)

    lp_graph.SetLineStyle(2)
    lp_graph.SetLineWidth(3)
    lp_graph.SetLineColor(1506)

    lp_obs_graph.SetLineStyle(1)
    lp_obs_graph.SetLineWidth(3)
    lp_obs_graph.SetLineColor(1506)

    d0_graph.SetFillColor(1500)
    d0_graph.SetLineColor(1500)
    d0_graph.SetFillStyle(1001)
    d0_graph.SetLineWidth(9900)

    tev_graph.SetFillColor(1504)
    tev_graph.SetLineColor(1504)
    tev_graph.SetFillStyle(1001)
    tev_graph.SetLineWidth(9900)

    hp_graph.SetFillColor(1505)
    hp_graph.SetLineColor(1505)
    hp_graph.SetFillStyle(1001)
    hp_graph.SetLineWidth(9900)

    lep_graph.SetFillColor(1502)
    lep_graph.SetLineColor(1502)
    lep_graph.SetFillStyle(1001)
    lep_graph.SetLineWidth(-9900)

    background = ROOT.TH1F("background", "background", max - min, min, max)
    background.GetXaxis().SetTitle("m_{A} [GeV]")
    background.GetXaxis().CenterTitle()
    background.GetYaxis().SetTitle("tan#beta")
    background.GetYaxis().CenterTitle()
    background.GetYaxis().SetTitleSize(0.065)
    background.GetYaxis().SetTitleOffset(0.7)
    background.GetXaxis().SetTitleSize(0.065)
    background.GetXaxis().SetTitleOffset(0.75)
    background.SetMaximum(ymax)
    background.SetStats(0)
    background.SetTitle("")

    canvas = ROOT.TCanvas("blah", "blah", 800, 800)
    canvas.SetLeftMargin(0.11)
    canvas.SetBottomMargin(0.13)

    background.Draw()

    lep_graph.Draw("l")
    if not exponly:
        observed_graph.Draw("l,same")
    #d0_graph.Draw("l,same")
    #tev_graph.Draw("l,same")
    expected_graph.Draw("l,same")
    if add_moriond:
        moriond_graph.Draw("l,same")
        if not exponly:
            moriond_obs_graph.Draw("l,same")
    if add_lp:
        lp_graph.Draw("l,same")
        if not exponly:
            lp_obs_graph.Draw("l,same")

    if not exponly:
        observed_up_graph.Draw("l,same")
        observed_down_graph.Draw("l,same")
    if add_hplus:
        hp_graph.Draw("l, same")

    def unshitify(pave):
        pave.SetFillStyle(0)
        pave.SetBorderSize(0)

    #legend = ROOT.TLegend(0.58, 0.27, 0.90, 0.48,
    legend = ROOT.TLegend(0.58, 0.25, 0.90, 0.42,
    #legend = ROOT.TLegend(0.62, 0.25, 0.9, 0.48,
                          "", "NDC")
    unshitify(legend)
    if not exponly:
        legend.AddEntry(observed_graph, "CMS observed", "f")
        legend.AddEntry(observed_up_graph, "#pm1#sigma theory", "l")
    legend.AddEntry(expected_graph, "CMS expected", "l")
    if add_hplus:
        legend.AddEntry(hp_graph, "CMS H^{+} observed", "f")
    #legend.AddEntry(d0_graph, "D0 7.3 fb^{-1}", "f")
    legend.AddEntry(lep_graph, "LEP", "f")
    if add_moriond:
        if not exponly:
            legend.AddEntry(moriond_obs_graph, "CMS 2010 observed", "l")
        legend.AddEntry(moriond_graph, "CMS 2010 expected", "l")
    if add_lp:
        if not exponly:
            legend.AddEntry(lp_obs_graph, "CMS LP observed", "l")
        legend.AddEntry(lp_graph, "CMS LP expected", "l")
    #legend.AddEntry(tev_graph, "Tevatron", "f")
    legend.Draw()

    #cl_label = ROOT.TPaveText(0.62, 0.48, 0.9, 0.52, "NDC")
    cl_label = ROOT.TPaveText(0.62, 0.42, 0.9, 0.44, "NDC")
    unshitify(cl_label)
    cl_label.SetTextSize(0.027)
    cl_label.SetTextAlign(31)
    cl_label.AddText("95% CL excluded regions")
    cl_label.Draw()

    #cms_label = ROOT.TPaveText(0.7, 0.55, 0.9, 0.7, "NDC")
    cms_label = ROOT.TPaveText(0.07, 0.9, 0.9, 1.0, "NDC")
    unshitify(cms_label)
    cms_label.SetTextSize(0.05)
    cms_label.SetTextAlign(12)
    cms_label.AddText("CMS Preliminary 2011 4.6 fb^{-1}")

    theory_label = ROOT.TPaveText(0.3, 0.18, 0.9, 0.25, "NDC")
    unshitify(theory_label)
    theory_label.SetTextSize(0.04)
    theory_label.SetTextAlign(32)
    theory_label.AddText("MSSM m_{h}^{max} scenario, M_{SUSY} = 1 TeV")

    cms_label.Draw()
    theory_label.Draw()

    background.Draw("axis, same")

    canvas.Update()
    canvas.RedrawAxis()

    # Add some extra lines on the right and top
    top_frame_line = ROOT.TLine(min, ymax, max, ymax)
    top_frame_line.Draw()

    right_frame_line = ROOT.TLine(max, 0, max, ymax)
    right_frame_line.Draw()

    name = "tan_beta_limit.pdf"
    if add_hplus:
        name = name.replace('.pdf', '_with_hplus.pdf')
    if add_moriond:
        name = name.replace('.pdf', '_with_moriond.pdf')
    if add_lp:
        name = name.replace('.pdf', '_with_lp.pdf')
    if exponly:
        name = name.replace('.pdf', '_exponly.pdf')

    canvas.SaveAs(name)
