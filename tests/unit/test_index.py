"""
Unit test for main blueprint.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################
import werkzeug.exceptions

########################################################################################################################
# TESTS ################################################################################################################
########################################################################################################################
def test_index(testClient):
    """
    GIVEN a Flask factory
    WHEN the main index is requested
    THEN present the page
    """
    response = testClient.get('/')
    assert response.status_code == 200
    assert b'Ertie' in response.data