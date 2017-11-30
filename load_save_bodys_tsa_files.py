# *******************************************************************
# ** Guimaraes, Abel & Ghassem, Tofighi (2017)                     **
# ** Implementing load image for Transport Security TSA analysis   **
# ** Python and scikits image script for digital image analysis    **
# *******************************************************************

import numpy as np
import pickle
import pandas as pd


df = pd.read_csv('stage1_labels_zones.csv')

loaded_body = df['body_Id'].unique()

# Those files can be download from Kaggle competition
# path = '0043db5e8c819bffc15261b1f1ac5e42.a3d'
start_at = 2
stop_at = 2
count = 1
for body in loaded_body:
    path = 'data/pickle/data_zones_body/zone' + str(count) + '/' + body + '.pickle'
    if start_at > count:
        count += 1
        continue
    data = pickle.load(open(path, 'rb'))
    print(count)
    print('loading ' + path)
    for i in range(1, 18):
        index = np.where(data[:, :, :] != i)
        data[index] = 0
        paths = 'data/pickle/data_zones_body/zone' + str(i) + '/' + body + '.pickle'
        pickle.dump(data, open(paths, 'wb'))
        print('saved ' + paths)
    if stop_at == count:
        break
    count += 1
