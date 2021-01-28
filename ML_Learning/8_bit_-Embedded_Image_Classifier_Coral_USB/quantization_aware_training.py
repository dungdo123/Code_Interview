
import dataset
import tensorflow as tf
import argparse
import imageio
import time
from datetime import timedelta
import math
import random
from PIL import Image
import numpy as np
import os
import tensorflow.lite as lite

# Adding Seed so that random initialization is consistent
from numpy.random import seed

seed(1)
from tensorflow import set_random_seed

set_random_seed(2)

# Prepare input data
classes = os.listdir('training_data')
num_classes = len(classes)

# 20% of the data will automatically be used for validation
validation_size = 0.2
img_size = 128
num_channels = 3
train_path = 'training_data'
batch_size = 32

# We shall load all the training and validation images and labels into memory using openCV and use that during training
data = dataset.read_train_sets(train_path, img_size, classes, validation_size=validation_size)

print("Complete reading input data. Will Now print a snippet of it")
print("Number of files in Training-set:\t\t{}".format(len(data.train.labels)))
print("Number of files in Validation-set:\t{}".format(len(data.valid.labels)))


#Network graph params
total_iterations = 0

filter_size_conv1 = 3
num_filters_conv1 = 32

filter_size_conv2 = 3
num_filters_conv2 = 32

filter_size_conv3 = 3
num_filters_conv3 = 64

fc_layer_size = 128

def create_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.05))

def create_biases(size):
    return tf.Variable(tf.constant(0.05, shape=[size]))

def create_convolutional_layer(input,
                               num_input_channels,
                               conv_filter_size,
                               num_filters):
    ## We shall define the weights that will be trained using create_weights function.
    weights = create_weights(shape=[conv_filter_size, conv_filter_size, num_input_channels, num_filters])
    ## We create biases using the create_biases function. These are also trained.
    biases = create_biases(num_filters)

    ## Creating the convolutional layer
    layer = tf.nn.conv2d(input=input,
                         filter=weights,
                         strides=[1, 1, 1, 1],
                         padding='SAME')

    layer += biases

    ## We shall be using max-pooling.
    layer = tf.nn.max_pool(value=layer,
                           ksize=[1, 2, 2, 1],
                           strides=[1, 2, 2, 1],
                           padding='SAME')
    ## Output of pooling is fed to Relu which is the activation function for us.
    layer = tf.nn.relu(layer)

    return layer


def create_flatten_layer(layer):
    # We know that the shape of the layer will be [batch_size img_size img_size num_channels]
    # But let's get it from the previous layer.
    layer_shape = layer.get_shape()

    ## Number of features will be img_height * img_width* num_channels. But we shall calculate it in place of hard-coding it.
    num_features = layer_shape[1:4].num_elements()

    ## Now, we Flatten the layer so we shall have to reshape to num_features
    layer = tf.reshape(layer, [-1, num_features])

    return layer

def create_fc_layer(input,
                    num_inputs,
                    num_outputs,
                    use_relu=True):
    # Let's define trainable weights and biases.
    weights = create_weights(shape=[num_inputs, num_outputs])
    biases = create_biases(num_outputs)

    # Fully connected layer takes input x and produces wx+b.Since, these are matrices, we use matmul function in Tensorflow
    layer = tf.matmul(input, weights) + biases
    if use_relu:
        layer = tf.nn.relu(layer)

    return layer

def model(x):
    with tf.variable_scope('quantized_model'):
        layer_conv1 = create_convolutional_layer(input=x,
                                                 num_input_channels=num_channels,
                                                 conv_filter_size=filter_size_conv1,
                                                 num_filters=num_filters_conv1)
        layer_conv2 = create_convolutional_layer(input=layer_conv1,
                                                 num_input_channels=num_filters_conv1,
                                                 conv_filter_size=filter_size_conv2,
                                                 num_filters=num_filters_conv2)
        layer_conv3 = create_convolutional_layer(input=layer_conv2,
                                                 num_input_channels=num_filters_conv2,
                                                 conv_filter_size=filter_size_conv3,
                                                 num_filters=num_filters_conv3)
        layer_flat = create_flatten_layer(layer_conv3)

        layer_fc1 = create_fc_layer(input=layer_flat,
                                    num_inputs=layer_flat.get_shape()[1:4].num_elements(),
                                    num_outputs=fc_layer_size,
                                    use_relu=True)
        layer_fc2 = create_fc_layer(input=layer_fc1,
                                    num_inputs=fc_layer_size,
                                    num_outputs=num_classes,
                                    use_relu=False)
        y_pred = tf.nn.softmax(layer_fc2, name='y_pred')
        y_pred_cls = tf.argmax(y_pred, dimension=1)

        return y_pred, y_pred_cls

