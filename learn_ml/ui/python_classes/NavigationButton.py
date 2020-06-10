import random

from PySide2.QtCore import QObject, Signal, Slot
from utils.log_configurator import LogConfigurator


class NavigationButton(QObject):
    def __init__(self):
        QObject.__init__(self)

        # Instantiate LogConfigurator
        self.log_config = LogConfigurator()

        # Get the logger for module
        self.logger = self.log_config.get_logger(__name__)


    nextNumber = Signal(int)

    @Slot(str)
    def buttonPressed(self, button_text):
        self.logger.info("\"{}\" was pressed!!!!!!!!".format(button_text))