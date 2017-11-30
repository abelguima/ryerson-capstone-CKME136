# *******************************************************************
# ** Guimaraes, Abel & Ghassem, Tofighi (2017)                     **
# ** Implementing visual image for Transport Security TSA analysis **
# ** Python and scikits image script for digital image analysis    **
# *******************************************************************

import tsaview.view_zone_tsa as vtsa
import pickle
import numpy as np
import pandas as pd

df = pd.read_csv('stage1_labels_zones.csv')

loaded_body = df['body_Id'].unique()

# Those files can be download from Kaggle competition
# path = '0043db5e8c819bffc15261b1f1ac5e42.a3dold'
start_at = 66
stop_at = -1
count = 0
for body in loaded_body:
    path = 'pickle/data_zones_body/' + body + '.pickle'
    if start_at > count:
        count += 1
        continue
    data = pickle.load(open(path, 'rb'))
    np.where(data[:, :, :] == 1)
    surface = vtsa.get_view(data, 0)
    if stop_at == count:
        break
    count += 1
