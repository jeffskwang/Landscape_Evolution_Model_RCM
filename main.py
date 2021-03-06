#LEM written by Jeffrey Kwang 11/16/2014
#This reduced complexity model contains codes for a detachment limited & transport limited model
#importing libaries
import time
import os
import csv
import sys
import importlib
import shutil

#intialize
#start time
start_time = time.time()

#parent folder
parent_folder = os.getcwd()
sys.path.append(parent_folder +'/modules')
sys.path.append(parent_folder +'/parameters')

#cleanup
for files_temp in os.listdir(parent_folder+'/modules'):
    if files_temp.endswith('.pyc'):
        os.remove(parent_folder+'/modules/'+files_temp)
for files_temp in os.listdir(parent_folder+'/parameters'):
    if files_temp.endswith('.pyc'):
        os.remove(parent_folder+'/parameters/'+files_temp)

#parameters
parameters = importlib.import_module(sys.argv[1])
globals().update(parameters.__dict__)
if os.path.isdir(parent_folder+'/output/'+output_folder):
    shutil.rmtree(parent_folder+'/output/'+output_folder)
    time.sleep(5)
os.makedirs(parent_folder+'/output/'+output_folder)
os.makedirs(parent_folder+'/output/'+output_folder+'/input')
shutil.copyfile(parent_folder+'/parameters/'+sys.argv[1]+'.py',parent_folder+'/output/'+output_folder+'/input/'+sys.argv[1]+'.py')
if input_file != '':
    shutil.copyfile(parent_folder+'/input/'+input_file,parent_folder+'/output/'+output_folder+'/input/'+input_file)

#modules
from variables import *
from F_initial import *
from BC1 import *
from BC2 import *
from F_direction import *
from F_hole import *
from F_hole_update import *
from F_discharge import *
from F_discharge_update import *
##from F_discharge_d8 import *
##from F_discharge_bifurcation import *
##from F_discharge_d_infinity import *
from F_forward import *
from F_lateral import *
from F_update import *
from F_time_series import *
from F_time_series_print import *
from F_print import *

#Basic outline---functions
eta_old,eta_average = f_initial(eta_old,eta_average,parent_folder)

#main loop
number_of_holes = 0
for t in xrange (1,cellst+1):
    eta_old = f_bc1(eta_old)
    direction,slope,hole,direction_update = f_direction(eta_old,direction,slope,hole,direction_update)
    if hole[0] == 1 and hole_function == 1 and direction_update[0] == 1:
        number_of_holes += 1
        eta_ghost = f_hole(eta_old,eta_ghost,direction)
    	eta_ghost = f_bc1(eta_ghost)
        direction,slope,hole,direction_update = f_direction(eta_ghost,direction,slope,hole,direction_update)
        eta_old,slope = f_hole_update(eta_old,eta_ghost,slope)
##    if flow_type == 0:
##        discharge,area = f_discharge_d8(discharge,area,direction,eta_ghost,precipitation)
##    elif flow_type == 1:
##        discharge,area = f_discharge_bifurcation(discharge,area,eta_ghost,precipitation)
##    elif flow_type == 2:
##        discharge,area = f_discharge_d_infinity(discharge,area,eta_ghost,precipitation)
##    else:
    if direction_update[0] == 1:
        discharge,area = f_discharge_update(discharge, area)
        discharge,area = f_discharge(discharge,area,direction,precipitation)
        
    if lateral_incision_boolean == 1:
        lateral_incision,lateral_incision_cumulative,lateral_incision_threshold = f_lateral(discharge,lateral_incision,lateral_incision_cumulative,area,slope,direction,lateral_incision_threshold,eta_old)        
    eta_old = f_bc2(eta_old)
    eta_new,incision,diffusion,lateral_incision_cumulative = f_forward(eta_old,eta_temp,eta_new,discharge,slope,uplift,precipitation,incision,diffusion,lateral_incision_cumulative,lateral_incision_threshold,direction)
    if plot_array[t] != 0 or t == 1:
        if elevation_plot == 1:
            f_print(eta_new,'elevation',plot_array[t],parent_folder)
        if elevation_average_plot == 1:
            f_print(eta_average,'elevation_average',plot_array[t],parent_folder)
        if area_plot == 1:
            f_print(area,'area',plot_array[t],parent_folder)
        if uplift_plot == 1:
            f_print(uplift,'uplift',plot_array[t],parent_folder)
        if slope_plot == 1:
            f_print(slope,'slope',plot_array[t],parent_folder)
        if direction_plot == 1:
            f_print(direction,'direction',plot_array[t],parent_folder)
        if discharge_plot == 1:
            f_print(discharge,'discharge',plot_array[t],parent_folder)
        if incision_plot == 1:
            f_print(incision,'incision',plot_array[t],parent_folder)
        if lateral_incision_plot == 1:
            f_print(lateral_incision,'lateral_incision',plot_array[t],parent_folder)
        if diffusion_plot == 1:
            f_print(diffusion,'diffusion',plot_array[t],parent_folder)
        if precipitation_plot == 1:
            f_print(precipitation,'precipitation',plot_array[t],parent_folder)
        print str(int(float(t)/float(cellst) * 1000.) / 10.) +'% done'
    time_series = f_time_series(time_series,t,eta_old,incision,diffusion,direction,discharge,slope)
    eta_old, eta_temp, eta_new, eta_average,incision,lateral_incision,diffusion = f_update(eta_old,eta_temp, eta_new, eta_average,incision,lateral_incision,diffusion,t)

f_time_series_print(time_series,parent_folder)
#cleanup
for files_temp in os.listdir(parent_folder+'/modules'):
    if files_temp.endswith('.pyc'):
        os.remove(parent_folder+'/modules/'+files_temp)
for files_temp in os.listdir(parent_folder+'/parameters'):
    if files_temp.endswith('.pyc'):
        os.remove(parent_folder+'/parameters/'+files_temp)

stop_time = time.time()

print str(round((stop_time -start_time )/60.,1))+' mins'
