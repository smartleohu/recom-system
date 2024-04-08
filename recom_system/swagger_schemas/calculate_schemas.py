from drf_yasg import openapi

calculate_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'result_id': openapi.Schema(type=openapi.TYPE_STRING),
        'user_name': openapi.Schema(type=openapi.TYPE_STRING),
    }
)
