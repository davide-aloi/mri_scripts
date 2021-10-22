# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 12:12:55 2021

@author: Davide Aloi, PhD student - University of Birmingham 
"""

from nilearn import image
import numpy as np

def sig_to_noise_nifti(input_path,ROI_path=None,save_output=False):
    
    """   
    Calculates the signal-to-noise ratio (SNR) of a functional scan. If a ROI is provided, the script applies the ROI to the scan before 
    calculating the SNR
    
    input_path = path of the functional scan (nifti format)
    ROI_path = path to the ROI (if you're using one). Default = None
    save_output = save the masked file. Default = False                           
    """
    
    #Loading functional scan
    input_image = image.load_img(input_path)
    input_image_data = input_image.get_fdata()

    #Loading ROI, if present
    if ROI_path != None:
        ROI_image = image.load_img(ROI_path)    
        
        #Resampling ROI to functional scan
        from nilearn.image import resample_to_img
        ROI_image_resampled = resample_to_img(ROI_image,input_image,interpolation='nearest')            
        ROI_image_data = np.where(ROI_image_resampled.get_fdata() > 0, 1, np.nan)
        
        #Applying ROI to input image
        for i in range(0,input_image_data.shape[3]):
            print('Applying mask to volume: ' + str(i))
            input_image_data[:,:,:,i] = np.multiply(input_image_data[:,:,:,i], ROI_image_data)
    
    #Calculating mean and standard deviation
    mean = np.nanmean(input_image_data,3)
    std = np.nanstd(input_image_data,3)
         
    #Saving masked file
    if save_output == True:
        image.math_img("img", img=input_image_data).to_filename(input_path.split('/')[-1] + '_masked.nii.gz')
    
    return np.nanmean(mean/std)