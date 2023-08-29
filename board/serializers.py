from rest_framework import serializers
from .models import Post, Comment


class PostSerializers(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.email')
    like = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ['id', 'gather_title', 'writer', 'context', 'img', 'like', 'public', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.email')
    like = serializers.ReadOnlyField()
    post = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'writer', 'content', 'like', 'created_at', 'updated_at']
