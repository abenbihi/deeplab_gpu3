
import sys
caffe_root='/home/gpu_user/assia/ws/tf/deeplab/code/'
sys.path.insert(0, caffe_root + 'python')
import caffe

import cv2

import numpy as np
from PIL import Image

import random

class CLCSegDataLayer(caffe.Layer):
    """
    Load (input image, label image) pairs from CLC dataset
    one-at-a-time while reshaping the net to preserve dimensions.

    Use this to feed data to a fully convolutional network.
    """

    def setup(self, bottom, top):
        """
        Setup data layer according to parameters:

        - clc_dir: path to CLC dir
        - split: train / val / test
        - mean: tuple of mean values to subtract
        - randomize: load in random order (default: True)
        - seed: seed for randomization (default: None / current time)

        for CLC semantic segmentation.

        example

        params = dict(data_dir="/path/to/CLC/",
            mean=(B-mean, G-mean, R-mean, IR-mean),
            split="train")
        """
        # config
        params = eval(self.param_str)
        self.data_dir = params['data_dir']
        self.split = params['split']
        self.split_list = params['split_list']
        self.mean = np.array(params['mean'])
        self.random = params.get('randomize', True)
        self.seed = params.get('seed', None)

        # two tops: data and label
        if len(top) != 2:
            raise Exception("Need to define two tops: data and label.")
        # data layers have no bottoms
        if len(bottom) != 0:
            raise Exception("Do not define a bottom.")

        # load indices for images and labels
        split_f  = '{}/{}.txt'.format(self.data_dir,
                self.split_list)
        # list of pair of image and label filenames
        # indices[0].split()[0]: image filename
        # indices[0].split()[1]: label filename
        self.indices = open(split_f, 'r').read().splitlines()
        self.idx = 0

        # make eval deterministic
        if 'train' not in self.split:
            self.random = False

        # randomization: seed and pick
        if self.random:
            random.seed(self.seed)
            self.idx = random.randint(0, len(self.indices)-1)


    def reshape(self, bottom, top):
        image_filename = self.indices[self.idx].split()[0]
        label_filename = self.indices[self.idx].split()[1]
        self.data = self.load_image(image_filename)
        self.label = self.load_label(label_filename)

        top[0].reshape(1, *self.data.shape)
        top[1].reshape(1, *self.label.shape)


    def forward(self, bottom, top):
        # assign output
        top[0].data[...] = self.data
        top[1].data[...] = self.label

        # pick next input
        if self.random:
            self.idx = random.randint(0, len(self.indices)-1)
        else:
            self.idx += 1
            if self.idx == len(self.indices):
                self.idx = 0


    def backward(self, top, propagate_down, bottom):
        pass


    def load_image(self, filename):
        """
        Load input image and preprocess for Caffe:
        - cast to float
        - switch channels RGB -> BGR
        - subtract mean
        - transpose to channel x height x width order
        """
        #print("image_filename: ", filename)
        im = Image.open(filename)
        im = im.resize((321,321), Image.BILINEAR)
        in_ = np.array(im, dtype=np.float32)
        #print("in_.shape: ", in_.shape)
        
        # RGB-IR -> BGR-IR
        bgr_im = in_[:,:,0:3]
        bgr_im = bgr_im[:,:,::-1]
        in_[:,:,0:3] = bgr_im

        #print("in_.shape: ", in_.shape)
        in_ -= self.mean
        in_ = in_.transpose((2,0,1)) #HWC -> CHW
        #print("in_.shape: ", in_.shape)
        return in_


    def load_label(self, filename):
        """
        Load label image as 1 x height x width integer array of label indices.
        The leading singleton dimension is required by the loss.
        """
        im = Image.open(filename)
        im = im.resize((321,321), Image.BILINEAR)
        label = np.array(im, dtype=np.uint8)
        label = label[np.newaxis, ...]
        return label


