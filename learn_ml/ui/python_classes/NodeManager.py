'''
'''

import random
import numpy as np
import difflib
import json

from PySide2.QtCore import QObject, Signal, Slot, Property
from PySide2.QtQml import QQmlProperty

from learn_ml.utils.log_configurator import LogConfigurator
import learn_ml.generators.json_generators as json_generators
import learn_ml.generators.generator_utils as generator_utils
import learn_ml.generators.python_generators as python_generators


class NodeManager(QObject):
    ''' Receives a user input and generates a list of search results. 

    Interfaces with QML through the use of slots, signals, and properties.
    '''

    def __init__(self):
        QObject.__init__(self)

        # Instantiate LogConfigurator
        self.log_config = LogConfigurator()

        # Get the logger for module
        self.logger = self.log_config.get_logger(__name__)

        self.layer_options = json.load(open(
            "learn_ml/generators/options/layer_options.json"))["layer_options"]

        self.json_config = json_generators.ModelJsonGenerator("project/model.json")

        # Store all layer names in order
        self.layers = []

    @Slot(str)
    def add_node(self, name):
        self.layers.append({
            "name": name,
            "args": {}
        }
        )

    @Slot(str, result="QVariant")
    def get_parameters(self, name):
        return self.layer_options[name]

    @Slot("QVariant")
    def update_params(self, nodes):
        nodes = nodes.toVariant()
        for i in range(len(nodes)):
            name = nodes[i].property("text")
            parameters = nodes[i].property("parameters").toVariant()

            parameters = self.__convert_params(parameters)

            self.layers[i]["args"] = parameters

    # Convert parameters from front-end to back-end format
    def __convert_params(self, parameters):
        converted_params = {}
        for param in parameters:
            if param["type"] == "int":
                param["value"] = int(param["value"])
            elif param["type"] == "List[int]":
                param["value"] = list(map(int,param["value"].split('[')[1].split(']')[0].replace(" ","").split(',')))
                # newparam = list(map(int, test))
            converted_params[param["name"]] = param["value"]
        return converted_params

    @Slot(str)
    def add_model(self, model_name):
        self.json_config.add_model(model_name)

    @Slot()
    def train(self):
        self.add_model("sequential")

        for layer in self.layers:
            self.json_config.add_layer(layer["name"].lower(), layer["args"])

        args = {
        "loss" : "crossentropy",
        "optimizer" : generator_utils.create_fn_dict("adam", {"learning_rate" : 0.001}),
        "metrics" : ["accuracy"]
        }
        self.json_config.add_compile(args)

        self.json_config.write()

        create_model()
        create_pipeline_json()
        create_pipeline()
        import project.train as train

        train.train("pipeline_1", "model_1")

    # QML accessible properties
def create_model():
    pipe_gen = python_generators.ModelGenerator(model_config="project/model.json",
                                                map_config="learn_ml/generators/model_map.json",
                                                out="./project/models/model_1.py")
    pipe_gen.gen_model()

def create_pipeline():
    pipe_gen = python_generators.PipelineGenerator(pipeline_config="project/pipeline.json",
                                                   map_config="learn_ml/generators/pipeline_map.json",
                                                   out="./project/pipelines/pipeline_1.py")
    pipe_gen.gen_pipeline()

def create_pipeline_json():
    config_gen = json_generators.PipelineJsonGenerator("project/pipeline.json")

    config_gen.add_dataset("mnist")

    args = {
        "map_func" : "normalize_img",
        "num_parallel_calls" : "autotune"
    }
    config_gen.add_train_operation("map", args)

    args = {}
    config_gen.add_train_operation("cache", args)

    args = {
        "buffer_size" : "train_size",
    }
    config_gen.add_train_operation("shuffle", args)

    args = {
        "batch_size" : 128
    }
    config_gen.add_train_operation("batch", args)

    args = {
        "buffer_size" : "autotune"
    }
    config_gen.add_train_operation("prefetch", args)

    args = {
        "map_func" : "normalize_img",
        "num_parallel_calls" : "autotune"
    }
    config_gen.add_test_operation("map", args)

    args = {}
    config_gen.add_test_operation("cache", args)

    args = {
        "batch_size" : 128
    }
    config_gen.add_test_operation("batch", args)

    args = {
        "buffer_size" : "autotune"
    }
    config_gen.add_test_operation("prefetch", args)


    config_gen.write()