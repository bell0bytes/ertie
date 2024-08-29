"""
Fixtures for PyTest
"""

########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################
import os
from pickle import FALSE

import pytest
from app import createApp
from conf.conf import Config                                        # the configuration file

########################################################################################################################
# FIXTURES #############################################################################################################
########################################################################################################################
@pytest.fixture(scope='module')
def testApp():
    # set the testing configuration prior to creating the Flask application
    Config.DEBUG = False
    Config.TESTING = True
    testApp = createApp(configClass=Config)
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

@pytest.fixture()
def debugClient(debugApp):
    # returns a debug client which makes requests to the application without running a live server
    return debugApp.test_client()

@pytest.fixture()
def testRunner(testApp):
    # returns a test cli runner which runs CLI commands in isolation
    return testApp.test_cli_runner()

@pytest.fixture()
def debugRunner(debugApp):
    # returns a test cli runner which runs CLI commands in isolation
    return debugApp.test_cli_runner()