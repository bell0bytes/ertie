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
from app.factory.conf import Config                                        # the configuration file

########################################################################################################################
# FIXTURES #############################################################################################################
########################################################################################################################
@pytest.fixture(scope='module')
def testApp():
    # set the testing configuration prior to creating the Flask factory
    Config.DEBUG = False
    Config.TESTING = True
    testApp = createApp(configClass=Config)
    yield testApp

@pytest.fixture(scope='module')
def debugApp():
    # set the testing configuration prior to creating the Flask factory
    Config.DEBUG = True
    Config.TESTING = True
    debugApp = createApp(configClass=Config)
    yield debugApp

@pytest.fixture()
def testClient(testApp):
    # returns a test client which makes requests to the factory without running a live server
    return testApp.test_client()
