'''Main entry-point to launch the application.

This will launch the learn_ml application to a new project.
'''

import sys
from utils.log_configurator import LogConfigurator
from ui.App import LearnML
from Qt.QtWidgets import QApplication
import argparse




def main(verbosity, log_to_file):
    # Configure the LogConfigurator and instantiate logger for this module
    logConfig = LogConfigurator(verbosity = "DEBUG", output_to_logfile = log_to_file)

    app = QApplication(sys.argv)

    instance = LearnML.instance()
    if instance is not None:
        app.setActiveWindow(instance)
        instance.show()

        try:
            sys.exit(app.exec_())
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbosity', help='Verbosity level, options are DEBUG, INFO, WARN, ERROR, CRITICAL', default="INFO")
    parser.add_argument('-p', '--print', help='Address of the coral device', action= "store_false")
    args = parser.parse_args()

    main(args.verbosity, False)
