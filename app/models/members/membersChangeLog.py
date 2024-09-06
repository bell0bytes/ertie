"""
Changelog for members

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
from datetime import datetime, timezone
import sqlalchemy.orm
from app.factory.extensions import database

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.members import Member

########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class MemberChangeLog(database.db.Model):
    # TABLE NAME #######################################################################################################
    __tablename__ = 'member_changelog'

    # DATABASE MODEL ###################################################################################################
    uid: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('uid', primary_key=True)
    memberFK: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('member_fk',
                                                                        sqlalchemy.ForeignKey('member.uid') ,index=True)
    oldUsername: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('old_username',
                                                                           sqlalchemy.String(64))
    oldGivenName: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('old_given_name',
                                                                            sqlalchemy.String(64))
    oldFamilyName: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('old_family_name',
                                                                             sqlalchemy.String(64))
    oldEmail: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('old_email', sqlalchemy.String(64))
    newUsername: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('new_username',
                                                                           sqlalchemy.String(64))
    newGivenName: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('new_given_name',
                                                                            sqlalchemy.String(64))
    newFamilyName: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('new_family_name',
                                                                             sqlalchemy.String(64))
    newEmail: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('new_email', sqlalchemy.String(64))
    when: sqlalchemy.orm.Mapped[datetime] = sqlalchemy.orm.mapped_column('when',
                                                                         default=lambda: datetime.now(timezone.utc))
    who: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('who',
                                                                   sqlalchemy.ForeignKey('member.uid'))
    why: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('why', sqlalchemy.String(4096))

    # RELATIONSHIPS ####################################################################################################
    member: sqlalchemy.orm.Mapped['Member'] = sqlalchemy.orm.relationship(back_populates='history',
                                                                          foreign_keys='MemberChangeLog.memberFK')