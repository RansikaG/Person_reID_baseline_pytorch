import os
from shutil import copyfile
from PIL import Image


# Helper function to save image as grayscale
def save_grayscale(source, destination):
    img = Image.open(source).convert('L')
    img.save(destination)


# Checks the boat class from the labels and return the class as a string
def boat_class(txt_file_path):
    file = open(txt_file_path, 'r')
    contents = file.read()
    boat_cls = contents.split(' ')
    return boat_cls[0]

def clean_ID(name):
    ID = name.split('_')[0]
    slices = ID.split('-')
    if slices[-1].isnumeric():
        clean_name = '-'.join(slices[:-1])
    else:
        clean_name = '-'.join(slices)
    return clean_name

# You only need to change this line to your dataset download path
download_path = 'F:/Downloads/archive/Ships dataset'

if not os.path.isdir(download_path):
    print('please change the download_path')

save_path = download_path + '/pytorch'
if not os.path.isdir(save_path):
    os.mkdir(save_path)
# -----------------------------------------
# #query
# query_path = download_path + '/query'
# query_save_path = download_path + '/pytorch/query'
# if not os.path.isdir(query_save_path):
#     os.mkdir(query_save_path)
#
# for root, dirs, files in os.walk(query_path, topdown=True):
#     for name in files:
#         if not name[-3:]=='jpg':
#             continue
#         ID  = name.split('_')
#         src_path = query_path + '/' + name
#         dst_path = query_save_path + '/' + ID[0]
#         if not os.path.isdir(dst_path):
#             os.mkdir(dst_path)
#         copyfile(src_path, dst_path + '/' + name)
#
# #-----------------------------------------
# #multi-query
# query_path = download_path + '/gt_bbox'
# # for dukemtmc-reid, we do not need multi-query
# if os.path.isdir(query_path):
#     query_save_path = download_path + '/pytorch/multi-query'
#     if not os.path.isdir(query_save_path):
#         os.mkdir(query_save_path)
#
#     for root, dirs, files in os.walk(query_path, topdown=True):
#         for name in files:
#             if not name[-3:]=='jpg':
#                 continue
#             ID  = name.split('_')
#             src_path = query_path + '/' + name
#             dst_path = query_save_path + '/' + ID[0]
#             if not os.path.isdir(dst_path):
#                 os.mkdir(dst_path)
#             copyfile(src_path, dst_path + '/' + name)
#
# #-----------------------------------------
# #gallery
# gallery_path = download_path + '/bounding_box_test'
# gallery_save_path = download_path + '/pytorch/gallery'
# if not os.path.isdir(gallery_save_path):
#     os.mkdir(gallery_save_path)
#
# for root, dirs, files in os.walk(gallery_path, topdown=True):
#     for name in files:
#         if not name[-3:]=='jpg':
#             continue
#         ID  = name.split('_')
#         src_path = gallery_path + '/' + name
#         dst_path = gallery_save_path + '/' + ID[0]
#         if not os.path.isdir(dst_path):
#             os.mkdir(dst_path)
#         copyfile(src_path, dst_path + '/' + name)

# ---------------------------------------
# train
# This takes all the images from train and val and creates train folder
train_path = download_path + '/train/images'
train_label_path = download_path + '/train/labels'
val_path = download_path + '/val/images'
val_label_path = download_path + '/val/labels'
train_save_path = download_path + '/pytorch/train'
if not os.path.isdir(train_save_path):
    os.mkdir(train_save_path)
    for paths in [(train_path, train_label_path), (val_path, val_label_path)]:
        for root, dirs, files in os.walk(paths[0], topdown=True):
            for name in files:
                if not name[-3:] == 'jpg':
                    continue
                ID = clean_ID(name)
                src_path = paths[0] + '/' + name
                src_label_path = paths[1] + '/' + name[:-3] + 'txt'
                dst_path = train_save_path + '/' + ID + boat_class(src_label_path)
                if not os.path.isdir(dst_path):
                    os.mkdir(dst_path)
                save_grayscale(src_path, dst_path + '/' + name)

# ---------------------------------------
# train_val
val_save_path = download_path + '/pytorch/val'
if not os.path.isdir(val_save_path):
    os.mkdir(val_save_path)

folder_index = -1
folders = ()
for root, dirs, files in os.walk(train_save_path, topdown=True):
    if folder_index == -1 :
        folders = dirs
    else:
        name = files[-1]
        if not name[-3:] =='jpg':
            continue
        dest_folder_name = folders[folder_index]
        src_path = train_save_path + '/' + dest_folder_name + '/' + name
        dst_path = val_save_path + '/' + dest_folder_name
        if not os.path.isdir(dst_path):
            os.mkdir(dst_path)
        copyfile(src_path, dst_path + '/' + name)
        os.remove(src_path)
    folder_index += 1
