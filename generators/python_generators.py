''' This script defines a base Python code generator.

Strings can be written to a file and formatted with indentations and docstrings.
'''
import json
import os
import sys
from abc import abstractmethod


class PythonGenerator(object):
    '''Generates a Python script and writes code to it.
    '''

    def __init__(self, out):

        self.out_file_name = out
        self.out = open(self.out_file_name, "w+")  # Code written to this file

        self.indent_level = 0  # Keeps track of current indentation
        self.indent_str = "    "

    def _indent(self, inc=1):
        ''' Increments the indent level of the output string.
        '''

        self.indent_level += inc

    def _unindent(self, dec=1):
        ''' Decrements the indent level of the output string.
        '''

        self.indent_level -= dec

    def _spaces(self):
        '''Returns a string of the correct number of spaces for the current indent level.
        '''

        return self.indent_str * self.indent_level

    def _write(self, lines):
        ''' Writes lines of code to the file.
        '''

        self.out.write(self._spaces() + lines) if isinstance(lines, str) \
            else [(self.out.write(self._spaces() + line)) for line in lines]

    def _write_docstring(self, line):
        ''' Writes a line of docstring to the file.
            line: Docstring comment without docstring quotes.
        '''

        self.out.write(self._spaces() + "'''" + line)
        self.out.write(self._spaces() + "'''\n\n")

    def _close(self):
        self.out.close()

    def get_gen_file_name(self):
        '''Returns the name of the generated Python script.

        Currently the file name is not modifiable.
        '''

        return self.out


class ClassGenerator(PythonGenerator):
    ''' Blah.
    '''

    def __init__(self, class_config, map_config, out):

        super(ClassGenerator, self).__init__(out)

        # Load config files
        config_file = open(class_config)  # JSON defining the model
        mapping_file = open(map_config)  # JSON defining values specific to program language
        self.class_ = json.load(config_file)
        self.map = json.load(mapping_file)["map"]

    def _write_imports(self, imports_dict):
        self._write("# Imports\n")

        for _import, _abbrev in imports_dict.items():
            self._write("import {import_} as {abbrev_}\n".format(import_=_import,
                                                                 abbrev_=_abbrev))
        self._write("\n\n")

    def _start_class(self, name, base, docstring):
        self._write("class {name}({base}):\n".format(name=name, base=base))
        self._indent()
        self._write_docstring(docstring)

    def _start_method(self, name="", args={}, docstring=None):
        '''Formats out string to generate a method.
        '''
        _args = ", ".join([arg for arg in args])
        self._write("def {name}({args}):\n".format(name=name,
                                                   args=_args))
        self._indent()
        self._write_docstring(docstring) if docstring is not None else {}

    def _end_class(self):
        self._unindent()

    def _end_method(self):
        '''Formats out string once method is done.
        '''

        self._write("\n\n")
        self._unindent()

    @abstractmethod
    def _imports(self):
        pass

    @abstractmethod
    def _class_def(self):
        pass

    def _map(self, input):
        ''' Converts an input to its language-specific representation.

        This function allows the model JSON language to be independent of implementation syntax.
        For example, the model may have a dense layer. The Tensorflow code for this is 
        tf.keras.layers.Dense(). This input retrieves that language-specific syntax.
        '''

        # Return the mapped output in quotations if it is of type string
        if isinstance(input, str) and input in self.map:
            return self.map[input]["name"] if self.map[input]["type"] is not "string" \
                else "\"{}\"".format(self.map[input]["name"])
        
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
            mapped_fn["args"][self._map(_param)] = self._fn_str(self._map_fn(
                _value)) if isinstance(_value, dict) else self._map(_value)

        return mapped_fn

    def _arg_str(self, arg_dict):
        return ', '.join(["{param}={val}".format(param=param, val=val)
                          for param, val in arg_dict.items()])

    def _fn_str(self, fn_dict):
        ''' Convert a function in dictionary form to a string.
        '''
        return "{fn_name}({args})".format(fn_name=fn_dict["name"],
                                          args=self._arg_str(fn_dict["args"]))

    def _fn(self, fn_dict):
        return self._fn_str(self._map_fn(fn_dict))


