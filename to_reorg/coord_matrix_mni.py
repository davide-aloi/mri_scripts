# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 00:06:38 2021

@author: davide
"""

for i in range(0,len(table['Cluster Size (mm3)'])):
    
    coords = np.array([table['X'][i],table['Y'][i],table['Z'][i]])

    first_arg = np.transpose(np.linalg.inv(rot_mat))
    second_arg = (np.array([coords[0],coords[1],coords[2], 1]));
    
    mat_coord = np.dot(second_arg,first_arg);
    mat_coord = mat_coord[0:3];
    mat_coord = np.round(mat_coord[:]);#matrix coordinates for the MNI coordinates of the cluster

    label = atlas_data[int(mat_coord[0])-1,int(mat_coord[1])-1,int(mat_coord[2])-1]
    
    print('Cluster coordinate (MNI)')
    print(coords)
    print('Cluster coordinate (matrix space)')

    print(mat_coord)
    print('T value')
    print(dti_data[int(mat_coord[0])-1,int(mat_coord[1])-1,int(mat_coord[2])-1])
    print(atlas_data[int(mat_coord[0])-1,int(mat_coord[1])-1,int(mat_coord[2])-1])
    
    