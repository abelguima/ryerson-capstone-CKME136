# *******************************************************************
# ** Guimaraes, Abel & Ghassem, Tofighi (2017)                     **
# ** Implementing load image for Transport Security TSA analysis   **
# ** Python and scikits image script for digital image analysis    **
# *******************************************************************

import dataio.read_tsa_img as img_data
import tsabody.zones_body as body
import tsafilter.filter_image as tsa_filter
import matplotlib.image as multiplied_image
import pandas as pd
import numpy as np
# from joblib import Parallel, delayed
import multiprocessing
import os


# Those files can be download from Kaggle competition
# boundary_zones is [actual_zone,zone_up,zone_down,zone_left,zone_right]
def process_input(loaded_body):
    path_directory = 'data/data_zones_body/'
    # limit of zones [zone, zone up, zone down]
    border_zones = [[1, 2, 5],
                    [2, -1, 1],
                    [3, 4, 5],
                    [4, -1, 3],
                    [5, -1, [6, 7]],
                    [6, [5, 17], 8],
                    [7, [5, 17], 10],
                    [8, 6, 11],
                    [9, [6, 7], [11, 12]],
                    [10, 7, 12],
                    [11, 8, 13],
                    [12, 10, 14],
                    [13, 11, 15],
                    [14, 12, 16],
                    [15, 13, -1],
                    [16, 14, -1],
                    [17, -1, [6, 7]]
                    ]
    # flip zones
    flip_zones = [[1, 3], [2, 4], [3, 1], [4, 2],
                  [5, 5], [6, 7], [7, 6], [8, 10],
                  [9, 9], [10, 8], [11, 12], [12, 11],
                  [13, 14], [14, 13], [15, 16], [16, 15],
                  [17, 17]]
    # don't flip those zones
    not_flip_zones = [5, 9, 17]
    # path of a3d
    path = 'stage1/a3d/' + loaded_body + '.a3d'
    print('loading ' + path)
    # read data
    data1 = img_data.read_data(path)
    # clean data
    data = tsa_filter.clean_image(data1)
    # label body in zones
    data_z = body.setZonesBody(data)
    # save png zones in files
    for i in range(1, 18):
        path_dir_zone = 'zone' + str(i)
        path_dir_zone_threat = 'zone_threat' + str(i)
        path_dir_zone_threat_flip = 'zone_threat' + str(flip_zones[i - 1][1])
        border_zone_up1 = -1
        border_zone_up2 = -1
        border_zone_down1 = -1
        border_zone_down2 = -1
        # recover from csv the threat zone of this body
        zone_body_threat = np.array(df.ix[np.where(df.ix[:, 0] == loaded_body)].iloc[:, 1:])
        # copy of body in auxiliary
        data_auxiliary = data_z.copy()
        # index all labels that is not i (reference)
        index = np.where(data_z[:, :, :] != i)
        # set those labels to 0
        data_auxiliary[index] = 0
        # look for the label i (reference)
        index1 = np.where(data_auxiliary[:, :, :] > 0)
        # set label to 1
        data_auxiliary[index1] = 1
        # multiply this label = 1 and label = 0 with data original recover just the ROI
        data_multiplied = np.multiply(data_auxiliary, data1)
        # index the ROI
        index2 = np.where(data_multiplied[:, :, :] > 0)
        # Transfer data to be analyze between max and min of z
        dat1 = np.zeros((512, 512, np.max(index2[2]) + 1))
        dat1[index2] = data_multiplied[index2[0], index2[1], index2[2]]
        z_min = np.min(index2[2])
        dat2 = dat1[:, :, z_min:]
        # initialize z reference
        count_z = 0
        # analyzing label data to be saved as sliced figure for that zone i (reference)
        # treating every slice image (img)
        for img in dat2.T:
            # clear path and path flip
            path = ''
            path_flip = ''
            # verify is this is a threat body
            if zone_body_threat.size > 0:
                # get z max and min values from zone threat slice
                for zone_threat in zone_body_threat:
                    # this slice is a z threat of the zone?
                    if zone_threat[0] <= count_z + z_min <= zone_threat[1]:
                        if zone_threat[2] == i:
                            path = path_directory + path_dir_zone_threat + \
                                   '/' + loaded_body + '_z_' + str(count_z + z_min) + '.png'
                            if zone_threat[2] != flip_zones[i - 1][1] and zone_threat[2] != not_flip_zones[0] and \
                                    zone_threat[2] != not_flip_zones[1] and zone_threat[2] != not_flip_zones[2]:
                                path_flip = path_directory + path_dir_zone_threat_flip \
                                            + '/' + loaded_body + '_z_' + str(count_z + z_min) + '.png'
                        else:
                            if np.size(border_zones[i - 1][1]) > 1:
                                border_zone_up1 = border_zones[i - 1][1][0]
                                border_zone_up2 = border_zones[i - 1][1][1]
                            else:
                                border_zone_up1 = border_zones[i - 1][1]
                                border_zone_up2 = -1
                            if np.size(border_zones[i - 1][2]) > 1:
                                border_zone_down1 = border_zones[i - 1][2][0]
                                border_zone_down2 = border_zones[i - 1][2][1]
                            else:
                                border_zone_down1 = border_zones[i - 1][2]
                                border_zone_down2 = -1
                            if zone_threat[2] == border_zone_up1 or \
                                    zone_threat[2] == border_zone_up2 or \
                                    zone_threat[2] == border_zone_down1 or \
                                    zone_threat[2] == border_zone_down2:
                                path = path_directory + path_dir_zone_threat \
                                + '/' + loaded_body \
                                    + '_z_' + str(count_z + z_min) + '.png'
                                if zone_threat[2] != flip_zones[i - 1][1] \
                                        and zone_threat[2] != not_flip_zones[0] and \
                                        zone_threat[2] != not_flip_zones[1] and \
                                        zone_threat[2] != not_flip_zones[2]:
                                    path_flip = path_directory + path_dir_zone_threat_flip +\
                                                '/' + loaded_body + '_z_' + \
                                                str(count_z + z_min) + '.png'
                        break
                if path.__eq__(''):
                    path = path_directory + path_dir_zone + \
                           '/' + loaded_body + '_z_' + str(count_z + z_min) + '.png'
                    if not os.path.exists(path_directory + path_dir_zone):
                        os.makedirs(path_directory + path_dir_zone)
                    multiplied_image.imsave(path, np.flipud(img), origin='upper', cmap='viridis')
                    print('saved ' + path)
                else:
                    if not os.path.exists(path_directory + path_dir_zone_threat):
                        os.makedirs(path_directory + path_dir_zone_threat)
                    multiplied_image.imsave(path, np.flipud(img), origin='upper', cmap='viridis')
                    print('saved ' + path)
                    if not path_flip.__eq__(''):
                        if not os.path.exists(path_directory + path_dir_zone_threat_flip):
                            os.makedirs(path_directory + path_dir_zone_threat_flip)
                        multiplied_image.imsave(path_flip, np.flipud(np.fliplr(img)), origin='upper', cmap='viridis')
                        print('saved ' + path_flip)
            else:
                path = path_directory + path_dir_zone + \
                       '/' + loaded_body + '_z_' + str(count_z + z_min) + '.png'
                if not os.path.exists(path_directory + path_dir_zone):
                    os.makedirs(path_directory + path_dir_zone)
                multiplied_image.imsave(path, np.flipud(img), origin='upper', cmap='viridis')
                print('saved ' + path)
            count_z += 1


# what are your inputs, and what operation do you want to
# perform on each input. For example...
df = pd.read_csv('stage1_labels_zones.csv')

bodies = df['body_Id'].unique()
start_at = 1
stop_at = 200

num_cores = multiprocessing.cpu_count()
# results = Parallel(n_jobs=num_cores)(delayed()
c = 0
for loaded_body in bodies[start_at:stop_at]:
    c += 1
    print(c)
    process_input(loaded_body)
