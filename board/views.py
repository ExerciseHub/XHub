from rest_framework.generics import CreateAPIView
from .models import Post
from .serializers import PostSerializers
from rest_framework.permissions import IsAuthenticated


# 게시글 작성 시, 권한을 확인합니다.
# 권한이 없다면, 401 에러를 반환합니다. 권한이 있다면, 게시글을 작성합니다.

class PostCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializers
