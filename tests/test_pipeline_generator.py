import generators.python_generators as python_generators
import os
import sys
sys.path.append(os.getcwd())


def main():
    '''Generate a dataset pipeline script.
    '''

    pipe_gen = python_generators.PipelineGenerator(pipeline_config="project/pipeline.json",
                                                   map_config="generators/pipeline_map.json")
    pipe_gen.gen_pipeline()


if __name__ == "__main__":
    main()
