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
from wtforms import StringField, SubmitField, SelectField                           # fields
from wtforms import validators                                                      # validators

########################################################################################################################
# FORM #################################################################################################################
########################################################################################################################
class FormMembersAdd(FlaskForm):
    username = StringField('Username', validators=[validators.InputRequired(),
                                                         validators.Length(min=6, max=64),
                                                         validators.Regexp(r'^[\w.@+-]+$')])   # no white spaces
    email = StringField('E-Mail', validators=[validators.InputRequired(),
                                                    validators.Email(),
                                                    validators.Length(min=6, max=128)])
    familyName = StringField('Family Name', validators=[validators.InputRequired(),
                                                              validators.Length(min=6, max=64)])
    givenName = StringField('Family Name', validators=[validators.InputRequired(),
                                                             validators.Length(min=6, max=64)])
    nickname = StringField('Nickname', validators=[validators.Length(min=6, max=64)])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
                                         validators=[validators.InputRequired()])
    picture = StringField('Picture', validators=[validators.URL()])
    submit = SubmitField('Member Erstellen')
