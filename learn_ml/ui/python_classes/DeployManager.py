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

    @Slot(str)
    def deploy(self, task):
        self.__deploy(task)

    def __deploy(self, task):
        print("Deploying")
        deploy.deploy_usb(task)