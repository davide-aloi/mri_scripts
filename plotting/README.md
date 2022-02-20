Plotting functions

1) plot_roast: plots ROAST results, masked using a brain mask.
Example:
```
# Plotting slice 68 of the coronal plane
fig = roast_vector_sim(e_v.get_fdata(), emag_map.get_fdata(), mask_touched.get_fdata(),
                 axis = 1, 
                 vmin = 0, vmax = 0.16,
                 vmax_v = 0.5,
                 subsample = 5,
                 vmin_v = 0.08,
                 which_slice = 68, #68
                 scale = 4,
                 figsize=(10,10))
plt.show(fig)
```
<img src="https://github.com/Davi93/mri_scripts/blob/main/plots/roast_plot.png" data-canonical-src="https://github.com/Davi93/mri_scripts/blob/main/plots/roast_plot.png" width="300" height="300" />
<img src="https://github.com/Davi93/mri_scripts/blob/main/plots/roast_plot2.png" data-canonical-src="https://github.com/Davi93/mri_scripts/blob/main/plots/roast_plot.png" width="300" height="300" />
<img src="https://github.com/Davi93/mri_scripts/blob/main/plots/roast_plot3.png" data-canonical-src="https://github.com/Davi93/mri_scripts/blob/main/plots/roast_plot.png" width="300" height="300" />


