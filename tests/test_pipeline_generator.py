import os, sys
# sys.path.append(os.getcwd())
import generators.preprocessor.pipeline_generator as pipeline_generator

def main():
    '''Generate a dataset pipeline script.
    '''

    pipe_gen = pipeline_generator.PipelineGenerator(pipeline_config="generators/preprocessor/pipeline.json",
                                 mapping_config="generators/preprocessor/variable_map.json")
    pipe_gen.gen_pipeline()


if __name__ == "__main__":
    main()