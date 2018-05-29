###PARAMETERS###
################
import sys
import os

##NUMERICAL PARAMETERS##
########################
#IO
output_folder = os.path.basename(__file__)[:-3]
input_file = ''

#controls
hole_function = 1 #1 is on , 0 is off
diffusion_deposition = 0 #0 do not allow, 1 is allow

#outputs: 0- don't plot, 1 - plot
elevation_plot = 1
area_plot = 0
uplift_plot = 0
slope_plot = 0
direction_plot = 0
discharge_plot = 1
incision_plot = 0
diffusion_plot = 0
precipitation_plot = 0

#number of plots
    
num_plots = 6 #plots

#units
time_unit = 'yr' #'sec' or 'hr' or 'yr'
length_unit = 'm'#'mm' or 'm' or 'km'

#number of cells <---THIS WILL BE OVERWRITTEN IF THERE IS AN INPUT FILE
cellsx = 100
cellsy = 100

#time step
dt = 100. # time unit

#boundary conditions: 0-closed,1-open,2-periodic (NOTE: if top/bottom or left/right must both be 2 in order to work)
#list is top, bottom, left, right
BC = [1,1,2,2]
#can only be closed or open
nan_BC = 0

#initial conditions
rando_scale = 1. #length_unit
rando_seed = 13

##PHYSICAL PARAMETERS##
#######################

#basin size  <---THIS WILL BE OVERWRITTEN IF THERE IS AN INPUT FILE
Lx = 1000. # length unit
Ly = 1000. # length unit

#simulation time
sim_time = 1. * 10. ** (6.) # time unit

#uplift rate
U = 0.001 #length unit / time unit

#stream power incision model
m = 0.5 #-
n = 1.0 #-
K = 1.0 * 10. ** (-4.) #length unit ^ (1-3m) / time unit ^(1-m)
P = 1.0 #length unit / time unit

#lateral erosion component
Kl = K * 1.0

#diffusion coefficient
D = 0.0 #length unit ^ (2) / time unit

###DO NOT MODIFY###
###################
#time cells
cellst = int(round(sim_time / dt))

#plotting
dt_plot = sim_time / float(num_plots - 1)
x_plot = [0,Lx]
y_plot = [0,Ly]

#plot array
plot_array = [0 for i in xrange(0,cellst + 1)]
for i in xrange (1,num_plots):
    plot_array[(cellst) * i / (num_plots - 1)] = i
    
#grid size  <---THIS WILL BE OVERWRITTEN IF THERE IS AN INPUT FILE
dx = Lx/cellsx#m
dy = Ly/cellsy#m
    
#conversion to meters and seconds
if time_unit == 'yr':
    time_conversion = 365.25 * 24. * 3600.
elif time_unit == 'hr':
    time_conversion = 3600.
elif time_unit == 'sec':
    time_conversion = 1.0
else:
    sys.exit('invalid time unit')
        
if length_unit == 'mm':
    length_conversion = 0.001    
elif length_unit == 'm':
    length_conversion = 1.0    
elif length_unit == 'km':
    length_conversion = 1000.0    
else:
    sys.exit('invalid length unit')

dt *= time_conversion
dx *= length_conversion
dy *= length_conversion
Lx *= length_conversion
Ly *= length_conversion
sim_time *= time_conversion
U *= length_conversion/time_conversion
K *= (length_conversion**(1. - 3. * m))/(time_conversion**(1. - m))
P *= length_conversion/time_conversion
D *= length_conversion*length_conversion/time_conversion
rando_scale *= length_conversion

#input file parameters
import os
if input_file != '':
    with open(os.getcwd() + '/input/' + input_file, 'r') as f:
        for i in range(6):
            key, val = f.readline().split()
            if key == 'ncols':
                cellsy = int(val)
            elif key == 'nrows':
                cellsx = int(val)
            elif key == 'cellsize':
                dx = dy = float(val)
            elif key == 'NODATA_value':
                nan_val = int(val)
    Lx = float(cellsx) * dx
    Ly = float(cellsy) * dy

#neighbors
xn = [-1,0,1,-1,1,-1,0,1]
yn = [1,1,1,0,0,-1,-1,-1]
dn = [(dx**2.0+dy**2.0)**0.5,dy,(dx**2.0+dy**2.0)**0.5,dx,dx,(dx**2.0+dy**2.0)**0.5,dy,(dx**2.0+dy**2.0)**0.5]
dop = [7,6,5,4,3,2,1,0]

#lateral node dictionary
lateral_nodes = {'11': (0,2)\
                 '33': (0,5)\
                 '44': (2,7)\
                 '66': (5,7)\
                 '13': (1,1)\
                 '14': (1,1)\
                 '41': (4,4)\
                 '46': (4,4)\
                 '63': (6,6)\
                 '64': (6,6)\
                 '31': (3,3)\
                 '36': (3,3)\
                 '10': (1,1)\
                 '12': (1,1)\
                 '42': (4,4)\
                 '47': (4,4)\
                 '65': (6,6)\
                 '67': (6,6)\
                 '30': (3,3)\
                 '35': (3,3)\
                 '00': (1,3)\
                 '22': (1,4)\
                 '55': (3,6)\
                 '77': (4,6)\
                 '02': (0,0)\
                 '05': (0,0)\
                 '20': (2,2)\
                 '27': (2,2)\
                 '50': (5,5)\
                 '57': (5,5)\
                 '72': (7,7)\
                 '75': (7,7)\
                 '01': (0,0)\
                 '03': (0,0)\
                 '21': (2,2)\
                 '24': (2,2)\
                 '53': (5,5)\
                 '56': (5,5)\
                 '74': (7,7)\
                 '76': (7,7)}

#boundary conditions
x_lower = 1
x_upper = cellsx+1
y_lower = 1
y_upper = cellsy+1

if BC[0] == 1:
    y_upper = cellsy
if BC[1] == 1:
    y_lower = 2
if BC[2] == 1:
    x_lower = 2
if BC[3] == 1:
    x_upper = cellsx
