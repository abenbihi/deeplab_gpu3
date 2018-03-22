"""
Previous data augmentation on 
0 :: 5114 :: Fruit orchards 
2 :: 5113 :: Tree Farms
3 :: 63 :: Continental water shores
4 :: 211 :: Vineyards
7 :: 52 :: Chopping areas
12 :: 142 :: Dumps and Extraction classes

Data augmentation on new dataset
9 :: 5114 :: Fruit orchards 
8 :: 5113 :: Tree Farms
1 :: 63 :: Continental water shores
13 :: 211 :: Vineyards
10 :: 32 :: Ripariang groves
3 :: 142 :: Dumps and Extraction classes
"""

import numpy as np
import cv2
import os

SubImagesNamelength = 10
#LowRep = [0,2,3,4,7,12] # Previous under represented classes 
LowRep = [9,8,13,10,3] # New under represented classes

def img_namer(number):
    str1 = str(number)
    i = len(str1)
    it = SubImagesNamelength-i
    while it > 0:
        str2 = '0'+str1
        str1 = str2
        it -= 1
    return str1

def augmentData(img,label):
    """ 
    Run transformations over input image and label and returns a list of image
    and label.
    Args:
        img: input image
        label: label map
    """
    angles = [90,180,270]
    flip = [[0], [0], [0]]
    img_list = []
    label_list = []

    #cv2.imwrite("img" + str(count) + ".png", img)

    for a,i in zip(angles,range(len(angles))):
        rows, cols,_ = img.shape
        M = cv2.getRotationMatrix2D((cols/2,rows/2),a,1)
        
        tmp_img = cv2.warpAffine(img,M,(cols,rows))
        tmp_label = cv2.warpAffine(label,M,(cols,rows))
        img_list.append(tmp_img)
        label_list.append(tmp_label)
        #cv2.imwrite("img_" + str(a) + ".png", tmp_img)
        
        for j in flip[i]:
            tmp_img = cv2.flip(tmp_img,j)
            tmp_label = cv2.flip(tmp_label,j)
            img_list.append(tmp_img)
            label_list.append(tmp_label)
            #cv2.imwrite("img_" + str(a) + "_" + str(j) +".png", tmp_img)
    
    for j in flip[0]:
        tmp_img = cv2.flip(img,j)
        tmp_label = cv2.flip(label,j)
        img_list.append(tmp_img)
        label_list.append(tmp_label)
        #cv2.imwrite("img_0_" + str(j) +".png", tmp_img)
        
    return img_list, label_list

data_dir='/home/gpu_user/AgroParisTech/data/new_dataset/Data2015/'
input_dir= data_dir + 'Train/RGB/'
label_dir= data_dir + 'Train/Label/'
augmented_img_dir = input_dir + '75000/'
augmented_label_dir = label_dir + '75000/'

#if os.path.exists(augmented_img_dir) == True:
#    print("Warining: this directory already exists.")
#    print("Provide another dir to store augmented data.")
#    print("Abort.")

count = 0 # number of processed images until now
it = -1
img_id = 75000 # number of images

for root, dirs, files in os.walk(input_dir):
    for d in dirs:
        input_dir_full_path = os.path.join(input_dir + d)
        label_dir_full_path = os.path.join(label_dir + d)
        #print("d_full_path: ", d_full_path)
        
        for f in os.listdir(input_dir_full_path):
            img_full_path = os.path.join(input_dir_full_path, f)
            label_full_path = os.path.join(label_dir_full_path, f)
            #print("img: ", img_full_path)
            #print("label: ", label_full_path)

            count +=1
            if count % 1000==0:
                print("Processed ", count, " images ...")

            img = cv2.imread(img_full_path, cv2.IMREAD_UNCHANGED)
            label = cv2.imread(label_full_path, cv2.IMREAD_UNCHANGED)
            label_id = np.unique(label)
            for j in LowRep:
                # if this img contains under represented classes augment it
                if j in label_id:
                    img_list, label_list = augmentData(img,label)
                    for img_aug, label_aug in zip(img_list, label_list):
                        img_id +=1
                        augmented_img_full_path = os.path.join(augmented_img_dir, img_namer(img_id)+".png") 
                        augmented_label_full_path = os.path.join(augmented_label_dir, img_namer(img_id)+".png")

                        #print("augmented_img_full_path: ", augmented_img_full_path)
                        #print("augmented_label_full_path: ", augmented_label_full_path)
                        cv2.imwrite( augmented_img_full_path,img_aug)
                        cv2.imwrite( augmented_label_full_path,label_aug)

                        break
           
#print("Number of files: ", count) #60609 before data aug
#
#for i in range(5):
#    name = img_namer(i)
#    print("i: ", i)
#    print("name: ", name)

