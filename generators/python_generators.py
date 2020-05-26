''' Defines classes that generate Python scripts based off JSON files.

The purpose of these classes is to generate a class-based Python script based off parameters
set by a user stored in a JSON file. The layout is as follows:

Classes:
    PythonGenerator: Base class with writing methods.
    ClassGenerator: Adds in generic class formatting for code generation.
    PipelineGenerator: Generates a dataset pipeline object script.
    ModelGenerator: Generates a machine learning model object script.
'''
import json
import os
from abc import abstractmethod
import warnings
import numpy as np
import pdb


class PythonGenerator(object):
    '''Generates a Python script and writes code to it.

    This class is not very useful by itself. It can be used to write to a python file and
    keep track of indent levels.
    '''

    def __init__(self, out):

        self.out_file_name = out
        self.out = open(self.out_file_name, "w+")  # Code is written to this file

        self.indent_level = 0  # Keeps track of current indentation
        self.indent_str = "    "  # Standard 4-space indents

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

        Args:
            lines: A string or list of strings.

        Example usage:

            _write("This is a line.\n")
            _write(["This is line 1\n",
                    "This is line 2\n"])
        '''
        try:
            self.out.write(self._spaces() + lines) if isinstance(lines, str) \
                else [(self.out.write(self._spaces() + line)) for line in lines]
        except TypeError:
            warnings.warn("Nothing written - lines arg must be type str or List[str]", UserWarning)

    def _write_docstring(self, line=None):
        ''' Writes a line of docstring to the file.

        Args:
            line: Docstring comment without docstring quotes. Defaults to None and does nothing.
        '''
        if isinstance(line, list):
            self._write("'''" + line[0] + "\n")
            self._write(line[1:])
            self._write("'''\n\n")
        elif isinstance(line, str):
            self._write("'''" + line)
            self._write("'''\n\n")

    def _close(self):
        self.out.close()

    def get_gen_file_name(self):
        '''Returns the name of the generated Python script.
        '''

        return self.out_file_name


