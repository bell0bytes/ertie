"""
The Logger class encapsulates the logging functionality.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
import logging
import logging.handlers
import pathlib
from app.factory.conf import Config


########################################################################################################################
# LOGGING CLASS ########################################################################################################
########################################################################################################################
class Logger:
    def __init__(self) -> None:
        self._fileLogger = _createRotatingFileHandler()
        self._dbLogger = _createDBLogger()

    ####################################################################################################################
    # PUBLIC METHODS ###################################################################################################
    ####################################################################################################################
    def info(self, msg: str) -> None:
        self._fileLogger.info(msg)

    def debug(self, msg: str) -> None:
        self._fileLogger.debug(msg)

    def error(self, msg: str) -> None:
        self._fileLogger.error(msg)

    def critical(self, msg: str) -> None:
        self._fileLogger.critical(msg)

    ####################################################################################################################
    # GETTERS ##########################################################################################################
    ####################################################################################################################
    @property
    def fileLogger(self) -> logging.Logger:
        return self._fileLogger

    @property
    def dbLogger(self) -> logging.Logger:
        return self._dbLogger


########################################################################################################################
# HELPERS ##############################################################################################################
########################################################################################################################
def _createRotatingFileHandler() -> logging.Logger:
    """
    Helper method to create a rotating file handler. Options are read from the configuration file.
    """
    try:
        fileHandler = _getFileHandler('ertie.log')
        if Config.DEBUG is True:
            fileHandler.setLevel(logging.DEBUG)
        else:
            fileHandler.setLevel(logging.INFO)

        fileLogger = logging.getLogger('ErtieLogger')
        fileLogger.addHandler(fileHandler)
        if Config.DEBUG is True:
            fileLogger.setLevel(logging.DEBUG)
        else:
            fileLogger.setLevel(logging.INFO)

        # return the file logger
        return fileLogger

    except Exception as e:
        raise RuntimeError('Unable to create the File Logger!') from e


def _createDBLogger() -> logging.Logger:
    """
    Helper method to create a rotating file handler for DB queries. Options are read from the configuration file.
    """
    try:
        # define the file handler
        fileHandler = _getFileHandler('db.log')
        if Config.DEBUG is True:
            fileHandler.setLevel(logging.DEBUG)
        else:
            fileHandler.setLevel(logging.INFO)

        dbLogger = logging.getLogger('sqlalchemy.engine')
        dbLogger.addHandler(fileHandler)
        if Config.DEBUG is True:
            dbLogger.setLevel(logging.DEBUG)
        else:
            dbLogger.setLevel(logging.INFO)

        # return the file logger
        return dbLogger

    except Exception as e:
        raise RuntimeError('Unable to create the DB Logger!') from e


def _getFileHandler(logFile: str) -> logging.handlers.RotatingFileHandler:
    pathToLogsDirectory = _getLogDirectory()

    fileHandler = logging.handlers.RotatingFileHandler(f'{pathToLogsDirectory}/{logFile}',
                                                       maxBytes=Config.MAX_LOG_SIZE,
                                                       backupCount=Config.MAX_LOG_COUNT)

    fileHandler.setFormatter(logging.Formatter('{} --- {:<5s}: {}'.format('%(asctime)s',
                                                                          '%(levelname)s',
                                                                          '%(message)s'),
                                               datefmt='%A, %d/%m/%Y @ %H:%M:%S %Z %z'))

    return fileHandler


def _getLogDirectory() -> pathlib.Path:
    pathToBaseDirectory = pathlib.Path().absolute()
    pathToLogsDirectory = pathToBaseDirectory / 'logs'
    if not pathToLogsDirectory.is_dir(): # pragma: no cover
        # log directory does not exist -> create it
        pathToLogsDirectory.mkdir(parents=True, exist_ok=False)

    return pathToLogsDirectory
