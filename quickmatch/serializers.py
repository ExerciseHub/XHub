from rest_framework import serializers

from .models import Meeting, MeetingMessage, MeetingRoom

class MeetingSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Meeting
        fields = '__all__'
    
    def create(self, validated_data):
        meeting = Meeting(**validated_data)
        return meeting


class MeetingChangeSerializer(serializers.ModelSerializer):
    class Meta():
        model = Meeting
        fields = ['title', 'description', 'status', 'age_limit', 'category', 'gender_limit', 'max_participants']
    
    def update(self, instance, validated_data):
        print('hi there!')
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
        depth = 1
    
    def get_create_at_formatted(self, obj):
        return obj.created_at.strftime("%d-%m-%y %H:%M:%S")
        

class MeetingRoomSerializer(serializers.ModelSerializer):
    pass