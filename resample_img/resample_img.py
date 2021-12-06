# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 13:29:38 2021

@author: Davide Aloi
"""


import os
from nilearn import image

main_folder = ""
output_path = ""
func_file = "" # func file
mask = ""

# func path
func_map = os.path.join(main_folder, func_file) #path to func file

# Loading func
func_map = image.load_img(func_map) #load func file

# mask path
mask_map = os.path.join(main_folder,mask)

# Loading mask
mask_map = image.load_img(mask_map) # left thalamus


from nilearn.image import resample_to_img
mask_resampled = resample_to_img(mask_map,func_map)

print('Your old mask has a shape of\n')
print(mask_map.get_fdata().shape)

print('Your functional file has a shape of\n')
print(func_map.get_fdata().shape)

print('Your new mask  has a shape of\n')
print(mask_resampled.get_fdata().shape)

#Saving everything

image.math_img("img", img=mask_resampled).to_filename('maskxsabri.nii.gz')



