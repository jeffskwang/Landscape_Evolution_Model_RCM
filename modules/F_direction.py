import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)

def f_direction(eta,direction,slope,hole,direction_update):
        f_slope = [0.0 for i in xrange(0,8)]
        hole[0] = 0
        direction_update[0] = 0
	for x in xrange(x_lower,x_upper):
		for y in xrange(y_lower,y_upper):
			for i in xrange (0,8):
				f_slope[i]=(eta[x][y]-eta[x+xn[i]][y+yn[i]])/(dn[i])

			if max(f_slope) <= 0.0:
                                slope[x][y] = 0.0
                                direction[x][y] = -9999
                                hole[0] = 1
                        else:
                                max_slope = 0.0
                                max_slope_int = -9999
                                for i in xrange (0,8):
                                        if max_slope < f_slope[i]:
                                                max_slope_int = i
                                                max_slope = f_slope[i]
                                if direction[x][y] != max_slope_int:
                                        direction_update[0] = 1
                                direction[x][y] = max_slope_int
                                slope[x][y] = max_slope
	return direction, slope, hole, direction_update
