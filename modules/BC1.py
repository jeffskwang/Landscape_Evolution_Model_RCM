import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)

def f_bc1(eta):
        for i in xrange(0,4):
                if BC[i] == 0:
                        if i == 0:
                                for x in xrange(0,cellsx+2):
                                        eta[x][-1] = 1. * 10. ** (20.)
                        elif i == 1:
                                for x in xrange(0,cellsx+2):
                                        eta[x][0] = 1. * 10. ** (20.)
                        elif i == 2:
                                for y in xrange(0,cellsy+2):
                                        eta[0][y] =1. * 10. ** (20.)
                        elif i == 3:
                                for y in xrange(0,cellsy+2):
                                        eta[-1][y] = 1. * 10. ** (20.)
                elif BC[i] == 2:
                        if i == 0:
                                for x in xrange(0,cellsx+2):
                                        eta[x][-1] = eta[x][1]
                        elif i == 1:
                                for x in xrange(0,cellsx+2):
                                        eta[x][0] = eta[x][-2]
                        elif i == 2:
                                for y in xrange(0,cellsy+2):
                                        eta[0][y] = eta[-2][y]
                        elif i == 3:
                                for y in xrange(0,cellsy+2):
                                        eta[-1][y] = eta[1][y]
                
	return eta
