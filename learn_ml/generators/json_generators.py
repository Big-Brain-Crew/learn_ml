''' Contains classes for generating pipeline and model configuration files.

These classes are used by the front-end application to define a dataset pipeline and
machine learning model in the form of a JSON file. Options are stored in about the same format
as they would be selected by the user. After these JSONs are generated, the actual
DatasetPipeline and Model classes can be generated based on the JSONs.

Classes::
    JsonGenerator: Base class for writing to a JSON.
    PipelineJsonGenerator: Writes JSON entries specific to the Pipeline class.
    ModelJsonGenerator: Writes JSON entries specific to the Model class.

'''

import json
import warnings
import pdb
import learn_ml.generators.generator_utils as generator_utils

class JsonGenerator(object):
    ''' Base class that adds content to a JSON file.
    
    Attributes:
        out_file (str): The file to write to.
        out: The file object that performs write operations.
        root (dict): Stores all the data before writing.
        index (dict): Keeps track of the current indentation in the root dict.

    '''

    def __init__(self, out_file):

        self.out_file = out_file
        self.out = open(self.out_file, "w+")

        self.root = {}
        self.index = self.root

    def _close(self):
        ''' Close the file object.'''

        self.out.close()

    def _indent(self, key):
        '''Set the entry point for writing to the JSON.

        After indenting, new entries will be added to this indented level. Indents can only be set 
        to dictionaries. Will raise a warning if trying to indent to anything else.

        Args:
            name (str): Dictionary key in the JSON. If the key does not already exist in the JSON,
                then it is added with an empty dictionary value.

        '''

        if key not in self.index:
            self.index[key] = {}
            self.index = self.index[key]
        elif not isinstance(self.index[key], dict):
            warnings.warn("Cannot be indented any further", UserWarning)
        else:
            self.index = self.index[key]

    def _unindent(self, key=None):
        ''' Sets the entry point back to the root of the JSON file.'''
        
        self.index = self.root
        if key:
            self.index = self.root[key]

    def add_entry(self, key, value):
        ''' Adds a key-value entry to the file.

        The entry is added at the current indent level. If the entry is being added to a key
        that already exists in the JSON, then it will overwrite the current value. If the existing
        key has a list as its value, then the entry is appended to the end of the list.

        Args:
            key (str): Dictionary key to add to the file.
            value : Dictionary value to add to the file. Can be of any type allowed in Python
                dictionaries.

        '''

        if key in self.index and isinstance(self.index[key], list):
            self.index[key].append(value)
        else:
            self.index[key] = value

    def add_fn(self, key, fn_name, args=None):
        ''' Adds a function to the file.

        A function is defined as a dictionary with "name" and "args" keys. The name is a string
        and the args is a dictionary.

        Args:
            key (str): Key value in the JSON file.
            fn_name (str): Function name
            args (dict): Function arguments as a dictionary.

        Example usage:
            >>> json_gen = JsonGenerator("out.json")
            >>> args = {
            >>>     "parameter_1" : "value_1",
            >>>     "parameter_2" : [28, 28, 1]
            >>> }
            >>> json_gen.add_fn("key", "function", args)
            >>> print(json_gen.root)
            {
                "key" : {
                    "name" : "function",
                    "args" : {
                        "parameter_1" : "value_1",
                        "parameter_2" : [28, 28, 1]
                    }
                }
            }

        '''

        # Raise exceptions if args incorrectly formatted
        generator_utils._is_valid_arg_dict(args)

        _fn = {
            "name": fn_name,
            "args": args
        }
        self.add_entry(key, _fn)

    def write(self):
        ''' Writes the root dictionary to the JSON file and closes the file.'''

        json.dump(self.root, self.out, indent=4)
        self._close()
        print("Saved to {}".format(self.out_file))


