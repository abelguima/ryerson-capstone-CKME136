import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
import tsabody.body as body

from skimage import measure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from numba import cuda


def view_animation_tsa_image(image_data, ax, fig):
    def animate(i):
        im = ax.imshow(np.flipud(image_data[:, :, i].transpose()), cmap='viridis')
        return [im]

    return ani.FuncAnimation(fig, animate, frames=range(0, image_data.shape[2]), interval=200, blit=True)


# @cuda.jit
def binarized_surface(data, ax, dcolors):
    """ Do a 3D plot of the surfaces in a binarized image

    The function does the plotting with scikit-image and some fancy
    commands that we don't need to worry about at the moment.
    """
    for i in range(1, 9):
        index = np.where(data[:, :, :] == i)
        dat1 = np.zeros((np.shape(data)[0], np.shape(data)[1], np.shape(data)[2]))
        dat1[index[0], index[1], index[2]] = i
        verts, faces, normals, values = measure.marching_cubes(dat1, 0.0)
        # Fancy indexing: `verts[faces]` to generate a collection of triangles
        mesh = Poly3DCollection(verts[faces], linewidths=0, alpha=0.7)
        mesh.set_facecolor(dcolors[i-1])
        ax.add_collection3d(mesh)


# @jit
def get_view(data, view_type='surface'):
    fig = plt.figure(figsize=(6, 6))
    if view_type.__eq__('surface'):
        ax = fig.add_subplot(111, projection='3d')
        colors = ("red", "green", "blue", "yellow", "brown", "orange", "cyan", "violet")  # , "pink")#, "gray")#, "fuchsia")
        binarized_surface(data, ax, colors)
        ax.set_xlim(0, data.shape[0])
        ax.set_ylim(0, data.shape[1])
        ax.set_zlim(0, data.shape[2])
    else:
        ax = fig.add_subplot(111)
        result = view_animation_tsa_image(data, ax, fig)
    plt.show()
