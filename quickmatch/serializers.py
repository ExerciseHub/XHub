from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Meeting, MeetingMessage, MeetingRoom

User = get_user_model()

class MeetingSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Meeting
        fields = '__all__'
    
    def create(self, validated_data):
        meeting = Meeting(**validated_data)
        return meeting


class MemberSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()

    position_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'nickname', 'email', 'activity_point', 'position', 'position_display']

    def get_nickname(self, obj):
        return obj.nickname or obj.email
    
    def get_position_display(self, obj):
        return obj.get_position_display()


# TODO - detail 전달될 때 전달하는 항목 지정, organizer eamil로 전달?
class MeetingDetailSerializer(serializers.ModelSerializer):
    meeting_member = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Meeting
        fields = '__all__'


class MeetingMessageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta():
        model = MeetingMessage
        fields = '__all__'


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta():
        model = MeetingRoom
        fields = '__all__'
        
    def create(self, validated_data):
        meeting_room = MeetingRoom(**validated_data)
        return meeting_room
