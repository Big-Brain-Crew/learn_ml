import generators.preprocessor.pipeline_generator as pipeline_generator
import os
import sys
sys.path.append(os.getcwd())


def main():
    '''Generate a dataset pipeline script.
    '''

    config_gen = pipeline_generator.PipelineConfigGenerator("generators/preprocessor/pipeline.json")

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


if __name__ == "__main__":
    main()
