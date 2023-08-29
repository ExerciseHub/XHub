import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

## AllowedHostsOriginValidator 때문에 403 Access Denied
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

## 테스트 버전
from django.urls import path
from quickmatch import consumers

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # Just HTTP for now. (We can add other protocols later.)
})




