import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np
from read_tsa_img import read_data


def view_tsa_image(path):
    data = read_data(path)
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)

    def animate(i):
        im = ax.imshow(np.flipud(data[:, :, i].transpose()), cmap='viridis')
        return [im]

    return ani.FuncAnimation(fig, animate, frames=range(0, data.shape[2]), interval=200, blit=True)


# Those files can be download from Kaggle competition
#path = 'C:\\Users\\abelguima\\Google Drive\\sample\\0043db5e8c819bffc15261b1f1ac5e42.a3d'
path = 'C:\\Users\\abelguima\\Google Drive\\sample\\0043db5e8c819bffc15261b1f1ac5e42.aps'
animation = view_tsa_image(path)
plt.show()
