import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)

def f_hole(eta_old,eta_ghost,direction):
        #stage 1
        for x in xrange(0,cellsx+2):
		for y in xrange(0,cellsy+2):
                        eta_ghost[x][y] = eta_old[x][y]
	for x in xrange(x_lower,x_upper):
		for y in xrange(y_lower,y_upper):
                        eta_ghost[x][y] = max(max(eta_old)) ** 2.0
        
        #stage 2
        epsilon = dx * 0.0001
        bingo = 0
        go = 0
        while bingo == 0:
                bingo = 1
                for y in xrange(y_lower,y_upper):
                        for x in xrange(x_lower,x_upper):
                                if eta_ghost[x][y] > eta_old[x][y]:
                                        for i in xrange (0,8):
                                                if eta_old[x][y] >= eta_ghost[x+xn[i]][y+yn[i]] + epsilon:
                                                        bingo = 2
                                        if bingo == 1:
                                                for i in xrange (0,8):
                                                        if eta_ghost[x][y] > eta_ghost[x+xn[i]][y+yn[i]] + epsilon:
                                                                eta_ghost[x][y] = eta_ghost[x+xn[i]][y+yn[i]] + epsilon
                                                                bingo = 0
                                        elif bingo == 2:
                                                eta_ghost[x][y] = eta_old[x][y]
                                                go += 1
                                                break
                        if bingo == 2:
                                break
                if bingo == 2:
                        bingo = 0                                  
	return eta_ghost
