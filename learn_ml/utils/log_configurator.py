import logging, logging.handlers
import traceback
import os
import sys
from singleton_decorator import singleton

@singleton
class LogConfigurator():
    """ Class to configure logger and get a logger for modules.

    This is a singleton class to configure the logging and retrieve a logger for each class.
    This class should be instantiated at the very start of the program with the desired configuration.
    Next, each module gets the instance and calls the get_logger function with the module name to
    get a configured logger for the module.

    """

    def __init__(self, verbosity = "INFO", output_to_logfile = True, log_dir = "logs",
                    log_name = "app.log", max_bytes = 1000000, num_logs_to_keep = 5):
        """ Initializes the LogConfigurator class.

        args:
            verbosity: Verbosity level of the logs. Options are DEBUG, INFO, WARN, ERROR, CRITICAL.
                Default - INFO
            output_to_logfile: Whether or not to output to logfiles. If False, output will be written
                to stderr. Default - True
            log_dir: Only used if output_to_logfile = True. Directory in which to store logfiles.
                Default - "logs"
            log_name: Only used if output_to_logfile = True. Name of the logfile.
                Default - "app.log"
            max_bytes: Only used if output_to_logfile = True. Maximum logfile size. Default - 1000000 (1 MB)
            num_logs_to_keep: Only used if output_to_logfile = True. Number of log files to store before deleting
                Default - 5

        """

        # Instantiate the root logger
        self.root_logger = logging.getLogger()

        # Create a StreamHandler if not outputting to a log file
        # The StreamHandler will output to stderr
        # Else, write the logs to a rotating log file
        if not output_to_logfile:
            self.handler = logging.StreamHandler()
        else:
            # Save the arguments for rotating file handler
            self.log_dir = log_dir
            self.log_name = os.path.join(self.log_dir, log_name)
            self.max_bytes = max_bytes
            self.num_logs_to_keep = 5

            # Ensure log dir exists
            if(not os.path.exists(self.log_dir)):
                os.makedirs(self.log_dir)

            # Create a rotating file handler
            self.handler = logging.handlers.RotatingFileHandler(self.log_name, maxBytes = self.max_bytes, backupCount = self.num_logs_to_keep)

        # Define the log format
        formatter = logging.Formatter('%(levelname)s - %(name)s - %(asctime)s: %(message)s')
        self.handler.setFormatter(formatter)

        # Add the handler to the root logger
        self.root_logger.addHandler(self.handler)

        self.set_level(verbosity)

        sys.excepthook = self._get_exception_handler()

    def _get_exception_handler(self):
        def except_handler(type, value, error_traceback):
            self.root_logger.exception("Uncaught exception: {}, {}, {}".format(str(type), str(value), traceback.format_tb(error_traceback)))

        return except_handler

    def set_level(self, verbosity):
        """ Set verbosity level of logger.

        args:
            verbosity: Verbosity level. Options are DEBUG, INFO, WARN, ERROR, CRITICAL

        """

        self.root_logger.setLevel(verbosity)
        print(self.root_logger.getEffectiveLevel())

    def get_logger(self, name):
        """ Returns a logger object for a specific module.

        Args:
            name: Name of the logger, the value passed should be __name__

        Returns:
            logger object used to output logs from the module.
        """
        return logging.getLogger(name)

    def debug_enabled(self):
        """ Returns true if debug level should be printed.

        """
        return self.root_logger.getEffectiveLevel >= 10

    def info_enabled(self):
        """ Returns true if info level should be printed.

        """
        return self.root_logger.getEffectiveLevel >= 20

    def warning_active(self):
        """ Returns true if warning level should be printed.

        """
        return self.root_logger.getEffectiveLevel >= 30

    def error_active(self):
        """ Returns true if error level should be printed.

        """
        return self.root_logger.getEffectiveLevel >= 40

    def critical_active(self):
        """ Returns true if critical level should be printed.

        """
        return self.root_logger.getEffectiveLevel >= 50

