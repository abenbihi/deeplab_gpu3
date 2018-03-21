#!/bin/bash 

ROOT_DIR=/home/gpu_user/assia/ws/tf/deeplab
DATA_ROOT_DIR=/home/gpu_user/assia/ws/datasets/
###########################################
# You can either use this script to generate the DenseCRF post-processed results
# or use the densecrf_layer (wrapper) in Caffe
###########################################
DATASET=antoine
XP_NAME=bgrir_sgd

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

SAVE_DIR=${ROOT_DIR}/exper/${DATASET}/res/${TEST_SET}/bin
CRF_DIR=${ROOT_DIR}/code/densecrf

IMG_DIR_NAME="${DATA_ROOT_DIR}"antoine 
IMG_DIR=${IMG_DIR_NAME}/63000_PPMImages

CRF_BIN=${CRF_DIR}/prog_refine_pascal_v4
FEATURE_DIR=${ROOT_DIR}/exper/${DATSET}/features/${TEST_SET}

mkdir -p ${SAVE_DIR}

# run the program
#echo "${CRF_BIN} -id ${IMG_DIR} -fd ${FEATURE_DIR} -sd ${SAVE_DIR} -i ${MAX_ITER} -px ${POS_X_STD} -py ${POS_Y_STD} -pw ${POS_W} -bx ${Bi_X_STD} -by ${Bi_Y_STD} -br ${Bi_R_STD} -bg ${Bi_G_STD} -bb ${Bi_B_STD} -bw ${Bi_W}"

${CRF_BIN} -id ${IMG_DIR} -fd ${FEATURE_DIR} -sd ${SAVE_DIR} -i ${MAX_ITER} -px ${POS_X_STD} -py ${POS_Y_STD} -pw ${POS_W} -bx ${Bi_X_STD} -by ${Bi_Y_STD} -br ${Bi_R_STD} -bg ${Bi_G_STD} -bb ${Bi_B_STD} -bw ${Bi_W}

