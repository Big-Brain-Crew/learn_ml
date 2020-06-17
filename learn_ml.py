'''Main entry-point to launch the application.

This will launch the learn_ml application to a new project.
'''

import sys, os
import argparse

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide2.QtCore import QUrl

from learn_ml.utils.log_configurator import LogConfigurator
from learn_ml.ui.python_classes.NavigationButton import NavigationButton
from learn_ml.ui.python_classes.SearchPanel import SearchPanel
from learn_ml.ui.python_classes.NodeManager import NodeManager

def main(verbosity, log_to_file):

    # Configure the LogConfigurator and instantiate logger for this module
    logConfig = LogConfigurator(verbosity = "DEBUG", output_to_logfile = log_to_file)

    # Create the QML Application and Engine
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Instantiate custom python classes and add them to QML engine
    nav_buttons = NavigationButton()
    search_panels = SearchPanel()
    engine.rootContext().setContextProperty("nav_buttons", nav_buttons)    
    qmlRegisterType(SearchPanel, "Search", 1, 0, "SearchPanel")
    qmlRegisterType(NodeManager, "Node", 1, 0, "NodeManager")

    # Load the main QML file
    engine.load(QUrl("learn_ml/ui/app.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    # Begin execution
    sys.exit(app.exec_())

if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbosity', help='Verbosity level, options are DEBUG, INFO, WARN, ERROR, CRITICAL', default="INFO")
    parser.add_argument('-p', '--print', help='Address of the coral device', action= "store_false")
    args = parser.parse_args()

    main(args.verbosity, False)
