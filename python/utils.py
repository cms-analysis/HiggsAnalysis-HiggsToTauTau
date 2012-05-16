


def parseArgs(args) :
    """
    parse a list of arguments which can be intergers or of type intA-intB
    where intA<=intB and fill this list of arguments into a list if ints
    """
    list = []
    for elem in args :
        if elem.find("-") > -1 :
            if elem.find(":") > -1 :
                step = int(elem[elem.find(":")+1:])
                min = int(elem[:elem.find("-")  ])
                max = int(elem[elem.find("-")+1:elem.find(":")])
            else :
                step = 1
                min = int(elem[:elem.find("-")  ])
                max = int(elem[elem.find("-")+1:])
            while min <= max :
                list.append(min)
                min=min+step
        else :
            list.append(int(elem))
    return list
