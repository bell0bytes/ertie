"""
Fixtures for PyTest

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################
import pytest
from app import createApp
from conf.conf import Config                                        # the configuration file

########################################################################################################################
# TEST CLASSES #########################################################################################################
########################################################################################################################
# mock the Auth library
class AuthFunctions:
    @staticmethod
    def authorize_redirect(url: str) -> str:
        return 'http://localhost'
    @staticmethod
    def authorize_access_token():
        return {'name': 'cosmo',
                'email': 'cosmo@best.dog'}

class AuthTest:
    def __init__(self, config):
        authFunctions = AuthFunctions()
        setattr(self, config.get('AUTH_NAME'), authFunctions)

########################################################################################################################
# FIXTURES #############################################################################################################
########################################################################################################################
@pytest.fixture(scope='module')
def testApp():
    # set the testing configuration prior to creating the Flask application
    Config.DEBUG = False
    Config.TESTING = True
    testApp = createApp(configClass=Config)
    testApp.auth = AuthTest(testApp.config)
    yield testApp

@pytest.fixture(scope='module')
def debugApp():
    # set the testing configuration prior to creating the Flask application
    Config.DEBUG = True
    Config.TESTING = True
    debugApp = createApp(configClass=Config)
    yield debugApp

@pytest.fixture()
def testClient(testApp):
    # returns a test client which makes requests to the application without running a live server
    return testApp.test_client()
