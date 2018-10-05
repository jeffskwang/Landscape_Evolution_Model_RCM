import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)

def f_discharge_update(discharge, area):
	for x in xrange(0,cellsx+2):
		for y in xrange(0,cellsy+2):
                        area[x][y] = 0.0
			discharge[x][y] = 0.0
	return discharge, area
			
