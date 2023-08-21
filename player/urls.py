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

    # 회원 탈퇴
    # path("<str:playerId>/", 기능, name="remove"),
    path("unregister/", UnregisterUserView.as_view(), name="unregister"),

    # 전체 회원 조회
    path("search/", UserListView.as_view(), name="search"),

    # 친구 조회
    path('friends/', FriendListView.as_view(), name='friends'),

    # 친구 추가
    path('add_friend/', AddFriendView.as_view(), name='add_friend'),
]
