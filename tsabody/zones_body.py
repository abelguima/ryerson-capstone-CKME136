# *******************************************************************
# ** Guimaraes, Abel & Ghassem, Tofighi (2017)                     **
# ** Implementing zone image for Transport Security TSA analysis   **
# ** Python and scikits image script for digital image analysis    **
# *******************************************************************

import numpy as np


def setZonesBody(data):
    # calculate the left and right of the body
    x_half = np.int64(np.shape(data)[0] / 2)
    # calculate the portion of body
    # p = np.int64(np.max(np.where(data[x_half:x_half + 1, :, :] > 0)) / 8)
    p = np.int64(np.max(np.where(data[:, :, :] > 0)) / 8)
    # divide in to zones left and right body
    # left body
    data[np.where(data[:x_half, :, :] == 1)] = 20
    # right body
    data[np.where(data[:, :, :] == 1)] = 21

    # todo see clxmin at height
    # minimum x left of the body forearm
    clxmin = np.min(np.where(data[:x_half, :, :] == 20)[0])
    # max x left of the body forearm sliced on 5
    clxmax = np.min(np.where(data[:x_half, :, 5 * p:(5 * p) + 1] == 20)[0]) - np.int64(p / 8)
    # min z left of the body forearm sliced on 5
    czmin = 5 * p
    # max z left of the body forearm sliced on 5
    cc = 0
    while True:
        cc += 1
        czmax = np.max(np.where(data[clxmin:clxmin + cc, :, :])[2])
        if czmax > czmin:
            break
    # volume of the left region of the body arm sliced on 5
    campl = np.where(data[:clxmax, :, czmin:czmax] == 20)
    # add czmin to centralize body arm
    lcamp = list(campl)
    lcamp[2] += czmin
    campl = tuple(lcamp)
    data[campl] = 13
    camplz = np.where(data[:, :, czmax:] == 20)
    lcampz = list(camplz)
    lcampz[2] += czmax
    camplz = tuple(lcampz)
    data[camplz] = 15
    head_distance = np.int64(p / 2)
    hh = x_half - clxmin + head_distance
    if hh > (x_half - head_distance):
        hh = x_half - (clxmin + head_distance)
    hhcamp = np.where(data[hh:, :, :(7 * p) + np.int64(p / 4)] == 15)
    hhcampl = list(hhcamp)
    hhcampl[0] += hh
    hhcamp = tuple(hhcampl)
    data[hhcamp] = 0
    data[np.where(data[hh:, :, (6 * p):] == 20)[0] + hh, np.where(data[hh:, :, (6 * p):] == 20)[1],
         np.where(data[hh:, :, (6 * p):] == 20)[2] + (6 * p)] = 0
    # todo see crxmin at height
    # crxmax = np.max(np.where(data[:, :, :] == 21)[0])
    crxmin = np.max(np.where(data[:, :, 5 * p:(5 * p) + 1] == 21)[0]) + np.int64(p / 8)
    campr = np.where(data[crxmin:, :, czmin:czmax] == 21)
    rcamp = list(campr)
    rcamp[2] += czmin
    rcamp[0] += crxmin
    campr = tuple(rcamp)
    data[campr] = 14
    camprz = np.where(data[:, :, czmax:] == 21)
    rcampz = list(camprz)
    rcampz[2] += czmax
    camprz = tuple(rcampz)
    data[camprz] = 16
    hhr = crxmin
    hhrcamp = np.where(data[:hhr, :, :(7 * p) + np.int64(p / 4)] == 16)
    hhrcampr = list(hhrcamp)
    # hhrcampr[2] += czmax
    hhrcamp = tuple(hhrcampr)
    data[hhrcamp] = 0
    data[np.where(data[:hhr, :, (6 * p):] == 21)[0], np.where(data[:hhr, :, (6 * p):] == 21)[1],
         np.where(data[:hhr, :, (6 * p):] == 21)[2] + (6 * p)] = 0

    low = 0
    high = 0
    for i in range(0, 8):
        a = 3/4
        c = 6/4
        if i == 0 or i == 2:
            p1 = np.int64(a*p)
        elif i == 3:
            p1 = np.int64(c*p)
        else:
            p1 = p
        low = high
        high += p1
        index = np.where(data[:, :, low:high] == 20)
        data[index[0], index[1], index[2] + low] = i * 2 + 1
        index = np.where(data[:, :, low:high] == 21)
        data[index[0], index[1], index[2] + low] = i * 2 + 2

    data[np.where(data[:, :, :] == 11)] = 12
    y_body_min = np.min(np.where(data[:, :, :] == 12)[1])
    y_body_max = np.max(np.where(data[:, :, :] == 12)[1])
    y_body_half = y_body_min + np.int64((y_body_max - y_body_min)/2) + np.int64(p / 3)
    data[np.where(data[:, :y_body_half, :] == 12)] = 11

    x_body_min = np.min(np.where(data[:, :, :] == 7)[0])
    x_body_max = np.max(np.where(data[:, :, :] == 8)[0])
    x_body_half = x_body_min + np.int64((x_body_max - x_body_min)/2)

    a = np.int64((x_body_half-x_body_min)/3)
    campx = np.where(data[x_body_half-a:, :, :] == 7)
    xcamp = list(campx)
    xcamp[0] += x_body_half - a
    campx = tuple(xcamp)
    data[campx] = 17
    data[np.where(data[:x_body_half+a, :, :] == 8)] = 17

    dataaux = np.copy(data)

    dataaux[np.where(data[:, :, :] == 1)] = 15
    dataaux[np.where(data[:, :, :] == 2)] = 16
    dataaux[np.where(data[:, :, :] == 3)] = 13
    dataaux[np.where(data[:, :, :] == 4)] = 14
    dataaux[np.where(data[:, :, :] == 5)] = 11
    dataaux[np.where(data[:, :, :] == 6)] = 12
    dataaux[np.where(data[:, :, :] == 7)] = 8
    dataaux[np.where(data[:, :, :] == 8)] = 10
    dataaux[np.where(data[:, :, :] == 9)] = 6
    dataaux[np.where(data[:, :, :] == 10)] = 7
    dataaux[np.where(data[:, :, :] == 11)] = 5
    dataaux[np.where(data[:, :, :] == 12)] = 17
    dataaux[np.where(data[:, :, :] == 13)] = 1
    dataaux[np.where(data[:, :, :] == 14)] = 3
    dataaux[np.where(data[:, :, :] == 15)] = 2
    dataaux[np.where(data[:, :, :] == 16)] = 4
    dataaux[np.where(data[:, :, :] == 17)] = 9

    return dataaux

