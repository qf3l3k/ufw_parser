import logging
import os

from logging.handlers import RotatingFileHandler


def initialize_loggers(log_directory='~/.ufw_parser/logs', log_filename='ufw_parser.log', log_level=logging.DEBUG):
    """
    Set up and configure two loggers for the application: console and file.
    Logs will be stored in the specified log_directory with the filename log_filename.
    The log_level determines the minimum level of messages that get logged.

    Args:
    log_directory (str): The directory where log files will be stored.
    log_filename (str): The filename for the log file.
    log_level (int): The logging level as defined in Python's logging module.
    """

    # Expand path
    log_directory = os.path.expanduser(log_directory)

    # Create log directory if it doesn't exist
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Create a logger object
    logger = logging.getLogger("ufw_parser_log")
    logger.setLevel(log_level)

    # Define the log message format
    log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(message)s')

    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(log_level)

    # Set up file handler with rotation
    file_path = os.path.join(log_directory, log_filename)
    file_handler = RotatingFileHandler(file_path, maxBytes=10485760, backupCount=5) # 10MB per file, max 5 files
    file_handler.setFormatter(log_format)
    file_handler.setLevel(log_level)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger



