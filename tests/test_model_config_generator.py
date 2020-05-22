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

    
    args = {
        "loss" : "crossentropy",
        "optimizer" : config_gen.create_fn_dict("adam", {"learning_rate" : 0.001}),
        "metrics" : ["accuracy", "mae"]
    }
    config_gen.add_compile(args)

    config_gen.write()


if __name__ == "__main__":
    main()

