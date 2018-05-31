import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)

def f_update(eta_old, eta_new, area, discharge,incision,diffusion):
	for x in xrange(x_lower,x_upper):
		for y in xrange(y_lower,y_upper):
			eta_old[x][y] = eta_new[x][y]
	for x in xrange(0,cellsx+2):
		for y in xrange(0,cellsy+2):
			area[x][y] = 0.0
			discharge[x][y] = 0.0
			incision[x][y] = 0.0
			diffusion[x][y] = 0.0
	return eta_old, eta_new, area, discharge,incision,diffusion
			
