# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 16:07:30 2021

@author: davide
"""

## Export all regions from JHU atlas ##

import os
from nilearn import image
import numpy as np

## Files and parameters ##
main_folder = "C:\\Users\\davide\\Documents\\GitHub\\fmri_scripts\\dti" # Folder where you have your data (maps, atlas and csv file with labels)

# Atlas
atlas_path = os.path.join(main_folder, 'JHU-ICBM-labels-1mm.nii' ) #path to atlas file
atlas = image.load_img(atlas_path) #load atlas 
atlas_data = atlas.get_fdata() #atlas in numpy.array format

masks = np.unique(atlas_data[atlas_data!=0]) #List of tracts

from nilearn.image import new_img_like
for mask in masks:
    masked_map = np.where(atlas_data == mask,1,0)
    atlas_masked = new_img_like(atlas, masked_map, affine=None, copy_header=True) #Create new image with only one tract
    atlas_masked.to_filename('JHU_label_' + str(int(mask)) + '.nii')
    