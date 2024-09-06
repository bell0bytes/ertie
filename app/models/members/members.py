"""
DB model for physical people / members / users

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
import sqlalchemy.orm
from typing import List
from app.factory.extensions import database, loginManager
from app.models.searchableMixin import SearchableMixin
from flask_login import UserMixin

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.members import MemberChangeLog

########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class Member(UserMixin, SearchableMixin, database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'member'

    # FULL-TEXT SEARCH #################################################################################################
    __searchable__ = ['username', 'givenName', 'familyName', 'email']

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    username: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('username',
                                                                        sqlalchemy.String(64), unique=True)
    givenName: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('given_name',
                                                                         sqlalchemy.String(64))
    familyName: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('family_name',
                                                                          sqlalchemy.String(64))
    email: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('email',
                                                                     sqlalchemy.String(128), unique=True)

    # RELATIONSHIPS ####################################################################################################
    history: sqlalchemy.orm.Mapped[List['MemberChangeLog']] = sqlalchemy.orm.relationship(back_populates='member',
                                                                                foreign_keys='MemberChangeLog.memberFK')

    # OVERRIDES ########################################################################################################
    def __repr__(self) -> str:
        return f'{self.givenName} {self.familyName}'

    def __eq__(self, other: 'Member') -> bool:
        """
        Compares two objects. Ignores the UID and SQL Alchemy state.
        Returns True if all other member variables are equal.
        """
        if self.__class__ != other.__class__:
            # different classes -> return false
            return False

        # check equality of class members
        for key, value in self.__dict__.items():
            # check each item in dictionary
            if key not in ['_sa_instance_state', 'uid', 'history']:
                if value != other.__dict__[key]:
                    return False
        return True

# PUBLIC METHODS #######################################################################################################
@loginManager.user_loader
def loadUser(userID: str) -> Member:
    # the flask login manager passes the id as a string
    return database.db.session.get(Member, int(userID))