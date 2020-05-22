import os
import sys
sys.path.append(os.getcwd())

import generators.json_generators as json_generators


def main():
    '''Generate a dataset pipeline script.
    '''

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

    optim_args = {
        "learning_rate" : 0.001
    }
    args = {
        "loss" : "crossentropy",
        "optimizer" : config_gen.add_optimizer("adam", optim_args),
        "metrics" : "accuracy"
    }
    config_gen.add_compile(args)

    config_gen.write()


if __name__ == "__main__":
    main()

