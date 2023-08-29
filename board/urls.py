from django.urls import path
from .views import PostCreateView, PostListView, PostDetailView, LikePostView, PostDeleteView, UpdatePostView, CommentWriteView, UpdateCommmentView, CommentDeleteView, LikeCommentView, PostCommentsListView

app_name = 'board'

urlpatterns = [
    # 게시글 조회(list)
    path('', PostListView.as_view(), name='list'),

    # 게시글 생성
    path('write/', PostCreateView.as_view(), name='write'),

    # 게시글 상세보기
    path('<int:id>/', PostDetailView.as_view(), name='detail'),

    # 게시글 삭제
    path('<int:id>/delete/', PostDeleteView.as_view(), name='delete'),

    # 게시글 수정
    path('<int:id>/update/', UpdatePostView.as_view(), name='update'),

    # 게시글 좋아요
    path('<int:id>/like/', LikePostView.as_view(), name='like'),

    ### Comment
    # 댓글 작성
    path('<int:board_id>/comment/', CommentWriteView.as_view(), name='cm-write'),

    # 댓글 수정
    path('<int:board_id>/<int:id>/edit', UpdateCommmentView.as_view(), name='cm-edit'),

    # 댓글 삭제
    path('<int:board_id>/<int:id>/delete/', CommentDeleteView.as_view(), name='cm-delete'),

    # 댓글 좋아요
    path('<int:board_id>/<int:id>/like/', LikeCommentView.as_view(), name='cm-like'),

    # 댓글 리스트
    path('<int:board_id>/comments/', PostCommentsListView.as_view(), name="cm-list")
]
