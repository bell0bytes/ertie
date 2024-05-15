"""
This file handles the entire initialization of the Ertië app.
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# FLASK ################################################################################################################
import flask
import werkzeug.exceptions

# CONFIGURATION ########################################################################################################
from conf.conf import Config                                        # the configuration file

# LOGGING ##############################################################################################################
import traceback                                                    # exception history handling
from app.components.logging import Logger

########################################################################################################################
# GLOBALS ##############################################################################################################
########################################################################################################################
db = None
loginManager = None


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

    # ERROR HANDLING ###################################################################################################
    try:
        # define exception logger with lambda function
        app.exceptionLogger = lambda err: app.logger.error(f'{err}\n\n{traceback.format_exc()}\n-----\n')
        app.exceptionLogger.__doc__ = """Lambda function to log exceptions."""

        # define exception flasher with lambda function
        app.exceptionFlasher = lambda err: flask.flash(f'{err}', 'danger')
        app.exceptionFlasher.__doc__ = """Lambda function to flash exceptions."""

        # register the error handling blueprint, which also adds custom 404, 405 and 500 error pages
        from app.components.errors import bpErrors
        app.register_blueprint(bpErrors)

        # log success
        app.logger.info('Error Handlers: Operational!')

    except Exception as e:
        _logAndRaiseException(app.logger, 'Unable to create the error handling module!', e)

    # log success
    app.logger.info('Ertië is operational ... waking up Frodo and Gandalf ...')
    app.logger.info('Frodo and Gandalf are ready to lead your club to glory. Gl hf!\n-----\n')

    return app
