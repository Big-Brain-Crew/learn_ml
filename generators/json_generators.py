''' Contains classes for generating pipeline and model configuration files.

These classes are used by the front-end application to define a dataset pipeline and
machine learning model in the form of a JSON file. Options are stored in about the same format
as they would be selected by the user. After these JSONs are generated, the actual
DatasetPipeline and Model classes can be generated based on the JSONs.
'''
import json


class JsonGenerator(object):
    ''' Base class that adds content to a JSON file.
    '''

    def __init__(self, out_file):

        self.out_file = out_file
        self.out = open(self.out_file, "w+")

        self.root = {}  # This will store all info before writing to JSON
        self.index = self.root  # Keep track of entry place in JSON dict

    def _close(self):
        ''' Close the file object.
        '''
        self.out.close()

    def _indent(self, key):
        '''Set the entry point for writing to the JSON.

        After indenting, new entries will be added to this indented level.

        Args:
            name : Dictionary key in the JSON. If the key does not already exist in the JSON,
            then it is added with an empty dictionary value.
        '''
        if key not in self.root:
            self.root[key] = {}
        self.index = self.root[key]

    def _unindent(self):
        ''' Sets the entry point back to the root of the JSON file.
        '''
        self.index = self.root

    def add_entry(self, key, value):
        ''' Adds a key-value entry to the file.

        The entry is added at the current indent level. If the entry is being added to a key
        that already exists in the JSON, then it will overwrite the current value. If the existing
        key has a list as its value, then the entry is appended to the end of the list.

        Args:
            key : Dictionary key to add to the file.
            value : Dictionary value to add to the file.
        '''
        if key in self.index and isinstance(self.index[key], list):
            self.index[key].append(value)
        else:
            self.index[key] = value

    def add_fn(self, key, fn_name, args):
        ''' Adds a function to the file.

        A function is defined as a dictionary with "name" and "args" keys. The name is a string
        and the args is a dictionary.

        Args:
            key: Key value in the JSON file.
            fn_name: Function name ; String
            args : Function arguments as a dictionary.

        Example usage:

            args = {
                "parameter_1" : "value_1",
                "parameter_2" : [28, 28, 1]
            }
            add_fn("key", "function" args)
        '''

        _fn = {
            "name": fn_name,
            "args": args
        }
        self.add_entry(key, _fn)

    def create_fn_dict(self, name, args=None):
        ''' Creates a dictionary representation of a function.

        This function exists so the user doesn't have to worry about the internal representation
        of a function in the JSON file.

        Args:
            name : Name of the function.
            args : A dictionary of function arguments as "parameter" : "value" elements.

        Returns:
            A dict representing the function.

        Example usage:

            function_name = "flatten"
            args = {
                "input_shape" : [28, 28, 1],
                "parameter" : "value"
            }
            fn_dict = create_fn_dict(function_name, args)
        '''
        return {
            "name": name,
            "args": args if args else None
        }

    def write(self):
        ''' Writes the root dictionary to the JSON file and closes the file.
        '''
        json.dump(self.root, self.out, indent=4)
        self._close()
        print("Saved to {}".format(self.out_file))


class PipelineJsonGenerator(JsonGenerator):
    ''' Generates a dataset pipeline configuration file based on user selections..
    '''

    def __init__(self, out_file):

        super(PipelineJsonGenerator, self).__init__(out_file)

        # Add the root dict
        self.add_entry("pipeline", {})

        # Add the dataset and operations
        self._indent("pipeline")
        self.add_entry("dataset", {})
        self.add_entry("operations", [])

    def add_dataset(self, label):
        ''' Add a dataset source.

        All available datasets can be found in the Tensorflow Datasets catalog.
            (https://www.tensorflow.org/datasets/catalog/overview)

        Args:
            label : dataset identifier. Equivalent to the Tensorflow dataset name.
        '''

        self.add_entry("dataset", {"label": label})

    def add_operation(self, op_name, args=None):
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
        self.add_fn("operations", op_name, args)

    def get_dataset_list(self):
        '''Return a list of all possible dataset sources.
        '''
        pass

    def get_operations_list(self):
        ''' Return a list of all possible preprocessing operations.
        '''
        pass


class ModelJsonGenerator(JsonGenerator):
    ''' Generates a configuration file representing a machine learning model.
    '''

    def __init__(self, out_file):

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
            model_name : Name of the model. Refer to model_options.json for possible model names.
        '''
        self.add_entry("model", {"name": model_name})

    def add_layer(self, layer_name, args=None):
        '''Adds a neural net layer to the file.

        Args:
            layer_name: Name of the layer. Refer to the model_options.json for possible layer names.
            args : A dictionary of arguments (param : value) to pass into the layer function.

        Example usage:

        add_layer("dense", args={
            "units" : 10,
            "activation" : "softmax"
        })

        This translates to tf.keras.layers.Dense(units=10, activation="softmax")
        '''
        self.add_fn("layers", layer_name, args)

    def add_compile(self, args=None):
        '''Adds compiler options to the file.

        Refer to model_options.json for all compiler arg options.

        Args:
            args : A dictionary of arguments passed into the compile function.
        '''
        self.add_fn("compile", "compile", args)

    def get_model_list(self):
        ''' Get the list of all possible model types.
        '''
        pass

    def get_layers_list(self):
        ''' Get the list of all possible layer functions.
        '''
        pass

    def get_compile_list(self):
        ''' Get the list of all possible compile arguments.
        '''
        pass
