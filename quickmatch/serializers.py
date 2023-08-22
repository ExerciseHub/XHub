from rest_framework import serializers

from .models import Meeting, MeetingChat

class MeetingSerializer(serializers.ModelSerializer):
    class Meta():
        model = Meeting
        fields = '__all__'
    
    def create(self, validated_data):
        meeting = Meeting(**validated_data)
        return meeting