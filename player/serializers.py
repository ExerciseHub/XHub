from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    nickname = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('An email address is required to log in.')
        
        if password is None:
            raise serializers.ValidationError('A password is required to log in.')
        
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found')
        
        return {'email': user.email, 'user': user}
