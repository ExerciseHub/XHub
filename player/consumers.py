import json
import redis
from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from .models import DirectMessage, DMRoom

User = get_user_model()
r = redis.StrictRedis(host='redis', port=6379, db=0)

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

        # Redis에 메시지 저장
        self.save_message_to_redis(message)
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
            'message': f"{message} check"
        }))

    @database_sync_to_async
    def store_message(self, message):
        user_id = self.scope["url_route"]["kwargs"]["user_id_1"]
        user = User.objects.get(id=user_id)
        room = DMRoom.objects.get(name=self.name, host=user)
        DirectMessage.objects.create(room=room, user=user, content=message)

    def save_message_to_redis(self, message):
        # 메시지를 직렬화하여 저장
        print(f"message: {message}")
        message_data = {
            'content': message,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        print(f"message_data: {message_data}")
        r.lpush(self.name, json.dumps(message_data).encode('utf-8'))  # 직렬화 및 인코딩
        # 최근 10개의 메시지만 저장하도록 리스트 크기를 제한
        r.ltrim(self.name, 0, 9)
