"""
Unit test for main blueprint.
"""
import pytest


########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################
import werkzeug.exceptions

########################################################################################################################
# TESTS ################################################################################################################
########################################################################################################################
def test_index(testClient):
    """
    GIVEN a Flask application
    WHEN the main index is requested
    THEN present the page
    """
    response = testClient.get('/')
    assert response.status_code == 200
    assert b'Ertie' in response.data