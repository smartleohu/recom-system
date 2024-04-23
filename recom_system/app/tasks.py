import logging

from celery import current_task, shared_task
from django.forms.models import model_to_dict

from recom_system.ai.recommendation_model import find_similar_anomalies
from recom_system.storage.elasticsearch import ElasticSearchStorage
from recom_system.storage.postgresql import PostgresStorage

logger = logging.getLogger(__name__)


def model_to_dict_recursive(instance, fields=None, exclude=None):
    """
    Recursively converts a model instance to a dictionary,
    including related objects.
    """
    data = model_to_dict(instance, fields=fields, exclude=exclude)
    for field_name, field_value in data.items():
        if hasattr(field_value, '__dict__'):
            # If the field is a related object
            related_instance = getattr(instance, field_name)
            data[field_name] = model_to_dict_recursive(related_instance)

        elif isinstance(field_value, list):
            # If the field is a list of related objects
            related_instance_list = getattr(instance, field_name).all()
            data[field_name] = [
                model_to_dict_recursive(related_instance)
                for related_instance in related_instance_list
            ]

    return data


@shared_task
def calculate_similar_anomalies_async(anomaly_id, user_name):
    anomalies = []
    logger.info(f'Current Task ID: {current_task.request.id}')
    for anomaly_info in find_similar_anomalies(anomaly_id):
        anomaly = PostgresStorage.get_anomaly(
            anomaly_info['anomaly_id'])
        logger.info(f'get_anomaly: {anomaly}')
        res = model_to_dict_recursive(anomaly)
        logger.info(f'model_to_dict_recursive: {res}')
        res.update(anomaly_info)
        res['timestamp'] = res['timestamp'].isoformat()
        logger.info(f'update: {res}')
        anomalies.append(res)
    # Store the similarity result in Elasticsearch
    es_storage = ElasticSearchStorage.get_instance()
    doc = {
        'user_name': user_name,
        'anomalies': anomalies,
    }
    es_storage.store_similarity(
        calculate_similar_anomalies_async.request.id, doc
    )
    return doc