class PipelineGenerator(ClassGenerator):
    '''Generates a dataset preprocessing pipeline based off a JSON config file.
    '''

    def __init__(self, pipeline_config="generators/preprocessor/pipeline.json",
                 map_config="generators/preprocessor/pipeline_map.json"):

        assert pipeline_config is not None
        assert map_config is not None

        super(PipelineGenerator, self).__init__(class_config=pipeline_config,
                                                map_config=map_config,
                                                out="project/pipeline.py")

        self.pipeline = self.class_["pipeline"]
        self.dataset = self.pipeline["dataset"]["label"]  # Label for dataset being used

    def _imports(self):
        ''' Generate import statements.
        '''
        imports = {
            "tensorflow": "tf",
            "tensorflow_datasets": "tfds",
            "tf_utils": "tf_utils"
        }
        self._write_imports(imports)

    def _class_def(self):
        ''' Generate DatasetPipeline class definition.
        '''

        self._start_class(name="DatasetPipeline",
                          base="object",
                          docstring="Represents a dataset that has been preprocessed.\n")

        # Init
        self._start_method(name="__init__",
                           args=["self"])

        self._write([
            "(self.ds_train, self.ds_test), self.ds_info = self.load_dataset()\n\n",
            "self.preprocess()\n"
        ])

        self._end_method()

    def _load_dataset(self):
        '''Generate code for loading the dataset.
        '''

        self._start_method(name="load_dataset",
                           args=["self"],
                           docstring="Load the dataset from Tensorflow Datasets.\n")

        # Load dataset from Tensorflow Datasets
        self._write("return tfds.load(\'{ds}\',".format(ds=self.dataset) +
                    "split=['train', 'test']," +
                    "shuffle_files=True," +
                    "as_supervised=True," +
                    "with_info = True)\n")

        self._end_method()

    def _operations(self):
        ''' Generate code for all preprocessing operations.
        '''

        self._start_method(name="preprocess",
                           args=["self"],
                           docstring="Apply data preprocessing operations.\n")

        for _op in self.pipeline["operations"]:

            _op = self._fn(_op)
            self._write("self.ds_train = self.ds_train.{op}\n".format(op=_op))

        self._end_method()

    def _helper_funcs(self):
        ''' Generates get/set helper functions.
        '''

        # def get_training_dataset()
        self._start_method(name="get_training_dataset",
                           args=["self"],
                           docstring="Returns the training dataset.\n")
        self._write("return self.ds_train\n")
        self._end_method()

        # def get_test_dataset()
        self._start_method(name="get_test_dataset",
                           args=["self"],
                           docstring="Returns the test dataset.\n")
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
        self._end_class()
        self._close()

        print("Saved to {}".format(self.out_file_name))


class ModelGenerator(ClassGenerator):
    '''Generates a machine learning model based off a JSON config file.
    '''

    def __init__(self,
                 model_config="generators/model/model.json",
                 map_config="generators/model/model_variable_map.json"):

        assert model_config is not None

        super(ModelGenerator, self).__init__(class_config=model_config,
                                             map_config=map_config,
                                             out="project/model.py")

        self.model = self.class_["model"]
        # Label for dataset being used
        self.model_name = self._map(self.model["model"]["name"])

    def _imports(self):
        ''' Generate import statements.
        '''

        imports = {
            "tensorflow": "tf",
            "tf_utils": "tf_utils"
        }

        self._write_imports(imports)

    def _class_def(self):
        ''' Generate Model class definition.
        '''

        # DatasetPipeline class
        self._start_class(name="Model",
                          base="object",
                          docstring="Represents a Tensorflow Model.\n")

        # Init
        self._start_method(name="__init__",
                           args=["self", "dataset"])

        self._write([
            "self.ds = dataset\n",
            "self.build()\n",
            "self.compile()\n\n"
        ])
        self._end_method()

    def _build_model(self):
        '''Generate code for building the model.
        '''

        self._start_method(name="build",
                           args=["self"],
                           docstring="Build the MNIST model.\n")

        self._write("self.model = {model}([\n".format(model=self.model_name))
        self._indent()

        [self._write(self._fn(_layer) + ",\n") for _layer in self.model["layers"]]

        self._unindent()
        self._write("])\n")
        self._end_method()

    def _compile_model(self):
        '''Generate code for the model compiler.
        '''

        self._start_method(name="compile",
                           args=["self"],
                           docstring="Compile the MNIST model.\n")

        compile_fn = self._fn(self.model["compile"])
        self._write("self.model.{fn}".format(fn=compile_fn))

        self._end_method()

    def _train(self):
        ''' Generate code to train the model.
        '''

        self._start_method(name="train",
                           args=["self"],
                           docstring="Train the model.\n")
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
        self._end_class()
        self._close()

        print("Saved to {}".format(self.out_file_name))

