"""
This file handles the entire initialization of the Ertië app.
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# OPERATING SYSTEM #####################################################################################################
import os
import tempfile

# LOGGING ##############################################################################################################
import traceback                                                    # exception history handling

# FLASK ################################################################################################################
import flask
from flask_paranoid import Paranoid
import flask_sqlalchemy
import flask_migrate
import werkzeug
import werkzeug.exceptions
import flask_bootstrap
import flask_moment

# CONFIGURATION ########################################################################################################
from conf.conf import Config                                        # the configuration file

# HELPERS ##############################################################################################################
from app.helpers import Logger


########################################################################################################################
# HELPERS ##############################################################################################################
########################################################################################################################
def _printAndRaiseException(msg: str, e: Exception):
    print(msg + f'\nMessage: {e}')
    raise werkzeug.exceptions.InternalServerError(msg) from e


def _logAndRaiseException(logger, msg: str, e: Exception):
    logger.error(msg)
    logger.error(f'Message: {e}')
    raise werkzeug.exceptions.InternalServerError(msg) from e


########################################################################################################################
# MAIN APP #############################################################################################################
########################################################################################################################
def createApp(configClass=Config) -> flask.Flask:
    """
    Main entry point. Creates the Flask app.
    """
    app = None

    try:
        # create a Flask app with specified configuration
        app = flask.Flask(__name__)                 # the main application object ...
        app.config.from_object(configClass)         # ... and its configuration

    except Exception as e:
        _printAndRaiseException('Unable to initialize the Flask app!', e)

    # LOGGER ###########################################################################################################
    try:
        # create logging class
        app.logger = Logger(app.config)

        # set print startup message
        app.logger.info('Ertië is initialising ...\n-----')
        app.logger.info('Loggers: Operational!')

    except Exception as e:
        _printAndRaiseException('Unable to create loggers!', e)

    # log success
    app.logger.info('Ertië is operational ... waking up Frodo and Gandalf ...')
    app.logger.info('Frodo and Gandalf are ready to lead your club to glory. Gl hf!\n-----\n')

    return app
