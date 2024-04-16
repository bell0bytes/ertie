########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
import flask
import werkzeug.exceptions
from app.components.errors import bpErrors


########################################################################################################################
# ERROR HANDLING #######################################################################################################
########################################################################################################################

# 404: Not Found #######################################################################################################
@bpErrors.app_errorhandler(werkzeug.exceptions.NotFound)
@bpErrors.app_errorhandler(404)
def errorHandlerNotFound(error):
    """
    On a "404: Not Found" error:
    The error is logged, and a custom 404 template is rendered with a flashed error message.

    **Template**: 404.html
    """
    if flask.current_app is not None:
        # flash and log error (request.url returns the requested URL)
        flask.current_app.exceptionFlasher(flask.request.url)       # noqa
        flask.current_app.exceptionFlasher(error)                   # noqa
        flask.current_app.exceptionLogger(flask.request.url)        # noqa

    # render 404 template
    return flask.render_template('errors/404.html'), 404


# 405: Method Not Allowed ##############################################################################################
@bpErrors.app_errorhandler(werkzeug.exceptions.MethodNotAllowed)
@bpErrors.app_errorhandler(405)
def errorHandlerMethodNotAllowed(error):
    """
    On a "405: Method Not Allowed" error, the error is logged and a custom 405 template is rendered
    with a flashed error message.

    **Template**: 405.html
    """
    if flask.current_app is not None:
        # flash and log error (request.url returns the requested URL)
        flask.current_app.exceptionFlasher(flask.request.url)   # noqa
        flask.current_app.exceptionFlasher(error)               # noqa
        flask.current_app.exceptionLogger(error)                # noqa

    # render 405 template
    return flask.render_template('errors/405.html'), 405


# 500: Internal Server Error ###########################################################################################
@bpErrors.app_errorhandler(werkzeug.exceptions.InternalServerError)
@bpErrors.app_errorhandler(500)
def errorHandlerInternalServerError(e):
    """
    On a "500: Internal Server Error" error, the error is logged and a custom 500 template
    is rendered with a flashed error message.

    **Template**: 500.html
    """
    if flask.current_app is not None:
        # flash and log message
        flask.current_app.exceptionFlasher(e)                   # noqa
        flask.current_app.exceptionLogger(e)                    # noqa

    # get original exception
    original = e.original_exception

    # render exception template
    return flask.render_template('errors/500.html', e = original), 500
