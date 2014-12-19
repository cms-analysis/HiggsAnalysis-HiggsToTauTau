from HiggsAnalysis.HiggsToTauTau.utils import subvec
from HiggsAnalysis.HiggsToTauTau.utils import vec2str

import os

def tanb_grid(args, cmd, sub, opt, smartGrid=False, customTanb="") :

    #if "lowmH" in opt :  #smartGrid can't be used for lowmH since some parameter regions are corrupted and shall not be touched
    #    smartGrid=False
        
    limits = []
    reduced_grid = [] 
    grid = []
    full_grid_mA = []
    mass=(args[0].split("/"))[-1]
    
    if not customTanb == "" :
        custom_tanb = [float(k) for k in customTanb.split(',')]
        idx=0
        while idx < len(custom_tanb) :
            #dirs = vec2str(subvec(args,  -1000,  1000))
            dirs = ""
            for dir in args :
                dirs += dir+" "
            if idx < len(custom_tanb)-1 :
                grid_save = [
                    "{CMD} -n 2 --min {START} --max {END} {SUB} {OPTS} {USER} {DIRS}".format(START=custom_tanb[idx], END=custom_tanb[idx+1], CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]
            else :
                grid_save = [
                    "{CMD} -n 1 --min {START} --max {END} {SUB} {OPTS} {USER} {DIRS}".format(START=custom_tanb[idx], END=custom_tanb[idx], CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]
            grid = grid+grid_save
            idx=idx+2
    
    elif smartGrid :
        os.system("rm "+str(args[0])+"/fixedMu_*.root")
        #os.system("rm "+str(args[0])+"/batch_*.root")
        exclusion = open(str(args[0])+"/exclusion_{MASS}.out".format(MASS=mass), 'r')
        line = exclusion.readlines()
        highlimits = line[0].rstrip("\n").split(" ")
        exclusion.close()
        highlimits.pop(0)
        lowlimits = line[1].rstrip("\n").split(" ")
        exclusion.close()
        lowlimits.pop(0)
        limits = highlimits+lowlimits
        limits.sort(key=float)
        if "lowmH" in opt :
            full_grid_mA = [ 1.5, 2.0, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5 ] ##define the maximum grid for lowmH
        elif "tauphobic" in opt :
            full_grid_mA = [ 1.0, 2.0, 4.0, 6.0, 7.0, 8.0, 10.0, 13.0, 15.0, 17.0, 20.0, 23.0, 25.0, 27.0, 30.0, 33.0, 35.0, 37.0, 40.0, 43.0, 45.0, 47.0, 50.0 ] ##define the maximum grid for tauphobic
        elif "lightstopmod" in opt :
            full_grid_mA = [ 0.7, 0.8, 0.9, 1.0, 2.0, 4.0, 6.0, 7.0, 8.0, 10.0, 13.0, 15.0, 17.0, 20.0, 23.0, 25.0, 27.0, 30.0, 33.0, 35.0, 37.0, 40.0, 43.0, 45.0, 47.0, 50.0, 53.0, 55.0, 57.0, 60.0 ] ##define the maximum grid for lightstopmod
        else :
            full_grid_mA = [ 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 2.0, 4.0, 6.0, 7.0, 8.0, 10.0, 13.0, 15.0, 17.0, 20.0, 23.0, 25.0, 27.0, 30.0, 33.0, 35.0, 37.0, 40.0, 43.0, 45.0, 47.0, 50.0, 53.0, 55.0, 57.0, 60.0 ] ##define the maximum grid for all scenarios except lowmH, lightstopmod and tauphobic
        ##build up a reduced grid 
        for limit in limits :
            tanb_low_idx = -999
            tanb_low = 0.0
            tanb_high_idx = -999
            tanb_high = 0.0
            helper = True
            for idx, point in enumerate(full_grid_mA) :
                if float(limit) <= float(point) and helper :
                    if idx-2 > 0 :
                        tanb_low_idx = idx-3
                    else :
                        tanb_low_idx = 0
                    if idx+2 <= len(full_grid_mA)-2 :
                        tanb_high_idx = idx+3
                    else :
                        tanb_high_idx = len(full_grid_mA)
                    helper = False 
            while tanb_low_idx < tanb_high_idx :
                if full_grid_mA[tanb_low_idx] not in reduced_grid :
                    reduced_grid.append(full_grid_mA[tanb_low_idx])
                tanb_low_idx=tanb_low_idx+1
            reduced_grid.sort(key=float)
        ##if the reduced_grid is empty add last three element otherwise other scripts do not work
        if not reduced_grid :
            reduced_grid.append(full_grid_mA[-1]) 
            reduced_grid.append(full_grid_mA[-2]) 
            reduced_grid.append(full_grid_mA[-3])
        print 'reducded_grid:', reduced_grid 
        ##build up the grid for the reduced_grid
        idx=0    
        while idx < len(reduced_grid) :
            dirs = vec2str(subvec(args,  90,  3100))
            if idx < len(reduced_grid)-1 :
                grid_save = [
                    "{CMD} -n 2 --min {START} --max {END} {SUB} {OPTS} {USER} {DIRS}".format(START=reduced_grid[idx], END=reduced_grid[idx+1], CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]
            else :
                grid_save = [
                    "{CMD} -n 1 --min {START} --max {END} {SUB} {OPTS} {USER} {DIRS}".format(START=reduced_grid[idx], END=reduced_grid[idx], CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]
            grid = grid+grid_save
            idx=idx+2   
            
    else :       
        if "lowmH" in opt : #for lowmH MSSM scenario
            if len(subvec(args, 300, 2999))>0 :
                dirs = vec2str(subvec(args, 300, 2999))
                grid = [
                    "{CMD} -n  4 --min 1.5  --max 3.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  4 --min 3.5  --max 5.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  4 --min 5.5  --max 7.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 7.5  --max 9.5 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]
            if len(subvec(args, 3000, 3100))>0 :
                dirs = vec2str(subvec(args, 3000, 3100))
                grid = [
                    "{CMD} -n  2 --min 2.5  --max 3.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  4 --min 3.5  --max 5.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  4 --min 5.5  --max 7.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 7.5  --max 9.5 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]
        elif "lightstopmod" in opt :  #for lightstopmod MSSM scenarios
            if len(subvec(args,  90, 249))>0 :
                dirs = vec2str(subvec(args,  90,  249))
                grid = [
                    "{CMD} -n  4 --min  0.7  --max  1.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  4 --min  2.0  --max  8.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs) 
                    ,"{CMD} -n  3 --min  9.0  --max 15.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  3 --min 20.0  --max 30.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    #,"{CMD} -n  2 --min 35.0  --max 40.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    #,"{CMD} -n  2 --min 50.0  --max 60.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]
            if len(subvec(args, 250, 299))>0 :
                dirs = vec2str(subvec(args, 250,  299))
                grid = [
                    "{CMD} -n  2 --min  0.7  --max  1.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min  3.0  --max 15.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 20.0  --max 40.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    #,"{CMD} -n  2 --min 50.0  --max 60.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]                
            if len(subvec(args, 300, 399))>0 :
                dirs = vec2str(subvec(args, 300,  399))
                grid = [
                    "{CMD} -n  3 --min  2.0  --max 10.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 13.0  --max 25.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  3 --min 30.0  --max 40.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  2 --min 50.0  --max 60.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]                                
            if len(subvec(args, 400, 599))>0 :
                dirs = vec2str(subvec(args, 400,  599))
                grid = [
                    "{CMD} -n  3 --min  2.0  --max 10.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  2 --min 15.0  --max 20.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 25.0  --max 45.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  2 --min 50.0  --max 60.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]                                
            if len(subvec(args, 600, 1000))>0 :
                dirs = vec2str(subvec(args, 600, 1000))
                grid = [
                    "{CMD} -n  3 --min  2.0  --max 10.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  3 --min 15.0  --max 25.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 30.0  --max 50.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  2 --min 55.0  --max 60.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]
        elif "tauphobic" in opt :  #for tauphobic MSSM scenarios
            if len(subvec(args,  90, 249))>0 :
                dirs = vec2str(subvec(args,  90,  249))
                grid = [
                    "{CMD} -n  2 --min  1.0  --max  2.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  3 --min  4.0  --max  8.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs) 
                    ,"{CMD} -n  3 --min  9.0  --max 15.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  3 --min 20.0  --max 30.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    #,"{CMD} -n  2 --min 35.0  --max 40.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]
            if len(subvec(args, 250, 299))>0 :
                dirs = vec2str(subvec(args, 250,  299))
                grid = [
                    "{CMD} -n  2 --min  1.0  --max  3.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  4 --min  6.0  --max 15.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 20.0  --max 40.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]                
            if len(subvec(args, 300, 399))>0 :
                dirs = vec2str(subvec(args, 300,  399))
                grid = [
                    "{CMD} -n  3 --min  2.0  --max 10.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 13.0  --max 25.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 30.0  --max 50.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]                                
            if len(subvec(args, 400, 599))>0 :
                dirs = vec2str(subvec(args, 400,  599))
                grid = [
                    "{CMD} -n  3 --min  2.0  --max 10.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  3 --min 15.0  --max 25.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 30.0  --max 50.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]                                
            if len(subvec(args, 600, 1000))>0 :
                dirs = vec2str(subvec(args, 600, 1000))
                grid = [
                    "{CMD} -n  3 --min  2.0  --max 10.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  3 --min 15.0  --max 25.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 30.0  --max 50.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]
        elif "low-tb-high" in opt :
            if len(subvec(args,  150, 501))>0 :
                dirs = vec2str(subvec(args, 150, 501))
                grid = [
                    "{CMD} -n  3 --min  0.5 --max 0.9 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n 4 --min  1.5 --max 4.5 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs) 
                    ,"{CMD} -n 5 --min  5.5 --max 9.5 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]
        elif "2HDM" in opt :
            dirs = ""
            for dir in args :
                dirs += dir+" "
            grid = [
                "{CMD} -n  3 --min  1.0  --max  3.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                ,"{CMD} -n  4 --min  4.0  --max  7.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs) 
                ,"{CMD} -n  3 --min  8.0  --max 10.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                ]
        else :  #for all other MSSM scenarios except lowmH, lightstopmod and tauphobic
            if len(subvec(args,  90, 249))>0 :
                dirs = vec2str(subvec(args,  90,  249))
                grid = [
                    "{CMD} -n  6 --min  0.5  --max  1.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  4 --min  2.0  --max  8.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs) 
                    ,"{CMD} -n  3 --min  9.0  --max 15.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  3 --min 20.0  --max 30.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    #,"{CMD} -n  2 --min 35.0  --max 40.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    #,"{CMD} -n  2 --min 50.0  --max 60.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]
            if len(subvec(args, 250, 299))>0 :
                dirs = vec2str(subvec(args, 250,  299))
                grid = [
                    "{CMD} -n  2 --min  0.5  --max  1.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min  3.0  --max 15.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 20.0  --max 40.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    #,"{CMD} -n  2 --min 50.0  --max 60.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]                
            if len(subvec(args, 300, 399))>0 :
                dirs = vec2str(subvec(args, 300,  399))
                grid = [
                    "{CMD} -n  3 --min  2.0  --max 10.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 13.0  --max 25.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  3 --min 30.0  --max 40.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  2 --min 50.0  --max 60.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]                                
            if len(subvec(args, 400, 599))>0 :
                dirs = vec2str(subvec(args, 400,  599))
                grid = [
                    "{CMD} -n  3 --min  2.0  --max 10.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  2 --min 15.0  --max 20.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 25.0  --max 45.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  2 --min 50.0  --max 60.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]                                
            if len(subvec(args, 600, 1000))>0 :
                dirs = vec2str(subvec(args, 600, 1000))
                grid = [
                    "{CMD} -n  3 --min  2.0  --max 10.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  3 --min 15.0  --max 25.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  5 --min 30.0  --max 50.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ,"{CMD} -n  2 --min 55.0  --max 60.0 {SUB} {OPTS} {USER} {DIRS}".format(CMD=cmd, SUB=sub, OPTS=opt, USER=opt, DIRS=dirs)
                    ]
    return grid
