"""
The Flask factory which handles the entire initialization of the Ertië app.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from typing import Type

# FLASK & EXTENSIONS ###################################################################################################
import flask
import werkzeug.exceptions
from .extensions import csrf, bootstrap, moment, auth, database, loginManager

# CONFIGURATION ########################################################################################################
from .conf import Config                                        # the configuration file

# COMPONENTS ###########################################################################################################
import traceback                                                # exception history handling
from app.components.logging import Logger                       # the logging component
from app.components.auth import bpAuth                          # the authentication component
from app.components.main import bpMain                          # the main/index component
from app.components.members import bpMembers                    # the member management component
from app.components.admin import bpAdmin                        # the administration component

########################################################################################################################
# FLASK APP FACTORY ####################################################################################################
########################################################################################################################
def createApp(configClass : Type[Config] = Config) -> flask.Flask:
    """
    Main entry point. Creates the Flask app.
    """
    app = None

    # main flask factory
    try:
        # create a Flask app with specified configuration
        app = flask.Flask(__name__, template_folder=configClass.FLASK_TEMPLATES_DIR) # the main factory object ...
        app.config.from_object(configClass)         # ... and its configuration
        csrf.init_app(app)                          # ... and the csrf protection

    except Exception as e:
        _printAndRaiseException('Unable to initialize the Flask app!', e)

    # LOGGER ###########################################################################################################
    try:
        # create logging class
        app.logger = Logger()

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
        app.logger.info('Error Handlers: Operational!\n-----')

    except Exception as e:
        _logAndRaiseException(app.logger, 'Unable to create the error handling module!', e)

    # BOOTSTRAP ########################################################################################################
    try:
        # initialize the bootstrap theme
        bootstrap.init_app(app)
        app.logger.info('Bootstrap: Operational!')

        # initialize the moment extension (for time and date)
        moment.init_app(app)
        app.logger.info('Moment: Operational!\n-----')
    except Exception as e:
        _logAndRaiseException(app.logger, 'Unable to initialize Bootstrap!', e)

    # AUTHENTICATION ###################################################################################################
    try:
        # OAUth Provider
        auth.init_app(app)
        auth.register(name=app.config.get('AUTH_NAME'),
                      client_id=app.config.get('AUTH_CLIENT_ID'),
                      client_secret=app.config.get('AUTH_CLIENT_SECRET'),
                      server_metadata_url=app.config.get('AUTH_METADATA_URL'),
                      client_kwargs= {
                          'scope': 'openid profile email',
                          'code_challenge_method': 'S256' # enable PKCE
                      }
        )
        app.logger.info('OAuth: Operational!')

        # LoginManager
        loginManager.init_app(app)
        app.logger.info('LoginManager: Operational!\n-----')
    except Exception as e:
        _logAndRaiseException(app.logger, 'Unable to initialize the Authentication module!', e)

    # DATABASE #########################################################################################################
    try:
        # initialize the database and its migration
        database.init(app)

        # log success
        app.logger.info('Database: Operational!\n-----')
    except Exception as e:
        _logAndRaiseException(app.logger, 'Unable to initialize the database.', e)

    # BLUEPRINTS #######################################################################################################
    try:
        # initialize the index / main module
        app.register_blueprint(bpMain)
        app.logger.info('Index Module: Operational!')

        # initialize the authentication module
        app.register_blueprint(bpAuth)
        app.logger.info('Authentication Module: Operational!')

        # initialize the members module
        app.register_blueprint(bpMembers)
        app.logger.info('Members Module: Operational!')

        # initialize the administration module
        app.register_blueprint(bpAdmin)
        app.logger.info('Administration Module: Operational!\n-----')
    except Exception as e:
        _logAndRaiseException(app.logger, 'Unable to initialize blueprints!.', e)

    # log success
    app.logger.info('Ertië is operational ... waking up Frodo and Gandalf ...')
    app.logger.info('Frodo and Gandalf are ready to lead your club to glory. Gl hf!\n-----\n')

    return app

########################################################################################################################
# HELPERS ######################3#######################################################################################
########################################################################################################################
def _printAndRaiseException(msg: str, e: Exception):  # pragma: no cover
    print(msg + f'\nMessage: {e}')
    raise werkzeug.exceptions.InternalServerError(msg) from e

def _logAndRaiseException(logger, msg: str, e: Exception):  # pragma: no cover
    logger.error(msg)
    logger.error(f'Exception: {e}')
    raise werkzeug.exceptions.InternalServerError(msg) from e