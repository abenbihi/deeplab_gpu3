"""
Run the finetuning
"""
# Setup python environment
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
caffe_root='/home/gpu_user/assia/ws/tf/deeplab/code/'
sys.path.insert(0, caffe_root + 'python')
import caffe
from caffe import layers, params
from caffe.proto import caffe_pb2
import cv2
import json
import time

import tools

# Set caffe mode
caffe.set_device(0)
caffe.set_mode_gpu()

# set display defaults
plt.rcParams['figure.figsize'] = (10, 10)        # large images
plt.rcParams['image.interpolation'] = 'nearest'  # don't interpolate: show square pixels
plt.rcParams['image.cmap'] = 'gray'  # use grayscale output rather than a (potentially misleading) color heatmap

def main():
    # Check trained weights exist
    model_weights = '/home/gpu_user/assia/ws/tf/deeplab/exper/antoine/config/resnet/train_iter_20000.caffemodel'
    if os.path.isfile(model_weights):
      print 'Old weigths found'
    else:
      print 'Error: Old weigths do not exist'
      exit()
    
    # Run one training step
    new_solver = caffe.get_solver('/home/gpu_user/assia/ws/tf/deeplab/exper/antoine/config/resnet/solver_train.prototxt') 
    new_solver.net.copy_from(model_weights)
    new_solver.step(1)

    # check data
    batch_index = 0
    for batch_index in range(1):
        image = new_solver.net.blobs['data'].data[batch_index]
        label = new_solver.net.blobs['label'].data[batch_index]

        label = label.transpose(1,2,0)
        #print('image_shape', image.shape)
        #print('label_shape', label.shape)

        mean = (104.008, 116.669, 122.675, 128.00)
        image_processed = tools.deprocess_net_image_multi_channel(image, mean)
        
        image_bgr = image_processed[:,:,0:3]
        image_ir = image_processed[:,:,3]
        cv2.imwrite('image_bgr_%d.png'%(batch_index), image_bgr)
        cv2.imwrite('image_ir_%d.png'%(batch_index), image_ir)
        cv2.imwrite('label_%d.png' %(batch_index), label)

if __name__=='__main__':
    main()


