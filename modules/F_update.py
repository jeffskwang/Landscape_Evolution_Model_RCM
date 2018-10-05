import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)

def f_update(eta_old,eta_temp,eta_new,eta_average,incision,lateral_incision,diffusion,t):
	for x in xrange(x_lower,x_upper):
		for y in xrange(y_lower,y_upper):
                        eta_average[x][y] = (eta_average[x][y] * float(t) + eta_new[x][y]) / float(t + 1)
			eta_old[x][y] = eta_new[x][y]
	for x in xrange(0,cellsx+2):
		for y in xrange(0,cellsy+2):
			eta_temp[x][y] = 0.0
			incision[x][y] = 0.0
			lateral_incision[x][y] = 0.0
			diffusion[x][y] = 0.0
	return eta_old,eta_temp,eta_new,eta_average,incision,lateral_incision,diffusion
			
