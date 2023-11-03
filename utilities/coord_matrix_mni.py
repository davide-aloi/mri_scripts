import numpy as np


import numpy as np


def mni_to_matrix(mni_coords, T):
    """
    Converts MNI coordinates to matrix coordinates using the transformation matrix T.

    Args:
    - mni_coords (list): A list of 3 floats representing the MNI coordinates.
    - T (numpy.ndarray): A 4x4 transformation matrix.

    Returns:
    - mat_coord (numpy.ndarray): A 3x1 numpy array representing the matrix coordinates.
    """
    # From MNI space to Matrix space
    first_arg = np.transpose(np.linalg.inv(T))
    second_arg = np.array([mni_coords[0], mni_coords[1], mni_coords[2], 1])
    mat_coord = np.dot(second_arg, first_arg)
    mat_coord = mat_coord[0:3]
    mat_coord = np.round(mat_coord[:])

    return mat_coord


def matrix_to_mni(matrix_coord, T):
    """
    Converts a matrix coordinate to MNI coordinate using a transformation matrix.

    Args:
        matrix_coord (list): A list of 3 integers representing the matrix coordinate.
        T (numpy.ndarray): A 4x4 transformation matrix.

    Returns:
        numpy.ndarray: A 1x3 array representing the MNI coordinate.
    """
    second_arg = np.array([matrix_coord[0], matrix_coord[1], matrix_coord[2], 1])
    second_arg = np.reshape(second_arg, [-1, 1])
    mni_coord = np.dot(T, second_arg)

    return np.reshape(mni_coord[0:3], [1, -1])
