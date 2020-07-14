''' Classes to stream video from camera sources.

These classes create a background thread that continuously streams camera images.
Any number of other threads can tune in and receive new images. The class structure can 
easily be extended by implementing a few package-specific functions. For example, the
OpenCVCamera class only has to implement the code to read an image using OpenCV.

Classes:
    BaseCamera: Base class that handles threading, starting/stopping, and getting frames.
    OpenCVCamera: Streams video using OpenCV.

'''

import os
import cv2
from abc import abstractmethod
import numpy as np
import time

from thread_manager import ThreadManager


class BaseCamera(object):
    ''' Base class for streaming video in a background thread.

    This class continuously pulls new images in a thread. When a separate thread calls the 
    get() function to retrieve a frame, the ThreadManager blocks until a new frame comes in
    and then returns a frame to all listeners. This ensures that no duplicate frames are retreived.

    Attributes:
        source (str): The file path of the video source.
            For example, this could be "/dev/video0". Run v4l2-ctl --list-devices to find your device.
        resolution (tuple[int]): Stores the camera resolution.
        frame (array[int]): Stores the current frame.
        thread_manager: A separate class that handles incoming requests for frames. 

    '''
    def __init__(self,
                 source,
                 resolution):
        ''' Sets the video source and creates the thread manager.

        Args:
            source (str): The file path of the video stream.
            resolution (tuple[int]): The camera resolution. 

        '''

        self.source = source
        self.resolution = resolution
        self.frame = None  # current frame is stored here by background thread

        self.thread_manager = ThreadManager(self)

    def __iter__(self):
        ''' Returns itself as an iterator.

        Since the class is structured around generators, there is no need for a separate 
        iterator.

        '''

        return self

    def __next__(self):
        ''' Returns the newest frame.

        This operator allows the class usage to be abstracted. The user can call next(source), and 
        the source can be any video stream that implements this operator.

        Returns: The newest frame.

        '''

        return self.get_frame()

    def _thread(self):
        ''' Continuously pulls new frames from the camera.

        An infinite generator is used to pull new frames. Once a new frame is pulled,
        the thread manager is set, notifying all listeners and handing them the new frame.
        If there have been no listeners for 10 seconds, then the thread stops.

        '''

        frames_iterator = self.frames()
        for frame in frames_iterator:
            self.frame = frame

            # Send signal to listeners
            self.thread_manager.set()

            # if there haven't been any listeners asking for frames in
            # the last 10 seconds then stop the thread
            if self.thread_manager.time_lapsed() > 10:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity.')
                break

        self.thread_manager.stop()

    def start(self):
        ''' Starts the streaming thread.
        '''

        self.thread_manager.start()

    def get_frame(self):
        ''' Waits for a new frame and returns it.
        '''

        self.thread_manager.wait()
        return self.frame

    def get_resolution(self):
        ''' Returns the camera resolution.
        '''

        return self.resolution

    @abstractmethod
    def frames(self):
        ''' Generator that continuously yields frames.

        This method must be implemented by child classes. It should be an infinite while loop
        that yields new camera frames.

        Yields: The newest camera frame.

        '''

        pass


# TODO: Add a way to change the input camera resolution. This will reduce processing time.
class OpenCVCamera(BaseCamera):
    ''' Streams video from a camera using OpenCV.

    Attributes:
        camera: The camera source object.

    '''

    def __init__(self,
                 source="/dev/video0"):
        ''' Creates the camera source.

        Args:
            source (str): The file path of the video source. Defaults to the first video source 
                (usually a laptop camera or the first usb webcam plugged in).
        '''

        self.camera = self.set_camera(source)

        resolution = (self.camera.get(3), self.camera.get(4))

        super(OpenCVCamera, self).__init__(source,
                                           resolution)

    def frames(self):
        ''' Continuously yields new frames.
        '''

        while True:

            # read current frame
            _, frame = self.camera.read()

            yield frame

    def set_camera(self, source):
        ''' Sets the OpenCV video source.

        OpenCV creates a source using an integer that is taken from the last character of the
        camera file path. For example, "/dev/video0" can be created with cv2.VideoCapture(0).

        Args:
            source (str): The file path of the video source. Must be of the form "/dev/videoX",
                where X is an integer.

        Raises:
            ValueError: Cannot interpret the input string.
            RuntimeError: Cannot start the camera (meaning camera doesn't exist).

        '''
        try:
            split = source.split("/")
            video_source = int(split[2][-1])

        except (IndexError, ValueError):
            raise ValueError("source must of the form /dev/{source}." +
                             " Run v4l2-ctl --list-devices for available sources.")

        camera = cv2.VideoCapture(video_source)

        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        return camera