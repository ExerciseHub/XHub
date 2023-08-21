from django.urls import path

app_name = 'board'

urlpatterns = [
    # 게시글 조회(list)
    # path('', 기능, name='list'),

    # 게시글 생성
    # path('write/', 기능, name='write'),

    # 게시글 상세보기
    # path('<int:board_id>/detail/', 기능, name='detail'),

    # 게시글 삭제
    # path('<int:board_id>/delete/', 기능, name='delete'),

    # 게시글 수정
    # path('<int:board_id>/detail/', 기능, name='update'),

    # 게시글 좋아요
    # path('<int:board_id>/like/', 기능, name='like')

    # 댓글 작성
    # path('<int:board_id>/comment/write/', 기능, name='cm-write'),

    # 댓글 삭제
    # path('<int:board_id>/<int:comment_id>/delete/', 기능, name='cm-delete'),

    # 댓글 수정
    # path('<int:board_id>/<int:comment_id>/edit', 기능, name='cm-edit'),

    # 댓글 좋아요
    # path('<int:board_id>/<int:comment_id>/like/', 기능, name='cm-like'),
]
