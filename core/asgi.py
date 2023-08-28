"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
<<<<<<< HEAD
    "http": asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            player.routing.websocket_urlpatterns)
    )
=======
    "http": django_asgi_app,
    # Just HTTP for now. (We can add other protocols later.)
>>>>>>> parent of 66bd356 (1:1 실시간 채팅 설정(Daphne, nginx, docker-compose))
})
