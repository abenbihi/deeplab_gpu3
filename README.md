# Installation

## Compilation 
    
    # DO NOT USE CMAKE !!!!
    # if you already did, upload the Makefile from the official repo
    
    cd code
    make -j12 all tools pycaffe

## Load N channels images instead of color or black-white

    # in deeplab/code/src/caffe/util/io.cpp
    # cv::Mat ReadImageToCVMat(
    //cv::Mat cv_img_origin = cv::imread(filename, cv_read_flag);
    cv::Mat cv_img_origin = cv::imread(filename, CV_LOAD_IMAGE_UNCHANGED);

# Dataset manipulation

## Dataset structure

For the dataset of name Data1955, you have two folders: Train and Valid which contains the images to train and test respectively.
Inside Label contains the ground truth segmentation, RGB and IR contains the input image with RGB channels in RGB/ and RGB-IR in IR/.
IR is empty for black and white images. 
In each of these directory, images are organised in directories 0, 1000, ... each containing 1000 images.
TODO why ?  

	.
	├── Data1955
	│   ├── Train
	│   │   ├── IR
	│   │   ├── Label
	│   │   │   ├── 0
	│   │   │   ├── 1000
	│   │   │   ├── 10000
	│   │   │   ├── 11000
	│   │   │   ├── 12000
	│   │   └── RGB
	│   │       ├── 0
	│   │       ├── 1000
	│   │       ├── 10000
	│   │       ├── 11000
	│   │       ├── 12000
	│   └── Valid
	│       ├── IR
	│       ├── Label
	│       │   ├── 0
	│       │   ├── 1000
	│       │   ├── 10000
	│       │   ├── 11000
	│       │   ├── 12000
	│       ├── PPMImages
	│       │   ├── 0
	│       │   ├── 1000
	│       │   ├── 10000
	│       │   ├── 11000
	│       │   ├── 12000
	│       └── RGB
	│           ├── 0
	│           ├── 1000
	│           ├── 10000
	│           ├── 11000
	│           ├── 12000

If you wan to create a new dataset, please follow this structure

	.
	├── <DATASET NAME>
	│   ├── Train
	│   │   ├── IR
	│   │   ├── Label
	│   │   │   ├── 0
	│   │   └── RGB
	│   │       ├── 0
	│   └── Valid
	│       ├── IR
	│       ├── Label
	│       │   ├── 0
	│       ├── PPMImages
	│       │   ├── 0
	│       └── RGB
	│           ├── 0


## Cut your images to 300x300 images

TODO by Antoine

## Convert your validations image dataset into ppm format (you need matlab to do so)
DO NOT USE ANY OTHER CODE TO DO THE CONVERSION !!!! 
The crf script accepts only the ppm images generated with this code.
Don't ask why.

Specify the directory of valid images

	cd exper/dataset
    # Change the hard coded path in the file before running
	vim SaveJpgToPPM.m
	img_root_folder = '/home/gpu_user/AgroParisTech/data/new_dataset/Data2015BW/Valid/RGB/';
	save_root_folder = '/home/gpu_user/AgroParisTech/data/new_dataset/Data2015BW/Valid/PPMImages/';	
	
	matlab
    SaveJpgToPPM

## Send your data to supelec

Copy the dataset to a hard drive and give it to Assia

# Training

## Connect to supelec gpus

