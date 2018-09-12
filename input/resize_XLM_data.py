from scipy.interpolate import griddata
import numpy as np
import random

resize_x,resize_y = 150,150
resize = np.zeros((resize_x,resize_y)) 
resize_grid = np.zeros((resize_x*resize_y,2))
resize_unravel = np.zeros((resize_x*resize_y))
resize_grid_size_x = 0.5 / float(resize_x)
resize_grid_size_y = 0.5 / float(resize_y)

data_raw = np.loadtxt('_topo_0012.asc', skiprows=6)
data = data_raw[:,12:1012]
#data = np.rot90(np.rot90(data_raw[:,12:1012]))
data_grid_size = 0.0005
data_x,data_y =  data.shape
data_grid = np.zeros((data_x*data_y,2))
data_unravel = np.zeros((data_x*data_y))


for x in xrange(0,data_x):
    side_val = data[x,974]
    side_range = ((data[x,974] - data[x,975]) ** 2.0) ** 0.5
    for y in xrange(975,1000):
        data[x,y] = side_val + random.random() * side_range
        
for y in xrange(0,data_y):
    upper_val = data[50,y]
    upper_range = ((data[50,y] - data[49,y]) ** 2.0) ** 0.5
    lower_val = data[949,y]
    lower_range = ((data[949,y] - data[950,y]) ** 2.0) ** 0.5
    
    for x in xrange(0,50):
        data[x,y] = upper_val + random.random() * upper_range #- upper_range * (49. - float(x))
        
    for x in xrange(950,1000):
        data[x,y] = lower_val + random.random() * lower_range #- lower_range * (float(x) - 950.)
      
i = 0
for x in xrange(0,data_x):
    for y in xrange(0,data_y):
        data_grid[i,0] = data_grid_size / 2.0 + float(x) * data_grid_size
        data_grid[i,1] = data_grid_size / 2.0 + float(y) * data_grid_size
        data_unravel[i] = data[x,y]
        i += 1
i = 0
for x in xrange(0,resize_x):
    for y in xrange(0,resize_y):
        resize_grid[i,0] = resize_grid_size_x / 2.0 + float(x) * resize_grid_size_x
        resize_grid[i,1] = resize_grid_size_y / 2.0 + float(y) * resize_grid_size_y
        i += 1

resize_unravel = griddata(data_grid,data_unravel,resize_grid,method='cubic')
i = 0
for x in xrange(0,resize_x):
    for y in xrange(0,resize_y):
        resize[x,y] = (resize_unravel[i] - np.min(resize_unravel)) / 1000.
        i += 1
        
np.savetxt('resize.asc',resize,delimiter='\t',newline='\n',header= 'nrows\t'+str(resize_x)+'\ncellsize\t'+str(resize_grid_size_x)+'\nxllcorner\t0\nncols\t'+str(resize_y)+'\nyllcorner\t0\nNODATA_value\t-9999', comments='')
