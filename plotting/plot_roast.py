import numpy as np
import nibabel as nib
from nilearn import image
import matplotlib.pyplot as plt

def roast_vector_sim(e: np.ndarray, e_mag: np.ndarray, mask: np.ndarray, vmin=0, vmax=0.35,
                     vmin_v=0.1, vmax_v=2, axis=2, which_slice=0, subsample=2, scale=3, figsize=(30, 30)):
    """
    Plot results from electric field maps generated by ROAST, masked using a brain mask.

    Parameters:
        e (np.ndarray): Electric field vectors map.
        e_mag (np.ndarray): Electric field magnitude map.
        mask (np.ndarray): Brain mask map. It should contain only 0 and 1. Used to mask the data.
        vmin (float, optional): Minimum value for electric field magnitude colormap. Default is 0.
        vmax (float, optional): Maximum value for electric field magnitude colormap. Default is 0.35.
        vmin_v (float, optional): Vectors with electric field magnitude below this threshold won't be shown.
                                  Default is 0.1.
        vmax_v (float, optional): Vectors with electric field magnitude above this threshold won't be shown.
                                  Default is 2.
        axis (int, optional): Which axis to plot. 0 = axial, 1 = coronal, 2 = sagittal. Default is 2.
        which_slice (int, optional): Slice of the scan to plot. Default is 0.
        subsample (int, optional): Remove vectors every N elements to avoid overcrowded plots. Default is 2.
        scale (int, optional): Factor of scale for the vectors. Higher -> smaller vectors. Default is 3.
        figsize (tuple, optional): Size of the matplotlib plot. Default is (30, 30).

    Returns:
        matplotlib.axes._subplots.AxesSubplot: The axis of the generated plot.

    Raises:
        Exception: Electric field map and mask should have the same dimension.
        Exception: Invalid axis. Axis can only be equal to 0 (x), 1 (y), or 2 (z).
        Exception: Slice chosen exceeds scan dimension on the chosen axis.
    """
    
    # Check if input dimensions match
    if (e.shape[0:3] != mask.shape != mask.shape):
        raise Exception("Electric field map and mask should have the same dimension.")

    # Check for valid axis value
    if not np.isin(axis, [0, 1, 2]):
        raise Exception("Invalid axis. Axis can only be equal to 0 (x), 1 (y), or 2 (z).")

    # Determine the slice to plot based on the chosen axis
    if e_mag.shape[axis] > which_slice:
        
        if axis == 0:  
            # Flipping left -> right (x axis)
            e_mag = np.flip(e_mag, 0)
            e = np.flip(e, 0)
            e_mag = np.where(mask[which_slice, :, :] != 0, e_mag[which_slice, :, :], 0)
            x = -e[which_slice, :, :, 0]
            y = -e[which_slice, :, :, 1]
            
        if axis == 1:
            e_mag = np.where(mask[:, which_slice, :] != 0, e_mag[:, which_slice, :], 0)
            e_mag = np.flip(np.rot90(e_mag), -1)  # Flipping x axis
            x = e[:, which_slice, :, 0]
            y = e[:, which_slice, :, 2]
            x = np.flip(np.rot90(x), -1)
            y = np.flip(np.rot90(y), -1)
            
        if axis == 2:
            e_mag = np.where(mask[:, :, which_slice] != 0, e_mag[:, :, which_slice], 0)
            e_mag = np.flip(e_mag, 0)  # Flipping y axis 
            x = np.flip(e[:, :, which_slice, 1], 0)
            y = np.flip(e[:, :, which_slice, 2], 0)

        # Subsample vectors and create a mask based on magnitude thresholds
        idxs = np.zeros(x.ravel().size, bool)
        idxs[::subsample] = 1
        idxs = np.where(((e_mag.ravel() > vmin_v) & (e_mag.ravel() < vmax_v)) & (idxs == 1), 1, 0)
        idxs = idxs.reshape(x.shape)
        x = np.where(idxs == 1, x, np.nan)
        y = np.where(idxs == 1, y, np.nan)

        # Plot the results
        f, ax = plt.subplots(figsize=figsize)
        ax.imshow(e_mag, cmap=plt.get_cmap('jet'), vmin=vmin, vmax=vmax)
        ax.quiver(x, y, scale=scale,
                  minlength=2,
                  headwidth=3, headlength=3, alpha=0.7,
                  linewidth=0.2)
        ax.axis('off')

        return ax

    else:
        raise Exception("Slice chosen exceeds scan dimension on the chosen axis ({}).\n"
                        "Scan shape: {}\n"
                        "Slice chosen: {}".format(axis, e_mag.shape, which_slice))
