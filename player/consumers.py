import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import DirectMessage, DMRoom


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Save the message
        await self.save_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.scope['user'].instance.email
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user'].instance

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))

    @sync_to_async
    def save_message(self, message):
        user = self.scope['user'].instance
        room = DMRoom.objects.get(id=self.room_name)
        DirectMessage.objects.create(user=user, room=room, content=message)
