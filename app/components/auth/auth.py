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
import werkzeug.exceptions
from flask import current_app

########################################################################################################################
# BLUEPRINT ############################################################################################################
########################################################################################################################
bpAuth = flask.Blueprint('auth', __name__)


########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpAuth.route('/login')
def login():
    try:
        # redirect to the auth provider
        redirect_uri = flask.url_for('auth.callback', _external=True)
        return getattr(flask.current_app.auth, current_app.config.get('AUTH_NAME')).authorize_redirect(redirect_uri)
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError('Unable to login!') from e

@bpAuth.route('/callback')
def callback():
    try:
        # handle the callback from the auth provider and store the user token in the session variable
        flask.session['user'] = flask.current_app.auth.zitadel.authorize_access_token()
        return flask.redirect(flask.url_for('main.index'))
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError('Unable to authorize!') from e

@bpAuth.route('/logout')
def logout():
    try:
        # delete the session variable
        flask.session.pop('user', None)
        return flask.redirect('/')
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError('Unable to logout!') from e