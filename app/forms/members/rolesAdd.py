"""
Form to create a new member.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from flask_wtf import FlaskForm                                                     # forms
from wtforms import StringField, SubmitField                                        # fields
from wtforms import validators                                                      # validators

########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormRolesAdd(FlaskForm):
    name = StringField('Name', validators=[validators.InputRequired(),
                                                     validators.Length(min=3, max=64),
                                                     validators.Regexp(r'^[\w.@+-]+$')])   # no white spaces
    description = StringField('Description', validators=[validators.InputRequired(),
                                                    validators.Length(max=4096)])
    submit = SubmitField('Create Role')
