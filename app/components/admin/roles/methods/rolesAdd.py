"""
Security Roles

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
import flask
import sqlalchemy
from app.models.members import Role
from app.forms.members import FormRolesAdd
from app.factory.extensions import database

########################################################################################################################
# METHODS ##############################################################################################################
########################################################################################################################
def validateAndCommitSecurityRole(form: FormRolesAdd) -> bool:
    # if a validated form is received, check for duplicates first
    duplicate = database.db.session.execute(database.db.select(Role)
                                   .filter(sqlalchemy.or_(Role.name == form.name.data,
                                                          Role.description == form.description.data))).first()
    if duplicate is not None:
        # the exact same object already exists -> flash a message with a URL and return False
        flask.flash('The desired security role already exists!', 'warning')
        return False

    newSecurityRole = Role(name=form.name.data, description=form.description.data)
    database.addCommitFlushRefresh(newSecurityRole)
    flask.flash(f'New Security Role: {newSecurityRole.name}', 'success')
    return True