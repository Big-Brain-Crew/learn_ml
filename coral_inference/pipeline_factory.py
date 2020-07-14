''' Factory classes for creating an inference pipeline.

The pipeline factory classes can be used to create inference pipelines for different inference
tasks. The class heirarchy can be extended by creating a child class that defines methods for
creating a source, engine, postprocessor, and stream(s).

Classes:
    PipelineFactory: Abstract factory defining the interface for all child classes.
    DetectionPipelineFactory: Creates a pipeline for performing object detection.

'''

from abc import abstractmethod

import camera
import engine
import threaded_engine
import postprocessor
import stream_spi
import pipeline

instance = None # Only one factory allowed per program.

def get_instance(task):
    ''' Create or return the instance of the factory.

    The factory must be a singleton so that only one pipeline can be made. Currently, there is no 
    way to run inference with multiple models on the same edge TPU.

    Args:
        task (str): The inference task to be performed. Currently only supports "detection"
    
    Returns:
        An instance of the pipeline factory.
    '''

    global instance
    if not instance:
        if task == "detection":
            instance = DetectionPipelineFactory()
        else:
            raise ValueError("Task not supported yet.")

    return instance


class PipelineFactory(object):
    ''' Abstract base class for pipeline factories.

    Attributes:
        pipeline: The inference pipeline.
    '''

    def __init__(self):
        self.pipeline = None

    @abstractmethod
    def create_pipeline(self, params):
        ''' Creates an end-to-end inference pipeline.

        The pipeline can be configured with the input parameters. The parameters should be stored 
        in a JSON file like the following example:

        {
            "app_params" : {
                "source" : {
                    "param_1" : "val_1",
                    "param_2" : "val_2"
                },
                "engine" : {
                    "param" : "val"
                },
                "postprocessor" : {
                    "param" : "val"
                },
                "stream_spi" : true,
                "stream_flask" : false
            }
        }

        Refer to app_param_options.json for all possible params and their values.

        Args:
            params: A dictionary of parameters for creating the pipeline.

        '''
        pass

    @abstractmethod
    def create_source(self, params):
        ''' Creates the image source.

        Args:
            params: Dictionary of parameters to be set.

        '''
        pass

    @abstractmethod
    def create_engine(self, source, params):
        ''' Creates the inference engine.

        Args:
            source: input image source.
            params: Dictionary of parameters to be set.

        '''
        pass

    @abstractmethod
    def create_postprocessor(self, source, params):
        ''' Creates the postprocessor.

        Args:
            source: inference engine source.
            params: Dictionary of parameters to be set.

        '''
        pass

    @abstractmethod
    def create_streams(self, use_spi, use_flask):
        ''' Creates the data streams.

        Currently only supports either Arduino SPI or flask video stream.

        Args:
            use_spi (bool): True for Arduino data stream.
            use_flask (bool): True for Flask data stream.
        
        '''
        pass


class DetectionPipelineFactory(PipelineFactory):
    ''' Factory methods for creating an object detection inference pipeline.
    '''
    
    def __init__(self):

        super(DetectionPipelineFactory, self).__init__()

    def get_pipeline(self):
        return self.pipeline

    def create_pipeline(self, params):

        if self.pipeline:
            return self.pipeline

        # Create source
        self.source = self.create_source(params["source"])

        # Create engine
        self.engine = self.create_engine(self.source, params["engine"])

        # Create postprocessor
        self.postprocessor = self.create_postprocessor(self.engine, params["postprocessor"])

        # Create streams
        self.streams = self.create_streams(params["stream_spi"], params["stream_flask"])

        # Create inference pipeline
        self.pipeline = pipeline.Pipeline(self.source,
                                          self.engine,
                                          self.postprocessor,
                                          self.streams)

        return self.pipeline

    def create_source(self, params):
        return camera.OpenCVCamera(source=params["source"])

    def create_engine(self, source, params):
        detection_engine = engine.DetectionEngine(model_path=params["model_path"],
                                                  label_path=params["label_path"],
                                                  top_k=params["top_k"],
                                                  threshold=params["threshold"])

        return threaded_engine.ThreadedEngine(source, detection_engine)

    def create_postprocessor(self, source, params):
        return postprocessor.DetectionPostProcessor(source,
                                                    output_resolution=params["output_resolution"])

    def create_streams(self, use_spi, use_flask):
        streams = []
        if use_spi:
            spi = stream_spi.SPIComms(self.postprocessor)
            streams.append(spi)
        if use_flask:
            pass

        return streams
