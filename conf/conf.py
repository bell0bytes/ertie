"""
Configuration file. Reads data from a .env file in the root of the installation directory.
WARNING: This file will be overridden when Ertië is updated, change it at your own risk
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


########################################################################################################################
# MAIN CONFIGURATION CLASS #############################################################################################
########################################################################################################################
class Config(object):
    # NOTE: Flask debug settings are set in ~/.profile as they need to be available before the settings file is loaded

    # ERTIE OPTIONS ####################################################################################################
    ERTIE_ENV = os.environ.get('ERTIE_ENV')

    # FLASK OPTIONS ####################################################################################################
    DEBUG = True if ERTIE_ENV in ['development', 'test'] else False
    SECRET_KEY = os.environ.get('SECRET_KEY')                                   # the secret key to protect against CSRF
    PERMANENT_SESSION_LIFETIME = timedelta(hours=int(os.environ.get('PERMANENT_SESSION_LIFETIME')))
    REMEMBER_COOKIE_DURATION = timedelta(days=int(os.environ.get('REMEMBER_COOKIE_DURATION')))

    # SQLALCHEMY SETTINGS ##############################################################################################
    DB_DIALECT = os.environ.get('DB_DIALECT')                       # i.e. postgresql, oracle, mysql, sqlite ...
    DB_DRIVER = os.environ.get('DB_DRIVER')                         # i.e. psycopg2, oracle, ...
    DB_USERNAME = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PW')                           # if no pw is set, SSL mode is assumed
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_DATABASE = os.environ.get('DB_DATABASE')                     # oracle -> service
    DB_SSL_CERTIFICATE = os.environ.get('DB_SSL_CERT')              # path to the ssl certificate
    DB_SSL_CERTIFICATE_KEY = os.environ.get('DB_SSL_CERT_KEY')      # path to the ssl key associated with the above cert
    DB_SSL_CERTIFICATE_ROOT = os.environ.get('DB_SSL_CERT_ROOT')    # path to the root CA
    DB_SSL_MODE = os.environ.get('DB_SSL_MODE')                     # the SSL mose to use, i.e. verify-full
    DB_URL = f'{DB_DIALECT}+{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'

    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'max_identifier_length': 128}
    SQLALCHEMY_ECHO = DEBUG

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

    # MEILISEARCH ######################################################################################################
    MEILISEARCH_URL = os.environ.get('MEILISEARCH_URL')
    MEILISEARCH_PORT = os.environ.get('MEILISEARCH_PORT')
    MEILISEARCH_INDEX = os.environ.get('MEILISEARCH_INDEX')
    MEILISEARCH_API_KEY = os.environ.get('MEILISEARCH_API_KEY')

    # PAGINATION #######################################################################################################
    RESULTS_PER_PAGE = int(os.environ.get('RESULTS_PER_PAGE'))

    # STATIC PATHS #####################################################################################################
    STATIC_PATH = 'static'                                                  # path of static files
    AUTODOC_PATH = 'static/autodoc'                                         # autodoc files

    # LOG SETTINGS #####################################################################################################
    MAX_LOG_SIZE = int(os.environ.get('MAX_LOG_SIZE'))                      # maximal size per log file
    MAX_LOG_COUNT = int(os.environ.get('MAX_LOG_COUNT'))                    # maximal number of logs to keep in rotation

    # AUTHENTICATION ###################################################################################################
    ZITADEL_DOMAIN = os.environ.get('ZITADEL_DOMAIN')
    ZITADEL_CLIENT_ID = os.environ.get('ZITADEL_CLIENT_ID')
    ZITADEL_CLIENT_SECRET = os.environ.get('ZITADEL_CLIENT_SECRET')
