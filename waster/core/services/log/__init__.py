"""
Configure logging for the service.
"""
import atexit
import json
import logging.config
import logging
import os
from typing import Optional

from ._logger import *

__all__ = ['JSONFormatter', 'NonErrorFilter', 'setup_logging']

LOGGING_CFG_DEFAULT = './config/logging.json'
LOGGING_CFG_ENVVAR = 'WASTER_LOGGING_CONFIG_FILE'


def setup_logging(
        config_file: str | None = None
) -> bool:
    """

    Set up the logging system.

    It tries to load the configuration in the following order, if one source is found then the next ones are ignored.

    #. File provided as a parameter
    #. File defined in the environment variable WASTER_LOGGING_CONFIG_FILE
    #. Default file in "./config/logging.json"
    #. Default logging (no set up)

    :param config_file: The path to the json logging configuration file.
    :type config_file: str, optional
    :raises FileNotFoundError: when the configured file path is not a file.
    """
    config_file = _get_config_file_path(config_file)
    if config_file is None:
        return False  # There is no logging configuration to do.

    with open(config_file, 'r') as config_file:
        config = json.load(config_file)

    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)


def _get_config_file_path(config_file: str = None) -> Optional[str]:
    if config_file is None:
        config_file = os.environ.get('WASTER_LOGGING_CONFIG_FILE')

    if config_file is not None and not os.path.isfile(config_file):
        raise FileNotFoundError(f'"{config_file}" is not a file')

    elif config_file is None and os.path.isfile(LOGGING_CFG_DEFAULT):
        return LOGGING_CFG_DEFAULT

    return config_file
