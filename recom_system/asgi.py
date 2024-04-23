import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recom_system.settings')
django_asgi_app = get_asgi_application()


async def application(scope, receive, send):
    await django_asgi_app(scope, receive, send)
