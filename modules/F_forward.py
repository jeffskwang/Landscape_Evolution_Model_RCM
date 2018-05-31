import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)

def f_forward(eta_old,eta_new,discharge,slope,uplift,precipitation,incision,diffusion,lateral_incision,lateral_incision_threshold,direction):
        for x in xrange(1,cellsx+1):
                eta_new[x][1] = eta_old[x][1]
                eta_new[x][cellsy] = eta_old[x][cellsy]
        for y in xrange(1,cellsy+1):
                eta_new[1][y] = eta_old[1][y]
                eta_new[cellsx][y] = eta_old[cellsx][y]
        
	for x in xrange(x_lower,x_upper):
		for y in xrange(y_lower,y_upper):
			diffusion[x][y]= D / (dx * dy)* \
			((eta_old[x-1][y]-2.*eta_old[x][y]+eta_old[x+1][y])+ \
			(eta_old[x][y-1]-2.*eta_old[x][y]+eta_old[x][y+1]))

			if diffusion[x][y] > 0.0 and diffusion_deposition == 0:
                                diffusion[x][y] = 0.0
			
			incision[x][y] = K *(discharge[x][y]**m)*(slope[x][y]**n)
			
			eta_new[x][y] = eta_old[x][y] + dt * (uplift[x][y] + diffusion[x][y] - incision[x][y])

        if lateral_incision_boolean == 1:
                for x in xrange(x_lower,x_upper):
                        for y in xrange(y_lower,y_upper):
                                if lateral_incision[x][y] > lateral_incision_threshold[x][y]:
                                        i = direction[x][y]
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
                                                        
                                        lateral_incision[x][y] = 0.0
                                        eta_new[x][y] = eta_new[xloc][yloc]	
                
	return eta_new,incision,diffusion
			
