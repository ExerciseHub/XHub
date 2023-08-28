from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<user_id_1>\d+)/(?P<user_id_2>\d+)/$', ChatConsumer.as_asgi()),
]
