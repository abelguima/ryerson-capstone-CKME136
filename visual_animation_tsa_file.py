import tsaview.view_tsa as vtsa
import dataio.read_tsa_img as img_data
import tsafilter.filter_image as tfilter

# Those files can be download from Kaggle competition
# path = 'C:\\Users\\abelguima\\Google Drive\\sample\\0043db5e8c819bffc15261b1f1ac5e42.a3d'
path = 'C:\\Users\\abelguima\\Google Drive\\sample\\0043db5e8c819bffc15261b1f1ac5e42.aps'
data = img_data.read_data(path)
# if want clean
data = tfilter.clean_image(data)
animation = vtsa.get_view(data, 'animation')



