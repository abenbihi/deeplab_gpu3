# Compilation 
    
    # DO NOT USE CMAKE !!!!
    # if you already did, upload the Makefile from the official repo
    
    cd code
    make -j12 all tools pycaffe

# Load N channels images

    # in deeplab/code/src/caffe/util
    # cv::Mat ReadImageToCVMat(
    //cv::Mat cv_img_origin = cv::imread(filename, cv_read_flag);
    cv::Mat cv_img_origin = cv::imread(filename, CV_LOAD_IMAGE_UNCHANGED);


# Convert your image dataset into ppm format (you need matlab to do so)
    
    # Change the hard coded path in the file before running
    # DO NOT USE ANY OTHER CODE TO DO THE CONVERSION !!!! 
    # the crf script accepts only the ppm images generated with this code.
    # Don't ask why.
    deeplab/code/densecrf/my_script/SaveJpgToPPM.m

# Generate features map to feed crf: this creates fcn8 in deeplab/exper/voc12/features/deep_largeFOV/val/fc8
    # This run your trained network on your test set and save the wanted
    # feature map in .mat format
    cd exper
    # Assuming you have generated test_val.prototxt with run_pascal.sh 
    /home/gpu_user/assia/ws/tf/deeplab//code/.build_release/tools/caffe.bin test --model=voc12/config/deep_largeFOV/test_val.prototxt --weights=voc12/config/deep_largeFOV/train_iter_20000.caffemodel --gpu=0 --iterations=1449
    # The code freezes on the output line "Running 1449 iterations": it is
    normal. It is computing the feature maps on the 1449 images.
    # You can kill it once you see "data layer prefetch queue empty ..."

# Post process your feature maps using crf (... it is long)
    # This process your features maps with crf and save the segmentation result
    # into a binary file
    cd exper
    ./run_densecrf.sh

# Visualize your results
    # In matlab
    /home/gpu_user/assia/ws/tf/deeplab/code/densecrf/my_script/GetDenseCRFResult.m

# Add the layer to write feature maps to your prototxt
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
Modify Makefile to include matio lib

    USE_MATIO ?= 1
    ifeq ($(USE_MATIO), 1)
        LIBRARIES += matio
    endif

Add path to hdf5

    export CPATH="/usr/include/hdf5/serial/"

# Learn the crf parameters with gridsearch

