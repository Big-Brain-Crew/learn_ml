''' Manages data requests for a generic threaded function.

This function will handle starting, stopping, and data requests for any given thread. 
The wait() function should be called in any get() method to spawn a new request for data. This
request will be granted once the latest thread loop has been run. This class can handle any 
number of listener threads requesting data.

Classes:
    Event: Stores all the listener threads waiting on data. Signals those threads when the data is
        ready.
    ThreadManager: Manages the starting, waiting, and setting of a generic thread.

'''

import time
import threading

try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident


class Event(object):
    """ An Event-like class that signals all active clients when a new frame is
    available.
    """

    def __init__(self):
        self.events = {}

    def wait(self):
        """ Invoked from each client's thread to wait for the next frame."""
        ident = get_ident()
        if ident not in self.events:
            # this is a new client
            # add an entry for it in the self.events dict
            # each entry has two elements, a threading.Event() and a timestamp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """ Invoked by the camera thread when a new frame is available."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # if this client's event is not set, then set it
                # also update the last set timestamp to now
                event[0].set()
                event[1] = now
            else:
                # if the client's event is already set, it means the client
                # did not process a previous frame
                # if the event stays set for more than 5 seconds, then assume
                # the client is gone and remove it
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """ Invoked from each client's thread after a frame was processed."""
        self.events[get_ident()][0].clear()


class ThreadManager(object):
    ''' Manages a generic thread.

    Attributes:
        thread: Stores the background thread.
        last_access (float): The time that the thread was last requested for data.
        event: Event() class that handles notifying all listeners.

    '''

    def __init__(self,
                 obj):
        ''' Initializes thread.

        The object being passed as a parameter must defined a _thread() function. This function
        will be passed to the background thread to be run.

        Args:
            obj: The class with the thread to be managed.

        '''

        self.thread = None  # Background thread
        self.last_access = 0
        self.event = Event()

        """Start the background thread if it isn't running yet."""
        if self.thread is None:
            self.last_access = time.time()

            # start background frame thread
            self.thread = threading.Thread(target=obj._thread)

    def start(self):
        ''' Start the thread.
        '''

        if not self.thread.is_alive():
            self.thread.start()
    
    def wait(self):
        ''' Waits for the signal that the thread loop has completed.
        '''

        self.last_access = time.time()

        # wait for a signal from the camera thread
        self.event.wait()
        self.event.clear()

    def set(self):
        ''' Notifies all listeners that new data is ready.
        '''

        self.event.set()

    def time_lapsed(self):
        return time.time() - self.last_access

    def stop(self):
        ''' Stops the thread.
        '''
        
        self.thread = None

