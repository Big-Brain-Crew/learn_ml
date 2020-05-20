# Imports
import tensorflow as tf
from tf_utils import *


class Model(object):
    '''Represents a Tensorflow Model.
    '''

    def __init__(self):

        self.model = self.build_model()

        

