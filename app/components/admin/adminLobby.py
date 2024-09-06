########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################

# FLASK ################################################################################################################
import flask
import werkzeug.exceptions
import werkzeug.urls
import sqlalchemy

# APPLICATION ##########################################################################################################
from app.components.admin import bpAdmin
from app.factory.extensions import database

# DATABASE MODELS ######################################################################################################
from app.models.members import Role

########################################################################################################################
# ROUTING ##############################################################################################################
########################################################################################################################
@bpAdmin.route('/')
def lobby():
    """
    The main lobby for the administration module.
    """
    try:
        query = sqlalchemy.select(Role).order_by(Role.name.asc())
        payload = {
            'roles': database.db.session.scalars(query).all()
        }

        # render template
        return flask.render_template('admin/lobby.html', payload = payload)

    except Exception as e:
         raise werkzeug.exceptions.InternalServerError('Unable to enter the administration lobby!') from e