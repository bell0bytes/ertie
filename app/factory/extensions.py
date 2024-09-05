"""
Extensions for Flask. The namespace serves as a singleton for extension variables.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from app.factory.conf import Config
from flask_wtf.csrf import CSRFProtect                              # CSRF protection for non FlaskForm forms
import flask_bootstrap                                              # bootstrap CSS
import flask_moment                                                 # date and time
from authlib.integrations.flask_client import OAuth                 # OAuth client for Flask
import sqlalchemy                                                   # DB agnostic SQL support
import flask_sqlalchemy                                             # Flask integration with SQLAlchemy
import flask_migrate                                                # Alembic support for DB migrations
from app.factory.classes.fullTextSearch import FullTextSearch       # FullTextSearch Wrapper

########################################################################################################################
# GLOBAL EXTENSIONS ####################################################################################################
########################################################################################################################
csrf = CSRFProtect()
bootstrap = flask_bootstrap.Bootstrap5()
moment = flask_moment.Moment()
auth = OAuth()
db = flask_sqlalchemy.SQLAlchemy(metadata=sqlalchemy.MetaData(naming_convention=Config.SQLALCHEMY_NAMING_CONVENTION,
                                                              schema=Config.SQLALCHEMY_SCHEMA),
                                 session_options={'autoflush': False})
dbMigrate = flask_migrate.Migrate()
fullTextSearch = FullTextSearch()