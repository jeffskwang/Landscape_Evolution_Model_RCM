import importlib
import sys
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)
import os
import numpy as np

def f_time_series_print(data,parent_folder):
        time_series_data_size = 5
        data_print = np.zeros((cellst,time_series_data_size))
        for t in xrange(0,cellsx):
                for j in xrange(0,time_series_data_size):
                        data_print[t,j] = data[t][j]
        np.savetxt(parent_folder+'/output/'+output_folder+'/'+ '_time_series.txt',data_print,delimiter='\t',newline='\n',header= 'nrows\t'+str(cellsx)+'\ncellsize\t'+str(dx)+'\nxllcorner\t0\nncols\t'+str(cellsy)+'\nyllcorner\t0\nNODATA_value\t-9999', comments='')
	return
