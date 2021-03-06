import os
import numpy as np
import cv2
import sys
import cPickle as pickle
import glob
import random
from tqdm import tqdm
from eliaLib import dataRepresentation
import matplotlib.pyplot as plt

import theano
import theano.tensor as T
import lasagne

from lasagne.layers import InputLayer, DenseLayer, NonlinearityLayer,InverseLayer
from lasagne.layers import Conv2DLayer as ConvLayer
from lasagne.layers import Pool2DLayer as PoolLayer
from lasagne.nonlinearities import softmax
from lasagne.utils import floatX

from lasagne.layers import DenseLayer
from lasagne.layers import InputLayer
from lasagne.layers import DropoutLayer
from lasagne.layers import Conv2DLayer
from lasagne.layers import MaxPool2DLayer
from lasagne.layers import Upscale2DLayer
from lasagne.nonlinearities import softmax

def buildNetwork( inputWidth, inputHeight, input_var=None ):
    net = {}
    net['input'] = InputLayer((None, 3, inputWidth, inputHeight), input_var=input_var)
    #print "Input: {}".format(net['input'].output_shape[1:])
    
    net['conv1_1'] = ConvLayer(net['input'], 64, 3, pad=1)
    net['conv1_1'].add_param(net['conv1_1'].W, net['conv1_1'].W.get_value().shape, trainable=False)
    net['conv1_1'].add_param(net['conv1_1'].b, net['conv1_1'].b.get_value().shape, trainable=False)
    #print "Input: {}".format(net['conv1_1'].output_shape[1:])
    
    net['conv1_2'] = ConvLayer(net['conv1_1'], 64, 3, pad=1)
    net['conv1_2'].add_param(net['conv1_2'].W, net['conv1_2'].W.get_value().shape, trainable=False)
    net['conv1_2'].add_param(net['conv1_2'].b, net['conv1_2'].b.get_value().shape, trainable=False)
    #print "Input: {}".format(net['conv1_2'].output_shape[1:])
    
    net['pool1'] = PoolLayer(net['conv1_2'], 2)
    #print "Input: {}".format(net['pool1'].output_shape[1:])
    
    net['conv2_1'] = ConvLayer(net['pool1'], 128, 3, pad=1)
    net['conv2_1'].add_param(net['conv2_1'].W, net['conv2_1'].W.get_value().shape, trainable=False)
    net['conv2_1'].add_param(net['conv2_1'].b, net['conv2_1'].b.get_value().shape, trainable=False)
    #print "Input: {}".format(net['conv2_1'].output_shape[1:])
    
    net['conv2_2'] = ConvLayer(net['conv2_1'], 128, 3, pad=1)
    net['conv2_2'].add_param(net['conv2_2'].W, net['conv2_2'].W.get_value().shape, trainable=False)
    net['conv2_2'].add_param(net['conv2_2'].b, net['conv2_2'].b.get_value().shape, trainable=False)
    #print "Input: {}".format(net['conv2_2'].output_shape[1:])
    
    net['pool2'] = PoolLayer(net['conv2_2'], 2)
    #print "Input: {}".format(net['pool2'].output_shape[1:])
    
    net['conv3_1'] = ConvLayer(net['pool2'], 256, 3, pad=1)
    net['conv3_1'].add_param(net['conv3_1'].W, net['conv3_1'].W.get_value().shape, trainable=False)
    net['conv3_1'].add_param(net['conv3_1'].b, net['conv3_1'].b.get_value().shape, trainable=False)
    #print "Input: {}".format(net['conv3_1'].output_shape[1:])
    
    net['conv3_2'] = ConvLayer(net['conv3_1'], 256, 3, pad=1)
    net['conv3_2'].add_param(net['conv3_2'].W, net['conv3_2'].W.get_value().shape, trainable=False)
    net['conv3_2'].add_param(net['conv3_2'].b, net['conv3_2'].b.get_value().shape, trainable=False)
    #print "Input: {}".format(net['conv3_2'].output_shape[1:])
    
    net['conv3_3'] = ConvLayer(net['conv3_2'], 256, 3, pad=1)
    net['conv3_3'].add_param(net['conv3_3'].W, net['conv3_3'].W.get_value().shape, trainable=False)
    net['conv3_3'].add_param(net['conv3_3'].b, net['conv3_3'].b.get_value().shape, trainable=False)
    #print "Input: {}".format(net['conv3_3'].output_shape[1:])
    
    net['pool3'] = PoolLayer(net['conv3_3'], 2)
    #print "Input: {}".format(net['pool3'].output_shape[1:])
    
    net['conv4_1'] = ConvLayer(net['pool3'], 512, 3, pad=1)
    net['conv4_1'].add_param(net['conv4_1'].W, net['conv4_1'].W.get_value().shape, trainable=False)
    net['conv4_1'].add_param(net['conv4_1'].b, net['conv4_1'].b.get_value().shape, trainable=False)
    #print "Input: {}".format(net['conv4_1'].output_shape[1:])
    
    net['conv4_2'] = ConvLayer(net['conv4_1'], 512, 3, pad=1)
    net['conv4_2'].add_param(net['conv4_2'].W, net['conv4_2'].W.get_value().shape, trainable=False)
    net['conv4_2'].add_param(net['conv4_2'].b, net['conv4_2'].b.get_value().shape, trainable=False)
    #print "Input: {}".format(net['conv4_2'].output_shape[1:])
    
    net['conv4_3'] = ConvLayer(net['conv4_2'], 512, 3, pad=1)
    net['conv4_3'].add_param(net['conv4_3'].W, net['conv3_1'].W.get_value().shape, trainable=False)
    net['conv4_3'].add_param(net['conv4_3'].b, net['conv4_3'].b.get_value().shape, trainable=False)
    #print "Input: {}".format(net['conv4_3'].output_shape[1:])
    
    net['pool4'] = PoolLayer(net['conv4_3'], 2)
    #print "Input: {}".format(net['pool4'].output_shape[1:])
    
    net['conv5_1'] = ConvLayer(net['pool4'], 512, 3, pad=1)
    net['conv5_1'].add_param(net['conv5_1'].W, net['conv5_1'].W.get_value().shape, trainable=False)
    net['conv5_1'].add_param(net['conv5_1'].b, net['conv5_1'].b.get_value().shape, trainable=False)
    #print "Input: {}".format(net['conv5_1'].output_shape[1:])
    
    net['conv5_2'] = ConvLayer(net['conv5_1'], 512, 3, pad=1)
    net['conv5_2'].add_param(net['conv5_2'].W, net['conv5_2'].W.get_value().shape, trainable=False)
    net['conv5_2'].add_param(net['conv5_2'].b, net['conv5_2'].b.get_value().shape, trainable=False)
    #print "Input: {}".format(net['conv5_2'].output_shape[1:])
    
    net['conv5_3'] = ConvLayer(net['conv5_2'], 512, 3, pad=1)
    net['conv5_3'].add_param(net['conv5_3'].W, net['conv5_3'].W.get_value().shape, trainable=False)
    net['conv5_3'].add_param(net['conv5_3'].b, net['conv5_3'].b.get_value().shape, trainable=False)
    #print "Input: {}".format(net['conv5_3'].output_shape[1:])
    
    net['pool5'] = PoolLayer(net['conv5_3'], 2)
    #print "Input: {}".format(net['output'].output_shape[1:])

    net['upool5'] = Upscale2DLayer(net['pool5'], scale_factor=2)
    #print "upool5: {}".format(net['upool5'].output_shape[1:])

    net['uconv5_3'] = ConvLayer(net['upool5'], 512, 3, pad=1)
    #print "uconv5_3: {}".format(net['uconv5_3'].output_shape[1:])

    net['uconv5_2'] = ConvLayer(net['uconv5_3'], 512, 3, pad=1)
    #print "uconv5_2: {}".format(net['uconv5_2'].output_shape[1:])

    net['uconv5_1'] = ConvLayer(net['uconv5_2'], 512, 3, pad=1)
    #print "uconv5_1: {}".format(net['uconv5_1'].output_shape[1:])

    net['upool4'] = Upscale2DLayer(net['uconv5_1'], scale_factor=2)
    #print "upool4: {}".format(net['upool4'].output_shape[1:])

    net['uconv4_3'] = ConvLayer(net['upool4'], 512, 3, pad=1)
    #print "uconv4_3: {}".format(net['uconv4_3'].output_shape[1:])

    net['uconv4_2'] = ConvLayer(net['uconv4_3'], 512, 3, pad=1)
    #print "uconv4_2: {}".format(net['uconv4_2'].output_shape[1:])

    net['uconv4_1'] = ConvLayer(net['uconv4_2'], 512, 3, pad=1)
    #print "uconv4_1: {}".format(net['uconv4_1'].output_shape[1:])

    net['upool3'] = Upscale2DLayer(net['uconv4_1'], scale_factor=2)
    #print "upool3: {}".format(net['upool3'].output_shape[1:])

    net['uconv3_3'] = ConvLayer(net['upool3'], 256, 3, pad=1)
    #print "uconv3_3: {}".format(net['uconv3_3'].output_shape[1:])

    net['uconv3_2'] = ConvLayer(net['uconv3_3'], 256, 3, pad=1)
    #print "uconv3_2: {}".format(net['uconv3_2'].output_shape[1:])

    net['uconv3_1'] = ConvLayer(net['uconv3_2'], 256, 3, pad=1)
    #print "uconv3_1: {}".format(net['uconv3_1'].output_shape[1:])

    net['upool2'] = Upscale2DLayer(net['uconv3_1'], scale_factor=2)
    #print "upool2: {}".format(net['upool2'].output_shape[1:])

    net['uconv2_2'] = ConvLayer(net['upool2'], 128, 3, pad=1)
    #print "uconv2_2: {}".format(net['uconv2_2'].output_shape[1:])

    net['uconv2_1'] = ConvLayer(net['uconv2_2'], 128, 3, pad=1)
    #print "uconv2_1: {}".format(net['uconv2_1'].output_shape[1:])

    net['upool1'] = Upscale2DLayer(net['uconv2_1'], scale_factor=2)
    #print "upool1: {}".format(net['upool1'].output_shape[1:])

    net['uconv1_2'] = ConvLayer(net['upool1'], 64, 3, pad=1)
    #print "uconv1_2: {}".format(net['uconv1_2'].output_shape[1:])

    net['uconv1_1'] = ConvLayer(net['uconv1_2'], 64, 3, pad=1)
    #print "uconv1_1: {}".format(net['uconv1_1'].output_shape[1:])

    net['output'] = ConvLayer(net['uconv1_1'], 1, 1, pad=0)
    #print "output: {}".format(net['output'].output_shape[1:])


    return net

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):

        yield l[i:i+n]

