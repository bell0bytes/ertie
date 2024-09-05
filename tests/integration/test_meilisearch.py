"""
Tests for the FTS component.
Warning: this is a stub

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################
from app.factory.extensions import fullTextSearch

########################################################################################################################
# TESTS ################################################################################################################
########################################################################################################################
class TestModel:
    uid = 1
    name = 'test'
    __searchable__ = ['name']

class TestIndex:
    @classmethod
    def update_documents(cls, documents):
        return documents

    @classmethod
    def delete_document(cls, document):
        return document

    @classmethod
    def search(cls, query):
        return {'query': query,
                'estimatedHits': 1,
                'estimatedTotalHits': 1,
                'hits': [{'id': 1}]}

def test_add_to_index(mocker):
    testIndex = TestIndex()
    mocker.patch('meilisearch.client.Client.index', return_value=testIndex)
    mocker.patch('meilisearch.index.Index.update_documents', return_value='success')
    assert fullTextSearch.addToIndex('ertie_dev', TestModel()) is None

def test_remove_from_index(mocker):
    testIndex = TestIndex()
    mocker.patch('meilisearch.client.Client.index', return_value=testIndex)
    mocker.patch('meilisearch.index.Index.delete_documents', return_value='success')
    assert fullTextSearch.removeFromIndex('ertie_dev', TestModel()) is None

def test_query_index(mocker):
    testIndex = TestIndex()
    mocker.patch('meilisearch.client.Client.index', return_value=testIndex)
    mocker.patch('meilisearch.index.Index.search', return_value='success')

    ids, total = fullTextSearch.queryIndex('ertie_dev', 'test', resync=False)
    assert ids == [1]
    assert total == 1

    hits, total = fullTextSearch.queryIndex('ertie_dev', 'test', resync=True)
    assert hits == [{'id': 1}]
    assert total == 1