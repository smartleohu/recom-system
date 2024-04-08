from drf_yasg import openapi

search_result_item_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'user_name': openapi.Schema(type=openapi.TYPE_STRING),
        'anomalies': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'anomaly_id': openapi.Schema(type=openapi.TYPE_STRING),
                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                    'severity': openapi.Schema(type=openapi.TYPE_STRING),
                    'timestamp': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_DATETIME),
                    'recommended_product': openapi.Schema(
                        type=openapi.TYPE_STRING),
                    'user_names': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'user_name': openapi.Schema(
                                    type=openapi.TYPE_STRING),
                                'role': openapi.Schema(
                                    type=openapi.TYPE_STRING),
                                'email': openapi.Schema(
                                    type=openapi.TYPE_STRING)
                            }
                        )
                    ),
                    'similarity': openapi.Schema(type=openapi.TYPE_NUMBER)
                }
            )
        )
    }
)

search_results_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'search_results': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=search_result_item_schema
        )
    }
)
