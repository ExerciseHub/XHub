from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination

from drf_yasg.utils import swagger_auto_schema

from .models import Post, Comment
from .serializers import PostSerializers, CommentSerializer


# 게시글 작성 시, 권한을 확인합니다.
# 권한이 없다면, 401 에러를 반환합니다. 권한이 있다면, 게시글을 작성합니다.

### Post
@swagger_auto_schema(tags=["게시판"])
class PostCreateView(CreateAPIView):
    """
    게시글 작성

    - gather_title: string = 게시글 제목입니다.
    - context: string = 게시글 내용입니다.
    - public: boolean = 공개여부입니다.

    Post 객체가 생성됩니다.
    """
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializers

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)  # 로그인 한 유저가 작성자로 저장


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


@swagger_auto_schema(tags=["게시판"])
class PostListView(ListAPIView):
    """
    게시판의 모든 게시글을 봅니다.

    JSON 형식으로 모든 Post 객체를 반환합니다.
    """
    permission_classes = [AllowAny,]
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'like']
    ordering = ['-created_at']
    pagination_class = StandardResultsSetPagination


@swagger_auto_schema(tags=["게시판"])
class PostDetailView(RetrieveAPIView):
    """
    작성된 게시글의 상세페이지를 봅니다.

    - id: int = 게시글 id 값을 받습니다.

    id 값에 맞는 Post 객체를 반환합니다.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = [AllowAny]
    lookup_field = 'id'  # URL에서 Post ID를 어떤 필드로 받아올지 지정


@swagger_auto_schema(tags=["게시판"])
class LikePostView(UpdateAPIView):
    """
    작성된 게시글이 맘에 들 경우 좋아요를 합니다.

    - id: int = Post 객체의 id 값을 받습니다.

    상황에 맞는 message 값이 반환됩니다.
    """
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


@swagger_auto_schema(tags=["게시판"])
class UpdatePostView(RetrieveUpdateAPIView):
    """
    작성되어 있는 게시글을 수정합니다.

    - id: int = 수정을 원하는 Post 객체의 id 값을 받습니다.

    수정된 Post 객체를 반환합니다.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


@swagger_auto_schema(tags=["게시판"])
class IsOwner(BasePermission):
    """
    글을 작성 한, 로그인 한 해당 유저만이 글을 삭제 할 수 있도록.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.writer == request.user


@swagger_auto_schema(tags=["게시판"])
class PostDeleteView(DestroyAPIView):
    """
    작성된 게시글을 삭제합니다.

    - id: int = 삭제한 게시글의 객체 id 값을 받습니다.


    """
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = (IsAuthenticated, IsOwner)
    lookup_field = 'id'


### Comment
@swagger_auto_schema(tags=["게시판"])
class CommentWriteView(CreateAPIView):
    """
    작성된 게시글에 댓글을 답니다.

    - content: string = 댓글 내용을 입력받습니다.
    - board_id: int = 댓글을 작성할 Post 객체의 id 값을 입력받습니다.

    Comment 객체가 반환됩니다.
    """
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


@swagger_auto_schema(tags=["게시판"])
class UpdateCommmentView(RetrieveUpdateAPIView):
    """
    작성된 댓글을 수정합니다.

    - content: string = 수정할 댓글내용을 입력받습니다.
    - board_id: int = 댓글이 작성된 Post 객체의 id 값을 받습니다.
    - id: int = 수정을 원하는 Comment 객체의 id 값을 받습니다.

    수정된 Comment 객체를 반환합니다.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


@swagger_auto_schema(tags=["게시판"])
class CommentDeleteView(DestroyAPIView):
    """
    작성된 댓글을 삭제합니다.

    - board_id: int = 댓글이 작성된 Post 객체의 id 값을 입력받습니다.
    - id: int = 삭제를 원하는 Comment 객체의 id 값을 받습니다.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    lookup_field = 'id'


@swagger_auto_schema(tags=["게시판"])
class LikeCommentView(UpdateAPIView):
    """
    작성된 댓글이 맘에들 경우 좋아요를 합니다.

    - board_id: int = 댓글이 작성된 Post 객체의 id 값을 입력받습니다.
    - id: int = Post 객체의 id 값을 입력합니다.

    상황에 맞는 message 값이 반환됩니다.
    """
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


@swagger_auto_schema(tags=["게시판"])
class PostCommentsListView(ListAPIView):
    """
    특정 게시판의 모든 댓글을 확인합니다.

    - board_id: int = 모든 댓글을 확인하고 싶은 Post 객체의 id 값을 받습니다.

    특정 Post 객체의 작성된 댓글을 반환합니다.
    """
    serializer_class = CommentSerializer
    permission_classes = [AllowAny,]

    def get_queryset(self):
        board_id = self.kwargs['board_id']
        return Comment.objects.filter(post__id=board_id)
