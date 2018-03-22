# KO
# Get existing label id

import os
import numpy as np
import cv2

data_dir_root = '/home/gpu_user/AgroParisTech/data/dataset/CaffeAll_300IR3Set/'
train_label_dir = data_dir_root + 'train_label'
val_label_dir = data_dir_root + 'val_label'


num_classes = 15 #[1,14] + 255
label_count = np.zeros((2,num_classes+1), dtype=np.int)


    
for root, dirs, files in os.walk(val_label_dir):
    for d in dirs:
        print("d: ", d)
        d_full_path = os.path.join(dirname + d)
        print("d_full_path: ", d_full_path)

        for f in os.listdir(d_full_path):
            print("f: ", f)
            
            f_full_path = os.path.join(d_full_path, f)
            label_map = cv2.imread(f_full_path, cv2.IMREAD_UNCHANGED)
            label_id,count = np.unique(label_map,return_counts = True)
            

        
            for i in range(count.shape[0]):
                if label_id[i]==0:
                    print("here")
                if label_id[i] == 255:
                    label_count[1,15] += count[i]
                else:    
                    label_count[1,label_id[i]] += count[i]


print(label_id)      
print(count)
print(label_count)
label_count[1,15]=0
label_ratio = label_count * 100.0 / np.sum(label_count)
label_ratio[0] = np.arange(num_classes+1)
print(label_ratio)

np.savetxt("label_ratio.txt",label_ratio, fmt='%.3f')




