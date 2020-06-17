''' Interfaces with QML to receive user input and generate a list of search results.
'''

import random
import numpy as np
import difflib
import json

from PySide2.QtCore import QObject, Signal, Slot, Property
from PySide2.QtQml import QQmlProperty
from learn_ml.utils.log_configurator import LogConfigurator


class SearchPanel(QObject):
    ''' Receives a user input and generates a list of search results.

    Interfaces with QML through the use of slots, signals, and properties.
    '''

    def __init__(self):
        QObject.__init__(self)

        # Instantiate LogConfigurator
        self.log_config = LogConfigurator()

        # Get the logger for module
        self.logger = self.log_config.get_logger(__name__)

        self.__results = []  # Store search results
        self.__results_idx = 0
        self.__num_results = len(self.__results)

        self.results_options = self.get_results_options(
            json.load(open("learn_ml/generators/options/layer_options.json")))

    def get_results_options(self, results_options_config):
        results_options = []
        layers = results_options_config["layer_options"]
        for name, args in layers.items():
            results_options.append(name)
        return results_options

    def get_results(self):
        ''' Returns a single result from the results list.

        The class keeps track of which results have already been passed to QML.
        '''

        result=self.__results[self.__results_idx]
        self.__results_idx += 1
        return result

    def get_num_results(self):
        return self.__num_results

    def __set_results(self, results):
        ''' Set new search results and emit a signal to QML.
        '''

        self.__results=results
        self.__num_results=len(self.__results)
        self.__results_idx=0
        self.resultsChanged.emit(1)

    def __search(self, input):
        new_results=difflib.get_close_matches(input, self.results_options, n=8, cutoff=0.4)

        self.__set_results(new_results)

    # Signal: emits when search results are updated
    resultsChanged=Signal(int)

    # Called when user enters a new input
    @ Slot(str)
    def search(self, search_input):
        self.__search(search_input)

    # QML accessible properties
    results=Property(str, get_results, notify=resultsChanged)
    numResults=Property(int, get_num_results, notify=resultsChanged)
