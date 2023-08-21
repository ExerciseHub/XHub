from rest_framework import serializers

from .models import Meeting, MeetingChat

class MeetingSerializer(serializers.ModelSerializer):
    class Meta():
        model = Meeting
        # TODO - 선택필요
        fields = '__all__'
    
    def create(self, validated_data):
        meeting = Meeting.objects.create(**validated_data)
        return meeting