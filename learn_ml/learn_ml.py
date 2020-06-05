'''Main entry-point to launch the application.

This will launch the learn_ml application to a new project.
'''

import sys
from utils.log_configurator import LogConfigurator
from Qt.QtWidgets import QApplication
import argparse

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QUrl

from ui.NavigationButton import NavigationButton



def main(verbosity, log_to_file):
    # Configure the LogConfigurator and instantiate logger for this module
    logConfig = LogConfigurator(verbosity = "DEBUG", output_to_logfile = log_to_file)

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    nav_buttons = NavigationButton()
    engine.rootContext().setContextProperty("nav_buttons", nav_buttons)

    engine.load(QUrl("learn_ml/ui/app.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbosity', help='Verbosity level, options are DEBUG, INFO, WARN, ERROR, CRITICAL', default="INFO")
    parser.add_argument('-p', '--print', help='Address of the coral device', action= "store_false")
    args = parser.parse_args()

    main(args.verbosity, False)
