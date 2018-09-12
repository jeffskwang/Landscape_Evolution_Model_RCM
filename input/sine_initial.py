import numpy as np
import matplotlib.pyplot as plt
import random

Y_locations =[0.0,0.0,0.0,0.0]
zz = 0
W_list = (1.375* 2.54,1.125* 2.54,0.875* 2.54,0.625* 2.54)

x_test = np.linspace(0.,50.,10001)
y_L_test = np.zeros((10001,4))
y_U_test = np.zeros((10001,4))
TOP = np.zeros(10001) + 25.
BOTTOM = np.zeros(10001) - 25.
for W in W_list: 
    L = 50.
    wavelength = L * 2. / 3.
    amplitude = 10.
    padding = 2.0

    cells = 10001
    x = np.linspace(0. - padding,L+padding,cells)
    x_L = np.zeros(cells)
    y_L = np.zeros(cells)
    x_U = np.zeros(cells)
    y_U = np.zeros(cells)
    dx_array = np.zeros(cells)

    sine = amplitude * np.sin(np.pi * x / wavelength * 2.0)
    cosine = amplitude * np.cos(np.pi * x / wavelength * 2.0) * np.pi / wavelength * 2.0

    for i in xrange(0, cells):
        if np.abs(cosine[i]) == 0.0:
            dx = W / 2.0
            x_L[i] = x[i]
            x_U[i] = x[i]
            if sine[i] < 0.0:
                y_L[i] = sine[i] - W / 2.0
                y_U[i] = sine[i] + W / 2.0
            else:
                y_L[i] = sine[i] - W / 2.0
                y_U[i] = sine[i] + W / 2.0
        else:
            dx = (1. + 1. / (np.abs(cosine[i]) ** 2.0)) ** (-0.5) * W / 2.0
            if cosine[i] > 0.0:
                x_L[i] = x[i] + dx
                y_L[i] = sine[i] -  dx / np.abs(cosine[i])
                x_U[i] = x[i] - dx
                y_U[i] = sine[i] +  dx / np.abs(cosine[i])
            else:
                x_L[i] = x[i] - dx
                y_L[i] = sine[i] - dx / np.abs(cosine[i])
                x_U[i] = x[i] + dx
                y_U[i] = sine[i] +  dx / np.abs(cosine[i])

    plt.figure(1,facecolor='white')
    plt.axes().set_aspect('equal')
    
    #plt.plot(x_L,y_L,color=(0.,0.,0.),lw = line_width)
    #plt.plot(x_U,y_U,color=(0.,0.,0.),lw = line_width)
    y_L_test[:,zz] = np.interp(x_test,x_L,y_L)
    y_U_test[:,zz] = np.interp(x_test,x_U,y_U)
    #plt.plot(x_test,y_L_test,color=(0.,0.,0.),lw = line_width)
    #plt.plot(x_test,y_U_test,color=(0.,0.,0.),lw = line_width)
    zz += 1

color_levels = [1.0,0.75,0.5,0.25,0.0]
color_index = 0
plt.fill_between(x,y_U_test[:,0],TOP,color = (color_levels[color_index],color_levels[color_index],color_levels[color_index]))
color_index = 1
plt.fill_between(x,y_U_test[:,0],y_U_test[:,1],color = (color_levels[color_index],color_levels[color_index],color_levels[color_index]))
color_index = 2
plt.fill_between(x,y_U_test[:,1],y_U_test[:,2],color = (color_levels[color_index],color_levels[color_index],color_levels[color_index]))
color_index = 3
plt.fill_between(x,y_U_test[:,2],y_U_test[:,3],color = (color_levels[color_index],color_levels[color_index],color_levels[color_index]))
color_index = 4
plt.fill_between(x,y_L_test[:,3],y_U_test[:,3],color = (color_levels[color_index],color_levels[color_index],color_levels[color_index]))
color_index = 3
plt.fill_between(x,y_L_test[:,3],y_L_test[:,2],color = (color_levels[color_index],color_levels[color_index],color_levels[color_index]))
color_index = 2
plt.fill_between(x,y_L_test[:,2],y_L_test[:,1],color = (color_levels[color_index],color_levels[color_index],color_levels[color_index]))
color_index = 1
plt.fill_between(x,y_L_test[:,1],y_L_test[:,0],color = (color_levels[color_index],color_levels[color_index],color_levels[color_index]))
color_index = 0
plt.fill_between(x,y_L_test[:,0],BOTTOM,color = (color_levels[color_index],color_levels[color_index],color_levels[color_index]))
    
plt.ylim(-25.,25.)
plt.xlim(0.,50.)

resolution = 150
eta = np.zeros((resolution,resolution))
y = np.linspace(-25.,25.,resolution)
x = np.linspace(0.,50.,resolution)
levels = [0.0, -2.54 / 8., -2.54 / 8. * 2.,-2.54 / 8. * 3.,-2.54 / 8. * 4.]
for x_int in xrange(0,resolution):
    for y_int in xrange(0,resolution):
        y_value_8 = np.interp(x[x_int],x_test,y_U_test[:,0])
        y_value_7 = np.interp(x[x_int],x_test,y_U_test[:,1])
        y_value_6 = np.interp(x[x_int],x_test,y_U_test[:,2])
        y_value_5 = np.interp(x[x_int],x_test,y_U_test[:,3])
        y_value_4 = np.interp(x[x_int],x_test,y_L_test[:,3])
        y_value_3 = np.interp(x[x_int],x_test,y_L_test[:,2])
        y_value_2 = np.interp(x[x_int],x_test,y_L_test[:,1])
        y_value_1 = np.interp(x[x_int],x_test,y_L_test[:,0])

        if y[y_int] > y_value_8:
            eta[x_int,y_int] = levels[0]
        elif y[y_int] <= y_value_8 and y[y_int] > y_value_7:
            eta[x_int,y_int] = levels[1]
        elif y[y_int] <= y_value_7 and y[y_int] > y_value_6:
            eta[x_int,y_int] = levels[2]
        elif y[y_int] <= y_value_6 and y[y_int] > y_value_5:
            eta[x_int,y_int] = levels[3]
        elif y[y_int] <= y_value_5 and y[y_int] > y_value_4:
            eta[x_int,y_int] = levels[4]
        elif y[y_int] <= y_value_5 and y[y_int] > y_value_3:
            eta[x_int,y_int] = levels[3]
        elif y[y_int] <= y_value_5 and y[y_int] > y_value_2:
            eta[x_int,y_int] = levels[2]
        elif y[y_int] <= y_value_5 and y[y_int] > y_value_1:
            eta[x_int,y_int] = levels[1]
        elif y[y_int] <= y_value_1:
            eta[x_int,y_int] = levels[0]
        eta[x_int,y_int] /= 100.
        #eta[x_int,y_int] += (0.5 - random.random()) * 0.001
plt.figure(2,facecolor='white')
plt.axes().set_aspect('equal')
plt.pcolor(x,y,eta)
np.savetxt('sine_initial.asc',\
           np.flip(np.rot90(eta),0),delimiter='\t',newline='\n',header= 'nrows\t'+str(resolution)+'\ncellsize\t'+str(0.5 / float(resolution))\
           +'\nxllcorner\t0\nncols\t'+str(resolution)+'\nyllcorner\t0\nNODATA_value\t-9999', comments='')
#plt.show()
