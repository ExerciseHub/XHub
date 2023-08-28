from djangochannelsrestframework import permissions
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer

from channels.db import database_sync_to_async

from . import models
from . import serializers

class ChatConsumer(GenericAsyncAPIConsumer):
    queryset = models.DirectMessage.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @action()
    async def create_room(self, name, **kwargs):
        """
        채팅방 생성
        """
        room = models.DMRoom(name=name)
        room.save()
        room.current_users.add(self.scope['user'])
        return {'room_id': room.id}, 200

    @action()
    async def join_room(self, room_id, **kwargs):
        """
        채팅방 참가 (만약 이전 대화가 있다면 대화내용 확인)
        """
        room = await database_sync_to_async(models.DMRoom.objects.get)(pk=room_id)
        room.current_users.add(self.scope['user'])
        messages = models.DirectMessage.objects.filter(room=room)
        return serializers.MessageSerializer(messages, many=True).data, 200

    @action()
    async def send_message(self, room_id, content, **kwargs):
        """
        실시간 채팅
        """
        room = await database_sync_to_async(models.DMRoom.objects.get)(pk=room_id)
        message = models.DirectMessage(room=room, sender=self.scope['user'], content=content)
        message.save()
        return serializers.MessageSerializer(message).data, 200

    @action()
    async def leave_room(self, room_id, **kwargs):
        """
        채팅방 나가기
        """
        room = await database_sync_to_async(models.DMRoom.objects.get)(pk=room_id)
        room.current_users.remove(self.scope['user'])
        return {"message": "채팅방에서 나갔습니다."}, 200
