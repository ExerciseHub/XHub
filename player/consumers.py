import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import DirectMessage, DMRoom
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id_1 = self.scope['url_route']['kwargs']['user_id_1']
        user_id_2 = self.scope['url_route']['kwargs']['user_id_2']

        # Ensure user_id_1 is always less than user_id_2 to create a unique name
        self.name = f"chat_{min(user_id_1, user_id_2)}_{max(user_id_1, user_id_2)}"

        await self.channel_layer.group_add(
            self.name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.store_message(message)

        await self.channel_layer.group_send(
            self.name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def store_message(self, message):
        user_id = self.scope["url_route"]["kwargs"]["user_id_1"]
        user = User.objects.get(id=user_id)
        room = DMRoom.objects.get(name=self.name, host=user)
        DirectMessage.objects.create(room=room, user=user, content=message)
