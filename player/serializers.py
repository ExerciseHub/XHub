from datetime import datetime

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

from .models import User, DMRoom, DirectMessage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ("email", "password", "nickname", "profile_image", "age")
        fields = ("email", "password")
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


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


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'activity_point',
            'profile_img',
            'age',
            'gender',
            'category',
            'position',
            'height',
            'weight',
            'location',
            'friend',
        ]

        read_only_fields = ('token', 'email', 'activity_point',)

        def update(self, instance, validated_data):
            password = validated_data.pop('password', None)

            for key, value in validated_data.items():
                setattr(instance, key, value)

            if password is not None:
                instance.set_password(password)

            instance.save()

            return instance
        
        def validate_current_password(self, value):
            user = self.context['request'].user
            if not check_password(value, user.password):
                raise serializers.ValidationError('현재 비밀번호가 맞지 않습니다.')
            return value


class MessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = DirectMessage
        exclude = []
        depth = 1

    def get_created_at_formatted(self, obj):
        # 만약 obj.created_at이 문자열이면 그대로 반환합니다.
        if isinstance(obj.created_at, str):
            return obj.created_at
        # 만약 obj.created_at이 datetime 객체면, 포맷에 맞게 변환해서 반환합니다.
        elif isinstance(obj.created_at, datetime):
            return obj.created_at.strftime("%Y-%m-%d %H:%M%S")
        # 그 외의 경우에는 None을 반환합니다.
        else:
            return None


class RoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    messages = MessageSerializer(read_only=True)

    class Meta:
        model = DMRoom
        fields = ["pk", "name", "host", "messages", "current_users", "last_message"]
        depth = 1
        read_only_fields = ["messages", "last_message"]

    def get_last_message(self, obj):
        return MessageSerializer(obj.messages.order_by('created_at').last()).data


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not check_password(value, self.context['request'].user.password):
            raise serializers.ValidationError('현재 비밀번호가 맞지 않습니다.')
        return value
