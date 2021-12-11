# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 00:06:38 2021

@author: davide
"""

import numpy as np

def mni_to_matrix(mni_coords,T=0):
    if T==0:
        T = np.array([[-1 ,   0,     0,    91],
                      [ 0,     1,     0,  -127],
                      [ 0,     0,     1,   -73],
                      [ 0,     0,     0,     1]])    

    first_arg = np.transpose(np.linalg.inv(T))
    second_arg = (np.array([mni_coords[0],mni_coords[1],mni_coords[2], 1]));
    
    mat_coord = np.dot(second_arg,first_arg);
    mat_coord = mat_coord[0:3];
    mat_coord = np.round(mat_coord[:]);#matrix coordinates for the MNI coordinates of the cluster
    
    return mat_coord


def matrix_to_mni(matrix_coord,T=0):
    if T == 0:
        T = np.array([[-4,   0,     0,    84],
                      [ 0,     4,     0,  -116],
                      [ 0,     0,     4,   -56],
                      [ 0,     0,     0,     1]])
        
        second_arg = np.array([matrix_coord[0],matrix_coord[1],matrix_coord[2], 1]);
        second_arg = np.reshape(second_arg,[-1,1])
        mni_coord = np.dot(T,second_arg)
        return np.reshape(mni_coord[0:3],[1,-1])
