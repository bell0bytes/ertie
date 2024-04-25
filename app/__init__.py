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

    # DATABASE #########################################################################################################
    try:
        # initialize the database and its migration
        db = flask_sqlalchemy.SQLAlchemy(session_options={'autoflush': False})
        migrate = flask_migrate.Migrate()
        db.init_app(app)
        migrate.init_app(app, db)

        # log success
        app.logger.info('Database: Operational!')
    except Exception as e:
        _logAndRaiseException(app.logger, 'Unable to initialize the database.', e)

    # SECURITY #########################################################################################################
    try:
        # initialize the login manager
        from authlib.integrations.flask_oauth2 import ResourceProtector
        from app.components.auth import ZitadelIntrospectTokenValidator
        app.authManager = ResourceProtector()
        app.authManager.register_token_validator(ZitadelIntrospectTokenValidator(app.config))
        app.logger.info('Auth Manager: Operational!')

        # session protection
        paranoid = Paranoid(app)
        paranoid.redirect_view = '/'

    except Exception as e:
        _logAndRaiseException(app.logger, 'Unable to initialize flask extensions.', e)

    # BOOTSTRAP ########################################################################################################
    try:
        bootstrap = flask_bootstrap.Bootstrap5()  # bootstrap support
        moment = flask_moment.Moment()  # Moment support

        # initialize the bootstrap theme
        bootstrap.init_app(app)
        app.logger.info('Bootstrap: Operational!')

        # initialize the moment extension (for time and date)
        moment.init_app(app)
        app.logger.info('Moment: Operational!')

    except Exception as e:
        _logAndRaiseException(app.logger, 'Unable to initialize flask extensions.', e)

    # FULL_TEXT SEARCH #################################################################################################
    try:
        # initialize the fulltext search engine
        from app.components.search import MeiliSearch
        app.fullTextSearch = MeiliSearch(app.config)

        # log success
        app.logger.info(f'FullText Search Engine Operational: {app.fullTextSearch.name} - {app.fullTextSearch.index}!')

    except Exception as e:
        _logAndRaiseException(app.logger, 'Unable to initialise Full-Text Search capabilities.', e)

    # log success
    app.logger.info('Ertië is operational ... waking up Frodo and Gandalf ...')
    app.logger.info('Frodo and Gandalf are ready to lead your club to glory. Gl hf!\n-----\n')

    return app
