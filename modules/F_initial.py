import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)
import random
import numpy as np

def f_initial(eta,eta_average,parent_folder):
        random.seed(rando_seed)
        if input_file == '':
                for x in xrange (1,cellsx+1):
                        for y in xrange (1,cellsy+1):
                                eta[x][y] = random.random() * rando_scale  + inclination_initial * dy * float(y)
                                eta_average[x][y] = eta[x][y]
        else:
                if input_file.endswith('.asc'):
                        input_data = np.loadtxt(parent_folder+'/input/'+input_file, skiprows=6)
                        for x in xrange (1,cellsx+1):
                                for y in xrange (1,cellsy+1):
                                        eta[x][y] = int(input_data[x-1,y-1] / precision) * precision + inclination_initial * dy * float(y) + random.random() * rando_scale
                                        eta_average[x][y] = eta[x][y]
        return eta,eta_average

