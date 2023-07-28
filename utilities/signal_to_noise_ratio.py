"""
@author: Davide Aloi, PhD student - University of Birmingham
"""

def sig_to_noise_nifti(input_path, ROI_path=None, save_output=False):

    """
    sig_to_noise_nifti Function
    
    Calculates the signal-to-noise ratio (SNR) of a functional MRI (fMRI) scan, with the option to apply a region of interest (ROI) mask for localized SNR computation.
    
    Parameters:
        input_path (str): Path of the functional scan in NIfTI format (.nii or .nii.gz).
        ROI_path (str or None, optional): Path of the ROI file in NIfTI format (.nii or .nii.gz). If provided, the ROI will be applied to the functional scan before calculating SNR. Default is None.
        save_output (bool, optional): Whether to save the masked file. If True, the masked functional scan will be saved with a filename appended with '_masked.nii'. Default is False.
    
    Returns:
        snr_ratio (float): The calculated signal-to-noise ratio (SNR) represented as the mean divided by the standard deviation across all volumes.
        mean (ndarray): A 3D numpy array representing the mean of the functional scan across time (volumes).
        std (ndarray): A 3D numpy array representing the standard deviation of the functional scan across time (volumes).
    
    Notes:
    - The input_path should point to the functional scan (4D NIfTI file) with dimensions (x, y, z, t), where (x, y, z) are the spatial dimensions and 't' is the time dimension (number of volumes).
    - If a ROI_path is provided, the ROI will be resampled to match the spatial dimensions of the functional scan using nearest-neighbor interpolation.
    - The ROI will then be applied to the functional scan, keeping the voxels within the ROI and setting voxels outside the ROI to NaN.
    - SNR is computed as the ratio of the mean and standard deviation of the functional scan after applying the ROI mask.
    - NaN values resulting from the ROI masking are excluded from SNR computation.
    - The mean and standard deviation arrays represent the mean and standard deviation of the functional scan across the time dimension (volumes) at each voxel.
    - If save_output is set to True, the masked functional scan will be saved as a NIfTI file in the same directory as the input_path with '_masked.nii' appended to the original filename.
    
    Example:
        snr, mean, std = sig_to_noise_nifti('func_scan.nii', ROI_path='roi_mask.nii', save_output=True)
    
    Author:
    Davide Aloi, PhD student - University of Birmingham
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
