"""
SQLAlchemy Wrapper

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import flask

import sqlalchemy                                                   # DB agnostic SQL support
import flask_sqlalchemy                                             # Flask integration with SQLAlchemy
import flask_migrate                                                # Alembic support for DB migrations
from app.factory.conf import Config

########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class Database:
    def __init__(self) -> None:
        self._db = flask_sqlalchemy.SQLAlchemy(
            metadata=sqlalchemy.MetaData(naming_convention=Config.SQLALCHEMY_NAMING_CONVENTION,
                                         schema=Config.SQLALCHEMY_SCHEMA),
            session_options={'autoflush': False})
        self._migrate = flask_migrate.Migrate()

    ####################################################################################################################
    # PUBLIC METHODS €##################################################################################################
    ####################################################################################################################
    def init(self, app: 'flask.Flask') -> None:
        self._db.init_app(app)
        self._migrate.init_app(app, self._db)

    # COMMIT ###########################################################################################################
    def addCommitFlushRefresh(self, obj: flask_sqlalchemy.extension.Model) -> None:
        try:
            self._db.session.add(obj)
            self._db.session.commit()
            self._db.session.flush()
            self._db.session.refresh(obj)
        except Exception as e:
            self._rollbackAndRaise(e)

    def commitFlushRefresh(self, obj: flask_sqlalchemy.extension.Model) -> None:
        try:
            self._db.session.commit()
            self._db.session.flush()
            self._db.session.refresh(obj)
        except Exception as e:
            self._rollbackAndRaise(e)

    def commitFlush(self) -> None:
        try:
            self._db.session.commit()
            self._db.session.flush()
        except Exception as e:
            self._rollbackAndRaise(e)

    # ROLLBACK #########################################################################################################
    def rollback(self) -> None:
        self._db.session.rollback()

    # DELETE ###########################################################################################################
    def deleteObject(self, obj: flask_sqlalchemy.extension.Model) -> None:
        try:
            self._db.session.delete(obj)
            self._db.session.commit()
        except Exception as e:
            self._rollbackAndRaise(e)

    def deleteObjectAndHistory(self, obj: flask_sqlalchemy.extension.Model) -> None:
        try:
            # noinspection PyUnresolvedReferences
            for history in obj.history:
                self._db.session.delete(history)
            self.deleteObject(obj)
        except Exception as e:
            self._rollbackAndRaise(e)

    # HISTORY ##########################################################################################################
    @staticmethod
    def getListOfModificationsAsString(original: flask_sqlalchemy.extension.Model,
                                       new: flask_sqlalchemy.extension.Model) -> str:
        why = 'Modification(s): ['
        for key, value in new.__dict__.items():
            if key not in ['_sa_instance_state', 'uid', 'asset', 'categories']:
                if value != original.__dict__[key]:
                    why += f'{key}, '

        if why.endswith(', '):
            # remove trailing comma
            why = why[:-2]
        why += ']'

        return why

    ####################################################################################################################
    # GETTERS ##########################################################################################################
    ####################################################################################################################
    @property
    def db(self) -> flask_sqlalchemy.SQLAlchemy:
        return self._db

    @property
    def migrate(self) -> flask_migrate.Migrate:
        return self._migrate

    ####################################################################################################################
    # PRIVATE METHODS ##################################################################################################
    ####################################################################################################################
    def _rollbackAndRaise(self, exception: Exception):
        # rollback the session and raise a runtime exception
        self._db.session.rollback()
        raise RuntimeError from exception