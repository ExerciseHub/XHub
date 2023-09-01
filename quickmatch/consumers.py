import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async

# from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
# from djangochannelsrestframework.observer import model_observer
# from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin, action

from .models import MeetingMembers, MeetingMessage, MeetingRoom, User
# from .serializers import MeetingMessageSerializer, MeetingRoomSerializer
# from player.serializers import UserSerializer


class MeetingRoomConsumerTest(WebsocketConsumer):
    
    def connect(self):
        
        self.room_name = self.scope['url_route']['kwargs']['quickmatchId']
        self.room_group_name = 'chat_%s' % self.room_name
        
        # 그룹에 join
        # send 등 과 같은 동기적인 함수를 비동기적으로 사용하기 위해서는 async_to_sync 로 감싸줘야한다.
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # self.test = self.scope['url_route']['kwargs']['quickmatchId']
        # self.send(text_data=json.dumps({"message2": self.test}))
        
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # room group 에게 메세지 send
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        
        # self.send(text_data=json.dumps({"message": message}))
        
    def chat_message(self, event):
        message = event['message']
        
        # WebSocket 에게 메세지 전송
        self.send(text_data=json.dumps({
            'message': message
        }))
        

class MeetingRoomConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['quickmatchId']
        self.room_group_name = 'quickmatch_%s_chat' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 회원 멤버인지 확인
        self.members_email = await self.get_members_email()
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'room_chat_message',
                'message': message,
                'mail': self.members_email,
            }
        )

    # Receive message from room group
    async def room_chat_message(self, event):
        message = event['message']
        email = event['mail']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'email': email,
        }))
        
    @database_sync_to_async
    def get_members_email(self):
        members = MeetingMembers.objects.filter(quickmatch=self.room_name)
        members_email = [i.attendant.email for i in members]
        return members_email
    
    @database_sync_to_async
    def save_message(self, message):
        user_email = message['email']
        user = User.objects.get(email=user_email)
        meetingid = self.scope["url_route"]["kwargs"]["quickmatchId"]
        meetingroom = MeetingRoom.objects.get(meeting=meetingid)
        MeetingMessage.objects.create(room=meetingroom, user=user, content=message)


# class MeetingRoomConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
#     queryset = MeetingRoom.objects.all()
#     serializer_class = MeetingRoomSerializer
#     lookup_field = "pk"

#     async def disconnect(self, code):
#         if hasattr(self, "room_subscribe"):
#             await self.remove_user_from_room(self.room_subscribe)
#             await self.notify_users()
#         await super().disconnect(code)

#     @action()
#     async def join_room(self, pk, **kwargs):
#         self.room_subscribe = pk
#         await self.add_user_to_room(pk)
#         await self.notify_users()

#     @action()
#     async def leave_room(self, pk, **kwargs):
#         await self.remove_user_from_room(pk)

#     @action()
#     async def create_message(self, message, **kwargs):
#         room: MeetingRoom = await self.get_room(pk=self.room_subscribe)
#         await database_sync_to_async(MeetingMessage.objects.create)(
#             room=room,
#             user=self.scope["user"],
#             text=message
#         )

#     @action()
#     async def subscribe_to_messages_in_room(self, pk, request_id, **kwargs):
#         await self.message_activity.subscribe(room=pk, request_id=request_id)

#     @model_observer(MeetingMessage)
#     async def message_activity(
#         self,
#         message,
#         observer=None,
#         subscribing_request_ids = [],
#         **kwargs
#     ):
#         """
#         This is evaluated once for each subscribed consumer.
#         The result of `@message_activity.serializer` is provided here as the message.
#         """
#         # since we provide the request_id when subscribing we can just loop over them here.
#         for request_id in subscribing_request_ids:
#             message_body = dict(request_id=request_id)
#             message_body.update(message)
#             await self.send_json(message_body)

#     @message_activity.groups_for_signal
#     def message_activity(self, instance: MeetingMessage, **kwargs):
#         yield 'room__{instance.room_id}'
#         yield f'pk__{instance.pk}'

#     @message_activity.groups_for_consumer
#     def message_activity(self, room=None, **kwargs):
#         if room is not None:
#             yield f'room__{room}'

#     @message_activity.serializer
#     def message_activity(self, instance:MeetingMessage, action, **kwargs):
#         """
#         This is evaluated before the update is sent
#         out to all the subscribing consumers.
#         """
#         return dict(data=MeetingMessageSerializer(instance).data, action=action.value, pk=instance.pk)

#     async def notify_users(self):
#         room: MeetingRoom = await self.get_room(self.room_subscribe)
#         for group in self.groups:
#             await self.channel_layer.group_send(
#                 group,
#                 {
#                     'type':'update_users',
#                     'usuarios':await self.current_users(room)
#                 }
#             )

#     async def update_users(self, event: dict):
#         await self.send(text_data=json.dumps({'usuarios': event["usuarios"]}))

#     @database_sync_to_async
#     def get_room(self, pk: int) -> MeetingRoom:
#         return MeetingRoom.objects.get(pk=pk)

#     @database_sync_to_async
#     def current_users(self, room: MeetingRoom):
#         return [UserSerializer(user).data for user in room.current_users.all()]

#     @database_sync_to_async
#     def remove_user_from_room(self, room):
#         user: User = self.scope["user"]
#         user.current_rooms.remove(room)

#     @database_sync_to_async
#     def add_user_to_room(self, pk):
#         user: User = self.scope["user"]
#         if not user.current_rooms.filter(pk=self.room_subscribe).exists():
#             user.current_rooms.add(MeetingRoom.objects.get(pk=pk))
