# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 13:29:38 2021

@author: Davide Aloi, PhD student - University of Birmingham
"""


#Imports to run the code
import os
from nilearn import image
from nilearn import plotting

import numpy as np
import pandas as pd
import time

## Files and parameters ##

#DTI files
main_folder = "C:\\Users\\davide\\Documents\\GitHub\\fmri_scripts\\dti" # Folder where you have your data (maps, atlas and csv file with labels)
dti_file = 'tbss_tfce_corrp_tstat1.nii' # This is your TFCE MAP 
dti_mean_FA = ''

#Background anatomical file
bck_img = 'MNI152_T1_1mm_Brain.nii'
bck_img_path = os.path.join(main_folder, bck_img) 
bck_img_data = image.load_img(bck_img_path) #load DTI file


# Atlas
atlas_file = 'JHU-ICBM-labels-1mm.nii' # This is the John Hopkins University Atlas (white matter) 
atlas_labels_file = 'atlas.csv' #Name of the CSV file with the lables (id = n roi in the atlas_file)
# Labels of the atlas
atlas_labels_path = os.path.join(main_folder,atlas_labels_file)
atlas_labels = pd.read_csv(atlas_labels_path)

# Threshold
th = 0.95 #threshold (1-p-val). This is the threshold used in the TFCE analysis. Values lower than this threshold are already not in the map

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



#Based on atlas_labels, I want to generate specific maps and tables for the tracts I'm interested in.

# Insert here the ID of the tracts you're interested in. You can group together multiple tracts.
# i.e. IDs corpus callosum = 3, 4, 5.
# IDs corticospinal tracts = 7, 8.

#This tells you the number os significant voxels. Helpful if you want to cross-check with FSL
num_sig_voxels = (dti_data > th).sum() 
print('Significant voxels (p<0.05): ' + str(num_sig_voxels))

tracts = [[3,4,5],[7,8],[11,12,13,14]]
csize = 20 #Custer size (this is just for the table) 

from nilearn.image import new_img_like
from nilearn.reporting import get_clusters_table 

all_tables = [] #Array containing all the output tables

for group_tracts in tracts:
    
    atlas_masked = np.where(np.in1d(atlas_data, group_tracts).reshape(atlas_data.shape)==True,1,0)
    atlas_masked = new_img_like(atlas, atlas_masked, affine=None, copy_header=True)
    #plotting.plot_roi(atlas_masked, bg_img = bck_img_data, colorbar = False, dim = -0.1,
     #                      draw_cross=False, black_bg=False, cmap = 'red_transparent')
                        
    dti_masked = image.math_img("img * img2", img=dti_map, img2 = atlas_masked) #Applying  mask
    
    this_table = get_clusters_table(dti_masked, stat_threshold=th,
                                    cluster_threshold=csize)
    
    this_table['Tracts'] = " ".join((atlas_labels['abbr'].loc[atlas_labels['id'].isin(group_tracts)].tolist()))

    all_tables.append(this_table)
    
for table in all_tables:
    print(table)
    
    
    
    
    
print('Exec time:' + str (time.time() - t))
dti_CC_bin = image.math_img("np.where((img > 0.95),1,0)", img=dti_CC)



# If you want to cross check that get_clusters_table is outputting the right results
# here's the same code but written by me (it's also faster)
from skimage import measure
from coord_matrix_mni import matrix_to_mni

t = time.time()
nclusters = 0
arr = measure.label(dti_CC_bin.get_fdata(), connectivity = 1)
peaks = []
coords = []
mni_coords = []
means = [] #This is calculated on the t-map but ideally you need the FA mean map (mean_FA)

for i in np.unique(arr[arr!=0]):
    #print('Analysing cluster ' + str(i))
    if (arr==i).sum()<csize:
        arr[arr==i] = 0
    else:
        nclusters +=1
        peaks.append(np.max(dti_CC.get_fdata()[arr==i]))
        means.append(np.mean(dti_CC.get_fdata()[arr==i]))
        this_coord = np.argmax(np.where(np.where(arr == i,True,False),dti_CC.get_fdata(),0))
        coords.append(np.unravel_index(this_coord,arr.shape))
        mni_coords.append(matrix_to_mni(np.array(coords[-1])+1,T=0)) #+1 because python indeces from 0
        
a = measure.regionprops(arr)


print('Exec time:' + str (time.time() - t))

#Results from get_clusters_table
print(tableCC)

#Results from my code
print('Total clusters: ' + str(nclusters))
for i in range(0,nclusters):
    print('Cluster ID: ' + str(i+1))
    print('Cluster size:' + str(a[i].area))
    print('Cluster Peak: ' + str(round(peaks[i],3)) + ' MNI:' + str(mni_coords[i]))





#plotting.plot_stat_map(atlas)
#plotting.plot_stat_map(atlas, colorbar = False,draw_cross=False, vmax = 1, cmap = 'red_transparent')
#plotting.plot_stat_map(dti_CC,colorbar = True,draw_cross=False, vmax = 1,cmap='winter_r')



