import learn_ml.generators.generator_utils as generator_utils
import learn_ml.generators.python_generators as python_generators
import learn_ml.generators.json_generators as json_generators
import os
import sys
sys.path.append(os.getcwd())


def create_pipeline_json():
    config_gen = json_generators.PipelineJsonGenerator("project/pipeline.json")

    config_gen.add_dataset("mnist")

    args = {
        "map_func": "normalize_img",
        "num_parallel_calls": "autotune"
    }
    config_gen.add_train_operation("map", args)

    args = {}
    config_gen.add_train_operation("cache", args)

    args = {
        "buffer_size": "train_size",
    }
    config_gen.add_train_operation("shuffle", args)

    args = {
        "batch_size": 128
    }
    config_gen.add_train_operation("batch", args)

    args = {
        "buffer_size": "autotune"
    }
    config_gen.add_train_operation("prefetch", args)

    args = {
        "map_func" : "normalize_img",
        "num_parallel_calls" : "autotune"
    }
    config_gen.add_test_operation("map", args)

    args = {}
    config_gen.add_test_operation("cache", args)

    args = {
        "batch_size" : 128
    }
    config_gen.add_test_operation("batch", args)

    args = {
        "buffer_size" : "autotune"
    }
    config_gen.add_test_operation("prefetch", args)

    config_gen.write()


def create_model_json():
    config = json_generators.ModelJsonGenerator("project/model.json")

    config.add_model("sequential")

    # Input
    config.add_layer("input", args={
        "shape": [28, 28],
        "dtype": "float32",
        "name": "\"TEST\""
    })

    # Reshape
    config.add_layer("reshape", args={
        "target_shape": [28, 28, 1]
    })

    # Conv2D
    config.add_layer("conv2d", args={
        "filters": 12,
        "kernel_size": [3, 3],
        "activation": "relu"
    })

    # Max Pooling
    config.add_layer("max_pooling_2d", args={
        "pool_size": [2, 2],
    })

    # Flatten
    config.add_layer("flatten")

    # Dropout
    config.add_layer("dropout", args={
        "rate": 0.2
    })

    # Dense
    config.add_layer("dense", args={
        "units": 10,
        "activation": "softmax"
    })

    args = {
        "loss": "crossentropy",
        "optimizer": generator_utils.create_fn_dict("adam"),
        "metrics": ["accuracy"]
    }
    config.add_compile(args)

    config.write()


def create_pipeline():
    pipe_gen = python_generators.PipelineGenerator(pipeline_config="project/pipeline.json",
                                                   map_config="learn_ml/generators/pipeline_map.json",
                                                   out="./project/pipelines/pipeline_1.py")
    pipe_gen.gen_pipeline()


def create_model():
    pipe_gen = python_generators.ModelGenerator(model_config="project/model.json",
                                                map_config="learn_ml/generators/model_map.json",
                                                out="./project/models/model_1.py")
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
