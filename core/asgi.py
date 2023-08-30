import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()


from django.urls import path, re_path
from quickmatch.consumers import MeetingRoomConsumer
from player.consumers import ChatConsumer
from channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack

application = ProtocolTypeRouter({
    "websocket": JWTAuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/chat/(?P<user_id_1>\d+)/(?P<user_id_2>\d+)/$', ChatConsumer.as_asgi()),
            re_path(r'ws/quickmatch/(?P<quickmatchId>\d+)/room/$', MeetingRoomConsumer.as_asgi()),
        ])
    ),
})
