"""
Fulltext search for Ertië based on Meilisearch.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
import meilisearch


########################################################################################################################
# CLASS ################################################################################################################
########################################################################################################################
class MeiliSearch:
    def __init__(self, conf):
        self._name = 'MeiliSearch'
        self._index = conf['MEILISEARCH_INDEX']
        self._url = f'{conf["MEILISEARCH_URL"]}:{conf["MEILISEARCH_PORT"]}'
        self._apiKey = conf['MEILISEARCH_API_KEY']

        self._client = meilisearch.Client(f'{self._url}', f'{self._apiKey}')

    ####################################################################################################################
    # GETTERS ##########################################################################################################
    ####################################################################################################################
    @property
    def name(self):
        return self._name

    @property
    def index(self):
        return self._index

    @property
    def url(self):
        return self._url

    ####################################################################################################################
    # PUBLIC METHODS €##################################################################################################
    ####################################################################################################################
    def addToIndex(self, index, model):
        index = self._indexHelper(index)

        # create the document to add ; existing documents with the same ID will be updated
        document = {'id': model.uid}
        for field in model.__searchable__:
            # for each field that should be searchable, create an entry
            document[field] = getattr(model, field)

        # now add the document to the index
        self._client.index(index).update_documents([document])

    def removeFromIndex(self, index, model):
        index = self._indexHelper(index)

        # delete document with ID = model.uid
        self._client.index(index).delete_document(model.uid)

    def queryIndex(self, index, query, resync=False):
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

    def isHealthy(self):
        try:
            return True if self._client.health().get('status') == 'available' else False
        except Exception as e:
            raise RuntimeError(e)

    ####################################################################################################################
    # PRIVATE METHODS ##################################################################################################
    ####################################################################################################################
    def _indexHelper(self, index):
        # helper function to select index based on prod / dev / test ; converts indices to lower case
        pre = self._index if self._index is not None else None

        # convert index to lowercase
        index = (pre + index).lower() if pre is not None else index.lower()
        return index
