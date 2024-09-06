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

from typing import TYPE_CHECKING, Optional
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
    oldNickname: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_nickname',
                                                                           sqlalchemy.String(64))
    oldGender: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('old_gender', sqlalchemy.String(1))
    oldPicture: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('old_picture',
                                                                          sqlalchemy.String(4096))
    newUsername: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('new_username',
                                                                           sqlalchemy.String(64))
    newGivenName: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('new_given_name',
                                                                            sqlalchemy.String(64))
    newFamilyName: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('new_family_name',
                                                                             sqlalchemy.String(64))
    newEmail: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('new_email', sqlalchemy.String(64))

    newNickname: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_nickname',
                                                                           sqlalchemy.String(64))
    newGender: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('new_gender', sqlalchemy.String(1))
    newPicture: sqlalchemy.orm.Mapped[Optional[str]] = sqlalchemy.orm.mapped_column('new_picture',
                                                                          sqlalchemy.String(4096))
    when: sqlalchemy.orm.Mapped[datetime] = sqlalchemy.orm.mapped_column('when',
                                                                         default=lambda: datetime.now(timezone.utc))
    who: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column('who',
                                                                   sqlalchemy.ForeignKey('member.uid'))
    why: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column('why', sqlalchemy.String(4096))

    # RELATIONSHIPS ####################################################################################################
    member: sqlalchemy.orm.Mapped['Member'] = sqlalchemy.orm.relationship(back_populates='history',
                                                                          foreign_keys='MemberChangeLog.memberFK')