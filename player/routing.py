from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'player/chat-room/(?P<room_id>\d+)/$', consumers.RoomConsumer.as_asgi()),
]
