"""
Full-Text Search

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################
from app.factory.conf import Config

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.factory.extensions import db

########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class FullTextSearch:
    def __init__(self) -> None:
        self._engine = None
        if Config.FULLTEXT_SEARCH_PROVIDER == 'meilisearch':
            # create a meilisearch object
            from app.factory.classes.fullTextSearch.meiliSearch import MeiliSearch
            self._engine = MeiliSearch()

    ####################################################################################################################
    # GETTERS ##########################################################################################################
    ####################################################################################################################
    @property
    def searchEngine(self):
        return self._engine

    @property
    def url(self) -> str:
        return self._engine.url

    @property
    def index(self) -> str:
        return self._engine.index

    ####################################################################################################################
    # PUBLIC METHODS €##################################################################################################
    ####################################################################################################################
    def addToIndex(self, index: str, model: 'db.Model'):
        return self._engine.addToIndex(index, model)

    def removeFromIndex(self, index: str, model: 'db.Model'):
        return self._engine.removeFromIndex(index, model)

    def queryIndex(self, index: str, query: str, resync:bool=False):
        return self._engine.queryIndex(index=index, query=query, resync=resync)