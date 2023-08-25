import json
from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin, action

from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


from .models import DirectMessage, DMRoom, User
from .serializers import MessageSerializer, RoomSerializer

class RoomConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = DMRoom.objects.all()
    serializer_class = RoomSerializer
    lookup_field = "pk"

    async def connect(self):
        self.room_id = None  # 초기에는 방의 ID를 None으로 설정
        await self.accept()  # 연결 허용

    @action()
    async def create_message(self, message, **kwargs):
        if self.room_id is None:
            # 방의 ID가 설정되지 않은 경우 메시지를 반환하고 종료
            return {"error": "Room ID not set."}

        room: DMRoom = await self.get_room(pk=self.room_id)
        await database_sync_to_async(DirectMessage.objects.create)(
            room=room,
            user=self.scope["user"],
            text=message
        )

    @action()
    async def subscribe_to_messages_in_room(self, pk, request_id, **kwargs):
        self.room_id = pk  # 방의 ID를 저장
        await self.message_activity.subscribe(room=pk, request_id=request_id)

    @model_observer(DirectMessage)
    async def message_activity(
        self,
        message,
        observer=None,
        subscribing_request_ids = [],
        **kwargs
    ):
        for request_id in subscribing_request_ids:
            message_body = dict(request_id=request_id)
            message_body.update(message)
            await self.send_json(message_body)

    @message_activity.groups_for_signal
    def message_activity(self, instance: DirectMessage, **kwargs):
        yield 'room__{instance.room_id}'

    @message_activity.serializer
    def message_activity(self, instance:DirectMessage, action, **kwargs):
        return dict(data=MessageSerializer(instance).data, action=action.value, pk=instance.pk)

    @database_sync_to_async
    def get_room(self, pk: int) -> DMRoom:
        return DMRoom.objects.get(pk=pk)
