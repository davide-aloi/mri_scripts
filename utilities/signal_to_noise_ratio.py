"""
@author: Davide Aloi, PhD student - University of Birmingham
"""

def sig_to_noise_nifti(input_path, ROI_path=None, save_output=False):

    """
    Calculates the signal-to-noise ratio (SNR) of a functional scan. If a ROI is provided, the script applies the ROI to the scan before
    calculating the SNR

    input_path = path of the functional scan (nifti format)
    ROI_path = path of the ROI (if you're using one). Default = None
    save_output = save the masked file. Default = False

    Output: SNR (Mean/SD), mean and standard deviation
    """
    
    from nilearn import image
    import numpy as np

    #Loading functional scan
    input_image = image.load_img(input_path)
    input_image_data = input_image.get_fdata()

    #Loading ROI, if present
    if ROI_path != None:
        ROI_image = image.load_img(ROI_path)

        #Resampling ROI to functional scan
        from nilearn.image import resample_to_img
        ROI_image_resampled = resample_to_img(ROI_image, input_image, interpolation='nearest')
        ROI_image_data = np.where(ROI_image_resampled.get_fdata() > 0, 1, np.nan)

        #Applying ROI to input image
        for i in range(0,input_image_data.shape[3]):
            #print('Applying mask to volume: ' + str(i+1))
            input_image_data[:,:,:,i] = np.multiply(input_image_data[:,:,:,i], ROI_image_data)

    #Calculating mean and standard deviation
    mean = np.nanmean(input_image_data, 3)
    std = np.nanstd(input_image_data, 3)

    #Saving masked file
    if save_output == True:
        import nibabel as nib
        ni_img = nib.Nifti1Image(input_image_data, input_image.affine)
        nib.save(ni_img, input_path.split('/')[-1] + '_masked.nii')

    return np.nanmean(mean/std), mean, std