def train(num_iteration, args):
    # define place holder
    image_tf = tf.placeholder(tf.float32, shape=[None, img_size, img_size, num_channels], name='input')
    y_true = tf.placeholder(tf.float32, shape=[None, num_classes], name='output')
    y_true_cls = tf.argmax(y_true, dimension=1)

    # build the model and insert into the graph fake nodes(min/max) for further quantization
    with tf.variable_scope('quantize'):
        y_pred, y_pred_cls = model(image_tf)
    tf.contrib.quantize.create_training_graph(quant_delay = 0)

    # definition of the loss, the optimizer
    loss = tf.losses.mean_squared_error(labels=y_true, predictions=y_pred)

    saver = tf.train.Saver(max_to_keep=1000)

    update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
    with tf.control_dependencies(update_ops):
        optimizer = tf.train.AdamOptimizer().minimize(loss)

    # run training for the several iterations and save dummy checkpoint
    global total_iterations

    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        for i in range(total_iterations, total_iterations + num_iteration):
            x_batch, y_true_batch, _, cls_batch = data.train.next_batch(batch_size)
            x_valid_batch, y_valid_batch, _, valid_cls_batch = data.valid.next_batch(batch_size)

            feed_dict_tr = {image_tf: x_batch, y_true: y_true_batch}
            feed_dict_val = {image_tf: x_valid_batch, y_true: y_valid_batch}

            training_loss, _ = sess.run([loss, optimizer], feed_dict=feed_dict_tr)

            if i % int(data.train.num_examples / batch_size) == 0:
                val_loss = sess.run(loss, feed_dict=feed_dict_val)
                epoch = int(i/int(data.train.num_examples / batch_size))
                #msg = "Training Epoch {0} -- Training Loss: {1>} -- validation loss"
                print(epoch+1, training_loss, val_loss)
                saver.save(sess=sess, save_path = os.path.join(args.chkp, 'dog_cat_test'))

        total_iterations += num_iteration

def export(args):
    graph = tf.Graph()
    with graph.as_default():
        # define the input placeholder and the model (add useless op after the main model,
        # so tflite will not ignore fake min/max nodes of the last layer)
        input = tf.placeholder(tf.float32, [None, img_size, img_size, num_channels], name = 'input')
        with tf.variable_scope('quantize'):
            output, _lable = model(x=input)
            #output = tf.maximum(output, -1e27)

        # define eval graph, by quantizing the weights of the model with learned min/max for each layer
        g = tf.get_default_graph()
        tf.contrib.quantize.create_eval_graph(input_graph = g)
        saver = tf.train.Saver()

        graph.finalize()

        with open('eval.pb', 'w') as f:
            f.write(str(g.as_graph_def()))

    with tf.Session(graph=graph) as session :
        checkpoint = tf.train.latest_checkpoint(args.chkp)
        saver.restore(session, checkpoint)

        # fix the input, output, choose types of the weights and activations for the tflite model
        converter = lite.TFLiteConverter.from_session(session, [input], [output])
        converter.inference_type = tf.uint8
        converter.inference_input_type = tf.uint8
        input_arrays = converter.get_input_arrays()
        converter.quantized_input_stats = {input_arrays[0] : (0., 1.)}

        flatbuffer = converter.convert()

        with open('cat_dog.tflite',  'wb') as outfile:
            outfile.write(flatbuffer)
    print("codel sucessfully converted")

def test():
    # read or create test image, convert to uint8 for the inference with quantized activation
    test_image = imageio.imread('test.jpg')
    test_image = np.array(Image.fromarray(test_image).resize([img_size, img_size]), dtype=np.uint8)

    # define the tflite interpreter and infer on the test image
    interpreter = lite.Interpreter('cat_dog.tflite')

    input_info = interpreter.get_input_details()[0]
    output_info = interpreter.get_output_details()[0]

    interpreter.resize_tensor_input(input_info['index'], (1, img_size, img_size, num_channels))
    interpreter.allocate_tensors()
    interpreter.set_tensor(input_info['index'], test_image[None, ...])
    interpreter.invoke()
    result = interpreter.get_tensor(output_info['index'])
    print(result)
    print('Result saved in the training directory')
def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', default='train', type=str, help='run mode, train/export/test')
    parser.add_argument('--chkp', default='chkp', type=str, help='path to checkpoint directory')
    args = parser.parse_args()

    if args.mode == 'train':
        if not os.path.exists(args.chkp):
            os.makedirs(args.chkp)
        train(200, args)
    if args.mode == 'export':
        export(args)
    if args.mode == 'test':
        test()

if __name__ == '__main__':
    run()



