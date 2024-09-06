"""
Route to add a new security role.

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
import werkzeug.urls

# APPLICATION ##########################################################################################################
from app.components.admin import bpAdmin
from .methods import validateAndCommitSecurityRole

# FORMS ################################################################################################################
from app.forms.admin import FormRolesAdd

########################################################################################################################
# ROUTE ################################################################################################################
########################################################################################################################
@bpAdmin.route('/roles/add', methods=['GET', 'POST'])
def roleAdd():
    try:
        # get the referrer
        if flask.request.method == 'GET':
            flask.session['referrer'] = flask.request.referrer

        # create the form
        form = FormRolesAdd()

        if form.validate_on_submit():
            # validate and commit the new object to the DB
            if validateAndCommitSecurityRole(form):
                return flask.redirect(flask.session['referrer'])

        # show the form -> a validated form (on button click) re-enters this method with "validate_on_submit"
        return flask.render_template('admin/roles/rolesAdd.html', form=form)

    except Exception as e:
        raise werkzeug.exceptions.InternalServerError('Unable to create new asset type!') from e