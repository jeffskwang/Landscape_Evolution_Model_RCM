import importlib
import sys
import random
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)

def f_lateral(discharge,lateral_incision,lateral_incision_cumulative,area,slope,direction,lateral_incision_threshold,eta_old):
	for x in xrange(x_lower,x_upper):
		for y in xrange(y_lower,y_upper):

                        #the cells at play
			x1 = x
			y1 = y
			
                        i1 = direction[x1][y1]
                        if y1 == cellsy and BC[0] == 1:
                                bingo = 1
                        elif y1 == 1 and BC[1] == 1:
                                bingo = 1
                        elif x1 == 1 and BC[2] == 1:
                                bingo = 1
                        elif x1 == cellsx and BC[3] == 1:
                                bingo = 1
                        elif i1 == -9999:
                                bingo = 1
			else:
                                x2 = x1 + xn[i1]
                                y2 = y1 + yn[i1]
                                
                                if BC[0] == 2 and BC[1] == 2:
                                        if y2 == cellsy+1:
                                                y2 = 1
                                        elif y2 == 0:
                                                y2 = cellsy
                                elif BC[2] == 2 and BC[3] == 2:
                                        if x2 == cellsx+1:
                                                x2 = 1
                                        elif x2 == 0:
                                                x2 = cellsx
                                                
                                lateral_incision_threshold[x1][y1] = (eta_old[x1][y1] - eta_old[x2][y2]) * dx * dy
                                i2 = direction[x2][y2]
                                
                                if y2 == cellsy and BC[0] == 1:
                                        bingo = 1
                                elif y2 == 1 and BC[1] == 1:
                                        bingo = 1
                                elif x2 == 1 and BC[2] == 1:
                                        bingo = 1
                                elif x2 == cellsx and BC[3] == 1:
                                        bingo = 1
                                elif i2 == -9999:
                                        bingo = 1
                                else:
                                        x3 = x2 + xn[i2]
                                        y3 = y2 + yn[i2]
                                        
                                        if BC[0] == 2 and BC[1] == 2:
                                                if y3 == cellsy+1:
                                                        y3 = 1
                                                elif y3 == 0:
                                                        y3 = cellsy
                                        elif BC[2] == 2 and BC[3] == 2:
                                                if x3 == cellsx+1:
                                                        x3 = 1
                                                elif x3 == 0:
                                                        x3 = cellsx

                                        #lateral node location                              
                                        curve = str(i1) + str(i2)
                                        lateral_node_direction = lateral_nodes[curve][int(0.5 + random.random())]
                                        xlat = x2 + xn[lateral_node_direction]
                                        ylat = y2 + yn[lateral_node_direction]
                                                
                                        if BC[0] == 2 and BC[1] == 2:
                                                if ylat == cellsy+1:
                                                        ylat = 1
                                                elif ylat == 0:
                                                        ylat = cellsy
                                        elif BC[2] == 2 and BC[3] == 2:
                                                if xlat == cellsx+1:
                                                        xlat = 1
                                                elif xlat == 0:
                                                        xlat = cellsx
                                
                                        if ylat == cellsy and BC[0] == 1:
                                                bingo = 1
                                        elif ylat == 1 and BC[1] == 1:
                                                bingo = 1
                                        elif xlat == 1 and BC[2] == 1:
                                                bingo = 1
                                        elif xlat == cellsx and BC[3] == 1:
                                                bingo = 1
                                        else:
                                                inverse_radius_curavture = lateral_nodes[curve][2]
                                                lateral_incision[xlat][ylat] = Kl *(discharge[x2][y2]**m_l)*(slope[x2][y2]**n_l) * inverse_radius_curavture * (discharge_constant * discharge[x2][y2] ** discharge_exponent * dx)
                                                lateral_incision_cumulative[xlat][ylat] += dt * Kl *(discharge[x2][y2]**m_l)*(slope[x2][y2]**n_l) * inverse_radius_curavture * (discharge_constant * discharge[x2][y2] ** discharge_exponent * dx)
                        
##                                                lateral_incision[xlat][ylat] = Kl *(discharge[x1][y1]**m_l)*(slope[x1][y1]**n_l) * inverse_radius_curavture * (discharge_constant * discharge[x1][y1] ** discharge_exponent * dx)
##                                                lateral_incision_cumulative[xlat][ylat] += dt * Kl *(discharge[x1][y1]**m_l)*(slope[x1][y1]**n_l) * inverse_radius_curavture * (discharge_constant * discharge[x1][y1] ** discharge_exponent * dx)
                        
	return lateral_incision,lateral_incision_cumulative, lateral_incision_threshold
