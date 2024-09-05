"""
Tests for the database / SQLAlchemy wrapper.
Warning: this is a stub

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""


########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################
import pytest
import flask_sqlalchemy.extension
import flask_migrate
from app.factory.extensions import database

########################################################################################################################
# TESTS ################################################################################################################
########################################################################################################################
def test_add_commit_flush_refresh(testClient, mocker):
    with testClient:
        mocker.patch('sqlalchemy.orm.scoping.scoped_session.add', return_value='success')
        mocker.patch('sqlalchemy.orm.scoping.scoped_session.commit', return_value='success')
        mocker.patch('sqlalchemy.orm.scoping.scoped_session.flush', return_value='success')
        mocker.patch('sqlalchemy.orm.scoping.scoped_session.refresh', return_value='success')
        assert database.addCommitFlushRefresh('test') is None

        with pytest.raises(Exception):
            mocker.patch('sqlalchemy.orm.scoping.scoped_session.add', side_effect=Exception)
            mocker.patch('sqlalchemy.orm.scoping.scoped_session.rollback', return_value='success')
            database.addCommitFlushRefresh('test')

def test_commit_flush_refresh(testClient, mocker):
    with testClient:
        mocker.patch('sqlalchemy.orm.scoping.scoped_session.commit', return_value='success')
        mocker.patch('sqlalchemy.orm.scoping.scoped_session.flush', return_value='success')
        mocker.patch('sqlalchemy.orm.scoping.scoped_session.refresh', return_value='success')
        assert database.commitFlushRefresh('test') is None

        with pytest.raises(Exception):
            mocker.patch('sqlalchemy.orm.scoping.scoped_session.refresh', side_effect=Exception)
            mocker.patch('sqlalchemy.orm.scoping.scoped_session.rollback', return_value='success')
            database.commitFlushRefresh('test')

def test_commit_flush(testClient, mocker):
    with testClient:
        mocker.patch('sqlalchemy.orm.scoping.scoped_session.commit', return_value='success')
        mocker.patch('sqlalchemy.orm.scoping.scoped_session.flush', return_value='success')
        assert database.commitFlush() is None

        with pytest.raises(Exception):
            mocker.patch('sqlalchemy.orm.scoping.scoped_session.flush', side_effect=Exception)
            mocker.patch('sqlalchemy.orm.scoping.scoped_session.rollback', return_value='success')
            database.commitFlush()

def test_rollback(testClient, mocker):
    with testClient:
        mocker.patch('sqlalchemy.orm.scoping.scoped_session.rollback', return_value='success')
        assert database.rollback() is None

        with pytest.raises(Exception):
            mocker.patch('sqlalchemy.orm.scoping.scoped_session.rollback', side_effect=Exception)
            database.rollback()

def test_delete_object(testClient, mocker):
    with testClient:
        mocker.patch('sqlalchemy.orm.scoping.scoped_session.delete', return_value='success')
        mocker.patch('sqlalchemy.orm.scoping.scoped_session.commit', return_value='success')
        assert database.deleteObject('test') is None

        with pytest.raises(Exception):
            mocker.patch('sqlalchemy.orm.scoping.scoped_session.delete', side_effect=Exception)
            mocker.patch('sqlalchemy.orm.scoping.scoped_session.rollback', return_value='success')
            database.deleteObject('test')

class ObjectWithHistory:
    def __init__(self, name:str='test'):
        self.history='test'
        self.name=name

def test_delete_object_and_history(testClient, mocker):
    with testClient:
        mocker.patch('sqlalchemy.orm.scoping.scoped_session.delete', return_value='success')
        mocker.patch('sqlalchemy.orm.scoping.scoped_session.commit', return_value='success')
        assert database.deleteObjectAndHistory(ObjectWithHistory()) is None

        with pytest.raises(Exception):
            mocker.patch('sqlalchemy.orm.scoping.scoped_session.delete', side_effect=Exception)
            mocker.patch('sqlalchemy.orm.scoping.scoped_session.rollback', return_value='success')
            database.deleteObjectAndHistory('test')

def test_modifications(testClient):
    with testClient:
        why = database.getListOfModificationsAsString(original=ObjectWithHistory('test1'),
                                                      new=ObjectWithHistory('test2'))
        assert 'name' in why

def test_get_db():
    assert isinstance(database.db, flask_sqlalchemy.SQLAlchemy)

def test_get_migrate():
    assert isinstance(database.migrate, flask_migrate.Migrate)