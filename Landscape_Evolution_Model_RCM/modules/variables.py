import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)

eta_old = [[0. for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
eta_new = [[0. for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
eta_ghost = [[0. for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
slope = [[0. for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
direction = [[0 for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
area = [[0 for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
discharge = [[0.0 for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
incision = [[0. for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
diffusion = [[0. for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
precipitation = [[P for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
uplift = [[U for i in xrange(cellsy+2)]for j in xrange(cellsx+2)]
hole = [0]
