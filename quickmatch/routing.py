from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.MeetingRoomConsumer),
    path('ws/quickmatch/<int:quickmathId>/room/', consumers.MeetingRoomConsumer.as_asgi()),
    # re_path(r'^ws/quickmatch/(?P<quickmatchId>\d+)/room/$', consumers.MeetingRoomConsumer.as_asgi()),
]
