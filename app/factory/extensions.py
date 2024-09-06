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
from flask_login import LoginManager                                # the Flask LoginManager
from app.factory.classes.fullTextSearch import FullTextSearch       # FullTextSearch Wrapper
from app.factory.classes.database import Database                   # SQLAlchemy Wrapper


########################################################################################################################
# GLOBAL EXTENSIONS ####################################################################################################
########################################################################################################################
csrf = CSRFProtect()
bootstrap = flask_bootstrap.Bootstrap5()
moment = flask_moment.Moment()
auth = OAuth()
loginManager = LoginManager()
database = Database()
fullTextSearch = FullTextSearch()