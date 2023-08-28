import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
asgi_app  = get_asgi_application()

# from django_channels_jwt.middleware import JwtAuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from player.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    "http": asgi_app,
    "websocket": AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
    ),
})
