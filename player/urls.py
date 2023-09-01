from django.urls import path
from .views import (
    RegisterView,
    Login,
    Logout,
    Update,
    UnregisterUserView,
    UserListView,
    FriendListView,
    AddFriendView,
    RemoveFriendView,
    MessageListView,
    CreateRoomView,
    PasswordChangeView,
)

app_name = "player"

urlpatterns = [
    # 회원가입
    # path("register/", RegisterView, name="register"),
    path("register/", RegisterView.as_view(), name="register"),

    # 로그인
    # path('login/', Login, name='login'),
    path("login/", Login.as_view(), name="login"),

    # 로그아웃
    # path('logout/', Logout, name='logout'),
    path('logout/', Logout.as_view(), name='logout'),

    # 회원 정보수정
    # path('update/', Update, name='update'),
    path('update/', Update.as_view(), name='update'),

    # 비밀번호 수정
    path('update/ps/', PasswordChangeView.as_view(), name='pw_change'),

    # 회원 탈퇴
    # path("<str:playerId>/", 기능, name="remove"),
    path("unregister/", UnregisterUserView.as_view(), name="unregister"),

    # 전체 회원 조회
    path("search/", UserListView.as_view(), name="search"),

    # 친구 조회
    path('friends/', FriendListView.as_view(), name='friends'),

    # 친구 추가
    path('add-friend/', AddFriendView.as_view(), name='add_friend'),

    # 친구 삭제
    path('rm-friend/<int:friend_id>/', RemoveFriendView.as_view(), name='rm-friend'),

    # 채팅 목록
    path('chat-room/<int:room_id>/', MessageListView.as_view(), name="chat"),

    # 채팅방 생성
    path('chat-room/create/', CreateRoomView.as_view(), name='create_room'),
]
