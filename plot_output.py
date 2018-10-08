import sys
import os
import importlib
import numpy as np
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

from matplotlib.colors import LightSource
ls = LightSource(azdeg=315, altdeg=15)

#parent folder
output_folder = sys.argv[1]
parent_folder = os.getcwd()
sys.path.append(parent_folder +'/output/'+output_folder+'/input')
os.chdir(parent_folder +'/output/'+output_folder)

#get parameters file
for files_temp in os.listdir(parent_folder +'/output/'+output_folder+'/input'):
    if files_temp.endswith('.py'):
        parameters = importlib.import_module(files_temp[:-3])
        globals().update(parameters.__dict__)

#change of time unit
def time_unit_function(time_unit, time_unit_plot):
    if time_unit == 'sec' and time_unit_plot == 'sec':
        time_rescale = 1.0
    elif time_unit == 'sec' and time_unit_plot == 'hr':
        time_rescale = 1. / 3600.
    elif time_unit == 'sec' and time_unit_plot == 'day':
        time_rescale = 1. / 3600. / 24. 
    elif time_unit == 'sec' and time_unit_plot == 'yr':
        time_rescale = 1. / 3600. / 24. / 365.25
    elif time_unit == 'sec' and time_unit_plot == 'kyr':
        time_rescale = 1. / 3600. / 24. / 365.25 / 1000.
    elif time_unit == 'sec' and time_unit_plot == 'Myr':
        time_rescale = 1. / 3600. / 24. / 365.25 / 1000000.
    elif time_unit == 'sec' and time_unit_plot == 'Byr':
        time_rescale = 1. / 3600. / 24. / 365.25 / 1000000000.
        
    elif time_unit == 'hr' and time_unit_plot == 'sec':
        time_rescale = 3600.
    elif time_unit == 'hr' and time_unit_plot == 'hr':
        time_rescale = 1.
    elif time_unit == 'hr' and time_unit_plot == 'day':
        time_rescale = 1. / 24. 
    elif time_unit == 'hr' and time_unit_plot == 'yr':
        time_rescale = 1.  / 24. / 365.25
    elif time_unit == 'hr' and time_unit_plot == 'kyr':
        time_rescale = 1.  / 24. / 365.25 / 1000.
    elif time_unit == 'hr' and time_unit_plot == 'Myr':
        time_rescale = 1.  / 24. / 365.25 / 1000000.
    elif time_unit == 'hr' and time_unit_plot == 'Byr':
        time_rescale = 1.  / 24. / 365.25 / 1000000000.
        
    elif time_unit == 'day' and time_unit_plot == 'sec':
        time_rescale = 24. * 3600.
    elif time_unit == 'day' and time_unit_plot == 'hr':
        time_rescale = 24.
    elif time_unit == 'day' and time_unit_plot == 'day':
        time_rescale = 1.
    elif time_unit == 'day' and time_unit_plot == 'yr':
        time_rescale = 1. / 365.25
    elif time_unit == 'day' and time_unit_plot == 'kyr':
        time_rescale = 1. / 365.25 / 1000.
    elif time_unit == 'day' and time_unit_plot == 'Myr':
        time_rescale = 1. / 365.25 / 1000000.
    elif time_unit == 'day' and time_unit_plot == 'Byr':
        time_rescale = 1. / 365.25 / 1000000000.
        
    elif time_unit == 'yr' and time_unit_plot == 'sec':
        time_rescale = 3600. * 24. * 365.25
    elif time_unit == 'yr' and time_unit_plot == 'hr':
        time_rescale = 24. * 365.25
    elif time_unit == 'yr' and time_unit_plot == 'day':
        time_rescale = 365.25
    elif time_unit == 'yr' and time_unit_plot == 'yr':
        time_rescale = 1.
    elif time_unit == 'yr' and time_unit_plot == 'kyr':
        time_rescale = 1. / 1000.
    elif time_unit == 'yr' and time_unit_plot == 'Myr':
        time_rescale = 1. / 1000000.
    elif time_unit == 'yr' and time_unit_plot == 'Byr':
        time_rescale = 1. / 1000000000.
        
    return time_rescale
