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

    def __indent(self, inc=1):
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

    def __write(self, line):
        ''' Writes a line of code to the file.
        '''

        self.out.write(self.__spaces() + line)

    def __write_docstring(self, line):
        ''' Writes a line of docstring to the file.
            line: Docstring comment without docstring quotes.
        '''

        self.out.write(self.__spaces() + "'''" + line)
        self.out.write(self.__spaces() + "'''\n\n")

    def __start_method(self):
        '''Formats out string to generate a method.
        '''

        self.__indent()

    def __end_method(self):
        '''Formats out string once method is done.
        '''

        self.__write("\n\n")
        self.__unindent(2)

    def __imports(self):
        ''' Generate import statements.
        '''

        self.__write("# Imports\n")
        self.__write("import os\n")
        self.__write("import sys\n")
        self.__write("sys.path.append(os.path.join(os.getcwd(), \"preprocessor\"))\n")
        self.__write("import tensorflow as tf\n")
        self.__write("import tensorflow_datasets as tfds\n")
        self.__write("import json\n")
        self.__write("from tf_utils import *\n")
        self.__write("\n\n")

    def __class_def(self):
        ''' Generate DatasetPipeline class definition.
        '''

        # DatasetPipeline class
        self.__write("class DatasetPipeline(object):\n")
        self.__indent()
        self.__write_docstring("Represents a dataset that has been preprocessed.\n")

        # Init
        self.__write("def __init__(self):\n\n")
        self.__indent()
        self.__write(
            "(self.ds_train, self.ds_test), self.ds_info = self.load_dataset()\n\n")
        self.__write("self.preprocess()\n")

        self.__end_method()

    def __load_dataset(self):
        '''Generate code for loading the dataset.
        '''

        self.__start_method()
        self.__write("def load_dataset(self):\n")
        self.__indent()
        self.__write_docstring("Load the dataset from Tensorflow Datasets.\n")

        # Load dataset from Tensorflow Datasets
        self.__write("return tfds.load(\'{ds}\',".format(ds=self.dataset) +
                     "split=['train', 'test']," +
                     "shuffle_files=True," +
                     "as_supervised=True," +
                     "with_info = True)\n")

        self.__end_method()

    def __map_variables(self, params):
        ''' Convert parameter value representations to their actual values.
            This is necessary to keep the pipeline config file independent of
            specific function names, i.e. tf2 function calls.
        '''

        for _param in enumerate(params):
            value = list(_param[1].values())[0]

            if value in self.variable_map:

                # Replace parameter code for its real value
                params[_param[0]][list(_param[1].keys())[0]] = self.variable_map[value]

        return params

    def __operations(self):
        ''' Generate code for all preprocessing operations.
        '''

        self.__start_method()
        self.__write("def preprocess(self):\n")
        self.__indent()
        self.__write_docstring("Apply data preprocessing operations.\n")

        for _op in self.ops:

            # Retrieve variables and map their values
            variables = self.__map_variables(list(_op.values())[0])

            # Define the Tensorflow function
            fn_str = 'self.ds_train = self.ds_train.{fn}'.format(fn=list(_op)[0])

            # Define the variables to the function
            param_str = ', '.join(["{param}={val}".format(param=list(param)[0],
                                                          val=list(param.values())[0])
                                   for param in variables])

            # Concatenate them all
            op_str = fn_str + '(' + param_str + ')\n'
            self.__write(op_str)

        self.__end_method()

    def __helper_funcs(self):
        ''' Generates get/set helper functions.
        '''

        # def get_training_dataset()
        self.__start_method()
        self.__write("def get_training_dataset(self):\n")
        self.__indent()
        self.__write_docstring("Returns the training dataset.\n")
        self.__write("return self.ds_train\n")

        self.__end_method()

        # def get_test_dataset()
        self.__start_method()
        self.__write("def get_test_dataset(self):\n")
        self.__indent()
        self.__write_docstring("Returns the test dataset.\n")
        self.__write("return self.ds_test\n")

        self.__end_method()

    def gen_pipeline(self):
        ''' Generate all code part of the dataset pipeline.
        '''

        self.__imports()
        self.__class_def()
        self.__load_dataset()
        self.__operations()
        self.__helper_funcs()

    def get_pipeline_file_name(self):
        '''Returns the name of the generated pipeline script.

        Currently the file name is not modifiable.
        '''

        return self.out


def main():
    '''Generate a dataset pipeline script.
    '''

    pipe_gen = PipelineGenerator(pipeline_config="preprocessor/pipeline.json",
                                 mapping_config="preprocessor/variable_map.json")
    pipe_gen.gen_pipeline()


if __name__ == "__main__":
    main()
