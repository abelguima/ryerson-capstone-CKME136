import numpy as np


def setZonesBody(data):
    p = np.int64(np.max(np.where(data[:, :, :] > 0)) / 8)
    b = np.int64(np.shape(data)[1] / 2)
    data[np.where(data[:b, :, :] == 1)] = 10
    data[np.where(data[:, :, :] == 1)] = 11
    # regions = [2,2]
    for i in range(0, 8):
        index = np.where(data[:, :, p * i:p * (i + 1)] == 10)
        data[index[0], index[1], index[2] + (i * p)] = i + 1
        index = np.where(data[:, :, p * i:p * (i + 1)] == 11)
        data[index[0], index[1], index[2] + (i * p)] = i + 2
    return data