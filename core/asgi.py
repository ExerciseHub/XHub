import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
asgi_app  = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter

from player.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    "http": asgi_app,
    "websocket": URLRouter(
                websocket_urlpatterns
            ),
})
