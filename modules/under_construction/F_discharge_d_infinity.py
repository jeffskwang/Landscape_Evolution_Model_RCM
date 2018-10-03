import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)
import numpy as np

def f_discharge_d_infinity(discharge,area,eta_old,precipitation): #UPDATE SLOPE! RUN FASTER?
        facet_dir_1 = [3,1,1,4,3,6,6,4]
        facet_dir_2 = [0,0,2,2,5,5,7,7]
        facet_dir_1_to_2 = [1,3,4,1,6,3,4,6]
        
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
                
                f_r = [0.0 for i in xrange(0,8)]
                f_s = [0.0 for i in xrange(0,8)]

                slope_max = 0.0

                #This for loop is not the bottleneck 2.7 min vs 8 min, 0.2 min
##                for i in xrange (0,8):
##                        eta_0 = eta_old[x][y]
##                        eta_1 = eta_old[x+xn[facet_dir_1[i]]][y+yn[facet_dir_1[i]]]
##                        eta_2 = eta_old[x+xn[facet_dir_2[i]]][y+yn[facet_dir_2[i]]]
##
##                        d1 = dn[facet_dir_1[i]]
##                        d2 = dn[facet_dir_1_to_2[i]]
##                        
##                        s1 = max((eta_0 - eta_1) / d1,0.0)
##                        s2 = max((eta_1 - eta_2) / d2,0.0)
##
##                        diagonal_angle = np.arctan(d2/d1)
##                        diagonal_distance = (d1 ** 2.0 + d2 ** 2.0) ** 0.5
##
##                        if s1 == 0:
##                                f_r[i] = diagonal_angle
##                                f_s[i] = (eta_0 - eta_2) / diagonal_distance
##                        else:
##                                f_r[i] = np.arctan(s2/s1)
##                                f_s[i] = (s1 ** 2.0 + s2 ** 2.0) ** 0.5
##                                
##                                if f_r[i] < 0.0:
##                                        f_r[i] = 0.0
##                                        f_s[i] = s1
##                                        
##                                elif f_r[i] > diagonal_angle:
##                                        f_r[i] = diagonal_angle
##                                        f_s[i] = (eta_0 - eta_2) / diagonal_distance
##                        if f_s[i] > slope_max:
##                                slope_max = f_s[i]
##                                i_max = i
     
                #slope is right, parcel is correct? verything is r = pi/4
                #i_max = np.argmax(f_s) #ARGMAX SLOW?

                i_max = 6
                f_r[6] = np.pi / 8.
                f_s[6] = 0.001
                diagonal_angle = np.arctan(dy/dx)
                diagonal_distance = (dy ** 2.0 + dx ** 2.0) ** 0.5
                
                r_prime = f_r[i_max]
                s_prime = f_s[i_max]

                alpha_1 = r_prime
                alpha_2 = diagonal_angle - r_prime
                
                discharge[x][y] += precipitation[x][y] * dx * dy
                area[x][y] += dx * dy
                
                discharge[x+xn[facet_dir_1[i_max]]][y+yn[facet_dir_1[i_max]]] += discharge[x][y]* alpha_2 / diagonal_angle
                area[x+xn[facet_dir_1[i_max]]][y+yn[facet_dir_1[i_max]]] += area[x][y]* alpha_2 / diagonal_angle
                
                discharge[x+xn[facet_dir_2[i_max]]][y+yn[facet_dir_2[i_max]]] += discharge[x][y]* alpha_1 / diagonal_angle
                area[x+xn[facet_dir_2[i_max]]][y+yn[facet_dir_2[i_max]]] += area[x][y] * alpha_1 / diagonal_angle
                
	return discharge, area
