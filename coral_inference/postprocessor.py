''' Processes inference predictions to be streamed or visualized.

Right now these classes can be used to stream the data as bytes over SPI to the Arduino or 
video streamed using Flask. The video stream will add bounding boxes and labels to help with
visualization.

Classes:
    PostProcessor: Abstract base class.
    DetectionPostProcessor: Converts detection results into bytes and video streams.

'''

from abc import abstractmethod
import cv2
import numpy as np

import thread_manager


class PostProcessor(object):
    ''' Abstract base class for inference postprocessors.

    Attributes:
        source: Inference source. Contains original image and predictions.
        output_resolution (tuple[int]): Resolution of the output video stream (if there is one).
        thread_manager: Handles requests for data from listeners.

    '''

    def __init__(self,
                 source,
                 output_resolution):
        self.source = source
        self.input_resolution = None
        self.set_output_resolution(output_resolution)
        self.thread_manager = thread_manager.ThreadManager(self)

    def start(self):
        ''' Starts the postprocessor.
        '''

        self.thread_manager.start()

    def set_output_resolution(self, output_resolution):
        ''' Sets the camera output resolution.

        The resolution must be a string of the form 'WIDTHxHEIGHT'. Any width and height
        combo is allowed. Default behavior is to output the raw camera resolution.

        Args:
            output_resolution (str): Output resolution.

        Raises:
            ValueError: Input string is not of the right form.

        '''

        try:
            res_string = output_resolution.lower().split("x")
            self.output_resolution = (int(res_string[0]), int(res_string[1]))
        except (ValueError, IndexError, AttributeError) as e:
            raise ValueError("Resolution must be a string of the form 'WIDTHxHEIGHT'")

    @abstractmethod
    def _thread(self):
        ''' Thread function that performs the postprocessing in a background thread.

        This function must have a for loop that continuously retrieves predictions from the 
        results generator (defined below). It must then notify the thread manager that new results
        have been received.

        '''
        pass

    def results_gen(self):
        ''' Infinite generator that yields predictions from the source.
        '''

        while True:
            yield next(self.source)

class DetectionPostProcessor(PostProcessor):
    ''' Creates SPI data streams and visualization streams for object detection inference results.

    Attributes:
        pred: Inference results.
        frame: Original input frame.
        elements: Number of elements per prediction for the flattened SPI data stream.
        flatten_length: Length of the flattened array that must be sent by the SPI stream.

    '''

    def __init__(self,
                 source,
                 output_resolution='640x480'):

        self.pred = None
        self.frame = None

        self.elements = 5
        self.flatten_length = source.get_max_length() * self.elements

        super(DetectionPostProcessor, self).__init__(source,
                                                     output_resolution)

    def _thread(self):
        results = self.results_gen()
        for pred, frame in results:
            self.pred = pred
            self.frame = frame

            # Set the input resolution if it hasn't been set
            if not self.input_resolution:
                shape = np.shape(self.frame)
                self.input_resolution = (shape[0], shape[1])

            # Notify the listeners
            self.thread_manager.set()

    def tobytes(self):
        ''' Flatten the detection results into a byte stream.
        
        This method can be used to sent bytes over SPI. Each prediction result is a
        DetectionCandidate object. Each object is taken an converted into 5 elements: the
        label_id and the top-left and bottom-right bounding box coordinates. So, the total flattened
        length is equal to 5 * the number of DetectionCandidate objects. This array is then 
        converted to bytes.

        Returns:
            Flattened predictions as bytes.

        '''

        # Wait for the newest prediction
        self.thread_manager.wait()

        flattened_output = np.zeros(shape=(self.flatten_length,),
                                    dtype=np.float32)

        i = 0
        for pred in self.pred:
            flattened_output[i * self.elements] = pred.label_id
            flattened_output[i * self.elements + 1] = pred.bounding_box[0][0]
            flattened_output[i * self.elements + 2] = pred.bounding_box[0][1]
            flattened_output[i * self.elements + 3] = pred.bounding_box[1][0]
            flattened_output[i * self.elements + 4] = pred.bounding_box[1][1]
            i += 1

        return flattened_output.tobytes()

    def get_flatten_length(self):
        ''' Return the length of the flattened results for the SPI stream.

        This is needed since the SPI stream requires a static length. So, if the flatten length 
        can handle a maximum of 5 detection candidates and only 3 are detected, then the last 10
        elements will just be 0.

        '''

        return self.flatten_length

    def scale_bounding_box(self, coords):
        ''' Scales the relative bounding box coordinates for the desired output resolution.

        Args:
            coords (array[float]): The 4 bounding box coordinates from 0-1. Relative coordinates
                allow for the bounding box to be easily scaled to whatever the output resolution is.

        Returns:
            Bounding box coordinates as integers scaled to the output resolution.

        '''
        
        scaled_coordinates = np.zeros(shape=(len(coords)))
        for i, coord in enumerate(coords):
            scaled_coordinates[i] = coord * self.output_resolution[i % 2]

        return scaled_coordinates.astype("int")

    def visualize(self):
        ''' Draws bounding boxes and labels on the original image.
        '''

        # Wait for the newest prediction
        self.thread_manager.wait()

        # Resize the image to the output resolution
        output = cv2.resize(self.frame.copy(),
                            self.output_resolution,
                            interpolation=cv2.INTER_AREA)

        for pred in self.pred:

            # Get the 4 bounding box coordinates 
            # (top-left x, top-left y, bottom-right x, bottom-right y)
            bb = self.scale_bounding_box(pred.bounding_box.flatten())

            # Get the label corresponding to the prediction ID.
            label = self.source.label(pred)
           
            # Draw the bounding box and label text
            output = cv2.rectangle(output, (bb[0], bb[1]), (bb[2], bb[3]), (255, 255, 0), 2)
            output = cv2.putText(output,
                                 label,
                                 (bb[0] + 4, bb[1] + 25),
                                 cv2.FONT_HERSHEY_SIMPLEX,
                                 fontScale=1,
                                 color=(255, 255, 0),
                                 thickness=2)
        return output

    def frame_tobytes(self):
        ''' Encode the output frame into bytes.
        '''
        
        return cv2.imencode('.jpg', self.visualize())[1].tobytes()
