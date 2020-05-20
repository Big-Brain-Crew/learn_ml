''' This script generates a dataset pipeline script based off a JSON config file.
 This config  file is generated from user inputs on the frontend. The generated script
 describes a DatasetPipeline object that can then be used for agnostic model training.
'''
import json
from generators.base_generators import PythonGenerator, JsonGenerator


class PipelineGenerator(PythonGenerator):
    '''Generates a dataset preprocessing pipeline based off a JSON config file.
    '''

    def __init__(self, pipeline_config="generators/preprocessor/pipeline.json",
                 mapping_config="generators/preprocessor/variable_map.json"):
        assert pipeline_config is not None

        # Load config files
        config_file = open(pipeline_config)  # JSON defining pipeline
        mapping_file = open(mapping_config)  # JSON defining parameter representations
        self.pipeline = json.load(config_file)["pipeline"]
        self.variable_map = json.load(mapping_file)["variable_map"]

        self.dataset = self.pipeline["dataset"]["label"]  # Label for dataset being used
        self.ops = self.pipeline["operations"]  # Preprocessing performed on the dataset

        super(PipelineGenerator, self).__init__(out="generators/preprocessor/pipeline.py")

    def _indent(self, inc=1):
        ''' Increments the indent level of the output string.
        '''

        self.indent_level += inc

    def __unindent(self, dec=1):
        ''' Decrements the indent level of the output string.
        '''

        self.indent_level -= dec

    def __spaces(self):
        '''Returns a string of the correct number of spaces for the current indent level.
        '''

        return self.indent_str * self.indent_level

    def _write(self, line):
        ''' Writes a line of code to the file.
        '''

        self.out.write(self.__spaces() + line)

    def _write_docstring(self, line):
        ''' Writes a line of docstring to the file.
            line: Docstring comment without docstring quotes.
        '''

        self.out.write(self.__spaces() + "'''" + line)
        self.out.write(self.__spaces() + "'''\n\n")

    def _start_method(self):
        '''Formats out string to generate a method.
        '''

        self._indent()

    def _end_method(self):
        '''Formats out string once method is done.
        '''

        self._write("\n\n")
        self.__unindent(2)

    def _imports(self):
        ''' Generate import statements.
        '''

        self._write("# Imports\n")
        self._write("import os\n")
        self._write("import sys\n")
        self._write("sys.path.append(os.path.join(os.getcwd(), \"generators/preprocessor\"))\n")
        self._write("import tensorflow as tf\n")
        self._write("import tensorflow_datasets as tfds\n")
        self._write("import json\n")
        self._write("from tf_utils import *\n")
        self._write("\n\n")

    def _class_def(self):
        ''' Generate DatasetPipeline class definition.
        '''

        # DatasetPipeline class
        self._write("class DatasetPipeline(object):\n")
        self._indent()
        self._write_docstring("Represents a dataset that has been preprocessed.\n")

        # Init
        self._write("def __init__(self):\n\n")
        self._indent()
        self._write(
            "(self.ds_train, self.ds_test), self.ds_info = self.load_dataset()\n\n")
        self._write("self.preprocess()\n")

        self._end_method()

    def _load_dataset(self):
        '''Generate code for loading the dataset.
        '''

        self._start_method()
        self._write("def load_dataset(self):\n")
        self._indent()
        self._write_docstring("Load the dataset from Tensorflow Datasets.\n")

        # Load dataset from Tensorflow Datasets
        self._write("return tfds.load(\'{ds}\',".format(ds=self.dataset) +
                     "split=['train', 'test']," +
                     "shuffle_files=True," +
                     "as_supervised=True," +
                     "with_info = True)\n")

        self._end_method()

    def __map_variables(self, params):
        ''' Convert parameter value representations to their actual values.
            This is necessary to keep the pipeline config file independent of
            specific function names, i.e. tf2 function calls.
        '''

        # Create a new dictionary to store the new mapped params
        mapped_params = {}

        for _param, value in params.items():
            if value in self.variable_map:
                # Replace parameter code for its real value
                mapped_params[_param] = self.variable_map[value]
            else:
                mapped_params[_param] = value

        return mapped_params

    def _operations(self):
        ''' Generate code for all preprocessing operations.
        '''

        self._start_method()
        self._write("def preprocess(self):\n")
        self._indent()
        self._write_docstring("Apply data preprocessing operations.\n")

        for _op in self.ops:

            # Retrieve variables and map their values
            variables = self.__map_variables(_op["args"])

            # Define the Tensorflow function
            fn_str = 'self.ds_train = self.ds_train.{fn}'.format(fn=_op["name"])

            # Define the variables to the function
            param_str = ', '.join(["{param}={val}".format(param=param, val=val)
                                   for param, val in variables.items()])

            # Concatenate them all
            op_str = fn_str + '(' + param_str + ')\n'
            self._write(op_str)

        self._end_method()

    def _helper_funcs(self):
        ''' Generates get/set helper functions.
        '''

        # def get_training_dataset()
        self._start_method()
        self._write("def get_training_dataset(self):\n")
        self._indent()
        self._write_docstring("Returns the training dataset.\n")
        self._write("return self.ds_train\n")

        self._end_method()

        # def get_test_dataset()
        self._start_method()
        self._write("def get_test_dataset(self):\n")
        self._indent()
        self._write_docstring("Returns the test dataset.\n")
        self._write("return self.ds_test\n")

        self._end_method()

    def gen_pipeline(self):
        ''' Generate all code part of the dataset pipeline.
        '''

        self._imports()
        self._class_def()
        self._load_dataset()
        self._operations()
        self._helper_funcs()

        print("Saved to {}".format(self.out_file_name))

    def get_pipeline_file_name(self):
        '''Returns the name of the generated pipeline script.

        Currently the file name is not modifiable.
        '''

        return self.out


class PipelineConfigGenerator(JsonGenerator):
    ''' Generates a pipeline config JSON file based on user selections.

    Generates a config file that describes a dataset preprocessing pipeline
    based off a user's selection of dataset source and preprocessing operations.
    '''

    def __init__(self, out_file):

        super(PipelineConfigGenerator, self).__init__(out_file)

        # Add the root dict
        self.add_entry("pipeline", {})

        # Add the dataset and operations 
        self.indent("pipeline")
        self.add_entry("dataset", {})
        self.add_entry("operations", [])

    def add_dataset(self, label):
        ''' Add a dataset source. 

        All available datasets can be found in the Tensorflow Datasets catalog.
            (https://www.tensorflow.org/datasets/catalog/overview)

        Args:
            label : dataset identifier. Equivalent to the Tensorflow dataset name.
        '''

        self.add_entry("dataset", {"label" : label})

    def add_operation(self, op_name, args={}):
        ''' Add a preprocessing operation.

        A list of all allowable operations can be found as methods for the tf.data.Dataset class
            (https://www.tensorflow.org/api_docs/python/tf/data/Dataset)

        Args:
            op_name : Name of the operation. Equivalent to a tf.Dataset method name.
            args : Dictionary of arguments (param : value) passed to the method. The value doesn't 
                always correspond to the actual argument so that functionality can be abstracted 
                from specific machine learning libraries. Check variable_map.json for all values 
                and their representations.

            Example usage:

            args = {
                    "map_func" : "normalize_img",
                    "num_parallel_calls" : "autotune"
                    }

            pipeline.add_operation("map", args)
        '''

        operation = {
            "name" : op_name,
            "args" : args
        }
        self.add_entry("operations", operation)
    