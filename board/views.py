from rest_framework.generics import CreateAPIView,ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Post
from .serializers import PostSerializers


# 게시글 작성 시, 권한을 확인합니다.
# 권한이 없다면, 401 에러를 반환합니다. 권한이 있다면, 게시글을 작성합니다.

class PostCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializers

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)  # 로그인 한 유저가 작성자로 저장


class PostListView(ListAPIView):
    permission_classes = [AllowAny,]
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'like']  # 어떤 필드에 대해 정렬할지 지정
    ordering = ['-created_at']  # 기본 정렬 방식은 최신 게시글


class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = [AllowAny,]
    lookup_field = 'id'  # URL에서 Post ID를 어떤 필드로 받아올지 지정


class LikePostView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        post = self.get_object()

        # 이미 좋아요를 눌렀다면, 좋아요 취소
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like -= 1
            post.save()
            return Response({"message": "좋아요 취소"}, status=status.HTTP_200_OK)
        else:
            post.likes.add(request.user)
            post.like += 1
            post.save()
            return Response({"message": "좋아요 추가"}, status=status.HTTP_200_OK)
