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
from app.factory.classes.fullTextSearch.meiliSearch import MeiliSearch
from app.factory.conf import Config

########################################################################################################################
# TESTS ################################################################################################################
########################################################################################################################
def test_get_engine():
    engine = fullTextSearch.searchEngine
    if Config.FULLTEXT_SEARCH_PROVIDER == 'meilisearch':
        assert type(engine) == type(MeiliSearch())

def test_get_url():
    assert isinstance(fullTextSearch.url, str) is True

def test_get_index():
    assert isinstance(fullTextSearch.index, str) is True

def test_add_to_index(mocker):
    mocker.patch('app.factory.classes.fullTextSearch.meiliSearch.meiliSearch.MeiliSearch.addToIndex',
                 return_value='success')
    assert fullTextSearch.addToIndex('ertie_dev', {'uid': 1}) == 'success'

def test_remove_from_index(mocker):
    mocker.patch('app.factory.classes.fullTextSearch.meiliSearch.meiliSearch.MeiliSearch.removeFromIndex',
                 return_value='success')
    assert fullTextSearch.removeFromIndex('ertie_dev', {'uid': 1}) == 'success'

def test_query_index(mocker):
    mocker.patch('app.factory.classes.fullTextSearch.meiliSearch.meiliSearch.MeiliSearch.queryIndex',
                 return_value='success')
    assert fullTextSearch.queryIndex('ertie_dev', 'search', False) == 'success'