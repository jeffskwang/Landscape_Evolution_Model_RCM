import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)
import numpy as np

def f_discharge_d8(discharge,area,direction,eta_old,precipitation):
        
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

                i = direction[x][y]
                                
                discharge[x][y] += precipitation[x][y] * dx * dy
                area[x][y] += dx * dy
                
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
                discharge[xloc][yloc] += discharge[x][y]
                area[xloc][yloc] += area[x][y]

	return discharge, area
