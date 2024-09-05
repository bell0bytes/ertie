"""
Configuration file. Reads data from a .env file in the root of the installation directory.
Serves as a singleton for global configuration variables.

WARNING: This file will be overridden when Ertië is updated, change it at your own risk.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
import os                                                                   # operating system stuff
import pathlib                                                              # paths
from dotenv import load_dotenv                                              # environment variables
from datetime import timedelta                                              # time functions

########################################################################################################################
# DIRECTORY AND FILE PATHS #############################################################################################
########################################################################################################################
pathToBaseDirectory = pathlib.Path().absolute()                             # the base directory of Ertië

########################################################################################################################
# LOAD ENVIRONMENT VARIABLES ###########################################################################################
########################################################################################################################
load_dotenv(pathToBaseDirectory.joinpath('.env'))
load_dotenv(pathToBaseDirectory.joinpath('.flaskenv'))


########################################################################################################################
# MAIN CONFIGURATION CLASS #############################################################################################
########################################################################################################################
class Config:
    # NOTE: Flask debug settings are set in ~/.profile as they need to be available before the settings file is loaded

    # FLASK OPTIONS ####################################################################################################
    FLASK_APP = os.environ.get('APP_ENV')
    FLASK_TEMPLATES_DIR = pathToBaseDirectory.joinpath("app").joinpath('templates')
    ERTIE_ENV = os.environ.get('ERTIE_ENV', 'production')
    DEBUG = True if ERTIE_ENV == 'development' else False
    TESTING = True if ERTIE_ENV == 'test' else False
    TRAP_HTTP_EXCEPTIONS = True if os.environ.get('TRAP_HTTP_EXCEPTIONS', '0') == '1' else False

    SECRET_KEY = os.environ.get('SECRET_KEY')                                   # the secret key to protect against CSRF
    if len(SECRET_KEY) < 32: # pragma: no cover
        raise RuntimeError('SECRET_KEY must be at least 32 characters long!')

    # SESSION OPTIONS ##################################################################################################
    PERMANENT_SESSION_LIFETIME = timedelta(days=int(os.environ.get('PERMANENT_SESSION_LIFETIME', '31')))
    SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME', None)
    SESSION_COOKIE_DOMAIN = os.environ.get('SESSION_COOKIE_DOMAIN', None)
    SESSION_COOKIE_PATH = os.environ.get('SESSION_COOKIE_PATH', None)
    SESSION_COOKIE_HTTPONLY = True if os.environ.get('SESSION_COOKIE_HTTPONLY', '1') == '1' else False
    SESSION_COOKIE_SECURE = True if os.environ.get('SESSION_COOKIE_SECURE', '1') == '1' else False
    SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE', None)
    SESSION_REFRESH_EACH_REQUEST = True if os.environ.get('SESSION_REFRESH_EACH_REQUEST', '1') == '1' else False
    MAX_COOKIE_SIZE = int(os.environ.get('MAX_COOKIE_SIZE', '4093'))

    # SERVER SETTINGS ##################################################################################################
    USE_X_SENDFILE = True if os.environ.get('USE_X_SENDFILE', '1') == '1' else False
    SEND_FILE_MAX_AGE_DEFAULT = None
    SERVER_NAME = os.environ.get('SERVER_NAME', None)
    APPLICATION_ROOT = os.environ.get('APPLICATION_ROOT', '/')
    PREFERRED_URL_SCHEME = os.environ.get('PREFERRED_URL_SCHEME', 'http')
    MAX_CONTENT_LENGTH = None
    TEMPLATES_AUTO_RELOAD = True if DEBUG is True else False
    EXPLAIN_TEMPLATE_LOADING = True if DEBUG is True else False

    # DATABASE SETTINGS ################################################################################################
    DB_DIALECT = os.environ.get('DB_DIALECT', 'postgresql')         # i.e. postgresql, oracle, mysql, sqlite ...
    DB_DRIVER = os.environ.get('DB_DRIVER', 'psycopg2')             # i.e. psycopg2, oracle, ...
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')                     # if no pw is set, SSL mode is assumed
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = int(os.environ.get('DB_PORT', '5432'))
    DB_DATABASE = os.environ.get('DB_DATABASE')                     # oracle -> service
    DB_SSL_CERTIFICATE_CLIENT = os.environ.get('DB_SSL_CERTIFICATE_CLIENT')         # path to the ssl certificate
    DB_SSL_CERTIFICATE_CLIENT_KEY = os.environ.get('DB_SSL_CERTIFICATE_CLIENT_KEY') # path to the ssl key
    DB_SSL_CERTIFICATE_ROOT = os.environ.get('DB_SSL_CERTIFICATE_ROOT')             # path to the root CA
    DB_SSL_MODE = os.environ.get('DB_SSL_MODE', 'verify-full')      # the SSL mose to use, i.e. verify-full

    # SQLALCHEMY SETTINGS ##############################################################################################
    SQLALCHEMY_DATABASE_URI = f'{DB_DIALECT}+{DB_DRIVER}://'
    if DB_PASSWORD != '':
        SQLALCHEMY_ENGINE_OPTIONS = {'max_identifier_length': 128,
                                     'connect_args': {
                                         'host': DB_HOST,
                                         'user': DB_USERNAME,
                                         'password': DB_PASSWORD,
                                         'port': DB_PORT,
                                         'dbname': DB_DATABASE}
                                     }
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {'max_identifier_length': 128,
                                     'connect_args': {
                                         'host': DB_HOST,
                                         'user': DB_USERNAME,
                                         'port': DB_PORT,
                                         'dbname': DB_DATABASE,
                                         'sslmode': DB_SSL_MODE,
                                         'sslcert': DB_SSL_CERTIFICATE_CLIENT,
                                         'sslkey': DB_SSL_CERTIFICATE_CLIENT_KEY,
                                         'sslrootcert': DB_SSL_CERTIFICATE_ROOT}
                                    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG
    SQLALCHEMY_NAMING_CONVENTION = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
    SQLALCHEMY_SCHEMA = 'ertie'

    # FULL-TEXT SEARCH SETTINGS ########################################################################################
    FULLTEXT_SEARCH_PROVIDER = os.environ.get('FULLTEXT_SEARCH_PROVIDER', 'meilisearch')    # the fts provider
    FULLTEXT_SEARCH_URL = os.environ.get('FULLTEXT_SEARCH_URL')
    FULLTEXT_SEARCH_INDEX = os.environ.get('FULLTEXT_SEARCH_INDEX')
    FULLTEXT_SEARCH_API_KEY = os.environ.get('FULLTEXT_SEARCH_API_KEY')

    # EMAIL SETTINGS ###################################################################################################
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # BOOTSTRAP ########################################################################################################
    BOOTSTRAP_SERVE_LOCAL = True if os.environ.get('BOOTSTRAP_SERVE_LOCAL') == '1' else False
    BOOTSTRAP_BTN_STYLE = 'primary'
    BOOTSTRAP_BTN_SITE = 'md'
    BOOTSTRAP_FORM_GROUP_CLASSES = 'mb-3'
    BOOTSTRAP_FORM_INLINE_CLASSES = 'row row-cols-lg-auto g-3 align-items-center'
    BOOTSTRAP_ICON_SIZE = 'md'
    BOOTSTRAP_ICON_COLOR = None
    BOOTSTRAP_BOOTSWATCH_THEME = os.environ.get('BOOTSTRAP_BOOTSWATCH_THEME')
    BOOTSTRAP_MSG_CATEGORY = 'primary'
    BOOTSTRAP_TABLE_VIEW_TITLE = 'View'
    BOOTSTRAP_TABLE_EDIT_TITLE = 'Edit'
    BOOTSTRAP_TABLE_DELETE_TITLE = 'Delete'
    BOOTSTRAP_TABLE_NEW_TITLE = 'New'

    # PAGINATION #######################################################################################################
    RESULTS_PER_PAGE = int(os.environ.get('RESULTS_PER_PAGE'))

    # STATIC PATHS #####################################################################################################
    STATIC_PATH = 'static'                                                  # path of static files
    AUTODOC_PATH = 'static/autodoc'                                         # autodoc files

    # LOG SETTINGS #####################################################################################################
    MAX_LOG_SIZE = int(os.environ.get('MAX_LOG_SIZE'))                      # maximal size per log file
    MAX_LOG_COUNT = int(os.environ.get('MAX_LOG_COUNT'))                    # maximal number of logs to keep in rotation

    # AUTHENTICATION ###################################################################################################
    AUTH_CLIENT_ID = os.environ.get('AUTH_CLIENT_ID', '123')
    AUTH_CLIENT_SECRET = os.environ.get('AUTH_CLIENT_SECRET', 'secret')
    AUTH_METADATA_URL = os.environ.get('AUTH_METADATA_URL', 'http://localhost:5000')
    AUTH_NAME = os.environ.get('AUTH_NAME', 'oauth')

    # CLUB SETTINGS ####################################################################################################
    CLUB_NAME = os.environ.get('CLUB_NAME', 'Best Club Ever')