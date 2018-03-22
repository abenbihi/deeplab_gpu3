"""

"""
caffe_root='/home/gpu_user/assia/ws/tf/deeplab/code/'

# Setup python environment
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, caffe_root + 'python') # add caffe module is in path
import caffe
from caffe import layers, params

# set display defaults
plt.rcParams['figure.figsize'] = (10, 10)        # large images
plt.rcParams['image.interpolation'] = 'nearest'  # don't interpolate: show square pixels
plt.rcParams['image.cmap'] = 'gray'  # use grayscale output rather than a (potentially misleading) color heatmap
# Helper function for deprocessing preprocessed images, e.g., for display.


def deprocess_net_image(image, mean):
    """
    mean: [R,G,B]
    """
    image = image.copy()              # don't modify destructively
    image = image[::-1]               # BGR -> RGB
    image = image.transpose(1, 2, 0)  # CHW -> HWC
    image += mean  #[123, 117, 104]          # (approximately) undo mean subtraction

    # clamp values in [0, 255]
    image[image < 0], image[image > 255] = 0, 255

    # round and cast from float32 to uint8
    image = np.round(image)
    image = np.require(image, dtype=np.uint8)

    return image

def deprocess_net_image_multi_channel(image, mean):
    """
    mean: [R,G,B,IR]
    """
    image = image.copy()              # don't modify destructively
    image = image.transpose(1, 2, 0)  # CHW -> HWC
    image += mean  #[123, 117, 104]          # (approximately) undo mean subtraction

    # clamp values in [0, 255]
    image[image < 0], image[image > 255] = 0, 255

    # round and cast from float32 to uint8
    image = np.round(image)
    image = np.require(image, dtype=np.uint8)

    return image

def disp_preds(net, image, labels):
    input_blob = net.blobs['data']
    net.blobs['data'].data[0, ...] = image
    output = net.forward(start='conv1')['n.score'][0]
    plt.imshow(deprocess_net_image(image, mean))
    #plt.imshow(deprocess_net_image(labels))
    #plt.imshow(deprocess_net_image(output))

