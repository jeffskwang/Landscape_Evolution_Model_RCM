import sys
import os
import importlib
import numpy as np
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

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

#plot_function
def plot(plot_type,plot_num,slabel,normalize,log_scale):
    s = np.loadtxt(plot_type + '_'+ '%06d' % plot_num + '.asc', skiprows=6)
    s[s==-9999.]=np.nan
    plt.figure(1)
    if log_scale == 0:
        plt.imshow(np.rot90(s)/normalize,extent=[x_plot[0],x_plot[1],y_plot[0],y_plot[1]])
    elif log_scale == 1:
        s[s==0.0]=np.nan
        plt.imshow(np.rot90(np.log10(s/normalize)),extent=[x_plot[0],x_plot[1],y_plot[0],y_plot[1]])
    plt.xlabel('x ['+length_unit+']')
    plt.ylabel('y ['+length_unit+']')
    plt.title('Simulation time = ' + str(float(plot_num) * float(dt_plot)) + time_unit)
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
        plot('uplift',plot_numrr,r'$\upsilon$ ['+length_unit+'/'+time_unit+']',length_conversion/time_conversion,0)
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
    print str(int(float(plot_num)/float(num_plots - 1) * 1000.) / 10.) +'% done'
