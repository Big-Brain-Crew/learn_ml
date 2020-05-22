import os
import sys
sys.path.append(os.getcwd())

import generators.json_generators as json_generators
import generators.python_generators as python_generators

def create_pipeline_json():
    config_gen = json_generators.PipelineJsonGenerator("project/pipeline.json")

    config_gen.add_dataset("mnist")

    args = {
        "map_func" : "normalize_img",
        "num_parallel_calls" : "autotune"
    }
    config_gen.add_operation("map", args)

    args = {}
    config_gen.add_operation("cache", args)

    args = {
        "buffer_size" : "train_size",
    }
    config_gen.add_operation("shuffle", args)

    args = {
        "batch_size" : 128
    }
    config_gen.add_operation("batch", args)

    args = {
        "buffer_size" : "autotune"
    }
    config_gen.add_operation("prefetch", args)

    config_gen.write()

def create_model_json():
    config_gen = json_generators.ModelJsonGenerator("project/model.json")

    config_gen.add_model("sequential")

    args = {
        "input_shape" : [28, 28, 1]
    }
    config_gen.add_layer("flatten", args)

    args = {
        "units" : 128,
        "activation" : "relu"
    }
    config_gen.add_layer("dense", args)

    args = {
        "units" : 10,
        "activation" : "softmax"
    }
    config_gen.add_layer("dense", args)

    
    args = {
        "loss" : "crossentropy",
        "optimizer" : config_gen.create_fn_dict("adam", {"learning_rate" : 0.001}),
        "metrics" : ["accuracy"]
    }
    config_gen.add_compile(args)

    config_gen.write()

def create_pipeline():
    pipe_gen = python_generators.PipelineGenerator(pipeline_config="project/pipeline.json",
                                                   map_config="generators/pipeline_map.json")
    pipe_gen.gen_pipeline()

def create_model():
    pipe_gen = python_generators.ModelGenerator(model_config="project/model.json",
                                 map_config="generators/model_map.json")
    pipe_gen.gen_model()


def main():
    '''Generate a dataset pipeline script.
    '''
    create_pipeline_json()
    create_pipeline()
    create_model_json()
    create_model()

if __name__ == "__main__":
    main()
