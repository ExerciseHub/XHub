from django.urls import path
from .views import RegisterView

app_name = "player"

urlpatterns = [
    # 회원가입
    path("register/", RegisterView.as_view(), name="register"),

    # 로그인
    # path("login/", 기능, name="login"),

    # 로그아웃
    # path("logout/", 기능, name="logout"),

    # 회원 정보수정
    # path("update/", 기능, name="update"),

    # 회원 탈퇴
    # path("<str:playerId>/", 기능, name="remove"),

    # 회원 조회
    # path("search/<str:playerId>/", 기능, name="search"),
]
