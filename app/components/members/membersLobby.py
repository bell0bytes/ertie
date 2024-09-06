"""
The main members lobby. Shows the list of all members.

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
import werkzeug.urls
from app.components.members import bpMembers
from app.models.members import Member
import sqlalchemy
from app.factory.extensions import database

########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpMembers.route('/')
def lobby():
    try:
        # get all the members
        query = sqlalchemy.select(Member).order_by(Member.familyName.asc()).order_by(Member.givenName.asc())
        payload = {
            'members': database.db.session.scalars(query).all()
        }
        return flask.render_template('members/lobby.html', payload=payload)
    except Exception as e:
        raise werkzeug.exceptions.InternalServerError('Unable to enter the Members lobby!') from e

########################################################################################################################
# HELPERS ##############################################################################################################
########################################################################################################################
