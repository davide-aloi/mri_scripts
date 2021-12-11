# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 13:29:38 2021

@author: Davide Aloi, PhD student - University of Birmingham
"""


#Imports to run the code
import os
from nilearn import image
import numpy as np
import pandas as pd
from nilearn.reporting import get_clusters_table


## Files and parameters ##
#DTI files
main_folder = "C:\\Users\\davide\\Desktop" # Folder where you have your data (maps, atlas and csv file with labels)
dti_file = 'tbss_tfce_corrp_tstat1.nii' # This is your TFCE MAP 
dti_mean_FA = ''
# Atlas
atlas_file = 'JHU-ICBM-labels-1mm.nii' # This is the John Hopkins University Atlas (white matter) 
atlas_labels_file = 'atlas.csv' #Name of the CSV file with the lables (id = n roi in the atlas_file)
# Labels of the atlas
atlas_labels_path = os.path.join(main_folder,atlas_labels_file)
atlas_labels = pd.read_csv(atlas_labels_path)

# Threshold
th = 0.950 #threshold (1-p-val). This is the threshold used in the TFCE analysis. Values lower than this threshold are already not in the map

## Loading files ##
# DTI TFCE MAP
dti_map_path = os.path.join(main_folder, dti_file) #path to DTI  file
dti_map = image.load_img(dti_map_path) #load DTI file
dti_data = dti_map.get_fdata() #data in numpy.array format (not used but you can take a look to see what your data looks like)

# Atlas
atlas_path = os.path.join(main_folder, atlas_file) #path to atlas file
atlas = image.load_img(atlas_path) #load atlas 
atlas_data = atlas.get_fdata() #atlas in numpy.array format
#atlas_data is just an image with values that are either 0 or a
#number from 1 to 48 (that corresponds to the areas in the db atlas_labels)
#i.e. voxels with values = 3 correspond to the Genu of Corpus callosum (id 3 in atlas_labels)

num_sig_voxels = (dti_data > th).sum()
print('Significant voxels (p<0.05): ' + str(num_sig_voxels))





atlasCC = image.math_img("np.where((img > 2)&(img < 6),1,0)", img=atlas)
dti_CC = image.math_img("img * img2", img=dti_map, img2 = atlasCC) #Applying  mask

#dti_CC_norm = image.math_img("img * img2", img=dti_map) #Applying  mask



csize = 20    
tableCC = get_clusters_table(dti_CC, stat_threshold=th,
                           cluster_threshold=csize)    


import skimage
nclusters = 0
arr = measure.label(np.where(dti_CC.get_fdata()>th,1,0),connectivity = 1)

for i in np.unique(arr):
    if (arr==i).sum()<csize:
        nclusters +=1
        arr[arr==i] = 0
        
a = measure.regionprops(arr)

for i in (a):
    print(i.area)





from nilearn import plotting
plotting.plot_stat_map(atlas)
plotting.plot_stat_map(atlas, colorbar = False, vmax = 1, cmap = 'red_transparent')
plotting.plot_stat_map(dti_CC,colorbar = True, vmax = 1,cmap='winter')