class ClassGenerator(PythonGenerator):
    ''' Abstract class that defines methods for writing object-oriented strings to a python file.
    '''

    def __init__(self, class_config, map_config, out):

        self._check_configs(class_config, map_config)

        super(ClassGenerator, self).__init__(out)

        # Load config files
        config_file = open(class_config)  # JSON defining the class
        mapping_file = open(map_config)  # JSON defining terms specific to the interpreting language
        self.class_ = json.load(config_file)
        self.map = json.load(mapping_file)["map"]

    # TODO: Would be nice if this also checked for json file structure being valid.
    def _check_configs(self, class_config, map_config):
        '''Check that the config files exist.
        '''
        if not os.path.exists(class_config):
            raise FileNotFoundError("ERROR: Cannot find class config file.")
        if not os.path.exists(map_config):
            raise FileNotFoundError("ERROR : Cannot find map config file.")

    def _write_imports(self, imports_dict):
        '''Write import statements to file.

        Args:
            import_dict: A dictionary of strings containing the import packages and their
            abbreviations.

        Example usage:

        imports_dict = {
            "tensorflow" : "tf",
            "numpy" : "np"
        }
        _write_imports(imports_dict)
        '''
        if not isinstance(imports_dict, dict):
            raise TypeError("imports_dict must be a dictionary.")

        self._write("# Imports\n")

        for _import, _abbrev in imports_dict.items():
            self._write("import {import_} as {abbrev_}\n".format(import_=_import,
                                                                 abbrev_=_abbrev))
        self._write("\n\n")

    def _start_class(self, name, base="object", docstring=None):
        '''Write the class definition to file.

        Defines the class and writes docstring to file.

        Args:
            name : A string of the class name.
            base : A string of the base class. Default is "object".
            docstring : A string to be written as a docstring. Default is None.

        '''
        self._write("class {name}({base}):\n".format(name=name, base=base))
        self._indent()
        self._write_docstring(docstring)

    def _end_class(self):
        ''' Signify end of class and remove indents.
        '''
        self._unindent()

    def _end_method(self):
        '''Signify end of method and remove indents.
        '''

        self._write("\n\n")
        self._unindent()

    @abstractmethod
    def _imports(self):
        ''' Write imports to file.
        '''
        pass

    @abstractmethod
    def _class_def(self):
        ''' Define a class.

        This method should call _start_class() and should include an __init__ method.
        '''
        pass

    def _is_valid_arg_dict(self, arg_dict):
        ''' Check if arguments are formatted correctly in the dictionary.

        The argument dict must follow the convention of Python function arguments. Args with
        default parameters must come after args without. All keys must be of type string. 
        Values may take the forms:
             string: To represent any object. Will be written without quotes.
             int/float: To represent a number value.
             list: A list input.
             None: This can be used to signify there is no default parameter. 

        This function raises exceptions if any of these rules are not followed.

        Args:
            arg_dict: A dict of method arguments in the form ("param" : "value"). param must be 
            string and value may be string or None. arg_dict can be None instead of dict
            if there are no args

        Raises:
            TypeError: Arguments must be formatted as a dictionary.
            ValueError: All None values must come before all string values.
            TypeError: All keys must be strings and all values must be strings or None.
        '''
        # Args must be in a dict
        if arg_dict:
            if not isinstance(arg_dict, dict):
                raise TypeError("Arguments must be formatted as a dictionary.")

            def allowed_val_type(v):
                return (isinstance(v, str) or
                        isinstance(v, int) or
                        isinstance(v, float) or
                        isinstance(v, list) or
                        v is None)

            # Check that all keys are strings and all vals are string, int or None
            all_str_keys = [isinstance(k, str) for k in arg_dict.keys()]
            all_str_vals = [allowed_val_type(v) for v in arg_dict.values()]

            # Check for default parameters before args w/o default parameters
            bad_arg_order = False
            default_param = False
            for val in arg_dict.values():
                if val and not default_param:
                    default_param = True
                elif not val and default_param:
                    bad_arg_order = True

            if bad_arg_order:
                raise ValueError("All None values must come before all string values.")
            if not np.all(all_str_keys) or not np.all(all_str_vals):
                raise TypeError("All keys must be strings and all values must be strings, \
                    int, float, or None.")

    def _is_valid_fn_dict(self, fn_dict):
        ''' Check if function is formatted correctly in a dictionary.

        The function dictionary must be correctly formatted so it can be parsed. It must have two 
        keys: "name" and "args". The value of "name" must be a string, and args must be formatted
        as an arg_dict (see _is_valid_arg_dict for that format). Any input deviating from this will
        raise an exception.

        Args:
            fn_dict: A dict containing function details.

        Raises:
            TypeError: Input must be of type dict.
            ValueError: Must have a "name" key in the dict.
            ValueError: Must have an "args" key in the dict.
            ValueError: The only keys must be "name' and "args".
            TypeError: Function name must be a string. 
        '''
        if not isinstance(fn_dict, dict):
            raise TypeError("fn_dict must be of type dict.")

        if "name" not in fn_dict:
            raise ValueError("Must have a \"name\" key in the dict.")

        if "args" not in fn_dict:
            raise ValueError("Must have an \"args\" key in the dict.")

        for param in fn_dict.keys():
            if param != "name" and param != "args":
                raise ValueError("The only keys must be \"name\" and \"args\".")

        if not isinstance(fn_dict["name"], str):
            raise TypeError("Function name must be a string.")

        self._is_valid_arg_dict(fn_dict["args"])

    def _arg_str(self, arg_dict):
        ''' Converts function arguments to a string.

        Args:
            arg_dict : A dict of arguments. Can be None if there are no args.

        Returns:
            A string of the concatenated arguments.

        Example usage:

            arg_dict = {
                "param_1" : None,
                "param_2" : "val_2"
            }
            _arg_str(arg_dict) ; 'param_1, param_2=val_2'
        '''
        # Raise an error if arg dict incorrectly formatted
        self._is_valid_arg_dict(arg_dict)

        if not arg_dict:
            return ""

        arg_str = []
        for param, val in arg_dict.items():
            arg_str.append("{param}={val}".format(param=param, val=val) if val
                           else "{param}".format(param=param))

        return ", ".join(arg_str)

    def _fn_str(self, fn_dict):
        ''' Convert a function from dictionary form to a string.

        Args:
            fn_dict : A dict representing a function.

        Example usage:

            fn_dict = {
                "name" : "function",
                "args" : {
                    "param" : "val"
                }
            }
            _fn_str(fn_dict) ; 'function(param=val)
        '''
        # Raise an exception if formatted incorrectly
        self._is_valid_fn_dict(fn_dict)

        return "{fn_name}({args})".format(fn_name=fn_dict["name"],
                                          args=self._arg_str(fn_dict["args"]))

    def _map(self, input_):
        ''' Converts an input to its language-specific representation.

        This function allows the model JSON language to be independent of implementation syntax.
        For example, the model may have a "dense" layer. The Tensorflow code for this is
        tf.keras.layers.Dense(). This function returns that language-specific syntax.

        Args:
            input : A string representing the term to be mapped.
        '''

        # Return the mapped output in quotations if it is of type string
        if isinstance(input_, str) and input_ in self.map:
            return self.map[input_]["name"] if self.map[input_]["type"] != "string" \
                else "\"{}\"".format(self.map[input_]["name"])

        return input_  # Input not in the map

    def _map_fn(self, function):
        ''' Convert the elements of a function dictionary to their real values.

        Args:
            function : A dict representing a function

        Returns:
            A mapped dictionary of the same form as the input.

        Example usage:

            function = {
                "name" : "function"
                "args" : {
                    "param" : "value"
                }
            }
            _map_fn(function)
        '''

        # Create mapped function dict and add name
        mapped_fn = {
            "name": self._map(function["name"]),
            "args": {}
        }

        # Map function args; recursively if an arg is a function dict
        for _param, _value in function["args"].items():
            mapped_fn["args"][self._map(_param)] = self._fn_str(self._map_fn(
                _value)) if isinstance(_value, dict) else self._map(_value)

        return mapped_fn

    def _fn(self, fn_dict):
        ''' Maps a function dictionary and returns it as a string.

        Args:
            fn_dict : A dict representing a function.

        Returns:
            A mapped dictionary of the same form as the input.

        Example usage:

            fn_dict = {
                "name" : "function",
                "args" : {
                    "param" : "value"
                }
            }
            _fn(fn_dict) ; 'mapped_function(mapped_param=mapped_value)
        '''
        return self._fn_str(self._map_fn(fn_dict))

    def _start_method(self, name, args=None, docstring=None):
        '''Writes the method definition to file.

        Args:
            name : A string of the method name.
            args : A dict of args passed to the method. Default to None
            docstring : A string to be written as a docstring. Default to None.
        '''
        # _args = ", ".join([arg for arg in args]) if args else ""
        self._write("def {name}({args}):\n".format(name=name,
                                                   args=self._arg_str(args)))
        self._indent()
        self._write_docstring(docstring)

    def _start_class_method(self, name, arg_dict=None, docstring=None):
        '''Writes a class method definition to file.

        Args:
            name : A string of the method name.
            args : A dict of args passed to the method. Don't include "self". Default to None
            docstring : A string to be written as a docstring. Default to None.
        '''
        self._is_valid_arg_dict(arg_dict)
        args = {
            "self" : None,
        }
        if arg_dict : args.update(arg_dict)

        self._start_method(name, args, docstring)


