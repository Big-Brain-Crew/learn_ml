# Imports
import tensorflow as tf
import tf_utils as tf_utils


class Model(object):
    '''Represents a Tensorflow Model.
    '''

    def __init__(self, dataset):
        self.ds = dataset
        self.build()
        self.compile()

        

    def build(self):
        '''Build the MNIST model.
        '''

        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=[28, 28, 1]),
            tf.keras.layers.Dense(units=128, activation=tf.nn.relu),
            tf.keras.layers.Dense(units=10, activation=tf.nn.softmax),
        ])
        

    def compile(self):
        '''Compile the MNIST model.
        '''

        self.model.compile(loss=tf.keras.losses.sparse_categorical_crossentropy, optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), metrics=['accuracy'])        

    def train(self):
        '''Train the model.
        '''

        self.model.fit(self.ds,epochs=5)

        

    def save(self, filepath="./project/model"):
        '''Save the model in Tensorflow format.
        '''

        self.model.save(filepath)
        

