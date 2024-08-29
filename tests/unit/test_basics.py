"""
Basic unit tests for the creation of the Flask app.
"""

########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################
import logging

########################################################################################################################
# TESTS ################################################################################################################
########################################################################################################################
def test_logger_info(testApp):
    """
    GIVEN a Flask application without debugging enabled
    THEN check that the logger is able to write info, error and critical messages
    """
    _testLoggers(testApp, debug=False)

def test_logger_debug(debugApp):
    """
    GIVEN a Flask application with debugging enabled
    THEN check that the logger is able to write debug, info, error and critical messages
    """
    _testLoggers(debugApp, debug=True)

########################################################################################################################
# HELPERS ##############################################################################################################
########################################################################################################################
def _testLoggers(app, debug=False):
    # assert that the loggers exist
    dbLogger = app.logger.dbLogger
    fileLogger = app.logger.fileLogger

    assert type(dbLogger) is logging.Logger
    assert type(fileLogger) is logging.Logger

    # assert that the file logger can print to the output file
    app.logger.info('Info Test Message')
    if debug is True: app.logger.debug('Debug Test Message')
    app.logger.error('Error Test Message')
    app.logger.critical('Critical Test Message')

    with open('logs/ertie.log', 'r') as file:
        content = file.read()
        # assert that the strings printed above are actually there
        assert 'Info Test Message' in content
        if debug is True: assert 'Debug Test Message' in content
        assert 'Error Test Message' in content
        assert 'Critical Test Message' in content

    # assert that the db logger can print to the output file
    app.logger.dbLogger.info('Info Test Message')
    if debug is True: app.logger.dbLogger.debug('Debug Test Message')
    app.logger.dbLogger.error('Error Test Message')
    app.logger.dbLogger.critical('Critical Test Message')

    with open('logs/db.log', 'r') as file:
        content = file.read()
        # assert that the strings printed above are actually there
        assert 'Info Test Message' in content
        if debug is True: assert 'Debug Test Message' in content
        assert 'Error Test Message' in content
        assert 'Critical Test Message' in content