#plot_function
def plot(plot_type,plot_num,slabel,normalize,log_scale):
    s = np.loadtxt(plot_type + '_'+ '%06d' % plot_num + '.asc', skiprows=6)
    s[s==-9999.]=np.nan
    plt.figure(1)

    if plot_type == 'elevation':
        rgb = ls.shade(np.rot90(s)/normalize,cmap=cmap,blend_mode='soft',vert_exag=1,dx=dx,dy=dy)
        plt.imshow(rgb,extent=[x_plot[0],x_plot[1],y_plot[0],y_plot[1]])
        im_dummy = plt.imshow(np.rot90((s/normalize)), cmap=cmap, extent=[x_plot[0],x_plot[1],y_plot[0],y_plot[1]])
        im_dummy.remove()
    else:
        if log_scale == 0:
            plt.imshow(np.rot90(s)/normalize,extent=[x_plot[0],x_plot[1],y_plot[0],y_plot[1]])
        elif log_scale == 1:
            s[s==0.0]=np.nan
            plt.imshow(np.rot90(np.log10(s/normalize)),extent=[x_plot[0],x_plot[1],y_plot[0],y_plot[1]])
    plt.xlabel('x ['+length_unit+']')
    plt.ylabel('y ['+length_unit+']')

    time_rescale = time_unit_function(time_unit, time_unit_plot)
    
    plt.title('Simulation time = ' + str(float(plot_num) * float(dt_plot) * time_rescale)  + ' ' + time_unit_plot)

    if plot_type == 'elevation':
        plt.colorbar(im_dummy, label = slabel)
    else:
        plt.colorbar(label = slabel)
    plt.tight_layout()
    plt.savefig(plot_type + '_'+ '%06d' % plot_num + '.png',dpi=300)
    plt.clf()

#plot_paraview_function
def plot_paraview(plot_type,plot_num):
    if plot_num == 0 and input_file != '':
        os.chdir(parent_folder +'/output/'+output_folder+'/input')
        s = np.loadtxt(input_file, skiprows=6)
        s[s==-9999.]=np.nan
        os.chdir(parent_folder +'/output/'+output_folder)
    else:
        s = np.loadtxt(plot_type + '_'+ '%06d' % plot_num + '.asc', skiprows=6)
        s[s==-9999.]=np.nan

    xyz_data = np.zeros((cellsx * cellsy,4))

    dx_paraview = x_plot[1] / float(cellsx)
    dy_paraview = y_plot[1] / float(cellsy)
    x = np.linspace(dx_paraview / 2.0, x_plot[1] - dx_paraview / 2.0, cellsx)
    y = np.linspace(dy_paraview / 2.0, y_plot[1] - dy_paraview / 2.0, cellsy)
    
    k = 0
    for i in xrange(0,cellsx):
        for j in xrange(0,cellsy):
            xyz_data[k,0] = x[i]
            xyz_data[k,1] = y[j]
            xyz_data[k,2] = s[i,j]
            xyz_data[k,3] = s[i,j]
            k += 1
    np.savetxt(plot_type +'.csv.'+ '%06d' % (plot_num),xyz_data,delimiter=',',header= 'x, y, z, s', comments='')
 
def time_plot(plot_num,normalize,label,unit):
    s = np.loadtxt('_time_series.txt', skiprows=1)
    plt.figure(1)
    plt.plot(s[:,0]/time_conversion,s[:,plot_num]/normalize)
    plt.xlabel('t ['+time_unit+']')
    plt.ylabel(label + ' ['+unit+']')
    plt.tight_layout()
    plt.savefig('_' + label + '.png',dpi=300)
    plt.clf()
    
print 'plotting...'
cmap = matplotlib.cm.viridis
cmap.set_bad('k',1.)

for plot_num in xrange(0, num_plots):
    if elevation_plot == 1:
        plot('elevation',plot_num,r'$\eta$ ['+length_unit+']',length_conversion,0)
    if elevation_paraview_plot == 1:
        plot_paraview('elevation',plot_num)
    if elevation_average_plot == 1:
        plot('elevation_average',plot_num,r'$\eta$ ['+length_unit+']',length_conversion,0)
    if area_plot == 1:
        plot('area',plot_num,r'$A$ ['+length_unit+r'$^2$]',length_conversion * length_conversion,0)
    if uplift_plot == 1:
        plot('uplift',plot_num,r'$\upsilon$ ['+length_unit+'/'+time_unit+']',length_conversion/time_conversion,0)
    if slope_plot == 1:
        plot('slope',plot_num,r'$S$ [-]',1.0,0)
    if direction_plot == 1:
        plot('direction',plot_num,r'$direction$ [-]',1.0,0)
    if discharge_plot == 1:
        plot('discharge',plot_num,r'log($Q$) [-]',length_conversion * length_conversion* length_conversion / time_conversion,1)
    if incision_plot == 1:
        plot('incision',plot_num,r'$\epsilon/\upsilon$ [-]',U,0)
    if lateral_incision_plot == 1:
        plot('lateral_incision',plot_num,r'$\epsilon_l$ [-]',1,0)
    if diffusion_plot == 1:
        plot('diffusion',plot_num,r'$D/\upsilon$ [-]',U,0)
    if precipitation_plot == 1:
        plot('precipitation',plot_num,r'$P$ ['+length_unit+'/'+time_unit+']',length_conversion/time_conversion,0)
    #print str(int(float(plot_num)/float(num_plots - 1) * 1000.) / 10.) +'% done'

if time_series_plot == 1:
    time_plot(1,length_conversion,'relief',length_unit)
    time_plot(2,length_conversion/time_conversion,'mean incision',length_unit+'/'+time_unit)
    time_plot(3,length_conversion/time_conversion,'mean diffusion',length_unit+'/'+time_unit)
    time_plot(4,1,'energy expenditure','J/s')

print 'done'
