"""
Compute data weights for segnet (different that batch norm weights)
Tested against previous implementation on previous dataset: OK
"""
import cv2
import csv
import os
import numpy as np

data_root_dir = '/home/gpu_user/AgroParisTech/data/new_dataset/Data2015BW/'
path_Label_train = data_root_dir + 'Train/Label/'
path_Label_val = data_root_dir + 'Valid/Label/'

# Test on previous dataset
#data_root_dir = '/home/gpu_user/AgroParisTech/data/dataset/CaffeAll_300IR3Set/'
#path_Label_train = data_root_dir + 'train_label/'
#path_Label_val = data_root_dir + 'val_label/'
#path_Label_test = data_root_dir + 'test_label/'

NUM_CLASSES = 14 # label id in [0,13]

classCount = np.zeros(NUM_CLASSES+1) # additional bin for background label
present_in_data = np.zeros(NUM_CLASSES+1)
freq = np.zeros(NUM_CLASSES+1)
a = np.zeros(NUM_CLASSES+1)

i = 0
for path, dirs, files in os.walk(path_Label_train):
    for filenames in files:
        i += 1
        if i%1000 == 0:
            print str(i)+" images processed"
        mat = cv2.imread(path+"/"+filenames,cv2.IMREAD_UNCHANGED)
        label_id,count = np.unique(mat, return_counts=True)
        # process real label id
        for l_id, c in zip(label_id, count):
            if l_id==255:
                classCount[NUM_CLASSES] += c
                present_in_data[NUM_CLASSES] += 1
            else:
                classCount[l_id] += c
                present_in_data[l_id] += 1

        #cv2.imwrite(path+"/"+filenames,mat2)

for path, dirs, files in os.walk(path_Label_val):
    for filenames in files:
        i += 1
        if i%1000 == 0:
            print str(i)+" images processed"
        mat = cv2.imread(path+"/"+filenames,cv2.IMREAD_UNCHANGED)
        label_id,count = np.unique(mat, return_counts=True)
        for l_id, c in zip(label_id, count):
            if l_id==255:
                classCount[NUM_CLASSES] += c
                present_in_data[NUM_CLASSES] += 1
            else:
                classCount[l_id] += c
                present_in_data[l_id] += 1

print classCount
print present_in_data

for i in range(NUM_CLASSES+1):
    if present_in_data[i]!=0:
        freq[i] = float(classCount[i]) / float(present_in_data[i])
        median_freq = 0.5*sum(freq)/(len(classCount))

for i in range(NUM_CLASSES+1):
    if freq[i]!=0:
        a[i] = float(median_freq) / float(freq[i])

print "weights"
count = 0
f = open("weights_" + data_root_dir.split("/")[-2] + ".txt", 'w')
for i in a:
    print "    class"+str(count)+"_weighting: {:.4f}".format(i)
    to_write =  "class"+str(count)+"_weighting: {:.4f}".format(i) +"\n"
    f.write(to_write)
    count += 1
f.close()
