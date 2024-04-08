from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Recommandation System",
        default_version='v1',
        description="it is a recommandation system against anomalies",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="ruijing.hu@ens-cachan.fr"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
