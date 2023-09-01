import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django_asgi_app = get_asgi_application()


from django.urls import re_path
from quickmatch.consumers import MeetingRoomConsumer
from player.consumers import ChatConsumer
from channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack
# from channels.security.websocket import AllowedHostsOriginValidator

application = ProtocolTypeRouter({
    "websocket": JWTAuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/chat/(?P<user_id_1>\d+)/(?P<user_id_2>\d+)/$', ChatConsumer.as_asgi()),
            re_path(r'ws/quickmatch/(?P<quickmatchId>\d+)/room/$', MeetingRoomConsumer.as_asgi()),
        ]),
    ),
})
