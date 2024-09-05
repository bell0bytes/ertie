"""
Wrapper around MeiliSearch

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
import meilisearch
from app.factory.conf import Config

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.factory.extensions import db

########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class MeiliSearch:
    def __init__(self) -> None:
        self._index = Config.FULLTEXT_SEARCH_INDEX
        self._url = Config.FULLTEXT_SEARCH_URL
        self._apiKey = Config.FULLTEXT_SEARCH_API_KEY
        self._client = meilisearch.Client(url=self._url, api_key=self._apiKey)

    ####################################################################################################################
    # GETTERS ##########################################################################################################
    ####################################################################################################################
    @property
    def index(self) -> str:
        return self._index

    @property
    def url(self) -> str:
        return self._url

    ####################################################################################################################
    # PUBLIC METHODS €##################################################################################################
    ####################################################################################################################
    def addToIndex(self, index: str, model: 'db.Model') -> None:
        index = self._indexHelper(index)

        # create the document to add ; existing documents with the same ID will be updated
        document = {'id': model.uid}
        for field in model.__searchable__:
            # for each field that should be searchable, create an entry
            document[field] = getattr(model, field)

        # now add the document to the index
        self._client.index(index).update_documents([document])

    def removeFromIndex(self, index: str, model: 'db.Model') -> None:
        index = self._indexHelper(index)

        # delete document with ID = model.uid
        self._client.index(index).delete_document(model.uid)

    def queryIndex(self, index: str, query: str, resync:bool=False) -> tuple[list[int], int]:
        index = self._indexHelper(index)
        try:
            search = self._client.index(index).search(query)
        except Exception as e:
            raise RuntimeError(e)

        # get estimated hits
        estimatedTotalHits = search.get('estimatedTotalHits')

        # parse the output
        ids = [int(hit['id']) for hit in search['hits']] if estimatedTotalHits != 0 else []

        # return the result
        if resync is False:
            # searching -> return the ids to query from the oracle DB
            return ids, estimatedTotalHits
        else:
            # resyncing -> return the actual hits
            return search['hits'], estimatedTotalHits

    ####################################################################################################################
    # PRIVATE METHODS ##################################################################################################
    ####################################################################################################################
    def _indexHelper(self, index: str) -> str:
        # helper function to select index based on prod / dev / test ; converts indices to lower case
        pre = self._index if self._index is not None else None

        # convert index to lowercase
        index = (pre + index).lower() if pre is not None else index.lower()
        return index