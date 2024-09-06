"""
Authentication module for Ertië.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# FLASK ################################################################################################################
import flask
import flask_login
import sqlalchemy.exc
import werkzeug.exceptions

# ERTIE ################################################################################################################
from app.factory.extensions import auth, database
from app.factory.conf import Config
from app.models.members import Member

########################################################################################################################
# BLUEPRINT ############################################################################################################
########################################################################################################################
bpAuth = flask.Blueprint('auth', __name__)

########################################################################################################################
# DEFINITIONS ##########################################################################################################
########################################################################################################################
mainIndex = 'main.index'

########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpAuth.route('/login')
def login():
    try:
        if flask_login.current_user.is_authenticated:
            # if the user is already logged in -> redirect to the main index page
            return flask.redirect(flask.url_for(mainIndex))

        # let the OAuth provider handle the login
        return _login()
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError('Unable to login!') from e

@bpAuth.route('/callback')
def callback():
    try:
        # handle the callback from the auth provider and store the user token in the session variable
        userInfo = _getUserInfo()

        try:
            # check if the user already exists
            user = database.db.session.execute(database.db.select(Member)
                                      .filter_by(username=userInfo.get('username'))).scalar_one()
            # log the user in and flash a welcome message
            flask_login.login_user(user, remember=True)
            flask.flash(f'Hallo, {user}', 'success')
        except sqlalchemy.exc.NoResultFound:
            # the user does not yet exist -> create it
            pass

        return flask.redirect(flask.url_for(mainIndex))
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError('Unable to authorize!') from e

@bpAuth.route('/logout')
def logout():
    try:
        _logout()
        return flask.redirect(flask.url_for(mainIndex))
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError('Unable to logout!') from e

########################################################################################################################
# HELPERS ##############################################################################################################
########################################################################################################################
def _login() -> str:
    # redirect to the auth provider
    redirect_uri = flask.url_for('auth.callback', _external=True)
    return getattr(auth, Config.AUTH_NAME).authorize_redirect(redirect_uri)

def _getUserInfo() -> dict:
    # get the user information from the access token
    return getattr(auth, Config.AUTH_NAME).authorize_access_token().get('userinfo')

def _logout() -> None:
    # pop the user from the session
    flask.session.pop('user', None)