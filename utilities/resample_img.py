"""
@author: Davide Aloi, PhD student - University of Birmingham

Simple example on how to resample a mask file to a functional or structural file, using nilearn
"""

import os
from nilearn import image

main_folder = ""
output_path = ""
output_fname = "" #name of the resampled mask image
func_file = "" # Functional / structural file
mask = ""

# func path
func_map = os.path.join(main_folder, func_file) #path to functional / structural file
func_map = image.load_img(func_map)

# mask path
mask_map = os.path.join(main_folder,mask) #Path to mask
mask_map = image.load_img(mask_map)


from nilearn.image import resample_to_img
mask_resampled = resample_to_img(mask_map,func_map)

print('Your old mask has a shape of\n')
print(mask_map.get_fdata().shape)

print('Your functional file has a shape of\n')
print(func_map.get_fdata().shape)

print('Your new mask  has a shape of\n')
print(mask_resampled.get_fdata().shape)

#Saving everything
image.math_img("img", img=mask_resampled).to_filename(output_fname)
