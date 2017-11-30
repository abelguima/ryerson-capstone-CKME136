# *******************************************************************
# ** Guimaraes, Abel & Ghassem, Tofighi (2017)                     **
# ** Implementing load image for Transport Security TSA analysis   **
# ** Python and scikits image script for digital image analysis    **
# *******************************************************************

import dataio.read_tsa_img as img_data
from tsafilter.filter_image import clean_image
from tsabody import zones_body
import pickle
import pandas as pd

df = pd.read_csv('stage1_labels_zones.csv')

loaded_body = df['body_Id'].unique()

# Those files can be download from Kaggle competition
# path = '0043db5e8c819bffc15261b1f1ac5e42.a3dold'
start_at = 100
stop_at = 100
count = 1
for body in loaded_body:
    if start_at > count:
        count += 1
        continue
    path = 'stage1/a3d/' + body + '.a3d'
    print('loading ' + path)
    data = img_data.read_data(path)
    data = clean_image(data)
    data = zones_body.setZonesBody(data)
    pickle.dump(data, open('pickle/data_zones_body/zone' + str(count) + '/' + body + '.pickle', 'wb'))
    print('saved ' + path)
    if stop_at == count:
        break
    count += 1
