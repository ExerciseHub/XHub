from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination

from .models import Post, Comment
from .serializers import PostSerializers, CommentSerializer

# 게시글 작성 시, 권한을 확인합니다.
# 권한이 없다면, 401 에러를 반환합니다. 권한이 있다면, 게시글을 작성합니다.

### Post
class PostCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializers

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)  # 로그인 한 유저가 작성자로 저장


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class PostListView(ListAPIView):
    permission_classes = [AllowAny,]
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'like']
    ordering = ['-created_at']
    pagination_class = StandardResultsSetPagination


class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = [AllowAny]
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


class UpdatePostView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class IsOwner(BasePermission):
    """
    글을 작성 한, 로그인 한 해당 유저만이 글을 삭제 할 수 있도록.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.writer == request.user


class PostDeleteView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = (IsAuthenticated, IsOwner)
    lookup_field = 'id'


### Comment
class CommentWriteView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs.get('board_id')  # URL에서 Post ID를 가져옴
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist."})

        serializer.save(writer=self.request.user, post=post)  # 로그인 한 유저가 작성자로 저장 + 가져온 ID에 해당하는 post에 저장


class UpdateCommmentView(RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class CommentDeleteView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    lookup_field = 'id'


class LikeCommentView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        comment = self.get_object()

        # 이미 좋아요를 눌렀다면, 좋아요 취소
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
            comment.like -= 1
            comment.save()
            return Response({"message": "좋아요 취소"}, status=status.HTTP_200_OK)
        else:
            comment.likes.add(request.user)
            comment.like += 1
            comment.save()
            return Response({"message": "좋아요 추가"}, status=status.HTTP_200_OK)


class PostCommentsListView(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny,]

    def get_queryset(self):
        board_id = self.kwargs['board_id']
        return Comment.objects.filter(post__id=board_id)
