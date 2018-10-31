import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)
##import numpy

def f_time_series(time_series,t,eta_old,incision,diffusion,direction,discharge,slope):
        min_ele = eta_old[x_lower][y_lower]
        max_ele = eta_old[x_lower][y_lower]
        sum_incision = 0.0
        count_incision = 0
        sum_diffusion = 0.0
        count_diffusion = 0
        sum_energy = 0.0
	for x in xrange(x_lower,x_upper):
		for y in xrange(y_lower,y_upper):
                        #relief
                        if eta_old[x][y] > max_ele:
                                max_ele = eta_old[x][y]
                        if eta_old[x][y] < min_ele:
                                min_ele = eta_old[x][y]
                        #mean_incision
                        sum_incision += incision[x][y]
                        count_incision += 1
                        #mean_diffusion
                        sum_diffusion += diffusion[x][y]
                        count_diffusion += 1
                        #energy_expenditure
                        if direction[x][y] != -9999:
                                sum_energy += 1.0 * (discharge[x][y] ** 0.5) * dn[direction[x][y]]
        
        #time                
        time_series[t-1][0] = (t - 1) * dt
        #relief
        time_series[t-1][1] = max_ele - min_ele
        #mean_incision
        time_series[t-1][2] = sum_incision / float(count_incision)
        #mean_diffusion
        time_series[t-1][3] = sum_diffusion / float(count_diffusion)
        #energy_expenditure
        time_series[t-1][4] = sum_energy
##        #95 percentile of the elevation data
##        time_series[t-1][5] = numpy.percentile(eta_old,95)
        
	return time_series
			
