"""
This class serves as glue between the actual DB and the fulltext search engine.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
import sqlalchemy
from app.factory.extensions import fullTextSearch, database
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import flask_sqlalchemy

########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class SearchableMixin:
    @classmethod
    def search(cls, expression: str, page: int, perPage: int) -> tuple[sqlalchemy.orm.scoped_session.Scalar_Result, int]:
        # noinspection PyUnresolvedReferences
        ids, total = fullTextSearch.queryIndex(index=cls.__tablename__,
                                               query=expression, resync=False,
                                               page=page, perPage=perPage)
        if total == 0:
            return [], 0

        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))

        # noinspection PyUnresolvedReferences
        query = sqlalchemy.select(cls).where(cls.uid.in_(ids)).order_by(database.db.case(*when, value=cls.uid))
        return database.db.session.scalars(query), total

    @classmethod
    def beforeCommit(cls, session: flask_sqlalchemy.session) -> None:
        session._changes = {
            'add': [obj for obj in session.new if isinstance(obj, cls)],
            'update': [obj for obj in session.dirty if isinstance(obj, cls)],
            'delete': [obj for obj in session.deleted if isinstance(obj, cls)]}

    @classmethod
    def afterCommit(cls, session: flask_sqlalchemy.session) -> None:
        for obj in session._changes['add']:
            fullTextSearch.addToIndex(obj.__tablename__, obj)
        for obj in session._changes['update']:
            fullTextSearch.addToIndex(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            fullTextSearch.removeFromIndex(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls) -> None:
        for obj in database.db.session.scalars(sqlalchemy.select(cls)):
            # noinspection PyUnresolvedReferences
            fullTextSearch.addToIndex(cls.__tablename__, obj)

# LISTENERS ############################################################################################################
database.db.event.listen(database.db.session, 'before_commit', SearchableMixin.beforeCommit)
database.db.event.listen(database.db.session, 'after_commit', SearchableMixin.afterCommit)