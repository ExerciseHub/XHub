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
from quickmatch import consumers
from player.consumers import ChatConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        re_path(r'ws/chat/(?P<user_id_1>\d+)/(?P<user_id_2>\d+)/$', ChatConsumer.as_asgi()),
        path("ws/quickmatch/<int:quickmatchId>/room/", consumers.MeetingRoomConsumer.as_asgi()),
    ]),
})

## AuthMiddlewareStack, AllowedHostsOriginValidator 때문에 403 Access Denied
# import quickmatch.routing

# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     # Just HTTP for now. (We can add other protocols later.)
#     # WebSocket chat handler
#     "websocket": AllowedHostsOriginValidator(
#         AuthMiddlewareStack(
#             URLRouter(
#                 # path("quickmatch/<int:quickmatchId>/ws/room/", MeetingRoomConsumer.as_asgi()),
#                 quickmatch.routing.websocket_urlpatterns
#             )
#         )
#     ),
# })