# *******************************************************************
# ** Guimaraes, Abel & Ghassem, Tofighi (2017)                     **
# ** Implementing visual image for Transport Security TSA analysis **
# ** Python and scikits image script for digital image analysis    **
# *******************************************************************

import tsaview.view_tsa as vtsa
import pickle
import pandas as pd

df = pd.read_csv('stage1_labels_zones.csv')

loaded_body = df['body_Id'].unique()

# Those files can be download from Kaggle competition
# path = 'ad3/0043db5e8c819bffc15261b1f1ac5e42.a3dold'
start_at = 100
stop_at = 100
count = 1
for body in loaded_body:
    path = 'pickle/data_zones_body/zone' + str(count) + '/' + body + '.pickle'
    if start_at > count:
        count += 1
        continue
    print(count)
    print(path)
    data1 = pickle.load(open(path, 'rb'))
    surface = vtsa.get_view(data1, 'surface')
    if stop_at == count:
        break
    count += 1
