import os, sys
sys.path.append(os.getcwd())
import generators.model.model_generator as model_generator

def main():
    '''Generate a dataset pipeline script.
    '''

    pipe_gen = model_generator.ModelGenerator(model_config="generators/model/model.json",
                                 mapping_config="generators/model/model_map.json")
    pipe_gen.gen_model()


if __name__ == "__main__":
    main()