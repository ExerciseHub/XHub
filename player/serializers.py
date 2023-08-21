from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User
from django.contrib.auth import authenticate
from .models import User


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
    password = serializers.CharField(write_only=True)

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
        ]

        read_only_fields = ('token', 'email', 'activity_poins',)

        def update(self, instance, validated_data):
            password = validated_data.pop('password', None)

            for key, value in validated_data.items():
                setattr(instance, key, value)

            if password is not None:
                instance.set_password(password)

            instance.save()

            return instance