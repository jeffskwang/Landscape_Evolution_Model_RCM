import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)

def f_hole_update(eta_old,eta_ghost):
        for x in xrange(0,cellsx+2):
		for y in xrange(0,cellsy+2):
                        eta_old[x][y] = eta_ghost[x][y]                               
	return eta_old