Follow instructions from [http://192.93.8.150/sp/gpu_supelec.git]

## Make docker image (If necessary only)

Check that the gpu you connected to doesn't already have a deeplab images

	docker images
	> deeplab latest b13da678c9bb 3 months ago 2.97GB

If it has not, follow instructions from [http://192.93.8.150/sp/docker_generic.git] in the deeplab directory

## Environment creation (Skip, I already did it)

Your working directory is 

	/opt/BenbihiAssia/deeplab

The environment should already be there. 
Else if you need to create it 

### Root directory

	WS_DIR = /opt/BenbihiAssia/deeplab/
	cd $WS_DIR
	mkdir datasets
	mkdir exper

### Dataset directory
Copy your dataset here

	cd datasets
	mkdir <dataset name>
	cd <dataset name>
	# place everything related to this dataset here
	chmod 777 -R <dataset name>

### Exper directory (Skip this section)
	
	# SKIP !!!!!
	cd exper
	./create_dir.sh <xp name>

You should have files with the name of the images for train and test. Copy them:

	cp train.txt <xp name>/list/
	cp val.txt <xp name>/list/
	cp val_id.txt <xp name>/list/

Copy the network model into config

	cp *.prototxt <xp name>/resnet/config
	cp *.caffemodel <xp name>/resnet/config #from which you finetune

### Make everything 777
	
chmod everything you added 
	chmod 777 -R <xp name>/resnet/config
	chmod 777 -R <xp name>/list/
	chmod 777 -R <dataset name>


## Your experiment

Your working directory is 

	/opt/BenbihiAssia/deeplab

The environment should already be there. 
Else if you need to create it 

	cd /opt/BenbihiAssia/deeplab/

Copy your dataset here

	cd datasets
	mkdir <dataset name>
	cd <dataset name>
	# place everything related to this dataset here
	chmod 777 -R <dataset name>

You should have files with the name of the images for train and test. Copy them:

	cp train.txt antoine/list/<dataset name>/
	cp val.txt antoine/list/<dataset name>/
	cp val_id.txt antoine/list/<dataset name>/

Copy the network model into config

	cp *.prototxt antoine/resnet/config/<xp name>
	
	# If you finetune from something different that what is provided by deeplab
	cp *.caffemodel antoine/resnet/config/<xp name> 

### Make everything 777
	
chmod everything you added 
	chmod 777 -R antoine/list/<dataset name>/
	chmod 777 -R antoine/resnet/config/<xp name>

## Training

Copy one of the prototxt experiment and set the correct path

	cd exper/antoine/config
	cp -r bgr_adam <xp name>
	cd <xp name>
	vim train_train.prototxt
	# Change source to your file list
	image_data_param {
    root_folder: "/"
    source: "antoine/list/<dataset name>/train.txt"
    batch_size: 1
    shuffle: true
    label_type: PIXEL
  	}

	vim solver_train.prototxt
	train_net: "antoine/config/<xp name>/train_train.prototxt"
	snapshot_prefix: "antoine/model/<xp name>/train"
	

Run the docker image
	
	nvidia-docker run --volume=/opt/BenbihiAssia/deeplab/:/home/ws -it -u root deeplab bash

Train
	cd exper
	caffe train --solver=antoine/config/<xp name>/solver_train.prototxt --weights=antoine/config/train_iter_20000.caffemodel

Wait for 5 days ...


## Generate segmentation maps and feature maps without crf 

### Generate segmentation results

	cd exper/antoine/config
	cp -r bgr_adam <xp name>
	cd <xp name>
	vim test_val.prototxt
	# Change source to your file list
	image_data_param {
    root_folder: "/"
    source: "antoine/list/<dataset name>/val.txt"
    batch_size: 1
    label_type: NONE
  	}

Specify where to store the result

	cd exper/antoine/config
	vim test_val.txt # At the end of the file

	layer {
	  name: "fc1_mat"
	  type: "MatWrite"
	  bottom: "fc1_interp_argmax"
	  bottom: "fc1_interp"
	  include {
	    phase: TEST
	  }
	  mat_write_param {
	    prefix: "<xp name>"
	    source: "antoine/list/val_id.txt"
	    strip: 0
	    period: 1
	 }
	}

Comment everything under 

	# #### crf ###

Generates the results. It takes time, it is normal
	
	caffe test --model=antoine/config/resnet/bgr_adam/test_val.prototxt --weights=antoine/model/resnet/bgr_adam/train_iter_120000.caffemodel --gpu=0 --iterations=<NUM TEST IMAGE>

The feature maps are in exper/antoine/features/<xp name>

### Run crf (ON GPU3 !!!!)

Bring them back to GPU3

	tar -cvzf <xp name>.tar.gz <xp name>
	mv v.tar.gz ~/tmp

Connect to gpu 3

	# On gpu 3
	cd /home/gpu_user/assia/ws/tf/deeplab/exper/features/
	scp benbihi_ass@ghome.metz.supelec.fr:~/tmp/<xp name>.tar.gz .
	tar -xvzf v.tar.gz
	rm <xp name>.tar.gz

Copy the densecrf script and adjust the parameter

	cd exper
	cp run_densecrf.sh run_densecrf/run_densecrf<xp name>.sh

Modify the parameters
	
	cd run_densecrf
	vim run_densecrf<xp name>.sh

	DATASET=Data2015
	XP_NAME=bgrir_sgd

Run crf. The res are in res/<xp name>/bin/
	
	./run_densecrf<xp name>.sh

## Generate segmentation maps and feature maps with crf 
	
	
	cd exper/antoine/config
	vim test_val.txt # At the end of the file

Comment 

	#layer {
	#  bottom: "fc1_interp"
	#  top: "fc1_interp_argmax"
	#  name: "fc1_interp_argmax"
	#  type: "ArgMax"
	#  argmax_param {
	#    axis: 1
	#  }
	#}
	#layer {
	#  name: "fc1_mat"
	#  type: "MatWrite"
	#  bottom: "fc1_interp_argmax"
	#  bottom: "fc1_interp"
	#  include {
	#    phase: TEST
	#  }
	#  mat_write_param {
	#    prefix: "antoine/features/resnet/val/60k/"
	#    source: "antoine/list/val_id.txt"
	#    strip: 0
	#    period: 1
	# }
	#}

Uncomment everything under

	# #### crf ###


## Compute metrics

Convert bin crf output to png. 
Put the crf output in res/<xp name>/bin/
	
	cd exper/metrics
	vim GetDenseCRFResult.m
	xp_name = <xp name>

	matlab
	GetDenseCRFResult

Specify you variables

	vim GetVOCopts.m
	matlab
	EvalSegResults


# Misc 

## Crf on supelec gpu

This assumes that you also have the PPI images on the supelec gpu.
The densecrf/Makefile uploaded by the docker with the deeplab-ver2 repository lacks a link. So the best strategy for now is to compile it by hand once you run the docker image.

It seems that running crf gives wrong outputs on the supelec gpu. I don't know why. 
So i wouldn't advise to run densecrf there unless it is inside the network.

- Compile the crf code
Add the missing link to libhfd5 after -lmatio.
	
	# In the docker image
	cd code/densecrf
	vim Makefile
	$(CC) refine_pascal_v4/dense_inference.cpp -o prog_refine_pascal_v4 $(CFLAGS) -L. -lDenseCRF -lmatio -lhdf5 -I./util/

If you have a segfault, check that your feature maps have the correct pattern
In the main file, it is the variable strip_pattern.
By default, it is 'blob_0' but you may have 'blob_1' or another 
	
	// TODO Set pattern to blob_0 or 1
  	std::string strip_pattern("_blob_1");

## Add the layer to write feature maps to your prototxt
    # Add the following files to your caffe implementation
        # deeplab/code/src/caffe/layers/mat_write_layer.cpp
        # deeplab/code/include/caffe/layers/mat_write_layer.hpp
        # deeplab/code/src/caffe/util/matio_io.cpp
        # deeplab/code/include/caffe/util/matio_io.hpp
    # DO NOT FORGET TO:
        # Edit the caffe.proto file ("caffe_root"/src/caffe/proto/caffe.proto)
            # Add the following line in the message LayerParameter
                # optional MatWriteParameter mat_write_param = 145;
                # DO NOT FORGET TO edit the number to one which isn't used
            # Add the following message:
                # message MatWriteParameter {
                #     required string prefix = 1;
                #     optional string source = 2 [default = ""];
                #     optional int32 strip = 3 [default = 0];
                #     optional int32 period = 4 [default = 1];
                # }
        # Edit the Makefile ("caffe_root"/Makefile) to link the matio lib
            # Add "USE_MATIO ?= 1" bellow "# handle IO dependencies"
            # Add the following underneath
                # ifeq ($(USE_MATIO), 1)
                #     LIBRARIES += matio
                # endif
        # Run make clean in caffe's root directory
        # Run make all -jn with n number of workers in caffe's root directory
    # Add the following layer to your prototxt. e.g. writing the feature map
    # fc8_interp
    # The layer needs a file holding the image index val_id.txt to know how to
    # name the feature map file
    layer {
      name: "fc8_mat"
      type: "MatWrite"
      bottom: "fc8_interp"
      include {
        phase: TEST
      }
      mat_write_param {
        prefix: "voc12/features/deep_largeFOV/val/fc8/"
        source: "voc12/list/val_id.txt"
        strip: 0
        period: 1
      }
    }

## Compile caffe
Modify Makefile.config

	INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include /usr/include/hdf5/serial/
	LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib /usr/lib/x86_64-linux-gnu/hdf5/serial/

Modify Makefile to include matio lib

    USE_MATIO ?= 1
    ifeq ($(USE_MATIO), 1)
        LIBRARIES += matio
    endif

(Not necessary anymore)
Add path to hdf5

    export CPATH="/usr/include/hdf5/serial/"

# Learn the crf parameters with gridsearch
	
	TODO
