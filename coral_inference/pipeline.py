''' Inference pipeline for any source, engine, postprocessor, and stream.

Each step of the pipeline must follow the base class interface defined in the other scripts.

'''

# TODO: Add the ability to add a stream or display while running inference
class Pipeline(object):
    '''Runs end-to-end inference.

    Attributes:
        source: The image source.
        engine: The inference engine.
        postprocessor: Processes the inference predictions for streaming.
        streams: One or multiple streams for the data.
    '''

    def __init__(self,
                 source,
                 engine,
                 postprocessor,
                 streams = []):
        
        self.source = source
        self.engine = engine
        self.postprocessor = postprocessor
        self.streams = streams

    def start(self):
        ''' Start all the pipeline stages.
        '''

        self.source.start()
        self.engine.start()
        self.postprocessor.start()

        if isinstance(self.streams, list):
            for stream in self.streams:
                stream.start()
        elif self.streams:
            self.streams.start()

    def get_source_frame(self):
        ''' Return the original image.
        '''

        return next(self.engine)[1]
    
    def get_prediction(self):
        ''' Return the inference prediction.
        '''

        return next(self.engine)[0]

    def get_output_frame_bytes(self):
        ''' Return the postprocessed frame in bytes.
        '''
        
        return self.postprocessor.frame_tobytes()
