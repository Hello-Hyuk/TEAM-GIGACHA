#!/usr/bin/env python3
import os
from glob import glob
import shutil
from matplotlib import image
from sklearn.model_selection import train_test_split


src_dir = "/home/jay/DataSets/udacity/export/"
dst_dir = "/home/jay/DataSets/test/"

train_dir = dst_dir + "train"
test_dir = dst_dir + "test"

#getting list of images
img_files = glob(os.path.join("/home/jay/DataSets/udacity/export/*.jpg"))
images = [name.replace(".jpg", "") for name in img_files]
print(len(images))

#split the data
#train : test = 8 : 2
train_names, test_names = train_test_split(images, test_size=0.2,
random_state=42, shuffle=True)
# test -> 0.5 test /val

def batch_move_files(file_list, src_path, dst_path):
    for file in file_list:
        img = file.split('/')[-1] + '.jpg'
        txt = file.split('/')[-1] + '.txt'
        # #print(img)
        # print("copy img ",os.path.join(src_path, img)," to ", dst_path)
        shutil.copy(os.path.join(src_path, img), dst_path)
        shutil.copy(os.path.join(src_path, txt), dst_path)
    return

#print(train_dir)
#img = images[0].split('/')[-1] + '.jpg'
print("copy train data to ", train_dir)
batch_move_files(train_names, src_dir, train_dir)
print("finish train data")

print("copy train data to ", test_dir)
batch_move_files(test_names, src_dir, test_dir)
print("finish test data")

# splitfolders.ratio("/home/jay/DataSets/udacity/export", output="/home/jay/DataSets/udacity", seed=77, ratio=(.7, .3), group_prefix=2)
# i = 1
# for (root, directories, files) in os.walk(dir_path):
#     for file in files:
#         if '.txt' in file:
#             print(len(files))
#             print("orignin file_name : ",file)
#             file_name = file.rstrip('.txt')
#             txt_file_path = os.path.join(root, file_name +'.txt')
#             jpg_file_path = os.path.join(root, file_name +'.jpg')
#             print(txt_file_path)
#             print(jpg_file_path)
#             if i <= 20000:
#                 print("training\n")
#                 mv_txt = os.path.join('/home/jay/DataSets/udacity/udacity_train' ,file_name + '.txt')
#                 mv_jpg = os.path.join('/home/jay/DataSets/udacity/udacity_train',file_name + '.jpg')
#                 print(mv_txt)
#                 print(mv_jpg)
#                 shutil.copy(txt_file_path, mv_txt)
#                 shutil.copy(jpg_file_path, mv_jpg)
#                 print("complete : ", i)
#                 i += 1
#             else :
#                 print("validation\n")
#                 mv_txt = os.path.join('/home/jay/DataSets/udacity/udacity_val' ,file_name + '.txt')
#                 mv_jpg = os.path.join('/home/jay/DataSets/udacity/udacity_val',file_name + '.jpg')
#                 print(mv_txt)
#                 print(mv_jpg)
#                 shutil.copy(txt_file_path, mv_txt)
#                 shutil.copy(jpg_file_path, mv_jpg)
#                 print("complete : ", i)
