from datetime import datetime

import pytest

from recom_system.app.models import Anomaly
from recom_system.app.tasks import calculate_similar_anomalies_async


@pytest.mark.django_db
def test_calculate_similar_anomalies_async(monkeypatch):
    # Mocking the find_similar_anomalies function
    def mock_find_similar_anomalies(*args, **kwargs):
        return [{'anomaly_id': '02', 'severity': 'Medium',
                 'recommended_product': 'Product B'}]

    monkeypatch.setattr('recom_system.app.tasks.find_similar_anomalies',
                        mock_find_similar_anomalies)

    # Creating a mock Anomaly object
    mock_anomaly = Anomaly(anomaly_id='02', description='Test anomaly',
                           severity='Medium',
                           recommended_product='Product B',
                           timestamp=datetime(2022, 4, 10, 12, 0))

    # Mocking the get_anomaly method of PostgresStorage
    def mock_get_anomaly(*args, **kwargs):
        return mock_anomaly

    monkeypatch.setattr('recom_system.app.tasks.PostgresStorage.get_anomaly',
                        mock_get_anomaly)

    # Mocking the ElasticSearchStorage instance
    class MockElasticSearchStorage:
        def store_similarity(self, *args, **kwargs):
            pass

    mock_es_storage_instance = MockElasticSearchStorage()
    monkeypatch.setattr(
        'recom_system.app.tasks.ElasticSearchStorage.get_instance',
        lambda: mock_es_storage_instance)

    # Calling the function under test
    result = calculate_similar_anomalies_async(anomaly_id='01',
                                               user_name='test_user')

    # Asserting the result
    expected_result = {'user_name': 'test_user', 'anomalies': [
        {'anomaly_id': '02', 'description': 'Test anomaly',
         'severity': 'Medium', 'timestamp': '2022-04-10T12:00:00',
         'recommended_product': 'Product B', 'user_names': []}]}
    assert result == expected_result
