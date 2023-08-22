from rest_framework import generics, permissions
from rest_framework.generics import CreateAPIView
from .models import Post
from .serializers import PostSerializers
from rest_framework.permissions import IsAuthenticated, BasePermission

# 게시글 작성 시, 권한을 확인합니다.
# 권한이 없다면, 401 에러를 반환합니다. 권한이 있다면, 게시글을 작성합니다.

class PostCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializers


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = (IsAuthenticated,)


class IsOwner(BasePermission):
    """
    글을 작성 한, 로그인 한 해당 유저만이 글을 삭제 할 수 있도록.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.writer == request.user


class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = (IsAuthenticated, IsOwner)


