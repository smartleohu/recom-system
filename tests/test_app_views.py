from unittest.mock import MagicMock, patch

import pytest
from django.test import RequestFactory

from recom_system.app.views import (calculate_similar_anomalies,
                                    fetch_similar_anomalies)


@pytest.fixture
def sample_request():
    factory = RequestFactory()
    return factory.post('/calculate_similar_anomalies/',
                        {'anomaly_id': 'test_anomaly',
                         'user_name': 'test_user'})


@patch('recom_system.app.views.calculate_similar_anomalies_async.delay')
def test_calculate_similar_anomalies(mock_delay, sample_request):
    mock_delay.return_value = MagicMock(id='mock_result_id')
    response = calculate_similar_anomalies(sample_request)
    assert response.status_code == 200
    assert response.data == {'result_id': 'mock_result_id',
                             'user_name': 'test_user'}


@patch('recom_system.app.views.ElasticSearchStorage.get_instance')
def test_fetch_similar_anomalies(mock_get_instance, sample_request):
    mock_instance = MagicMock()
    mock_instance.get_similarities_by_res_id.return_value = {
        'result': 'mock_result'}
    mock_get_instance.return_value = mock_instance
    sample_request.method = 'GET'
    sample_request.query_params = {'task_result_id': 'test_task_result_id',
                                   'user_name': 'test_user'}
    response = fetch_similar_anomalies(sample_request)
    assert response.status_code == 200
    assert response.data == {'search_results': {'result': 'mock_result'}}
