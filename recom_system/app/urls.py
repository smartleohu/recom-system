from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from recom_system.app import views
from recom_system.swagger_schemas.schema_views import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),  # Swagger UI URL
    path('calculate_similar_anomalies/',
         views.calculate_similar_anomalies,
         name='calculate_similar_anomalies'),
    path('fetch_similar_anomalies/', views.fetch_similar_anomalies,
         name='fetch_similar_anomalies'),
]

urlpatterns += staticfiles_urlpatterns()
