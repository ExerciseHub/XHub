import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
asgi_app  = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import player.routing


application = ProtocolTypeRouter({
    "http": asgi_app,
    "websocket": URLRouter(player.routing.websocket_urlpatterns)
})
