#!/bin/bash 

ROOT_DIR=/home/gpu_user/assia/ws/tf/deeplab
DATA_ROOT_DIR=/home/gpu_user/assia/ws/datasets/
###########################################
# You can either use this script to generate the DenseCRF post-processed results
# or use the densecrf_layer (wrapper) in Caffe
###########################################
DATASET=antoine
LOAD_MAT_FILE=1

MODEL_NAME=antoine

TEST_SET=val          #val, test

# the features  folder save the features computed via the model trained with the train set
# the features2 folder save the features computed via the model trained with the trainval set
FEATURE_NAME=features #features, features2
FEATURE_TYPE=fc8

# specify the parameters
MAX_ITER=10

Bi_W=4
Bi_X_STD=49
Bi_Y_STD=49
Bi_R_STD=5
Bi_G_STD=5 
Bi_B_STD=5

POS_W=3
POS_X_STD=3
POS_Y_STD=3


#######################################
# MODIFY THE PATY FOR YOUR SETTING
#######################################
SAVE_DIR=${ROOT_DIR}/exper/${DATASET}/res/${FEATURE_NAME}/${MODEL_NAME}/${TEST_SET}/${FEATURE_TYPE}/62/post_densecrf_W${Bi_W}_XStd${Bi_X_STD}_RStd${Bi_R_STD}_PosW${POS_W}_PosXStd${POS_X_STD}

echo "SAVE TO ${SAVE_DIR}"

CRF_DIR=${ROOT_DIR}/code/densecrf

# NOTE THAT the densecrf code only loads ppm images
IMG_DIR_NAME="${DATA_ROOT_DIR}"antoine 
IMG_DIR=${IMG_DIR_NAME}/62000_PPMImages

if [ ${LOAD_MAT_FILE} == 1 ]
then
    # the features are saved in .mat format
    CRF_BIN=${CRF_DIR}/prog_refine_pascal_v4
    #FEATURE_DIR=${ROOT_DIR}/exper/${DATASET}/${FEATURE_NAME}/${MODEL_NAME}/${TEST_SET}/${FEATURE_TYPE}
    #FEATURE_DIR=/home/gpu_user/antoine/ws/data/MAT/files
    FEATURE_DIR=/home/gpu_user/assia/ws/datasets/antoine/features/62000
else
    # the features are saved in .bin format (has called SaveMatAsBin.m in the densecrf/my_script)
    CRF_BIN=${CRF_DIR}/prog_refine_pascal
    FEATURE_DIR=${ROOT_DIR}/exper/${DATASET}/${FEATURE_NAME}/${MODEL_NAME}/${TEST_SET}/${FEATURE_TYPE}/bin
fi

mkdir -p ${SAVE_DIR}

# run the program
echo "${CRF_BIN} -id ${IMG_DIR} -fd ${FEATURE_DIR} -sd ${SAVE_DIR} -i ${MAX_ITER} -px ${POS_X_STD} -py ${POS_Y_STD} -pw ${POS_W} -bx ${Bi_X_STD} -by ${Bi_Y_STD} -br ${Bi_R_STD} -bg ${Bi_G_STD} -bb ${Bi_B_STD} -bw ${Bi_W}"
${CRF_BIN} -id ${IMG_DIR} -fd ${FEATURE_DIR} -sd ${SAVE_DIR} -i ${MAX_ITER} -px ${POS_X_STD} -py ${POS_Y_STD} -pw ${POS_W} -bx ${Bi_X_STD} -by ${Bi_Y_STD} -br ${Bi_R_STD} -bg ${Bi_G_STD} -bb ${Bi_B_STD} -bw ${Bi_W}

