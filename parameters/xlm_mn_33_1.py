###PARAMETERS###
################
import sys
import os

##NUMERICAL PARAMETERS##
########################
#IO
output_folder = os.path.basename(__file__)[:-3]
input_file = ''#'sine_initial.asc'
precision = 0.00000000000000000000000000000000000000000000001
inclination_initial = 0.0

#controls
hole_function = 0 #1 is on , 0 is off
fill_holes = 0 #0 do not fill holes, 1 fills holes
diffusion_deposition = 1 #0 do not allow, 1 is allowed
lateral_incision_boolean = 0 #0 no lateral incision, 1 lateral incison is allowed

#outputs: 0- don't plot, 1 - plot
elevation_plot = 1
elevation_paraview_plot = 1
elevation_average_plot = 0
area_plot = 0
uplift_plot = 0
slope_plot = 0
direction_plot = 0
discharge_plot = 1
incision_plot = 1
lateral_incision_plot = 0
diffusion_plot = 0
precipitation_plot = 0
time_series_plot = 1

#number of plots
num_plots = 11 #plots

#units
time_unit = 'hr' #'sec' or 'hr' or 'yr'
length_unit = 'mm'#'mm' or 'm' or 'km'

#number of cells <---THIS WILL BE OVERWRITTEN IF THERE IS AN INPUT FILE
cellsx = 150
cellsy = 150

#time step
dt = 1.0 / 60. # time unit

#boundary conditions: 0-closed,1-open,2-periodic (NOTE: if top/bottom or left/right must both be 2 in order to work)
#list is top, bottom, left, right
BC = [0,1,0,0]
#can only be closed or open
nan_BC = 0

#initial conditions
rando_scale = 0.10 #length_unit
rando_seed = 43563

#hole functoin
hole_adjustment = 0.00000000000001

##PHYSICAL PARAMETERS##
#######################

#basin size  <---THIS WILL BE OVERWRITTEN IF THERE IS AN INPUT FILE
Lx = 500. # length unit
Ly = 500. # length unit

#simulation time
sim_time = 200. # time unit

#uplift rate
U = 10.185 #length unit / time unit

#stream power incision model
m = 0.33 #-
n = 1.0 #-
K = 0.9480175804516335/0.951534520548711/1.0151777690369757 #length unit ^ (1-3m) / time unit ^(1-m)
P = (39.70854912 + 37.94958792 + 36.36652284)/3.0 #length unit / time unit
P_rando_scale = 0.0

#lateral erosion component
m_l = 1.0
n_l = 1.0
Kl = K * 1.5
discharge_constant = 0.4
discharge_exponent = 0.35

#diffusion coefficient
D = 7.0 #length unit ^ (2) / time unit

###DO NOT MODIFY###
###################
time_series_header = 'time [s]\ttotal_relief [m]\tmean incision[m/s]\tmean diffusion [m/s]\tenergy expenditure [J/s]'

#time cells
cellst = int(round(sim_time / dt))

#plotting
dt_plot = sim_time / float(num_plots - 1)

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
P_rando_scale *= length_conversion/time_conversion
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

#plotting
x_plot = [0,Lx]
y_plot = [0,Ly]

#neighbors
xn = [-1,0,1,-1,1,-1,0,1]
yn = [1,1,1,0,0,-1,-1,-1]
dn = [(dx**2.0+dy**2.0)**0.5,dy,(dx**2.0+dy**2.0)**0.5,dx,dx,(dx**2.0+dy**2.0)**0.5,dy,(dx**2.0+dy**2.0)**0.5]
dop = [7,6,5,4,3,2,1,0]

#lateral node dictionary
#0|1|2
#3|x|4
#5|6|7
lateral_nodes = {'11': (0,2,0.23/dx),\
                 '33': (0,5,0.23/dx),\
                 '44': (2,7,0.23/dx),\
                 '66': (5,7,0.23/dx),\
                 '13': (1,1,1.37/dx),\
                 '14': (1,1,1.37/dx),\
                 '41': (4,4,1.37/dx),\
                 '46': (4,4,1.37/dx),\
                 '63': (6,6,1.37/dx),\
                 '64': (6,6,1.37/dx),\
                 '31': (3,3,1.37/dx),\
                 '36': (3,3,1.37/dx),\
                 '10': (1,1,0.67/dx),\
                 '12': (1,1,0.67/dx),\
                 '42': (4,4,0.67/dx),\
                 '47': (4,4,0.67/dx),\
                 '65': (6,6,0.67/dx),\
                 '67': (6,6,0.67/dx),\
                 '30': (3,3,0.67/dx),\
                 '35': (3,3,0.67/dx),\
                 '00': (1,3,0.23/dx),\
                 '22': (1,4,0.23/dx),\
                 '55': (3,6,0.23/dx),\
                 '77': (4,6,0.23/dx),\
                 '02': (0,0,1.37/dx),\
                 '05': (0,0,1.37/dx),\
                 '20': (2,2,1.37/dx),\
                 '27': (2,2,1.37/dx),\
                 '50': (5,5,1.37/dx),\
                 '57': (5,5,1.37/dx),\
                 '72': (7,7,1.37/dx),\
                 '75': (7,7,1.37/dx),\
                 '01': (0,0,0.67/dx),\
                 '03': (0,0,0.67/dx),\
                 '21': (2,2,0.67/dx),\
                 '24': (2,2,0.67/dx),\
                 '53': (5,5,0.67/dx),\
                 '56': (5,5,0.67/dx),\
                 '74': (7,7,0.67/dx),\
                 '76': (7,7,0.67/dx)}

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
