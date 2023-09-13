from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Meeting, MeetingMessage, MeetingRoom, UserEvaluation

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


class MeetingChangeSerializer(serializers.ModelSerializer):
    class Meta():
        model = Meeting
        fields = ['title', 'description', 'status', 'age_limit', 'category', 'gender_limit', 'max_participants']
    
    def update(self, instance, validated_data):
        print(validated_data)
        
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.age_limit = validated_data.get('age_limit', instance.age_limit)
        instance.category = validated_data.get('category', instance.category)
        instance.gender_limit = validated_data.get('gender_limit', instance.gender_limit)
        instance.max_participants = validated_data.get('max_participants', instance.max_participants)

        instance.save()
        return instance


class MeetingMessageSerializer(serializers.ModelSerializer):
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


class UserEvaluationSerializer(serializers.ModelSerializer):
    evaluator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = UserEvaluation
        fields = ['meeting', 'evaluator', 'evaluated', 'evaluation']
