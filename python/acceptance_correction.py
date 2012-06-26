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

def acceptance_correction(process, mass) :
    """
    function to return the acceptance correction for the smearing of MSSM higgs masses
    at high nominal mass due to initial and infal state radiation. Pivotal values
    correspond to the simulated masses. Values in between are interpolated liearly.
    The parameter mass is expected to be of type float. The parameter process is
    expected to be of type string. It can take 'ggH' or 'bbH' as values. The acceptance
    correction currently is only available from 90 to 500, beyond the values for 90 or
    500 are passed on as best approximations.
    """
    ## map of pivotal values (from 90 up to 500 at the moment)
    values = {
        90.   : ({"ggH" : 1.032, "bbH" : 1.011}),
        100.  : ({"ggH" : 1.033, "bbH" : 1.011}),
        120.  : ({"ggH" : 1.033, "bbH" : 1.011}),
        130.  : ({"ggH" : 1.032, "bbH" : 1.011}),
        140.  : ({"ggH" : 1.034, "bbH" : 1.011}),
        160.  : ({"ggH" : 1.035, "bbH" : 1.011}),
        180.  : ({"ggH" : 1.035, "bbH" : 1.012}),
        200.  : ({"ggH" : 1.038, "bbH" : 1.013}),
        250.  : ({"ggH" : 1.044, "bbH" : 1.014}),
        300.  : ({"ggH" : 1.060, "bbH" : 1.017}),
        350.  : ({"ggH" : 1.134, "bbH" : 1.025}),
        400.  : ({"ggH" : 1.173, "bbH" : 1.032}),
        450.  : ({"ggH" : 1.246, "bbH" : 1.041}),
        500.  : ({"ggH" : 1.400, "bbH" : 1.049}),
        }

    if mass<90 :
        return values[90][process]
    if mass>500 :
        return values[500][process]

    bin = interval(values.keys(), mass)
    if bin[0]<0 :
        return -999.
    else :
        dx = bin[1]-bin[0]
        dy = values[bin[1]][process]-values[bin[0]][process]
        return values[bin[0]][process] if dx==0 else values[bin[0]][process]+dy/dx*(float(mass)-bin[0])

#print acceptance_correction("ggH", "95")
