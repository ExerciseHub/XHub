from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

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
