import time
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import mnist_inference
import mnist_train

EVAL_INTERVAL_SECS = 10

def evaluate(mnits):
    with tf.Graph().as_default() as g:
        x = tf.placeholder(tf.float32,shape=[None,mnist_inference.INPUT_NODE],name="x-input")
        y_ = tf.placeholder(tf.float32,shape=[None,mnist_inference.OUTPUT_NODE],name="y-input")
        validate_feed = {x:mnits.validation.images,y_:mnits.validation.labels}
        y = mnist_inference.inference(x,None)
        correct_predition = tf.equal(tf.arg_max(y,1),tf.arg_max(y_,1))
        accuracy = tf.reduce_mean(tf.cast(correct_predition,tf.float32))
        variable_averages = tf.train.ExponentialMovingAverage(mnist_train.MOVING_AVERAGE_DECAY)
        variable_to_restore = variable_averages.variables_to_restore()
        saver = tf.train.Saver(variable_to_restore)

        while True:
            with tf.Session() as sees:
                ckpt = tf.train.get_checkpoint_state(mnist_train.MODEL_SAVE_PATH)
                if ckpt and ckpt.model_checkpoint_path:
                    saver.restore(sees,ckpt.model_checkpoint_path)
                    global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
                    accuracy_score = sees.run(accuracy,feed_dict=validate_feed)
                    print("After %s training step(s),validation accuracy = %g" % (global_step,accuracy_score))
                else:
                    print("No checkpoint file found")
            time.sleep(EVAL_INTERVAL_SECS)

def main(argv=None):
    mnist = input_data.read_data_sets("MNIST_data", one_hot=True)
    evaluate(mnist)

if __name__ == '__main__':
    main()