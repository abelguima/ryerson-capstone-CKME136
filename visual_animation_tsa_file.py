import tsaview.view_tsa as vtsa
import tsafilter.filter_image as tfilter
import dataio.read_tsa_img as img_data
import numpy as np
import pandas as pd

df = pd.read_csv('stage1_labels_zones.csv')

loaded_body = df['body_Id'].unique()

# Those files can be download from Kaggle competition
start_at = 71
stop_at = 72
count = 0
for body in loaded_body:
    if start_at > count:
        count += 1
        continue
    path = 'stage1/aps/' + body +'.aps'
    #path = 'stage1/aps/' + body + '.aps'
    print(count)
    print(path)

    data1 = img_data.read_data(path)
    # if want clean
    #data = tfilter.clean_image(data1)
    #datam = np.multiply(data, data1)
    # animation = vtsa.get_view(data1, 'animation', loaded_body[1])

    for i in range(260, 380):
        animation = vtsa.get_view(data1, 'animation', i, body)
    if stop_at == count:
        break
    count += 1
