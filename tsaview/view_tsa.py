# *******************************************************************
# ** Guimaraes, Abel & Ghassem, Tofighi (2017)                     **                                                             **
# ** Implementing view image for Transport Security TSA analysis   **
# ** Python and scikits image script for digital image analysis    **                                                   **
# *******************************************************************

import matplotlib.animation as ani
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np

from skimage import measure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from numba import cuda


def view_animation_tsa_image(image_data, ax, fig):
    def animate(i):
        im = ax.imshow(np.flipud(image_data[:, :, i]), origin='upper', cmap='viridis')
        print(i)
        return [im]

    return ani.FuncAnimation(fig, animate, frames=range(0, image_data.shape[2]), interval=200, blit=True)


#@cuda.jit
def binarized_surface(data, ax, decorated_colors):
    """ Do a 3D plot of the surfaces in a binarized image

    The function does the plotting with scikit-image and some fancy
    commands that we don't need to worry about at the moment.
    """
    for i in range(1, np.size(decorated_colors)+1):
        index = np.where(data[:, :, :] == i)
        dat1 = np.zeros((np.shape(data)[0], np.shape(data)[1], np.shape(data)[2]))
        dat1[index[0], index[1], index[2]] = i
        if np.size(index[0]) > 0:
            vertices, faces, normals, values = measure.marching_cubes(dat1, 0.0)
            # Fancy indexing: `verts[faces]` to generate a collection of triangles
            mesh = Poly3DCollection(vertices[faces], linewidths=0, alpha=0.95)
            print(decorated_colors[i - 1])
            mesh.set_facecolor(decorated_colors[i - 1])
            ax.add_collection3d(mesh)
        else:
            print(i)

def plot_image(image_data, ax, fig, i):
    ax.imshow(np.flipud(image_data[:, :, i]), origin='lower', cmap='viridis')


#@jit
def get_view(data, view_type='surface', i=0, title=''):
    fig = plt.figure(figsize=(10, 10))
    plt.title(title)
    if view_type.__eq__('surface'):
        ax = fig.add_subplot(111, projection='3d')
        colors = ("red", "gold", "blue", "yellow", "brown", "orange", "cyan", "violet", "pink", "gray", "green",
                  "magenta", "indigo", "khaki", "coral", "cadetblue", "black")
        binarized_surface(data, ax, colors)
        ax.set_xlim(0, data.shape[0])
        ax.set_ylim(0, data.shape[1])
        ax.set_zlim(0, data.shape[2])
    elif view_type.__eq__('img'):
        ax = fig.add_subplot(111)
        ax.grid(False)
        loc = plticker.MultipleLocator(base=25)
        ax.xaxis.set_major_locator(loc)
        #ax.set_xlim(0, data.shape[0])
        ax.yaxis.set_major_locator(loc)
        #plt.ylim(0, data.shape[1])

        # Add the grid
        #ax.grid(which='major', axis='both', linestyle='-')
        plot_image(data, ax, fig, i)
    else:
        ax = fig.add_subplot(111)
        result = view_animation_tsa_image(data, ax, fig)

    plt.show()
