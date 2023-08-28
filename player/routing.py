from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('chat-room/create/', ChatConsumer.as_asgi()),
]
