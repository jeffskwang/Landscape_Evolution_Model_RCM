import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)
import random
import numpy as np

def f_initial(eta,parent_folder):
        if input_file == '':
                random.seed(rando_seed)
                for x in xrange (1,cellsx+1):
                        for y in xrange (1,cellsy+1):
                                eta[x][y] = random.random() * rando_scale
                        
        else:
                if input_file.endswith('.asc'):
                        input_data = np.loadtxt(parent_folder+'/input/'+input_file, skiprows=6)
                        for x in xrange (1,cellsx+1):
                                for y in xrange (1,cellsy+1):
                                        eta[x][y] = input_data[x-1,y-1]
        return eta

