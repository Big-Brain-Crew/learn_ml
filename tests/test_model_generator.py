import os, sys
sys.path.append(os.getcwd())
import generators.python_generators as python_generators
def main():
    '''Generate a dataset pipeline script.
    '''

    pipe_gen = python_generators.ModelGenerator(model_config="generators/model/model.json",
                                 map_config="generators/model/model_map.json")
    pipe_gen.gen_model()


if __name__ == "__main__":
    main()