"""
Unit tests for the auth blueprint.
Warning: this is a stub

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
from flask import session


########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################

########################################################################################################################
# TESTS ################################################################################################################
########################################################################################################################
def test_logout(testClient):
    with testClient:
        testClient.get("/logout")
        assert session.get('user') is None

def test_login(testClient):
    with testClient.application.test_request_context():
        response = testClient.get('/login')
        assert response.status_code == 302

def test_callback(testClient, mocker):
    response = testClient.get('/callback')
    assert response.status_code == 500