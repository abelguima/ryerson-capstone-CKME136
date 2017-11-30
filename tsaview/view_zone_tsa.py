# *******************************************************************
# ** Guimaraes, Abel & Ghassem, Tofighi (2017)                     **                                                             **
# ** Implementing view image for Transport Security TSA analysis   **
# ** Python and scikits image script for digital image analysis    **                                                   **
# *******************************************************************

import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np

from skimage import measure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from numba import jit


def binarized_surface(data, ax, decorated_color):
    """ Do a 3D plot of the surfaces in a binarized image

    The function does the plotting with scikit-image and some fancy
    commands that we don't need to worry about at the moment.
    """
    vertices, faces, normals, values = measure.marching_cubes(data, 0.0)
    # Fancy indexing: `verts[faces]` to generate a collection of triangles
    mesh = Poly3DCollection(vertices[faces], linewidths=0, alpha=0.95)
    print(decorated_color)
    mesh.set_facecolor(decorated_color)
    ax.add_collection3d(mesh)


#@jit
def get_view(data, index_color=0):
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    colors = ("red", "gold", "blue", "yellow", "brown", "orange", "cyan", "violet", "pink", "gray", "green",
            "magenta", "indigo", "khaki", "coral", "cadetblue", "black")
    binarized_surface(data, ax, colors[index_color])
    ax.set_xlim(0, data.shape[0])
    ax.set_ylim(0, data.shape[1])
    ax.set_zlim(0, data.shape[2])
    plt.show()
