
def interval(keys, mass) :
    """
    return the interval in which the value mass resides. This interval will be used
    for further interpolation. The list of keys (keylist) is expected to contain
    floats. The value masses is expected to be a float.
    """
    flip = 0.
    keys.sort()
    for idx in range(len(keys)) :
        if mass == keys[idx] :
            return (keys[idx], keys[idx])
        else :
            if flip < 0 :
                if keys[idx]-mass>0 :
                    return (keys[idx-1], keys[idx])
            if flip > 0 :
                if keys[idx]-mass<0 :
                    return (keys[idx-1], keys[idx])
            flip = keys[idx]-mass
    return (-1., -1.)    

def acceptance_correction(process, mass, period) :
    """
    function to return the acceptance correction for the smearing of MSSM higgs masses
    at high nominal mass due to initial and infal state radiation. Pivotal values
    correspond to the simulated masses. Values in between are interpolated linearly.
    The parameter mass is expected to be of type float. The parameter process is
    expected to be of type string. It can take 'ggH' or 'bbH' as values. For other
    processes than these -999. will be returned.
    """
    if not (process == "ggH" or process == "bbH") :
        return -999.
    values_14TeV = {  #14TeV = 8TeV for debugging
        80.   : ({"ggH" :  0.10297, "bbH" :  0.10103}),
        90.   : ({"ggH" :  0.10301, "bbH" :  0.10103}),
        100.  : ({"ggH" :  0.10309, "bbH" :  0.10107}),
        120.  : ({"ggH" :  0.10318, "bbH" :  0.10111}),
        130.  : ({"ggH" :  0.10321, "bbH" :  0.10111}),
        140.  : ({"ggH" :  0.10322, "bbH" :  0.10112}),
        160.  : ({"ggH" :  0.10330, "bbH" :  0.10115}),
        180.  : ({"ggH" :  0.10337, "bbH" :  0.10118}),
        200.  : ({"ggH" :  0.10359, "bbH" :  0.10122}),
        250.  : ({"ggH" :  0.10413, "bbH" :  0.10132}),
        300.  : ({"ggH" :  0.10565, "bbH" :  0.10164}),
        350.  : ({"ggH" :  0.11232, "bbH" :  0.10234}),
        400.  : ({"ggH" :  0.11543, "bbH" :  0.10286}),
        450.  : ({"ggH" :  0.12152, "bbH" :  0.10349}),
        500.  : ({"ggH" :  0.13408, "bbH" :  0.10436}),
        600.  : ({"ggH" :  0.27492, "bbH" :  0.10712}),
        700.  : ({"ggH" :  0.38186, "bbH" :  0.10972}),
        800.  : ({"ggH" :  0.53704, "bbH" :  0.11305}),
        900.  : ({"ggH" :  0.76101, "bbH" :  0.11716}),
        1000. : ({"ggH" :  1.07387, "bbH" :  0.12235}),
        }
    values_8TeV = {  #8TeV
        80.   : ({"ggH" :  1.0297, "bbH" :  1.0103}),
        90.   : ({"ggH" :  1.0301, "bbH" :  1.0103}),
        100.  : ({"ggH" :  1.0309, "bbH" :  1.0107}),
        120.  : ({"ggH" :  1.0318, "bbH" :  1.0111}),
        130.  : ({"ggH" :  1.0321, "bbH" :  1.0111}),
        140.  : ({"ggH" :  1.0322, "bbH" :  1.0112}),
        160.  : ({"ggH" :  1.0330, "bbH" :  1.0115}),
        180.  : ({"ggH" :  1.0337, "bbH" :  1.0118}),
        200.  : ({"ggH" :  1.0359, "bbH" :  1.0122}),
        250.  : ({"ggH" :  1.0413, "bbH" :  1.0132}),
        300.  : ({"ggH" :  1.0565, "bbH" :  1.0164}),
        350.  : ({"ggH" :  1.1232, "bbH" :  1.0234}),
        400.  : ({"ggH" :  1.1543, "bbH" :  1.0286}),
        450.  : ({"ggH" :  1.2152, "bbH" :  1.0349}),
        500.  : ({"ggH" :  1.3408, "bbH" :  1.0436}),
        600.  : ({"ggH" :  2.7492, "bbH" :  1.0712}),
        700.  : ({"ggH" :  3.8186, "bbH" :  1.0972}),
        800.  : ({"ggH" :  5.3704, "bbH" :  1.1305}),
        900.  : ({"ggH" :  7.6101, "bbH" :  1.1716}),
        1000. : ({"ggH" : 10.7387, "bbH" :  1.2235}),
        }
    values_7TeV = {  #7TeV
        90.   : ({"ggH" :  1.0310, "bbH" :  1.0107}),
        100.  : ({"ggH" :  1.0317, "bbH" :  1.0109}),
        120.  : ({"ggH" :  1.0332, "bbH" :  1.0112}),
        130.  : ({"ggH" :  1.0337, "bbH" :  1.0114}),
        140.  : ({"ggH" :  1.0345, "bbH" :  1.0115}),
        160.  : ({"ggH" :  1.0351, "bbH" :  1.0121}),
        180.  : ({"ggH" :  1.0354, "bbH" :  1.0120}),
        200.  : ({"ggH" :  1.0385, "bbH" :  1.0130}),
        250.  : ({"ggH" :  1.0444, "bbH" :  1.0139}),
        300.  : ({"ggH" :  1.0617, "bbH" :  1.0173}),
        350.  : ({"ggH" :  1.1345, "bbH" :  1.0249}),
        400.  : ({"ggH" :  1.1725, "bbH" :  1.0321}),
        450.  : ({"ggH" :  1.2462, "bbH" :  1.0395}),
        500.  : ({"ggH" :  1.4006, "bbH" :  1.0494}),
        600.  : ({"ggH" :  3.2471, "bbH" :  1.0829}),
        700.  : ({"ggH" :  4.7654, "bbH" :  1.1175}),
        800.  : ({"ggH" :  6.9610, "bbH" :  1.1627}),
        900.  : ({"ggH" : 10.4280, "bbH" :  1.2221}),
        1000. : ({"ggH" : 15.3254, "bbH" :  1.3023}),
        }

    if period=="14TeV" :
        if mass<80 :
            return values_14TeV[80][process]
        if mass>1000 :
            return values_14TeV[1000][process]
        
        bin = interval(values_14TeV.keys(), mass)
        if bin[0]<0 :
            return -999.
        else :
            dx = bin[1]-bin[0]
            dy = values_14TeV[bin[1]][process]-values_14TeV[bin[0]][process]
            return values_14TeV[bin[0]][process] if dx==0 else values_14TeV[bin[0]][process]+dy/dx*(float(mass)-bin[0])

    if period=="8TeV" :
        if mass<80 :
            return values_8TeV[80][process]
        if mass>1000 :
            return values_8TeV[1000][process]
        
        bin = interval(values_8TeV.keys(), mass)
        if bin[0]<0 :
            return -999.
        else :
            dx = bin[1]-bin[0]
            dy = values_8TeV[bin[1]][process]-values_8TeV[bin[0]][process]
            return values_8TeV[bin[0]][process] if dx==0 else values_8TeV[bin[0]][process]+dy/dx*(float(mass)-bin[0])

    if period=="7TeV" :
        if mass<90 :
            return values_7TeV[90][process]
        if mass>1000 :
            return values_7TeV[1000][process]   

        bin = interval(values_7TeV.keys(), mass)
        if bin[0]<0 :
            return -999.
        else :
            dx = bin[1]-bin[0]
            dy = values_7TeV[bin[1]][process]-values_7TeV[bin[0]][process]
            return values_7TeV[bin[0]][process] if dx==0 else values_7TeV[bin[0]][process]+dy/dx*(float(mass)-bin[0])

#print acceptance_correction("ggH", "95")
