"""
@author: Davide Aloi - PhD student - University of Birmingham

Calculates MNI coordinates from matrix coordinates or matrix coordinates from MNI coordinates.
Input: MNI / matrix coordinates, and transformation / rotation matrix

Please, remember that python indices from 0, as such, you have to add + 1 to the resulting matrix coordinates 

"""

import numpy as np

def mni_to_matrix(mni_coords,T=None):
    # From MNI space to Matrix space

    if T==None:
        T = np.array([[-1 ,   0,     0,    91],
                      [ 0,     1,     0,  -127],
                      [ 0,     0,     1,   -73],
                      [ 0,     0,     0,     1]])

    first_arg = np.transpose(np.linalg.inv(T))
    second_arg = (np.array([mni_coords[0],mni_coords[1],mni_coords[2], 1]));

    mat_coord = np.dot(second_arg,first_arg);
    mat_coord = mat_coord[0:3];
    mat_coord = np.round(mat_coord[:]);

    return mat_coord


def matrix_to_mni(matrix_coord,T=None):
    # From matrix space to MNI space


    if T == None:
        T = np.array([[-1,   0,     0,    91],
                      [ 0,     1,     0,  -127],
                      [ 0,     0,     1,   -73],
                      [ 0,     0,     0,     1]])

        second_arg = np.array([matrix_coord[0],matrix_coord[1],matrix_coord[2], 1]);
        second_arg = np.reshape(second_arg,[-1,1])
        mni_coord = np.dot(T,second_arg)
        return np.reshape(mni_coord[0:3],[1,-1])