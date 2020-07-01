from PySide2.QtCore import QObject, Signal, Slot, Property
from PySide2.QtQml import QQmlProperty

from learn_ml.deploy import deploy 
from learn_ml.utils.log_configurator import LogConfigurator


class DeployManager(QObject):

    def __init__(self):
        QObject.__init__(self)

        # Instantiate LogConfigurator
        self.log_config = LogConfigurator()

        # Get the logger for module
        self.logger = self.log_config.get_logger(__name__)

        self.video = ""

    @Slot(str, str)
    def deploy(self, task, stream):
        self.__deploy(task, stream)

    def __deploy(self, task, stream):
        print("Deploying")
        stream = deploy.deploy_usb(task, stream)
        self.__set_stream(stream)
    
    def __set_stream(self, stream):
        self.video = stream
        self.streamChanged.emit(stream)
    
    def get_stream(self):
        return self.video

    streamChanged = Signal(str)

    stream = Property(str, get_stream, notify=streamChanged)