
import os


def dir2file(input_dir, label_dir, list_file):

    if os.path.exists(list_file):
        os.remove(list_file)
    f_handle = open(list_file, 'w')
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

                to_write = img_full_path + " " + label_full_path + "\n"
                f_handle.write(to_write)

    f_handle.close()

def val2valid(val_filename, val_id_filename):
    if os.path.exists(val_id_filename):
        os.remove(val_id_filename)

    fval = open(val_filename)
    fval_id = open(val_id_filename,'w')

    for l in fval:
        full_img_name = l.split()[0] 
        img_name = full_img_name.split("/")[-1]
        img_id = img_name.split(".")[0]
        
        # Why did I want to do this ?
        #find = img_id.find("0")
        #while find == 0 and len(img_id)>1:
        #    img_id = img_id[1:]
        #    find = img_id.find("0")

        fval_id.write(str(img_id) + "\n")

    fval.close()
    fval_id.close()



############
# Data2015
############
data_dir='/home/gpu_user/AgroParisTech/data/new_dataset/Data2015/'

# IR Train
label_dir= data_dir + 'Train/Label/'
input_dir= data_dir + 'Train/IR/'
list_file = input_dir + 'train.txt'
dir2file(input_dir, label_dir, list_file)


# IR Valid
label_dir= data_dir + 'Valid/Label/'
input_dir= data_dir + 'Valid/IR/'
list_file = input_dir + 'val.txt'
id_file = input_dir + 'val_id.txt'
dir2file(input_dir, label_dir, list_file)
val2valid(list_file, id_file)

# IR Train
label_dir= data_dir + 'Train/Label/'
input_dir= data_dir + 'Train/RGB/'
list_file = input_dir + 'train.txt'
dir2file(input_dir, label_dir, list_file)

# IR Valid
label_dir= data_dir + 'Valid/Label/'
input_dir= data_dir + 'Valid/RGB/'
list_file = input_dir + 'val.txt'
id_file = input_dir + 'val_id.txt'
dir2file(input_dir, label_dir, list_file)
val2valid(list_file, id_file)

##############
# Data2015BW #
##############
data_dir='/home/gpu_user/AgroParisTech/data/new_dataset/Data2015BW/'

# RGB Train
label_dir= data_dir + 'Train/Label/'
input_dir= data_dir + 'Train/RGB/'
list_file = input_dir + 'train.txt'
dir2file(input_dir, label_dir, list_file)

# RGB Valid
label_dir= data_dir + 'Valid/Label/'
input_dir= data_dir + 'Valid/RGB/'
list_file = input_dir + 'val.txt'
id_file = input_dir + 'val_id.txt'
dir2file(input_dir, label_dir, list_file)
val2valid(list_file, id_file)

############
# Data1955 #
############
data_dir='/home/gpu_user/AgroParisTech/data/new_dataset/Data1955/'

# RGB Train
label_dir= data_dir + 'Train/Label/'
input_dir= data_dir + 'Train/RGB/'
list_file = input_dir + 'train.txt'
dir2file(input_dir, label_dir, list_file)

# RGB Valid
label_dir= data_dir + 'Valid/Label/'
input_dir= data_dir + 'Valid/RGB/'
list_file = input_dir + 'val.txt'
id_file = input_dir + 'val_id.txt'
dir2file(input_dir, label_dir, list_file)
val2valid(list_file, id_file)
