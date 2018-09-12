from tempfile import mkstemp
from shutil import move
from os import fdopen, remove

import numpy as np
mn_list_a = np.loadtxt('_a_mn_list.txt')
mn_list_b = np.loadtxt('_b_mn_list.txt')
mn_list_c = np.loadtxt('_c_mn_list.txt')

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

import os
import shutil
parent = os.getcwd()
seed_list = [43563,226,27,89,1234]
j = 1
for i in xrange (25,37):
    shutil.copyfile(parent + '//xlm_example.py',parent +'//xlm_mn_'+str(i)+'_'+str(j)+'.py')
    replace(parent + '//xlm_mn_'+str(i)+'_'+str(j)+'.py','m = 0.32','m = 0.'+str(i))
    replace(parent + '//xlm_mn_'+str(i)+'_'+str(j)+'.py','K = 1.25','K = '+str(mn_list_a[i-25]) + '/' +str(mn_list_b[i-25])+ '/' +str(mn_list_c[i-25])) 
    replace(parent + '//xlm_mn_'+str(i)+'_'+str(j)+'.py','rando_seed = 1234','rando_seed = '+str(seed_list[j-1]))
        
