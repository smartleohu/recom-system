from unittest.mock import MagicMock

import pytest

from recom_system.storage.elasticsearch import ElasticSearchStorage


@pytest.fixture
def mock_elasticsearch_connection(monkeypatch):
    mock_connection = MagicMock()
    monkeypatch.setattr(
        'recom_system.storage.elasticsearch.ELASTICSEARCH_CONNECTION',
        mock_connection)
    return mock_connection


def test_get_index_name():
    es_storage = ElasticSearchStorage(index_prefix='test_index')
    res_id = '123'
    expected_index_name = 'test_index_123'
    assert es_storage.get_index_name(res_id) == expected_index_name


def test_store_similarity(mock_elasticsearch_connection):
    es_storage = ElasticSearchStorage(index_prefix='test_index')
    res_id = '123'
    doc = {'user_name': 'test_user',
           'anomalies': [{'anomaly_id': '01', 'description': 'Test anomaly'}]}
    es_storage.store_similarity(res_id, doc)
    mock_elasticsearch_connection.index.assert_called_once_with(
        index='test_index_123', body=doc)


def test_get_similarities_by_res_id(mock_elasticsearch_connection):
    es_storage = ElasticSearchStorage(index_prefix='test_index')
    mock_elasticsearch_connection.search.return_value = {
        'hits': {
            'hits': [
                {'_source': {'user_name': 'test_user', 'anomalies': [
                    {'anomaly_id': '01', 'description': 'Test anomaly'}]}},
                {'_source': {'user_name': 'other_user', 'anomalies': [
                    {'anomaly_id': '02', 'description': 'Another anomaly'}]}}
            ]
        }
    }
    res_id = '123'
    user_name = 'test_user'
    expected_result = [{'user_name': 'test_user', 'anomalies': [
        {'anomaly_id': '01', 'description': 'Test anomaly'}]}]
    assert es_storage.get_similarities_by_res_id(res_id,
                                                 user_name) == expected_result


def test_clear(mock_elasticsearch_connection):
    es_storage = ElasticSearchStorage(index_prefix='test_index')
    es_storage.clear()
    mock_elasticsearch_connection.indices.delete.assert_called_once_with(
        index='_all')


def test_build():
    es_storage1 = ElasticSearchStorage.build()
    es_storage2 = ElasticSearchStorage.build()
    assert es_storage1 is es_storage2


def test_get_instance(monkeypatch):
    mock_build = MagicMock(return_value=MagicMock())
    monkeypatch.setattr(
        'recom_system.storage.elasticsearch.ElasticSearchStorage.build',
        mock_build)
    es_storage1 = ElasticSearchStorage.get_instance()
    es_storage2 = ElasticSearchStorage.get_instance()
    assert es_storage1 is es_storage2