if __name__ == "__main__":
	
	# Load data
	print 'Loading validation data...'
	with open( 'validationData.pickle', 'rb') as f:
		validationData = pickle.load( f )       
	print '-->done!'

	# with open( 'testData.pickle', 'rb') as f:
		# testData = pickle.load( f )   

	# Create network
	inputImage = T.tensor4()
	outputSaliency = T.tensor4()

	width = 256
	height = 192

	net = buildNetwork(height,width,inputImage)
	
	epochToLoad = 0
	
	with np.load("modelWights{:04d}.npz".format(epochToLoad)) as f:
		param_values = [f['arr_%d' % i] for i in range(len(f.files))]
	lasagne.layers.set_all_param_values(net['output'], param_values)

	test_prediction = lasagne.layers.get_output(net['output'], deterministic=True)
	predict_fn = theano.function([inputImage], test_prediction)

	imageMean = np.array([[[103.939]],[[116.779]],[[123.68]]])

	# Let's pick a random image and process it!
	
	numRandom = random.choice(range(len(validationData)))
	
	cv2.imwrite( 'validationRandomImage.png', cv2.cvtColor( validationData[numRandom].image.data, cv2.cv.CV_RGB2BGR ) )
	cv2.imwrite( 'validationRandomSaliencyGT.png', validationData[numRandom].saliency.data )
		
	blob = np.zeros((1, 3, height, width ), theano.config.floatX )
	blob[0,...] = ( validationData[numRandom].image.data.astype(theano.config.floatX).transpose(2,0,1)-imageMean)/255.
	result = np.squeeze( predict_fn( blob ) )
	
	cv2.imwrite( 'validationRandomSaliencyPred.png', ( result * 255 ).astype(np.uint8) )
	

	