class PipelineJsonGenerator(JsonGenerator):
    ''' Generates a dataset pipeline configuration file based on user selections.'''

    def __init__(self, out_file):
        ''' Set up json dict format.

        The root is set to a "pipeline" key. Two keys are then created within the root.
        The "dataset" key contains info about the dataset source and format. 
        The "operations" key stores an ordered list of the preprocessing operations to 
        perform on the dataset.

        '''

        super(PipelineJsonGenerator, self).__init__(out_file)

        # Add the root dict
        self.add_entry("pipeline", {})

        # Add the dataset and operations
        self._indent("pipeline")
        self.add_entry("dataset", {})
        self.add_entry("operations", {})
        self._indent("operations")
        self.add_entry("train", [])
        self.add_entry("test", [])
        self._unindent("pipeline")

    def add_dataset(self, label):
        ''' Add a dataset source.

        All available datasets can be found in the Tensorflow Datasets catalog.
            (https://www.tensorflow.org/datasets/catalog/overview)

        Args:
            label (str): Dataset identifier. Equivalent to the Tensorflow dataset name.

        '''

        self.add_entry("dataset", {"label": label})

    def _add_operation(self, key, op_name, args=None):
        ''' Add a preprocessing operation.

        A list of all allowable operations can be found as methods for the tf.data.Dataset class
            (https://www.tensorflow.org/api_docs/python/tf/data/Dataset)

        Args:
            op_name (str): Name of the operation. Equivalent to a tf.Dataset method name.
            args (dict): The method arguments {"param" : "value"}. The value doesn't always 
                correspond to the actual argument so that functionality can be abstracted from
                specific machine learning libraries. Check variable_map.json for all values
                and their representations.

            Example usage:
                >>> pipeline = PipelineJsonGenerator("out.json")
                >>> args = {
                >>>         "map_func" : "normalize_img",
                >>>         "num_parallel_calls" : "autotune"
                >>>         }
                >>> pipeline.add_operation("map", args)
                >>> print(pipeline.root["operations"])
                [
                    {
                        "name" : "map",
                        "args" : {
                            "map_fun" : "normalize_img",
                            "num_parallel_calls" : "autotune"
                        }
                    }
                ]

        '''
        self._indent("operations")
        self.add_fn(key, op_name, args)
        self._unindent("pipeline")

    def add_train_operation(self, op_name, args=None):
        ''' Add an operation to the training dataset.'''

        self._add_operation("train", op_name, args)

    def add_test_operation(self, op_name, args=None):
        ''' Add an operation to the test dataset.'''
        
        self._add_operation("test", op_name, args)

    def get_dataset_list(self):
        '''Return a list of all possible dataset sources.'''

        pass

    def get_operations_list(self):
        ''' Return a list of all possible preprocessing operations.'''

        pass


class ModelJsonGenerator(JsonGenerator):
    ''' Generates a configuration file representing a machine learning model.'''

    def __init__(self, out_file):
        ''' Creates the json file format.

        The root is set to a "model" key. The root has three subkeys, "model", "layers", and
        "compile". The sub "model" key contains information on the model name and format.
        The "layers" key is an ordered list of all layers in the model. Each layer is formatted
        as a function dictionary. The "compile" key contains the arguments passed in to the 
        compile() method. 

        '''

        super(ModelJsonGenerator, self).__init__(out_file)

        # Add the root dict
        self.add_entry("model", {})

        # Add the model, layers, and compile sections
        self._indent("model")
        self.add_entry("model", {})
        self.add_entry("layers", [])
        self.add_entry("compile", {})

    def add_model(self, model_name):
        ''' Adds a model type to the file.

        Args:
            model_name (str): Model name. Refer to model_options.json for possible model names.

        '''

        self.add_entry("model", {"name": model_name})

    def add_layer(self, layer_name, args=None):
        '''Adds a neural net layer to the file.

        Args:
            layer_name (str): Layer name. Refer to the model_options.json for possible layer names.
            args (dict): Args {param : value} to pass into the layer function.

        Example usage:
            >>> model = ModelJsonGenerator("out.json")
            >>> args={
            >>>     "units" : 10,
            >>>     "activation" : "softmax"
            >>> }
            >>> add_layer("dense", args)
            >>> print(model.root["layers"])
            [
                {
                    "name" : "dense",
                    "args" : {
                        "units" : 10,
                        "activation" : "softmax"
                    }
                }
            ]

        '''

        self.add_fn("layers", layer_name, args)

    def add_compile(self, args=None):
        '''Adds compiler options to the file.

        Refer to model_options.json for all compiler arg options.

        Args:
            args (dict): Arguments passed into the compile function.
        '''

        self.add_fn("compile", "compile", args)

    def get_model_list(self):
        ''' Get the list of all possible model types.'''

        pass

    def get_layers_list(self):
        ''' Get the list of all possible layer functions.'''

        pass

    def get_compile_list(self):
        ''' Get the list of all possible compile arguments.'''
        
        pass
