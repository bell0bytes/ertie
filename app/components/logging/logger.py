"""
The Logger class encapsulates the logging functionality.

:Authors:
    - Gilles Bellot
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
import logging
import logging.handlers
import pathlib


########################################################################################################################
# LOGGING CLASS ########################################################################################################
########################################################################################################################
class Logger:
    def __init__(self, config):
        self._fileLogger = _createRotatingFileHandler(config)
        self._dbLogger = _createDBLogger(config)

    ####################################################################################################################
    # PUBLIC METHODS ###################################################################################################
    ####################################################################################################################
    def info(self, msg: str):
        self._fileLogger.info(msg)

    def debug(self, msg: str):
        self._fileLogger.debug(msg)

    def error(self, msg: str):
        self._fileLogger.error(msg)

    def critical(self, msg: str):
        self._fileLogger.critical(msg)

    ####################################################################################################################
    # GETTERS ##########################################################################################################
    ####################################################################################################################
    @property
    def fileLogger(self):
        return self._fileLogger

    @property
    def dbLogger(self):
        return self._dbLogger


########################################################################################################################
# HELPERS ##############################################################################################################
########################################################################################################################
def _createRotatingFileHandler(config) -> logging.Logger:
    """
    Helper method to create a rotating file handler. Options are read from the configuration file.
    """
    try:
        fileHandler = _getFileHandler('ertie.log', config)
        if config.get('DEBUG') is True:
            fileHandler.setLevel(logging.DEBUG)
        else:
            fileHandler.setLevel(logging.INFO)

        fileLogger = logging.getLogger('ErtieLogger')
        fileLogger.addHandler(fileHandler)
        if config.get('DEBUG') is True:
            fileLogger.setLevel(logging.DEBUG)
        else:
            fileLogger.setLevel(logging.INFO)

        # return the file logger
        return fileLogger

    except Exception as e: # pragma: no cover
        raise RuntimeError('Unable to create the File Logger!') from e


def _createDBLogger(config) -> logging.Logger:
    """
    Helper method to create a rotating file handler for DB queries. Options are read from the configuration file.
    """
    try:
        # define the file handler
        fileHandler = _getFileHandler('db.log', config)
        if config.get('DEBUG') is True:
            fileHandler.setLevel(logging.DEBUG)
        else:
            fileHandler.setLevel(logging.INFO)

        dbLogger = logging.getLogger('sqlalchemy.engine')
        dbLogger.addHandler(fileHandler)
        if config.get('DEBUG') is True:
            dbLogger.setLevel(logging.DEBUG)
        else:
            dbLogger.setLevel(logging.INFO)

        # return the file logger
        return dbLogger

    except Exception as e: # pragma: no cover
        raise RuntimeError('Unable to create the DB Logger!') from e


def _getFileHandler(logFile: str, config) -> logging.handlers.RotatingFileHandler:
    pathToLogsDirectory = _getLogDirectory()

    fileHandler = logging.handlers.RotatingFileHandler(f'{pathToLogsDirectory}/{logFile}',
                                                       maxBytes=config['MAX_LOG_SIZE'],
                                                       backupCount=config['MAX_LOG_COUNT'])

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
