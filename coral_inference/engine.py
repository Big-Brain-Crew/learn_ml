''' Classes to run inference on the Coral Edge TPU.

This script contains a set of classes that run inference on an edge device. Each child class is
tailored for a specific task, such as object detection or image classification. The classes can be 
easily extended by creating a child class that defines the preprocessing and inference functions.

Classes:
    BaseEngine: Abstract base engine that defines the interface for all child engines.
    DetectionEngine: Performs object detection inference with any SSD quantized model.

'''

import os
import cv2
from PIL import Image
from abc import abstractmethod
from edgetpu.detection.engine import DetectionEngine as EdgeTPUDetectionEngine
import numpy as np


class BaseEngine(object):
    ''' Abstract base engine defining methods for running inference.
    '''

    def __init__(self,
                 engine):
        ''' Stores the base engine.

        Args:
            engine: Inference engine that is specific to the task. For example, detection and 
                classification will have different engines.
        
        '''

        self.engine = engine

    def invoke(self, frame):
        ''' Performs inference on an image.

        This method will preprocess an image and run inference. The preprocessing and inference 
        methods must be defined by child classes.

        Args:
            frame (array[int]): An image from 0-255.
        
        Returns: Inference prediction

        '''

        inf_input = self.preprocess(frame)

        pred = self.run_inference(inf_input)

        return pred

    @abstractmethod
    def preprocess(self, frame):
        ''' Performs preprocessing required to correctly format the image for inference.
        '''
        pass

    @abstractmethod
    def run_inference(self, frame):
        ''' Performs inference. Specific to the inference task.
        '''
        pass


class DetectionEngine(BaseEngine):
    ''' Performs inference with any SSD object detection quantized model.

    This class will generate predictions for an image using a given object detection model. The
    number of predictions and labels can be customized. Any Single Shot Detector model that has
    been quantized for the Edge TPU can be used.

    Attributes:
        labels (dict, optional): Stores the mapping between prediction IDs and labels. If not
            specified, then the user can just retreive the label ID as an integer.
        top_k (int): The maximum number of detection candidates to return.
        threshold (float): The minimum confidence score of candidates to return.

    '''
    def __init__(self,
                 model_path,
                 label_path="",
                 top_k=5,
                 threshold=0.5):
        ''' Loads the engine and labels.
        '''

        if not os.path.exists(model_path):
            raise ValueError("Cannot find model file.")

        self.labels = self.load_labels(label_path)
        self.top_k = top_k
        self.threshold = threshold

        super(DetectionEngine, self).__init__(EdgeTPUDetectionEngine(model_path))

    def load_labels(self, label_path):
        ''' Loads label file into a dictionary.

        The label file must be a .txt file that specifies the label for each index. It should
        consist of lines like the following:

        0  person
        1  bicycle
        2  traffic light

        Args:
            label_path (str): Path to the labels file
        
        Returns:
            Dictionary of labels if the label_path exists, else None

        Example:
            (For the above labels)
            labels = {
                0: "person",
                1: "bicycle",
                2: "traffic light"
            }

        '''
        if label_path and os.path.exists(label_path):
            labels = {}
            with open(label_path, "r") as file:
                for line in file.readlines():
                    split = line.split(" ")
                    num = int(split[0])
                    label = line[len(split[0]):].strip(" \n")
                    labels[num] = label
            return labels
        else:
            return None

    def invoke(self, frame):
        ''' Runs inference.

        This method runs inference just like the base method. If labels have been
        specified, then it only returns the inference results if they have a corresponding label.
        This allows the user to specify a subset of predictions to return if the model is trained
        on many objects.

        Args:
            frame: input frame to the engine.

        Returns:
            list of DetectionCandidates (EdgeTPU class).

        '''
        preds = super().invoke(frame)

        if self.labels:
            labeled_preds = []
            for i, pred in enumerate(preds):
                if pred.label_id in self.labels:
                    labeled_preds.append(pred)

            return labeled_preds

        else:
            return preds

    def preprocess(self, frame):
        ''' Formats the input frame for the detection engine.

        The EdgeTPU engine expects RGB images in PIL format. The images are converted from 
        BGR in OpenCV to PIL.

        Args:
            frame: Input frame to the engine.

        Returns:
            RGB PIL image.

        '''

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb_frame)

        return image

    def run_inference(self, frame):
        return self.engine.detect_with_image(frame,
                                             threshold=self.threshold,
                                             top_k=self.top_k)

    def get_max_length(self):
        ''' Returns max number of detection candidates.
        '''

        return self.top_k

    def label(self, pred):
        ''' Returns the label for the prediction if it exists.
        '''
        
        if self.labels:
            return self.labels[pred.label_id]
        else:
            return ""
