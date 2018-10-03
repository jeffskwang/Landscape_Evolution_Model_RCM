import importlib
import sys
import random
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)

eta_old = [[0. for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
eta_new = [[0. for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
eta_temp = [[0. for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
eta_ghost = [[0. for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
eta_average = [[0. for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
slope = [[0. for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
direction = [[0 for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
area = [[0 for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
discharge = [[0.0 for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
incision = [[0. for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
diffusion = [[0. for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
precipitation = [[P for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
lateral_incision = [[0. for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
lateral_incision_cumulative = [[0. for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
lateral_incision_threshold = [[0. for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
uplift = [[U for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]

#0:time, 1:total relief, 2:average incision, 3:average diffusion, 4:energy expenditure
time_series = [[0.0 for i in xrange(5)]for j in xrange(cellst)]

hole = [0]

#precipitation
for x in xrange (1,cellsx+1):
        for y in xrange (1,cellsy+1):
                precipitation[x][y] += 2.0 * (0.5 - random.random()) * P_rando_scale
