#!/bin/bash 


# DO NOT CHANGE UNLESS YOU KNOW WHAT YOU ARE DOING
ROOT_DIR=/home/gpu_user/assia/ws/tf/deeplab
DATA_ROOT_DIR=/home/gpu_user/AgroParisTech/data/new_dataset/
CRF_DIR=${ROOT_DIR}/code/densecrf

# Crf parameter 
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

# TODO Your changes 
DATASET=Data2015
XP_NAME=bgrir_sgd



SAVE_DIR=${ROOT_DIR}/exper/antoine/res/${XP_NAME}/bin
IMG_DIR="${DATA_ROOT_DIR}""${DATASET}"/Valid/PPMImages/
CRF_BIN=${CRF_DIR}/prog_refine_pascal_v4
FEATURE_DIR=${ROOT_DIR}/exper/antoine/features/${XP_NAME}

mkdir -p ${SAVE_DIR}

# run the program
#echo "${CRF_BIN} -id ${IMG_DIR} -fd ${FEATURE_DIR} -sd ${SAVE_DIR} -i ${MAX_ITER} -px ${POS_X_STD} -py ${POS_Y_STD} -pw ${POS_W} -bx ${Bi_X_STD} -by ${Bi_Y_STD} -br ${Bi_R_STD} -bg ${Bi_G_STD} -bb ${Bi_B_STD} -bw ${Bi_W}"

${CRF_BIN} -id ${IMG_DIR} -fd ${FEATURE_DIR} -sd ${SAVE_DIR} -i ${MAX_ITER} -px ${POS_X_STD} -py ${POS_Y_STD} -pw ${POS_W} -bx ${Bi_X_STD} -by ${Bi_Y_STD} -br ${Bi_R_STD} -bg ${Bi_G_STD} -bb ${Bi_B_STD} -bw ${Bi_W}

