from thread_manager import ThreadManager
import time

# TODO: Find a better solution than putting the engine inside the threadedengine
class ThreadedEngine(object):

    def __init__(self,
                 source,
                 engine):
        self.source = source
        self.engine = engine
        self.thread_manager = ThreadManager(self)
        self.pred = None

    def __next__(self):
        return self.get_prediction()

    def _thread(self):
        predictions = self.inference_gen()
        for prediction in predictions:
            self.pred = prediction
            self.thread_manager.set()
    
    def inference_gen(self):
        while True:
            self.frame = next(self.source)
            yield self.engine.invoke(self.frame)

    def get_prediction(self):
        self.thread_manager.wait()
        return self.pred, self.frame

    def get_max_length(self):
        return self.engine.get_max_length()

    def label(self, pred):
        return self.engine.label(pred)
        
    def start(self):
        self.thread_manager.start()