class PipelineGenerator(ClassGenerator):
    '''Generates a dataset preprocessing pipeline based off a JSON config file.
    '''

    def __init__(self, pipeline_config="generators/pipeline.json",
                 map_config="generators/pipeline_map.json",
                 out="project/pipeline.py"):

        super(PipelineGenerator, self).__init__(class_config=pipeline_config,
                                                map_config=map_config,
                                                out=out)

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
        self._start_class_method(name="__init__")

        self._write([
            "(self.ds_train, self.ds_test), self.ds_info = self.load_dataset()\n\n",
            "self.preprocess()\n"
        ])

        self._end_method()

    def _load_dataset(self):
        '''Generate code for loading the dataset.
        '''

        self._start_class_method(name="load_dataset",
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

        self._start_class_method(name="preprocess",
                                 docstring="Apply data preprocessing operations.\n")

        [self._write("self.ds_train = self.ds_train.{op}\n".format(op=self._fn(_op)))
         for _op in self.pipeline["operations"]]

        self._end_method()

    def _helper_funcs(self):
        ''' Generates get/set helper functions.
        '''

        # def get_training_dataset()
        self._start_class_method(name="get_training_dataset",
                                 docstring="Returns the training dataset.\n")
        self._write("return self.ds_train\n")
        self._end_method()

        # def get_test_dataset()
        self._start_class_method(name="get_test_dataset",
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
                 model_config="generators/model.json",
                 map_config="generators/model_variable_map.json",
                 out="project/model.py"):

        super(ModelGenerator, self).__init__(class_config=model_config,
                                             map_config=map_config,
                                             out=out)

        self.model = self.class_["model"]  # Root of the json file
        self.model_name = self._map(self.model["model"]["name"])  # Model type

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
        self._start_class_method(name="__init__",
                                 args={
                                     "dataset" : None
                                 })

        self._write([
            "self.ds = dataset\n",
            "self.build()\n",
            "self.compile()\n\n"
        ])
        self._end_method()

    def _build_model(self):
        '''Generate code for building the model.
        '''

        self._start_class_method(name="build",
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

        self._start_class_method(name="compile",
                                 docstring="Compile the MNIST model.\n")

        compile_fn = self._fn(self.model["compile"])  # Map compile settings to function
        self._write("self.model.{fn}".format(fn=compile_fn))

        self._end_method()

    def _train(self):
        ''' Generate code to train the model.
        '''

        self._start_class_method(name="train",
                                 docstring="Train the model.\n")
        self._write("self.model.fit(self.ds,epochs=5)\n\n")

        self._end_method()

    def _helper_funcs(self):
        ''' Generates get/set helper functions.
        '''
        pass  # None for now

    def gen_model(self):
        ''' Generate all code for the Model class.
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
