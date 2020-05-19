''' This script generates a dataset pipeline script based off a JSON config file.
 This config  file is generated from user inputs on the frontend. The generated script
 describes a DatasetPipeline object that can then be used for agnostic model training.
'''
import json
import os
import sys
sys.path.append(os.path.join(os.getcwd(), "preprocessor"))


class PipelineGenerator(object):
    '''Generates a dataset preprocessing pipeline based off a JSON config file.
    '''

    def __init__(self, pipeline_config="preprocessor/pipeline.json",
                 mapping_config="preprocessor/variable_map.json"):
        assert pipeline_config is not None

        # Load config files
        config_file = open(pipeline_config)  # JSON defining pipeline
        mapping_file = open(mapping_config)  # JSON defining parameter representations
        self.pipeline = json.load(config_file)["pipeline"]
        self.variable_map = json.load(mapping_file)["variable_map"]

        self.dataset = self.pipeline["dataset"]["label"]  # Label for dataset being used
        self.ops = self.pipeline["operations"]  # Preprocessing performed on the dataset

        self.out = open("preprocessor/pipeline.py", "w+")  # Code is generated to this file

        self.indent_level = 0  # Keeps track of current indentation
        self.indent_str = "    "

    def indent(self, inc=1):
        ''' Increments the indent level of the output string.
        '''

        self.indent_level += inc

    def unindent(self, dec=1):
        ''' Decrements the indent level of the output string.
        '''

        self.indent_level -= dec

    def spaces(self):
        '''Returns a string of the correct number of spaces for the current indent level.
        '''

        return self.indent_str * self.indent_level

    def write(self, line):
        ''' Writes a line of code to the file.
        '''

        self.out.write(self.spaces() + line)

    def write_docstring(self, line):
        ''' Writes a line of docstring to the file. 
            line: Docstring comment without docstring quotes.
        '''

        self.out.write(self.spaces() + "'''" + line)
        self.out.write(self.spaces() + "'''\n\n")

    def start_method(self):
        '''Formats out string to generate a method.
        '''

        self.indent()

    def end_method(self):
        '''Formats out string once method is done.
        '''

        self.write("\n\n")
        self.unindent(2)

    def imports(self):
        ''' Generate import statements.
        '''

        self.write("# Imports\n")
        self.write("import os\n")
        self.write("import sys\n")
        self.write("sys.path.append(os.path.join(os.getcwd(), \"preprocessor\"))\n")
        self.write("import tensorflow as tf\n")
        self.write("import tensorflow_datasets as tfds\n")
        self.write("import json\n")
        self.write("from tf_utils import *\n")
        self.write("\n\n")

    def class_def(self):
        ''' Generate DatasetPipeline class definition.
        '''

        # DatasetPipeline class
        self.write("class DatasetPipeline(object):\n")
        self.indent()
        self.write_docstring("Represents a dataset that has been preprocessed.\n")

        # Init
        self.write("def __init__(self):\n\n")
        self.indent()
        self.write(
            "(self.ds_train, self.ds_test), self.ds_info = self.load_dataset()\n\n")
        self.write("self.preprocess()\n")

        self.end_method()

    def load_dataset(self):
        '''Generate code for loading the dataset.
        '''

        self.start_method()
        self.write("def load_dataset(self):\n")
        self.indent()
        self.write_docstring("Load the dataset from Tensorflow Datasets.\n")

        # Load dataset from Tensorflow Datasets
        self.write("return tfds.load(\'{ds}\',".format(ds=self.dataset) +
                   "split=['train', 'test']," +
                   "shuffle_files=True," +
                   "as_supervised=True," +
                   "with_info = True)\n")

        self.end_method()

    def map_variables(self, params):
        ''' Convert parameter value representations to their actual values.
            This is necessary to keep the pipeline config file independent of 
            specific function names, i.e. tf2 function calls.
        '''

        for i in range(0, len(params)):
            _param = params[i]
            value = list(_param.values())[0]

            if value in self.variable_map:

                # Replace parameter code for its real value
                params[i][list(_param.keys())[0]] = self.variable_map[value]

        return params

    def operations(self):
        ''' Generate code for all preprocessing operations.
        '''

        self.start_method()
        self.write("def preprocess(self):\n")
        self.indent()
        self.write_docstring("Apply data preprocessing operations.\n")

        for _op in self.ops:

            # Retrieve variables and map their values
            variables = self.map_variables(list(_op.values())[0])

            # Define the Tensorflow function
            fn_str = 'self.ds_train = self.ds_train.{fn}'.format(fn=list(_op)[0])

            # Define the variables to the function
            param_str = ', '.join(["{param}={val}".format(param=list(param)[0],
                                                          val=list(param.values())[0])
                                   for param in variables])

            # Concatenate them all
            op_str = fn_str + '(' + param_str + ')\n'
            self.write(op_str)

        self.end_method()

    def helper_funcs(self):
        ''' Generates get/set helper functions.
        '''

        # def get_training_dataset()
        self.start_method()
        self.write("def get_training_dataset(self):\n")
        self.indent()
        self.write_docstring("Returns the training dataset.\n")
        self.write("return self.ds_train\n")

        self.end_method()

        # def get_test_dataset()
        self.start_method()
        self.write("def get_test_dataset(self):\n")
        self.indent()
        self.write_docstring("Returns the test dataset.\n")
        self.write("return self.ds_test\n")

        self.end_method()

    def gen_pipeline(self):
        ''' Generate all code part of the dataset pipeline.
        '''

        self.imports()
        self.class_def()
        self.load_dataset()
        self.operations()
        self.helper_funcs()


def main():
    '''Generate a dataset pipeline script.
    '''

    pipe_gen = PipelineGenerator(pipeline_config="preprocessor/pipeline.json",
                                 mapping_config="preprocessor/variable_map.json")
    pipe_gen.gen_pipeline()


if __name__ == "__main__":
    main()
