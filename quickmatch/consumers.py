import json
import logging
import asyncio

from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import MeetingMembers, MeetingMessage, MeetingRoom
from .serializers import MeetingMessageSerializer

User = get_user_model()
logger = logging.getLogger(__name__)

class MeetingRoomConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        logger.info(f"WebSocket connection established for {self.scope['user']}")
        self.room_name = self.scope['url_route']['kwargs']['quickmatchId']
        self.room_group_name = 'quickmatch_%s_chat' % self.room_name
        # 미들웨어 이용한 user
        self.user = self.scope['user']
        self.rcc = self.scope['rcc']
        logger.info(f"WebSocket Reconnection Counter : {self.rcc}")
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        if self.rcc == '0':
            await self.change_recent_conversations(self.room_name)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'room_info_message',
                    'message' : f'{self.user} joined the chat.'
                }
            )

    async def disconnect(self, close_code):
        logger.warning(f"WebSocket connection closed for {self.scope['user']}. Close code: {close_code}")
        
        if close_code == 1006:
            await asyncio.sleep(2)  # 5초 대기
            await self.accept()  # 다시 연결 수락
        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'room_info_message',
                    'message' : f'{self.user} has left the chat.'
                }
            )
            
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_email = text_data_json['sender_email']
        # sender_id = text_data_json['sender_id']
        
        self.members_email = await self.get_members_email()
        
        if self.user.email in self.members_email:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'room_chat_message',
                    'message': message,
                    'sender_email': sender_email,
                    'room_id' : self.room_name,
                    'group_member': self.members_email,
                }
            )
        else:
            self.disconnect()

    # Receive message from room group
    async def room_chat_message(self, event):
        message = event['message']
        sender_email = event['sender_email']
        room_id = event['room_id']
        group_member = event['group_member']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'msg_type' : 'message',
            'message': message,
            'sender_email': sender_email,
            'room_id': room_id,
            'group_member': group_member
        }))
        
        # save to database
        if self.user.email == sender_email:
            await self.save_message(user=self.user.id, room_id=room_id, message=message)
    
    async def room_info_message(self, event):
        message = event['message']
        
        await self.send(text_data=json.dumps({
            'msg_type' : 'info',
            'message': message,
            'sender_email': 'system'
        }))
    
    async def change_recent_conversations(self, room_id):
        str_data = await self.load_recent_conversations(room_id)
        await self.send(text_data=str_data)
    
    @database_sync_to_async
    def get_members_email(self):
        members = MeetingMembers.objects.filter(quickmatch=self.room_name)
        members_email = [i.attendant.email for i in members]
        return members_email
    
    @database_sync_to_async
    def save_message(self, user, room_id, message):
        user = User.objects.get(id=user)
        meetingroom = MeetingRoom.objects.get(meeting=room_id)
        
        MeetingMessage.objects.create(room=meetingroom, user=user, content=message)
    
    @database_sync_to_async
    def load_recent_conversations(self, room_id):
        conversations = MeetingMessage.objects.filter(room=room_id).order_by('created_at')
        serializer = MeetingMessageSerializer(conversations, many=True)
        data = serializer.data
        
        str_data = json.dumps(data, ensure_ascii=False)
        return str_data
    
