from django.urls import path
from .views import RegisterView, UnregisterUserView
from .views import (
    RegisterView,
    Login,
    Logout,
    Update,
    UnregisterUserView,
    UserListView,
    FriendListView,
    AddFriendView
    )

app_name = "player"

urlpatterns = [
    # 회원가입
    path("register/", RegisterView, name="register"),

    # 로그인
    path('login/', Login, name='login'),

    # 로그아웃
    path('logout/', Logout, name='logout'),

    # 회원 정보수정
    path('update/', Update, name='update'),

    # 회원 탈퇴
    # path("<str:playerId>/", 기능, name="remove"),
    path("unregister/", UnregisterUserView, name="unregister"),

    # 전체 회원 조회
    path("search/", UserListView, name="search"),

    # 친구 조회
    path('friends/', FriendListView, name='friends'),

    # 친구 추가
    path('add_friend/', AddFriendView.as_view(), name='add_friend'),
]
