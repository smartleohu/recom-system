import logging
import time

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from elasticsearch import NotFoundError
from rest_framework.decorators import api_view
from rest_framework.response import Response

from common.logging_util import log_event
from recom_system.app.tasks import calculate_similar_anomalies_async
from recom_system.storage.elasticsearch import ElasticSearchStorage
from recom_system.swagger_schemas.calculate_schemas import \
    calculate_response_schema
from recom_system.swagger_schemas.search_schemas import search_results_schema

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'anomaly_id': openapi.Schema(type=openapi.TYPE_STRING),
            'user_name': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={200: calculate_response_schema}
)
@api_view(['POST'])
def calculate_similar_anomalies(request):
    if request.method == 'POST':
        anomaly_id = request.data.get('anomaly_id')
        user_name = request.data.get('user_name', 'DefaultUser')
        # asynchron call
        result = calculate_similar_anomalies_async.delay(anomaly_id=anomaly_id,
                                                         user_name=user_name)
        result_id = result.id
        return Response({'result_id': result_id, 'user_name': user_name},
                        status=200)
    else:
        return Response({'error': 'Method not allowed'}, status=405)


@swagger_auto_schema(
    method='GET',
    manual_parameters=[
        openapi.Parameter('task_result_id', openapi.IN_QUERY,
                          type=openapi.TYPE_STRING),
        openapi.Parameter('user_name', openapi.IN_QUERY,
                          type=openapi.TYPE_STRING, default='DefaultUser')
    ],
    responses={200: search_results_schema}
)
@api_view(['GET'])
def fetch_similar_anomalies(request):
    if request.method == 'GET':
        retry_count = 1
        max_retry_nb = 10
        retry_interval = 20
        max_retry_time = max_retry_nb * retry_interval
        task_result_id = request.query_params.get('task_result_id')
        user_name = request.query_params.get('user_name', 'DefaultUser')
        while retry_count <= max_retry_nb:
            try:
                # Connect to Elasticsearch
                es_storage = ElasticSearchStorage.get_instance()

                # Use Celery task result id as the index name for search
                # Perform search query in Elasticsearch
                search_results = es_storage.get_similarities_by_res_id(
                    task_result_id, user_name=user_name
                )
                log_event('fetch_similar_anomalies',
                          {'search_results': search_results})

                # Pass the search_result dictionary to the template
                return Response({'search_results': search_results}, status=200)
            except NotFoundError:
                log_event(
                    'fetch_similar_anomalies',
                    {'Retry': f'{task_result_id} by {user_name} reties in '
                              f'{retry_interval}s '
                              f'[{retry_count}/{max_retry_nb}]'})
                time.sleep(retry_interval)
                retry_count += 1
        return Response({
            'search_results':
                f'{task_result_id} by {user_name} does not reply over '
                f'{max_retry_time} seconds'},
            status=408)
    else:
        return Response({'error': 'Method not allowed'}, status=405)
