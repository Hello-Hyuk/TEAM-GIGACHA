from pycocotools.coco import COCO
import requests
import shutil
import os

# instantiate COCO specifying the annotations json path
coco = COCO('/home/jay/DataSets/coco/annotations/instances_train2017.json')
coco_val = COCO('/home/jay/DataSets/coco/annotations/instances_val2017.json')
dir_path = '/home/jay/DataSets/refine/coco/train/'
dir_path_val = '/home/jay/DataSets/refine/coco/val/'
# Specify a list of category names of interest
# coco_class = [
#     #'person',
#     'bicycle',
#     'car',
#     'motorcylce',
#     'bus',
#     'truck']

# put class name to download
class_name = ['bicycle']

catIds = coco.getCatIds(catNms=class_name)
# Get the corresponding image ids and images using loadImgs
imgIds = coco.getImgIds(catIds=catIds)
images = coco.loadImgs(imgIds)

catIds_val = coco_val.getCatIds(catNms=class_name)
# Get the corresponding image ids and images using loadImgs
imgIds_val = coco_val.getImgIds(catIds=catIds_val)
images_val = coco_val.loadImgs(imgIds_val)
im_len = len(images)
for im in images:
    #if you already download whole dataset (copy)
    #shutil.copy('images/train2017/' + im['file_name'], 'images/esens_coco_train/')
    #if you did not download dataset (download)
    img_data = requests.get(im['coco_url']).content
    with open(dir_path + im['file_name'], 'wb') as handler:
        handler.write(img_data)
print(len(images),"train images copy complete")

# Save the images into a local folder
for im in images_val:
    #shutil.copy('images/val2017/' + im['file_name'], 'images/esens_coco_val/')
    img_data = requests.get(im['coco_url']).content
    with open(dir_path_val + im['file_name'], 'wb') as handler:
        handler.write(img_data)
print(len(images_val),"validation images copy complete")


        