"""
DB model for user roles (auth).

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
import sqlalchemy.orm
from app.factory.extensions import database

########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class Role(database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'role'

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('name', sqlalchemy.String(64),
                                                                    unique=True)
    description: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('description',
                                                                           sqlalchemy.String(4096), unique=True)

    # OVERRIDES ########################################################################################################
    def __repr__(self) -> str:
        return f'{self.name}'

class RoleUserMapping(database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'role_user_mapping'

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    memberFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('member_fk',
                                                                        sqlalchemy.ForeignKey('member.uid'), index=True)
    roleFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('role_fk',
                                                                        sqlalchemy.ForeignKey('role.uid'), index=True)