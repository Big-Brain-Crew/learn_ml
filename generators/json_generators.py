import json

class JsonGenerator(object):
    def __init__(self, out_file):
        
        self.out_file = out_file
        self.out = open(self.out_file, "w+")

        self.root = {}
        self.index = self.root
    
    def _close(self):
        self.out.close()
        
    def indent(self, name):
        self.index = self.root[name]

    def unindent(self):
        self.index = self.root

    def add_entry(self, name, entry):
        if name in self.index and isinstance(self.index[name], list):
            self.index[name].append(entry)
        else:
            self.index[name] = entry
    
    def add_fn(self, location, fn_name, args):
        fn = {
            "name" : fn_name,
            "args" : args
        }
        self.add_entry(location, fn)
    
    def write(self):
        json.dump(self.root, self.out, indent=4)
        self._close()
        print("Saved to {}".format(self.out_file))
    
class PipelineJsonGenerator(JsonGenerator):
    ''' Generates a pipeline config JSON file based on user selections.

    Generates a config file that describes a dataset preprocessing pipeline
    based off a user's selection of dataset source and preprocessing operations.
    '''

    def __init__(self, out_file):

        super(PipelineJsonGenerator, self).__init__(out_file)

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
        self.add_fn("operations", op_name, args)
        
    
class ModelJsonGenerator(JsonGenerator):
    def __init__(self, out_file):

        super(ModelJsonGenerator, self).__init__(out_file)

        # Add the root dict
        self.add_entry("model", {})
        
        self.indent("model")
        self.add_entry("model", {})
        self.add_entry("layers", [])
        self.add_entry("compile", {})

    def add_model(self, model_name):
        self.add_entry("model", {
            "name" : model_name
        })    

    def add_layer(self, layer_name, args={}):
        self.add_fn("layers", layer_name, args)

    def add_optimizer(self, optim_name, args={}):
        self.optimizer = {
            "name" : optim_name,
            "args" : args
        }

    def add_compile(self, args={}):
        args["optimizer"] = self.optimizer

        self.add_fn("compile","compile", args)