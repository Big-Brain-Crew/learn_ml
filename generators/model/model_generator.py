'''
'''
import json
from generators.base_generators import PythonGenerator, JsonGenerator


class ModelGenerator(PythonGenerator):
    '''Generates a machine learning model based off a JSON config file.
    '''

    def __init__(self,
                 model_config="generators/model/model.json",
                 mapping_config="generators/model/model_variable_map.json"):

        assert model_config is not None

        # Load config files
        config_file = open(model_config)  # JSON defining the model
        mapping_file = open(mapping_config)  # JSON defining values specific to program language
        self.model = json.load(config_file)["model"]
        self.map = json.load(mapping_file)["model_map"]

        # Label for dataset being used
        self.model_name = self._map(self.model["model"]["model_name"])

        super(ModelGenerator, self).__init__(out="generators/model/model.py")

    def _imports(self):
        ''' Generate import statements.
        '''

        self._write("# Imports\n")
        self._write("import tensorflow as tf\n")
        self._write("import generators.tf_utils as tf_utils\n")
        self._write("\n\n")

    def _class_def(self):
        ''' Generate Model class definition.
        '''

        # DatasetPipeline class
        self._write("class Model(object):\n")
        self._indent()
        self._write_docstring("Represents a Tensorflow Model.\n")

        # Init
        self._write("def __init__(self, dataset):\n\n")
        self._indent()
        self._write("self.ds = dataset\n")
        self._write("self.build()\n")
        self._write("self.compile()\n\n")


        self._end_method()

    def _map(self, input):
        ''' Converts an input to its language-specific representation.

        This function allows the model JSON language to be independent of implementation syntax.
        For example, the model may have a dense layer. The Tensorflow code for this is 
        tf.keras.layers.Dense(). This input retrieves that language-specific syntax.
        '''

        # Return the mapped output in quotations if it is of type string
        if isinstance(input, str) and input in self.map:
            return "\"{}\"".format(self.map[input]["name"]) \
                if self.map[input]["type"] == "string" else self.map[input]["name"]
        else:
            return input  # Input not in the map

    def _map_fn(self, function):
        ''' Convert parameter value representations to their actual values.
            This is necessary to keep the pipeline config file independent of
            specific function names, i.e. tf2 function calls.
        '''

        # Create mapped function dict and add name
        mapped_fn = {
            "name": self._map(function["name"]),
            "args": {}
        }

        # Map function args
        for _param, _value in function["args"].items():
            mapped_fn["args"][self._map(_param)] = self._fn_str(self._map_fn(_value)) if isinstance(_value, dict) else self._map(_value)

        return mapped_fn

    def _fn_str(self, fn_dict):
        ''' Convert a function in dictionary form to a string.
        '''

        arg_str = ', '.join(["{param}={val}".format(param=param, val=val)
                             for param, val in fn_dict["args"].items()])
        return "{fn_name}({args})".format(fn_name=fn_dict["name"],
                                          args=arg_str)

    def _build_model(self):
        '''Generate code for building the model.
        '''

        self._start_method()
        self._write("def build(self):\n")
        self._indent()
        self._write_docstring("Build the MNIST model.\n")

        self._write("self.model = {model}([\n".format(model=self.model_name))
        self._indent()

        for _layer in self.model["layers"]:
            _layer = self._map_fn(_layer)
            self._write(self._fn_str(_layer) + ",\n")

        self._unindent()
        self._write("])\n")

        self._end_method()

    def _compile_model(self):
        '''Generate code for the model compiler.
        '''

        self._start_method()
        self._write("def compile(self):\n")
        self._indent()
        self._write_docstring("Compile the MNIST model.\n")

        compile_fn = self._fn_str(self._map_fn(self.model["compile"]))
        self._write("self.model.{fn}".format(fn=compile_fn))

        self._end_method()
    
    def _train(self):
        ''' Generate code to train the model.
        '''

        self._start_method()
        self._write("def train(self, epochs=5):\n")
        self._indent()
        self._write_docstring("Train the model.\n")
        self._write("self.model.fit(self.ds,epochs=5)\n\n")

        self._end_method()

    def _helper_funcs(self):
        ''' Generates get/set helper functions.
        '''
        pass

    def gen_model(self):
        ''' Generate all code part of the dataset pipeline.
        '''

        self._imports()
        self._class_def()
        self._build_model()
        self._compile_model()
        self._train()
        self._helper_funcs()

        print("Saved to {}".format(self.out_file_name))

    def get_pipeline_file_name(self):
        '''Returns the name of the generated pipeline script.

        Currently the file name is not modifiable.
        '''

        return self.out


# class PipelineConfigGenerator(JsonGenerator):
#     ''' Generates a pipeline config JSON file based on user selections.

#     Generates a config file that describes a dataset preprocessing pipeline
#     based off a user's selection of dataset source and preprocessing operations.
#     '''

#     def __init__(self, out_file):

#         super(PipelineConfigGenerator, self).__init__(out_file)

#         # Add the root dict
#         self.add_entry("pipeline", {})

#         # Add the dataset and operations
#         self.indent("pipeline")
#         self.add_entry("dataset", {})
#         self.add_entry("operations", [])

#     def add_dataset(self, label):
#         ''' Add a dataset source.

#         All available datasets can be found in the Tensorflow Datasets catalog.
#             (https://www.tensorflow.org/datasets/catalog/overview)

#         Args:
#             label : dataset identifier. Equivalent to the Tensorflow dataset name.
#         '''

#         self.add_entry("dataset", {"label": label})

#     def add_operation(self, op_name, args={}):
#         ''' Add a preprocessing operation.

#         A list of all allowable operations can be found as methods for the tf.data.Dataset class
#             (https://www.tensorflow.org/api_docs/python/tf/data/Dataset)

#         Args:
#             op_name : Name of the operation. Equivalent to a tf.Dataset method name.
#             args : Dictionary of arguments (param : value) passed to the method. The value doesn't
#                 always correspond to the actual argument so that functionality can be abstracted
#                 from specific machine learning libraries. Check variable_map.json for all values
#                 and their representations.

#             Example usage:

#             args = {
#                     "map_func" : "normalize_img",
#                     "num_parallel_calls" : "autotune"
#                     }

#             pipeline.add_operation("map", args)
#         '''

#         operation = {
#             "name": op_name,
#             "args": args
#         }
#         self.add_entry("operations", operation)
