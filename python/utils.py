def get_mass(directory) :
    '''
    Returns the mass from a directory string. directories
    are expected to end with a floating point number of
    with an integer number. Trailing slashes are removed.
    The mass is returned as a string.
    '''
    idx = directory.rfind("/")
    if idx == (len(directory) - 1):
        idx = directory[:idx - 1].rfind("/")
    mass  = directory[idx + 1:]
    return mass.rstrip('/')

def is_number(s):
    '''
    check if the string is a number or not (works for int and float)
    '''
    try:
        float(s)
        return True
    except ValueError:
        return False

def contained(elem, list) :
    """
    return true if the element is contained in the list
    """
    if elem in "\n".join(list) :
        return True
    return False


def mass_category(mass, category, channel) :
    """
    return the mass category depending on the value of mass. Currently we
    will have only one mass category for the pt sub-categorization.
    """
    # Temprorarily only use 1 mass cat.
    #return 0
    value = float(mass)
    mass_category = 0
    if "hbb" in channel :
        if category in "0 1 2 3 4 5" :
            if value>=180 :
                mass_category = 1
            elif value<180 :
                mass_category = 0
        if category in "6" :
            if value>=200 :
                mass_category = 1
            elif value<200 :
                mass_category = 0
    return mass_category

def is_integer(elem):
    try:
        int(elem)
    except ValueError:
        return False
    if abs(int(elem) - float(elem)) < 1e-6:
        return True
    return False

def parseArgs(args) :
    """
    parse a list of arguments which can be floats, intergers or of type
    intA-intB where intA<=intB and both intA and intB have to be integers
    and fill this list of arguments into a list
    """
    list = []
    for elem in args :
        if elem.find("-") > -1 :
            if elem.find(":") > -1 :
                step = float(elem[elem.find(":")+1:])
                min = float(elem[:elem.find("-")  ])
                max = float(elem[elem.find("-")+1:elem.find(":")])
            else :
                step = 1
                min = float(elem[:elem.find("-")  ])
                max = float(elem[elem.find("-")+1:])
            while min <= max :
                if is_integer(min):
                    list.append(int(min))
                else:
                    list.append(min)
                min=min+step
        else :
            if is_integer(elem):
                list.append(int(elem))
            else:
                list.append(elem)
    return list
