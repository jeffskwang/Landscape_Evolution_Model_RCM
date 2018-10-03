import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)
import numpy as np

def f_discharge_bifurcation(discharge,area,eta_old,precipitation):
        
        sort_int = 0
        eta_sort_list = np.zeros(((x_upper - x_lower)*(y_upper - y_lower)),dtype=int)        
	for x in xrange(x_lower,x_upper):
		for y in xrange(y_lower,y_upper):
                        eta_sort_list[sort_int] = eta_old[x][y]
                        sort_int += 1

        sorted_eta = np.flip(np.argsort(eta_sort_list),axis=0)
        
	for sort_int in sorted_eta:
                x = x_sort_list[sort_int]
                y = y_sort_list[sort_int]
                
                f_slope = [0.0 for i in xrange(0,8)]
                sum_slope = 0.0
                
                for i in xrange (0,8):
                        f_slope[i]=(eta_old[x][y]-eta_old[x+xn[i]][y+yn[i]])/(dn[i])
                        if f_slope[i] > 0.0:
                                sum_slope += f_slope[i]
                                
                discharge[x][y] += precipitation[x][y] * dx * dy
                area[x][y] += dx * dy
                
                for i in xrange (0,8):
                        if f_slope[i] > 0.0:
                               xloc = x + xn[i]
                               yloc = y + yn[i]
                               if BC[0] == 2 and BC[1] == 2:
                                       if yloc == cellsy+1:
                                               yloc = 1
                                       elif yloc == 0:
                                               yloc = cellsy
                               elif BC[2] == 2 and BC[3] == 2:
                                       if xloc == cellsx+1:
                                               xloc = 1
                                       elif xloc == 0:
                                               xloc = cellsx
                               discharge[xloc][yloc] += discharge[x][y] * f_slope[i] / sum_slope 
                               area[xloc][yloc] += area[x][y] * f_slope[i] / sum_slope 

	return discharge, area
