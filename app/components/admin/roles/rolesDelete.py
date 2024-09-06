"""
Route to delete a security role.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
import flask
import werkzeug.exceptions
from app.factory.extensions import database
from app.components.admin import bpAdmin
from app.models.members import Role

########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpAdmin.route('/roles/delete/<objectID>', methods=['GET', 'POST'])
def roleDelete(objectID):
    try:
        # get the referrer
        if flask.request.method == 'GET':
            flask.session['referrer'] = flask.request.referrer

        role = database.db.session.get(Role, objectID)
        if role is None:
            flask.flash(f'Warning: Role {objectID} not found!', 'warning')
            return flask.redirect(flask.session['referrer'])

        # do not delete roles with associated users

        # delete the object
        database.deleteObject(role)

        return flask.redirect(flask.session['referrer'])
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError('Unable to delete asset type!') from e